namespace HHL.HamiltonianSimulation.GraphColoring {
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
        // note that there might not be so many coin qubits in "path"
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
    //     /// # Summary
    // /// Computes `if (c == x) { action(target) }`, that is, applies `action` to `target`
    // /// if a BigInt value `c` is equal to the little-endian qubit register `x`
    // operation ApplyIfEqualL<'T>(
    //     action : 'T => Unit is Adj + Ctl,
    //     c : BigInt,
    //     xs : Qubit[],
    //     target : 'T
    // ) : Unit is Adj + Ctl {

    //     let cBitSize = BitSizeL(c);
    //     let xLen = Length(xs);
    //     if (cBitSize <= xLen) {
    //         let bits = BigIntAsBoolArray(c, Length(xs));
    //         within {
    //             ApplyPauliFromBitString(PauliX, false, bits, xs);
    //         } apply {
    //             Controlled ApplyAsSinglyControlled(xs, (a => action(a), target));
    //         }
    //     }
    // }

    // internal operation ApplyIfAssociatedByJK<'T>(
    //     action : 'T => Unit is Adj + Ctl,
    //     oracle : (Qubit[], Qubit[], Qubit[], Qubit) => Unit is Adj + Ctl,
    //     xQubits : Qubit[],
    //     yQubits : Qubit[],
    //     jQubits : Qubit[],
    //     kQubits : Qubit[],
    //     target : 'T
    // ) : Unit is Adj + Ctl {
    //     // it is guaranteed that x < y,
    //     // if y is x's jth neighbour and x is y's kth neighbour, then apply the specified action

    //     use ayQubits = Qubit[Length(xQubits)];
    //     use axQubits = Qubit[Length(yQubits)];
    //     use arQubits = Qubit[2];
    //     oracle(yQubits, jQubits, ayQubits, arQubits[0]);

    //     // Controlled oracle()

    //     within {

    //         oracle(ayQubits, kQubits, axQubits, arQubits[1]);
    //     } apply {}
    // }

