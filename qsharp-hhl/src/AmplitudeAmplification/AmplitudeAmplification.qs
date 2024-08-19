// not used at the moment

/// # Sample
/// Grover's search algorithm
///
/// # Description
/// Grover's search algorithm is a quantum algorithm that finds with high
/// probability the unique input to a black box function that produces a
/// particular output value.
///
/// This Q# program implements the Grover's search algorithm.
namespace AmplitudeAmplification {
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Arrays;
    open Microsoft.Quantum.Measurement;
    open Microsoft.Quantum.Diagnostics;
    open CommonOperation;

    // @EntryPoint()
    // operation Main() : Result[] {
    //     let nQubits = 5;

    //     // Grover's algorithm relies on performing a "Grover iteration" an
    //     // optimal number of times to maximize the probability of finding the
    //     // value we are searching for.
    //     // You can set the number iterations to a value lower than optimal to
    //     // intentionally reduce precision.
    //     let iterations = CalculateOptimalIterations(nQubits);
    //     Message($"Number of iterations: {iterations}");

    //     // Use Grover's algorithm to find a particular marked state.
    //     let results = GroverSearch(nQubits, iterations, ReflectAboutMarked);
    //     return results;
    // }

    /// # Summary
    /// Implements Grover's algorithm, which searches all possible inputs to an
    /// operation to find a particular marked state.
    operation ApplyAmplitudeAmplification(
        nQubits : Int,
        iterations : Int,
        marked : Int[],

    ) : Result[] {

        use qubits = Qubit[nQubits];

        // Initialize a uniform superposition over all possible inputs.
        PrepareUniform(qubits);

        // The search itself consists of repeatedly reflecting about the marked
        // state and our start state, which we can write out in Q# as a for loop.
        for _ in 1..iterations {
            ReflectAboutMarked(marked, qubits);
            ReflectAboutUniform(qubits);
        }

        // Measure and return the answer.
        return MResetEachZ(qubits);
    }

    /// # Summary
    /// Returns the optimal number of Grover iterations needed to find a marked
    /// item, given the number of qubits in a register.
    function CalculateOptimalIterations(nQubits : Int) : Int {
        if nQubits > 126 {
            fail "This sample supports at most 126 qubits.";
        }

        let nItems = 2.0^IntAsDouble(nQubits);
        let angle = ArcSin(1. / Sqrt(nItems));
        let iterations = Round(0.25 * PI() / angle - 0.5);
        iterations
    }

    /// # Summary
    /// Reflects about the basis state marked by alternating zeros and ones.
    /// This operation defines what input we are trying to find in the search.
    operation ReflectAboutMarked(marked : Int[], inputQubits : Qubit[]) : Unit {
        // marked represents the direct notation, e.g. [0,1,0,1] -> |0101>
        Message("Reflecting about marked state...");
        use outputQubit = Qubit();
        within {
            // We initialize the outputQubit to (|0⟩ - |1⟩) / √2, so that
            // toggling it results in a (-1) phase.
            X(outputQubit);
            H(outputQubit);
            // Flip the outputQubit for marked states.
            // Here, we get the state with alternating 0s and 1s by using the X
            // operation on every other qubit.
            for i in 0..Length(inputQubits) {
                if (marked[i] == 1) {
                    X(inputQubits[i]);
                }
            }
        } apply {
            Controlled X(inputQubits, outputQubit);
        }
    }


    /// # Summary
    /// Reflects about the all-ones state.
    operation ReflectAboutAllOnes(inputQubits : Qubit[]) : Unit {
        Controlled Z(Most(inputQubits), Tail(inputQubits));
    }

    /// # Summary
    /// Reflects about the uniform superposition state.
    operation ReflectAboutUniform(inputQubits : Qubit[]) : Unit {
        within {
            // Transform the uniform superposition to all-zero.
            Adjoint PrepareUniform(inputQubits);
            // Transform the all-zero state to all-ones
            for q in inputQubits {
                X(q);
            }
        } apply {
            // Now that we've transformed the uniform superposition to the
            // all-ones state, reflect about the all-ones state, then let the
            // within/apply block transform us back.
            ReflectAboutAllOnes(inputQubits);
        }
    }
}
