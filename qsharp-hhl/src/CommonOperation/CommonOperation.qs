// HHL Algorithm


namespace CommonOperation {
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Unstable.StatePreparation;

    operation ApplyCRotation(negVal : Bool, angleFunc : Int -> Double, clockQubits : Qubit[], anciliaQubit : Qubit) : Unit {
        mutable negValInt = 0;
        if negVal {
            set negValInt = 1;
        }

        let nClock = Length(clockQubits);
        let nAbsClock = nClock - negValInt;

        let nVal = 2^nClock;
        let nAbsVal = 2^nAbsClock;

        for i in 1..nAbsVal- 1 {
            let angle = angleFunc(i);
            ApplyControlledOnInt(i, Ry(angle, _), clockQubits[0..nAbsClock - 1], anciliaQubit);
        }

        if negVal {
            for i in 1..nAbsVal -1 {
                let negAngle = - angleFunc(i);
                // counteract
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Ry(negAngle, _), clockQubits[0..nAbsClock - 1], anciliaQubit));
                // Apply negative phase
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Ry(negAngle, _), clockQubits[0..nAbsClock - 1], anciliaQubit));
            }

        }
    }


    operation CRotationUnitTest() : Unit {

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
        // use clockQubits = Qubit[3];
        // use anciliaQubit = Qubit();
        // let clockState = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]; // |01> represent -1
        // PreparePureStateD(clockState, clockQubits); // Big endien
        // ApplyCReciprocal(0.25, true, clockQubits, anciliaQubit);
        // DumpMachine();
        // ResetAll(clockQubits + [anciliaQubit]);

    }

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


}