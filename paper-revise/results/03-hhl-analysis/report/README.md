# Single-PDF report

Updated after the request for a complete proof: Section 2 now states and proves the consistent-microstep HHL theorem, including median-QPE accuracy and success. Its leading per-attempt count is proportional to L C_comm kappa^2 / epsilon^2 up to logarithms; independent retries add a worst-case kappa^2 factor. The complete bound retains an additional L(1+B)kappa/epsilon term. The earlier direct-unitary allocation and exported adapter remain clearly marked as a different, more conservative method.

`completed-theorem.tex` contains the new proof. `validate_completed_proof.py` checks its logarithm/perturbation and scalar median-QPE lemmas; `completed_schedule.py` evaluates the exact integer schedule. These do not claim to simulate the full coherent median circuit. New raw checks are attached to the PDF.

The final user-facing artifact is `../HHL-logical-scaling-analysis.pdf`. It contains the complete derivations, seven numbered numerical figures, three data tables, the implementation audit, references, and an embedded ZIP of the raw data and reproduction materials. The attached files supplement the self-contained visible report.

`hhl-logical-scaling.tex` is the editable report. `make_figures.py` only reads existing CSV/JSON results; it does not draw new samples. `finalize_pdf.py` checks cross-references, figure captions, TeX overflow warnings and text boundaries, then embeds the data/source archive. Its result is recorded in `pdf-validation.json`.

Build from any working directory:

```bash
HHL_PLOT_PYTHON=/tmp/hhl-task03-venv/bin/python \
HHL_PDF_PYTHON=/tmp/hhl-task03-pdf/bin/python \
HHL_TECTONIC=/tmp/hhl-pdf-tools/tectonic \
bash paper-revise/results/03-hhl-analysis/report/build.sh
```

The paths above record the actual environment used. The portable defaults are `python3` and `tectonic`. The plotting and proof-check interpreter needs NumPy, SciPy and Matplotlib; the PDF interpreter needs PyMuPDF. Tectonic 0.17.0 obtains its TeX dependencies on the first build. The complete scientific experiments additionally need SciPy; contract export needs jsonschema and the sibling task-01 schema. Restore the attached results directories under the original repository checkout when rerunning scripts that capture Git and source-file provenance.

This report reflows the three original Figure 9 panels into a readable page layout and adds views covering every sampled synthetic configuration, every Poisson evolution configuration, family parameters, full successful-branch HHL error, and PDE conditioning/discretization validation. The new figure views reuse the 8 September archived data.

The report also spells out the two-term integral proof, multi-term telescoping, normalized perturbation and postselection proofs, step-allocation derivation, entry-error and observable-error propagation, explicit Pauli logarithm calculation, and the Poisson spectrum. Finite-QPE certification is now supplied for the new median-QPE construction; different QPE variants and the missing task-02 application/output benchmark are not covered automatically.
