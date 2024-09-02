namespace Test {
    open HHLGateCountTest;
    open HHLUnitTest;

    @EntryPoint()
    operation Main() : Unit {
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
        // HHLGateCountTest();
        // PhaseEstimationGateCountTest(24, 8);
        
        // HamiltonianSimulationGateCountTest(24);
        // ReciprocalGateCountTest(12);
        HamiltonianSimulationGateCountTest(0.02, 24,1, 0.1, 2.,3);
        
        // CReciprocalUnitTest();

        // PhaseEstimationDepthTest(2, 1);
        // HHLGateCountTest(20);
    }
}