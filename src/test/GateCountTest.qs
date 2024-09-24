namespace HHLGateCountTest {
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


    operation OracleGateCount() : Unit {
        let h = [
            [2.5, 0., 0., 0.],
            [0., 3., 0., 0.],
            [0., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];
        let n = 2;

        use qx = Qubit[n];
        use qy = Qubit[n];
        use qr = Qubit[10];
        use qc = Qubit[5];
        Oracle(h, qx, qc, qy, qr);
        ResetAll(qx + qy + qr + qc);
    }

    operation GraphColoringOracleGateCount() : Unit {
        let time = 0.3;
        let n = 2;
        let s = 2;
        let numbits = 10;
        let h = [
            [2.5, 0., 0., 0.],
            [0., 3., 0., 0.],
            [0., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];
        use qx = Qubit[n];
        use qy = Qubit[n];
        use qr = Qubit[10];
        use qc = Qubit[5];
        GraphColoringOracle(h, qx, qc, qy, qr);
        ResetAll(qx + qy + qr + qc);
    }

    operation DeterministicCoinTossingGateCount() : Unit {
        let n = 2;
        let h = [
            [2.5, 0., 0., 0.],
            [0., 3., 0., 0.],
            [0., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];
        use qx = Qubit[n];
        use qy = Qubit[n];
        use qj = Qubit[n];
        use qk = Qubit[n];
        use qc = Qubit[5];
        DeterministicCoinTossing(UnweightedOracle(h, _, _, _, _), qx, qy, qj, qk, qc);

        ResetAll(qx + qy + qj + qk + qc);
    }

    operation OneSparseHamiltonianSimulationGateCount() : Unit {
        let time = 0.3;
        let n = 2;
        let numbits = 10;
        let h = [
            [2.5, 0., 0., 0.],
            [0., 3., 0., 0.],
            [0., 0., 0., 1.],
            [0., 0., 1., 0.]
        ];
        use qx = Qubit[n];
        ApplyOneSparseHamiltonianSimulation(time, h, numbits, qx);
        DumpMachine();
    }
}