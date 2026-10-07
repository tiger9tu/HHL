# Paper Framework

This paper is about resource estimation of QLSA algorithm and compare with classical algorithm. 
Here we concisely describe the Resource modeling, where the techinical detail of each component can be found under subdirectories.

* The quantum QLSA resource
** logical resource 
** Physical hardware
** QEC scheduling

* The classical resource
** logical resource
** physical hardware

# The quanatum QLSA resource
Overall the quantum QLSA resource model accepts a problem instance described by several parameters, such as size, condition number, sparsity, and error tolerance. And it produce the time, and energy cost. We do this in 3 components, logical layer, QEC layer and physical layer. [HHL/paper-revise-clean/q-resource]

## logical resource
The logical resource model for a quantum algorithm accepts the problem parameter, and produce the T gate and qubit count. We provide the logical resource model for both the old HHL algorithm and a modern QLSA algorithm. [HHL/paper-revise-clean/q-resource/logical]

## physical hardware parmeters
The physcial hardware parameters describes the quantum computer. It includes number of physical qubits, the clock speed, the error rates, power...

## QEC 
The quantum error correction model accepts (logical)T gate and qubit count, and the physical hardware parameters, and output the space (physical qubit count), runtime and energy consumption for solving the problem on quantum computer. It internally is a contraint optimizer described in "the game of surface code".

# The classical resource
The classical resource model accepts problem instance, produce runtime and energy cost. 

## logical resource
We count the number of floating point instructions needed for a problem instance using the CGNE algorithm

## physical hardware parameters
The classical physical parameters uses HPCG in https://www.hpcg-benchmark.org/custom/sc25.html, from which we can derive runtime and energy cost on supercomputers.






