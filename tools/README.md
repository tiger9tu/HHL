# Surface-code resource estimator

This estimates a **T-count-limited** fault-tolerant computation's physical
qubits, runtime, and energy. It does not simulate the quantum circuit.
The core uses only the Python standard library (Python 3.6+); notebooks also
require NumPy and Matplotlib. Q# is needed only for `estimator.ipynb`.

## Use from the repository root

```python
from tools.resource_estimator import (
    Workload, Hardware, ErrorBudget, PowerModel, optimize,
)

result = optimize(
    Workload(logical_qubit_count=100, t_gate_count=10**8),
    Hardware(physical_error_rate=1e-4, cycle_time_seconds=1e-6,
             max_physical_qubits=200000),
    budget=ErrorBudget(distillation=0.01, surface=0.01),
    power=PowerModel(watts_per_physical_qubit=6.25, fixed_watts=0),
    objective="space_time",  # also: "runtime", "qubits", "energy"
)
print(result.physical_qubits, result.runtime_seconds, result.energy_joules)
print(result.code_distance, result.total_failure_bound)
```

The default error allocation is **1% distillation + 1% surface-code faults**, as
in Litinski's example; it is a 2% combined bound, independent of HHL approximation
error. For a 1% combined budget, use `ErrorBudget(0.005, 0.005)` or another split.
`InfeasibleConfiguration` is raised when no candidate meets the constraints.
Logical resources must be positive integers; zero-T/Clifford-only circuits are
outside this T-count runtime model. Physical error must lie strictly between
zero and the fitted 1% threshold. The default search uses odd distances 3--99.

For HHL inputs, `HHL(n, sparsity, kappa, epsilon, precision).as_workload()`
converts the original scaling formulas to integer counts, rounding up. Here
`n = log2(N)` and `precision` counts bits. The unused historical `ancilla_qubits=20`
attribute has been removed; it was never included in the logical-qubit formula.

When running a notebook in `tools/`, import `resource_estimator` without `tools.`.
`surface_code_opt.estimate_resources(...)` is a convenience interface using the
original argument order. `find_optimal_setting(...)` still returns four values;
its third value is now **physical code cycles**, not tile time steps. Multiply
it by the physical cycle duration exactly once. The old mutable low-level
helpers are replaced by `evaluate_configuration()` and `optimize()`.

## Calculation and search

For every admissible factory type, data layout, and factory count:

1. Require `T_count * magic_state_error <= distillation_budget`.
2. Compute tile steps from the slower of factory supply and data consumption.
3. Count integer data tiles, factories, buffers, and any `extra_routing_tiles`.
4. Choose the smallest odd distance satisfying
   `tiles * steps * d * 0.1*(100*p)**((d+1)/2) <= surface_budget`.
5. Compute `physical_qubits = 2*d**2*tiles` and reject hardware-limit violations.
6. Convert `code_cycles = steps*d` and `runtime_seconds = code_cycles*cycle_time`.
7. Compute `power = fixed_watts + physical_qubits*watts_per_physical_qubit`
   and `energy_joules = power*runtime_seconds`.

Search stops adding factories at supply/consumption saturation. Every candidate
has its distance re-evaluated; selection considers all factory types, rather
than choosing the smallest factory first. Error contributions and tile
components are included in the immutable `Estimate` result for inspection.

`space_time` minimizes physical-qubit seconds. It equals energy minimization
when fixed power is zero and per-qubit power is a positive constant. Other
objectives can choose different configurations.

## Published references and corrections

