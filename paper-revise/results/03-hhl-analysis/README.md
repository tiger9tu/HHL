# Task 03 — HHL analysis repair

**Current practical-estimation direction (9 September 2026):** use application-specific numerical calibration for Trotter step selection. See [Trotter-error-practical-method.pdf](Trotter-error-practical-method.pdf), [manuscript-text.md](manuscript-text.md), and `practical-trotter/README.md`. The bound-based reports and schedules below are retained as established validation references; their sufficient step counts are not the new central practical estimates. No new end-to-end application calibration is claimed by this methodology edit.

**Updated proof:** [HHL-logical-scaling-analysis.pdf](HHL-logical-scaling-analysis.pdf), Section 2, now includes a complete consistent-microstep HHL theorem with explicit median-QPE/filter and success guarantees. The older direct-unitary adapter below is retained as a separate method; its conditional exponent is not the final bound in the updated report. See `report/README.md` for the new source and validation.

**Supported work delivered; task 02 benchmark reconciliation remains blocked by its missing handoff.** The former B19/Proposition 1 prefactor is not certified. The replacement is a deterministic product-formula operator-error bound with explicit QPE/uncomputation and postselection accounting. Task 01 v1.0.0 compatibility is demonstrated for the exported core-stage fragment, not a complete workload.

Read:

- `derivation.md`: corrected proof, restricted dimension-uniform result, logical schedule and provisional PDE specialization.
- `audit-and-handoff.md`: manuscript/code trace, recovered historical experiment settings, reviewer coverage, downstream changes and exact missing inputs.
- `manuscript-text.md`: replacement proposition, appendix instructions, complete Figure 9 caption and dependent-claim edits.
- `resource-model.md`: task-01 field mapping, ownership, unresolved compilation and error inputs.
- `figure9.pdf` / `figure9.png`: replacement figure; `samples.csv`, `commutators.csv`, `summary.csv` contain raw and summarized evidence.
- `validation.json`, `pde-validation.csv`, `contract-validation.json`: numerical and interface validation.
- `model-input.json`, `model-output.json`, `contract-stage.json`: concrete restricted schedule and schema-valid stage fragment.
- `manifest.json`, `input-versions.json`, `requirements-tested.txt`, `run.log`: provenance, source hashes, environment and run result.

## Measured results

485 matrices, 3880 evolution-error measurements; all satisfied ||S_r(τ)−exp(iHτ)||≤τ²C_comm/(2r) within the 2×10^−12 comparison tolerance. The largest error/bound ratio was 0.9999881; the largest unitarity residual was 1.144×10^−14. This finite validation accompanies the proof and is not itself an asymptotic guarantee.

The original Z,X “tightness” example at τ=.2 gives effective-Hamiltonian error .2008868 against the written B18 RHS .2, disproving its claimed exact equality. The full clock/system exact-grid HHL test has reference success probability .2; successful-state error decreases from .0364249 at r=16 to .000137203 at r=4096. The conservative conditioned-state bound at r=4096 is .0543107. Some coarse-r analytic bounds exceed the maximum possible vector distance and are therefore uninformative but still valid.

PDE condition numbers increase from 5.8284 (N=9) to 57.6955 (N=121), matching the analytic spectrum. Dense relative solve residuals are below 3.5×10^−15; normalized manufactured-solution error decreases from .0400645 to .00373208. These tests do not define the still-missing common scalar output.

## Reproduce

Run from the repository root. The recorded run used `/tmp/hhl-task03-venv/bin/python` (Python 3.6.15) with one BLAS thread. This temporary environment is not an artifact dependency: recreate a Python environment with the versions in `requirements-tested.txt`. On a newer interpreter use compatible NumPy/SciPy/Matplotlib/jsonschema versions and record the new manifest; floating-point and bootstrap details can differ. PDF inspection used a separate temporary environment with PyMuPDF 1.28.2; no PDF library is needed to rerun the experiments.

```bash
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
python experiments.py  # when working in this results directory
python validate_pde.py
python logical_model.py model-input.json > model-output.json
python export_contract.py
python capture_versions.py
```

Equivalently, prefix every script/input path with `paper-revise/results/03-hhl-analysis/` when running from repository root. Scripts write to their own directory. `export_contract.py` requires the sibling task-01 schema. Only `experiments.py` uses the Git executable for recording the input commit. The raw files are deterministically ordered. Bootstrap samples are drawn at the matrix level; see the protocol before interpreting intervals or correlated pair observations.

The actual final commands used `/tmp/hhl-task03-venv/bin/python` in place of `python`. Requirements installation and source inspection do not alter shared repository code. No Q# compilation, MATLAB execution, QEC simulation or physical-resource validation is claimed.

Task 02 must supply its benchmark generator/version, matrix scaling, RHS, scalar output, accuracy/discretization target, access and preconditioning specification. Tasks 05–09 must resolve I/O, compiled costs, repetitions and physical/classical models before a new crossover can be quoted. Task 12 owns shared-code integration; unrelated workspace changes were preserved.
