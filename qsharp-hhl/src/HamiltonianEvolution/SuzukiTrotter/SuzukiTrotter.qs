namespace HamiltonianEvolution.SuzukiTrotter {
    import Microsoft.Quantum.Math.PI;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Unstable.StatePreparation;

    newtype PaulisWithCoef = (PauliList : Pauli[], Coef : Double);

    internal function _TrotterStepCoef_(order : Int, time : Double, pauliCoefLists : PaulisWithCoef[]) : PaulisWithCoef[] {
        if order == 1 {
            // return pauliCoefLists;
            mutable full = [];
            for idx in 0..Length(pauliCoefLists) - 1 {
                let (paulis, coef) = pauliCoefLists[idx]!;
                set full += [PaulisWithCoef(paulis, coef * time)];
            }
            return full;
        } elif order == 2 {
            mutable halves = [];
            for idx in 0..Length(pauliCoefLists) - 2 {
                let (paulis, coef) = pauliCoefLists[idx]!;
                set halves += [PaulisWithCoef(paulis, coef * time / 2.0)];
            }
            let full = [PaulisWithCoef(pauliCoefLists[Length(pauliCoefLists) - 1].PauliList, time * pauliCoefLists[Length(pauliCoefLists) - 1].Coef)];
            return halves + full + halves;
        } else {
            let reduction = 1.0 / (4.0 - 4.0^(1.0 / IntAsDouble(order - 1)));
            let halveOuter = _TrotterStepCoef_(order - 2, reduction * time, pauliCoefLists);
            let outer = halveOuter + halveOuter;
            let inner = _TrotterStepCoef_(order - 2, (1.0 - 4.0 * reduction) * time, pauliCoefLists);
            return outer + inner + outer;
        }
    }


    operation ApplySuzukiTrotter(order : Int, reps : Int, time : Double, pauliCoefLists : PaulisWithCoef[], qubits : Qubit[]) : Unit is Adj + Ctl {
        let singleRepCoef = _TrotterStepCoef_(order, time / IntAsDouble(reps), pauliCoefLists);
        for rep in 0..reps-1 {
            for i in 0..Length(singleRepCoef) - 1 {
                let (paulis, coef) = singleRepCoef[i]!;
                Exp(paulis, coef, qubits);
            }
        }
    }

    operation SuzukiTrotterUnitTest() : Unit {
        //  Expect:
        //  Basis | Amplitude      | Probability | Phase
        //  -----------------------------------------------
        //  |0⟩ | −1.0000+0.0000𝑖 |   100.0000% |   3.1416
        // let A is ((2,0), (0,0)),  e^i(A)t  = e^i(Z + I)t
        use targetQubit = Qubit();
        let eigenstateVector = [1.0, 0.0];
        PreparePureStateD(eigenstateVector, [targetQubit]);
        let pauliCoefZaddI = [PaulisWithCoef([PauliZ], PI() / 2.0), PaulisWithCoef([PauliI], PI() / 2.0)];
        ApplySuzukiTrotter(2, 14, 1.0, pauliCoefZaddI, [targetQubit]);

        // operation ExpiItdiv2_ExpiXt_ExpIdiv2(t : Double, qubit : Qubit) : Unit {
        //     Exp([PauliI], t / 2.0, [qubit]);
        //     Exp([PauliZ], t, [qubit]);
        //     Exp([PauliI], t / 2.0, [qubit]);
        // }

        // let reps = 14;
        // let t = PI() / 2.0;
        // for rep in 0..reps - 1 {
        //     ExpiItdiv2_ExpiXt_ExpIdiv2(t / IntAsDouble(reps), targetQubit);
        //     DumpMachine();
        // }

        DumpMachine();
        Reset(targetQubit);

    }
}
