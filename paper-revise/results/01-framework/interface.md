# Parameter dictionary and interface contract v1.0.0

`interface.schema.json` is JSON Schema Draft 7. `symbolic-example.json` is a valid, uninstantiated example of the capped observable calculation in `framework.md`. All fields are required unless the schema says otherwise; additional fields are rejected in fixed objects. Model-specific quantities belong in `parameters`, `limits`, or `symbols`; a change to the meaning of an existing field requires a new major contract version. Additive interface changes require a minor version and explicit reader support.

## Problem and configuration dictionary

| Field / notation | Meaning and unit | Constraint / owner |
|---|---|---|
| `pp.instance_id` | Instance/generator, dataset version and seed reference | Task 02; preserve common input across branches |
| `pp.N`, N | Original square matrix dimension, unit `1` | Positive integer; n = ceil(log₂ N) is index-register width, not N |
| `pp.matrix_class` | Real/complex, Hermitian/general, SPD/indefinite; invertibility assumptions | Explicit eligibility of each solver; singular problems need a different solution contract |
| `pp.s_row`, `pp.s_col` | Maximum nonzeros per row/column, `1` | Integers in [1,N] for invertible square A; do not assume equality except when justified |
| `pp.kappa_2`, κ₂(A) | Largest/smallest singular-value ratio, `1` | At least one; original operator, not a preconditioned or normal-equation operator |
| `pp.scaling` | Physical units of A,b,x, normalization, reversible scale factors | Scalar rescaling does not change κ₂; state normalization can change requested output |
| `pp.matrix_representation`, `input_access`, `input_location`, `rhs` | Sparse/dense/matrix-free input, access guarantees, initial location, nonzero RHS definition | Include generation, oracle construction, loading and retained storage; task 02 supplies instance, 05 supplies access costs |
| `pp.output.definition` | f(x), full vector, state, sample, or observable | Both branches implement exactly this output; dimension/count and normalization explicit |
| `pp.output.metric`, `epsilon`, `unit` | Output distance, tolerance and physical output units | `epsilon` is dimensionless: metric must be dimensionless or divided by a declared fixed reference scale. For dimensional outputs name that scale in `metric` and store it in the benchmark specification. Relative error needs a zero-output rule |
| `pp.output.delta_total` | Probability of failing the stated accuracy/delivery criterion, `1` | In (0,1); `success_scope` declares per-output or whole-batch delivery; separate from numeric error tolerance |
| `pp.output.reference_solution` | Exact target and trusted evaluation procedure | Benchmark accuracy and reference error supplied by 02/08 |
| `pp.reuse.outputs`, B | Number of requested outputs in workload, `1` | Positive integer, includes repeated RHS/observables as specified |
| `pp.reuse.groups`, `invalidation` | Which data/setup can be reused and what invalidates it | Reuse cannot span incompatible A, precision, access or hardware settings without justification |
| `cq.algorithm`, `cc.algorithm` | Algorithm/version and stopping criteria | Tasks 03/04 and 08; not interchangeable labels CG/CGNE |
| `*.transformed_operator`, `*.preconditioner` | Original-to-effective operator mapping and recovery | Store effective N,s,κ₂, block-encoding α and implementation error as separately named parameters; no overwriting `pp` |
| `*.precision` | Arithmetic bit widths, rounding, synthesis precision | Bits differ from accuracy; parameters use `bit` for widths |
| `*.io_model` | Versioned input/output adapter | 05 owns quantum I/O/repetition; 08 owns classical implementation consistent with 05 |
| `cq.compilation` | Logical gate basis, decomposition/synthesis and scheduling rules | Rotation/Toffoli counts cannot be added to their expanded T gates |
| `cq.qec` | Code, decoder, distances, factories, routing and logical failure model | Task 06; requested budget and achieved bound distinct |
| `*.hardware` | Device/node/network, control, memory and facility configuration | Tasks 07/08; distinguish measured, projected, and assumed |
| `*.parameters`, `*.limits` | Named quantities, such as physical error probability, cycle duration, bandwidth, memory capacity, qubit cap | Parameter keys and applicability documented by owning model; never convert Hz directly to FLOP/s |
| `*.optimization_policy` | Fixed configuration or optimized objective, constraints and candidate set | Same policy across each sensitivity sweep; report choices per sample |
| `*.model_version` | Commit, release, source/equation version | No floating “latest” dependency |

## Typed quantities and statistics

Every quantity has `unit`, `status`, and `note`. A `known` quantity has a nonnegative numerical `value`; a `symbolic` quantity has an unevaluated `expression`; `unknown` has neither. Unknown is never zero. Known values may be measured, assumed or derived: link evidence through the enclosing stage's assumption IDs. An exact zero is permitted only with an explanatory note, e.g. no physical qubits for the classical branch. Symbolic expressions are inert text and must never be passed to `eval`. All symbols, units, domains, equations and dependencies must be resolved by an owning downstream model before evaluation; this schema is an exchange contract, not a symbolic algebra engine.

Counts describe nonnegative resource use. Deterministic realized counts are integers; analytic upper bounds and expected counts can be real. Round up when allocating indivisible gates, attempts, qubits, bytes, factories or cycles. Do not round an expectation and silently call it a tail bound. A stage's `statistic` applies to its work counts/time/energy. Fields explicitly named `peak` are capacity bounds over the declared schedule, never expected occupancy. `statistic_note` identifies conditioning, tail probability, confidence level and whether the bound is analytic or modeled. Unknown schedules imply unresolved runtime.

