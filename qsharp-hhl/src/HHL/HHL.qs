// HHL Algorithm


namespace HHL {
    import HHL.CommonOperation.Log2;
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

    internal function _ReciprocalAngle_(scaling : Double, nClock : Int, i : Int) : Double {
        let reciprocalVal = scaling * (2.^IntAsDouble(nClock)) / IntAsDouble(i);
        mutable angle = 0.0;
        if reciprocalVal == 1.0 {
            set angle = PI();
        } elif reciprocalVal < 1.0 {
            set angle = 2.0 * ArcSin(reciprocalVal);
        }

        return angle;
    }

    internal operation _ApplyCReciprocal_(scaling : Double, negVal : Bool, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        mutable nClock = Length(clockQubits);

        CyRotation(negVal, _ReciprocalAngle_(scaling, nClock, _), clockQubits, ancillaQubit);
    }


    newtype HHLConfig = (
        N : Int,
        sparsity : Int,
        kappa : Double,
        C : Double, 
 
        epsilon : Double,
        negVal : Bool,
        repeatitive : Bool
    );

    internal function _GetNumClockQubits_(config : HHLConfig) : Int {
        Max([Ceiling(Log2(IntAsDouble(config.N))), Ceiling(Log2(config.kappa + 1.))]) + BoolAsInt(config.negVal)
    }

    // internal function _GetScaling_(config : HHLConfig) : Double {
    //     let lambdaMin = _DefMinAbsEigenVal_();
    //     let negVal = _DefNegVal_();
    //     let nAbsC = 2^(_GetNumClockQubits_() - BoolAsInt(negVal));
    //     lambdaMin / IntAsDouble(nAbsC)
    // }

    internal function _GetT0_(config : HHLConfig) : Double {
        let nc = _GetNumClockQubits_(config);
        let nAbsC = nc - BoolAsInt(config.negVal);
        2. * PI() / (2.^IntAsDouble(nAbsC)) // the Abs is because if CRotation implementation
    }

    internal operation _OracleHamiltonianSimulationUnitary_(t0 : Double, trotterReps : Int, power : Int, oracle : Qubit[] => Unit is Adj + Ctl, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        let hsO0 = Coef(OracleHamiltonianSimulation(_, oracle, _, yQubits, aQubit), IntAsDouble(power) * t0);
        ApplyTrotterSuzuki(2, trotterReps, [hsO0], xqubits);
    }

    operation ApplyHHL(config : HHLConfig, oracleA : (Qubit[]) => Unit is Adj + Ctl, qb : Qubit[]) : Unit {
        let nc = _GetNumClockQubits_(config);
        let t0 = _GetT0_(config);

        use qc = Qubit[nc];
        use qa = Qubit();

        // hamiltonian simulation qubits
        use qwy = Qubit[Length(qb)];
        use qwa = Qubit();

        // internal operation _UnitaryA_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        //     OracleHamiltonianSimulation(IntAsDouble(power) * 2. * PI(), OracleExample1, xqubits, yQubits, aQubit);
        // }

        let unitaryA = _OracleHamiltonianSimulationUnitary_(t0, 4,_,oracleA,_,qwy,qwa);
        // let unitaryA = _UnitaryA_(_,_, qwy, qwa);

        mutable postSelect : Result = Zero;
        repeat {
            within {
                ApplyPhaseEstimation(unitaryA, qc, qb);
            } apply {
                _ApplyCReciprocal_(config.C, config.negVal, qc, qa);
            }
            set postSelect = M(qa);
            ResetAll(qc + [qa]);
            Message("one circle");
        } until not config.repeatitive or postSelect == One;

    }


}