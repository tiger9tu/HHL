// HHL Algorithm


namespace HHL {
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Unstable.StatePreparation;

    open HamiltonianEvolution;
    open PhaseEstimation;
    open Reciprocal;


    internal operation CalculateNumClockQubits() : Int {
        return 3; // implement later
    }

    internal operation CalculateScaling() : Double {
        return 0.25; // implement later
    }

    operation ApplyHHL(unitaryA : (Qubit[], Int) => Unit is Adj + Ctl, targetRegister : Qubit[]) : Unit {

        let numClockQubits = CalculateNumClockQubits();
        use clockRegister = Qubit[numClockQubits];
        use anciliaRegister = Qubit();
        mutable postSelect : Result = Zero;
        let scaling = CalculateScaling();
        let negVal = true;

        repeat {
            within {
                ApplyPhaseEstimation(unitaryA, clockRegister, targetRegister);
            } apply {
                ApplyReciprocal(scaling, negVal, clockRegister, anciliaRegister);
            }

            set postSelect = M(anciliaRegister);
            ResetAll(clockRegister);
            Reset(anciliaRegister);
        } until postSelect == One;

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
        use clockQubits = Qubit[2];
        use phiQubits = Qubit[1];
        let eigenstateVector = [1.0 / Sqrt(2.0), 1.0 / Sqrt(2.0)];
        PreparePureStateD(eigenstateVector, phiQubits);
        operation UnitaryExp_i_X_2piDiv4(qubits : Qubit[], power : Int) : Unit is Adj + Ctl {
            Rx(- IntAsDouble(power) * 2.0 * 2.0 * PI() / 4.0, qubits[0]);
        }
        ApplyPhaseEstimation(UnitaryExp_i_X_2piDiv4, clockQubits, phiQubits);
        DumpMachine();
        ResetAll(clockQubits + phiQubits);

    }

    operation ReciprocalUnitTest() : Unit {

        // clock qubits : |01> represent 0.10 (1/2)
        // scaling : 0.25
        // negVal : false
        //
        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |010⟩ |  0.8660+0.0000𝑖 |    75.0000% |   0.0000
        // |011⟩ |  0.5000+0.0000𝑖 |    25.0000% |   0.0000
        // use clockQubits = Qubit[2];
        // use anciliaQubit = Qubit();
        // let clockState = [0.0, 1.0, 0.0, 0.0]; // |01> represent -1
        // PreparePureStateD(clockState, clockQubits); // Big endien
        // ApplyReciprocal(0.25, false, clockQubits, anciliaQubit);
        // DumpMachine();
        // ResetAll(clockQubits + [anciliaQubit]);

        // clock qubits : |011> represent - 0.10 (- 1/2)
        // scaling : 0.25
        // negVal : false
        //
        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |010⟩ |  0.8660+0.0000𝑖 |    75.0000% |   0.0000
        // |011⟩ |  - 0.5000+0.0000𝑖 |    25.0000% |   0.0000
        use clockQubits = Qubit[3];
        use anciliaQubit = Qubit();
        let clockState = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]; // |01> represent -1
        PreparePureStateD(clockState, clockQubits); // Big endien
        ApplyReciprocal(0.25, true, clockQubits, anciliaQubit);
        DumpMachine();
        ResetAll(clockQubits + [anciliaQubit]);


    }

    operation HHLUnitTest() : Unit {

        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |0⟩ |  1.0000+0.0000𝑖 |   100.0000% |  -0.0000
        let vector = [1.0, 3.0];
        let matrix = [
            [0.0, 1.0],
            [1.0, 0.0]
        ];
        use stateVectorb = Qubit[1];
        PreparePureStateD(vector, stateVectorb);
        ApplyHHL(HamiltonianEvolutionSample1, stateVectorb);
        DumpMachine();
        Reset(stateVectorb[0]);

    }

    @EntryPoint()
    operation Main() : Unit {

        // PhaseEstimationUnitTest();
        // ReciprocalUnitTest();
        HHLUnitTest();
    }
}