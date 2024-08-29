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

    internal function _ReciprocalAngle_(scaling : Double, nClock : Int, i : Int) : Double {
        let reciprocalVal = scaling * (2.^IntAsDouble(nClock)) / IntAsDouble(i);
        mutable angle = 0.0;
        if reciprocalVal == 1.0 {
            set angle = PI();
        } elif reciprocalVal < 1.0 {
            set angle = 2.0 * ArcSin(reciprocalVal);
        }

        // Message($"nAbsClock = {nAbsClock}, i = {i}, reciprocalVal = {reciprocalVal}");
        return angle;
    }

    internal operation _ApplyCReciprocal_(scaling : Double, negVal : Bool, clockQubits : Qubit[], ancillaQubit : Qubit) : Unit {
        mutable nClock = Length(clockQubits);

        CyRotation(negVal, _ReciprocalAngle_(scaling, nClock, _), clockQubits, ancillaQubit);
    }

    operation CReciprocalUnitTest() : Unit {
        use clockQubits = Qubit[2];
        use ancillaQubit = Qubit();
        let clockState = [0.0, 1.0, 0.0, 0.0]; // |01> represent -1
        PreparePureStateD(clockState, clockQubits); // Big endien
        _ApplyCReciprocal_(0.25, false, clockQubits, ancillaQubit);
        DumpMachine();
        ResetAll(clockQubits + [ancillaQubit]);
    }



    internal function _DefNumVecQubits_() : Int {
        2
    }

    internal function _DefMinAbsEigenVal_() : Double {
        1.
    }

    internal function _DefMaxAbsEigenVal_() : Double {
        2.
    }

    internal function _DefNegVal_() : Bool {
        true
    }

    internal function _DefVector_() : Double[] {
        [4.0, 2.0, 3.0, -1.0]
    }

    internal function _GetKappa_() : Double {
        _DefMaxAbsEigenVal_() / _DefMinAbsEigenVal_()
    }

    internal function _GetNumClockQubits_() : Int {
        let n = _DefNumVecQubits_();
        let kappa = _GetKappa_();
        let negVal = _DefNegVal_();
        Max([n, Ceiling(Log2(kappa + 1.))]) + BoolAsInt(negVal)
    }

    internal function _GetScaling_() : Double {
        let lambdaMin = _DefMinAbsEigenVal_();
        let negVal = _DefNegVal_();
        let nAbsC = 2^(_GetNumClockQubits_() - BoolAsInt(negVal));
        lambdaMin / IntAsDouble(nAbsC)
    }

    internal function _GetT0_() : Double {
        let nc = _GetNumClockQubits_();
        let negVal = _DefNegVal_();
        let nAbsC = nc - BoolAsInt(negVal);
        2. * PI() / (2.^IntAsDouble(nAbsC)) // the Abs is because if CRotation implementation
    }

    operation ApplyHHL(unitaryA : (Int, Qubit[]) => Unit is Adj + Ctl, targetRegister : Qubit[]) : Unit {
        let kappa = _GetKappa_();
        let negVal = _DefNegVal_();
        let numClockQubits = _GetNumClockQubits_();
        let scaling = _GetScaling_();

        use clockRegister = Qubit[numClockQubits];
        use ancillaRegister = Qubit();
        mutable postSelect : Result = Zero;

        repeat {
            within {
                ApplyPhaseEstimation(unitaryA, clockRegister, targetRegister);
            } apply {
                _ApplyCReciprocal_(scaling, negVal, clockRegister, ancillaRegister);
            }
            set postSelect = M(ancillaRegister);
            ResetAll(clockRegister + [ancillaRegister]);
            Message("one circle");
        } until postSelect == One;

    }

    operation HHLUnitTest() : Unit {

        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |0⟩ |  1.0000+0.0000𝑖 |   100.0000% |  -0.0000
        // let vector = [1.0, 3.0];
        // let matrix = [
        //     [0.0, 1.0],
        //     [1.0, 0.0]
        // ];
        // use stateVectorb = Qubit[1];
        // PreparePureStateD(vector, stateVectorb);
        // ApplyHHL(HamiltonianSimulationSample1, stateVectorb);
        // DumpMachine();
        // Reset(stateVectorb[0]);

        // Anticipate :
        // Basis | Amplitude      | Probability | Phase
        // -----------------------------------------------
        // |00⟩ |  0.7303+0.0000𝑖 |    53.3333% |  -0.0000
        // |01⟩ |  0.3651+0.0000𝑖 |    13.3333% |  -0.0000
        // |10⟩ |  0.1826+0.0000𝑖 |     3.3333% |  -0.0000
        // |11⟩ |  0.5477+0.0000𝑖 |    30.0000% |  -0.0000
        // let vector = [1.0, 3.0, 4.0, 2.0];
        //         let matrix = [
        //     [0.0, 0.0, 1.0, 0.0],
        //     [0.0, 0.0, 0.0, 1.0],
        //     [1.0, 0.0, 0.0, 0.0],
        //     [0.0, 1.0, 0.0, 0.0]
        // ];


        //////////////////////////////////Test Case 1////////////////////////////////////

        // let vector = [0.0, 1.0, 0.0, 0.0];
        // let matrix = [
        //     [0.0, 0.0, 0.0, 1.0],
        //     [0.0, 1.0, 0.0, 0.0],
        //     [0.0, 0.0, 1.0, 0.0],
        //     [1.0, 0.0, 0.0, 0.0]
        // ];
        // use stateVectorb = Qubit[2];
        // use yQubits = Qubit[2];
        // use aQubit = Qubit();
        // PreparePureStateD(vector, stateVectorb);
        // DumpMachine();

        // internal operation _UnitaryA_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        //     OracleHamiltonianSimulation(IntAsDouble(power) * 2.0 * PI() / 4.0, OracleExample0, xqubits, yQubits, aQubit);
        // }

        // ApplyHHL(_UnitaryA_(_, _, yQubits, aQubit), stateVectorb);
        // DumpMachine();
        // ResetAll(stateVectorb + yQubits + [aQubit]);

        //////////////////////////////////Test Case 2////////////////////////////////////
        // let nv = _DefNumVecQubits_();
        // let vector = _DefVector_();
        // let matrix = [
        //     [0.0, 1.0, 0.0, 0.0],
        //     [1.0, 0.0, 0.0, 0.0],
        //     [0.0, 0.0, 1.0, 0.0],
        //     [0.0, 0.0, 0.0, 1.0]
        // ];

        // use stateVectorb = Qubit[nv];
        // use yQubits = Qubit[2];
        // use aQubit = Qubit();
        // PreparePureStateD(vector, stateVectorb);
        // DumpMachine();

        // internal operation _UnitaryA_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        //     let t0 = _GetT0_();
        //     OracleHamiltonianSimulation(IntAsDouble(power) * t0, OracleExample1, xqubits, yQubits, aQubit);
        // }

        // ApplyHHL(_UnitaryA_(_, _, yQubits, aQubit), stateVectorb);
        // // DumpMachine();
        // DumpRegister(stateVectorb);
        // ResetAll(stateVectorb + yQubits + [aQubit]);

        //////////////////////////////////Test Case 3////////////////////////////////////

        // all the eigenvectors are fine, but for the non eigenvectors, there are problems
        // it is suprising because non eigenvectors are just linear combination of eigenvectors
        // so when eigenvectors work fine, then should it also be for non-eigenvectors
        let vector = [2., -1., 0., -1.];
        let matrix = [
            [0.0, 1.0, 0.0, 1.0],
            [1.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 2.0, 0.0],
            [1.0, 0.0, 0.0, 1.0]
        ];
        use stateVectorb = Qubit[2];
        use yQubits = Qubit[2];
        use aQubit = Qubit();
        PreparePureStateD(vector, stateVectorb);

        internal operation _Oracle0add1HamiltonianSimulation_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
            let t0 = _GetT0_();
            let hsO0 = Coef(OracleHamiltonianSimulation(_, OracleExample0, _, yQubits, aQubit), IntAsDouble(power) * t0);
            let hsO1 = Coef(OracleHamiltonianSimulation(_, OracleExample1, _, yQubits, aQubit), IntAsDouble(power) * t0);

            ApplyTrotterSuzuki(2, 14, [hsO0, hsO1], xqubits);
            // ApplyTrotterSuzuki(2, 14, [hsO0, hsO1], xqubits);
        }

        // ApplyHHL(_UnitaryA_(_, _, yQubits, aQubit), stateVectorb);
        ApplyHHL(_Oracle0add1HamiltonianSimulation_(_, _, yQubits, aQubit), stateVectorb);
        DumpMachine();
        ResetAll(stateVectorb + yQubits + [aQubit]);

        ////////////////////////////////////Test Case4 - Scale Up////////////////////////////////
        // let n = _DefNumVecQubits_();
        // use stateVectorb = Qubit[n];
        // let nclock = _GetNumClockQubits_();
        // use yQubits = Qubit[nclock];
        // use aQubit = Qubit();
        // // PreparePureStateD(vector, stateVectorb);

        // internal operation _Oracle2HamiltonianSimulation_(power : Int, xqubits : Qubit[], yQubits : Qubit[], aQubit : Qubit) : Unit is Adj + Ctl {
        //     let t0 = _GetT0_();
        //     let hsO0 = Coef(OracleHamiltonianSimulation(_, OracleExample2Large, _, yQubits, aQubit), IntAsDouble(power) * t0);
        //     ApplyTrotterSuzuki(2, 14, [hsO0], xqubits);
        // }

        // // ApplyHHL(_UnitaryA_(_, _, yQubits, aQubit), stateVectorb);
        // ApplyHHL(_Oracle2HamiltonianSimulation_(_, _, yQubits, aQubit), stateVectorb);
        // DumpMachine();
        // ResetAll(stateVectorb + yQubits + [aQubit]);
    }

    operation HHLGateCountTest(size : Int) : Unit {
        use qb = Qubit[size];
        use qc = Qubit[size];
        use qy = Qubit[size];
        use qa = Qubit();
        internal operation _FakeOracleHS_(power : Int, phiQ : Qubit[], qy : Qubit[], qa : Qubit) : Unit is Adj + Ctl {
            // OracleHamiltonianSimulation(1., OracleExample2Large, phiQ, qy, qa);
            let hsO0 = Coef(OracleHamiltonianSimulation(_, OracleExample2Large, _, qy, qa), 1.);
            ApplyTrotterSuzuki(2, 14, [hsO0], phiQ);
        }

        ApplyHHL(_FakeOracleHS_(_, _, qy, qa), qb);
    }

    operation ShowEndien() : Unit {
        use q0 = Qubit();
        use q1 = Qubit();
        X(q1);
        // |01>
        let a = 0;
    }

    @EntryPoint()
    operation Main() : Unit {
        // OracleExample1UnitTest()
        // OracleExample0HamiltonianSimulationUnitTest();
        // OracleExample0UnitTest();
        // ShowEndien();
        // WGateUnitTest();
        // U3UnitTest();
        // TrotterSuzukiUnitTest();
        // PhaseEstimationUnitTest();
        // CRotationUnitTest();
        // let depth = EstimateDepth();
        // HHLUnitTest();
        // CReciprocalUnitTest();

        // PhaseEstimationDepthTest(2, 1);
        HHLGateCountTest(20);
    }
}