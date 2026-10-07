# Classical resource model

Following [the framework](../frame.md), the model has two layers:
**problem parameters → floating-point work → runtime and energy**.

## Logical resource

For a real square system, let \(N\) be its dimension, \(s\le N\) the maximum
nonzeros per row/column, \(\kappa\ge1\) the original condition number, and
\(0<\epsilon<1\) the relative solution-error parameter. Appendix D, Eq. (D1)
of [the manuscript](../../paper/Explore_Practical_Quantum_Speedup_for_Quantum_Linear_System_of_Equations%20%281%29.pdf)
uses

\[
K_* = \frac{\kappa}{2}\ln\frac{2}{\epsilon},\qquad
n_{\mathrm{FLOPs}}^{D1}=K_*N(4s+14).
\]

Each modeled iteration contains two sparse matrix-vector products (\(4Ns\)),
three vector updates (\(6N\)), and coefficient calculations (\(8N\)).
The script defaults to \(K=\lceil K_*\rceil\); `--rounding paper` retains
the literal unrounded expression. Both counts are exported.

This is an **analytical FLOP estimate**, not an exact executed instruction
count or a validated finite-precision convergence certificate. The paper
labels its method CGNE; Figure 13's recurrence is CGLS/CGNR (implicit CG on
\(A^TA\)), rather than ordinary SPD CG. We preserve D1 without substituting
the latter's square-root conditioning dependence. The requested output
tolerance must be converted to this solution-error parameter before use.

## Physical hardware

[hardware.json](hardware.json) freezes these November 2025 values:

| System ID | HPCG (PFLOP/s) | System power (kW) |
|---|---:|---:|
| `el_capitan` | 17.41 | 29,685 |
| `fugaku` | 16.00 | 29,899 |
| `frontier` | 14.05 | 24,607 |
| `aurora` | 5.613 | 38,698 |

Rates come from [HPCG SC25](https://www.hpcg-benchmark.org/custom/sc25.html);
power comes from [TOP500 November 2025](https://www.top500.org/lists/top500/2025/11/).
With rate \(R\) in PFLOP/s and power \(P\) in kW,

\[
t_{\mathrm{core}}=\frac{n_{\mathrm{FLOPs}}}{10^{15}R}\ \mathrm{s},\qquad
E_{\mathrm{core}}=10^3P\,t_{\mathrm{core}}\ \mathrm{J}.
\]

HPCG scores already represent aggregate throughput: do not multiply by
core count or fraction of peak. HPCG uses multigrid-preconditioned CG;
transferring its FP64 rate to D1 is a modeling assumption. TOP500 power is
a proxy, not paired HPCG-job power. No PUE multiplier is applied.

These are **solver-core projections**. Setup, input/output, capacity,
small-problem utilization, and facility-energy coverage remain unresolved;
the formula alone does not establish end-to-end or quantum advantage.

## Run

Python 3.6+, standard library only; no dependency on the older task directory:

```sh
python3 paper-revise-clean/classical/model.py \
  --N 1073741824 --kappa 100 --s 5 --epsilon 0.001
```

JSON output contains both logical counts and all four hardware projections.
Use `--system frontier` for one machine, `--rounding paper` for literal D1,
or `--hardware path.json` for another hardware specification with the same
fields. The functions `logical_resources` and `physical_resources` can also
be imported independently.
