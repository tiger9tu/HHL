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

    operation WGate(qubits : Qubit[]) : Unit is Adj + Ctl {
        within {
            CNOT(qubits[0], qubits[1]);
            CNOT(qubits[1], qubits[0]);
        } apply {
            Controlled H([qubits[1]], (qubits[0]));
        }
    }

    operation NCNOT(cnQubits : Qubit[], tQubit : Qubit) : Unit is Adj + Ctl {

        within {
            X(cnQubits[0]);
        } apply {
            CCNOT(cnQubits[1], cnQubits[0], tQubit);
        }
    }

    operation U1Gate(theta : Double, qubit : Qubit) : Unit is Adj + Ctl {
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
        body (...) {
            Controlled ApplyOneSparseHamiltonianSimulation([], (time, h, numBits, qx));
        }

        controlled (ctrls, ...) {

            if Length(ctrls) >= 2 {
                use control = Qubit();
                within {
                    Controlled X(ctrls, control);
                } apply {
                    Controlled ApplyOneSparseHamiltonianSimulation([control], (time, h, numBits, qx));
                }
            } else {
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
                    Controlled eZZFtGate(ctrls, (time, qa, qr));
                }
            }
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
        body (...) {
            Controlled ApplyColorHamiltonianSimulation([], (time, h, numBits, j, k, color, qx));
        }

        controlled (ctrls, ...) {
            if Length(ctrls) >= 2 {
                use control = Qubit();
                within {
                    Controlled X(ctrls, control);
                } apply {
                    Controlled ApplyColorHamiltonianSimulation([control], (time, h, numBits, j, k, color, qx));
                }
            } else {

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
                        GraphColoringOracle(h, qx, qc, qy, qr);
                        // Zip4Op(ExactWGate, qx, qy, qtemp1, qtemp2);
                        Zip2Op(WGate, qx, qy);
                        Zip2Op(NCNOT(_, qa), qx, qy);
                    } apply {
                        // Z(qa);
                        Controlled eZZFtGate(ctrls, (time, qa, qr));
                    }
                }
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
        ApplyTrotterSuzuki(1, 2, coefs, qx); // here trotter step is only 3

    }
}



