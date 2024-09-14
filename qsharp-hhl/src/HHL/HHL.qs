// HHL Algorithm


namespace HHL {
    import HHL.HamiltonianSimulation.OracleHamiltonianSimulation;
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

    internal function _ReciprocalAngle_(C : Double, nClock : Int, i : Int, neg : Bool) : Double {
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

        CyRotation(negVal, _ReciprocalAngle_(C, nClock, _, _), clockQubits, ancillaQubit);
    }

    // newtype HHLConfig = (
    //     N : Int,
    //     sparsity : Int,
    //     kappa : Double,
    //     C : Double,

    //     epsilon : Double,
    //     negVal : Bool,
    //     repeatitive : Bool,

    //     // for bounding the error of trotter
    //     maxH : Double,
    //     cTrotter : Double,
    //     verticeQueries : Int,

    //     cQPE : Double,

    // );

    // internal function _GetNumClockQubits_(config : HHLConfig) : Int {
    //     let QPEAcurracy = (1. /  config.cQPE) * config.epsilon / config.kappa;
    //     // if QPE as a subroutine then we don not need to consider success probability.
    //     Max([Ceiling(Lg(IntAsDouble(config.N))), Ceiling(Lg(1. / QPEAcurracy))]) + BoolAsInt(config.negVal)
    // }

    // // internal function _GetC_(config : HHLConfig) : Double {
    // //     let lambdaMin = _DefMinAbsEigenVal_();
    // //     let negVal = _DefNegVal_();
    // //     let nAbsC = 2^(_GetNumClockQubits_() - BoolAsInt(negVal));
    // //     lambdaMin / IntAsDouble(nAbsC)
    // // }

    // function GetT0(config : HHLConfig) : Double {
    //     let nc = _GetNumClockQubits_(config);
    //     let nAbsC = nc - BoolAsInt(config.negVal);
    //     2. * PI() / (2.^IntAsDouble(nAbsC)) // the Abs is because if CRotation implementation
    // }


    operation HS2U(t0 : Double, power : Int, HS : (Double, Qubit[]) => Unit is Adj + Ctl, qx : Qubit[]) : Unit is Adj + Ctl {
        HS(IntAsDouble(power) * t0, qx);
    }

    operation ApplyHHL(oracleA : (Qubit[]) => Unit is Adj + Ctl, qb : Qubit[]) : Unit {
        // let nc = _GetNumClockQubits_(config);
        let nc = 4;


        // Message($"nc = {nc}");
        // let t0 = GetT0(config);

        let t0 = 2. * PI() / 2.^4.;
        let C = 1.;
        // let trotterReps = GetTrotterReps(config);

        use qc = Qubit[nc];
        use qa = Qubit();

        // let unitaryA = _OracleHamiltonianSimulationUnitary_(t0,config,_,[oracleA],_,qwy,qwa);
        // let hsConfig = HSConfig(config.repeatitive, config.sparsity, config.epsilon,config.maxH,  config.verticeQueries);
        let HS = OracleHamiltonianSimulation(_, oracleA, _);
        let unitaryA = HS2U(t0, _, HS, _);

        mutable postSelect : Result = Zero;
        repeat {
            within {
                ApplyPhaseEstimation(unitaryA, qc, qb);
            } apply {
                ApplyCReciprocal(C, true, qc, qa);
            }
            set postSelect = M(qa);
            ResetAll(qc + [qa]);
            Message("one circle");
            DumpMachine();
        } until postSelect == One;

    }

    operation ApplyHHLU(UA : (Int, Qubit[]) => Unit is Adj + Ctl, qb : Qubit[]) : Unit {
        // let nc = _GetNumClockQubits_(config);
        let nc = 4;


        // Message($"nc = {nc}");
        // let t0 = GetT0(config);

        let C = 1.;
        // let trotterReps = GetTrotterReps(config);

        use qc = Qubit[nc];
        use qa = Qubit();

        mutable postSelect : Result = Zero;
        repeat {
            within {
                ApplyPhaseEstimation(UA, qc, qb);
            } apply {
                ApplyCReciprocal(C, true, qc, qa);
            }
DumpMachine();
            set postSelect = M(qa);
            ResetAll(qc + [qa]);
            Message("one circle");
            DumpMachine();

        } until postSelect == One;

    }


}