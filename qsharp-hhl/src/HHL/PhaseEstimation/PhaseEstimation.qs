namespace HHL.PhaseEstimation {
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Unstable.StatePreparation;
    open Microsoft.Quantum.Convert;
    open HHL.CommonOperation;

    operation ApplyQFTWithReverse(qs : Qubit[]) : Unit is Adj + Ctl {
        ApplyQFT(qs);
        ReverseQubits(qs);
    }

    operation ApplyPhaseEstimation(unitary : ((Int, Qubit[]) => Unit is Adj + Ctl), clockQubits : Qubit[], phiQubits : Qubit[]) : Unit is Adj + Ctl {
        PrepareUniform(clockQubits);

        let nClock = Length(clockQubits);
        for i in 0..nClock - 1 {
            let power = 2^i; // little-endian, first qubits present less significant bits
            Controlled unitary([clockQubits[i]], (power, phiQubits));
        }

        Adjoint ApplyQFTWithReverse(clockQubits);
        // Adjoint ApplyQFT(Reversed(clockQubits));
        // ReverseQubits(clockQubits);
    }

}