import numpy as np
from qiskit.circuit import QuantumCircuit
from qiskit.transpiler.passes.synthesis import SolovayKitaev
from qiskit.quantum_info import Operator
from qiskit.compiler import transpile
from qiskit.circuit.library import TGate, HGate, SGate, CXGate, CCXGate
from qiskit.circuit.library import CRZGate
basis_gates = [TGate(), SGate(), HGate(), CXGate()]

skd = SolovayKitaev(recursion_degree=2)

u = Operator([[0, 1],
              [1, 0]])

w = Operator([[1,0,0,0],
              [0,1/np.sqrt(2),1/np.sqrt(2),0],
              [0,1/np.sqrt(2),- 1/np.sqrt(2),0],
              [0,0,0,1]])

crz = CRZGate(0.8)  # Controlled Rz gate with an angle of 0.5 radians
toff = CCXGate()  # Toffoli gate

def show_T_count(op: Operator) -> int:
    input_dims = op.input_dims()
    qc = QuantumCircuit(len(input_dims))
    qc.unitary(op, list(range(len(input_dims))), label='op')
    transpiled = transpile(qc, basis_gates=['u1', 'u2', 'u3', 'cx'], optimization_level=3)
    discretized = skd(transpiled)
    t_gate_count = discretized.count_ops().get('t', 0)
    print(f"T gate count: {t_gate_count}")

qc = QuantumCircuit(3)  
qc.append(toff, [0, 1,2])
transpiled = transpile(qc, basis_gates=['u1', 'u2', 'u3', 'cx'], optimization_level=3)
discretized = skd(transpiled)
t_gate_count = discretized.count_ops().get('t', 0)
print(f"T gate count: {t_gate_count}")
        
# show_T_count(w)





