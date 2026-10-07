# Task 13 handoff — QETU-based QLSA

The logical scaling is derived in [model.md](model.md), including a valid even QETU inverse polynomial, success overhead, controlled-evolution costs and error budgets. The project’s existing effective-Hamiltonian Trotter analysis gives a sufficient microstep count independent of the inverse-filter degree, provided every query uses the same microstep and exact adjoints.

For inverse gap K, order-p effective-H error a_app h^p, and state error ε_x, the evolution cost of a direct inverse filter with coherent amplification is

    Õ(g_step,p K² max{r_branch,(a_app K/ε_x)^(1/p)})

in the worst case. Here r_branch enforces the valid local-logarithm range. For first order when the accuracy requirement dominates, this is Õ(g_step,1 a_app K³/ε_x). Simple postselection instead costs a further factor K, up to logarithms. This is a sufficient scaling, not an optimality claim. A small prefactor relative to block encoding remains a hypothesis until both controlled microsteps and block-encoding circuits are compiled for the same application.

Deliverables:

* [Full derivation, assumptions and downstream interface](model.md).
* [Proposed manuscript text](manuscript-text.md) and [primary references](references.md).
* [Finite macro model](logical_model.py), [reproduction script](reproduce.py), and [validation script](validate.py).
* [Reused Poisson data and cost table](reused-poisson-costs.csv), [full finite models](poisson-models.json), and [validation results](validation.json).
* [Current task-02 application conversion](application-input.json) and [input hashes](input-versions.json).

The conservative finite construction includes its extra logarithmic success overhead; its polynomial degrees are sufficient analytic choices, not optimized QETU phase results. Null compiled costs are unresolved, not zero.

Reproduce from the repository root with Python 3.6+ and NumPy/SciPy:

```bash
python paper-revise/results/13-qetu-qlsa/reproduce.py
python paper-revise/results/13-qetu-qlsa/validate.py
```

Validated here with `/tmp/hhl-task03-venv/bin/python`, NumPy 1.19.5 and SciPy 1.5.4. No Slurm sweep is needed: five cases are read from the existing task-03 CSV, and two small inverse-state checks use its original generator. Grid tests passed for three inverse gaps; inverse-state errors at N=9 and 49 were approximately 5.78×10⁻⁴ and 9.43×10⁻⁵, below the diagnostic ε_x=.01. These are FP64 mathematical diagnostics, not an executed fault-tolerant circuit.

The current task-02 β=9, m=127 benchmark has sufficient state allowance 1.42961×10⁻⁵ and matrix allowance about 5.38×10⁻¹¹ for the chosen half-budget. The imported Poisson controls have β=0 and m≤31. A matched variable-conductivity Trotter curve and compiled fragment costs are still needed to produce its finite resources; no existing Poisson measurement is relabeled as that application.

Reviewer support: C1-1, C1-2, C1-5, C1-6, C2-1 and C2-3. Task 05 must supply the scalar-output and success policy; tasks 06–07 need compiled counts and schedules; task 09 must compare matched delivered-output costs. Shared code and previous task deliverables remain unchanged. The report records a legacy second-order ordering issue for task 12 to audit before claiming Strang accuracy.
