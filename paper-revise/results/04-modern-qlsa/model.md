# Resource model and integration contract

**Archived 9 September query-only model.** The user subsequently selected the near-optimal Algorithm-3 analytic bound and requested a finite T-count estimator. See [t-count-model.md](t-count-model.md) and `t_count.py` for the current model; task 02 now exists and is used there. Keep this model only as an Algorithm-4/norm-informed alternative.

## Assumptions and common problem

**A04-input (unresolved for task 02):** square invertible A and nonzero b; both solvers receive the same A,b and requested scalar output. The implemented example uses task 03's diagnostic A=.5I+.15Z+.2X, b=(1,1)/√2, N=2, s_row=s_col=2, κ₂=3, ||A||=.75. This is not an application benchmark. `epsilon_trace_algorithm=.01` is an allocated state-error budget, not task 02's missing scientific tolerance. There is no chosen hardware configuration: both branches must receive identical task-06/07 hardware assumptions and optimization policies once supplied.

**A04-access (conditional mathematical promise):** U_A exactly block-encodes A/α; U_b prepares b/||b||, including controlled and adjoint access. Define

K = α/σ_min(A) = (α/||A||)κ₂(A),  A_eff=A/α,  b_eff=b/||b||.

The local input `operator_norm` must be exact/certified, or the user must ensure the combined ratio gives a valid inverse-gap upper bound. In particular, plugging an upper bound for ||A|| into the denominator can underestimate K. κ₂ itself may be an upper bound only when the resulting K is certified. The diagnostic has α=1 and K=4, **not 3**. α is an access-normalization parameter; scalar normalization leaves κ₂ unchanged. The scaled solution norm is α||A⁻¹b||/||b||. Norm-informed input t refers to this scaled quantity. Padding reserves a new basis state: n_pad=ceil(log₂(N+1)); padding zeros do not redefine original pp.N or κ₂.

Sparsity is explicit metadata, not a hidden factor multiplying the bound. It affects α and implementation of U_A. Task 05 must select reversible row/column position and value access, a table/QRAM circuit or an analytic stencil, construct the block encoding, and certify its normalization and cost. No relationship s=κ=log N is assumed. Preconditioning requires new effective parameters and recovery costs while preserving original pp.

**A04-ideal (established under reference promises):** the formulas below concern ideal access and exact phase sequences. The runnable domain is 0<ε_alg≤0.1. Unknown-norm evaluation conservatively raises K to at least 2 to avoid the degenerate zero-stage case at K=1. This implementation restriction is not a limitation asserted for QLSAs generally.

## Unknown norm: selected baseline

Use Dalzell v2 Algorithm 4 and its fixed Table 2 parameters: β̂=15.4, χ̂=.0398, ĉ=20, r̂=3.37, q̂=5.41, Δ̂=.00424. Kernel reflection stages estimate norms along a sequence of modified operators; a final kernel projection filters the output. The finite bound is

Q_A ≤ 56K + 1.05K ln(√(1−ε_alg²)/ε_alg) + 2.78(ln K)³ + 3.17,
Q_b ≤ 2Q_A.

