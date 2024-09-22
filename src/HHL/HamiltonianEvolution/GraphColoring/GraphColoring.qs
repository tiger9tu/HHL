namespace HHL.HamiltonianSimulation.GraphColoring {
    import Microsoft.Quantum.Math.MaxI;
    open Microsoft.Quantum.Unstable.Arithmetic;
    import HHL.HamiltonianSimulation.Oracle.Oracle;
    import HHL.CommonOperation.ApplyBitwiseXOR;
    import HHL.CommonOperation.SliceArray;
    import HHL.CommonOperation.ApplyBitwiseCNOT;
    import HHL.CommonOperation.SwapRegs;
    import Microsoft.Quantum.Unstable.Arithmetic.ApplyIfEqualL;
    import Microsoft.Quantum.Arrays.Head;
    import HHL.CommonOperation.SumIntArray;
    import Microsoft.Quantum.Arrays.Fold;
    import Microsoft.Quantum.Math.Lg;
    import Microsoft.Quantum.Math.Ceiling;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Diagnostics;


    internal function GetFirst1AtNBitString(n : Int) : Bool[] {
        mutable bitString = Repeated(false, n + 1);
        set bitString w/= n <- true;
        bitString
    }

    operation GetLabel(
        preXiQubits : Qubit[],
        preYiQubits : Qubit[],
        xiQubits : Qubit[]
    ) : Unit is Adj + Ctl {
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
        mutable logStarN = 1; // apply an additional round when nclock == 3
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
            set lenXiList w/= i <- MaxI(Ceiling(Lg(IntAsDouble(lenXiList[i - 1]))), 3);
        }

        set lenXiList w/= logStarN <- 3;
        lenXiList
    }

    internal function GetTotalCoinQubitsNum(lenXiList : Int[]) : Int {
        // note that there might not be so many coin qubits in "path"
        mutable num = 0;
        let length = Length(lenXiList);
        for i in 0..length - 1 {
            let numVertices = length - i;
            set num += lenXiList[i] * numVertices;
        }
        num
    }


    internal operation CoinTossingStep(
        preRegLen : Int,
        regLen : Int,
        preVerticesRegs : Qubit[],
        verticesRegs : Qubit[]
    ) : Unit is Adj + Ctl {
        let numVertices = Length(verticesRegs) / regLen;
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


    internal operation FindNextVertexInPath(
        oracle : (Qubit[], Qubit[], Qubit[], Qubit) => Unit is Adj + Ctl,
        frontierVertexQubits : Qubit[],
        jQubits : Qubit[],
        kQubits : Qubit[],
        nextVertexQubits : Qubit[]
    ) : Unit is Adj + Ctl {
        // we want to find vertex in the path that's next to the current frontier,
        // the path is grown from small idx vertex to larger idx index : x0 < x1 < x2 < ...
        // so next vertex must be larger than frontier
        // that suggest that next vertex could only be frontier's jth neibour

        let length = Length(frontierVertexQubits);
        use aFrontierVertexQubits = Qubit[length];
        use aNextVertexQubits = Qubit[length];
        use arQubits = Qubit[2];


        within {
            oracle(frontierVertexQubits, jQubits, aNextVertexQubits, arQubits[0]);
            oracle(aNextVertexQubits, kQubits, aFrontierVertexQubits, arQubits[1]);
        } apply {
            Controlled ApplyIfEqualLE(
                arQubits,
                (
                    ApplyBitwiseCNOT,
                    aFrontierVertexQubits,
                    frontierVertexQubits,
                    (aNextVertexQubits, nextVertexQubits)
                )
            );
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

    internal function GetSupplyQubitsNum(lenX0 : Int) : Int {
        mutable n = 0;
        if lenX0 < 3 {
            set n = 3 - lenX0;
        }
        n
    }

    internal operation DeterministicCoinTossing(
        unweightedOracle : (Qubit[], Qubit[], Qubit[], Qubit) => Unit is Adj + Ctl,
        smallVertexQubits : Qubit[],
        largeVertexQubits : Qubit[],
        jQubits : Qubit[],
        kQubits : Qubit[],
        colorQubits : Qubit[]
    ) : Unit is Adj + Ctl {
        // prepare the color qubits
        // it is guaranteed that x < y
        // the color qubits is initially |j>|k>|000>
        // we assign the additional 3 digits color
        let lenX0Reg = Length(smallVertexQubits);
        let supX0Num = GetSupplyQubitsNum(lenX0Reg);
        use axQubits = Qubit[supX0Num];
        use ayQubits = Qubit[supX0Num];

        let lenSupX0Reg = lenX0Reg + supX0Num;


        let logStarN = GetLogStarN(lenSupX0Reg);
        let lenXiList = GetLenXiList(lenSupX0Reg);
        let numCoinQubits = GetTotalCoinQubitsNum(lenXiList);
        use aQubits = Qubit[numCoinQubits - 2 * lenSupX0Reg - 3]; // the last three are clock qubits

        let totalQubits = smallVertexQubits + axQubits + largeVertexQubits + ayQubits + aQubits + colorQubits;

        // for the first round, find all the near vertices connected in the path
        let numVertices = logStarN + 1;
        within {
            for i in 2..numVertices -1 {
                let prevQubits = SliceArray(totalQubits, i-1, lenSupX0Reg);
                let nextQubits = SliceArray(totalQubits, i, lenSupX0Reg);
                FindNextVertexInPath(unweightedOracle, prevQubits[0..lenX0Reg-1], jQubits, kQubits, nextQubits[0..lenX0Reg-1]);
            }

            for i in 1..logStarN - 1 {
                let (preXiRegsStartIdx, preXiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, i - 1);
                let (xiRegsStartIdx, xiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, i);
                CoinTossingStep(
                    lenXiList[i-1],
                    lenXiList[i],
                    totalQubits[preXiRegsStartIdx..preXiRegsEndIdx],
                    totalQubits[xiRegsStartIdx..xiRegsEndIdx]
                );
            }
        } apply {
            // the last
            let (preXiRegsStartIdx, preXiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, logStarN - 1);
            let (xiRegsStartIdx, xiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, logStarN);
            CoinTossingStep(
                lenXiList[logStarN-1],
                lenXiList[logStarN],
                totalQubits[preXiRegsStartIdx..preXiRegsEndIdx],
                totalQubits[xiRegsStartIdx..xiRegsEndIdx]
            );
        }

    }

    operation GraphColoringOracle(oracle : (Qubit[], Qubit[], Qubit[], Qubit[]) => Unit is Adj + Ctl, unweightedOracle : (Qubit[], Qubit[], Qubit[], Qubit) => Unit is Adj + Ctl, xQubits : Qubit[], cQubits : Qubit[], yQubits : Qubit[], rQubits : Qubit[]) : Unit is Adj + Ctl {
        // Input: vertex x, colour c = (om1, om2, f, g).
        // Output : m(x), w(x), where m(x) is the vertex y that shares an edge of colour c
        // with x, the weight w(x) of that edge, or m(x) = x and w(x) = O if the edge does
        // not exist.

        Fact((Length(cQubits) - 3) % 2 == 0, "GraphColoringOracle: Length(cQubits) must be 2k + 3.");
        let lenOrdMark = (Length(cQubits) - 3) / 2;
        let lenX = Length(xQubits);
        use ayQubits = Qubit[lenX];
        use axQubits = Qubit[lenX];
        use condQubits = Qubit[2];
        use arQubits = Qubit[2];

        let firstOrdMarkQubits = cQubits[0..lenOrdMark-1];
        let SecOrdMarkQubits = cQubits[lenOrdMark..2 * lenOrdMark-1];
        let colorQubits = cQubits[Length(cQubits) - 3..Length(cQubits) - 1];


        // we define that y is x's jth neighbour and x is y's kth neighbour
        // (firstOrdMark, SecOrdMark) = (j, k) if x <= y
        // (firstOrdMark, SecOrdMark) = (k, j) if x > y
        //
        // so there are two possibilities :
        // 1. x <= y: x --(j,k)-- y first order mark is j
        // 2. x >  y: x --(k,j)-- y first order mark is k

        // try first possibility:
        let p0JQubits = firstOrdMarkQubits;
        let p0KQubits = SecOrdMarkQubits;

        within {
            unweightedOracle(xQubits, p0JQubits, ayQubits, arQubits[0]);
            unweightedOracle(ayQubits, p0KQubits, axQubits, arQubits[1]);
            ApplyIfEqualLE(X, axQubits, xQubits, (condQubits[0]));
            ApplyIfLessOrEqualLE(X, xQubits, ayQubits, condQubits[1]);
            Controlled DeterministicCoinTossing(arQubits + condQubits, (unweightedOracle, xQubits, ayQubits, p0JQubits, p0KQubits, colorQubits));
        } apply {
            within {
                // I used a trick here to reduce need for aColorQubits
                ApplyToEachCA(X, colorQubits);
            } apply {
                Controlled oracle(arQubits + condQubits + colorQubits, (xQubits, p0JQubits, yQubits, rQubits));
            }
        }


        // try second possibility:
        let p1JQubits = SecOrdMarkQubits;
        let p1KQubits = firstOrdMarkQubits;

        within {
            unweightedOracle(xQubits, p1JQubits, ayQubits, arQubits[0]);
            unweightedOracle(ayQubits, p1KQubits, axQubits, arQubits[1]);
            ApplyIfEqualLE(X, axQubits, xQubits, (condQubits[0]));
            ApplyIfGreaterLE(X, xQubits, ayQubits, condQubits[1]);
            Controlled DeterministicCoinTossing(arQubits + condQubits, (unweightedOracle, ayQubits, xQubits, p1JQubits, p1KQubits, colorQubits));
        } apply {
            within {
                // I used a trick here to reduce need for aColorQubits
                ApplyToEachCA(X, colorQubits);
            } apply {
                Controlled oracle(arQubits + condQubits + colorQubits, (xQubits, p1JQubits, yQubits, rQubits));
            }
        }



    }

}


