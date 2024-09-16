namespace Test {
    // open HHLGateCountTest;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    import HHL.CommonOperation.PreparePureStateDL;
    open HHLUnitTest;
    open Microsoft.Quantum.Math;

    @EntryPoint()
    operation Main() : Unit {

        HHLSimulationUnitTest();
        // OracleHamiltonianSimulationUnitTest(0.4);
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
        // OracleExample1UnitTest();
        // QRAMOracleUnitTest();
        // OracleHamiltonianSimulationUnitTest(0.4);

        // HHLGateCountTest();
        // PhaseEstimationGateCountTest(24, 8);

        // HamiltonianSimulationGateCountTest(24);
        // ReciprocalGateCountTest(12);
        // HamiltonianSimulationGateCountTest(0.02, 4,3, 0.1, 2.,3);
        // PhaseEstimationGateCountTest(4, 4, 0.02);
        // OracleExample0HamiltonianSimulationUnitTest();

        // CReciprocalUnitTest();
        // OracleHamiltonianSimulationUnitTest(2. * PI()  / 2.^3.);
        // PhaseEstimationDepthTest(2, 1);
        // HHLGateCountTest(20);
    }
}