Canonical units: `s`, `J`, `W`, `byte` (8 bits), `bit`, `operation/s`, `byte/s`, `s/code_cycle`, `W/physical_qubit`, and typed dimensionless resource counters (`gate`, `query`, `layer`, `logical_qubit`, `physical_qubit`, `code_cycle`, `operation`, `1`). Decimal GB = 10⁹ bytes and GiB = 2³⁰ bytes are converted before exchange. The optional `m2` unit is available for an independently justified common installation footprint. Do not combine incomparable types just because they are mathematically dimensionless.

## Stage resources and ownership

| Schema group / field | Definition / aggregation |
|---|---|
| `logical.gates` | Exclusive compiled primitive buckets per invocation; key names defined by `gate_basis`; T bucket includes T and T† by default. Never sum a total bucket with its constituent buckets |
| `oracle_queries` | Diagnostic calls per oracle per invocation; `queries_expanded=true` means their gate implementation is already in `gates`. Otherwise QEC evaluation must wait for expansion or a documented external oracle adapter |
| `depth`, `t_depth` | Dependency layers and non-Clifford T layers per invocation under declared basis/schedule; neither is seconds nor determined uniquely by gate count |
| `logical_qubits_peak` | Simultaneously live algorithm, input, output and ancilla qubits; excludes QEC factories/encoding. Composition must account for retained registers and overlapping lifetimes |
| `classical.operations` | Count by disjoint kind and precision; real add/multiply convention explicit, FMA counted as two FLOPs if using FLOP convention; divisions, integer work and complex arithmetic not silently treated identically |
| `classical.memory_peak` | Peak allocated bytes by disjoint tier/device; includes inputs, factors, preconditioners, workspace, outputs and retained reusable state |
| `data_movement` | Bytes crossing a named interface in a specified direction; movement is traffic, not capacity. Counting DRAM and interconnect traffic is valid as separate resources, not one bandwidth denominator |
| `synchronizations` | Count of synchronization events; latency/topology in hardware model, blocking order in schedule |
| `qec.code_cycles` | Total syndrome-extraction rounds for the already composed input workload; code-distance factors and factory scheduling already included. Never multiply by distance again in the hardware adapter |
| `qec.physical_qubits_peak` | Data + syndrome + factories + storage + routing + any reserved capacity needed for peak execution |
| `qec.distance`, `factory_count` | Integer configuration choices for a homogeneous schedule; heterogeneous details must be provided through a versioned schedule artifact and configuration parameters |
| `qec.failure_bound` | Achieved bound for its full workload, including repetitions, not a per-gate target |
| `hardware.time`, `energy` | Schedule makespan in s and attributed energy in J; derived from complete workload at the stated scope |
| `hardware.memory_peak`, `physical_qubits_peak` | Capacity bounds; report infeasibility if they exceed declared limits; no bytes/qubits ratio |

Each stage has one owner, an ID, a branch, a scope, a reuse key, a multiplicity, a statistic, and a list of atomic cost tokens in `covers`. At the primitive workload layer, these tokens must be disjoint within a branch. For example, task 03 publishes a core model; task 05 incorporates it into a complete attempted circuit. A composed `q_try` may cover preparation, core and heralding: do not also add the imported task-03 core as a second primitive stage. Record its version as provenance instead. Coherent amplitude amplification/estimation belongs inside the circuit model; external repetition belongs in multiplicity. Never apply the success factor twice.

`resources` are per invocation of that stage; `multiplicity` counts invocations within its `scope`. All examples use `1` for aggregate QEC/hardware stages, because they already consume predecessor multiplicities. `derived_from` lists transformation dependencies, not additional costs to sum with this stage. A derived stage's `covers` must be exactly the disjoint union of its input coverage. Logical stages transform into QEC; QEC and host work transform into hardware time/energy. This makes resource transformations distinguishable from additive workload phases.

A full hardware total must cover every primitive cost token in its branch exactly once and use multiplicity one. Intermediate hardware records may cover separate scopes, but the total must consume them rather than repeat them. Schedule documents supply execution dependencies and overlap: `derived_from` is a resource-lineage DAG, not an execution-order DAG. Serialize only with explicit justification. For serial phases, sum work and duration, but take peak simultaneously live allocations, accounting for retained buffers. For parallel phases, schedule conflicts explicitly, sum concurrent power and space, and use makespan. A shared idle device is charged once over its occupied interval.

`scope=setup` is once per valid reuse group, `per_output` is per requested delivered output, and `batch` is once for the complete B-output workload. Converting scopes is a model operation with explicit reuse-group counts and output count in its schedule. A consumer applies each scope factor once. Preserve first-output latency, batch makespan, amortized time/energy, and peak capacity as distinct metrics, using separate records if necessary.

## Accuracy, uncertainty and acceptance

`budgets` separate normalized output-error allowances from failure probabilities, with the applicable `branch`, scope and event/conversion. Task 05 provides the conversion to the common output criterion; algorithm state error, residual tolerance and discretization error must not be added without such a conversion. Per-output and batch failure budgets require a justified conversion; union bounds are valid without independent failure events. Quantum and classical budgets are separate certificates for the same target, not additive costs or failure probabilities across alternative machines.

Run `python3 validate.py symbolic-example.json --self-test`. The validator checks schema structure, canonical resource units, IDs, acyclic lineage, non-overlapping coverage, complete final coverage, and selected numerical domains. Rejection cases exercise unit mixing and double counting. It does not prove symbolic algebra, accuracy certificates, feasibility, schedule correctness, confidence levels, or physically complete coverage. Those require the owning models and the review checklist in `assumptions.md`. A schema-valid record alone cannot support a crossover claim. `feasibility` records each branch as feasible, infeasible or unresolved with a reason. `status=evaluated` requires resolved quantities, matched-scope budgets for both branches and resolved feasibility, and additionally requires a separate scientific validation record before publication.
