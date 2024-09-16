// HHL Algorithm


namespace HHL.CommonOperation {
    import Microsoft.Quantum.Random.DrawRandomDouble;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Unstable.StatePreparation;


    operation CRotation(negVal : Bool, angleFunc : (Int, Bool) -> Double, Rn : (Double, Qubit) => Unit is Adj + Ctl, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        // little-endian
        mutable negValInt = 0;
        if negVal {
            set negValInt = 1;
        }

        let nClock = Length(clockQubits);
        let nAbsClock = nClock - negValInt;

        let nVal = 2^nClock;
        let nAbsVal = 2^nAbsClock;

        for i in 1..nAbsVal- 1 {
            let angle = angleFunc(i, false);
            ApplyControlledOnInt(i, Rn(angle, _), clockQubits[0..nAbsClock - 1], ancillaQubit);
        }

        if negVal {
            for i in 1..nAbsVal -1 {
                // counteract the previous rotation, and rotates negative angle.
                let negAngle = angleFunc(i, true) -  angleFunc(i, false);
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Rn(negAngle, _), clockQubits[0..nAbsClock - 1], ancillaQubit));
            }
        }
    }

    operation CyRotation(negVal : Bool, angleFunc : (Int, Bool) -> Double, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        CRotation(negVal, angleFunc, Ry(_, _), clockQubits, ancillaQubit);
    }

    operation CxRotation(negVal : Bool, angleFunc : (Int, Bool) -> Double, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        CRotation(negVal, angleFunc, Rx(_, _), clockQubits, ancillaQubit);
    }

    operation ReverseQubits(qubits : Qubit[]) : Unit is Adj + Ctl {
        let length = Length(qubits);
        for i in 0..length / 2 - 1 {
            SWAP(qubits[i], qubits[length - i - 1]);
        }
    }

    operation SwapRegs(reg1 : Qubit[], reg2 : Qubit[]) : Unit is Adj + Ctl {
        let length = Length(reg1);
        Fact(length == Length(reg2), "SwapRegs: regs must be with the same length.");
        for i in 0..length - 1 {
            SWAP(reg1[i], reg2[i]);
        }
    }

    operation PrepareUniform(qubits : Qubit[]) : Unit is Adj + Ctl {
        for q in qubits {
            H(q);
        }
    }

    // little-endian
    operation PreparePureStateDL(coefficients : Double[], qubits : Qubit[]) : Unit is Adj + Ctl {
        within {
            ReverseQubits(qubits);
        } apply {
            PreparePureStateD(coefficients, qubits);
        }
    }



    operation U3(theta : Double, phi : Double, lambda : Double, qubit : Qubit) : Unit is Adj + Ctl {
        Rz(lambda, qubit);
        Ry(theta, qubit);
        Rz(phi, qubit);
        R(PauliI, - (phi + lambda), qubit);
    }


    operation ZipOp(Op : (Qubit[] => Unit is Adj + Ctl), qubits1 : Qubit[], qubits2 : Qubit[]) : Unit is Adj + Ctl {
        let length = Length(qubits1);
        Fact(length == Length(qubits2), "ZipOp: qubits1 and qubits2 must be with the same length.");
        for i in 0..length-1 {
            Op([qubits1[i], qubits2[i]]);
        }
    }

    function BoolAsInt(b : Bool) : Int {
        mutable ib = 0;
        if b {
            set ib = ib + 1;
        }
        ib
    }

    // little-endian
    function IntToBinaryVector(n : Int, numBits : Int) : Int[] {
        mutable binaryVector = Repeated(0, numBits);
        mutable temp = n;

        for i in 0..numBits - 1 {
            set binaryVector w/= i <- (temp % 2);
            set temp = temp / 2;
        }
        return binaryVector;
    }


}