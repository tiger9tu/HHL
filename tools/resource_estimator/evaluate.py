"""Evaluate a complete configuration, including error, space, time, energy."""

import math

from .energy import power_watts
from .models import ErrorBudget, Estimate, InfeasibleConfiguration, PowerModel


def positive_integer(value, name):
    if isinstance(value, bool) or not math.isfinite(value) or value < 1 or int(value) != value:
        raise ValueError(name + " must be a positive integer")


def validate_inputs(workload, hardware, budget, power):
    positive_integer(workload.logical_qubit_count, "logical_qubit_count")
    positive_integer(workload.t_gate_count, "t_gate_count")
    if not 0 < hardware.physical_error_rate < 0.01:
        raise ValueError("physical_error_rate must be between 0 and 0.01 (model threshold)")
    if not math.isfinite(hardware.cycle_time_seconds) or hardware.cycle_time_seconds <= 0:
        raise ValueError("cycle_time_seconds must be finite and positive")
    if math.isnan(hardware.max_physical_qubits) or hardware.max_physical_qubits < 1:
        raise ValueError("max_physical_qubits must be positive (infinity is allowed)")
    if not (0 < budget.distillation < 1 and 0 < budget.surface < 1 and budget.total < 1):
        raise ValueError("Error budgets must be positive and sum to less than one")
    power_watts(0, power)


def logical_error_per_cycle(physical_error_rate, distance):
    """Circuit-level surface-code fit, Litinski Eq. (10)."""
    return 0.1 * (100 * physical_error_rate) ** ((distance + 1) / 2)


def surface_failure(physical_error_rate, tiles, time_steps, distance):
    return tiles * time_steps * distance * logical_error_per_cycle(physical_error_rate, distance)


def choose_code_distance(physical_error_rate, tiles, time_steps, error_budget,
                         max_code_distance=99):
    # Odd distances reproduce the paper's d=11/13 and d=25/27 comparisons.
    for distance in range(3, max_code_distance + 1, 2):
        if surface_failure(physical_error_rate, tiles, time_steps, distance) <= error_budget:
            return distance
    raise InfeasibleConfiguration("No odd code distance within the search limit meets the surface budget")


def evaluate_configuration(workload, hardware, protocol, data_protocol, factory_count,
                           budget=ErrorBudget(), power=PowerModel(),
                           code_distance=None, max_code_distance=99,
                           include_rejections=True, production_steps_per_state=None,
                           extra_routing_tiles=0):
    """Expected steady-state cost under the T-count-limited tile model.

    code_distance fixes d for reference configurations; otherwise it is selected
    per candidate. production_steps_per_state overrides the single-factory
    average ONLY to reproduce published rounded assumptions. Factory warm-up,
    burst scheduling, and T-depth parallelism are outside this model.
    """
    validate_inputs(workload, hardware, budget, power)
    positive_integer(factory_count, "factory_count")
    positive_integer(max_code_distance, "max_code_distance")
    if max_code_distance < 3:
        raise ValueError("max_code_distance must be at least 3")
    if (isinstance(extra_routing_tiles, bool) or not math.isfinite(extra_routing_tiles)
            or extra_routing_tiles < 0 or int(extra_routing_tiles) != extra_routing_tiles):
        raise ValueError("extra_routing_tiles must be a nonnegative integer")

    magic_error = protocol.error_rate(hardware.physical_error_rate)
    distillation_failure = workload.t_gate_count * magic_error
    if distillation_failure > budget.distillation:
        raise InfeasibleConfiguration(protocol.name + " exceeds the computation-wide distillation budget")

    production = (protocol.production_steps(hardware.physical_error_rate, include_rejections)
                  if production_steps_per_state is None else production_steps_per_state)
    if not math.isfinite(production) or production <= 0:
        raise ValueError("production_steps_per_state must be finite and positive")
    consumption = data_protocol.magic_consumption_time
    time_steps = workload.t_gate_count * max(production / factory_count, consumption)
    data_tiles = data_protocol.tiles(int(workload.logical_qubit_count))
    factory_tiles = protocol.number_of_tiles * factory_count
    storage_tiles = protocol.storage_tiles(data_protocol, factory_count)
    total_tiles = data_tiles + factory_tiles + storage_tiles + extra_routing_tiles

    if code_distance is None:
        distance = choose_code_distance(hardware.physical_error_rate, total_tiles, time_steps,
                                        budget.surface, max_code_distance)
    else:
        positive_integer(code_distance, "code_distance")
        distance = int(code_distance)
        if distance < 3 or distance % 2 != 1:
            raise ValueError("code_distance must be odd and at least 3")
    surface_error = surface_failure(hardware.physical_error_rate, total_tiles, time_steps, distance)
    if surface_error > budget.surface:
        raise InfeasibleConfiguration("Specified code distance exceeds the surface error budget")
    physical_qubits = 2 * distance ** 2 * total_tiles
    if physical_qubits > hardware.max_physical_qubits:
        raise InfeasibleConfiguration("Configuration exceeds max_physical_qubits")
    code_cycles = time_steps * distance
    runtime = code_cycles * hardware.cycle_time_seconds
    watts = power_watts(physical_qubits, power)
    return Estimate(
        protocol.name, data_protocol.name, factory_count, distance,
        data_tiles, factory_tiles, storage_tiles, extra_routing_tiles, total_tiles,
        physical_qubits, time_steps, code_cycles, runtime, watts, runtime * watts,
        magic_error, distillation_failure, surface_error,
        distillation_failure + surface_error, physical_qubits * runtime,
        production, consumption,
    )
