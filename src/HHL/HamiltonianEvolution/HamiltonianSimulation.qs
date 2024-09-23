namespace HHL.HamiltonianSimulation {
    import HHL.HamiltonianSimulation.TrotterSuzuki.ApplyTrotterSuzuki;
    import HHL.HamiltonianSimulation.GraphColoring.GraphColoringOracle;
    import Microsoft.Quantum.Arrays.Tail;
    import HHLUnitTest.TrotterSuzukiUnitTest;
    import Microsoft.Quantum.Diagnostics.DumpRegister;
    import Microsoft.Quantum.Arrays.Zipped;
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    open Microsoft.Quantum.Diagnostics;

    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open HHL.CommonOperation;
    open HHL.HamiltonianSimulation.Oracle;
    open TrotterSuzuki;

    internal operation WGate(qubits : Qubit[]) : Unit is Adj + Ctl {
        // Compiled with qsharp
        // [[1, 0, 0, 0],
        //  [0, 1/sqrt(2),  1/sqrt(2), 0],
        //  [0, 1/sqrt(2), -1/sqrt(2), 0],
        //  [0, 0, 0, 1]]
        // little-endian


        U3(PI(), 0.32175055439664213, 0.32175055439664213, qubits[0]);
        U3(1.4512678518986009, PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 4.0, -PI() / 2.0, PI() / 2.0, qubits[0]);
        U3(0.1688370309450062, -2.359774761217599, -2.3597747612176105, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 4.0, 0.0, -PI() / 2.0, qubits[0]);
        U3(1.4521247316971555, 1.4504171294224673, -3.1272723037036005, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.4982443934561056, 1.0725519333387918, qubits[0]);
        U3(3.0220641786934994, 0.0, PI() / 2.0, qubits[1]);


        // adjust global phase
        Exp([PauliI, PauliI], - 2.9085, qubits);
    }



    /// # Summary
    /// Prepares |Ψ+⟩ = (|01⟩+|10⟩)/√2 state assuming `register` is in |00⟩ state.
    internal operation PreparePsiPlus(register : Qubit[]) : Unit is Adj + Ctl {
        H(register[0]);                 // |+0〉
        X(register[1]);                 // |+1〉
        CNOT(register[0], register[1]); // 1/sqrt(2)(|01〉 + |10〉)
    }

    /// # Summary
    /// Prepares |Ψ−⟩ = (|10〉 - |01〉)/√2 state assuming `register` is in |00⟩ state.
    internal operation PreparePsiMinus(register : Qubit[]) : Unit is Adj + Ctl {
        H(register[1]);                 // |+0〉
        Z(register[1]);                 // |-0〉
        X(register[0]);                 // |-1〉
        CNOT(register[1], register[0]); // 1/sqrt(2)(|10〉 - |01〉)
    }

    internal operation ResetAndPrepareW(i : Int, qubits : Qubit[]) : Unit is Adj + Ctl {
        if i == 1 {
            ApplyXorInPlace(1, qubits);
            PreparePsiPlus(qubits);
        } elif i == 2 {
            ApplyXorInPlace(2, qubits);
            PreparePsiMinus(qubits);
        } elif i == 3 {
            ApplyXorInPlace(3, qubits);
        }
    }

    internal operation ExactWGate(qubits : Qubit[]) : Unit is Adj + Ctl {
        // implement wGate using qram, it has some problems..
        // there are four qubits: the first two qubits are x and y, the last two qubits are temp qubits.
        // the matrix description of this operation is (little-endian):
        // [[1,  0,    0,    0],
        //  [0,  1/<2, 1/<2, 0],
        //  [0, -1/<2, 1/<2, 0],
        // [[1,  0,    0,    1],

        for i in 0..3 {
            ApplyControlledOnInt(i, ResetAndPrepareW(i, _), qubits[0..1], (qubits[2..3]));
        }
        SwapRegs(qubits[0..1], qubits[2..3]);
    }

    internal operation NCNOT(cnQubits : Qubit[], tQubit : Qubit) : Unit is Adj + Ctl {

        within {
            X(cnQubits[0]);
        } apply {
            CCNOT(cnQubits[1], cnQubits[0], tQubit);
        }
    }

    internal operation U1Gate(theta : Double, qubit : Qubit) : Unit is Adj + Ctl {
        Exp([PauliI], theta / 2., [qubit]);
        Rz(theta, qubit);
    }

    operation eZZFtGate(time : Double, pQubit : Qubit, rQubits : Qubit[]) : Unit is Adj + Ctl {

        let length = Length(rQubits);
        Fact((length - 1) % 3 == 0, "eZZFtGate: (Length(rQubits) - 1) % 3 == 0.");
        let nr = (length - 1) / 3;
        let deo = 2^(2 * nr);

        use parityQubit = Qubit();
        within {
            CNOT(pQubit, parityQubit);
            CNOT(Tail(rQubits), parityQubit);
        } apply {
            for i in 0..length-2 {
                let theta = - time * 2.^IntAsDouble(i) / IntAsDouble(deo); // little-endian
                Controlled U1Gate([parityQubit], (theta, rQubits[i]));
            }

            within {
                X(parityQubit); // controll: operate on zero
            } apply {
                for i in 0..length-2 {
                    let theta = time * 2.^IntAsDouble(i) / IntAsDouble(deo); // little-endian
                    Controlled U1Gate([parityQubit], (theta, rQubits[i]));
                }
            }
        }

    }

    operation ApplyOneSparseHamiltonianSimulation(time : Double, h : Double[][], numBits : Int, qx : Qubit[]) : Unit is Adj + Ctl {
        let nx = Length(qx);
        use qy = Qubit[nx];
        use qj = Qubit[nx];
        use qr = Qubit[numBits];
        use qa = Qubit();

        within {
            Oracle(h, qx, qj, qy, qr);
            Zip2Op(WGate, qx, qy);
            Zip2Op(NCNOT(_, qa), qx, qy);
        } apply {
            eZZFtGate(time, qa, qr);
        }
    }

    operation ApplyColorHamiltonianSimulation(
        time : Double,
        h : Double[][],
        numBits : Int,
        j : Int,
        k : Int,
        color : Int,
        qx : Qubit[]
    ) : Unit is Adj + Ctl {
        let nx = Length(qx);
        use qy = Qubit[nx];
        use qc = Qubit[2 * nx + 3];

        use qr = Qubit[numBits];
        use qa = Qubit();

        use qtemp1 = Qubit[nx];
        use qtemp2 = Qubit[nx];

        within {
            // prepare qc
            ApplyXorInPlace(j, qc[0..nx-1]);
            ApplyXorInPlace(k, qc[nx..2 * nx-1]);
            ApplyXorInPlace(color, qc[Length(qc) - 3..Length(qc) -1]);
        } apply {
            within {
                let o = Oracle(h, _, _, _, _);
                let uwO = UnweightedOracle(h, _, _, _, _);

                GraphColoringOracle(o, uwO, qx, qc, qy, qr);
                // Zip4Op(ExactWGate, qx, qy, qtemp1, qtemp2);
                Zip2Op(WGate, qx, qy);
                Zip2Op(NCNOT(_, qa), qx, qy);
            } apply {
                // Z(qa);
                eZZFtGate(time, qa, qr);
            }
        }
    }

    internal function GetColorCoefList(time : Double, h : Double[][], numbits : Int, sparsity : Int) : Coef[] {

        mutable colorNum = 6;
        mutable coefList = [];

        for j in 0..sparsity-1 {
            for k in 0..sparsity-1 {
                for color in 0..colorNum - 1 {
                    let colorHS = ApplyColorHamiltonianSimulation(_, h, numbits, j, k, color, _);
                    let coef = Coef(colorHS, time);
                    set coefList = coefList + [coef];
                }
            }
        }

        return coefList;
    }


    operation ApplySparseHamiltonianSimulation(time : Double, sparsity : Int, h : Double[][], numBits : Int, qx : Qubit[]) : Unit is Adj + Ctl {
        let coefs = GetColorCoefList(time, h, numBits, sparsity);
        ApplyTrotterSuzuki(2, 5, coefs, qx); // here trotter step is only 3

    }
}

