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

    operation ApplyHHL(unitaryA : (Qubit[], Int) => Unit is Adj + Ctl, targetRegister : Qubit[]) : Bool {

        let numClockQubits = CalculateNumClockQubits();
        use clockRegister = Qubit[numClockQubits];
        use anciliaRegister = Qubit();

        Message("after stateprepare, before QPE");
        DumpMachine();
        within {
            // Unitary = HamiltonianSimulation?
            
            ApplyPhaseEstimation(unitaryA, clockRegister, targetRegister);
            
        } apply {
            Message("after QPE");
            DumpMachine();
            let scaling = CalculateScaling();
            let negVal = true;
            ApplyReciprocal(scaling, negVal, clockRegister, anciliaRegister);
            Message("after reciprocal");
            DumpMachine();
        }

        Message("after QPE diagger");
        DumpMachine();
        ResetAll(clockRegister);
        let postSelectResult = M(anciliaRegister);
        Message($"post selection result = {postSelectResult}");
        Reset(anciliaRegister);

        Message("after reset ancillia and clock");
        DumpMachine();

        // return true;

        if postSelectResult == One {
            Message("post selection succeed");
            DumpMachine();
            return true;
        } else {
            return false;
        }
    }


    operation PhaseEstimationUnitTest() : Unit {

        // exp(iX)
        use clockQubits = Qubit[2];
        use phiQubits = Qubit[1];

        let eigenstateVector = [1.0 / Sqrt(2.0), 1.0 / Sqrt(2.0) ];

        PreparePureStateD(eigenstateVector, phiQubits);
        operation UnitaryExp_i_X_2piDiv4(qubits : Qubit[], power : Int) : Unit is Adj + Ctl {
            Rx(- IntAsDouble(power) * 2.0 * 2.0 * PI() / 4.0, qubits[0]);
        }
        ApplyPhaseEstimation(UnitaryExp_i_X_2piDiv4,clockQubits,phiQubits);

        DumpMachine(); 
        // Anticipate
        //  
        //  Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |100⟩ |  0.7071+0.0000𝑖 |    50.0000% |  -0.0000
        // |101⟩ |  0.7071+0.0000𝑖 |    50.0000% |  -0.0000
        ResetAll(clockQubits + phiQubits);

        


    }

    operation ReciprocalUnitTest() : Unit {

        use clockQubits = Qubit[3];
        use anciliaQubit = Qubit();

        let clockState = [0.0,0.0,0.0,0.0,0.0, 1.0, 0.0, 0.0]; // |101> represent -1
        PreparePureStateD(clockState, clockQubits);
        ApplyReciprocal(0.8, true, clockQubits,anciliaQubit);


    }

    @EntryPoint()
    operation Main() : Unit {

        PhaseEstimationUnitTest();
        // ReciprocalUnitTest();
        // let vector = [1.0 , 0.0];
        // let matrix = [
        //     [0.0, 1.0],
        //     [1.0, 0.0]
        // ];

        // use stateVectorb = Qubit[1];
        // mutable result = false;
        // mutable count = 0;
        // repeat {
        //     PreparePureStateD(vector, stateVectorb);
        //     set result = ApplyHHL(HamiltonianEvolutionSample1, stateVectorb);
        //     set count = count + 1;

        //     if not result {
        //         ResetAll(stateVectorb);
        //     } else {
        //         Message($"count = {count}");
        //         DumpRegister(stateVectorb);
        //         ResetAll(stateVectorb);
        //     }
        // } until result;

    }
}