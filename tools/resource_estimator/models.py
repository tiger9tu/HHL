"""Immutable inputs and outputs; durations are in seconds and power in watts."""

from typing import NamedTuple


class Workload(NamedTuple):
    logical_qubit_count: int
    t_gate_count: int


class Hardware(NamedTuple):
    physical_error_rate: float
    cycle_time_seconds: float = 1e-6
    max_physical_qubits: float = float("inf")


class ErrorBudget(NamedTuple):
    # Defaults reproduce Litinski's TWO separate 1% budgets (2% combined).
    distillation: float = 0.01
    surface: float = 0.01

    @property
    def total(self):
        return self.distillation + self.surface


class PowerModel(NamedTuple):
    watts_per_physical_qubit: float = 6.25
    fixed_watts: float = 0.0


class Estimate(NamedTuple):
    distillation_protocol: str
    data_protocol: str
    factory_count: int
    code_distance: int
    data_tiles: int
    factory_tiles: int
    storage_tiles: int
    routing_tiles: int
    total_tiles: int
    physical_qubits: int
    time_steps: float
    code_cycles: float
    runtime_seconds: float
    power_watts: float
    energy_joules: float
    magic_state_error: float
    distillation_failure_bound: float
    surface_failure_bound: float
    total_failure_bound: float
    space_time_qubit_seconds: float
    production_steps_per_state: float
    consumption_steps_per_state: float


class InfeasibleConfiguration(ValueError):
    """A valid request cannot meet the specified resource/error constraints."""
