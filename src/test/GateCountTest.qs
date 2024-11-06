namespace HHLGateCountTest {
    import Std.Diagnostics.StopCountingOperation;
    import Std.Diagnostics.StartCountingOperation;
    import Std.Diagnostics.StartCountingFunction;
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


    operation StdGateSetCounting(op : (Int => Unit), n : Int) : Unit {
        StartCountingOperation(H);
        StartCountingOperation(X);
        StartCountingOperation(Y);
        StartCountingOperation(Z);
        StartCountingOperation(S);
        StartCountingOperation(T);
        StartCountingOperation(Rx);
        StartCountingOperation(Ry);
        StartCountingOperation(Rz);
        StartCountingOperation(CNOT);
        StartCountingOperation(CZ);
        StartCountingOperation(CY);
        StartCountingOperation(CCNOT);
        StartCountingOperation(M);

        StartCountingOperation(Oracle);
        StartCountingOperation(UnweightedOracle);

        op(n);

        let HCount = StopCountingOperation(H);
        let XCount = StopCountingOperation(X);
        let YCount = StopCountingOperation(Y);
        let ZCount = StopCountingOperation(Z);
        let SCount = StopCountingOperation(S);
        let TCount = StopCountingOperation(T);
        let RxCount = StopCountingOperation(Rx);
        let RyCount = StopCountingOperation(Ry);
        let RzCount = StopCountingOperation(Rz);
        let CNOTCount = StopCountingOperation(CNOT);
        let CZCount = StopCountingOperation(CZ);
        let CYCount = StopCountingOperation(CY);
        let CCNOTCount = StopCountingOperation(CCNOT);
        let MCount = StopCountingOperation(M);

        let OracleCount = StopCountingOperation(Oracle);
        let UniweightedOracleCount = StopCountingOperation(UnweightedOracle);


        Message($"X count: {XCount}");
        Message($"Y count: {YCount}");
        Message($"Z count: {ZCount}");
        Message($"S count: {SCount}");
        Message($"T count: {TCount}");
        Message($"Rx count: {RxCount}");
        Message($"Ry count: {RyCount}");
        Message($"Rz count: {RzCount}");
        Message($"CNOT count: {CNOTCount}");
        Message($"CZ count: {CZCount}");
        Message($"CY count: {CYCount}");
        Message($"CCNOT count: {CCNOTCount}");
        Message($"M count: {MCount}");
        Message($"Oracle count: {OracleCount}");
        Message($"UnweightedOracle count: {UniweightedOracleCount}");
    }

    operation OracleGateCount(n : Int) : Unit {
        let h = GenerateZeroMatrix(n);

        use qx = Qubit[n];
        use qy = Qubit[n];
        use qr = Qubit[10];
        use qc = Qubit[5];
        Oracle(h, qx, qc, qy, qr);
        ResetAll(qx + qy + qr + qc);
    }

    // same as oracle
    operation UnweightedOracleGateCount(n : Int) : Unit {

        let h = GenerateZeroMatrix(n);

        use qx = Qubit[n];
        use qy = Qubit[n];
        use qr = Qubit();
        use qc = Qubit[5];
        UnweightedOracle(h, qx, qc, qy, qr);

        ResetAll(qx + qy + [qr] + qc);
    }

    operation GraphColoringOracleGateCount(n : Int) : Unit {
        let time = 0.3;
        let s = 2;
        let numbits = 10;
        let h = GenerateZeroMatrix(n);
        use qx = Qubit[n];
        use qy = Qubit[n];
        use qr = Qubit[10];
        use qc = Qubit[5];
        GraphColoringOracle(h, qx, qc, qy, qr);
        ResetAll(qx + qy + qr + qc);
    }

    operation DeterministicCoinTossingGateCount(n : Int) : Unit {
        let h = GenerateZeroMatrix(n);
        use qx = Qubit[n];
        use qy = Qubit[n];
        use qj = Qubit[n];
        use qk = Qubit[n];
        use qc = Qubit[5];
        DeterministicCoinTossing(UnweightedOracle(h, _, _, _, _), qx, qy, qj, qk, qc);

        ResetAll(qx + qy + qj + qk + qc);
    }

    operation OneSparseHamiltonianSimulationGateCount(n : Int) : Unit {


        let time = 0.3;
        let numbits = 10;
        let h = GenerateZeroMatrix(2^n);
        use qx = Qubit[n];
        ApplyOneSparseHamiltonianSimulation(time, h, numbits, qx);
        DumpMachine();
    }
}