// HHL Algorithm


namespace Reciprocal {
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;

    function GetYRotationAngle(reciprocalVal : Double) : Double {
        mutable angle = 0.0;
        if reciprocalVal == 1.0 {
            set angle = PI();
        } elif reciprocalVal < 1.0 {
            set angle = 2.0 * ArcSin(reciprocalVal);
        }
        return angle;
    }


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
            let cDivLambda = scaling * IntAsDouble(nAbsVal) / IntAsDouble(i);
            let angle = GetYRotationAngle(cDivLambda);
            ApplyControlledOnInt(i, Ry(angle, _), clockQubits[0..nAbsClock - 1], anciliaQubit);
        }

        if negVal {
            for i in 1..nAbsVal -1 {

                let cDivLambda = scaling * IntAsDouble(nAbsVal) / IntAsDouble(i);
                let negAngle = - GetYRotationAngle(cDivLambda);
                // counteract
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Ry(negAngle, _), clockQubits[0..nAbsClock - 1], anciliaQubit));
                // Apply negative phase
                Controlled ApplyControlledOnInt([Tail(clockQubits)], (i, Ry(negAngle, _), clockQubits[0..nAbsClock - 1], anciliaQubit));
            }

        }
    }

}