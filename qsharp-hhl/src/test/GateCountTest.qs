namespace HHLGateCountTest {
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
    
    operation PhaseEstimationGateCountTest(nClock : Int, nPhi : Int) : Unit {
        use clockQubits = Qubit[nClock];
        use phiQubits = Qubit[nPhi];

        operation PowerUNoting(power : Int, qubits : Qubit[]) : Unit is Ctl + Adj {
            UNothing(qubits);
        }

        // let myOp = q => UNothing(q);
        StartCountingOperation(Controlled UNothing);
        ApplyPhaseEstimation(PowerUNoting, clockQubits, phiQubits);
        let UCount = StopCountingOperation(Controlled UNothing);

        Message($"controlled unitary calls : {UCount}");
    }

    // function GetTrotterRep

    operation HHLGateCountTest() : Unit {
        
        // newtype HHLConfig = (
        //     N : Int,
        //     sparsity : Int,
        //     kappa : Double,
        //     C : Double, 
    
        //     epsilon : Double,
        //     negVal : Bool,
        //     repeatitive : Bool,

        //     // for bounding the error of trotter
        //     maxH : Double,
        //     cTrotter : Double,
        //     verticeQueries : Int, // calls to simulate one sparse hamiltonian

        //     cQPE : Double,

        // );

        let config = HHLConfig(2^3, 5,4.,0., 0.1, false, false, 3., 0.1, 7, 0.1);
        let n = Ceiling(Lg(IntAsDouble(config.N)));

        use yQubits = Qubit[n];
        use bQubits = Qubit[n];
        use aQubit = Qubit();

        StartCountingOperation(OracleEmpty);
        ApplyHHL(config, OracleEmpty, bQubits);

        let oracleCalls = StopCountingOperation(OracleEmpty);
        Message($"Oracle calls = {oracleCalls}");
    }


}