namespace HHL.HamiltonianSimulation {
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
        //    [[1, 0, 0, 0],
        //     [0, 1/sqrt(2),  1/sqrt(2), 0],
        //     [0, 1/sqrt(2), -1/sqrt(2), 0],
        //     [0, 0, 0, 1]]
        //     little-endian

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

    internal operation CNNOT(cnQubits : Qubit[], tQubit : Qubit) : Unit is Adj + Ctl {
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

    operation ApplyHamiltonianSimulation(time : Double, h : Double[][], numBits : Int, qx : Qubit[]) : Unit is Adj + Ctl {
        let nx = Length(qx);
        use qy = Qubit[nx];
        use qj = Qubit[nx];
        use qr = Qubit[numBits];
        use qa = Qubit();

        within {
            Oracle(h, qx, qj, qy, qr);
            ZipOp(WGate, qx, qy);
            ZipOp(CNNOT(_, qa), qx, qy);
        } apply {
            eZZFtGate(time, qa, qr);
        }
    }
}