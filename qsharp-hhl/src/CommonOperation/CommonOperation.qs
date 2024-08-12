// HHL Algorithm


namespace CommonOperation {
    import Microsoft.Quantum.Random.DrawRandomDouble;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Unstable.StatePreparation;

    operation CRotation(negVal : Bool, angleFunc : Int -> Double, Rn : (Double, Qubit) => Unit is Adj + Ctl, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
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
            ApplyControlledOnInt(i, Rn(angle, _), clockQubits[0..nAbsClock - 1], ancillaQubit);
        }

        if negVal {
            for i in 1..nAbsVal -1 {
                let negAngle = - angleFunc(i);
                // counteract
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Rn(negAngle, _), clockQubits[0..nAbsClock - 1], ancillaQubit));
                // Apply negative phase
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Rn(negAngle, _), clockQubits[0..nAbsClock - 1], ancillaQubit));
            }

        }
    }

    operation CyRotation(negVal : Bool, angleFunc : Int -> Double, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        CRotation(negVal, angleFunc, Ry(_, _), clockQubits, ancillaQubit);
    }

    operation CxRotation(negVal : Bool, angleFunc : Int -> Double, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        CRotation(negVal, angleFunc, Rx(_, _), clockQubits, ancillaQubit);
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
        // use ancillaQubit = Qubit();
        // let clockState = [0.0, 1.0, 0.0, 0.0]; // |01> represent -1
        // PreparePureStateD(clockState, clockQubits); // Big endien
        // ApplyReciprocal(0.25, false, clockQubits, ancillaQubit);
        // DumpMachine();
        // ResetAll(clockQubits + [ancillaQubit]);
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

    operation PrepareUniform(qubits : Qubit[]) : Unit is Adj + Ctl {
        for q in qubits {
            H(q);
        }
    }

    operation ReverseQubits(qubits : Qubit[]) : Unit is Adj + Ctl {
        let n = Length(qubits);
        for i in 0..n / 2 - 1 {
            SWAP(qubits[i], qubits[n - i - 1]);
        }
    }

    operation U3(theta : Double, phi : Double, lambda : Double, qubit : Qubit) : Unit is Adj + Ctl {
        Rz(lambda, qubit);
        Ry(theta, qubit);
        Rz(phi, qubit);
        R(PauliI, - (phi + lambda), qubit);
    }

    operation U3UnitTest() : Unit {
        // expect that U3Rx is identical to Rx
        operation U3Rx(theta : Double, qubit : Qubit) : Unit {
            U3(theta, - PI() / 2.0, PI() / 2.0, qubit);
        }

        use q = Qubit();
        let theta = DrawRandomDouble(0.0, PI());
        U3Rx(theta, q);
        DumpMachine();
        Rx(- theta, q);
        DumpMachine();
        Reset(q);

    }

    operation ZipOp(Op : (Qubit[] => Unit is Adj + Ctl), qubits1 : Qubit[], qubits2 : Qubit[]) : Unit is Adj + Ctl {
        for i in 0..Length(qubits1)-1 {
            Op([qubits1[i], qubits2[i]]);
        }
    }
}