Here Q_A combines forward/adjoint/controlled block-encoding queries. Q_b combines the corresponding RHS-unitary queries. **Both are upper bounds on expectations for a delivered state**, already including internal failures, restarts and norm discovery. They are neither realized integer counts nor capped runtime bounds. The output guarantee is trace distance of the ensemble, not a guarantee for every random trajectory. These are Eq. (133) of [Dalzell v2](https://arxiv.org/html/2406.12086v2#Thmtheorem4); the lower-order terms must be retained in finite comparisons.

The local model evaluates that expression; it does not simulate Algorithm 4 or its stochastic trace. For B independent output preparations, BQ_A is a valid expectation upper bound with the same per-state promise. Task 05 must not apply another 1/p success factor to Q_A. Reusing a norm estimate would require a new certificate and model: this implementation conservatively repeats the complete solver. The baseline cannot silently amortize its norm-discovery cost away.

**A04-compilation (unresolved):** let g_A,g_b bound the compiled cost of the most costly required controlled/adjoint variant, including internal work and uncomputation. For each exclusive primitive bucket g,

E[G_g] ≤ Q_A g_A,g + 2Q_A g_b,g + H_g.

H_g is an independently supplied bound on expected non-oracle control/filter/measurement work over all stochastic paths; it is not zero. The same serial-work construction applies to expected layer counts using D_A,D_b,H_D and DT_A,DT_b,H_DT. It is not a deterministic depth or hardware makespan. Supply a full schedule for QEC. Peak qubits must be a lifetime maximum, never a query-weighted expectation. Algorithm 4's additional registers for rectangular intermediate operators and comparisons are not covered by Algorithm 1's ancilla statement.

## Certified norm: separately costed core

**A04-norm (assumed only with certificate):** a supplied t∈[1,K] satisfies ||x_eff||/t∈[1/β,β], β≥1. Its discovery/certification cost is separate. Set η=ε_alg/√(1+β²) and ℓ=ceil(K ln(2/η)/2). This conservative degree follows Eq. (6), avoiding the numerical singularity in Eq. (72) at K=1. One Algorithm 1 attempt has:

| Resource | Count |
|---|---:|
| controlled U_A / U_A† | ℓ each |
| controlled U_b / U_b† | 2ℓ each |
| QSVT projector-controlled NOT macros | 4ℓ |
| QSVT single-qubit rotations | 2ℓ |
| QSVT polynomial degree | 2ℓ |

The last two macro counts exclude block-encoding construction gates and endpoint logic. In particular each augmented A_t query uses a controlled rotation and equality checks; b′ preparation also has controls. These must be included in `g_Gt` below. A multi-controlled NOT is not one Clifford or one T gate.

For θ=atan(||x_eff||/t), cos θ≥1/√(1+β²) and sin(2θ)≥2/(β+β⁻¹). Theorem 1 therefore gives conditional trace error ≤ε_alg and

p_min = [2/(β+β⁻¹)]² [(1−η)/(1+η)]².

Expected attempts ≤1/p_min is diagnostic only, not included in this core. With independent identical trials and ideal access, task 05 can choose R=ceil(ln δ_retry / ln(1−p_min)) for a one-state delivery cap. This is an external multiplicity applied once. A batch needs its own failure allocation.

An implementable serial accounting template for each gate bucket is

G_core,g ≤ 2ℓ g_Gt,g + 4ℓ g_projector,g + 2ℓ g_rotation,g + g_endpoint,g.

`g_Gt` bounds either U_Gt or its inverse and includes the controlled original queries, augmented-operator/RHS circuits, and all uncomputation. Depth/T-depth follow the same expression with compiled layer costs. Endpoint cost includes initial basis-state preparation, success tests and measurement/reset, so task 05 must not add these twice. This template becomes numeric only with a circuit compiler, phase list and synthesis specification. `logical_model.py` exposes the exact supported macro counts and leaves compiled values null.

Theorem 1 quotes a+3 ancillas beyond the padded system. Appendix A.4 describes a+2 block-encoding ancillas for G_t, while Figure 11's caption calls it a+1. This apparent bookkeeping inconsistency needs a register-lifetime reconstruction before a numerical peak is certified. Store the theorem statement as a quoted analytic count, not a QEC allocation. Also add oracle workspace, multi-control decomposition ancillas, retained input memory and any padding workspace as actually live; do not count a twice.

## Precision, output and task 05 boundary

Arithmetic bit widths, oracle implementation error, QSVT phase-generation error and rotation synthesis tolerance are **not supplied by these query bounds**. They remain unresolved; ε_alg is not a bit width. For a fixed conditional-core circuit, operator-norm implementation errors telescope: ζ≤Σ_i ν_i. If ζ<√p_min, the implemented success bound is at least (√p_min−ζ)² and an additional normalized-state vector error is at most 2ζ/(√p_min−ζ). This follows by projecting both full output vectors, bounding their norm difference by ζ and normalizing; it also upper-bounds trace distance. Task 05 can allocate this allowance to per-call tolerances, then task 04/05 must compile those tolerances. Entrywise rounding error must first be converted to operator/block-encoding error. This deterministic argument does not by itself certify Algorithm 4's adaptive unbounded path: truncate/certify that protocol and account for all branches before QEC.

For ||O||≤1, |Tr[O(ρ−|x><x|)]|≤2ε_trace. Thus task 03's normalized-vector error bound implies a trace bound and can share this conservative observable conversion. A physical linear functional of x may require ||x|| and ||b|| recovery, not merely a normalized-state observable. A constant-factor norm certificate sufficient for Algorithm 1 is generally insufficient for accurate physical norm recovery. Discretization, estimation confidence and QEC failure remain distinct budgets.

| Cost | Owner / accounting boundary |
|---|---|
| Solver's internal A/b calls and control work | 04; imported once into attempted/delivered-state stage |
| Classical input generation, storage/loading, oracle construction, phase computation | 05 setup/reuse record; compilation cooperation with 04 |
| Implementation of every controlled/adjoint A/b query | 05 supplies prices; 04 expressions expand them once |
| Algorithm 4 norm discovery and internal retries | Already in its Q_A,Q_b; H must include their control work |
| Norm certificate for Algorithm 1 | 05 setup or per-RHS; explicit cost, error and invalidation rule |
| Algorithm 1 external retries | 05; absent from its per-attempt core |
| Scientific-output estimation, norm recovery, shot/coherent calls | 05; coherent estimation requires a unitary solver adapter, not inversion of a stochastic mean |
| QEC factories, routing, scheduling, full-workload failure | 06 after gates, lifetimes and caps resolve |
| Seconds, physical qubits, joules | 06/07, then comparison in 09 |

## Public interface and completion boundary

Task-01 v1.0.0 is used without modification. Exported stage fragments cover `q.core`, have multiplicity one and `queries_expanded=false`. The two fragments are alternatives; they cannot coexist as additive primitive stages in one branch. Original pp remains separate from cq's effective K, α, precision and algorithm/version. Quantity units are gate/query/layer/logical_qubit, never seconds. The unknown-norm stage's expected counters are annotated; the core's counters are per attempt. Full-workload validation and scientific certification are task 05's responsibility after assembly.

Required unresolved inputs: task-02 generator/version, output/error/access/preconditioning contract; certified α and spectral gap; U_A/U_b implementations with all control levels and workspace; phase lists and precision certificates; missing non-oracle costs and register lifetimes; norm certification where used; repetition/termination and complete error budgets; common QEC and hardware configurations. Task 03's 417852 controlled one-sparse calls cannot be compared numerically to Q_A, since their primitive meanings and error allocations differ. Finite query improvements alone determine neither a practical speedup nor the direction/magnitude of a crossover shift.
