# Task 08 restarted — September 20 prompt

The active deliverable now uses **only the manuscript's CG-family arithmetic model and an HPCG rate/power conversion**. The superseded reports and multi-solver archive have been removed. This directory contains the September 20 CG/HPCG deliverable.

- [September 20 CG/HPCG report PDF](Classical-Baseline-CG-HPCG-2026-09-20.pdf), [report and assumptions](report.md).
- [Executable model](cg_hpcg.py), [input](model-input.json), [output](model-output.json).
- [Published HPCG rates and power proxies](hardware.json), [source audit](sources.md).
- [Replacement manuscript text](manuscript-text.md).
- `scaling.csv`, `sensitivity.csv`, `task02-adapter.json`, `validation.json`, `input-versions.json`, `run.log`.

The extracted paper expression is

\[
n_{\rm FLOPs}^{D1}=\tfrac12\kappa\ln(2/\epsilon)\,(4Ns+14N),\qquad
 t=\frac{n_{\rm FLOPs}}{R_{\rm HPCG}\,10^{15}},\qquad
 E=t\,P_{\rm kW}\,10^3.
\]

`cg_hpcg.py` exports the literal D1 expression and its integer-iteration counterpart; the default uses the latter. These are paper-model FLOPs, not a measured ISA instruction count. Appendix D's recurrence is a normal-equation CG variant despite the manuscript's naming. The report explicitly retains that provenance instead of claiming D1 is ordinary SPD CG.

## Reproduce

Python 3.6+ standard library only, from the repository root:

```sh
python3 paper-revise/results/08-classical-baseline/reproduce.py
python3 paper-revise/results/08-classical-baseline/cg_hpcg.py
python3 paper-revise/results/08-classical-baseline/cg_hpcg.py --rounding paper
```

Edit `model-input.json` for N, kappa, s and epsilon, or pass `--input path.json`. `--rate-multiplier` and `--power-multiplier` expose transfer assumptions; both default to 1. `--memory-limit-bytes` can reject a scenario that cannot store even one vector, but does not certify complete solver memory. The reported time/energy always retain the formal arithmetic conversion; end-to-end fields stay null and capacity-infeasible rows remain explicitly flagged.

Rebuild the PDF after `reproduce.py` with Tectonic:

```sh
tectonic -X compile paper-revise/results/08-classical-baseline/report/cg-hpcg.tex --outdir paper-revise/results/08-classical-baseline/report --keep-logs
mv paper-revise/results/08-classical-baseline/report/cg-hpcg.pdf paper-revise/results/08-classical-baseline/Classical-Baseline-CG-HPCG-2026-09-20.pdf
```

No HPCG benchmark, production solver or power measurement was run. Published HPCG scores are the physical-rate proxy; published TOP500 power values are not verified paired HPCG measurements. This task implements the revised two-step request, but does not establish a matched quantum advantage or full-workload energy result. Task 05/07 handoffs, input/output/setup costs, application-rate calibration and achieved accuracy/reliability remain downstream requirements.
