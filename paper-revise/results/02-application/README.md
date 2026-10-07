# Task 02 handoff

Delivered **02-smooth-diffusion-v1**, using task 01 interface v1.0.0. This is a fully specified, manufactured steady-diffusion verification problem with a continuum mean-temperature output. It supports matched solver-pipeline evaluation, **not an unrestricted application advantage claim**, since its analytic answer is known. This limitation is material to how the manuscript may use it.

- [Specification, proofs, error/failure allocations, access status and preconditioners](specification.md).
- [108-row parameter table](parameters.csv), with mesh admissibility and sufficient representation precision.
- [Small reproducible generator](generate.py), [default metadata](instance.json), and [default arrays](instance.npz). NPZ contains CSR `data,indices,indptr`, row indices for NumPy matvec, b,c and sampled analytic U; U is not the exact discrete solution.
- [Task-01-compatible problem fragment](benchmark-pp.json). Original κ is unknown with derived bounds in `parameters`, never mislabeled as an exact value. This fragment does not pretend to be a complete resource record.
- [Proposed manuscript text](manuscript-text.md), [validation results](validation.json), [input hashes](input-manifest.json), and page-marked extracts of both reviews and relevant manuscript pages in `source-extracts/`.

Default: m=127, N=16,129, β=9, s=5, ε_out=10⁻⁴, δ_total=.01. The mesh-error bound is 8.30×10⁻⁶, below its 2.5×10⁻⁵ allowance. m=63 fails that conservative quarter-budget at the same β and ε, although its observed error can be smaller; acceptance uses the certificate. The original κ interval is approximately [664, 66,395]. No hardware runtime, energy or crossover was measured.

## Reproduction

From repository root, with Python, NumPy and jsonschema installed:

```sh
python3 paper-revise/results/02-application/reproduce.py
python3 paper-revise/results/02-application/generate.py --m 31 --beta 1 --epsilon 0.0001 --out /tmp/hhl-diffusion-small
python3 paper-revise/results/02-application/generate.py --m 16383 --metadata-only --out /tmp/hhl-diffusion-large
```

The main command runs 24 solves (m=3,7,15,31,63,127; β=0,1,9,99), checks analytic truncation and quadrature identities, continuum error against the derived bound, direct-solve agreement and spectra on tiny matrices, the symmetric Poisson-preconditioner bound, rounded-system scalar error, positive-identity padding, and three invalid-input cases. It regenerates the default NPZ/metadata, CSV, and validates the `pp` fragment against task 01's actual schema. FP64 diagnostics passed; they do not constitute interval certification or performance benchmarks. Exact formulas supply the mathematical certificate. The scripts are NumPy-only except for jsonschema in the reproduction wrapper, and pin single-thread BLAS for diagnostics. Recorded package versions are in the manifest. NPZ compression container timestamps may differ; reproducibility means equal arrays and metadata, not ZIP byte identity.

Both actual reviewer PDFs were extracted and read (3 and 5 pages), and relevant manuscript pages 1–3,5–6,17–18,24–26 inspected against task 01's extracts. Local extraction used pypdf 3.17.4 available under `/tmp/hhl-framework-pypdf-3`; extraction is not required to run the benchmark. Primary references were checked via their publisher/author documentation on 2026-09-09; links and support scope are in the specification and proposed text. The author-hosted Chen finite-difference notes were searched but full retrieval failed, so no technical claim depends on them. The stencil-specific formulas are derived here, not attributed to an unchecked reference.

Existing code inspected: `num/genSparse.m` generates shuffled random symmetric matrices without an SPD guarantee; `src/HHL/HHL.qs` prepares states without this scalar-output contract; its `Oracle.qs` scans supplied dense arrays rather than implementing the analytic stencil oracle. Task 08's `benchmark.py` uses a different provisional source/coefficient/output. Those files and the manuscript PDF were left unchanged.

## Required downstream reconciliation

| Task | Concrete inputs and required changes |
|---|---|
| 03 HHL | Use original N, s=5, κ interval/scenario and B=h²A. Include padded effective dimension/gap separately. Use the task-05 state-bias conversion, not ε_out directly. Implement neighbor enumeration; existing dense oracle counts are not evidence for this access model |
| 04 modern QLSA | Read `benchmark-pp.json`. Keep sparse normalization α_B=20C as a conservative construction scenario until compiled; α/gap differs from original κ. Existing provisional models must update source, output and required precision |
| 05 I/O | Own a concrete norm plus coherent signed-overlap adapter, all preparation/synthesis/repetition costs and achieved failure bounds. Use c=h²1, compact host input and the supplied scalar budgets. Quantum I/O is mathematically specified but not a verified efficient circuit |
| 08 classical | Replace provisional discontinuous coefficient/random source/discrete mean 1/N/ε=10⁻⁸ with this smooth coefficient/polynomial source/continuum integral/h² weights/ε=10⁻⁴. Use original-residual tolerance; include DST-tridiagonal and Poisson-PCG competitors. Charge generation from compact host description. Existing measurements remain a separately labeled stress test and cannot be reused as measurements of this problem |
| 09 / 10 | Reject inadmissible mesh rows and unresolved quantum costs; do not publish this known-answer benchmark as evidence of unrestricted advantage. Keep parameter studies conditional and limitations prominent |

No downstream result files were silently rewritten. The handoff is finalized as a common specification, but existing task-04/08 provisional results still need their owners to reconcile and rerun. Exact gates, finite-size preparation bounds, physical failure evidence, production solver timings and a nonmanufactured application for any advantage claim remain external work, not unspecified choices of this benchmark.

## Review coverage and assumptions

C1-6 is addressed by constant sparsity, a derived polynomial conditioning relation and contrast/mesh sensitivities. C2-3 is addressed at the canonical scientific-computing benchmark level, including continuum accuracy and competitive structured/preconditioned classical methods; empirical production workload validation remains absent and is stated explicitly. C1-2 and reviewer 1 minor 4 are supported by explicit access/readout limitations; minor 1 is supported by distinct N, m, n, B, κ and α definitions. Figure-label and general grammar comments remain with tasks 03/10/11.

Established here: edge-energy spectral bounds, truncation/quadrature bounds, residual and representation conversions, preconditioned spectrum and classical separable reduction. Chosen assumptions: square smooth diffusion, manufactured source, contrast/grid ranges, accuracy allocation, compact host starting state and failure-budget requests. Measured: only small FP64 numerical diagnostics. Unresolved: reversible circuit resources, scalar-output estimator resources, achieved delivery reliability, calibrated HPC resources and production representativeness. No essential input blocks the solver-verification specification; a stronger production-advantage conclusion is unsupported.
