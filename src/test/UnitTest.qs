namespace HHLUnitTest {
    open HHL.HamiltonianSimulation.GraphColoring;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Unstable.StatePreparation;

    open HHL;
    open HHL.PhaseEstimation;
    open HHL.HamiltonianSimulation;
    open HHL.CommonOperation;
    open HHL.HamiltonianSimulation.TrotterSuzuki;
    open HHL.HamiltonianSimulation.Oracle;

    operation TrotterSuzukiUnitTest() : Unit {
        //  Expect:
        //  Basis | Amplitude      | Probability | Phase
        //  -----------------------------------------------
        //  |0⟩ | −1.0000+0.0000𝑖 |   100.0000% |   3.1416
        // let A is ((2,0), (0,0)),  e^i(A)t  = e^i(Z + I)t
        use targetQubit = Qubit();
        let eigenstateVector = [1.0, 0.0];
        PreparePureStateD(eigenstateVector, [targetQubit]);
        let CoefZaddI = [Coef(Exp([PauliZ], _, _), PI() / 2.0), Coef(Exp([PauliI], _, _), PI() / 2.0)];
        ApplyTrotterSuzuki(2, 14, CoefZaddI, [targetQubit]);

        DumpMachine();
        Reset(targetQubit);

    }

    operation OneSparseHHLTest() : Unit {}


    operation OracleTest() : Unit {
        let h = [
            [2.5, 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];

        use qx = Qubit[2];
        use qj = Qubit[2];
        use qy = Qubit[2];
        use qr = Qubit[10];

        ApplyXorInPlace(3, qx);
        ApplyXorInPlace(0, qj);
        // ApplyXorInPlace(2, qy);
        // ApplyXorInPlace(64, qr);
        // DumpMachine();

        Oracle(h, qx, qj, qy, qr);
        DumpMachine();
        ResetAll(qx + qj + qy + qr);
    }

    operation ColorOracleTest() : Unit {
        let h = [
            [2.5, 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];

        use qx = Qubit[2];
        use qc = Qubit[7];
        use qy = Qubit[2];
        use qr = Qubit[10];

        ApplyXorInPlace(1, qx);
        ApplyXorInPlace(4, qc);
        // ApplyXorInPlace(2, qy);
        // ApplyXorInPlace(64, qr);
        // DumpMachine();

        let o = Oracle(h, _, _, _, _);
        let uwo = UnweightedOracle(h, _, _, _, _);
        GraphColoringOracle(o, uwo, qx, qc, qy, qr);
        DumpMachine();
        ResetAll(qx + qc + qy + qr);
    }

    operation FindNextNodeInPathUnitTest() : Unit {
        let h = [
            [2.5, 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., -5.],
            [0., 0., -5., 0.]
        ];

        use qx = Qubit[2];
        use qj = Qubit[2];
        use qk = Qubit[2];

        use qy = Qubit[2];

        ApplyXorInPlace(0, qx);
        ApplyXorInPlace(1, qj);
        ApplyXorInPlace(0, qk); // just to clearify


        let o = UnweightedOracle(h, _, _, _, _);
        FindNextVertexInPath(o, qx, qj, qk, qy);
        DumpRegister(qy);

        ResetAll(qx + qj + qk + qy);

    }

    operation DeterministicCoinTossingUnitTest() : Unit {
        let h = [
            [2.5, 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., -5.],
            [0., 0., -5., 0.]
        ];
        use qx = Qubit[2];
        use qy = Qubit[2];
        use qj = Qubit[2];
        use qk = Qubit[2];
        use qcolor = Qubit[3];

        ApplyXorInPlace(1, qx);
        ApplyXorInPlace(3, qy);
        ApplyXorInPlace(1, qj);
        ApplyXorInPlace(0, qk); // just to clearify


        let oHp = UnweightedOracle(h, _, _, _, _);

        DeterministicCoinTossing(oHp, qx, qy, qj, qk, qcolor);
        DumpRegister(qcolor);

        ResetAll(qx + qy + qj + qk + qcolor);
    }

    operation GraphColoringUnitTest() : Unit {
        let h = [
            [2.5, 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., -5.],
            [0., 0., -5., 0.]
        ];
        use qx = Qubit[2];
        use qj = Qubit[2];
        use qk = Qubit[2];
        use qcolor = Qubit[3];

        use qy = Qubit[2];
        use qr = Qubit[7]; // qw is not useful in coin tossing

        ApplyXorInPlace(1, qx);
        ApplyXorInPlace(0, qy); // just to clearify
        ApplyXorInPlace(0, qj);
        ApplyXorInPlace(0, qk);
        ApplyXorInPlace(0, qcolor);

        let qc = qj + qk + qcolor;

        let O = Oracle(h, _, _, _, _);
        let uwO = UnweightedOracle(h, _, _, _, _);

        GraphColoringOracle(O, uwO, qx, qc, qy, qr);
        DumpMachine();
        DumpRegister(qy);
        ResetAll(qx + qj + qk + qcolor + qy + qr);
    }

    operation ColorHamiltonianSimulationUnitTest() : Unit {
        let time = 0.2;
        use qx = Qubit[4];
        let ev = [0., 0., 1., -1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]; // eigen value = -1
        PreparePureStateDL(ev, qx);
        let H = [
            [0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 1., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
            [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        ];

        DumpMachine();
        ApplyColorHamiltonianSimulation(time, H, 10, 1, 0, 4, qx);
        DumpMachine();
        ResetAll(qx);

        // let ev = [0., 0., 0., 1., -1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]; // eigen value = -1
        // PreparePureStateDL(ev, qx);
        // let Hcolor10001 = [
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        // ];
        // DumpMachine();
        // ApplySparseHamiltonianSimulation(time, Hcolor10001, 10, qx);
        // DumpMachine();
        // ResetAll(qx);

    }


    operation SparseHamiltonianSimulationUnitTest() : Unit {
        let time = 0.2;
        use qx = Qubit[2];

        let ev = [-0.1, 0., 0.71, 0.70]; // eigen value = -1
        let h = [
            [2., 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., -5.],
            [0., 0., -5., 0.]
        ];
        PreparePureStateDL(ev, qx);
        // let h = [
        //     [0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 1., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 1., 0., 1., 1., 0., 0., 0., 0., 0., 0., 0., 1., 0., 0.],
        //     [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 1., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.],
        //     [0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.]
        // ];

        // DumpMachine();
        // ApplyColorHamiltonianSimulation(time, h, 7, 0, 0, 0, qx);
        ApplySparseHamiltonianSimulation(time, 2, h, 10, qx);
        DumpMachine();
        ResetAll(qx);
    }

    operation HHLSimulationUnitTest() : Unit {
        let A = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ];

        let b = [2., -3., 1., 1., 1., 0., 0.,-2.];

        HHLSimulation(A, b);
    }

    operation WGateFailedTest() : Unit {
        // use q = Qubit[2];
        // PreparePsiMinus(q);
        // DumpMachine();
        use qx = Qubit[2];
        // use qy = Qubit[2];
        use qt = Qubit[2];
        // use qt2 = Qubit[2];

        X(qx[0]);
        within {
            ExactWGate(qx + qt);
        } apply {

            DumpRegister(qx);
        }
        DumpMachine();
        ResetAll(qx + qt);

        // let qx0y0 = [qx[0]] + [qy[0]];
        // let qx1qy1 = [qx[1]] + [qy[1]];



        // ZipOp(WGate, qx, qy);


    }

    operation FailedUnitTest() : Unit {
        let time = 1. / 30.;
        let h = [
            [2.5, 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];
        let numbits = 10;
        let j = 1;
        let k = 0;
        let color = 0;
        use qx = Qubit[2];
        ApplyXorInPlace(2, qx);
        ApplyColorHamiltonianSimulation(time, h, numbits, j, k, color, qx);

        // DumpRegister
        ResetAll(qx);
        // use qx = Qubit[2];

    }

    operation OneSparseHHLUnitTest() : Unit {
        let h = [
            [2.5, 0., 0., 0.],
            [0., 3., 0., 0.],
            [0., 0., 0.,-1.],
            [0., 0., -1., 0.]
        ];
        let x = [2., 0., 1., 7.];
        OneSparseHHLSimulation(h, x);
    }

    operation HHLUnitTest() : Unit {
        let h = [
            [2.5, 0., 1., 0.],
            [0., 3., 0., 0.],
            [1., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];
        let x = [2., 3., 1., 0.];
        HHLSimulation(h, x);
    }
}

    