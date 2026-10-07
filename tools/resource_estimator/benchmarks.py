"""Reproduce four fixed configurations from arXiv:1808.02892v3, Sec. 4.

Run from the repository root: python3 -m tools.resource_estimator.benchmarks
The reference numbers are from the published tiles, distances, and rounded
production times, not from an optimizer run. Energy is our derived check.
"""

import json

from .evaluate import evaluate_configuration
from .models import Hardware, Workload
from .protocols import COMPACT, INTERMEDIATE, FAST, DISTILLATION_15_1, DISTILLATION_116_12


CASES = (
    ("Fig. 21a: compact", 1e-4, DISTILLATION_15_1, COMPACT, 1, 13, 11,
     164, 55432, 14300),
    ("Fig. 22a: intermediate", 1e-4, DISTILLATION_15_1, INTERMEDIATE, 2, 13, 11,
     226, 76388, 7150),
    ("Fig. 23a: fast", 1e-4, DISTILLATION_15_1, FAST, 11, 13, 11,
     363, 122694, 1300),
    ("Fig. 21b: compact", 1e-3, DISTILLATION_116_12, COMPACT, 1, 27, 9.27,
     210, 306180, 25029),
)


def reproduce():
    rows = []
    for name, error, protocol, data, factories, distance, production, tiles, qubits, seconds in CASES:
        result = evaluate_configuration(
            Workload(100, 10 ** 8), Hardware(error), protocol, data, factories,
            code_distance=distance, production_steps_per_state=production,
        )
        expected = {"total_tiles": tiles, "physical_qubits": qubits, "runtime_seconds": seconds}
        rows.append({"case": name, "expected": expected, "result": result._asdict(),
                     "matches": all(getattr(result, key) == value for key, value in expected.items())})
    return rows


if __name__ == "__main__":
    results = reproduce()
    print(json.dumps({"source": "https://arxiv.org/pdf/1808.02892v3",
                      "assumptions": {"logical_qubits": 100, "t_count": 10 ** 8,
                                      "cycle_time_seconds": 1e-6,
                                      "distillation_budget": 0.01, "surface_budget": 0.01,
                                      "power_watts_per_qubit": 6.25,
                                      "energy_is_derived_not_published": True},
                      "benchmarks": results}, indent=2))
    if not all(row["matches"] for row in results):
        raise SystemExit(1)
