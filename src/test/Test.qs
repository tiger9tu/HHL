namespace Test {
    // open HHLGateCountTest;
    import HHL.CommonOperation.SumIntArray;
    import HHL.HamiltonianSimulation.U1Gate;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    import HHL.CommonOperation.PreparePureStateDL;
    open HHLUnitTest;
    open Microsoft.Quantum.Math;
    open HHL.HamiltonianSimulation.GraphColoring;

    @EntryPoint()
    operation Main() : Unit {
        DeterministicCoinTossingUnitTest();
        // let
        // OracleUnitTest();
        // let id = GetXiStartIdx([9, 4, 3], 2);
        // let (s, e) = GetXiTotalRange([9, 4, 3], 2);
        // Message($"s = {s},{e}.");
        // Message($"{[i for i in 0..4]}");
        // Message($"a[0..0] = {a[0..0]}; suma[0..-1] = {SumIntArray(a[0..-1])}");
        // DeterministicCoinTossing();
        // OracleUnitTest();
        // WeightedOracleHamiltonianSimulationUnitTest();
        // RealOracleHamiltonianSimulationUnitTest();
        // HHLSimulationUnitTest();
    }
}