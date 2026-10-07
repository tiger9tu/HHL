"""Numerical references, independent search checks, and integration tests."""

import json
import math
from pathlib import Path
import unittest

from tools import surface_code_opt as legacy
from tools.resource_estimator import (
    Workload, Hardware, ErrorBudget, PowerModel, InfeasibleConfiguration,
    evaluate_configuration, optimize, DATA_PROTOCOLS, DISTILLATION_PROTOCOLS,
    COMPACT, INTERMEDIATE, FAST, DISTILLATION_15_1, DISTILLATION_116_12,
    DISTILLATION_225_1,
)
from tools.resource_estimator.benchmarks import reproduce


class PublishedReferences(unittest.TestCase):
    def test_all_four_published_configurations(self):
        for row in reproduce():
            with self.subTest(case=row["case"]):
                self.assertTrue(row["matches"])
                self.assertLessEqual(row["result"]["distillation_failure_bound"], 0.01)
                self.assertLessEqual(row["result"]["surface_failure_bound"], 0.01)

    def test_minimal_distances_are_selected_without_pinning(self):
        for p, factory, production, expected in [
            (1e-4, DISTILLATION_15_1, 11, 13),
            (1e-3, DISTILLATION_116_12, 9.27, 27),
        ]:
            with self.subTest(p=p):
                result = evaluate_configuration(Workload(100, 10**8), Hardware(p), factory,
                                                COMPACT, 1, production_steps_per_state=production)
                self.assertEqual(result.code_distance, expected)
                with self.assertRaises(InfeasibleConfiguration):
                    evaluate_configuration(Workload(100, 10**8), Hardware(p), factory,
                                           COMPACT, 1, code_distance=expected-2,
                                           production_steps_per_state=production)

    def test_intermediate_caption_correction_and_discrete_fast_layout(self):
        self.assertEqual(INTERMEDIATE.tiles(100), 204)
        self.assertEqual(FAST.tiles(100), 231)
        self.assertEqual(FAST.tiles(18), 49)

    def test_protocol_error_formulas(self):
        self.assertAlmostEqual(DISTILLATION_116_12.error_rate(1e-3) / 4.125e-11, 1)
        for p in [1e-3, 1e-4, 1e-5]:
            expected = 35 * (35 * p**3)**3
            self.assertAlmostEqual(DISTILLATION_225_1.error_rate(p) / expected, 1)
        self.assertEqual(DISTILLATION_225_1.production_steps(1e-3, False), 15)

    def test_reference_energy_is_derived_from_selected_qubits(self):
        first = reproduce()[0]["result"]
        self.assertEqual(first["energy_joules"], 4954235000)
        self.assertEqual(first["code_cycles"], 14300000000)
        self.assertEqual(first["time_steps"], 1100000000)


