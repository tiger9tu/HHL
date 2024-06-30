import numpy as np

# Import Qiskit
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import SparsePauliOp

from qiskit.circuit.library import PauliEvolutionGate
from qiskit.circuit.library.phase_estimation import PhaseEstimation
from qiskit.circuit.library.arithmetic.exact_reciprocal import ExactReciprocal


class HHL(QuantumCircuit):
    r"""Given hermitian matrix A and statevector b,
    construct corresponding HHL algorithm's quantum circuit.

    Note: math are used to figure out some parameters,
    such as scale of controld rotation"""

    def __init__(
        self,
        matrix: np.ndarray,
        vector: np.ndarray,
        tolerance: float = 1e-2,
        name: str = "HHL",
    ) -> None:
        super().__init__(name=name)

        self.matrix = matrix
        self.vector = vector
        self.tolerance = tolerance

        self.scaling = 1
        self.neg_eigenvals = True

        self.qc_pe_ejHt = None

        # build circuit
        self._check_configuration()
        self._set_qc_param()
        self._build()

    def _check_configuration(self, raise_on_failure: bool = True) -> bool:
        """Check if the current configuration is valid."""
        valid = True
        if self.matrix.shape[0] != self.matrix.shape[1]:
            if raise_on_failure:
                raise AttributeError("Input matrix must be square!")
            return False
        if np.log2(self.matrix.shape[0]) % 1 != 0:
            if raise_on_failure:
                raise AttributeError("Input matrix dimension must be 2^n!")
            return False
        if not np.allclose(self.matrix, self.matrix.conj().T):
            if raise_on_failure:
                raise AttributeError("Input matrix must be hermitian!")
            return False

        return valid

    def _get_delta(self, n_l: int, lambda_min: float, lambda_max: float) -> float:
        """Calculates the scaling factor to represent exactly lambda_min on nl binary digits.
        Args:
            n_l: The number of qubits to represent the eigenvalues.
            lambda_min: the smallest eigenvalue.
            lambda_max: the largest eigenvalue.

        Returns:
            The value of the scaling factor.
        """
        formatstr = "#0" + str(n_l + 2) + "b"
        lambda_min_tilde = np.abs(lambda_min * (2**n_l - 1) / lambda_max)
        # floating point precision can cause problems
        if np.abs(lambda_min_tilde - 1) < 1e-7:
            lambda_min_tilde = 1
        binstr = format(int(lambda_min_tilde), formatstr)[2::]
        lamb_min_rep = 0
        for i, char in enumerate(binstr):
            lamb_min_rep += int(char) / (2 ** (i + 1))
        return lamb_min_rep

    def _set_qc_param(self):
        self.num_vec_qubits = np.log2(len(self.vector))
        self.kappa = np.linalg.cond(self.matrix)
        self.num_clock_qubits = (
            int(max(self.num_vec_qubits + 1, int(np.ceil(np.log2(self.kappa + 1)))))
            + self.neg_eigenvals
        )

        lambda_max = max(np.abs(np.linalg.eigvals(self.matrix)))
        lambda_min = min(np.abs(np.linalg.eigvals(self.matrix)))
        self.delta = self._get_delta(
            self.num_clock_qubits - self.neg_eigenvals, lambda_min, lambda_max
        )
        self.evolution_time = (
            2 * np.pi * self.delta / lambda_min / (2**self.neg_eigenvals)
        )
        self.scaling = lambda_min

    def _get_state_preparation(self):
        qc_state_prepare = QuantumCircuit(self.num_vec_qubits)
        vec_norm = np.linalg.norm(self.vector)
        qc_state_prepare.prepare_state(self.vector / vec_norm)
        self.scaling /= vec_norm
        return qc_state_prepare

    def _get_ejHt(self):
        op_H = SparsePauliOp.from_operator(self.matrix)
        op_ejHt = PauliEvolutionGate(op_H, -self.evolution_time)
        qc_ejHt = QuantumCircuit(self.num_vec_qubits)
        qc_ejHt.append(op_ejHt, range(int(self.num_vec_qubits)))
        return qc_ejHt

    def _get_QPE(self):
        if self.qc_pe_ejHt is None:
            qc_ejHt = self._get_ejHt()
            self.qc_pe_ejHt = PhaseEstimation(self.num_clock_qubits, qc_ejHt)
        return self.qc_pe_ejHt

    def _get_controld_rotation(self):
        qc_cr = ExactReciprocal(
            self.num_clock_qubits, self.delta, neg_vals=self.neg_eigenvals
        )
        return qc_cr

    def _build(self):
        qr_state_prepare = QuantumRegister(self.num_vec_qubits)
        qr_clock = QuantumRegister(self.num_clock_qubits)
        qr_flag = QuantumRegister(1)  # suppose there is only one flag qubit
        qc = QuantumCircuit(qr_state_prepare, qr_clock, qr_flag)

        qc.append(self._get_state_preparation(), qr_state_prepare[:])
        qc.append(self._get_QPE(), qr_clock[:] + qr_state_prepare[:])
        qc.append(
            self._get_controld_rotation().to_instruction(),
            qr_clock[::-1] + [qr_flag[0]],
        )
        qc.append(self._get_QPE().inverse(), qr_clock[:] + qr_state_prepare[:])

        self.add_register(*qc.qregs)
        self.compose(qc, inplace=True)
