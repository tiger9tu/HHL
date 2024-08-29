namespace HHL.HamiltonianSimulation.TrotterSuzuki {
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
                // Message($"time = {time}");
                ha(time, qubits);
            }
        }
    }

}
