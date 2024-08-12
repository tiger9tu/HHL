namespace HamiltonianSimulation.TrotterSuzuki {
    import Microsoft.Quantum.Math.PI;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Unstable.StatePreparation;

    newtype Coef = (HamiltonianSimulator : (Double, Qubit[]) => Unit is Adj + Ctl, time : Double);

    internal function _TrotterStepCoef_(order : Int, reduction : Double, CoefLists : Coef[]) : Coef[] {
        if order == 1 {
            mutable full = [];
            for idx in 0..Length(CoefLists) - 1 {
                let (ha, time) = CoefLists[idx]!;
                set full += [Coef(ha, reduction * time)];
            }
            return full;

        } elif order == 2 {
            mutable halves = [];
            for idx in 0..Length(CoefLists) - 2 {
                let (ha, time) = CoefLists[idx]!;
                set halves += [Coef(ha, reduction * time / 2.0)];
            }
            let middle = CoefLists[Length(CoefLists) - 1];
            let full = [Coef(middle.HamiltonianSimulator, middle.time * reduction)];
            return halves + full + halves;
        } else {
            let newReduction = 1.0 / (4.0 - 4.0^(1.0 / IntAsDouble(order - 1)));
            let halveOuter = _TrotterStepCoef_(order - 2, newReduction * reduction, CoefLists);
            let outer = halveOuter + halveOuter;
            let inner = _TrotterStepCoef_(order - 2, (1.0 - 4.0 * newReduction) * reduction, CoefLists);
            return outer + inner + outer;
        }
    }


    operation ApplyTrotterSuzuki(order : Int, reps : Int, CoefLists : Coef[], qubits : Qubit[]) : Unit is Adj + Ctl {
        let singleRepCoef = _TrotterStepCoef_(order, 1.0 / IntAsDouble(reps), CoefLists);
        for rep in 0..reps-1 {
            for i in 0..Length(singleRepCoef) - 1 {
                let (ha, time) = singleRepCoef[i]!;
                // Exp(s, coef, qubits);
                ha(time, qubits);
            }
        }
    }

    operation TrotterSuzukiUnitTest() : Unit {
        //  Expect:
        //  Basis | Amplitude      | Probability | Phase
        //  -----------------------------------------------
        //  |0⟩ | −1.0000+0.0000𝑖 |   100.0000% |   3.1416
        // let A is ((2,0), (0,0)),  e^i(A)t  = e^i(Z + I)t
        use targetQubit = Qubit();
        let eigenstateVector = [1.0, 0.0];
        PreparePureStateD(eigenstateVector, [targetQubit]);
        let CoefZaddI = [Coef(Exp([PauliZ], _, _), PI() / 2.0), Coef(Exp([PauliI], _, _), PI() / 2.0)];
        ApplyTrotterSuzuki(2, 14, CoefZaddI, [targetQubit]);

        DumpMachine();
        Reset(targetQubit);

    }


    newtype PauliCoef = (PauliList : Pauli[], Coef : Double);
    internal function _TrotterStepPauliCoef_(order : Int, time : Double, pauliCoefLists : PauliCoef[]) : PauliCoef[] {
        if order == 1 {
            // return pauliCoefLists;
            mutable full = [];
            for idx in 0..Length(pauliCoefLists) - 1 {
                let (paulis, coef) = pauliCoefLists[idx]!;
                set full += [PauliCoef(paulis, coef * time)];
            }
            return full;
        } elif order == 2 {
            mutable halves = [];
            for idx in 0..Length(pauliCoefLists) - 2 {
                let (paulis, coef) = pauliCoefLists[idx]!;
                set halves += [PauliCoef(paulis, coef * time / 2.0)];
            }
            let full = [PauliCoef(pauliCoefLists[Length(pauliCoefLists) - 1].PauliList, time * pauliCoefLists[Length(pauliCoefLists) - 1].Coef)];
            return halves + full + halves;
        } else {
            let reduction = 1.0 / (4.0 - 4.0^(1.0 / IntAsDouble(order - 1)));
            let halveOuter = _TrotterStepPauliCoef_(order - 2, reduction * time, pauliCoefLists);
            let outer = halveOuter + halveOuter;
            let inner = _TrotterStepPauliCoef_(order - 2, (1.0 - 4.0 * reduction) * time, pauliCoefLists);
            return outer + inner + outer;
        }
    }


    operation ApplyPauliTrotterSuzuki(order : Int, reps : Int, time : Double, pauliCoefLists : PauliCoef[], qubits : Qubit[]) : Unit is Adj + Ctl {
        let singleRepCoef = _TrotterStepPauliCoef_(order, time / IntAsDouble(reps), pauliCoefLists);
        for rep in 0..reps-1 {
            for i in 0..Length(singleRepCoef) - 1 {
                let (paulis, coef) = singleRepCoef[i]!;
                Exp(paulis, coef, qubits);
            }
        }
    }

    operation PauliTrotterSuzukiUnitTest() : Unit {
        //  Expect:
        //  Basis | Amplitude      | Probability | Phase
        //  -----------------------------------------------
        //  |0⟩ | −1.0000+0.0000𝑖 |   100.0000% |   3.1416
        // let A is ((2,0), (0,0)),  e^i(A)t  = e^i(Z + I)t
        use targetQubit = Qubit();
        let eigenstateVector = [1.0, 0.0];
        PreparePureStateD(eigenstateVector, [targetQubit]);
        let pauliCoefZaddI = [PauliCoef([PauliZ], PI() / 2.0), PauliCoef([PauliI], PI() / 2.0)];
        ApplyPauliTrotterSuzuki(2, 14, 1.0, pauliCoefZaddI, [targetQubit]);

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
