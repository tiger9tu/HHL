# Corrected analysis (proposed replacement, 8 September 2026)

## Status and notation

This is a deterministic, conservative replacement for the argument underlying “Statement 1” in the review (Proposition 1 in the supplied PDF, p. 3). It is **not** a proof of its original gate-count prefactor. Task 01's directory was initially empty, but its v1.0.0 contract appeared during the run and was used for the validated stage export. Task 02's handoff remains absent, so application reconciliation is pending; see resource-model.md.

Let N be matrix dimension, n_sys = ceil(log2 N), s the maximum nonzeros per row, L the number of supplied Hermitian summands, b_bits entry precision, m the clock width, and r_j the number of product-formula steps. None of these is interchangeable. All norms below are spectral/operator norms, or Euclidean norms for vectors. Evolution time τ is in inverse units of the normalized matrix; physical runtime is t_wall in seconds. Normalize H=A/α, with a declared α ≥ ||A||. For the SPD specialization assume eigenvalues of H in [1/κ_bound,1]. If α=||A||, κ_bound is the spectral condition number. The exact normalization used in the experiments is classical diagnostic preprocessing, not an assumed efficient quantum operation.

## A supported bound, without fixed positions

Given **any** Hermitian decomposition H=Σ_(a=1)^L H_a and integer r≥1, define

S_r(τ) = (exp(iH_1 τ/r) ··· exp(iH_L τ/r))^r,
C_comm = Σ_(a<b) ||[H_a,H_b]||.

Then, in exact arithmetic,

**||S_r(τ)−exp(iHτ)|| ≤ min{2, τ² C_comm/(2r)}.** (R1)

