# Task 04: modern QLSA comparison

**Table V explanation:** [step-by-step PDF](Modern-QLSA-Table-V-explained.pdf), including formulas, assumptions, and the worked example.

**Table V implementation:** [code and usage](table-v/README.md) now reproduce the discrete-adiabatic QLSA T-count formula in Dalzell et al., arXiv:2211.12489v1, Table V. For `(N,kappa,epsilon_state,delta)=(1024,100,.01,.01)`, using the explicit defaults documented there, the model gives **12,386,477,814,166,393 T per attempt** and **86,705,344,699,164,751 T for seven attempts**. This published-formula estimate is separate from the certified-construction Shortcut bound below; it retains the source's numerical assumptions and omitted terms.

**Current upper-bound deliverable (14 September 2026):** [paper-ready report](Modern-QLSA-T-count-report.pdf), [LaTeX source](report/modern-qlsa-t-count.tex), and [callable estimator](report/upper_bound.py). `upper_bound.f(p)` returns an exact integer sufficient T-gate cap for one normalized solution state, with explicit trace-error and abort bounds. It expands matrix and RHS queries and includes controlled block encoding, QSVT, finite norm sampling, and bounded heralded rotation synthesis. The construction is deliberately conservative, not a practical cost forecast. Read [the reproduction guide](report/README.md).

For `N=1024`, `kappa=100`, `epsilon_state="0.01"`, `delta="0.01"`, the sufficient cap is **86721425529887187200 T gates**. The mathematical guarantee and its input-access/classical preprocessing assumptions are proved in the report; the program has not compiled an entire QLSA circuit. Task-02's matrix is instantiated, but scientific scalar extraction and QEC remain downstream costs.

The older expected-cost model below is preserved for practical modeling; its heuristic synthesis assumption does not provide the new report's guarantee.

**Earlier practical estimate (10 September 2026):** [t_count.py](t_count.py) exposes `f(p) -> T_count` and `estimate(p) -> detailed breakdown`. It combines the user-selected near-optimal unknown-norm Shortcut analytic bound with Clader et al.'s minimum-count stored-data block encoding. Read [t-count-model.md](t-count-model.md) for the complete formula, inputs, precision model and limits.

```python
from t_count import f
T = f({"N": 1024, "kappa": 100, "epsilon_state": 0.01})
# 1.477088576213547e12 modeled expected logical T gates
```

Run `python3 paper-revise/results/04-modern-qlsa/reproduce_t_count.py` from the repository root to reproduce the T-count examples, 72-row sensitivity table, 11 validation checks, task-01 stage exports and source manifest. Run `python3 paper-revise/results/04-modern-qlsa/t_count.py paper-revise/results/04-modern-qlsa/t-count-input.json` for a single JSON result. The model itself uses only the standard library; validation uses NumPy and jsonschema.

Task 02 is now reconciled at matrix/normalization level. Its actual diffusion instance has a separately generated example in `t-count-application-output.json`. The stored-data construction is a baseline, not a specialized PDE circuit. The returned cost includes RHS-unitary calls, controls, QSVT gates and ideal internal retries. It is a **modeled expected T count**, with an exposed rotation-synthesis approximation; it is not a compiled or certified end-to-end scalar estimate. Task 05 remains absent, and full output/QEC/hardware costs remain unresolved.

The older query-only deliverables below are preserved as **archived alternatives**. Their Algorithm 4 selection and statements that task 02 is unavailable are superseded by the current model. They should not be added to the new T-count stage.

Original delivery: verified reference/algorithm selection, an executable finite query model, a conditional norm-informed circuit model, task-01 stage exports, proposed manuscript text, and an explicit task-05/QEC handoff. At that original input capture task 02 and task 05 were unavailable.

Run from the repository root:

```sh
python3 paper-revise/results/04-modern-qlsa/reproduce.py
```

The script writes both model outputs, stage fragments, a sensitivity CSV, validation results, and input hashes. Standard-library model evaluation works on Python 3.6+; reproduction also requires `jsonschema` for structural validation and NumPy for the dense reflection check. Tested versions are recorded in `validation.json`. No shared source or manuscript PDF is changed. `sources/` preserves the two versioned reference PDFs and PDF text extracts. PDF extraction used PyPDF2 1.28.6 installed in `/tmp/hhl-task04-pdf-reader`; reproduction of the resource model does not need it.

Read [model.md](model.md) for equations, assumptions and cost boundaries; [references.md](references.md) for the reference audit; [manuscript-text.md](manuscript-text.md) for proposed wording. `model-input.json` and `norm-core-input.json` are task-local inputs, not complete task-01 workload records. `contract-stages.json` contains alternative stage fragments, which must never be summed together.

Reviewer coverage: C1-1 has a supported modern algorithm discussion/model, but its requested crossover shift awaits tasks 02 and 05–09. The handoff also supports C1-2 and C1 minor 1/4 (notation and limitations), and C2-1 (replaceable solver within the framework). Both actual reviewer PDFs were read, including the minor comments; this task does not claim to resolve unrelated comments.

Next: task 05 composes representation, coherent output and readout costs; tasks 04/05 validate phase generation and actual synthesis; task 06 schedules QEC; task 09 recomputes the comparison. The current remaining inputs are enumerated in t-count-model.md. No physical crossover is claimed.
