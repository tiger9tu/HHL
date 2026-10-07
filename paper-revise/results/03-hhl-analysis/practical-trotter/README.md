# Practical Trotter methodology — current manuscript direction

Deliverable: [Trotter-error-practical-method.pdf](../Trotter-error-practical-method.pdf), three pages. `method-section.tex` is the proposed section; `../manuscript-text.md` supplies the current manuscript/handoff language. The previous bound-based draft is archived here as `manuscript-text-bound-based.md`.

This update follows the user's request to make application-specific numerical Trotter estimation central to practical resource estimation. It supplies the BCH shorthand, first-order sign derivation, higher-order convention, application-dependence argument, verified software references and common-microstep resource-count interface. It adds no new application experiment or end-to-end resource estimate. The completed 850-matrix study and earlier bound proofs remain unchanged.

Technical distinctions retained:

- For exp(+i h H1)...exp(+i h HL), the leading effective-H correction is +(i h/2) sum_[a<b] [Ha,Hb]. BCH commutator degree q+1 gives effective-H power h^q.
- A local logarithm branch and the same microstep across QPE powers are required for a common effective matrix.
- A BCH truncation is an estimate without omitted-term/numerical-error control. PennyLane's TrotterProduct.error concerns the evolution-operator norm, not directly the effective-H norm. Its BCH APIs generate/evaluate effective-H approximations. These API references were verified, but PennyLane was not installed or run for this text update.
- A general impossibility claim about simple tight bounds is not made: the existing Poisson data are nearly tight. Nor is the cited paper's asymptotic diagonal-error result substituted for HHL's full matrix perturbation, which can change eigenvectors and inverse states.
- Numerical calibration is conditional on the application and tested range. Task 02's application/RHS/output handoff remains absent. A common output target and complete HHL validation are still needed before publishing new end-to-end application resource estimates.

Reviewer coverage: C1-5 (remove unsupported small-matrix-to-universal scaling), C1-6 and C2-3 (application dependence), C2-1 (framework with empirical resource-model inputs). This is the requested methodology component, not closure of every reviewer comment.

Primary references verified 9 September 2026:

1. Maxwell et al., arXiv:2606.30738v1, Section III.2, especially Eqs. 9–18: https://arxiv.org/html/2606.30738v1
2. PennyLane BCH: https://docs.pennylane.ai/en/stable/code/api/api/pennylane.labs.trotter_error.bch_expansion.html
3. Effective Hamiltonian: https://docs.pennylane.ai/en/stable/code/api/api/pennylane.labs.trotter_error.effective_hamiltonian.html
4. Evolution-error bounds: https://docs.pennylane.ai/en/stable/code/api/pennylane.TrotterProduct.html

Source/code inspection: supplied reviewer PDFs, manuscript Proposition 1 and Appendix B, `num/trotter.m`, `num/epsA.m`, `src/HHL/HHL.qs`, task-03 prior reports and resource contract. The legacy `epsA.m` takes the long-time principal logarithm; the proposed procedure explicitly uses the microstep instead. No shared implementation was modified.

Validation: `check_bch.py` independently checks the positive-time sign against dense matrix exponentials/logarithms on three complex Hermitian 4x4 fragments. The residual after the first-order effective-H term converges quadratically (orders 2.0043, 2.0021, 2.0010). This is a formula sanity check, not an application experiment. `pdf-validation.json` records source/PDF hashes and layout checks.

Rebuild:

```bash
HHL_NUMERICS_PYTHON=/tmp/hhl-task03-venv/bin/python \
HHL_PDF_PYTHON=/tmp/hhl-task03-pdf/bin/python \
HHL_TECTONIC=/tmp/hhl-pdf-tools/tectonic \
bash paper-revise/results/03-hhl-analysis/practical-trotter/build.sh
```

Portable requirements: NumPy/SciPy for the check, Tectonic for TeX, and PyMuPDF in a compatible Python environment for PDF validation. No Slurm job is necessary for this small check or document build. Recorded versions: Python 3.6.15 / NumPy 1.19.5 / SciPy 1.5.4; Tectonic 0.17.0; PyMuPDF 1.28.2 in the separate PDF environment.
