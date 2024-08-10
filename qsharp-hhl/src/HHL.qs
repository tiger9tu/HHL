// HHL Algorithm


namespace HHL {
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Unstable.StatePreparation;

    open PhaseEstimation;
    open HamiltonianEvolution;
    open CommonOperation;
    open HamiltonianEvolution.SuzukiTrotter;


    internal function _CalculateNumClockQubits_() : Int {
        return 3; // implement later
    }

    internal function _CalculateScaling_() : Double {
        return 0.25; // implement later
    }

    internal function _ReciprocalAngle_(scaling : Double, nAbsClock : Int, i : Int) : Double {
        let reciprocalVal = scaling * IntAsDouble(nAbsClock) / IntAsDouble(i);
        mutable angle = 0.0;
        if reciprocalVal == 1.0 {
            set angle = PI();
        } elif reciprocalVal < 1.0 {
            set angle = 2.0 * ArcSin(reciprocalVal);
        }
        return angle;
    }

    internal operation _ApplyCReciprocal_(scaling : Double, negVal : Bool, clockQubits : Qubit[], anciliaQubit : Qubit) : Unit {
        mutable nAbsClock = Length(clockQubits);
        if negVal {
            set nAbsClock -= 1;
        }
        ApplyCRotation(negVal, _ReciprocalAngle_(scaling, nAbsClock, _), clockQubits, anciliaQubit);

    }

    operation ApplyHHL(unitaryA : (Int, Qubit[]) => Unit is Adj + Ctl, targetRegister : Qubit[]) : Unit {

        let numClockQubits = _CalculateNumClockQubits_();
        use clockRegister = Qubit[numClockQubits];
        use anciliaRegister = Qubit();
        mutable postSelect : Result = Zero;
        let scaling = _CalculateScaling_();
        let negVal = true;

        repeat {
            within {
                ApplyPhaseEstimation(unitaryA, clockRegister, targetRegister);
            } apply {
                _ApplyCReciprocal_(scaling, negVal, clockRegister, anciliaRegister);
            }
            DumpMachine();
            set postSelect = M(anciliaRegister);
            ResetAll(clockRegister);
            Reset(anciliaRegister);
        } until postSelect == One;

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
        // ApplyHHL(HamiltonianEvolutionSample1, stateVectorb);
        // DumpMachine();
        // Reset(stateVectorb[0]);

        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |00⟩ |  0.7303+0.0000𝑖 |    53.3333% |  -0.0000
        // |01⟩ |  0.3651+0.0000𝑖 |    13.3333% |  -0.0000
        // |10⟩ |  0.1826+0.0000𝑖 |     3.3333% |  -0.0000
        // |11⟩ |  0.5477+0.0000𝑖 |    30.0000% |  -0.0000
        let vector = [1.0, 3.0, 4.0, 2.0];
        let matrix = [
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0]
        ];
        use stateVectorb = Qubit[2];
        PreparePureStateD(vector, stateVectorb);
        ApplyHHL(HamiltonianEvolutionSample2, stateVectorb);
        DumpMachine();
        ResetAll(stateVectorb);

    }

    @EntryPoint()
    operation Main() : Unit {
        // SuzukiTrotterUnitTest();
        // PhaseEstimationUnitTest();
        // CRotationUnitTest();
        HHLUnitTest();
    }
}