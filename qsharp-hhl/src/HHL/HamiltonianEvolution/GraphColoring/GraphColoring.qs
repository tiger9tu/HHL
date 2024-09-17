namespace HHL.HamiltonianSimulation.GraphColoring {
    import HHL.CommonOperation.ApplyBitwiseCNOT;
    import HHL.CommonOperation.SwapRegs;
    import HHL.CommonOperation.ApplyGetEqualty;
    import Microsoft.Quantum.Unstable.Arithmetic.ApplyIfEqualL;
    import Microsoft.Quantum.Arrays.Head;
    import HHL.CommonOperation.SumIntArray;
    import Microsoft.Quantum.Arrays.Fold;
    import Microsoft.Quantum.Math.Lg;
    import Microsoft.Quantum.Math.Ceiling;
    import HHL.HamiltonianSimulation.CNNOT;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;

    internal function GetFirst1AtNBitString(n : Int) : Bool[] {
        mutable bitString = Repeated(false, n + 1);
        set bitString w/= n <- true;
        bitString
    }

    operation GetLabel(preXiQubits : Qubit[], preYiQubits : Qubit[], xiQubits : Qubit[]) : Unit is Adj + Ctl {
        // get the color label of the next xi
        // xi Qubits is initially 0
        let lenPre = Length(preXiQubits);
        use aQubits = Qubit[lenPre];
        within {
            // if preXi[j] == preYi[j] then aQubis[j] == |0>
            ApplyBitwiseCNOT(preXiQubits, aQubits);
            ApplyBitwiseCNOT(preYiQubits, aQubits);
        } apply {
            for j in 0..lenPre - 1 {
                let first1AtNBitString = GetFirst1AtNBitString(j);
                ApplyControlledOnBitString(first1AtNBitString, ApplyXorInPlace(j, _), aQubits, xiQubits);
            }
        }
    }

    internal function GetLogStarN(n : Int) : Int {
        mutable nIter = n;
        mutable logStarN = 0;
        while nIter > 3 {
            set nIter = Ceiling(Lg(IntAsDouble(nIter)));
            set logStarN += 1;
        }
        logStarN
    }

    internal function GetLenXiList(lenX0 : Int) : Int[] {
        let logStarN = GetLogStarN(lenX0);
        mutable lenXiList = Repeated(0, logStarN + 1);

        set lenXiList w/= 0 <- lenX0;

        for i in 1..logStarN - 1 {
            set lenXiList w/= i <- Ceiling(Lg(IntAsDouble(lenXiList[i - 1])));
        }

        set lenXiList w/= logStarN <- 3;

        lenXiList
    }

    internal function GetTotalCoinQubitsNum(lenXiList : Int[]) : Int {
        mutable num = 0;
        let length = Length(lenXiList);
        for i in 0..length - 1 {
            let numVertices = length - i;
            set num += lenXiList[i] * numVertices;
        }
        num
    }

    internal operation CoinTossingStep(preVertocesRegs : Qubit[][], verticesRegs : Qubit[][]) : Unit is Adj + Ctl {
        let lenVertices = Length(verticesRegs);
        Fact(Length(preVertocesRegs) == lenVertices + 1, "CoinTossingStep: each step the number of vertices must reduce by 1.");
        for i in 0..lenVertices {
            GetLabel(preVertocesRegs[i], preVertocesRegs[i + 1], verticesRegs[i]);
        }
    }

    internal operation FindNextNodeInPath(oracle : (Qubit[], Qubit[], Qubit[]) => Unit is Adj + Ctl, xQubits : Qubit[], yQubits : Qubit[], cQubits : Qubit[], zQubits : Qubit[]) : Unit is Adj + Ctl {
        // we know x,y want to find vertex z that the (j,k) of x--y is equal to that of y--z. In other words, we want to find next node z in the "path"
        // we have j and k in cQubits, cQubits = |j>|k>|ccc> or |k>|j>|ccc> doesn't matter.
        // there are three possibilities:
        //    1.oracle|y>|c[0..lenjOrk-1]>|0> = |y>|c[0..lenjOrk-1]>|z>
        //    2.oracle|y>|c[0..lenjOrk-1]>|0> = |y>|c[0..lenjOrk-1]>|x>
        //            => oracle|y>|c[lenjOrk..2*lenjOrk-1]>|0> = |y>|c[c[lenjOrk..2*lenjOrk-1]>|z>
        //    3.x == y we come to this later

        use aQubits = Qubit[Length(yQubits)];
        let lenjOrk = (Length(cQubits) - 3) / 2;
        let cHeadQubits = cQubits[0..lenjOrk -1];
        oracle(yQubits, cHeadQubits, aQubits);

        use ifEqualQubit = Qubit();

        within {
            ApplyGetEqualty(xQubits, aQubits, ifEqualQubit);

        } apply {

            // if not equal, then the first case
            within {
                X(ifEqualQubit);
            } apply {
                Controlled SwapRegs([ifEqualQubit], (aQubits, zQubits));
            }

            // if equal the the second case
            let cMidQubits = cQubits[lenjOrk..2 * lenjOrk-1];

            Controlled oracle([ifEqualQubit], (yQubits, cMidQubits, zQubits));
            Controlled ApplyBitwiseCNOT([ifEqualQubit], (xQubits, aQubits)); // clean aQubits
        }

    }

    internal operation DeterministicCoinTossing(oracle : (Qubit[], Qubit[], Qubit[]) => Unit is Adj + Ctl, xQubits : Qubit[], yQubits : Qubit[], cQubits : Qubit[]) : Unit is Adj + Ctl {
        // prepare the color qubits
        // the color qubits is initially |j>|k>|000>
        // we assign the additional 3 digits color
        let lenX0Reg = Length(xQubits);
        let logStarN = GetLogStarN(lenX0Reg);

        let lenXiList = GetLenXiList(lenX0Reg);
        let numCoinQubits = GetTotalCoinQubitsNum(lenXiList);
        use aQubits = Qubit[numCoinQubits - 2 * Head(lenXiList) - 3];

        // assign the start value
        let totalQubits = xQubits + yQubits + aQubits + cQubits[Length(cQubits) - 3..Length(cQubits)-1];

        // for the first round, find all the vertices connected in the path
        let numVertices = logStarN + 1;
        for i in 2..numVertices {
            let xIterQubits = totalQubits[(i-2) * lenX0Reg..(i-1) * lenX0Reg-1];
            let yIterQubits = totalQubits[(i-1) * lenX0Reg..i * lenX0Reg-1];
            let zIterQubits = totalQubits[i * lenX0Reg..(i + 1) * lenX0Reg-1];
            FindNextNodeInPath(oracle, xIterQubits, yIterQubits, cQubits, zIterQubits);
        }


        for i in 1..logStarN {
            


        }


    }

}


