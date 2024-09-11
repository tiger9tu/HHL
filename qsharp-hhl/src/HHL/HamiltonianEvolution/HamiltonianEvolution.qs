namespace HHL.HamiltonianSimulation {
    import HHLUnitTest.TrotterSuzukiUnitTest;
    import Microsoft.Quantum.Diagnostics.DumpRegister;
    import Microsoft.Quantum.Arrays.Zipped;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open HHL.CommonOperation;
    open HHL.HamiltonianSimulation.Oracle;

    open TrotterSuzuki;


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


    internal operation _CNNOT_(cnQubits : Qubit[], tQubit : Qubit) : Unit is Adj + Ctl {
        within {
            X(cnQubits[1]);
        } apply {
            CCNOT(cnQubits[0], cnQubits[1], tQubit);
        }
    }

    operation OracleHamiltonianSimulation(time : Double, oracle : Qubit[] => Unit is Adj, xQubits : Qubit[] ) : Unit is Adj + Ctl {
        use yQubits = Qubit[Length(xQubits)];
        use aQubit = Qubit();
        
        within {
            oracle(xQubits + yQubits);
            ZipOp(_PreCompiledWGate_, xQubits, yQubits);
            ZipOp(_CNNOT_(_, aQubit), xQubits, yQubits);
        } apply {
            Rz(- 2.0 * time, aQubit);
        }
    }

    // newtype HSConfig = (
    //     real : Bool,
    //     sparsity : Int,
    //     epsilon : Double,
    //     // for bounding the error of trotter
    //     maxH : Double,
    //     // cTrotter : Double,
    //     verticeQueries : Int,
    // );

    // function log5(x : Double) : Double {
    //     Lg(x) / Lg(5.)
    // }

    // operation OracleSparseHamiltonianSimulationFake(hsConfig : HSConfig, time : Double, oracle : Qubit[] => Unit is Adj + Ctl, xQubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
    //     let simulateGraphColoredOracle = repeatOp(hsConfig.verticeQueries, oracle, _);
        
    //     let singleHSCoef = Coef(OracleHamiltonianSimulation(_,  simulateGraphColoredOracle, _ ), time);

    //     let m = 6* hsConfig.sparsity*hsConfig.sparsity;

    //     let sparseHSCoef = Repeated(singleHSCoef, m);
    //     let k = Round((1./2.)*(Sqrt(log5(IntAsDouble(m)*hsConfig.maxH*time / hsConfig.epsilon ) + 1.)));
    //     Message($"k = {k}");
    //     // let sparseHSCoef = Repeated(singleHSCoef, 1);
    //     let trotterReps = Ceiling((4.*5.^(IntAsDouble(k) - 1./2.))*(IntAsDouble(m)*hsConfig.maxH*time)^(1.+1./(2.*IntAsDouble(k))) / (hsConfig.epsilon^(1./(2.*IntAsDouble(k))))); // according to paper's sclalign
    //     Message($"trotterReps = {trotterReps}");
    //     // ApplyTrotterSuzuki(k, 1, sparseHSCoef, xQubits);
    //     ApplyTrotterSuzuki(k, trotterReps, sparseHSCoef, xQubits);

    // }

    // operation OracleSparseHamiltonianSimulation(hsConfig : HSConfig, time : Double, oracle : Qubit[] => Unit is Adj + Ctl, xQubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
    //     if(hsConfig.real) {
    //         Message("real");
    //         OracleHamiltonianSimulation(time, oracle,xQubits);
    //     }
    //     else {
    //         OracleSparseHamiltonianSimulationFake(hsConfig, time, oracle, xQubits, yQubits, aQubit);
    //     }
    // }


}