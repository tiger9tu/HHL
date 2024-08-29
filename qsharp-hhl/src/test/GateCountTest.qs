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
        ApplyPhaseEstimation(PowerUNoting, clockQubits, phiQubits);
    }

    // function GetTrotterRep

    operation HHLGateCountTest(qbSize : Int, qcSize : Int, trotterReps : Int) : Unit {
        use qb = Qubit[qbSize];
        use qc = Qubit[qcSize];
        use qy = Qubit[qbSize];
        use qa = Qubit();

        internal operation _FakeOracleHS_(trotterReps : Int, power : Int, phiQ : Qubit[], qy : Qubit[], qa : Qubit) : Unit is Adj + Ctl {
            // OracleHamiltonianSimulation(1., OracleExample2Large, phiQ, qy, qa);
            let hsO0 = Coef(OracleHamiltonianSimulation(_, OracleExample2Large, _, qy, qa), 1.);
            ApplyTrotterSuzuki(2, trotterReps, [hsO0], phiQ);
        }

        // ApplyHHL(_FakeOracleHS_(trotterReps, _, _, qy, qa), qb);
    }


}