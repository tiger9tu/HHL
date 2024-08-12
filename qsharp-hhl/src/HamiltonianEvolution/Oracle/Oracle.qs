namespace HamiltonianSimulation.Oracle {
    import Microsoft.Quantum.Diagnostics.DumpMachine;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open CommonOperation;

    internal operation _Circuit30418_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(PI() / 2.0, -PI() / 2.0, 3.0 * PI() / 4.0, qubits[0]);
        U3(0.835788143228214, PI() / 2.0, PI() / 4.0, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6894679218926363, 0.014320349886192574, -1.4504171294224655, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, -0.37483032543138384, 0.0, qubits[0]);
        U3(1.6903248016911907, -2.0133297347392016, -PI() / 2.0, qubits[1]);
    }

    internal operation _Circuit30421_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(2.526112944919406, -PI() / 2.0, 2.992824203422879, qubits[0]);
        U3(0.11952847489629548, -PI() / 2.0, 0.273686123289957, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6894679218926363, 0.014320349886192574, -1.4504171294224655, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, 0.9542454480517968, 0.0, qubits[0]);
        U3(1.6903248016911905, -PI() / 4.0, -PI() / 2.0, qubits[1]);
    }

    internal operation _Circuit30424_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(PI() / 2.0, PI() / 2.0, -PI() / 2.0, qubits[0]);
        U3(1.4512678518986009, PI() / 2.0, 0.0, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6894679218926363, 0.014320349886192574, -1.4504171294224655, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, 1.12523507285157, -PI(), qubits[0]);
        U3(1.4512678518986024, -7.0 * PI() / 8.0, PI() / 2.0, qubits[1]);
    }



    internal operation _Circuit30427_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(PI(), -0.5445311813683054, -1.6697662542198755, qubits[0]);
        U3(3.022064178693497, PI() / 2.0, -0.7064610239295459, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6894679218926363, 0.014320349886192574, -1.4504171294224655, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, 0.3137619422308213, -PI(), qubits[0]);
        U3(0.6658696885011542, -PI(), PI() / 2.0, qubits[1]);
    }

    internal operation _Circuit30430_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(0.527631020707379, -1.2177803120823185, -0.30819801626335597, qubits[0]);
        U3(1.4512678518986009, PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.640956065145825, 0.43050850861257794, -1.4614362657485387, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.6139616328824142, -0.6190972017382568, -0.7976418178417539, qubits[0]);
        U3(0.11952847489629444, -2.3316445913544674, -PI() / 2.0, qubits[1]);
    }

    internal operation _Circuit30433_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(0.47809804858816274, -1.6782676380893629, 0.09549842613996073, qubits[0]);
        U3(1.4512678518986009, PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.6845581055852314, 0.05520879958969038, -1.4505890453925367, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.6634946050016306, 0.8317967918616538, -1.6370653566499804, qubits[0]);
        U3(0.1195284748962942, 1.9389455096557437, -PI() / 2.0, qubits[1]);
    }

    internal operation _Circuit30436_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(2.1994952331170974, -2.6985095346381396, -2.9431132695168003, qubits[0]);
        U3(1.9165076641862282, -2.1764016102114905, -1.0260943729620413, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.352887223268017, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6533013075712104, 0.3203374029794279, -1.4565566503166627, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(0.5681868585827928, 1.062680539163698, -0.68055889749962, qubits[0]);
        U3(1.4056557161543703, -1.8590118449245634, -1.933643636963772, qubits[1]);
    }
    internal operation _Circuit30439_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(0.26817892460288323, 1.1462202531503003, 2.836122144378731, qubits[0]);
        U3(0.7269441267600535, -2.1133727909215314, -1.7247727540798885, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.21760235042611, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6892568069128675, 0.016077983151707276, -1.4504203611302273, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.4718732754230444, 0.22254356309922407, 1.0198551600811463, qubits[0]);
        U3(0.5413355138909366, 0.6030260357584489, -1.1198727321714212, qubits[1]);
    }


    internal operation _Circuit30442_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(0.9544652195200443, -2.96599883863768, 1.272991330942273, qubits[0]);
        U3(1.451267851898601, PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.5846235606920067, 1.086404245007686, -1.5148396492370546, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.1871274340697497, 2.8437876577371695, -1.8833290839066157, qubits[0]);
        U3(0.11952847489629402, 3.0 * PI() / 4.0, -PI() / 2.0, qubits[1]);
    }

    internal operation _Circuit30445_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(0.43369831392967706, -2.074417773601388, 0.4636476090008079, qubits[0]);
        U3(1.4512678518986009, PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.6403288771932745, 0.4362423339705823, -1.4617271829378797, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.707894339660116, 0.46364760900080704, -1.6484838004039624, qubits[0]);
        U3(0.11952847489629351, -PI() / 2.0, -PI() / 2.0, qubits[1]);
    }

    internal operation _Circuit30448_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(1.5715591187588163, 0.010721197365317625, 0.0198112869397562, qubits[0]);
        U3(2.2408387867619766, 1.5960639957028118, 3.137646571925651, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.3508810096265744, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.62063470177712, 0.6260256367033561, -1.4733166754403806, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(1.5713061818087046, 2.3127929346783063, -2.50974580277515, qubits[0]);
        U3(2.0284018835906914, 3.0136005010452607, -2.404906984583051, qubits[1]);
    }

    internal operation _Circuit30451_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(1.451615410258359, -1.9923500428125143, -0.014874581890717664, qubits[0]);
        U3(2.396393666320431, -2.796560727200113, 0.3184644448687086, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(0.6713547616316583, -PI() / 2.0, PI() / 2.0, qubits[0]);
        U3(0.7374248275460028, -1.7490845376818065, -3.0089896868199792, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(0.21418054696190977, -PI(), PI() / 2.0, qubits[0]);
        U3(1.4521247316971555, 1.4504171294224673, -3.1272723037036005, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(1.7302704921728387, 0.0941064219592449, -0.2722052464753517, qubits[0]);
        U3(2.3805677642734957, 0.3081835316779564, 0.06876773847279916, qubits[1]);
    }

    operation OracleExample11(qubits : Qubit[]) : Unit is Adj + Ctl {
        // 0 0 0 1
        // 0 1 0 0
        // 0 0 1 0
        // 1 0 0 0
        SwapReverseRegister(qubits);

        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[3]);
        CNOT(qubits[1], qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit30418_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(0.0, 0.0, PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 6.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, PI() / 2.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit30421_([qubits[0], qubits[1]]);
        CNOT(qubits[0], qubits[3]);
        CNOT(qubits[1], qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[3]);
        CNOT(qubits[2], qubits[3]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[3]);
        CNOT(qubits[0], qubits[3]);
        CNOT(qubits[1], qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[3]);
        CNOT(qubits[2], qubits[3]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[1], qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit30424_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 2.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit30427_([qubits[0], qubits[1]]);
        CNOT(qubits[0], qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[1], qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[2], qubits[3]);
        U3(0.0, 0.0, -3.0 * PI() / 8.0, qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[1], qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[0], qubits[3]);
        _Circuit30430_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 2.0, qubits[3]);
        U3(0.0, 0.0, PI() / 6.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, PI() / 6.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, PI() / 8.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit30433_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit30436_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(0.0, 0.0, -0.39431141316608725, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -0.5058114562853502, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, -0.21465677384023263, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, 1.8342672190947833, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit30439_([qubits[0], qubits[1]]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, PI() / 8.0, qubits[3]);
        CNOT(qubits[1], qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, -PI() / 8.0, qubits[3]);
        CNOT(qubits[2], qubits[3]);
        U3(0.0, 0.0, -3.0 * PI() / 8.0, qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[3]);
        CNOT(qubits[1], qubits[3]);
        U3(0.0, 0.0, -PI() / 8.0, qubits[3]);
        CNOT(qubits[0], qubits[3]);
        _Circuit30442_([qubits[0], qubits[1]]);
        U3(0.0, 0.0, PI() / 4.0, qubits[3]);
        CNOT(qubits[2], qubits[3]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 4.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit30445_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit30448_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(0.0, 0.0, 0.0016123314673632816, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -0.7980216998542546, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, -0.3639451353043853, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -1.5640033053654023, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit30451_([qubits[0], qubits[1]]);
        Exp([PauliI, PauliI, PauliI, PauliI], 2.6883, qubits);

        SwapReverseRegister(qubits);
    }

    operation OracleExample11UnitTest() : Unit {
        // use xQubit = Qubit[2];
        // use yQubit = Qubit[2];
        // OracleExample(xQubit + yQubit);
        // // Expect |0011⟩ |  1.0000+0.0000𝑖 |   100.0000% |   0.0000
        // DumpMachine();
        // ResetAll(xQubit + yQubit);

        use xQubit = Qubit[2];
        use yQubit = Qubit[2];
        X(xQubit[1]);
        OracleExample11(xQubit + yQubit);
        // Expect |0011⟩ |  1.0000+0.0000𝑖 |   100.0000% |   0.0000
        DumpMachine();
        ResetAll(xQubit + yQubit);
    }

}
