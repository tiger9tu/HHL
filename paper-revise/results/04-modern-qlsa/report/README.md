# Finite modern-QLSA T-gate upper bound

[Read the paper-ready PDF](../Modern-QLSA-T-count-report.pdf) or edit [the LaTeX source](modern-qlsa-t-count.tex).

`upper_bound.py:f(p)` returns an exact **integer sufficient T-gate cap**, including block encoding, RHS preparation, controls, filter overhead, solver retries and heralded rotation-synthesis retries. Conditioned on success, the output ensemble is within `epsilon_state` trace distance of the normalized solution state; overall abort probability is at most `delta`. It is a conservative construction, not the minimum required count or a practical forecast.

```python
from upper_bound import f, estimate
p = {"N": 1024, "kappa": 100,
     "epsilon_state": "0.01", "delta": "0.01"}
assert f(p) == 86721425529887187200
print(estimate(p))
```

From this directory, run `python3 upper_bound.py input.json` for a complete JSON breakdown. The estimator uses only Python's standard library (tested on Python 3.6 and 3.11). Rational strings are supported and all scheduling arithmetic is exact. `N` and `kappa` are required. Optional `rho_upper` supplies a certified Frobenius/spectral ratio bound; optional `effective_inverse_gap` instead supplies a direct certified Frobenius-normalized inverse gap. These two options are mutually exclusive. The default ratio is the rational upper bound `2**ceil(ceil(log2(N))/2)` on `sqrt(D)`, where D is the padded dimension. Parameters must satisfy the report's matrix promises; the program cannot verify a supplied spectral certificate without the matrix.

The mathematical guarantee assumes ideal logical operations, clean ancillas, and certified classical angle/phase preprocessing. It covers arbitrary real nonsingular matrices with nonsingular padding. It excludes classical preprocessing/storage, scientific output extraction, and QEC. The diffusion example uses the task-02 matrix but does not deliver its signed scalar observable. The report proves the conservative synthesis construction and finite sampling/error bounds; no full QLSA circuit has been compiled.

`reproduce.py` regenerates the inputs, JSON outputs, 24-row sensitivity CSV, LaTeX numerical fragments, input/source hashes and component validation. NumPy is needed for its small state simulations; the estimator itself does not require it. `validation.json` records the checks. Tests supplement the proof and do not establish a universal bound by sampling.

To build and package the report, install NumPy, PyMuPDF and Tectonic, then run `bash build.sh`. Optional environment variables select executables:

```sh
HHL_NUMERICS_PYTHON=/path/to/python-with-numpy \
HHL_PDF_PYTHON=/path/to/python-with-pymupdf \
HHL_TECTONIC=/path/to/tectonic bash build.sh
```

The PDF has an embedded reproduction ZIP, also saved as `reproduction.zip`. `pdf-validation.json` records layout/reference checks and final artifact hashes. Source papers are cited and hashed but not redistributed inside the ZIP. Reproduction of the diffusion example from the repository reads `../../02-application/instance.json`; the ZIP preserves the corresponding directory structure. Build from the extracted `04-modern-qlsa/report` directory.

The earlier `../t_count.py` is preserved as a separate heuristic expected-cost model. Its output is not this sufficient cap. The new report is the current upper-bound deliverable for task 04. Downstream task 05 supplies the output/error contract, task 06 QEC scheduling, and later tasks physical comparisons.