For two terms, variation of parameters represents the local error as a double integral of unitarily conjugated commutators. Unitary invariance bounds its integrand by ||[H_1,H_2]||; the integration triangle has area |τ/r|²/2. Add terms by telescoping the splitting, then use ||[H_a,Σ_b H_b]||≤Σ_b||[H_a,H_b]||. Finally U^r−V^r=Σ_(k=0)^(r−1) U^k(U−V)V^(r−1−k) gives r times the one-step bound. Both operators are unitary, giving the independent ceiling 2. This proof holds for arbitrary finite N, arbitrary positions and weights, and either sign of τ. It is a deliberately looser pairwise version of Childs et al., Proposition 15, Eq. (145), [primary source](https://arxiv.org/html/1912.08854v3#S5.SS1).

A simple analytic envelope is C_comm≤2Σ_(a<b)||H_a||||H_b||≤L(L−1)Λ², with Λ=max_a||H_a||. Thus a dimension-uniform guarantee exists **if L and Λ are uniformly bounded for the specified family and normalization**. It does not follow merely from ||H||=1: decompositions can contain cancelling large terms. Neither a histogram nor a lack of visible trend establishes these hypotheses. Even under them, HHL's evolution times, conditioning, access costs, precision, and repetitions may grow with N.

For a real symmetric s-sparse matrix, a classical greedy edge coloring supplies a position-independent existence construction: color off-diagonal undirected edges using at most 2Δ−1 colors (an edge conflicts with at most 2Δ−2 previously colored incident edges), with Δ≤s; put the diagonal in a separate term. Each color is a weighted matching and hence Hermitian one-sparse. This gives L≤2s for s≥1 (omit absent terms), without assuming L=s. With α=||A||, each term has norm at most max_ij |A_ij|/α≤1. A simple preprocessing implementation costs O(Ns²) work and O(Ns) stored edges; it is not a free coherent oracle. Table lookup, reversible computation and compilation must be charged. The repository's implicit coloring scheme instead enumerates L=6s²; its correctness and access implementation must be validated before resource use. For general complex Hermitian inputs, matching terms can carry conjugate weights, but the real-only HS1 circuit's gate estimate does not automatically apply.

## Why B8–B21 cannot be retained as written

B5 is a time-ordered exponential. B6–B7 are truncated expansions, so matching them does not establish the exact equality B8/B9, nor eliminate higher-order commutators. The first equality of B18 therefore has not been proved. A logarithm of a unitary is also nonunique. In particular, principal Log(exp(iHt))/(it) can differ from H when eigenphases wrap. Good operator error at one τ does not by itself certify an effective-Hamiltonian error or one common perturbed H across every QPE power. The matrix logarithm should be used only as a branch-qualified finite-instance diagnostic here.

B19 supplies neither a distribution nor a failure probability and omits decomposition/norm parameters. Remove it, not just the adjective “probabilistic.” The old Z,X example at τ=.2 has B18 RHS .2, not .1, and an effective logarithm error close to .2009, not exactly the bound (see validation.json). A further stress test has H_1=2Z, H_2=2X, H_3=−2Z, H_4=−2X, H_5=I. H=I is normalized SPD, each summand is Hermitian one-sparse, yet at τ=.001,r=1 its effective-Hamiltonian error exceeds .001. This is a cancelling decomposition counterexample to a decomposition-independent reading of B19, **not** to a disjoint-entry coloring claim. R1 still holds. No empirical tail bound for the archived ensemble has been established.

B20 is valid for an unnormalized classical solve when q=||A^−1||||ΔA||<1: the resolvent identity bounds ||y−x||/||x||≤q/(1−q), with x=A^−1 b and y=(A+ΔA)^−1 b. For normalized states, use ||y/||y||−x/||x||||≤2||y−x||/||x||, hence at most 2q/(1−q). One cannot assert both ||A||=1 and ||A^−1 b||=1 for an arbitrary fixed normalized b. This repair does not salvage B21 because its ΔA premise is unproved. We use circuit errors instead.

## Propagation through phase estimation and postselection

Take controlled evolution times τ_j=τ_base 2^j, j=0,…,m−1. A controlled-unitary replacement has the same operator error as the underlying unitary; adjoints preserve that error. With inverse QPE included, telescoping gives

η_PF ≤ 2Σ_j [τ_j² C_comm/(2r_j)] = C_comm Σ_j τ_j²/r_j. (R2)

This is an error on the full premeasurement state/circuit, not a solution-state error. Let a be the successful branch of the **reference circuit with exact evolutions**, with ||a||²=p≥p_min>0. If its implemented branch is b, then ||a−b||≤η and

||a/||a||−b/||b||||≤2η/√p_min,
p_implemented≥(√p_min−η)², provided η<√p_min. (R3)

The normalization inequality follows by adding and subtracting b/||a|| and using the reverse triangle inequality. It applies to the whole successful joint state including the clock; tracing out the clock cannot increase trace distance. Thus a PF contribution ε_state,PF is guaranteed by η_PF≤ε_state,PF√p_min/2. Other circuit implementation errors must be included in η for the final success lower bound. The reference circuit's finite-QPE/filter error relative to |x> is a separate budget; it is not certified by choosing m in the adapter.

For ideal exact inversion, rotation amplitude c/λ gives p=c²||H^−1 b||². If c=1/κ and spectrum lies in [1/κ,1], p≥1/κ². A finite-clock approximate reciprocal needs its **own** success/filter guarantee before this bound can be used. The exact-grid two-dimensional test explicitly checks the reference state and success probability. Plain uniform-clock QPE plus a singular reciprocal at zero is not automatically covered by the original HHL analysis. Cutoffs, tails, signed spectra, overflow and rotation synthesis need explicit treatment.

An expected number of independent attempts is 1/p_implemented; to obtain one success with failure probability δ_rep, a sufficient integer cap is ceil(log δ_rep / log(1−p_lower)), for 0<p_lower<1. Multiple successful samples required by the observable are additional. Amplitude amplification has a different circuit and query schedule; do not silently replace this repeat-until-success cost by √(1/p).

## Auditable logical-resource schedule

Let S=Σ_j |τ_j| and η_target=ε_state,PF√p_min/2. For C_comm>0 choose

r_j=max{1,ceil(C_comm S |τ_j|/η_target)}. (R4)

Each forward error is at most η_target|τ_j|/(2S), hence (R2) is at most η_target. If C_comm=0 use r_j=1. The number of controlled one-sparse exponentials including uncomputation is

K_HS1=2LΣ_j r_j ≤ 2L[m + C_comm S²/η_target]. (R5)

This count treats the supplied decomposition literally and does not merge adjacent terms. If H_a have different implementation costs, use Σ_j r_j Σ_a (cost_a,forward+cost_a,inverse) and optionally optimize the allocation using those weights. All coloring, value/position queries, uncomputation, controlled rotations and synthesis must be included in the per-term cost. Finite entry error ||ΔH|| contributes at most |τ_j|||ΔH|| per evolution by Duhamel's formula and requires its own total circuit budget.

For counts per attempt, G_attempt=G_prep+G_QPE,nonHS+G_recip+G_inverseQPE,nonHS+Σ_(j,a) r_j(G_HS1,a+G_HS1,a†)+G_success. Apply repetitions exactly once outside. Sequential depth is a conservative sum of compiled depths, not a T-count. Peak logical qubits are n_sys+m+1 plus simultaneously live workspace and preparation/readout ancillas, not the sum of all module workspaces. Rotations need a gate-set/synthesis specification before T-counts are numerical. Physical qubits, seconds and joules belong to tasks 06–07.

For orientation only, if a separately justified QPE scheme has S=O(κ/ε_QPE) and reference p_min=Ω(κ^−2), (R5) gives a sufficient PF cost O(L C_comm κ³/(ε_QPE² ε_state,PF)), plus clock terms, per attempt. With comparable error budgets this is O(L C_comm κ³/ε_state³). Repeat-until-success may add O(κ²). This is a conservative upper bound for the chosen proof strategy, **not** an optimal HHL complexity or a lower bound on runtime. A larger sufficient budget cannot establish that an advantage is impossible. Do not retain √(320/3)πκ²s/ε² or infer a replacement physical crossover from this expression alone.

## Provisional PDE specialization

The temporary family is the five-point −Δ discretization on (0,1)² with zero Dirichlet boundary conditions and m_grid interior points per side. N=m_grid², h=1/(m_grid+1), s≤5. Eigenvalues of the unscaled discrete operator are

λ_pq=4h^−2[sin²(pπ/(2(m_grid+1)))+sin²(qπ/(2(m_grid+1)))].

This follows directly by substituting tensor-product sine vectors into the stencil. Hence κ=cot²(π/(2(m_grid+1)))=Θ(N). Normalize by λ_max. Split into the diagonal and two horizontal/two vertical parity matchings: L=5; the diagonal commutes with all terms, and matching norms are at most 1/[4+4cos(π/(m_grid+1))]. Thus C_comm≤12/[4+4cos(π/(m_grid+1))]² for this decomposition. This bound is uniform in N, although κ and required evolution times grow. In d fixed dimensions, the analogous tensor-grid family has s≤2d+1 and κ=Θ(N^(2/d)); no logarithmic κ assumption applies without a specified preconditioner and its quantum access/recovery costs.

These matrix-level facts do not supply task 02's chosen RHS, scalar observable, discretization tolerance, preconditioning or input/output oracle. `validate_pde.py` adds a smooth manufactured-solution diagnostic, not an agreed application benchmark. The unpreconditioned family is explicitly distinct from synthetic indefinite matching sums. No scientific output or classical crossover is claimed from these diagnostics.
