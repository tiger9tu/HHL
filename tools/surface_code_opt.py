"""Compatibility entry points for the surface-code resource estimator.

New code should use resource_estimator.optimize() and its named Estimate result.
find_optimal_setting keeps the original four-value interface, but its third
value is now actual CODE CYCLES (tile time steps multiplied by code distance).
See tools/README.md for assumptions, changes, and published benchmarks.
"""

try:  # Import from repository root or from a notebook running in tools/.
    from .resource_estimator import (
        HHL, Task, Workload, Hardware, ErrorBudget, PowerModel,
        InfeasibleConfiguration, optimize, DATA_PROTOCOLS, DISTILLATION_PROTOCOLS,
    )
except ImportError:
    from resource_estimator import (
        HHL, Task, Workload, Hardware, ErrorBudget, PowerModel,
        InfeasibleConfiguration, optimize, DATA_PROTOCOLS, DISTILLATION_PROTOCOLS,
    )

# Historical spellings and index ordering retained for the notebooks.
data_protocals = DATA_PROTOCOLS
distillation_protocals = DISTILLATION_PROTOCOLS
data_compact, data_intermediate, data_fast = data_protocals
distillation_15_1, distillation_116_12, distillation_225_1 = distillation_protocals[:3]


def _select(protocols, index, name):
    if index is None:
        return protocols
    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index < len(protocols):
        raise ValueError(name + " must be a valid protocol index or None")
    return (protocols[index],)


def estimate_resources(t_gate_count, logical_qubit_count, physical_error_rate,
                       max_physical_qubits=float("inf"),
                       specify_distillation_protocol=None, specify_data_protocol=None,
                       clock_cycle_time=1e-6, watts_per_physical_qubit=6.25,
                       fixed_watts=0.0, budget=ErrorBudget(), objective="space_time",
                       include_rejections=True):
    """Return named space/time/energy/error results for a logical workload."""
    return optimize(
        Workload(logical_qubit_count, t_gate_count),
        Hardware(physical_error_rate, clock_cycle_time, max_physical_qubits),
        budget=budget, power=PowerModel(watts_per_physical_qubit, fixed_watts),
        objective=objective, include_rejections=include_rejections,
        protocols=_select(distillation_protocals, specify_distillation_protocol,
                          "specify_distillation_protocol"),
        data_protocols=_select(data_protocals, specify_data_protocol, "specify_data_protocol"),
    )


def find_optimal_setting(t_gate_count, logical_qubit_count, physical_error_rate,
                         max_physical_qubits, specify_distillation_protocol=None,
                         specify_data_protocol=None):
    """Return (factory count, data protocol, CODE CYCLES, physical qubits).

    Infeasible inputs raise InfeasibleConfiguration instead of returning Nones.
    Low-level mutable helpers from the original script have been replaced by
    evaluate_configuration() and optimize() in the resource_estimator package.
    """
    result = estimate_resources(
        t_gate_count, logical_qubit_count, physical_error_rate, max_physical_qubits,
        specify_distillation_protocol, specify_data_protocol,
    )
    data = next(p for p in data_protocals if p.name == result.data_protocol)
    return result.factory_count, data, result.code_cycles, result.physical_qubits
