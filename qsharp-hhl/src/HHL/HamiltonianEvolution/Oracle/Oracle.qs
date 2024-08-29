namespace HHL.HamiltonianSimulation.Oracle {
    // Precompiled by qiskit qs_decomposition

    import Microsoft.Quantum.Diagnostics.DumpMachine;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Convert;
    open HHL.CommonOperation;

    // operation QRAMOracle(UnitaryMatrix : Int[][], qubits: Qubit[]) : Unit is Adj + Ctl {

    // }

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

    operation OracleExample0(qubits : Qubit[]) : Unit is Adj + Ctl {
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




    /////////////////////////////////Oracle 2///////////////////////////////////////
    // 0 1 0 0
    // 1 0 0 0
    // 0 0 1 0
    // 0 0 0 1
    internal operation _Circuit31080_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(0.8005038404950419, 1.398714349375565, -2.896999746190743, qubits[0]);
        U3(1.4681193178462442, -0.8197390205625688, 1.9457669637968023, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.5054535565375105, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.683607964980131, 0.06312746641633638, -1.4506456922428814, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(1.3262163771205668, -0.6968582178009308, 3.0550530215045937, qubits[0]);
        U3(1.0635845157252681, -2.188844994057388, -1.381526578722998, qubits[1]);

    }

    internal operation _Circuit31083_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(0.33893274669405543, -2.087205280306609, 1.2230731160503021, qubits[0]);
        U3(0.8308051844331109, 1.3902332927141803, 2.1692173304006026, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.199357592067573, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6878690263938112, 0.02763233415483457, -1.450450907701212, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(1.380320966031717, 1.376768367242052, 2.374787167584861, qubits[0]);
        U3(2.4834486219360103, 1.5059850383112758, -1.406596131515975, qubits[1]);

    }


    internal operation _Circuit31086_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(PI(), 0.02641722145558223, -0.0734673634260159, qubits[0]);
        U3(1.6903248016911914, -PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(3.0 * PI() / 4.0, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6142519603595233, 0.6930561098952683, -1.4782710291457004, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, -3.1122876811261087, 0.0, qubits[0]);
        U3(1.6903248016911903, -1.6069680175680432, -PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31089_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(PI(), 0.05702113096365968, -1.5430801682949262, qubits[0]);
        U3(1.4512678518986006, PI() / 2.0, -3.105420962816651, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(3.0 * PI() / 4.0, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.605479860256207, 0.7919145236340501, -1.4863268892068007, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI() / 2.0, PI() / 4.0, -PI(), qubits[0]);
        U3(1.4512678518986029, -PI() / 2.0, PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31092_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(0.906006121531952, -1.1161834126326995, 1.4243749409306083, qubits[0]);
        U3(2.250420319653723, 1.110370726292027, -1.23399645587542, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.387237874121771, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6622388189404753, 0.24307273483069292, -1.4539603193654775, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(0.9060061215319511, 0.911305969226988, 2.6869797394275965, qubits[0]);
        U3(0.7998549482430559, -0.6462668610930384, 1.068040907034618, qubits[1]);

    }


    internal operation _Circuit31095_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(0.9060061215319515, 1.1161834126327026, 1.4759319048947805, qubits[0]);
        U3(2.4584970518646214, -2.150213775473686, 1.2968886788074219, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.387237874121771, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6622388189404753, 0.24307273483069292, -1.4539603193654775, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.2355865320578383, 1.7172177126591812, -2.6869797394276, qubits[0]);
        U3(2.1272452524224903, 1.3937143768588252, 1.9899702190269446, qubits[1]);

    }


    internal operation _Circuit31098_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(1.460612469449348, -2.839889168879239, -1.1228326568433804, qubits[0]);
        U3(2.3736957504049343, -2.0594107435964535, -2.2757093958689154, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.2900582989656737, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6643063570003802, 0.22541990646466425, -1.4534648319729992, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.0843321113014732, -0.17968016534934295, -0.6235319657629361, qubits[0]);
        U3(1.0321588681149374, 0.35505831722025505, -1.3346151665443777, qubits[1]);

    }


    internal operation _Circuit31101_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(2.22466269124712, -0.6862547323927055, 2.168538149114351, qubits[0]);
        U3(2.0117781390610046, 0.8243769595909249, -2.291936644448966, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(1.9333345918643812, -PI(), -PI() / 2.0, qubits[0]);
        U3(1.6534191633582218, 0.31930690844445886, -1.456517483999301, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(0.3879862513495968, -1.4131793699707667, -2.9568984015178987, qubits[0]);
        U3(2.635658882134798, 2.730512606391942, 1.714656425985317, qubits[1]);

    }


    internal operation _Circuit31104_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(PI(), 0.1699184547270609, -1.400877872067836, qubits[0]);
        U3(1.690324801691192, -PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.6648493632135961, 0.22079533389086858, -1.4533410883999114, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(0.0, 0.05514023891176123, 1.7239168500096111, qubits[0]);
        U3(3.0220641786934994, 0.0, PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31107_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(1.6838376359198337, -0.1262369478149079, -2.4149933725452737, qubits[0]);
        U3(1.6903248016911914, -PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.584229735111584, 1.093483420759001, -1.515594615720154, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(1.4577550176699623, -1.0568966358737768, 1.9255455385658768, qubits[0]);
        U3(3.0220641786934994, -0.024549898837883166, PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31110_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(0.7550704300944633, 0.889577386579214, -2.608294793314319, qubits[0]);
        U3(1.690324801691193, -PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.6013854414278288, 0.8415752337852407, -1.4906887105111792, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(2.386522223495331, -0.20300050544622295, -3.0875742197588565, qubits[0]);
        U3(3.0220641786934985, -1.9389455096557482, PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31113_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(2.311923064035886, -0.289039561328293, -1.9856934446488212, qubits[0]);
        U3(1.451267851898601, PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.655545153701213, 0.3007758213131182, -1.4558339820108888, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(0.8296695895539058, 3.0665324451899894, 0.0, qubits[0]);
        U3(0.1195284748962941, -1.34801569982323, -PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31116_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(1.283847717867271, 1.091607425089716, -2.9955839178879087, qubits[0]);
        U3(1.4512678518985997, PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.6092103715021282, 0.7487627767775287, -1.4827046656161356, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(1.857744935722523, -0.2995525182414416, 1.8334105283685176, qubits[0]);
        U3(0.1195284748962948, 2.9188120266181325, -PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31119_(qubits : Qubit[]) : Unit is Adj + Ctl {

        U3(0.0, 3.090170118268813, 1.6222188621158766, qubits[0]);
        U3(1.690324801691192, -PI() / 2.0, -PI(), qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), -0.19283580794916189, 1.377960518845736, qubits[0]);
        U3(1.6362893160372554, 0.47355335076167737, -1.4637074826979468, qubits[1]);
        CNOT(qubits[0], qubits[1]);
        U3(PI(), 2.1053683562981114, 0.9982196385040218, qubits[0]);
        U3(0.11952847489629416, PI() / 2.0, -PI() / 2.0, qubits[1]);

    }


    internal operation _Circuit31122_(qubits : Qubit[]) : Unit is Adj + Ctl {
        U3(0.0, -PI(), -PI(), qubits[0]);
        U3(PI(), PI() / 2.0, -PI() / 2.0, qubits[1]);
    }

    operation OracleExample1(qubits : Qubit[]) : Unit is Adj + Ctl {

        SwapReverseRegister(qubits);
        _Circuit31080_([qubits[0], qubits[1]]);
        U3(0.0, 0.0, -PI() / 2.0, qubits[3]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 3.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, -PI() / 3.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit31083_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, 0.0, qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit31086_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(-PI() / 2.0, 0.0, 0.0, qubits[2]);
        U3(0.0, 0.0, PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, PI() / 2.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit31089_([qubits[0], qubits[1]]);
        CNOT(qubits[0], qubits[3]);
        CNOT(qubits[1], qubits[3]);
        CNOT(qubits[0], qubits[3]);
        CNOT(qubits[2], qubits[3]);
        CNOT(qubits[0], qubits[3]);
        CNOT(qubits[1], qubits[3]);
        CNOT(qubits[0], qubits[3]);
        _Circuit31092_([qubits[0], qubits[1]]);
        U3(0.0, 0.0, -PI() / 2.0, qubits[3]);
        CNOT(qubits[2], qubits[3]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(0.0, 0.0, 2.0 * PI() / 3.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, PI() / 3.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit31095_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, 0.0, qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit31098_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(-PI() / 2.0, 0.0, 0.0, qubits[2]);
        U3(0.0, 0.0, PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, 5.0 * PI() / 12.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, PI() / 4.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, PI() / 12.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit31101_([qubits[0], qubits[1]]);
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
        U3(0.0, 0.0, PI() / 2.0, qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[1], qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[0], qubits[3]);
        _Circuit31104_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[3]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -5.0 * PI() / 8.0, qubits[3]);
        CNOT(qubits[1], qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI(), 0.0, 0.0, qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit31107_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(0.0, 0.0, -3.0 * PI() / 8.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, PI() / 6.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, PI() / 6.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, 5.0 * PI() / 8.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit31110_([qubits[0], qubits[1]]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, -PI() / 8.0, qubits[3]);
        CNOT(qubits[1], qubits[3]);
        U3(0.0, 0.0, -PI() / 8.0, qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, -PI() / 8.0, qubits[3]);
        CNOT(qubits[2], qubits[3]);
        U3(0.0, 0.0, PI() / 8.0, qubits[3]);
        CNOT(qubits[0], qubits[3]);
        U3(0.0, 0.0, PI() / 8.0, qubits[3]);
        CNOT(qubits[1], qubits[3]);
        U3(0.0, 0.0, PI() / 8.0, qubits[3]);
        CNOT(qubits[0], qubits[3]);
        _Circuit31113_([qubits[0], qubits[1]]);
        U3(0.0, 0.0, -3.0 * PI() / 8.0, qubits[3]);
        CNOT(qubits[2], qubits[3]);
        U3(0.0, 0.0, -PI() / 2.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -3.0 * PI() / 8.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(0.0, 0.0, -3.0 * PI() / 8.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, PI() / 2.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit31116_([qubits[0], qubits[1]]);
        U3(PI(), 0.0, 0.0, qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[1], qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        CNOT(qubits[0], qubits[2]);
        _Circuit31119_([qubits[0], qubits[1]]);
        U3(PI() / 2.0, 0.0, PI(), qubits[2]);
        U3(0.0, 0.0, -PI() / 2.0, qubits[2]);
        CNOT(qubits[0], qubits[2]);
        CNOT(qubits[1], qubits[2]);
        CNOT(qubits[0], qubits[2]);
        U3(0.0, 0.0, -PI() / 2.0, qubits[2]);
        CNOT(qubits[1], qubits[2]);
        _Circuit31122_([qubits[0], qubits[1]]);

        Exp([PauliI, PauliI, PauliI, PauliI], -0.2222, qubits);
        SwapReverseRegister(qubits);
    }



    operation OracleEmpty(qubits : Qubit[]) : Unit is Adj + Ctl {}


}
