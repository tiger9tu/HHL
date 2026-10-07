# A callable T-count function

The user-selected main model is now **near-optimal unknown-norm Shortcut (Algorithm 3)** with an analytic query bound and an explicit stored-data block encoding. The earlier Algorithm-4 files remain archived alternatives; they are not the current default. `t_count.py:f(p)` returns one numeric expected logical T-count estimate. `estimate(p)` also returns all components, assumptions and precision choices. T includes T†.

```python
from t_count import f, estimate
p = {"N": 1024, "kappa": 100, "epsilon_state": 0.01}
T = f(p)
details = estimate(p)
```

The scope is **one normalized solution-state preparation**, including internal norm search, successful/failed solver attempts, matrix access, RHS unitaries, controls, and QSVT overhead. The function is a finite resource **estimate**, not a claim of a compiled circuit or certified scientific-output accuracy. It does not return seconds or QEC resources. Independent scientific-output repetitions are task 05's responsibility; do not multiply this output by another internal 1/p success factor.

## Parameter contract

| Input | Meaning / default |
|---|---|
| `N` | Original dimension, integer ≥2; D=2^ceil(log₂N) |
| `kappa` | Certified condition upper bound for the nonsingular, positively padded matrix; equal to the original condition number if padding is inside its spectral range |
| `epsilon_state` | Requested trace-distance design tolerance for a normalized state, default .01, maximum .1; not scientific output accuracy |
| `frobenius_over_spectral` | Optional certified upper bound ρ on ||A_pad||F/||A_pad||₂; default √D |
| `effective_inverse_gap` | Optional direct certified bound αF/σ_min for this Frobenius BE; bypasses κρ, mutually exclusive with the previous field |
| `delta_retry` | Ideal abort allowance used for the finite synthesis design horizon; default .002 |
| `query_bound` | `auto`: Costa Eq19 within its validity range, Dalzell Eq118 outside it; alternatively select either explicitly |
| `rotation_synthesis_offset` | Model offset in R=ceil(3 log₂(1/δ_rot)+offset), default 10; an explicit synthesis assumption, not a proved constant |
| `rotation_T_override` | Optional uniform T cost for every rotation at the returned tolerance; requires `rotation_override_certificate` provenance |
| `angle_bits_min` | Optional minimum stored angle precision, default 1; not matrix-entry precision |
| `instance_id` | Optional provenance label |

Unknown keys and invalid/nonfinite values are rejected. `kappa` never silently means inverse gap. A supplied direct inverse gap can be tighter than a loose condition upper bound; it must be certified independently. For generic padding choose a positive value inside the original spectral interval and record the resulting normalization; no singular padding is introduced into the base matrix. The separate Shortcut augmentation is described below.

## Published BE model and why this one

