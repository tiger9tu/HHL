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
    open Microsoft.Quantum.Diagnostics;
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

    internal function GetRegRInt(a : Double, n : Int) : Int {
        // real value - > fraction(2n bits)--integer(n bits)--sign(1 bit)
        // little-endian

        let sign = a < 0.;

        let absA = AbsD(a);

        let aInt = Floor(absA); // Integer part of a
        let rIntBin = IntToBinaryVector(aInt, n);

        let aFrac = absA - IntAsDouble(aInt); // Fractional part of a
        let rFracBin = FracToBinaryVector(aFrac, 2 * n);

        // Message($"bin = {[sign] + rFracBin + rIntBin}");
        BinaryVecToInt(rFracBin + rIntBin + [sign])
    }

    // internal function RealToBinary
    operation Oracle(H : Double[][], qx : Qubit[], qj : Qubit[], qy : Qubit[], qr : Qubit[]) : Unit is Adj + Ctl {
        let lengthr = Length(qr);
        Fact((lengthr - 1) % 3 == 0, "Length(qr) must be 3r + 1.");
        let nr = (lengthr - 1) / 3;

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
                    ApplyControlledOnInt(cint, ApplyXorInPlace(GetRegRInt(w, nr), _), qx + qj, qr);
                }
            }
        }
    }

}