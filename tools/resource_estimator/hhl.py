"""Original HHL scaling model, rounded up to integer logical resources."""

import math

from .evaluate import positive_integer
from .models import Workload


class Task:
    def __init__(self, logical_qubit_count, t_gate_count):
        positive_integer(logical_qubit_count, "logical_qubit_count")
        positive_integer(t_gate_count, "t_gate_count")
        self.logical_qubit_count = int(logical_qubit_count)
        self.t_gate_count = int(t_gate_count)

    def as_workload(self):
        return Workload(self.logical_qubit_count, self.t_gate_count)


class HHL(Task):
    def __init__(self, n, sparsity, kappa, epsilon, precision):
        if not math.isfinite(n) or n <= 0:
            raise ValueError("n=log2(N) must be finite and positive")
        if not math.isfinite(sparsity) or sparsity <= 0:
            raise ValueError("sparsity must be finite and positive")
        if not math.isfinite(kappa) or kappa < 1:
            raise ValueError("kappa must be finite and at least one")
        if not 0 < epsilon < 1:
            raise ValueError("epsilon must lie between zero and one")
        positive_integer(precision, "precision")
        n = int(math.ceil(n))
        hs_count = math.sqrt(320 / 3) * math.pi * kappa ** 2 * sparsity / epsilon ** 2
        t_count = math.ceil(hs_count * (18 * n + 90 * precision + 15))
        clock_qubits = math.ceil(math.log2(math.sqrt(5 / 3) * kappa / epsilon))
        super().__init__(2 * n + int(precision) + clock_qubits, t_count)