We use **Clader, Dalzell, Stamatopoulos, Salton, Berta and Zeng**, *Quantum Resources Required to Block-Encode a Matrix of Classical Data*, IEEE Transactions on Quantum Engineering 3, article 3103323 (2022), DOI [10.1109/TQE.2022.3231194](https://doi.org/10.1109/TQE.2022.3231194). Equations here are pinned to [arXiv:2206.03505v1](https://arxiv.org/html/2206.03505v1), Tables 1/3/4, Secs. IV.4 and V. The HTML is archived and hashed in sources.

This is the minimum-T-count, fixed-precision, select-swap construction for real stored data. It embeds A/||A||F. Sparsity does not make it cheaper automatically: a sparse input can use this circuit, but no stencil optimization is credited. Its explicit constants and circuit data-access costs make it a reproducible baseline. The task-02 compact analytic input must first be converted into its data trees; this classical work and storage are explicitly excluded from quantum T counts, not from the future end-to-end workload. It is not a recommended fastest implementation of task 02. A structured sparse circuit may replace this adapter later without changing f's scope.

Let n=log₂D, t=angle bits, and R=T cost per arbitrary one-qubit rotation. The published counts are

    A_T = 8(2t+3)D − 16t(n+1) + 4Rnt − 24,
    b_T = 8(t+1)(D−1) + 2tnR − 8tn,
    W_A = D(t+1) + 3n − t + 1.

The first is a BE query; the second prepares an arbitrary real RHS from a precomputed binary tree. W_A is the published uncontrolled BE workspace allocation. The construction uses a classical table of D rows of angle/sign data; it does not grant unit-cost free QRAM queries. It does assume ideal logical access/connectivity and does not price physical storage, routing or error correction.

### Our explicit control and wrapper allowances

These allowances are **our conservative composition**, not additional formulas attributed to Clader's tables. Define L=(D−1)t+D bits per angle/sign tree. Following the data-gating construction in Clader Sec. IV.4, gate and ungate the loaded tree before each of the two state-preparation operations. Charge four L-bit register Fredkin operations, including both directions, and control the n system swaps. For RHS state preparation charge two L-bit operations:

    cA_T = A_T + 28L + 7n,
    cb_T = b_T + 14L.

Each Fredkin is two CNOTs plus a Toffoli, charged at seven T gates; no four-T measurement-assisted discount is applied to these new gates. All-zero angle/sign trees produce the identity state-preparation circuit. Gate synthesis must preserve the cancellation on an inactive control, using matched rotation/adjoint sequences. These full conservative register-gating costs include uncomputation. No control is added indiscriminately to every compiled Clifford gate. Adjoints have the same count.

For a concrete clean-ancilla multi-controlled NOT, a ladder of c−2 AND computations, one target Toffoli, and its reversed ladder costs

    M(c) = 0 (c≤1),  7(2c−3) (c≥2).

This is an explicit elementary construction; it is not an optimal count. Seven-T Toffoli decompositions are standard, e.g. [Selinger, PRA 87, 042302 (2013)](https://arxiv.org/abs/1210.0974). No Toffoli total is added again after its T expansion.

To avoid nested controls due solely to padding, use an equivalent doubled-system augmentation

    A_t = (A/αF) ⊕ t_guess⁻¹ I_D,
    b′ = (b_normalized, e_0)/√2.

Its solution is (x_eff,t_guess e_0)/√2. It has the same norm angle and nonzero-gap promises used in the Shortcut proof. A_t requires one controlled U_A and a controlled rotation on a new block ancilla in the other branch; b′ requires a Hadamard on the branch bit and one controlled U_b. Projecting the reflected state onto the original branch returns the same solution. This doubling is a **derived equivalent implementation**, not an assertion that the source uses identity augmentation. It replaces the source's single-coordinate augmentation and introduces no additional norm-search cost. The dense validation checks the resulting block encoding and kernel reflection.

Use n_pad=n+1 and an intentionally generous projector width

    W = W_A + 2L + n + 8.

This reserves oracle/data-gating space and flags without aggressive recycling. The two projector-NOTs per QSVT query may test all the clean workspace; checking extra qubits that remain clean does not alter the encoded operator. A valid (loose) allocation for these ladders and retained registers is 3W+2n_pad+20. This is a modeled allocation, not a measured minimum. It is far above the abstract source's a+3 register count; the old ancilla ambiguity is not used to set this allocation.

Our uniform per-query envelope is

    g_slot = cA_T + 2 cb_T + 6M(n_pad) + 2M(W) + 5R.

It includes original A access, RHS preparation/unpreparation, system checks, QSVT projectors, and rotations. Six system checks cover augmentation/projection/endpoints conservatively per query rather than per complete filter. Five rotations cover the controlled augmentation (two rotations), one QSVT phase, and two reserved rotations. The KP stage has fewer operations but is charged the same envelope. This overcounts small endpoint work deliberately, instead of leaving an unspecified additive term. Measurements, reset, basis initialization and classical branching are T-free in this convention; they still have hardware time costs. The g_slot formula is a resource envelope for the described realization, not a reported empirical compiler count.

## Analytic query multiplier

Set K=max(3,κρ), or use the direct inverse-gap bound. Use ε_alg=ε_state/2. The convenient [Costa et al. Eq19](https://arxiv.org/html/2604.22185v2#S3.E19) is

    Q19 = K[6 ln K + 6 + 1.07 ln(1/ε_alg)] + 6 + 3 ln K.

**An important correction to the earlier conversation:** its underlying derivation, Dalzell Eq128, assumes **3≤K≤10⁶**. It must not be extrapolated as a proven bound to arbitrary N or K. For larger K the estimator automatically uses the original finite [Dalzell Algorithm 3, Eq118](https://arxiv.org/html/2406.12086v2#A5.E118):

    S = 3 + 2 ln((K²+1)/2), μ=1/4,
    η = μ/(sqrt(S)+μ),
    η_KP = ε_alg sqrt(1−μ²)/(μ sqrt(1−ε_alg²)),
    d_KR = 2 ceil(K ln(2/η)/2),
    d_KP = 2 ceil(K ln(2/η_KP)/2),
    q0 = [(1−η)/(1+η)]²/(ln K+1),
    Q118 = d_KR/q0 + d_KP/(1−μ²).

Both are upper bounds on expected ideal-access A queries and include the repeated norm guesses and filtering failures. The RHS query bound is twice that count and is already in g_slot. They are not empirical fits. Auto mode can have a downward discontinuity when switching from loose Eq19 to tighter Eq118; for smooth sweeps select Eq118 throughout. This model estimates the KP version of Algorithm 3, not Costa's empirically priced early-abort LCU filter.

The requested function is therefore

    f(p) = Q_selected(K, ε_alg) × g_slot(D,t,R).

It returns a float because it prices an expectation. `T_count_ceiling` is merely the rounded expectation; it is not a delivery cap. `components` are exclusive terms that sum to f(p). `capped_T_allocation_model` instead multiplies the full-query envelope by a finite ideal schedule cap, below.

## Precision and status of the estimate

One full independent cycle makes a random norm guess, runs KR and, if KR succeeds, runs KP. Its joint success probability is at least q0 (Dalzell Eq122). Choose C_cap=ceil(ln δ_retry/ln(1−q0)) and Q_cap=C_cap(d_KR+d_KP). The latter charges full filters even for early failures. This ideal cap is used to choose a finite synthesis horizon, not multiplied into the expected query bound.

Set ν=(ε_state/2)(1−δ_retry)/(32Q_cap),

    t = max(angle_bits_min, ceil(log₂(2πn/ν))),
    δ_rot = ν/(8tn).

Clader Eq41 then gives πn2⁻ᵗ+4tnδ_rot≤ν for the **full BE unitary**, not merely the top-left matrix. The RHS error fits the same conservative allowance. Angle-generation error must also fit the rounding allowance. Four component allowances per query slot leave room for A, b, b† and wrapper rotations. This is a conservative precision design, with slack for postselection; it does not equate expected path length with the maximum number of faulty operations.

The published synthesis expression is 3log₂(1/δ_rot)+O(log log(1/δ_rot)), not a universally certified finite formula. We expose the assumption **R=ceil(3log₂(1/δ_rot)+10)** and provide offset sensitivity plus an override for independently certified compiled costs. The +10 is our modeling choice, not a theorem from the paper. Consequently the final T value is explicitly an estimate even though its ideal query multiplier is a theorem bound. To certify an actual finite implementation, supply phase lists, rotation synthesis records (with correct phase convention), finite random-norm discretization/probability errors, and verify the implemented adaptive success/error bound. The source's continuous norm guesses do not magically become exact finite classical arithmetic. Those limits do not prevent returning a useful numerical T-cost model.

## Task-02 reconciliation and exclusions

Task 02 now exists; the earlier missing-task text is superseded. `t-count-application-input.json` is generated from its actual m=127, β=9 example. For B=h²A and D-dimensional positive padding 4C I, the exact analytic Frobenius norm obeys

    αF² = (18m−2) Σ_(i=1)^m (1+βih)²
          +2m Σ_(i=1)^(m−1) (1+β(i+1/2)h)²
          +(D−m²)(4C)².

The reproduction uses closed sums of first and second powers, no matrix construction. Set K=αF/(h²λ₀). The separate reported κ upper bound 8C/(h²λ₀) is not overwritten by K. The task-02 sparse α=20C is **not** the normalization of this stored-data circuit. All comparison tables identify the Frobenius normalization instead.

For illustration we map task 02's phase-aligned vector allowance to a trace-distance design target by dividing by √2. This is only a budget proxy: an arbitrary global phase is unobservable in a standalone state, whereas task 02's signed overlap requires a coherent phase reference. The generated T number is not the cost of delivering the continuum scalar. Matrix/RHS representation, physical norm recovery, signed-overlap circuits, estimator repetitions, and their error budgets still require task 05. Classical table construction, data storage, QSVT phase generation, QEC and physical time/energy are separate stages. Nothing in this estimator establishes advantage for the known-answer manufactured workload.

Reproduce with `python3 reproduce_t_count.py`. It writes two default examples, an Eq118 sensitivity sweep, independent formula/circuit checks, schema stage fragments, a tested-environment/source manifest and numerical outputs. It changes no shared estimator or Q# source.

## Task-01 export assumptions and handoff

The two `t-count-*-stage.json` files are alternative examples of the same `q.core` stage, not additive stages. `queries_expanded=true` indicates A/b T costs are included; Clifford counts remain explicitly unknown, so no QEC-ready inference is permitted. Expected resource semantics are retained even when the query expression bounds that expectation. Import these assumption IDs with either fragment:

| ID | Status and requirement |
|---|---|
| A04T-access | Conditional: real, nonsingular positively padded input; stored-data Frobenius construction and certified inverse-gap input; classical tables constructed and charged separately |
| A04T-query | Established under ideal-access promises: Algorithm 3 Eq118, or its Eq19 simplification only in range; includes internal retries |
| A04T-controls | Derived resource envelope: data-gated controlled preparations, doubled identity augmentation, clean-ancilla ladders, explicit projector/endpoint allowances |
| A04T-synthesis | Assumed: chosen finite R model or supplied certificate; phase generation, finite norm guesses and implemented success still require validation |

Delivered: callable f, complete non-null T-cost breakdown, task-02 matrix instantiation, source/version capture and validation. Reviewer coverage remains C1-1 and the access-accounting portion of C1-2. Scientific scalar delivery, QEC scheduling and crossover claims remain downstream work. The old query-only fragments must not also be summed after importing this expanded core.
