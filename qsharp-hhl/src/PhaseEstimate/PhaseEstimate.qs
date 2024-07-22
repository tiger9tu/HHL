namespace PhaseEstimation {
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Arrays;

    operation PrepareUniform(qubits : Qubit[]) : Unit is Adj + Ctl {
        for q in qubits {
            H(q);
        }
    }

    operation ReverseQubits(qubits : Qubit[]) : Unit is Ctl + Adj {
        let n = Length(qubits);
        for i in 0..n / 2 - 1 {
            SWAP(qubits[i], qubits[n - i - 1]);
        }
    }

    operation ApplyPhaseEstimation(unitary : ((Qubit[], Int) => Unit is Adj + Ctl), clockQubits : Qubit[], phiQubits : Qubit[]) : Unit is Adj + Ctl {
        PrepareUniform(clockQubits);

        let nClock = Length(clockQubits);
        for i in 0..nClock - 1 {
            let power = 2^i; // little-endian, first qubits present less significant bits
            Controlled unitary([clockQubits[i]], (phiQubits, power));
        }

        Adjoint ApplyQFT(Reversed(clockQubits));
        ReverseQubits(clockQubits);
    }




}