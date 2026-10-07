# Proposed manuscript replacements — application-calibrated Trotter error

Current direction (9 September 2026): use application-specific numerical Trotter errors for practical resource estimates. This supersedes the earlier proposal to use a universal sufficient Trotter bound as the central step-selection rule. The previous draft is preserved in `practical-trotter/manuscript-text-bound-based.md`. The deterministic proofs and completed numerical comparison remain useful validation references.

The complete proposed section and notation details are in [practical-trotter/method-section.tex](practical-trotter/method-section.tex), rendered in [Trotter-error-practical-method.pdf](Trotter-error-practical-method.pdf).

## Main-text replacement: effective-H error

Let H=A/α=ΣₐHₐ be the normalized Hermitian input matrix with a specified decomposition and ordering. For a first-order microstep P₁(h)=exp(ihH₁)⋯exp(ihH_L), h=τ/r, define Ĥ(h)=Log(P₁(h))/(ih) on the logarithm branch continuous from h=0. The BCH expansion gives

\[
\Delta H(h)=\widehat H(h)-H
=\frac{ih}{2}\sum_{a<b}[H_a,H_b]
+h^2\mathcal K_2+h^3\mathcal K_3+\cdots,
\qquad \epsilon_H(h)=\|\Delta H(h)\|_2.
\]

Each coefficient K_q is a weighted sum of nested commutators containing q+1 fragments. Its coefficients depend on the product formula and ordering. This shorthand retains the higher-order structure without listing every term; compact BCH representations and their computational evaluation are developed by [Maxwell et al., Section III.2](https://arxiv.org/html/2606.30738v1).

The leading error depends on the norm of the sum of commutators. Bounding their norms separately discards cancellations, and replacing these by term-norm estimates discards further structure. Thus simple expressions in dimension, sparsity and maximum term norm need not tightly predict the error for a particular application. The size of this effect depends on the matrix, decomposition, ordering and step size. This does not assert that simple tight bounds are impossible: the Poisson instances in our numerical study provide a nearly tight structured example.

For practical resource estimation, we therefore select the Trotter step count from numerical studies of the specified application. We evaluate effective-H errors directly on tractable instances and use successively higher BCH orders, checked against direct calculations and step refinement, where direct evaluation becomes costly. We report the tested sizes, normalization, decomposition, ordering, error curves and numerical uncertainty. Extrapolation beyond the tested range is explicitly a modeling assumption; small generic matrices do not establish a dimension-independent error coefficient.

Software can evaluate both BCH error estimates and established bounds. PennyLane's [bch_expansion](https://docs.pennylane.ai/en/stable/code/api/api/pennylane.labs.trotter_error.bch_expansion.html) and [effective_hamiltonian](https://docs.pennylane.ai/en/stable/code/api/api/pennylane.labs.trotter_error.effective_hamiltonian.html) support the former; [TrotterProduct.error](https://docs.pennylane.ai/en/stable/code/api/pennylane.TrotterProduct.html) evaluates evolution-operator error bounds. A truncated BCH result is an estimate of effective-H error unless the omitted terms and numerical error are also controlled. Software-computed bounds can be supplementary checks for the application experiments.

## Appendix replacement and resource accounting

Use `practical-trotter/method-section.tex`, Section 2, for the general nested-commutator shorthand, sign convention, expansion order, logarithm branch and shared-microstep requirement. For an order-p formula, ΔH_p(h)=h^p K_p+O(h^(p+1)); a symmetric formula has an O(h^(p+2)) remainder. These are local fixed-instance expansions, not uniform-in-N bounds.

Use an empirically selected base repetition r₀ and shared microstep h=τ₀/r₀ for QPE powers τⱼ=2ʲτ₀, rⱼ=2ʲr₀. A first-order forward/inverse QPE pair then uses K_HS1=2Lr₀(2^m−1) elementary evolutions. Additional QPE repetitions, preparation, filtering, retries, access, synthesis and readout retain their own costs and error budgets. Higher-order formulas require revised stage counts. L is the actual decomposition term count and is not assumed equal to sparsity s.

A measured coefficient a_app in ε_H(h)≈a_app h^p guides initial step selection, r₀≈τ₀(a_app/ε_H,target)^(1/p). Verify the selected integer step count. The effective-H target must be related to the actual application output with the RHS, conditioning and remaining HHL errors included. This replaces the original numerical prefactor in Proposition 1; it does not justify a new universal asymptotic HHL claim.

## Figures and evidence already available

The completed [Trotter-error-estimation.pdf](Trotter-error-estimation.pdf) reports 850 matrices and 20,400 operator/effective-H measurements, with raw data in `trotter-error/experiments/`. It remains a bound-comparison study. Its five Poisson matrices are application-motivated operator tests; the random ensembles are supplementary implementation and sensitivity tests. No matched end-to-end application-output calibration is claimed from these data alone. Reuse its existing captions only for the datasets they actually describe.

For the revised application figures, report measured ε_H against step count and instance size; include the specified application generator, matrix normalization, decomposition order, RHS/output when relevant, tested sizes, numerical method, seeds/sample counts if random, convergence checks, and uncertainty. Bounds may appear as secondary reference curves. Do not relabel generic random samples as application instances or extrapolate a histogram edge into a probability guarantee.

## Dependent claims and handoff

Proposed abstract/results wording:

“We demonstrate the resource-estimation framework using application-specific numerical calibration of Trotter errors and explicit algorithm, input/output and hardware assumptions. Reported step counts apply to the studied instances and accuracy targets; extrapolated resource estimates are accompanied by their modeling assumptions and sensitivity analysis.”

Integrate this wording when the application calibration is complete. Existing old crossover locations, exact prefactors and asymptotic claims are not validated by changing the error-estimation strategy. The current contribution addresses reviewer C1-5's unsupported numerical-to-asymptotic inference and supports C1-6/C2-3's application-specific framing. Task 02's benchmark/output handoff is still absent; implementing that application and calibrating its output error are separate follow-on work. This edit delivers the requested BCH-based methodology, not new application results.
