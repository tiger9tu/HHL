namespace HamiltonianEvolution {
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;

    operation HamiltonianEvolutionSample1(targetRegister : Qubit[], power : Int) : Unit is Adj + Ctl {
        Rx(- 2.0 * IntAsDouble(power) * 2.0 * PI() / 4.0, targetRegister[0]) // exp(i*2pi*X)
    }


}