Source: [D. Litinski, *A Game of Surface Codes*, arXiv:1808.02892v3](https://arxiv.org/pdf/1808.02892v3).

- **Intermediate layout:** retain **2n+4**, agreeing with Section 2.2 and the
  204-tile example in Section 4.4. Figure 13(a)'s **2.5n+4** caption is inconsistent.
  The original script already used the consistent formula; this choice is now
  explicitly documented and tested.
- **116-to-12:** use **41.25 p^4**, not the old script's 4.125 p^4 (Section 3.5).
- **225-to-1:** use **35^4 p^9** and **15 steps** for the 176-tile factory
  (Section 3.5/Figure 19), replacing the old 1.5 p^7 and 5.5 steps.
- **Factory throughput:** defaults account for rejection as `(1-p)^n` for
  15-to-1 and 116-to-12; 225-to-1 uses the paper's approximate level-1 stall
  correction `(1-p)^15`. The 81-tile, 50-step 116-to-12 variant is available.
- **Discrete fast layout:** near-square paired patches with a shortened last
  column, following Section 2.3, give 231 data tiles for 100 logical qubits.
- **Energy:** use the selected configuration's qubits, replacing the notebook's
  fitted `4375*log2(N)+31250` estimate.

## Reproduce and test

From the repository root:

```bash
python3 -m tools.resource_estimator.benchmarks
python3 -m unittest discover -s tools/tests -v
```

The benchmarks use 100 logical qubits, 10^8 T gates, 1 microsecond per physical
cycle, and separate 1% error budgets. They fix the published distance and use
the paper's stated average production times (11 or 9.27 steps per state).

| Configuration | p | d | Tiles | Physical qubits | Seconds |
|---|---:|---:|---:|---:|---:|
| Figure 21a, compact, one 15-to-1 | 1e-4 | 13 | 164 | 55,432 | 14,300 |
| Figure 22a, intermediate, two 15-to-1 | 1e-4 | 13 | 226 | 76,388 | 7,150 |
| Figure 23a, fast, eleven 15-to-1 | 1e-4 | 13 | 363 | 122,694 | 1,300 |
| Figure 21b, compact, one 116-to-12 | 1e-3 | 27 | 210 | 306,180 | 25,029 |

These are fixed-configuration evaluator tests, not requirements that the optimizer
select these configurations. Rejection-adjusted defaults slightly change runtime:
for example, eleven 15-to-1 factories give approximately 1,301.95 seconds instead
of 1,300. The test suite separately verifies distance selection, optimization
against a larger independent search, error/hardware limits, and notebook use.
At 6.25 W/qubit the first row consumes **4,954,235,000 J**; this energy is derived
from our power assumption and is **not** a published Litinski energy result.

## Scope and approximations

- This is an expected **steady-state** rate model. It omits warm-up/drain time,
  burst/stall scheduling variance, T-depth parallelism, decoder/feed-forward
  latency, input/output transfer, and circuit-dependent routing.
- Default storage follows the compact/intermediate 15-to-1 examples (zero extra
  storage), the fast 15-to-1 example (one tile/factory), and compact 116-to-12
  (13 tiles/factory). The latter allowance is retained for other 116-to-12
  layouts; it is not an exact reproduction of every layout in the paper.
  225-to-1 has a one-tile output buffer. `extra_routing_tiles` allows additional
  overhead, but the estimator does not certify geometric routability.
- All patches, including factory and storage patches, use the same distance.
  Multi-level factories with different distances are not modeled.
- The fit and leading-order distillation polynomials are model estimates.
  Their summed error bounds are not a hardware validation or a simulation.
- The default 6.25 W/qubit is the original HHL study's power assumption, not
  a universal device specification; supply another `PowerModel` as needed.
- `heatmap.ipynb` and `protocols.ipynb` use the new estimator. Previously saved
  outputs are cleared because accounting changed; rerun to regenerate figures.
  The protocol plot marks configurations that exceed its qubit limit in gray.

## Files

- `resource_estimator/models.py`: immutable inputs/results.
- `resource_estimator/protocols.py`: data/factory models and source notes.
- `resource_estimator/evaluate.py`: one complete physical configuration.
- `resource_estimator/optimize.py`: constrained enumeration and objectives.
- `resource_estimator/energy.py`: parameterized power calculation.
- `resource_estimator/hhl.py`: optional HHL logical-resource adapter.
- `resource_estimator/benchmarks.py`: published fixed configurations.
- `surface_code_opt.py`: original main-call compatibility interface.
- `tests/test_resource_estimator.py`: numerical and integration checks.
