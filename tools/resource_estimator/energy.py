"""Energy for the actual selected physical configuration."""

import math


def power_watts(physical_qubits, model):
    for value in model:
        if not math.isfinite(value) or value < 0:
            raise ValueError("Power parameters must be finite and nonnegative")
    return model.fixed_watts + physical_qubits * model.watts_per_physical_qubit
