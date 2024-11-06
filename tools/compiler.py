import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.passes.synthesis import SolovayKitaev
from qiskit.quantum_info import Operator
 
circuit = QuantumCircuit(1)
circuit.rx(0.8, 0)
 
print("Original circuit:")
print(circuit.draw())
 
skd = SolovayKitaev(recursion_degree=2)
 
discretized = skd(circuit)
 
print("Discretized circuit:")
print(discretized.draw())
 
print("Error:", np.linalg.norm(Operator(circuit).data - Operator(discretized).data))