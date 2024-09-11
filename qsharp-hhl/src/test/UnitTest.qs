namespace HHLUnitTest {
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Unstable.StatePreparation;

    open HHL;
    open HHL.PhaseEstimation;
    open HHL.HamiltonianSimulation;
    open HHL.CommonOperation;
    open HHL.HamiltonianSimulation.TrotterSuzuki;
    open HHL.HamiltonianSimulation.Oracle;

    operation OracleExample0UnitTest() : Unit {
        // use xQubit = Qubit[2];
        // use yQubit = Qubit[2];
        // OracleExample(xQubit + yQubit);
        // // Expect |0011⟩ |  1.0000+0.0000𝑖 |   100.0000% |   0.0000
        // DumpMachine();
        // ResetAll(xQubit + yQubit);

        use xQubit = Qubit[2];
        use yQubit = Qubit[2];
        X(xQubit[1]);
        OracleExample0(xQubit + yQubit);
        // Expect |0011⟩ |  1.0000+0.0000𝑖 |   100.0000% |   0.0000
        DumpMachine();
        ResetAll(xQubit + yQubit);
    }

    operation OracleExample1UnitTest() : Unit {
        // 0 1 0 0
        // 1 0 0 0
        // 0 0 1 0
        // 0 0 0 1
        // use xQubit = Qubit[2];
        // use yQubit = Qubit[2];
        // OracleExample(xQubit + yQubit);
        // // Expect |0011⟩ |  1.0000+0.0000𝑖 |   100.0000% |   0.0000
        // DumpMachine();
        // ResetAll(xQubit + yQubit);

        use xQubit = Qubit[2];
        use yQubit = Qubit[2];
        // X(xQubit[1]);
        OracleExample1(xQubit + yQubit);
        // Expect |0001⟩ |  1.0000+0.0000𝑖 |   100.0000% |   0.0000
        DumpMachine();
        ResetAll(xQubit + yQubit);
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


    operation OracleExample0HamiltonianSimulationUnitTest() : Unit {
        use xQubits = Qubit[2];
        let eigenstateVector = [-1.0 / Sqrt(2.0), 0.0, 0.0, 1.0 / Sqrt(2.0)];
        PreparePureStateD(eigenstateVector, xQubits);
        use yQubits = Qubit[2];
        use aQubit = Qubit();
        // OracleHamiltonianSimulation(1.0 / 4.0, OracleExample0, xQubits);
        DumpMachine();
        ResetAll(xQubits);
    }

    operation TrotterSuzukiUnitTest() : Unit {
        //  Expect:
        //  Basis | Amplitude      | Probability | Phase
        //  -----------------------------------------------
        //  |0⟩ | −1.0000+0.0000𝑖 |   100.0000% |   3.1416
        // let A is ((2,0), (0,0)),  e^i(A)t  = e^i(Z + I)t
        use targetQubit = Qubit();
        let eigenstateVector = [1.0, 0.0];
        PreparePureStateD(eigenstateVector, [targetQubit]);
        let CoefZaddI = [Coef(Exp([PauliZ], _, _), PI() / 2.0), Coef(Exp([PauliI], _, _), PI() / 2.0)];
        ApplyTrotterSuzuki(2, 14, CoefZaddI, [targetQubit]);

        DumpMachine();
        Reset(targetQubit);

    }

    operation PhaseEstimationUnitTest() : Unit {

        // hermitian matrix : exp(iX_pi/4)
        // eigenState : [1/sqrt(2), 1/sqrt(2)]
        //
        // anticipate :
        //
        //  Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |100⟩ |  0.7071+0.0000𝑖 |    50.0000% |  -0.0000
        // |101⟩ |  0.7071+0.0000𝑖 |    50.0000% |  -0.0000
        // use clockQubits = Qubit[2];
        // use phiQubits = Qubit[1];
        // let eigenstateVector = [1.0 / Sqrt(2.0), 1.0 / Sqrt(2.0)];
        // PreparePureStateD(eigenstateVector, phiQubits);
        // operation UnitaryExp_i_X_2piDiv4(power : Int, qubits : Qubit[]) : Unit is Adj + Ctl {
        //     Rx(- IntAsDouble(power) * 2.0 * 2.0 * PI() / 4.0, qubits[0]);
        // }
        // ApplyPhaseEstimation(UnitaryExp_i_X_2piDiv4, clockQubits, phiQubits);
        // DumpMachine();
        // ResetAll(clockQubits + phiQubits);

        use clockQubits = Qubit[2];
        use phiQubits = Qubit[2];
        let eigenstateVector = [1.0, 1.0, 1.0, 1.0];
        PreparePureStateD(eigenstateVector, phiQubits);
        operation UnitaryExp_i_X_tensor_X_2piDiv4(power : Int, qubits : Qubit[]) : Unit is Adj + Ctl {
            Exp([PauliX, PauliX], 1.0 * IntAsDouble(power) * 2.0 * PI() / 4.0, qubits);
        }
        ApplyPhaseEstimation(UnitaryExp_i_X_tensor_X_2piDiv4, clockQubits, phiQubits);
        DumpMachine();
        ResetAll(clockQubits + phiQubits);

    }


    operation CRotationUnitTest() : Unit {

        // clock qubits : |01> represent 0.10 (1/2)
        // scaling : 0.25
        // negVal : false

        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |010⟩ |  0.8660+0.0000𝑖 |    75.0000% |   0.0000
        // |011⟩ |  0.5000+0.0000𝑖 |    25.0000% |   0.0000
        use clockQubits = Qubit[4];
        use ancillaQubit = Qubit();
        // let clockState = [0.0, 0.0, 1.0, 0.0]; // |01> represent -1
        X(clockQubits[1]);
        // PreparePureStateD(clockState, clockQubits); // Big endien
        ApplyCReciprocal(0.125, true, clockQubits, ancillaQubit);
        DumpMachine();
        ResetAll(clockQubits + [ancillaQubit]);


        // clock qubits : |011> represent - 0.10 (- 1/2)
        // scaling : 0.25
        // negVal : false
        //
        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |010⟩ |  0.8660+0.0000𝑖 |    75.0000% |   0.0000
        // |011⟩ |  - 0.5000+0.0000𝑖 |    25.0000% |   0.0000
        // use clockQubits = Qubit[3];
        // use ancillaQubit = Qubit();
        // let clockState = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]; // |01> represent -1
        // PreparePureStateD(clockState, clockQubits); // Big endien
        // ApplyCReciprocal(0.25, true, clockQubits, ancillaQubit);
        // DumpMachine();
        // ResetAll(clockQubits + [ancillaQubit]);

    }

    operation CReciprocalUnitTest() : Unit {
        use clockQubits = Qubit[2];
        use ancillaQubit = Qubit();
        let clockState = [0.0, 1.0, 0.0, 0.0]; // |01> represent -1
        PreparePureStateD(clockState, clockQubits); // Big endien
        ApplyCReciprocal(0.25, false, clockQubits, ancillaQubit);
        DumpMachine();
        ResetAll(clockQubits + [ancillaQubit]);
    }


    operation HHLUnitTest() : Unit {

        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |0⟩ |  1.0000+0.0000𝑖 |   100.0000% |  -0.0000
        // let vector = [1.0, 3.0];
        // let matrix = [
        //     [0.0, 1.0],
        //     [1.0, 0.0]
        // ];
        // use stateVectorb = Qubit[1];
        // PreparePureStateD(vector, stateVectorb);
        // ApplyHHL(HamiltonianSimulationSample1, stateVectorb);
        // DumpMachine();
        // Reset(stateVectorb[0]);

        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |00⟩ |  0.7303+0.0000𝑖 |    53.3333% |  -0.0000
        // |01⟩ |  0.3651+0.0000𝑖 |    13.3333% |  -0.0000
        // |10⟩ |  0.1826+0.0000𝑖 |     3.3333% |  -0.0000
        // |11⟩ |  0.5477+0.0000𝑖 |    30.0000% |  -0.0000
        // let vector = [1.0, 3.0, 4.0, 2.0];
        //         let matrix = [
        //     [0.0, 0.0, 1.0, 0.0],
        //     [0.0, 0.0, 0.0, 1.0],
        //     [1.0, 0.0, 0.0, 0.0],
        //     [0.0, 1.0, 0.0, 0.0]
        // ];


        //////////////////////////////////Test Case 1////////////////////////////////////

        // let vector = [0.0, 1.0, 0.0, 0.0];
        // let matrix = [
        //     [0.0, 0.0, 0.0, 1.0],
        //     [0.0, 1.0, 0.0, 0.0],
        //     [0.0, 0.0, 1.0, 0.0],
        //     [1.0, 0.0, 0.0, 0.0]
        // ];
        // use stateVectorb = Qubit[2];
        // use yQubits = Qubit[2];
        // use aQubit = Qubit();
        // PreparePureStateD(vector, stateVectorb);
        // DumpMachine();

        // internal operation _UnitaryA_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        //     OracleHamiltonianSimulation(IntAsDouble(power) * 2.0 * PI() / 4.0, OracleExample0, xqubits, yQubits, aQubit);
        // }

        // ApplyHHL(_UnitaryA_(_, _, yQubits, aQubit), stateVectorb);
        // DumpMachine();
        // ResetAll(stateVectorb + yQubits + [aQubit]);

        //////////////////////////////////Test Case 2////////////////////////////////////
        let matrix = [
            [0.0, 1.0, 0.0, 0.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0]
        ];
        
        let vector = [1.0, 2.0, -3.0, 1.0];
        // let vector = [1.0, -1.0, 0.0, 0.0];
        use stateVectorb = Qubit[2];

        PreparePureStateD(vector, stateVectorb);
        DumpMachine();

        // let config = HHLConfig(4,1,1.,0.25,0.1,true, true, 0.1, 1., 1, 0.05);

        ApplyHHL(OracleExample1, stateVectorb);
        ResetAll(stateVectorb);

        //////////////////////////////////Test Case 3////////////////////////////////////

        // all the eigenvectors are fine, but for the non eigenvectors, there are problems
        // it is suprising because non eigenvectors are just linear combination of eigenvectors
        // so when eigenvectors work fine, then should it also be for non-eigenvectors
        // let vector = [2., -1., 0., -1.];
        // let matrix = [
        //     [0.0, 1.0, 0.0, 1.0],
        //     [1.0, 1.0, 0.0, 0.0],
        //     [0.0, 0.0, 2.0, 0.0],
        //     [1.0, 0.0, 0.0, 1.0]
        // ];
        // use stateVectorb = Qubit[2];
        // use yQubits = Qubit[2];
        // use aQubit = Qubit();
        // PreparePureStateD(vector, stateVectorb);

        // internal operation _Oracle0add1HamiltonianSimulation_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        //     let t0 = GetT0();
        //     let hsO0 = Coef(OracleHamiltonianSimulation(_, OracleExample0, _, yQubits, aQubit), IntAsDouble(power) * t0);
        //     let hsO1 = Coef(OracleHamiltonianSimulation(_, OracleExample1, _, yQubits, aQubit), IntAsDouble(power) * t0);

        //     ApplyTrotterSuzuki(2, 14, [hsO0, hsO1], xqubits);
        //     // ApplyTrotterSuzuki(2, 14, [hsO0, hsO1], xqubits);
        // }

        // let config = HHLConfig(2, 2., 0.25, 4, 0.1, true, false);
        // // ApplyHHL(_UnitaryA_(_, _, yQubits, aQubit), stateVectorb);
        // ApplyHHL(_Oracle0add1HamiltonianSimulation_(_, _, yQubits, aQubit), stateVectorb);
        // DumpMachine();
        // ResetAll(stateVectorb + yQubits + [aQubit]);

        ////////////////////////////////////Test Case4 - Scale Up////////////////////////////////
        // let n = _DefNumVecQubits_();
        // use stateVectorb = Qubit[n];
        // let nclock = _GetNumClockQubits_();
        // use yQubits = Qubit[nclock];
        // use aQubit = Qubit();
        // // PreparePureStateD(vector, stateVectorb);

        // internal operation _Oracle2HamiltonianSimulation_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        //     let t0 = GetT0();
        //     let hsO0 = Coef(OracleHamiltonianSimulation(_, OracleEmpty, _, yQubits, aQubit), IntAsDouble(power) * t0);
        //     ApplyTrotterSuzuki(2, 14, [hsO0], xqubits);
        // }

        // // ApplyHHL(_UnitaryA_(_, _, yQubits, aQubit), stateVectorb);
        // ApplyHHL(_Oracle2HamiltonianSimulation_(_, _, yQubits, aQubit), stateVectorb);
        // DumpMachine();
        // ResetAll(stateVectorb + yQubits + [aQubit]);
    }

    operation OracleHamiltonianSimulationUnitTest(time : Double) : Unit {
        use qx = Qubit[2];
        // use qa = Qubit();
        let state = [1.,-1.,0.,0.];
        PreparePureStateD(state, qx);
        OracleHamiltonianSimulation(time, OracleExample1, qx);

        // DumpRegister(qx);
        // DumpRegister([qa]);
        DumpMachine();
        ResetAll(qx);
    }
}