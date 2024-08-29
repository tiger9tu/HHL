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


    operation CRotation(negVal : Bool, angleFunc : Int -> Double, Rn : (Double, Qubit) => Unit is Adj + Ctl, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        // little endien
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
                let negDoubleAngle = - 2. * angleFunc(i);
                // counteract
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Rn(negDoubleAngle, _), clockQubits[0..nAbsClock - 1], ancillaQubit));
                // Apply negative phase
                // Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Rn(negAngle, _), clockQubits[0..nAbsClock - 1], ancillaQubit));
            }

        }
    }

    operation CyRotation(negVal : Bool, angleFunc : Int -> Double, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        CRotation(negVal, angleFunc, Ry(_, _), clockQubits, ancillaQubit);
    }

    operation CxRotation(negVal : Bool, angleFunc : Int -> Double, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        CRotation(negVal, angleFunc, Rx(_, _), clockQubits, ancillaQubit);
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

    operation repeatOp(reps : Int, Op : (Qubit[] => Unit is Adj + Ctl), qubits : Qubit[]) : Unit is Adj + Ctl {
        for i in 0..reps {
            Op(qubits);
        }
    }

    function BoolAsInt(b : Bool) : Int {
        mutable ib = 0;
        if b {
            set ib = ib + 1;
        }
        ib
    }

    operation UNothing(qubits : Qubit[]) : Unit is Ctl + Adj {
        for q in qubits {
            X(q);
        }

        for q in qubits {
            X(q);
        }
    }
}