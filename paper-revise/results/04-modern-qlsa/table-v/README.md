# Table V QLSA estimator

[Step-by-step PDF explanation](../Modern-QLSA-Table-V-explained.pdf) covers the normalization, schedule, precision allocation, primitive costs, all six Table V terms, and the numerical example. [Editable LaTeX](step-by-step.tex). The PDF includes the source, estimator, input, output, and reproduction script as attachments. Rebuild using `bash build_explanation.sh` with Python 3.11+, Tectonic, and PyMuPDF; executable overrides are `HHL_PYTHON`, `HHL_PDF_PYTHON`, and `HHL_TECTONIC`.

`paper_table_v.py` implements the two T-count columns of Table V, page 22 of [Dalzell et al., arXiv:2211.12489v1](https://arxiv.org/pdf/2211.12489v1#page=22), with the controlled block-encoding and state-preparation costs from Tables III/IV, page 14. It is an alternative discrete-adiabatic solver model, separate from the earlier Shortcut estimators.

## Result and usage

From this directory, with Python 3.11 or later (standard library only):

```python
from paper_table_v import f, estimate
p = {"N": 1024, "kappa": 100, "epsilon_state": "0.01", "delta": "0.01"}
assert f(p) == 86705344699164751
print(estimate(p))
```

Or run `python3.11 paper_table_v.py input.json`. Run `python3.11 reproduce.py` to regenerate the numerical examples, source hashes, and validation. `output.json` contains every exclusive contribution. Five validation groups cover hand-calculated source-table values, normalization and error allocation, decimal precision, retry boundaries, and invalid inputs.

| Quantity | Example result |
|---|---:|
| Ordinary condition bound | 100 |
| Frobenius inverse-gap bound K | 3200 |
| Adiabatic schedule parameter Q | 12,800,000 |
| Filter degree d | 44,210 |
| Controlled matrix-BE calls per attempt, 2(Q+d) | 25,688,420 |
| RHS preparation/unpreparation calls per attempt, 4(Q+d) | 51,376,840 |
| T per controlled matrix BE | approximately 481,250,499.9233 |
| Table V single-attempt T, rounded upward | **12,386,477,814,166,393** |
| Retry cap for delta=0.01 | 7 |
| `f(p)`: seven-attempt T budget estimate | **86,705,344,699,164,751** |

The per-attempt total is a noninteger paper-model value before rounding. `f` multiplies the rounded per-attempt value by the retry cap. The returned integer is a reporting convention, not evidence of a certified Clifford+T circuit.

## Source formula and adapter choices

Writing L=2^ell for the padded dimension, the uncontrolled QLSS column is implemented as

```
T = 12 Q log2(1/epsilon_ar)
    + 2(Q+d) T_controlled_BE + 4(Q+d) T_SP
    + Q(24 ell+31) + 3d log2(1/epsilon_z) + d(32 ell-2).
```

`table_v(L,Q,d,epsilon_G,epsilon_h,epsilon_ar,epsilon_z,epsilon_tsp=None)` directly evaluates that row and, if `epsilon_tsp` is supplied, the controlled-QLSS row for the tomography sign circuit. It does not add tomography repetitions or optimization iterations.

Four problem parameters do not uniquely set all Table V inputs. The `estimate`/`f` adapter makes these explicit choices:

- `kappa` retains its earlier meaning: ordinary spectral condition bound. The default Frobenius/spectral ratio is sqrt(L); thus K=kappa sqrt(L). Positive nonsingular padding inside the original singular-value range is assumed. Supply `frobenius_over_spectral` for a tighter certified ratio, or `effective_inverse_gap` for K directly, but not both. The program validates domains, not spectral certificates.
- `adiabatic_constant` defaults to the paper's numerical assumption C=2000 for general matrices. Set Q=ceil(2CK), following its Eq.(66) numerical approximation. The omitted O(sqrt(K)) term is not bounded by this program.
- `epsilon_state` is the normalized solution-state error target, not tomography accuracy. Let s=epsilon_state/5. Choose epsilon_qsp=s, d=2 ceil(K ln(2/s)), epsilon_G=s/[2(Q+d)], epsilon_h=s/[4(Q+d)], epsilon_ar=s/(4Q), and epsilon_z=s/(2d). These five contributions sum to epsilon_state in the paper's Eq.(64). Equal splitting and even-degree rounding are our adapter choices. The 2d coefficient follows Eq.(64); Eq.(65) instead displays d, which we do not use. We do not apply the paper's tomography-dominated 90% allocation to a state-only task.
- `delta` is a solver abort target. Table V itself has no such parameter. The adapter chooses r=ceil(log2(1/delta)) independent attempts, assuming the ideal per-attempt success lower bound 1/2. Thus for delta=.01, r=7 and modeled abort is at most 1/128. Approximate circuit success is not independently recertified. This delta is not the paper's tomography-failure parameter.

All logarithms are evaluated with 80-digit Decimal arithmetic. The example's rounded result agrees at 40 and 100 digits too. The source's normalization bound need not be tight; `alternatives.json` also reports the different scenario K=100 and sensitivity to C=15307. Substituting the larger C alone does not certify the omitted schedule or synthesis terms.

## Interpretation

This is a faithful implementation of the displayed finite paper model, **not a rigorous sufficient upper bound**. Tables III/IV explicitly suppress doubly/triply logarithmic terms; the synthesis convention is R_T=3 log2(1/error); C=2000 is assumed numerically; and Q drops a remainder. These limitations are returned in the JSON. A certified upper bound requires replacing those approximations with explicit schedules and verified circuits.

The source's Table III BE has a leading L^2 cost, whereas the earlier Shortcut model selected a different, minimum-T stored-data construction. Comparing totals therefore changes both solver and BE implementation. Do not interpret the ratio as an isolated improvement in the QLSA algorithm. These counts include state preparation and internal quantum gates but exclude tomography, QIPM iterations, classical preprocessing, and QEC.

## Optional readout (version 1.1)

The default `include_readout=False` preserves the original state-only result. `include_readout=True` adds the paper's **full real-vector tomography** (Sec. IV.D/Proposition 4), returning a classical approximation to the normalized vector. This is a separate output task from the future PDE scalar-readout case.

```python
state_T = f(p)
vector_T = f(dict(p, include_readout=True,
                  epsilon_readout="0.01", delta_readout="0.01"))
```

`epsilon_readout` is the total normalized-vector error target xi (defaults to `epsilon_state`). `delta_readout` is the tomography failure allowance (defaults to `delta`). The adapter allocates 90% of xi to sampling, 5% to solver error after its 1.58 coefficient, and 5% to reference preparation after its 1.58 sqrt(L) coefficient. Thus:

```
epsilon_tomo = 0.9 xi
epsilon_core = min(epsilon_state, 0.05 xi / 1.58)
epsilon_tsp = 0.05 xi / (1.58 sqrt(L))
k = ceil(57.5 L ln(6L/delta_readout) /
         (epsilon_tomo^2 (1-epsilon_tomo^2/4)))
T_total = k * (ceil(T_QLSS) + ceil(T_controlled_QLSS))
```

The solver is repriced at `epsilon_core`; the two Table V columns are each executed k times. The source's sampling formula already includes unsuccessful solver flags. **Do not multiply this by the state-only retry cap, or add another state-only preparation budget.** `T_one_solver_execution` plus `T_additional_after_one_execution` is an exclusive decomposition of the total. Precision retuning means the cost is not obtained by merely appending measurements to the original seven-attempt budget.

For the same dimension/condition example, with both state and output targets .01 and failure allowance .01, there are **9,688,792,223 samples per circuit family** and a total modeled **271,767,176,507,565,562,710,978,575 T gates**. See `readout-input.json` and `readout-output.json`. This full-vector result does not predict the cost of estimating a single observable. Physical solution norm recovery, classical reconstruction, QIPM iterations, and QEC remain excluded.

`estimate(p)['T_total']` always matches `f(p)`. With readout enabled, top-level Q/d/precision and `T_retry_budget` retain the state-only baseline, while the `readout` object contains the actual retuned schedule, component errors, repetition counts, and both circuit costs. The same published-model limitations apply: these numbers are not certified circuit upper bounds. Disabled readout with explicit readout-only parameters is rejected, preventing accidental ignored settings.
