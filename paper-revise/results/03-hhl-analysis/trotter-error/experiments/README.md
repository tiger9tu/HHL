# Actual Trotter errors versus deterministic bounds

The standalone report is `../../Trotter-error-estimation.pdf`. All matrix errors use the principal logarithm of ONE microstep, not the principal logarithm of the entire time evolution.

## Protocol

- 850 matrix cases, 24 settings per case; deterministic seed 20260909 + case ID.
- Synthetic fixed-band, random-matching, and shifted positive-definite families: N = 8,16,32,64,128,256,512 with 2,4,8 matching terms. Each cell has 16 samples through N=128, 8 at N=256, 4 at N=512. Additionally each family has two N=1024 samples with four matching terms. The largest-size samples are exploratory, not an asymptotic fit.
- Fixed-band terms pair consecutive vertices after cyclic shifts, so supports repeat; random-matching terms use independent permutations. Edge weights are uniform on [-1,1]. SPD cases add (norm of off-diagonal sum + 0.25) times the identity.
- Five 2D Dirichlet Poisson stencils: q=3,7,15,23,31 interior vertices per side, N=q^2. Decomposition: 4I and four parity matchings. Grid spacing factor cancels on normalization.
- Controls: four commuting diagonal cases; six cancelling decompositions [aZ,aX,-aZ,-aX,I], a=1,4; one Pauli [Z,X] case. All cases normalize the SUM to spectral norm one, including the Pauli case (unlike the earlier unnormalized illustrative table in the report).
- Fixed-time sweep: tau=0.1,1,4 and r=1,2,4,8,16,32. Normalized-microstep sweep: hB=0.025,0.1,0.25,0.5,0.75,1.25 with tau=h and r=1.
- Operator bound: min(2,tau^2 C/(2r)). Effective-H bound: h C/[2(1-hB)] and coarser h C, compared ONLY for hB<=1/2 (1e-14 boundary tolerance).
- All norms are full spectral norms, not random-vector lower bounds. One-sparse exponentials use exact 2x2 formulas. Exact evolution uses a Hermitian eigendecomposition. Operator errors use a Gram eigensolver, with a full SVD fallback for a LAPACK convergence failure. Commutator norms use Hermitian eigendecompositions of i[A,B].
- Effective H uses the Hermitian Cayley transform followed by eigenvalue phases 2 arctan(k). Unitarity, reconstruction, branch gap and independent scipy.logm/SVD/expm comparisons are retained. The comparison tolerance is 5e-10 absolute; commuting zero-bound cases are reported separately as roundoff, not assigned error/bound ratios.
- Pointwise bootstrap intervals in summary.csv resample matrices, 2000 times (seed 20261909). Plot bands are the empirical 5th--95th percentiles, NOT confidence bands. Repeated settings of a matrix are correlated; pooled ratio percentiles describe this sweep, not a probability law. The ratio histogram uses one setting per matrix.
- Null kappa indicates a zero eigenvalue returned numerically; singular/indefinite synthetic matrices are valid simulation tests but are not asserted to be valid SPD HHL inputs.

## Execution and reproduction

The full study uses Slurm CPU compute nodes, complex128 arithmetic, 32 worker processes and two BLAS threads per worker. A small initial N=8 smoke check ran locally. Initial Slurm job 58122970 completed 845 cases; with the smoke check, 846 were available. Four failures were implementation/library issues, not error-bound violations: three highly degenerate cancelling cases triggered a LAPACK subset-eigensolver internal error; one singular synthetic case could not serialize infinite kappa as strict JSON. Job 58123095 resumes the four missing cases using an SVD fallback and null for singular kappa. The original source, failure records and both execution manifests are preserved. Existing completed results were not changed by these fixes.

```bash
# With numpy/scipy installed in the shared .venv (see run.slurm):
sbatch paper-revise/results/03-hhl-analysis/trotter-error/experiments/run.slurm
# After every case finishes; needs numpy, matplotlib:
python paper-revise/results/03-hhl-analysis/trotter-error/experiments/analyze_results.py
```

`configurations.json` specifies every matrix and seed. `shards/` retains per-case outputs. `errors.csv` contains every measured error, both coefficients, bounds, applicability flags and numerical diagnostics. `matrix-cases.csv` has matrix metadata; `independent-validation.csv` has cross-algorithm checks; `summary.csv` has grouped statistics; `results.json` has aggregate validation. Figures are available as PDF and PNG in `figures/`. `global-log-diagnostic.csv` gives a separate exact diagonal branch-wrapping demonstration; it is not included in the 20,400 measurements.

The tests validate this implementation on the sampled families; the derivations establish the deterministic bounds. They do not prove a universal empirical scaling in N or HHL success probability.

## Completed results

All 850 cases finished (20,400 measurements). There were zero operator-bound violations and zero violations among the 13,194 effective-H comparisons satisfying hB <= 1/2, at absolute tolerance 5e-10. Median actual/bound ratios excluding zero bounds: 0.41559 operator, 0.38309 refined effective H, 0.21810 coarse effective H. The largest corresponding ratios were 0.99999946, 0.99686747 and 0.50345923. The second Slurm job completed successfully; initial partial failures remain documented for provenance.

`write_findings.py` creates the report findings and additional conditioning/convergence checks from the CSV. Run it after `analyze_results.py` when updating the PDF. The complete report can be rebuilt with `../build.sh`. Dependencies used: NumPy 1.19.5, SciPy 1.5.4, Matplotlib 3.3.4 (Python 3.6.15) for experiments/analysis; Tectonic 0.17.0 and PyMuPDF 1.28.2 in a separate modern Python environment for the PDF. The shared virtual environment is excluded from the reproducibility archive.
