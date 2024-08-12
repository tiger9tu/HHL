namespace PhaseEstimation {
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Unstable.StatePreparation;
    open Microsoft.Quantum.Convert;
    open CommonOperation;

    operation ApplyPhaseEstimation(unitary : ((Int, Qubit[]) => Unit is Adj + Ctl), clockQubits : Qubit[], phiQubits : Qubit[]) : Unit is Adj + Ctl {
        PrepareUniform(clockQubits);

        let nClock = Length(clockQubits);
        for i in 0..nClock - 1 {
            let power = 2^i; // little-endian, first qubits present less significant bits
            Controlled unitary([clockQubits[i]], (power, phiQubits));
        }
        
        Adjoint ApplyQFT(Reversed(clockQubits));
        ReverseQubits(clockQubits);
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



}