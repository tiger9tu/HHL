namespace Test {
    // open HHLGateCountTest;
    import HHL.HamiltonianSimulation.NCNOT;
    import Std.Diagnostics.StopCountingOperation;
    import Std.Diagnostics.StartCountingOperation;
    import HHL.HamiltonianSimulation.Oracle.Oracle;
    import HHL.HamiltonianSimulation.Oracle.UnweightedOracle;
    import HHL.OneSparseHHLSimulation;
    import HHL.CommonOperation.SumIntArray;
    import HHL.HamiltonianSimulation.U1Gate;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    import HHL.CommonOperation.PreparePureStateDL;
    open HHLUnitTest;
    open Microsoft.Quantum.Math;
    open HHL.HamiltonianSimulation.GraphColoring;
    open HHLGateCountTest;


    @EntryPoint()
    operation Main() : Unit {
        // OneSparseHamiltonianSimulationGateCount(2);
        // WgateGateCount(2);
        // U1GateGateCount();
        use qubits = Qubit[1];
        Rz(1.0, qubits[0]);
        // NCNOT(qubits[0..1], qubits[2]);
    }
}