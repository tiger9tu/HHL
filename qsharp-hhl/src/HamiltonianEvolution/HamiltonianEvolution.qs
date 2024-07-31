namespace HamiltonianEvolution {
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;

    operation HamiltonianEvolutionSample1(power : Int, targetRegister : Qubit[]) : Unit is Adj + Ctl {
        Rx(- 2.0 * IntAsDouble(power) * 2.0 * PI() / 4.0, targetRegister[0]) // exp(i*2pi*X)
    }

    operation HamiltonianEvolutionSample2(power : Int, targetRegister : Qubit[]) : Unit is Adj + Ctl {
        Exp([PauliX, PauliX], 1.0 * IntAsDouble(power) * 2.0 * PI() / 4.0, targetRegister); // exp(i*2pi*X)
    }


}