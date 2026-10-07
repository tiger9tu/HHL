# QETU linear solver: logical scaling and Trotter-cost adapter

Task 13, 9 September 2026. This is an additional solver branch, not a replacement for task 04. The main result below is a derivation for a direct inverse filter. It does not claim the optimal QLSA success-amplification scaling or a demonstrated smaller gate prefactor.

## Result

Let the dimensionless Hermitian operator be H=A/α_HE, with spectrum in [1/K,1], K=α_HE/λ_min(A), and a specified decomposition H=Σ H_a. K is an inverse-gap bound; it equals κ₂ only with tight norm normalization. Suppose the project's application-specific microstep study establishes

    ||H_hat(h)−H|| = a_app h^p + controlled remainder,
    P_p(h) = exp(i h H_hat(h)).

Write g_step,p for the compiled logical cost of one *controlled* order-p microstep. A QETU inverse filter of degree d=O(K log(K/ε_x)) exists, with success amplitude σ=Θ(||H⁻¹ b_normalized||/K). The derivation below respects the even-polynomial restriction of the cited QETU theorem. With a common microstep and exact adjoints, selecting the matrix-error allowance O(ε_x/K) gives

    r = O(max{r_branch, τ(a_app K/ε_x)^(1/p)}),
    G_attempt = d r g_step,p + O(d) rotations + input/endpoint work.

For constant τ and suppressing logarithms, the evolution contribution is

| Delivery policy | Expected/scaling work for evolution, in logical gates |
|---|---|
| One heralded attempt | Õ(g_step,p K max{r_branch,(a_app K/ε_x)^(1/p)}) |
| Repeat until success | Above divided by σ²; worst case Õ(g_step,p K³ max{r_branch,(a_app K/ε_x)^(1/p)}) |
| Coherent amplitude amplification | Above divided by σ; worst case Õ(g_step,p K² max{r_branch,(a_app K/ε_x)^(1/p)}) |

Here r_branch≥1 enforces the validated local-logarithm/expansion range. For the project's sufficient first-order condition, r_branch=max{1,ceil(2τB_sum)}. This additional dependence matters for decompositions with large cancelling terms; it cannot be discarded solely because the fitted leading coefficient is small. The simplified powers below assume the accuracy-dependent term dominates this branch requirement.

Thus first-order Trotterization gives worst-case amplified evolution work Õ(g_step,1 a_app K³/ε_x) in that regime; order two gives Õ(g_step,2 sqrt(a_app) K^(5/2)/sqrt(ε_x)). Without amplification the respective exponents of K are four and 7/2. Preparation, reflections and final scalar estimation are additional. These are sufficient upper scalings, not lower bounds. If σ=Θ(1), the attempt scaling already describes delivered-state scaling up to retry/confidence factors. Higher-order a_app and stage costs must be recalibrated, not copied from first order.

For a Pauli decomposition of L terms of weight at most w, a serial implementation has g_step,1=O(L[w+log(1/ν)]) after rotation synthesis at per-rotation operator tolerance ν. Keep L, weights and coefficient-computation cost explicit: sparsity s does not imply L=s or L=poly(log N). A generic Pauli expansion can have N² terms. No SELECT/PREPARE encoding of A is required, but controlled time evolution still has a cost.

## Sources and what is established

