// HHL Algorithm


namespace Reciprocal {
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;

    operation ApplyReciprocal(scaling : Double, negVal : Bool, clockQubits : Qubit[], anciliaQubit : Qubit) : Unit {
        mutable negValInt = 0;
        if negVal {
            set negValInt = 1;
        }

        let nClock = Length(clockQubits);
        let nAbsClock = nClock - negValInt;

        let nVal = 2^nClock;
        let nAbsVal = 2^nAbsClock;

        for i in 1..nAbsVal- 1 {
            let angle = 2.0 * ArcSin(scaling * IntAsDouble(nAbsVal) / IntAsDouble(i));
            ApplyControlledOnInt(i, Ry(angle, _), clockQubits[0..nAbsClock - 1], anciliaQubit);
        }

        if negVal {
            for i in 1..nAbsVal -1 {
                // counteract
                let negAngle = - 2.0 * ArcSin(scaling * IntAsDouble(nAbsVal) / IntAsDouble(i));
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Ry(negAngle, _), clockQubits[0..nAbsClock - 1], anciliaQubit));
            }

            for i in 1..nAbsVal-1 {
                // two's complement representation
                let negAngle = 2.0 * ArcSin(scaling * (- 1.0) / (1.0 -IntAsDouble(i) / IntAsDouble(nAbsVal)));
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Ry(negAngle, _), clockQubits[0..nAbsClock - 1], anciliaQubit));
            }

        }

    }



}