    internal operation FindNextNodeInPath(oracle : (Qubit[], Qubit[], Qubit[], Qubit) => Unit is Adj + Ctl, xQubits : Qubit[], cQubits : Qubit[], yQubits : Qubit[]) : Unit is Adj + Ctl {
        // We know x,y (x < y is guaranteed), want to find vertex z that the (j,k) of x--y is equal to that of y--z.
        // In other words, we want to find next node z in the "path"
        // we have j and k in cQubits, cQubits = |j>|k>|ccc>.
        // If z exist, then oracle|y>|k>|0>|0> = |y>|k>|z>|1> && oracle|z>|j>|0>|0> = |z>|j>|y>|1>

        use ayQubits = Qubit[Length(xQubits)];
        use axQubits = Qubit[Length(xQubits)];
        use arQubits = Qubit[2];

        let lenjOrk = (Length(cQubits) - 3) / 2;
        let jQubits = cQubits[0..lenjOrk -1];
        let kQubits = cQubits[lenjOrk..2 * lenjOrk-1];

        within {
            oracle(xQubits, jQubits, ayQubits, arQubits[0]);
            oracle(ayQubits, kQubits, axQubits, arQubits[1]);
        } apply {
            Controlled ApplyIfEqualLE(arQubits, (ApplyBitwiseCNOT(_, _), axQubits, xQubits, (ayQubits, yQubits)));
        }



        // use ifEqual0Qubit = Qubit();
        // use ifEqual1Qubit = Qubit();

        // within {
        //     oracle(yQubits, jQubits, a0Qubits);
        //     oracle(a0Qubits, kQubits, a1Qubits);
        //     ApplyGetEqualty(xQubits, a0Qubits, ifEqual0Qubit);
        //     ApplyGetEqualty(yQubits, a1Qubits, ifEqual1Qubit);

        // } apply {
        //     within {
        //         X(ifEqual0Qubit);
        //     } apply {
        //         // assign z value a0 if ? != x and ^ != y
        //         Controlled ApplyBitwiseCNOT([ifEqual0Qubit, ifEqual1Qubit], (a0Qubits, zQubits));
        //     }
        // }

        // // swap j and k
        // within {
        //     oracle(yQubits, kQubits, a0Qubits);
        //     oracle(a0Qubits, jQubits, a1Qubits);
        //     ApplyGetEqualty(xQubits, a0Qubits, ifEqual0Qubit);
        //     ApplyGetEqualty(yQubits, a1Qubits, ifEqual1Qubit);

        // } apply {
        //     within {
        //         X(ifEqual0Qubit);
        //     } apply {
        //         Controlled ApplyBitwiseCNOT([ifEqual0Qubit, ifEqual1Qubit], (a0Qubits, zQubits));
        //     }
        // }

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


    internal operation DeterministicCoinTossing(unweightedOracle : (Qubit[], Qubit[], Qubit[], Qubit) => Unit is Adj + Ctl, xQubits : Qubit[], yQubits : Qubit[], cQubits : Qubit[]) : Unit is Adj + Ctl {
        // prepare the color qubits
        // it is not guaranteed that x < y so we have to figure it out first
        // the color qubits is initially |j>|k>|000>
        // we assign the additional 3 digits color
        let lenX0Reg = Length(xQubits);

        Fact(lenX0Reg > 3, "DeterministicCoinTossing: the length of the xqubits must be large than 3, otherwise deterministic coin tossing is not needed.");

        let logStarN = GetLogStarN(lenX0Reg);

        let lenXiList = GetLenXiList(lenX0Reg);
        let numCoinQubits = GetTotalCoinQubitsNum(lenXiList);
        use aQubits = Qubit[numCoinQubits - 3]; // the last three are clock qubits

        within {
            ApplyBitwiseCNOT(xQubits, aQubits[0..lenX0Reg-1]);
            ApplyBitwiseCNOT(yQubits, aQubits[lenX0Reg..2 * lenX0Reg-1]);

            // make sure the small one is in the front.
            ApplyIfGreaterLE(SwapRegs(_, _), xQubits, yQubits, (aQubits[0..lenX0Reg-1], aQubits[lenX0Reg..2 * lenX0Reg-1]));
        } apply {
            // assign the start value
            let totalQubits = aQubits + cQubits[Length(cQubits) - 3..Length(cQubits)-1];


            // for the first round, find all the near vertices connected in the path
            let numVertices = logStarN + 1;
            for i in 2..numVertices -1 {
                let xIterQubits = SliceArray(totalQubits, i-1, lenX0Reg);
                let yIterQubits = SliceArray(totalQubits, i, lenX0Reg);
                FindNextNodeInPath(unweightedOracle, yIterQubits, cQubits, yIterQubits);
            }

            for i in 1..logStarN {
                let (preXiRegsStartIdx, preXiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, i - 1);
                let (xiRegsStartIdx, xiRegsEndIdx) = GetXiRegsTotalRange(lenXiList, i);
                CoinTossingStep(lenXiList[i-1], lenXiList[i], totalQubits[preXiRegsStartIdx..preXiRegsEndIdx], totalQubits[xiRegsStartIdx..xiRegsEndIdx]);
            }
        }

    }

    operation GraphColoringOracle(oracle : (Qubit[], Qubit[], Qubit[], Qubit[]) => Unit is Adj + Ctl, unweightedOracle : (Qubit[], Qubit[], Qubit[], Qubit) => Unit is Adj + Ctl, xQubits : Qubit[], cQubits : Qubit[], yQubits : Qubit[], rQubits : Qubit[]) : Unit is Adj + Ctl {
        // Input: vertex x, colour c = (j, k, f, g).
        // Output : m(x), w(x), where m(x) is the vertex y that shares an edge of colour c
        // with x, the weight w(x) of that edge, or m(x) = x and w(x) = O if the edge does
        // not exist.

        Fact((Length(cQubits) - 3) % 2 == 0, "GraphColoringOracle: Length(cQubits) must be 2k + 3.");
        let lenjOrk = (Length(cQubits) - 3) / 2;
        let jQubits = cQubits[0..lenjOrk]; // again, j may not be "j" in the paper, j is just the first reg.
        let kQubits = cQubits[lenjOrk..2 * lenjOrk-1];

        use ayQubits = Qubit[Length(yQubits)];
        use arQubit = Qubit();

        let cQubitsSwapJK = cQubits[lenjOrk..2 * lenjOrk-1] + cQubits[0..lenjOrk-1] + cQubits[Length(cQubits)-3..Length(cQubits)-1];
        for qc in [cQubits, cQubitsSwapJK] {
            within {
                // 1.Check if vertex x has a jth neighbour, and if that jth neighbour's kth neighbour
                // is x. If so, call the neighbour y, otherwise return m(x) = x and w(x) = 0
                FindNextNodeInPath(unweightedOracle, xQubits, qc, ayQubits);
            } apply {
                // 2. Finish colouring the edge (x, y) using the deterministic coin tossing method,
                // or append to the colour "000" if x = y. If the computed colour does not match
                // the input colour f, return m(x) = x and w(x) = 0
                within {
                    // if the colors are the same, the last 3 color qubits of qc will be set to |000>
                    DeterministicCoinTossing(unweightedOracle, xQubits, ayQubits, qc);
                } apply {
                    ApplyControlledOnInt(0, oracle(_, _, _, _), qc[Length(qc) - 3..Length(qc) - 1], (xQubits, qc[0..lenjOrk-1], yQubits, rQubits));
                }

            }
        }

        // use ayQubits = Qubit[Length(yQubits)];
        // use axQubits = Qubit[Length(xQubits)];
        // use arQubit = Qubit();
        // use ifEqual0Qubit = Qubit();
        // use ifEqual1Qubit = Qubit();

        // use aColorQubits = Qubit[3];
        // use colorsSameQubit = Qubit();

        // // 1.Check if vertex x has a jth neighbour, and if that jth neighbour's kth neighbour
        // // is x. If so, call the neighbour y, otherwise return m(x) = x and w(x) = 0
        // within {
        //     unweightedOracle(xQubits, jQubits, ayQubits, arQubit);
        //     unweightedOracle(ayQubits, kQubits, axQubits, arQubit);
        //     ApplyGetEqualty(yQubits, ayQubits, ifEqual0Qubit);
        //     ApplyGetEqualty(xQubits, axQubits, ifEqual1Qubit);

        // } apply {
        //     // 2. Finish colouring the edge (x, y)a using the deterministic coin tossing method,
        //     // or append to the colour "000" if x = y. If the computed colour does not match
        //     // the input colour f, return m(x) = x and w(x) = 0

        //     within {
        //         // Controlled DeterministicCoinTossing([ifEqual0Qubit, ifEqual1Qubit, arQubit], (unweightedOracle, xQubits, yQubits, jQubits + kQubits + aColorQubits));
        //         Controlled ApplyGetEqualty([ifEqual0Qubit, ifEqual1Qubit], (aColorQubits, cQubits[Length(cQubits)-3..Length(cQubits)-1], colorsSameQubit));
        //     } apply {
        //         ApplyBitwiseCNOT(xQubits, yQubits);
        //         Controlled ApplyBitwiseCNOT([colorsSameQubit], (xQubits, yQubits)); // cancel the effect
        //         Controlled oracle([colorsSameQubit], (xQubits, cQubits, yQubits, rQubits)); // we do not need to double controll
        //     }
        // }
        // DumpMachine();
    }

}