[Dong, Lin and Tong, PRX Quantum 3, 040305 (2022), arXiv:2204.05955v2](https://arxiv.org/abs/2204.05955v2), Theorem 1, supplies a one-ancilla even-polynomial transformation F(cos(Θ/2)) with d controlled forward/adjoint evolution calls and d+1 ancilla rotations. Its Appendix C gives the generic Trotter telescoping analysis. Its application is ground-state preparation/energy estimation; its ground-state overlap is **not** QLSA success probability. The special control-free implementation requires anticommutation structure and is not assumed here.

[Gilyén, Su, Low and Wiebe, arXiv:1806.01838v1](https://arxiv.org/abs/1806.01838v1), Section 3.7, Lemma 40 and Theorem 41, supplies bounded reciprocal polynomials of degree O(g⁻¹ log(1/η)). We use this polynomial result, not its block-encoding circuit. The finite constructive variant below uses Lemma 40 directly with conservative normalization. Neither source claims the complete QETU-QLSA resource formula above; the composition, inverse perturbation and resource accounting here are our derivation. The targeted search did not identify a verified ready-made constant-factor QETU-QLSA model suitable for direct import; it is not an exhaustive absence claim.

The local source of Trotter estimates is task **03**, despite the prompt naming a task-02 subtask:

* `../03-hhl-analysis/practical-trotter/method-section.tex`: the current application-specific effective-H/BCH methodology, positive-time convention, and warning that a fitted leading coefficient is not a certified full-error bound.
* `../03-hhl-analysis/trotter-error/trotter-error-estimation.tex`: rigorous first-order bounds E_U≤τ² C_comm/(2r), E_H≤h C_comm/[2(1−h B_sum)] for h B_sum≤1/2, where B_sum=Σ||H_a|| and C_comm=Σ_(a<b)||[H_a,H_b]||.
* `../03-hhl-analysis/trotter-error/experiments/errors.csv`: existing measured effective-H errors, including five Poisson controls. We reuse these values and the original generator; we do not regenerate the 850-matrix study or infer a universal random-matrix coefficient.

## A valid inverse polynomial for native QETU

An unshifted even F(cos(τH/2)) cannot distinguish λ and −λ. Nor is F(x)=1/x the desired inverse of H: the spectral variable is a cosine. We explicitly fix both problems.

Take τ=1/2 and Θ=πI/2+τH. For an effective-H error Δ≤1/(4K), its eigenvalues lie in [1/(2K),5/4], a conservative enlarged interval. The controlled signal exp(−iΘ) uses a phase on its control for the identity shift and the adjoint of the project's positive-time simulation. Set

    x=cos(Θ/2), v=1−2x²=sin(τ H_hat),
    g=sin(τ/(2K)), a=sin(5τ/4)<1.

On the enlarged spectrum g≤v≤a and arcsin(v)=τλ exactly. Let R(v) be an odd polynomial bounded by one throughout [−1,1], approximating g/(2v) to η_R on |v|≥g. The reciprocal theorem gives deg R=O(g⁻¹ log(1/η_R)). Define q(v)=v/arcsin(v), continuously q(0)=1, and truncate its even Taylor series to degree 2J:

    q_J(v)=1−Σ_(j=1)^J a_j v^(2j),  a_j≥0,
    2/π≤q_J(v)≤1 on [−1,1],
    |q_J(v)−q(v)|≤a^(2J+2) on |v|≤a.

For completeness, positivity follows from q(v)=∫₀¹ cos(s arcsin v) ds. The hypergeometric expansion of the integrand has coefficients (-s/2)_j(s/2)_j/[(1/2)_j j!], negative for every j≥1 and 0<s<1. Thus Σa_j=1−2/π. The tail estimate follows by factoring out a^(2J+2). This is also checked numerically by the validation script.

The single polynomial

    F(x)=R(1−2x²) q_J(1−2x²)

is even, globally bounded by one, and approximates c/λ with c=g/(2τ)=Θ(1/K), error at most η_R+a^(2J+2)/2. Choose J=O(log(1/η)) and η_R≤η/2, a^(2J+2)≤η. Its degree is d=2(deg R+2J)=O(K log(K/ε_x)) for η=O(ε_x/K). This establishes the announced degree without assuming a numerically optimized reciprocal-of-cosine fit. The two polynomial factors are composed **classically into one phase sequence**, not executed as two separately postselected filters.

The same shifted construction can cover Hermitian indefinite inputs with |λ|≥1/K, using both signed intervals and inverse singular gap. Task-02 instantiation and numerical checks here are SPD. General non-Hermitian inputs require a costed Hermitian dilation, updated dimension/decomposition and recovery contract; this report does not claim those costs.

## Error and success accounting

Let ||b_normalized||=1, y=H⁻¹b_normalized, Δ=||H_hat−H|| and KΔ<1. The resolvent identity gives

    ||H_hat⁻¹b_normalized−y||/||y|| ≤ KΔ/(1−KΔ).

Normalizing nonzero vectors gives a phase-aligned vector-error bound

    ε_matrix ≤ 2KΔ/(1−KΔ).

Therefore Δ_target=ε_matrix/[K(2+ε_matrix)] suffices. No factor d occurs: the entire exact-arithmetic QETU circuit transforms **one fixed H_hat**. This argument requires identical microsteps on every query, an appropriate logarithm branch, a polynomial accurate on the enlarged spectrum, and inverse calls implemented by exact circuit adjoints. Reversing time without reversing a nonsymmetric term ordering is not the adjoint. Per-query adaptive formulas or inconsistent synthesized gates cannot silently use this argument.

For the ideal inverse filter of H_hat, σ_hat=c||H_hat⁻¹b_normalized||≥c/(1+Δ). If the implemented good block differs from cH_hat⁻¹ by η+ζ (polynomial error plus circuit operator error), then

    p_min = (σ_lower−η−ζ)²,   provided η+ζ<σ_lower,
    ε_filter+implementation ≤ 2(η+ζ)/σ_lower.

The latter follows by normalizing relative to the exact good vector; a more conservative denominator σ_lower−η−ζ is also valid. We use that conservative form in the runnable model. This is why an internal operator error cannot simply be set equal to ε_x. Polynomial precision must normally be O(ε_x/K). Total state error adds the matrix and conditional filter allowances. Failure probabilities are separate.

Independent retries have expected attempts ≤1/p_min and a cap R=ceil(log δ_retry/log(1−p_min)); capped work is R times one attempted circuit, not an expectation. Coherent amplification costs O(1/sqrt(p_min)) calls to the complete preparation/filter and their adjoints, plus reflections. Unknown success needs a justified adaptive or fixed-point policy and confidence factors. We provide this scaling, not a fabricated finite amplification schedule. Generic logical-gate synthesis errors should telescope across the **full amplified circuit** when amplification is used. The structured matrix perturbation bound need not be multiplied by the amplification length, since ideal amplification preserves its good-state direction.

### Reuse of the project's step-selection results

For first order the project's refined bound gives the explicit sufficient integer

    r_bound = max{1, ceil(2τ B_sum),
                   ceil(τ B_sum + τ C_comm/(2Δ_target))}.

It enforces the branch condition and E_H≤Δ_target, including C_comm=0. For a practical numerical curve, select a tested h with E_H(h), numerical uncertainty and a checked branch satisfying the target, then enforce τ/h integer. A smaller untested h is not automatically certified merely because an empirical curve looked monotone. If only a fitted a_app is used, report r≈τ(a_app/Δ_target)^(1/p) as an extrapolation and validate the chosen integer step. Norm rescaling changes E_H, B_sum and C_comm; under H→sH the leading order-p coefficient changes by s^(p+1).

For independently approximated queries, an alternative always-available analysis is ζ_U≤d E_U(τ,r). The project's first-order bound then gives r≥d τ² C_comm/(2ζ_U,target). For E_U≤C_U τ^(p+1)/r^p, r=O((C_U τ^(p+1)d K/ε_x)^(1/p)) for one attempt. With d=Õ(K), worst-case amplified evolution work is Õ(g_step,p C_U^(1/p) K^(2+2/p) ε_x^(−1/p)), **before** any extra tightening for a generic error bound over the amplified circuit. Do not add this Trotter contribution to the effective-H contribution: they are alternative analyses of the same approximation.

## Finite reproducible model and evidence

`logical_model.py` implements a conservative finite polynomial construction, not the optimized Theorem-41 window polynomial. In Lemma 40 write e=ε_filter/32, k=1/g,

    b=ceil(k² log(k/e)), j_max=min(b−1,ceil(sqrt(b log(4b/e)))),
    G(v)=4Σ_(j=0)^j_max (−1)^j Pr[Binomial(2b,1/2)>b+j] T_(2j+1)(v),
    S=sqrt(b)+e, R(v)=G(v)/S.

Since f(v)=[1−(1−v²)^b]/v satisfies |f|≤min(b|v|,1/|v|)≤sqrt(b), and ||G−f||≤e, this R is globally bounded. It approximates 1/(Sv) with error 2e/S on the spectral interval. Choose J with a^(2J+2)≤eg. Then F=R q_J has η≤3e/S and inverse scale c=1/(τS). The finite scale incurs an extra sqrt(log) success overhead relative to the existence construction, which is retained in every finite result and suppressed only in Õ notation. These constants are reproducible sufficient choices, not practical optimal prefactors. No classical phase list is synthesized; finite macro counts are conditional on implementing the certified polynomial to the allocated tolerance.

`reproduce.py` imports the five existing Poisson cases, writes `reused-poisson-costs.csv`, and records both a certified bound-based r and any eligible *already measured* r. If no measured step meets the target it writes null, not an extrapolated measurement. `validate.py` checks the actual polynomial on dense grids, the conservative global/tail bounds, and the effect of the original microstep implementation on inverse states of the two smallest Poisson controls. Finite precision checks are diagnostics, not interval certificates; analytic inequalities are the certificates. Large cases use imported measurements without new dense diagonalizations.

## Gate, space and downstream interface

For each exclusive compiled gate bucket g and a serial schedule,

    G_attempt,g = d r G_step,g + (d+1)G_phase,g
                  + d G_shift,g + G_endpoint,g.

Use depth and T-depth versions only with an explicit compiled step schedule. In the chosen π/2 shift G_shift is a Clifford phase on the control, but it must remain present for correct relative phases. One attempt has d/2 forward and d/2 adjoint calls, drM_p controlled fragment exponentials, d+1 phase rotations, n=ceil(log₂ D) system qubits and one QETU signal ancilla. Add live arithmetic, fragment workspace and retained input memory. These macro counts do not certify a total T count or T-depth.

For a nonidentity weight-w Pauli term, parity computation/uncomputation costs 2(w−1) CNOTs and basis changes; a controlled Rz can use two arbitrary Rz rotations and two CNOTs, giving 2w CNOTs per controlled term plus basis changes. Controlled identity phases, angle calculation and connectivity routing are separate. Synthesizing R rotations to total operator allowance ζ gives a sufficient per-rotation tolerance ζ/R and logarithmic T overhead; a chosen compiler must supply constants. One-sparse matching evolutions in the existing Poisson study are **not automatically weight-w Pauli rotations**. Their reversible index/value arithmetic must be compiled separately.

Task-01 interface version 1.0.0 remains unchanged. Model-specific parameters are K_HE, α_HE, τ, p, B_sum, C_comm/a_app, polynomial d,c, r, η, ζ and σ_lower. Counts emitted here are diagnostic `query`, `gate`-macro and `logical_qubit` quantities; they are not a fabricated schema-complete physical resource record. Unknown compiled quantities stay null. Task 05 owns preparation, retry/amplification policy, norm recovery, signed overlap and readout multiplicities; it must apply success overhead once. Tasks 06–07 must wait for compiled primitive counts, synthesis budgets and schedules before producing physical time/energy.

## Task-02 application and comparison with task 04

The current task-02 handoff exists: `02-smooth-diffusion-v1`, m=127, N=16129, β=9, output continuum mean temperature with ε_out=10⁻⁴. Older task-03/04 text saying it is absent is stale. Set H=(h_grid² A padded)/(8C), C=1+β, with the task-02 positive-identity padding. Then

    α_HE=8C/h_grid², K_HE=8C/(h_grid² λ₀).

Task 04's generic sparse encoding scenario has K_BE=20C/(h_grid²λ₀), hence K_BE/K_HE=2.5 for these **normalization scenarios**, not a measured gate advantage. A tighter block encoding could change this ratio. At fixed contrast, K_HE=Θ(N) and s=5. If the normalized microstep cost and a_app stay bounded up to polylog factors, the amplified first-order branch scales Õ(N³/ε_x), not Õ(log³N/ε_x); those microstep assumptions require application evidence.

Task 02 requires ε_x≤ε_out/(4||c_output||X_max), X_max=||b||/λ₀ or its certified upper bound. Its supplied F_bound permits X_max≤sqrt(N)F_bound/λ₀. Split this state allowance among Trotter, filtering and synthesis. ε_x is not ε_out, and a phase-aligned normalized state does not supply the unnormalized scalar. `application-input.json` records this conversion and flags the missing variable-conductivity Trotter calibration. Existing Poisson data have β=0, m≤31, norm-one normalization and a specified five-fragment ordering. They are controls, not measurements of β=9, m=127. The task-02 diagonal plus four edge-matchings offers a candidate five-fragment decomposition, but its coefficients, controlled costs and E_H curve need their own calibration.

To assess a small prefactor, compare the same delivered-output contract: QETU's cost per successful inverse state against task 04's complete delivered-state expected query bound Q_BE times compiled g_BE, including both branches' b calls and output work. A useful conditional inequality is M_success d r g_step < Q_BE g_BE after matching the omitted terms. There is currently no compiled g_BE or g_step for the common application, so no numeric crossover or established prefactor advantage follows. In commuting/exactly simulable cases Trotter approximation vanishes and QETU can be particularly attractive; direct inversion still carries its success overhead. Eliminating a SELECT/PREPARE implementation does not itself make a direct inverse filter an optimal QLSA.

## Handoff and limitations

Deliverables: this derivation, runnable finite macro model, imported-data table, small numerical checks, source hashes, references, and manuscript text. Reviewer coverage: C1-1 (additional modern algorithm branch), C1-2 (explicit success/I/O boundary), C1-5 and C1-6 (application-specific calibrated Trotter inputs and conditioning), C2-1/C2-3 (framework/application distinction). Other review comments remain outside task 13.

Required for a publishable finite end-to-end comparison: a task-02-matched microstep error curve and decomposition costs; generated/certified QETU phases and logical compilation; a concrete task-05 scalar-output and amplification implementation; task-04 costs reconciled to the same application. The requested logical scaling is determined here; those missing inputs limit finite prefactor and physical-advantage claims, not the conditional scaling derivation. No shared Q# implementation or existing result is modified. Inspection found the legacy second-order Q# coefficient builder appends `halves` without reversing it; this is not a valid generic Strang ordering. Task 12 should audit it before using that implementation as evidence for p=2. Our imported numerical evidence is first order and does not rely on that builder.
