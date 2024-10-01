namespace Test {
    // open HHLGateCountTest;
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
        // simple demo
        OneSparseHHLUnitTest();

        // this may take time to run
        // HHLUnitTest();
        // OracleGateCount();
        // GraphColoringOracleGateCount();
        // DeterministicCoinTossingGateCount();
        // GraphColoringUnitTest();
        // OneSparseHamiltonianSimulationGateCount();


    }
}