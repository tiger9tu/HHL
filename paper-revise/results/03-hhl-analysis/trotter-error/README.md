# Standalone Trotter-error derivation

Final artifact: `../Trotter-error-estimation.pdf`.

The note derives the one-step and repeated first-order operator-error bounds, an exact convergent-series bound on the effective matrix, the condition for one common matrix across all QPE powers, and an explicit step count for a normalized solution-error budget. It includes the original two-case check, a 850-matrix study with 20,400 paired operator/effective-H measurements, five comparison figures, numerical validation diagnostics and a primary reference. The full study protocol, data and Slurm provenance are in [experiments/README.md](experiments/README.md). It does not purport to provide the remaining QPE, synthesis or readout error budgets.

Editable sources: `trotter-error-estimation.tex` and `experiments-section.tex`. Rebuilding aggregates the existing completed experiment shards; it does not launch compute jobs.

Rebuild from the repository root with the recorded tool environments:

```bash
HHL_NUMERICS_PYTHON=/tmp/hhl-task03-venv/bin/python \
HHL_PDF_PYTHON=/tmp/hhl-task03-pdf/bin/python \
HHL_TECTONIC=/tmp/hhl-pdf-tools/tectonic \
bash paper-revise/results/03-hhl-analysis/trotter-error/build.sh
```

Portable defaults are `python3` and `tectonic`; the numerical interpreter requires NumPy/SciPy/Matplotlib, and the PDF interpreter requires PyMuPDF. `numerical-validation.json` records the example checks, and `pdf-validation.json` records the final source/PDF hashes and layout checks.
