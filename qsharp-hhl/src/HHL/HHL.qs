// HHL Algorithm


namespace HHL {
    import HHL.HamiltonianSimulation.ApplyHamiltonianSimulation;
    import HHL.CommonOperation.ReverseQubits;
    import HHL.HamiltonianSimulation.Oracle.Oracle;

    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Unstable.StatePreparation;

    open PhaseEstimation;
    open HamiltonianSimulation;
    open CommonOperation;
    open HamiltonianSimulation.TrotterSuzuki;
    open HamiltonianSimulation.Oracle;

    internal function ReciprocalAngle(C : Double, nClock : Int, i : Int, neg : Bool) : Double {
        mutable reciprocalVal = 0.0;
        if not neg {
            set reciprocalVal = C * 1. / IntAsDouble(i);
        } else {
            set reciprocalVal = - C * (1. / (2.^IntAsDouble(nClock) - IntAsDouble(i + 2^(nClock - 1))));
        }

        mutable angle = 0.0;

        if reciprocalVal == 1.0 {
            set angle = PI();
        } elif reciprocalVal < 1.0 {
            set angle = 2.0 * ArcSin(reciprocalVal);
        }

        return angle;
    }

    operation ApplyCReciprocal(C : Double, negVal : Bool, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        mutable nClock = Length(clockQubits);

        CyRotation(negVal, ReciprocalAngle(C, nClock, _, _), clockQubits, ancillaQubit);
    }

    operation HSPower(t0 : Double, power : Int, HS : (Double, Qubit[]) => Unit is Adj + Ctl, qx : Qubit[]) : Unit is Adj + Ctl {
        HS(IntAsDouble(power) * t0, qx);
    }

    operation HHLSimulation(A : Double[][], b : Double[]) : Unit {

        let N = Length(A);
        let nb = Ceiling(Lg(IntAsDouble(N)));

        // these parameters depends on other stuff, but we will come to that later..
        let nc = 4; // num clock qubits
        let C = 1.;  // scaling of ancilla rotation
        let ntrotter = 14;
        let t0 = 2. * PI() / 2.^IntAsDouble(nc);
        let nr = 10; // represent number of bits in r register of oracle

        use qb = Qubit[nb];
        use qc = Qubit[nc];
        use qa = Qubit();

        // let eiAt = OracleHamiltonianSimulation(_, nr, oA, _);
        let eiAt = ApplyHamiltonianSimulation(_, A, nr, _);
        let eiAtPower = HSPower(t0, _, eiAt, _);

        mutable postSelect : Result = Zero;

        repeat {
            PreparePureStateDL(b, qb);
            within {
                ApplyPhaseEstimation(eiAtPower, qc, qb);
            } apply {
                ApplyCReciprocal(C, true, qc, qa);
            }
            set postSelect = M(qa);
            ResetAll(qc + [qa]);
        } until postSelect == One
        fixup {
            ResetAll(qb);
        }

        ReverseQubits(qb); // represents big-endian
        DumpMachine();
        ResetAll(qb);

    }


}