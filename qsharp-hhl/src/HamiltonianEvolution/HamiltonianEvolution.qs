namespace HamiltonianSimulation {
    import Microsoft.Quantum.Diagnostics.DumpRegister;
    import Microsoft.Quantum.Arrays.Zipped;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open CommonOperation;
    open HamiltonianSimulation.Oracle;
    open Microsoft.Quantum.Unstable.StatePreparation;

    operation HamiltonianSimulationSample1(time : Double, targetRegister : Qubit[]) : Unit is Adj + Ctl {
        Rx(- 2.0 * time * 2.0 * PI() / 4.0, targetRegister[0]) // exp(i*2pi*X)
    }

    operation HamiltonianSimulationSample2(time : Double, targetRegister : Qubit[]) : Unit is Adj + Ctl {
        Exp([PauliX, PauliX], 1.0 * time * 2.0 * PI() / 4.0, targetRegister); // exp(i*2pi*X)
    }

    internal operation _PreCompiledWGate_(qubits : Qubit[]) : Unit is Adj + Ctl {
        //    [[1, 0, 0, 0],
        //     [0, 1/sqrt(2),  1/sqrt(2), 0],
        //     [0, 1/sqrt(2), -1/sqrt(2), 0],
        //     [0, 0, 0, 1]]
        //     big endien: |01> -> |1> -> 1/sqrt(2) (|01> + |10>)
        //     qsharp
        // U3(PI(), 0.32175055439664213, 0.32175055439664213, qubits[0]);
        // U3(1.4512678518986009, PI() / 2.0, -PI(), qubits[1]);
        // CNOT(qubits[0], qubits[1]);
        // U3(PI() / 4.0, -PI() / 2.0, PI() / 2.0, qubits[0]);
        // U3(0.1688370309450062, -2.359774761217599, -2.3597747612176105, qubits[1]);
        // CNOT(qubits[0], qubits[1]);
        // U3(PI() / 4.0, 0.0, -PI() / 2.0, qubits[0]);
        // U3(1.4521247316971555, 1.4504171294224673, -3.1272723037036005, qubits[1]);
        // CNOT(qubits[0], qubits[1]);
        // U3(PI(), -0.4982443934561056, 1.0725519333387918, qubits[0]);
        // U3(3.0220641786934994, 0.0, PI() / 2.0, qubits[1]);

        U3(PI(), 0.32175055439664213, 0.32175055439664213, qubits[1]);
        U3(1.4512678518986009, PI() / 2.0, -PI(), qubits[0]);
        CNOT(qubits[1], qubits[0]);
        U3(PI() / 4.0, -PI() / 2.0, PI() / 2.0, qubits[1]);
        U3(0.1688370309450062, -2.359774761217599, -2.3597747612176105, qubits[0]);
        CNOT(qubits[1], qubits[0]);
        U3(PI() / 4.0, 0.0, -PI() / 2.0, qubits[1]);
        U3(1.4521247316971555, 1.4504171294224673, -3.1272723037036005, qubits[0]);
        CNOT(qubits[1], qubits[0]);
        U3(PI(), -0.4982443934561056, 1.0725519333387918, qubits[1]);
        U3(3.0220641786934994, 0.0, PI() / 2.0, qubits[0]);


        // adjust global phase
        Exp([PauliI, PauliI], - 2.9085, qubits);
    }

    operation WGateUnitTest() : Unit {
        DumpMachine();
        use q2 = Qubit[2];
        _PreCompiledWGate_(q2);
        DumpMachine();
        // expect |00>
        X(q2[1]); // prepare |01>
        _PreCompiledWGate_(q2);
        DumpMachine();
        //  Expect :
        //  Basis | Amplitude      | Probability | Phase
        //  -----------------------------------------------
        //   |01⟩ | −0.7071+0.0000𝑖 |    50.0000% |   3.1416
        //   |10⟩ |  0.7071+0.0000𝑖 |    50.0000% |  -0.0000
        ResetAll(q2);
    }

    internal operation _CNNOT_(cnQubits : Qubit[], tQubit : Qubit) : Unit is Adj + Ctl {
        within {
            X(cnQubits[1]);
        } apply {
            CCNOT(cnQubits[0], cnQubits[1], tQubit);
        }
    }

    operation OracleHamiltonianSimulation(time : Double, oracle : Qubit[] => Unit is Adj, xQubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        within {
            oracle(xQubits + yQubits);
            ZipOp(_PreCompiledWGate_, xQubits, yQubits);
            ZipOp(_CNNOT_(_, aQubit), xQubits, yQubits);
        } apply {
            Rz(- 2.0 * time, aQubit);
        }
    }


    operation OracleExample0HamiltonianSimulationUnitTest() : Unit {
        use xQubits = Qubit[2];
        let eigenstateVector = [0.0, 1.0, 0.0, 0.0];
        PreparePureStateD(eigenstateVector, xQubits);
        use yQubits = Qubit[2];
        use aQubit = Qubit();
        OracleHamiltonianSimulation(1.0 / 4.0, OracleExample0, xQubits, yQubits, aQubit);
        DumpMachine();
        ResetAll(xQubits);
    }

}