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

    operation ReciprocalGateCountTest(nc : Int) : Unit {
        use qc = Qubit[nc];
        use qa = Qubit();
        ApplyCReciprocal(0.1,true, qc,qa);
    }

    // operation tcontrol(q : Qubit[]) : Unit is Ctl {
    //     H(q[0]);
    //     H(q[1]);
    //     X(q[1]);
    // }

    // operation test(qc : Qubit, q2 : Qubit[]) : Unit {
    //     // use qc = Qubit();
    //     // use q2 = Qubit[2];
    //     // Controlled H([qc],q2[0]);
    //     Controlled tcontrol([qc],(q2));
    // }

    
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

    operation HamiltonianSimulationGateCountTest(nx : Int) : Unit {
    //     newtype HSConfig = (
    //     real : Bool,
    //     sparsity : Int,
    //     epsilon : Double,
    //     // for bounding the error of trotter
    //     maxH : Double,
    //     cTrotter : Double,
    //     verticeQueries : Int,
    // );
        // let nqx = 8;
        // use qx = Qubit[nqx];
        // use qy = Qubit[nqx];
        // use qa = Qubit();
        // let hsConfig = HSConfig(false, 10, 0.1, 2.,0.1,7);
        // let time = 2. *PI() * 0.5;
        // let simulateSparseOracle = repeatOp(hsConfig.verticeQueries, OracleEmpty, _);
        // OracleSparseHamiltonianSimulationFake(hsConfig, time, simulateSparseOracle,qx,qy,qa);
        use qx = Qubit[nx];
        use qy = Qubit[nx];
        use qa = Qubit();
        OracleHamiltonianSimulation(0.2, OracleEmpty, qx,qy,qa);

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