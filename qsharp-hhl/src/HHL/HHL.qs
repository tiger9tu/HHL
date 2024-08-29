// HHL Algorithm


namespace HHL {
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

    internal function _ReciprocalAngle_(C : Double, nClock : Int, i : Int) : Double {
        let reciprocalVal = C * (2.^IntAsDouble(nClock)) / IntAsDouble(i);
        mutable angle = 0.0;

        if reciprocalVal > 1.0 {
            Message($"warning: reciprocal value = {reciprocalVal} > 1.0");
        }
        if reciprocalVal == 1.0 {
            set angle = PI();
        } elif reciprocalVal < 1.0 {
            set angle = 2.0 * ArcSin(reciprocalVal);
        }

        return angle;
    }

    internal operation _ApplyCReciprocal_(C : Double, negVal : Bool, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        mutable nClock = Length(clockQubits);

        CyRotation(negVal, _ReciprocalAngle_(C, nClock, _), clockQubits, ancillaQubit);
    }

    newtype HHLConfig = (
        N : Int,
        sparsity : Int,
        kappa : Double,
        C : Double, 
 
        epsilon : Double,
        negVal : Bool,
        repeatitive : Bool,

        // for bounding the error of trotter
        maxH : Double,
        cTrotter : Double,
        verticeQueries : Int,

        cQPE : Double,

    );

    internal function _GetNumClockQubits_(config : HHLConfig) : Int {
        let QPEAcurracy = (1. /  config.cQPE) * config.epsilon / config.kappa;
        // if QPE as a subroutine then we don not need to consider success probability.
        Max([Ceiling(Lg(IntAsDouble(config.N))), Ceiling(Lg(1. / QPEAcurracy))]) + BoolAsInt(config.negVal)
    }

    // internal function _GetC_(config : HHLConfig) : Double {
    //     let lambdaMin = _DefMinAbsEigenVal_();
    //     let negVal = _DefNegVal_();
    //     let nAbsC = 2^(_GetNumClockQubits_() - BoolAsInt(negVal));
    //     lambdaMin / IntAsDouble(nAbsC)
    // }

    function GetT0(config : HHLConfig) : Double {
        let nc = _GetNumClockQubits_(config);
        let nAbsC = nc - BoolAsInt(config.negVal);
        2. * PI() / (2.^IntAsDouble(nAbsC)) // the Abs is because if CRotation implementation
    }


    internal operation _HS2Unitary_(t0 : Double, power : Int, HS : (Double, Qubit[],Qubit[],Qubit) => Unit is Adj + Ctl, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        HS(IntAsDouble(power) * t0, xqubits,yQubits,aQubit);
    }

    operation ApplyHHL(config : HHLConfig, oracleA : (Qubit[]) => Unit is Adj + Ctl, qb : Qubit[]) : Unit {
        let nc = _GetNumClockQubits_(config);

        // Message($"nc = {nc}");
        let t0 = GetT0(config);
        // let trotterReps = GetTrotterReps(config);

        use qc = Qubit[nc];
        use qa = Qubit();

        // hamiltonian simulation qubits
        use qwy = Qubit[Length(qb)];
        use qwa = Qubit();

        // let unitaryA = _OracleHamiltonianSimulationUnitary_(t0,config,_,[oracleA],_,qwy,qwa);
        let hsConfig = HSConfig(config.repeatitive, config.sparsity, config.epsilon,config.maxH, config.cTrotter, config.verticeQueries);
        let HS = OracleSparseHamiltonianSimulation(hsConfig,_,oracleA, _,_,_);
        let unitaryA = _HS2Unitary_(t0, _, HS, _,qwy,qwa);
        
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
            DumpMachine();
        } until not config.repeatitive or postSelect == One;

    }


}