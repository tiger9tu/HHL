namespace HHLUnitTest {
    import HHL.HamiltonianSimulation.GraphColoring.DeterministicCoinTossing;
    import HHL.HamiltonianSimulation.GraphColoring.GetLabel;
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

    operation OracleUnitTest() : Unit {
        // it's for further testing coin tossing
        let H = [
            [0., 1., 0., 0., 0., 0., 0., 0.],
            [1., 0., 1., 0., 0., 0., 0., 0.],
            [0., 1., 0., 1., 0., 0., 0., 0.],
            [0., 0., 1., 0., 1., 1., 0., 0.],
            [0., 0., 0., 1., 0., 0., 0., 0.],
            [0., 0., 0., 1., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0.]
        ];
        use qx = Qubit[3];
        use qj = Qubit[3];
        use qy = Qubit[3];
        use qr = Qubit[4];


        let oH = Oracle(H, _, _, _, _);
        within {
            X(qx[2]);
        } apply {
            oH(qx, qj, qy, qr);
            DumpMachine();
        }

        ResetAll(qx + qj + qy + qr);
    }

    operation DeterministicCoinTossingUnitTest() : Unit {
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
        use qx = Qubit[4];
        use qj = Qubit[4];
        use qy = Qubit[4];
        use qrTrash = Qubit[4]; // qw is not useful in coin tossing
        use qj = Qubit[3];
        use qk = Qubit[3];
        use qcolor = Qubit[3];

        ApplyXorInPlace(3, qx);
        ApplyXorInPlace(13, qy);
        ApplyXorInPlace(1, qj);
        ApplyXorInPlace(0, qk); // just to clearify

        let qc = qj + qk + qcolor;


        let oHp = Oracle(H, _, _, _, qrTrash);
        DeterministicCoinTossing(oHp, qx, qy, qc);
        DumpMachine();

        ResetAll(qx + qj + qy + qrTrash + qc);
    }

    operation HamiltonianSimulationUnitTest() : Unit {
        let time = 0.2;
        use qx = Qubit[2];
        let state = [1.,-1., 0., 0.];
        PreparePureStateDL(state, qx);
        let h = [
            [0.0, 2.5, 0.0, 0.0],
            [2.5, 0.0, 0.0, 0.0],
            [0.0, 0.0, 2.5, 0.0],
            [0.0, 0.0, 0.0, 2.5]
        ];
        DumpMachine();
        ApplyHamiltonianSimulation(time, h, 10, qx);
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

        let b = [2., -3., 1., 1., 2., 1., 0.,-2.];

        HHLSimulation(A, b);
    }

}