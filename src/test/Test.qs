namespace Test {
    // open HHLGateCountTest;
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
        // OneSparseHHLUnitTest();
  
        StdGateSetCounting(OracleGateCount, 2);


    }
}