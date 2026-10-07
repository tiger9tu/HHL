# Proposed manuscript replacements

These passages replace the claims in the supplied PDF; no editable TeX source is available locally. Integrate with task 10's framework-first rewrite and renumber equations there.

## Proposition 1 and main-text scaling discussion (p. 3)

**Proposition 1 (conditional logical cost of the HHL case study).** Let H=A/α be Hermitian and let H=Σ_(a=1)^L H_a be a supplied Hermitian one-sparse decomposition. Write C_comm=Σ_(a<b)||[H_a,H_b]||. A first-order product formula with r steps approximates exp(iHτ) with operator error at most τ²C_comm/(2r). The bound holds for arbitrary matrix-element positions. It depends on the decomposition and its norms; row sparsity s alone does not determine its prefactor.

For phase estimation with controlled evolution times τ_j and its inverse, choose r_j so that C_commΣ_j τ_j²/r_j≤η_PF. The resulting circuit uses 2LΣ_j r_j controlled one-sparse evolutions per attempt. If the reference circuit has success probability at least p_min, this simulation error contributes at most 2η_PF/√p_min to the normalized successful joint state. A separate analysis must certify the reference phase-estimation and reciprocal-filter error. State preparation, gate synthesis, oracle implementation, and output sampling complete the logical workload before error correction and hardware modeling.

Our previous expressions (1)–(2) used an empirical matrix-error estimate to assign an exact resource prefactor. We replace that estimate with the bound above and retain compiled module costs as explicit inputs to the framework. Efficient decomposition and oracle access are not assumed solely from a fixed sparsity pattern. A generic construction and a structured application can have different numbers of summands and different access costs, which must be counted separately.

## Appendix B replacement

Replace B1–B28 by the definitions, proof, postselection inequality and schedule R1–R5 in `derivation.md`. The revised derivation bounds the difference between implemented and target unitaries directly. It does not equate a time-ordered exponential to a first-order truncation, and it does not infer an effective matrix perturbation from a principal logarithm without branch control. Cite Childs et al., *Theory of Trotter Error with Commutator Scaling*, Phys. Rev. X 11, 011020 (2021), Proposition 15; the proof of the looser pairwise bound is given explicitly in the replacement appendix.

The HHL state-output setting should retain a citation to Harrow, Hassidim and Lloyd, *Quantum algorithm for solving linear systems of equations*, Phys. Rev. Lett. 103, 150502 (2009), [primary paper](https://arxiv.org/abs/0811.3171). Its oracle/state-output assumptions do not by themselves certify the finite-clock demonstration circuit or its compiled costs.

## Figure 9 caption

**Figure 9. Finite-dimensional validation of a deterministic first-order product-formula bound.** All norms are spectral norms; matrices are normalized to ||H||₂=1. Left: median operator error ||S_r(τ)−exp(iHτ)||₂ versus matrix dimension N at τ=1 and r=4. Shaded bands are empirical 5th–95th percentiles, not confidence intervals. Each synthetic family uses 24 independently generated matrices at each N∈{8,16,32,64,128}, with four weighted matching terms and independent U[−1,1] edge weights. The fixed-band family uses cyclically shifted adjacent pairings; the random-matching family uses independent uniform vertex permutations for each term. The fixed-band construction may reuse supports, so four terms do not imply row sparsity four. The PDE curve uses one deterministic five-point Dirichlet Poisson matrix at each N∈{9,25,49,81,121}, decomposed into a diagonal and four parity matchings; no sampling interval is assigned to those points. Middle: histogram of error divided by τ²C_comm/(2r), at N=64, τ=1,r=4, with 24 matrices per synthetic family. Right: pair-commutator norm histograms for the same matrices, 144 pairs per family; pairs within a matrix are dependent. Seeds start at 20260908; per-matrix seeds, measured sparsity, term counts, conditioning, errors and descriptive uncertainty are archived in the accompanying data. The broader run uses two/four matching terms, τ=.1/1, and r=1/2/4/8, totaling 485 matrices and 3880 measurements. These finite samples test implementation and illustrate bound tightness; validity for arbitrary N follows from the proof, not extrapolation of the histograms.

## Application scaling (provisional; reconcile with task 02)

Sparsity and conditioning are independent benchmark inputs. For the unpreconditioned five-point Dirichlet Poisson operator on a square grid, N=m_grid², s≤5 and κ=cot²[π/(2(m_grid+1))]=Θ(N). Its normalized diagonal/parity-matching decomposition has five terms and a uniformly bounded commutator sum, but the increasing condition number still affects phase estimation and successful-state preparation. Thus a size-uniform Hamiltonian-simulation coefficient does not imply a size-uniform HHL cost. Logarithmic sparsity/conditioning sweeps represent explicitly assumed sensitivity scenarios rather than a generic scientific workload. Preconditioning requires a separately costed effective operator and solution-recovery map.

## Dependent abstract, results and conclusion language

Replace the abstract's specific crossover/resource sentence and any conclusions repeating it with:

“We organize resource comparisons into logical algorithm, input/output, error-correction and hardware layers. The revised HHL case study uses a deterministic simulation-error bound and explicit success/error budgets. Numerical crossover locations require these costs to be combined with a specified application output and classical implementation; the earlier crossover range is not retained as a validated estimate.”

For Figure 1 and all dependent resource curves, remove numerical advantage labels pending tasks 05–09 and use a temporary editorial marker: “Recompute using revised logical schedule, common output/error target, complete access/readout costs, and matched classical/hardware assumptions.” Do not present old plotted data under the replacement caption. The reported 2^33–2^48 range and associated physical qubit, runtime and energy numbers cannot be carried forward unchanged, nor repaired by a universal `60s` multiplier. The corrected sufficient bound does not predict the direction or magnitude of an actual optimized crossover shift.

Use N for matrix dimension, L for number of summands, m for clock width, b_bits for entry precision, r_j for product-formula steps, G_T for T/T† count, and t_wall for physical runtime. Correct “Taylor,” “Dyson,” and “Toffoli” in the relevant derivation. Retain explicit oracle, loading, readout, algorithm and hardware limitations when task 10 assembles the conclusion.
