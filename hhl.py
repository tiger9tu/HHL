import numpy as np
import scipy as sp

# Import Qiskit
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Operator, Statevector

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

        self._matrix = matrix
        self._vector = vector
        self._tolerance = tolerance

        # build circuit
        self._build()

    def eigs_bounds(self):
        """Return lower and upper bounds on the eigenvalues of the matrix."""
        matrix_array = self._matrix
        lambda_max = max(np.abs(np.linalg.eigvals(matrix_array)))
        lambda_min = min(np.abs(np.linalg.eigvals(matrix_array)))
        return lambda_min, lambda_max

    def condition_bounds(self):
        """Return lower and upper bounds on the condition number of the matrix."""
        matrix_array = self._matrix
        kappa = np.linalg.cond(matrix_array)
        return kappa, kappa

    def _get_delta(self, n_l: int, lambda_min: float, lambda_max: float) -> float:
        """Calculates the scaling factor to represent exactly lambda_min on nl binary digits.

        Args:
            n_l: The number of qubits to represent the eigenvalues.
            lambda_min: the smallest eigenvalue.
            lambda_max: the largest eigenvalue.

        Returns:
            The value of the scaling factor.
        """
        # formatstr = "#0" + str(n_l + 2) + "b"
        # lambda_min_tilde = np.abs(lambda_min * (2**n_l - 1) / lambda_max)
        # # floating point precision can cause problems
        # if np.abs(lambda_min_tilde - 1) < 1e-7:
        #     lambda_min_tilde = 1
        # binstr = format(int(lambda_min_tilde), formatstr)[2::]
        # lamb_min_rep = 0
        # for i, char in enumerate(binstr):
        #     lamb_min_rep += int(char) / (2 ** (i + 1))
        # return lamb_min_rep
        return lambda_min

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

    def _build(self):
        num_vec_qubits = np.log2(len(self._vector))
        kappa = self.condition_bounds()[0]
        num_clock_qubits = int(max(num_vec_qubits + 1, int(np.ceil(np.log2(kappa + 1)))))
        lambda_min, lambda_max = self.eigs_bounds()
        delta = self._get_delta(num_clock_qubits, lambda_min, lambda_max)
        evolution_time = 2 * np.pi * delta / lambda_min

        # Update the scaling of the solution
        self._scaling = lambda_min

        qr_vec = QuantumRegister(num_vec_qubits)
        qr_clock = QuantumRegister(num_clock_qubits)
        qr_flag = QuantumRegister(1)  # suppose there is only one flag qubit

        qc = QuantumCircuit(qr_vec , qr_clock , qr_flag)

        qc_vec = QuantumCircuit(qr_vec)
        vec_norm = np.linalg.norm(self._vector)
        qc_vec.prepare_state(self._vector / vec_norm )
        self._scaling *= vec_norm 
        qc.append(qc_vec, qr_vec[:])

        qc_mat = QuantumCircuit(qr_vec)
        e_mat = sp.linalg.expm(1j * self._matrix * evolution_time)
        qc_mat.append(Operator(e_mat).to_instruction(),[0])

        qc_pe_e_mat = PhaseEstimation(num_clock_qubits,qc_mat)
        qc.append(qc_pe_e_mat, qr_clock[:] + qr_vec[:])

        qc_cr = ExactReciprocal(num_clock_qubits, delta)
        qc.append(qc_cr.to_instruction(),  qr_clock[::-1] + [qr_flag[0]])

        qc.append(qc_pe_e_mat.inverse(), qr_clock[:] + qr_vec[:])

        self.add_register(*qc.qregs)
        self.compose(qc,  inplace=True)


A = np.array([[1,0],[0,1]]) 
b_ = np.array([7,1]) 
qc = HHL(A, b_)

print(qc)