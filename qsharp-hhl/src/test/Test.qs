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
        PhaseEstimationGateCountTest(10, 5);
        
        // CReciprocalUnitTest();

        // PhaseEstimationDepthTest(2, 1);
        // HHLGateCountTest(20);
    }
}