class OptimizerTests(unittest.TestCase):
    def test_full_computation_magic_state_budget(self):
        workload = Workload(100, 10**8)
        with self.assertRaises(InfeasibleConfiguration):
            evaluate_configuration(workload, Hardware(1e-3), DISTILLATION_15_1, COMPACT, 1)
        result = optimize(workload, Hardware(1e-3))
        self.assertNotEqual(result.distillation_protocol, "15-1")
        self.assertLessEqual(result.distillation_failure_bound, 0.01)

    def test_both_constraints_and_explicit_infeasibility(self):
        w = Workload(100, 10**8)
        r = optimize(w, Hardware(1e-4, max_physical_qubits=80000),
                     budget=ErrorBudget(0.005, 0.005))
        self.assertLessEqual(r.physical_qubits, 80000)
        self.assertLessEqual(r.distillation_failure_bound, 0.005)
        self.assertLessEqual(r.surface_failure_bound, 0.005)
        self.assertLessEqual(r.total_failure_bound, 0.01)
        for kwargs in [{"hardware": Hardware(1e-4, max_physical_qubits=1)},
                       {"hardware": Hardware(1e-4), "max_code_distance": 3},
                       {"hardware": Hardware(1e-4), "protocols": ()}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(InfeasibleConfiguration):
                optimize(w, **kwargs)

    def test_global_search_matches_independent_exhaustive_grid(self):
        # Intentionally search well past saturation, ALL odd distances, and
        # apply the formulas independently rather than call the evaluator.
        w = Workload(100, 10**8)
        p = 1e-3
        power = PowerModel(6.25, 1e6)
        for objective in ["runtime", "qubits", "energy", "space_time"]:
            best = float("inf")
            for protocol in DISTILLATION_PROTOCOLS:
                if w.t_gate_count * protocol.error_rate(p) > 0.01:
                    continue
                production = protocol.batch_steps / (protocol.output_states * (1-p)**protocol.rejection_exponent)
                for data in DATA_PROTOCOLS:
                    for count in range(1, 41):
                        tiles = data.tiles(100) + count*protocol.number_of_tiles + protocol.storage_tiles(data, count)
                        steps = 10**8 * max(production/count, data.magic_consumption_time)
                        for d in range(3, 40, 2):
                            surface_error = tiles * steps * d * 0.1 * (100*p)**((d+1)/2)
                            if surface_error > 0.01:
                                continue
                            qubits = 2*d*d*tiles
                            if qubits > 1100000:
                                continue
                            runtime = steps*d*1e-6
                            values = {"runtime": runtime, "qubits": qubits,
                                      "space_time": qubits*runtime,
                                      "energy": (qubits*6.25+1e6)*runtime}
                            best = min(best, values[objective])
            r = optimize(w, Hardware(p, max_physical_qubits=1100000), power=power, objective=objective)
            actual = {"runtime": r.runtime_seconds, "qubits": r.physical_qubits,
                      "space_time": r.space_time_qubit_seconds, "energy": r.energy_joules}[objective]
            self.assertAlmostEqual(actual / best, 1)

    def test_physical_time_and_power_scaling(self):
        w = Workload(100, 10**8)
        a = optimize(w, Hardware(1e-4))
        b = optimize(w, Hardware(1e-4, 2e-6), power=PowerModel(6.25, 100))
        self.assertEqual(a.physical_qubits, b.physical_qubits)
        self.assertEqual(b.runtime_seconds, 2*a.runtime_seconds)
        self.assertAlmostEqual(b.energy_joules, (a.physical_qubits*6.25+100)*b.runtime_seconds)

    def test_rejections_depend_on_error_rate(self):
        f = DISTILLATION_116_12
        self.assertGreater(f.production_steps(1e-3), f.production_steps(1e-4))
        self.assertAlmostEqual(f.production_steps(1e-3), 9.27, delta=0.01)

    def test_invalid_inputs(self):
        for workload, hardware, kwargs in [
            (Workload(0, 100), Hardware(1e-4), {}),
            (Workload(100, 0), Hardware(1e-4), {}),
            (Workload(100.5, 100), Hardware(1e-4), {}),
            (Workload(100, 100), Hardware(0.01), {}),
            (Workload(100, 100), Hardware(float("nan")), {}),
            (Workload(100, 100), Hardware(1e-4, 0), {}),
            (Workload(100, 100), Hardware(1e-4), {"objective": "unknown"}),
            (Workload(100, 100), Hardware(1e-4), {"budget": ErrorBudget(-1, 0.01)}),
            (Workload(100, 100), Hardware(1e-4), {"power": PowerModel(-1)}),
        ]:
            with self.subTest(workload=workload, hardware=hardware, kwargs=kwargs):
                with self.assertRaises(ValueError):
                    optimize(workload, hardware, **kwargs)


class IntegrationTests(unittest.TestCase):
    def test_legacy_protocol_zero_is_respected(self):
        # Automatic selection would reject 15-to-1 and select a stronger
        # protocol. Forcing index zero must instead fail its error budget.
        with self.assertRaises(InfeasibleConfiguration):
            legacy.find_optimal_setting(10**8, 100, 1e-3, float("inf"), 0)
        result = legacy.find_optimal_setting(10**8, 100, 1e-4, float("inf"), 0, 0)
        self.assertEqual(result[1], COMPACT)
        # With Compact forced, the optimizer uses two factories: consumption
        # at 9 steps/T is the bottleneck, so 9*10**8*13 microseconds.
        self.assertAlmostEqual(result[2]*1e-6, 11700)

    def test_calls_do_not_mutate_previous_results(self):
        a = legacy.estimate_resources(10**8, 100, 1e-4)
        legacy.estimate_resources(10**8, 1000, 1e-4)
        self.assertEqual(a, legacy.estimate_resources(10**8, 100, 1e-4))

    def test_hhl_adapter(self):
        task = legacy.HHL(10, 10, 10, 0.01, 5)
        expected = math.ceil(math.sqrt(320/3)*math.pi*100*10/0.01**2 * (180+450+15))
        self.assertEqual(task.t_gate_count, expected)
        self.assertEqual(task.logical_qubit_count, 36)
        self.assertEqual(task.as_workload(), Workload(36, expected))

    def test_notebook_resource_functions(self):
        # Execute just the numerical cells, without plotting or Q# imports.
        try:
            import numpy as np
        except ImportError:
            self.skipTest("NumPy is required for notebook integration")
        nb = json.loads((Path(__file__).parents[1] / "heatmap.ipynb").read_text())
        namespace = {"np": np, "sc": legacy}
        for cell in nb["cells"]:
            source = "".join(cell.get("source", []))
            if source.startswith("max_physical_qubits") or source.startswith("def calculate_q_resources") or source.startswith("def calculate_q_energy"):
                exec(compile(source, "heatmap.ipynb", "exec"), namespace)
        runtime, qubits, energy = namespace["calculate_q_resources"](10, 10, 100, np.array([2**10, 2**20]))
        np.testing.assert_allclose(energy, runtime*qubits*6.25)
        np.testing.assert_allclose(namespace["calculate_q_energy"](10, 10, 100, np.array([2**10, 2**20])), energy)
        self.assertTrue(np.all(np.isfinite(energy)))


if __name__ == "__main__":
    unittest.main()
