namespace HHL.HamiltonianSimulation.Oracle {
    // Precompiled by qiskit qs_decomposition

    import Microsoft.Quantum.Arrays.Mapped;
    import HHL.ApplyCReciprocal;
    import Microsoft.Quantum.Unstable.StatePreparation.PreparePureStateD;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open HHL.CommonOperation;

    internal function GetJ(HRow : Double[], y : Int) : Int {
        // can't set mutable inside a adjoint operation..
        mutable j = 0;
        for i in 0..y-1 {
            if HRow[i] != 0. {
                set j = j + 1;
            }
        }
        j
    }

    operation Oracle(H : Double[][], qx : Qubit[], qj : Qubit[], qy : Qubit[], qr : Qubit[]) : Unit is Adj + Ctl {
        for x in 0..Length(H)- 1 {
            ApplyControlledOnInt(x, ApplyXorInPlace(x, _), qx, qy);
            for y in 0..Length(H) -1 {
                let j = GetJ(H[x][0..Length(H)-1], y);
                let cint = x + j * 2^(Length(qx));
                let w = H[x][y];
                if w != 0. {
                    // little-endian
                    ApplyControlledOnInt(cint, ApplyXorInPlace(x, _), qx + qj, qy); // cancel the previous effect
                    ApplyControlledOnInt(cint, ApplyXorInPlace(y, _), qx + qj, qy);
                    ApplyControlledOnInt(cint, ApplyXorInPlace(Ceiling(w), _), qx + qj, qr);
                }
            }
        }

    }
}