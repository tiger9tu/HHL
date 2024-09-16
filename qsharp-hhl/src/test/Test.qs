namespace Test {
    // open HHLGateCountTest;
    import HHL.HamiltonianSimulation.U1Gate;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    import HHL.CommonOperation.PreparePureStateDL;
    open HHLUnitTest;
    open Microsoft.Quantum.Math;

    @EntryPoint()
    operation Main() : Unit {

        // OracleUnitTest();
        // WeightedOracleHamiltonianSimulationUnitTest();
        // RealOracleHamiltonianSimulationUnitTest();
        HHLSimulationUnitTest();
    }
}