"""Enumerate protocol/layout/factory combinations up to throughput saturation."""

import math

from .evaluate import evaluate_configuration, positive_integer, validate_inputs
from .models import ErrorBudget, InfeasibleConfiguration, PowerModel
from .protocols import DATA_PROTOCOLS, DISTILLATION_PROTOCOLS


OBJECTIVES = {
    "space_time": "space_time_qubit_seconds",
    "runtime": "runtime_seconds",
    "qubits": "physical_qubits",
    "energy": "energy_joules",
}


def optimize(workload, hardware, budget=ErrorBudget(), power=PowerModel(),
             objective="space_time", protocols=None, data_protocols=None,
             max_code_distance=99, include_rejections=True, extra_routing_tiles=0):
    """Return the best feasible configuration; raise explicitly if none exists."""
    if objective not in OBJECTIVES:
        raise ValueError("objective must be one of " + ", ".join(sorted(OBJECTIVES)))
    validate_inputs(workload, hardware, budget, power)
    positive_integer(max_code_distance, "max_code_distance")
    if max_code_distance < 3:
        raise ValueError("max_code_distance must be at least 3")
    protocols = DISTILLATION_PROTOCOLS if protocols is None else tuple(protocols)
    data_protocols = DATA_PROTOCOLS if data_protocols is None else tuple(data_protocols)
    best = None
    best_key = None
    for protocol in protocols:
        if workload.t_gate_count * protocol.error_rate(hardware.physical_error_rate) > budget.distillation:
            continue
        production = protocol.production_steps(hardware.physical_error_rate, include_rejections)
        for data in data_protocols:
            # Beyond saturation runtime cannot decrease and space/error volume
            # can only increase, including when distance is re-selected.
            saturation = int(math.ceil(production / data.magic_consumption_time))
            for factory_count in range(1, saturation + 1):
                try:
                    candidate = evaluate_configuration(
                        workload, hardware, protocol, data, factory_count,
                        budget=budget, power=power, max_code_distance=max_code_distance,
                        include_rejections=include_rejections, extra_routing_tiles=extra_routing_tiles,
                    )
                except InfeasibleConfiguration:
                    # A larger factory count can shorten execution enough to
                    # lower d and become feasible, so do not break here.
                    continue
                key = (getattr(candidate, OBJECTIVES[objective]), candidate.runtime_seconds,
                       candidate.physical_qubits, candidate.factory_count)
                if best_key is None or key < best_key:
                    best, best_key = candidate, key
    if best is None:
        raise InfeasibleConfiguration(
            "No configuration satisfies the error budgets, distance limit, and qubit limit")
    return best
