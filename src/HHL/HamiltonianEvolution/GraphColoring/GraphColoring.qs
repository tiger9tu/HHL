namespace HHL.HamiltonianSimulation.GraphColoring {
    import HHL.CommonOperation.ApplyBitwiseXOR;
    import HHL.CommonOperation.SliceArray;
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
        // xi = position of the first different digit -- the different digit
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
                // get position of the first digit
                ApplyControlledOnBitString(first1AtNBitString, ApplyXorInPlace(j, _), aQubits[0..j], xiQubits[0..Length(xiQubits)-2]);
                // copy the different digit to xi
                ApplyControlledOnBitString(first1AtNBitString, CNOT(preXiQubits[j], _), aQubits[0..j], xiQubits[Length(xiQubits)-1]);
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


    internal operation CoinTossingStep(preRegLen : Int, regLen : Int, preVerticesRegs : Qubit[], verticesRegs : Qubit[]) : Unit is Adj + Ctl {
        let numVertices = Length(verticesRegs) / regLen;
        // Message($"preRegLen : {preRegLen}; RegLen : {regLen}; Length(preRegVerticesRegs) : {Length(preVerticesRegs)} Length(verticesRegs) :{Length(verticesRegs)}.");
        Fact(Length(verticesRegs) % regLen == 0, "ConTossingStep: the regLen must divide verticesRegs.");
        Fact(Length(preVerticesRegs) % preRegLen == 0, "ConTossingStep: the preRegLen must divide preVerticesRegs.");
        Fact(Length(preVerticesRegs) / preRegLen == numVertices + 1, "CoinTossingStep: each step the number of vertices must reduce by 1.");

        for i in 0..numVertices - 1 {
            let preXiQubits = SliceArray(preVerticesRegs, i, preRegLen);
            let preYiQubits = SliceArray(preVerticesRegs, i + 1, preRegLen);
            let xiQubits = SliceArray(verticesRegs, i, regLen);
            GetLabel(preXiQubits, preYiQubits, xiQubits);
        }
    }

    internal operation FindNextNodeInPath(oracle : (Qubit[], Qubit[], Qubit[]) => Unit is Adj + Ctl, xQubits : Qubit[], yQubits : Qubit[], cQubits : Qubit[], zQubits : Qubit[]) : Unit is Adj + Ctl {
        // we know x,y want to find vertex z that the (j,k) of x--y is equal to that of y--z. In other words, we want to find next node z in the "path"
        // we have j and k in cQubits, cQubits = |j>|k>|ccc> or |k>|j>|ccc> doesn't matter.
        // there are 3 possibilities: (in here j and k represent two different regs in cQubits, there order does not matter)
        //      (1) oracle|y>|j>|0> = |y>|j>|x>
        //      (2) oracle|y>|j>|0> = |y>|j>|?>,  ? != x
        //              z exist          => oracle|?>|k>|0> = oracle|z>|k>|0> = |z>|k>|y>
        //              z does not exist => oracle|?>|k>|0> = |z>|k>|*> * != y


        use a0Qubits = Qubit[Length(yQubits)]; // to store the output of oracle|y>|j>, could be |z> or |x> or |0>
        use a1Qubits = Qubit[Length(yQubits)]; // to store |y> or |?> != |y> when we apply oracle the second time

        let lenjOrk = (Length(cQubits) - 3) / 2;
        let jQubits = cQubits[0..lenjOrk -1];
        let kQubits = cQubits[lenjOrk..2 * lenjOrk-1];

        use ifEqual0Qubit = Qubit();
        use ifEqual1Qubit = Qubit();

        within {
            oracle(yQubits, jQubits, a0Qubits);
            oracle(a0Qubits, kQubits, a1Qubits);
            ApplyGetEqualty(xQubits, a0Qubits, ifEqual0Qubit);
            ApplyGetEqualty(yQubits, a1Qubits, ifEqual1Qubit);

        } apply {
            within {
                X(ifEqual0Qubit);
            } apply {
                // assign z value a0 if ? != x and ^ != y
                Controlled ApplyBitwiseCNOT([ifEqual0Qubit, ifEqual1Qubit], (a0Qubits, zQubits));
            }
        }

        // swap j and k
        within {
            oracle(yQubits, kQubits, a0Qubits);
            oracle(a0Qubits, jQubits, a1Qubits);
            ApplyGetEqualty(xQubits, a0Qubits, ifEqual0Qubit);
            ApplyGetEqualty(yQubits, a1Qubits, ifEqual1Qubit);

        } apply {
            within {
                X(ifEqual0Qubit);
            } apply {
                Controlled ApplyBitwiseCNOT([ifEqual0Qubit, ifEqual1Qubit], (a0Qubits, zQubits));
            }
        }

    }

    function GetXiRegsTotalRange(lenXiList : Int[], i : Int) : (Int, Int) {
        mutable startIdx = 0;
        let maxVerticesNum = Length(lenXiList);

        // let
        for r in 0..i-1 {
            set startIdx += lenXiList[r] * (maxVerticesNum - r);
        }

        let range = lenXiList[i] * (maxVerticesNum - i);
        let endIdx = startIdx + range - 1;

        (startIdx, endIdx)
    }


    internal operation DeterministicCoinTossing(oracle : (Qubit[], Qubit[], Qubit[]) => Unit is Adj + Ctl, xQubits : Qubit[], yQubits : Qubit[], cQubits : Qubit[]) : Unit is Adj + Ctl {
        // prepare the color qubits
        // the color qubits is initially |j>|k>|000>
        // we assign the additional 3 digits color
        let lenX0Reg = Length(xQubits);

        Fact(lenX0Reg > 3, "DeterministicCoinTossing: the length of the xqubits must be large than 3, otherwise deterministic coin tossing is not needed.");

        let logStarN = GetLogStarN(lenX0Reg);

        let lenXiList = GetLenXiList(lenX0Reg);
        let numCoinQubits = GetTotalCoinQubitsNum(lenXiList);
        use aQubits = Qubit[numCoinQubits - 2 * Head(lenXiList) - 3];

        // assign the start value
        let totalQubits = xQubits + yQubits + aQubits + cQubits[Length(cQubits) - 3..Length(cQubits)-1];

        // for the first round, find all the near vertices connected in the path
        let numVertices = logStarN + 1;
        for i in 2..numVertices -1 {
            let xIterQubits = SliceArray(totalQubits, i-2, lenX0Reg);
            let yIterQubits = SliceArray(totalQubits, i-1, lenX0Reg);
            let zIterQubits = SliceArray(totalQubits, i, lenX0Reg);
            FindNextNodeInPath(oracle, xIterQubits, yIterQubits, cQubits, zIterQubits);
        }

        for i in 1..logStarN {
            let (preXiRegsStartIdx, preXiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, i - 1);
            let (xiRegsStartIdx, xiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, i);
            CoinTossingStep(lenXiList[i-1], lenXiList[i], totalQubits[preXiRegsStartIdx..preXiRegsEndIdx], totalQubits[xiRegsStartIdx..xiRegsEndIdx]);
        }

    }

    operation GraphColoringOracle(oracle : (Qubit[], Qubit[], Qubit[], Qubit[]) => Unit is Adj + Ctl, xQubits : Qubit[], cQubits : Qubit[], yQubits : Qubit[], rQubits : Qubit[]) : Unit is Adj + Ctl {
        use rTrashQubits = Qubit[Length(rQubits)];
        let unweightedOracle = oracle(_, _, _, rTrashQubits);

        Fact(Length(cQubits) - 3 % 2 == 0, "GraphColoringOracle: Length(cQubits) must be 2k + 3.");
        let lenjOrk = (Length(cQubits) - 3) / 2;
        let jQubits = cQubits[0..lenjOrk]; // again, j may not be "j" in the paper, j is just the first reg.
        let kQubits = cQubits[lenjOrk..2 * lenjOrk-1];
        use aColorQubits = Qubit[3];

        use colorsSameQubit = Qubit();
        within {
            // first dicide whether the colors are the same
            DeterministicCoinTossing(unweightedOracle, xQubits, yQubits, jQubits + kQubits + aColorQubits);
            ApplyGetEqualty(aColorQubits, cQubits[Length(cQubits)-3..Length(cQubits)-1], colorsSameQubit);
        } apply {
            Controlled oracle([colorsSameQubit], (xQubits, cQubits, yQubits, rQubits));
        }
    }

}


