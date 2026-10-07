# Logical-resource contract and adapter

**Methodology update, 9 September 2026:** the current practical route takes the common-microstep repetition `r0` from application-specific numerical calibration; see `practical-trotter/method-section.tex`. For a single forward/inverse QPE pair, `K_HS1 = 2 L r0 (2^m - 1)`. Store the instance/generator, normalization, decomposition/order, error metric, numerical method, tested range, uncertainty and empirical/validated-bound status with this input. The sufficient-bound adapter documented below and its exported example remain historical diagnostics. Its bound certificate cannot be transferred to an empirically selected schedule. A revised complete application contract requires the application/output calibration; none is fabricated in this update.

Task 01's **v1.0.0** interface became available during task 03. `contract-stage.json` uses its actual `definitions.stage` schema and typed quantities; `contract-validation.json` records the schema SHA-256 used. This is a **stage fragment**, intentionally not a fabricated complete quantum/classical workload or benchmark record. `export_contract.py` validates its structure against that definition. Task 05 must assemble it with assumptions, symbols, pp, cq, budgets, I/O stages and provenance, then run task 01's full lineage/coverage validator. Unknowns are not zero.

`logical_model.py` is a small internal numerical helper taking a flat task-local configuration (`model-input.json`); that input/output pair is **not itself task 01's schema**. `export_contract.py` performs the public export. It demonstrates R4 on the same 2×2 SPD instance as the circuit test. `model-output.json` is a schedule diagnostic, not a physical-resource estimate. No invented per-term gate costs are supplied.

## Mapping to v1.0.0

| Local symbol/input | Task-01 location / meaning |
|---|---|
| N, actual row/column sparsity, original κ | `pp.N`, `pp.s_row`, `pp.s_col`, `pp.kappa_2`, typed quantities, unit `1` |
| H=A/α, effective gap bound | `cq.transformed_operator` and `cq.parameters`; preserve original `pp.kappa_2` |
| L, C_comm, τ_base, p_min, m | Named `cq.parameters`; L,p_min dimensionless; m width uses `bit`; C_comm and τ use the explicitly dimensionless normalized H convention, not seconds |
| ε_state,PF | `cq.parameters` plus the task-05 conversion into the common output budget; do not equate to `pp.output.epsilon` automatically |
| K_HS1=2LΣr_j | Diagnostic internal counter; expand with controlled-term implementations into `resources.gates`, oracle queries and layers |
| G_core, D_core, DT_core, peak live workspace | Stage `resources.gates`, `depth`, `t_depth`, `logical_qubits_peak` |
| Core invocation count | `multiplicity=1` in exported fragment; task 05's attempted circuit receives the external capped/expected repetition multiplicity |
| Access queries | `oracle_queries.A`; `queries_expanded=false` prevents premature QEC evaluation. Supply expansion and set true only when oracle gates are included |
| Circuit error and postselection success | Accuracy certificate attached by assumption/provenance, not a substitute for a common observable error or failure budget |

Exported stage `q_hhl_core_03` covers `q.core` only. It includes forward QPE, reciprocal and inverse QPE (non-HS gates remain symbolic), but excludes preparation, heralding measurement, readout, classical setup and physical/QEC resources. After task 05 incorporates it in `q_try`, do **not** also add it as another primitive stage. External retry factors are not already applied. Coherent amplification requires replacing the core circuit and resource model.

The core export's symbolic gate counts are K_HS1·g_HS1_g+g_nonHS_g for exclusive compiled buckets g∈{T,Clifford}. A bucket's term cost includes controls, reversible color/position/value lookup and uncomputation, and rotation synthesis. `q_A_HS1` counts the corresponding original A-access calls. Non-HS core must also declare additional oracle calls if a chosen reciprocal/QPE implementation uses them; the current expression assumes none there. `D_HS1`, `DT_HS1`, `D_nonHS`, `DT_nonHS` are compiled layer counts for serial execution. `W_core_peak` is maximum extra simultaneously live workspace beyond the system, clock and reciprocal flag. These are unresolved nonnegative integers. The example's K_HS1=417852 is a sufficient schedule, not a measured optimal call count.

Assumption IDs to import with the fragment:

- **A03-commutator (proved, conditional inputs):** H is Hermitian, the supplied terms sum to H, C_comm bounds their pairwise commutator sum, and times/steps follow R4. In the 2×2 example C_comm=.06 is computed analytically from .15Z and .2X.
- **A03-reference (validated restricted instance; otherwise input required):** the reference finite-QPE circuit is accurate for the target and p≥p_min. Example eigenvalues .25,.75 lie on the 3-bit phase grid, τ_base=2π, exact successful branch probability .2≥1/9. This is not a theorem for arbitrary input matrices. Downstream reference/filter error must be budgeted separately.
- **A03-compilation (unresolved):** controlled term and non-HS implementations, entry precision, rotation synthesis and live-workspace schedule are supplied and their errors accounted for. Until resolved, no numerical T-count, depth, physical estimate or crossover is justified.

For a norm≤1 observable, normalized pure-state vector distance e implies expectation difference at most 2e by expanding the quadratic form; task 05 may use that conservative conversion when its actual output is this observable. A physical solution functional can require norm recovery and a different conversion. State error, stochastic failure and discretization error remain distinct.

Success lower bound `(sqrt(p_min)−η_PF)^2` in the local output accounts for **PF error only**. Add all other full-circuit implementation errors before exporting a final retry cap. The reference's own algorithmic bias is a separate output-error certificate. The helper's `expected_attempts...` is a diagnostic upper bound, never the capped multiplicity required to guarantee delivery with δ_total.

Pending reconciliation is solely with task 02's unavailable instance and task 05's future I/O/error implementation, plus any later incompatible revision of the now-versioned task-01 contract. No complete output target has been invented to fill those gaps.
