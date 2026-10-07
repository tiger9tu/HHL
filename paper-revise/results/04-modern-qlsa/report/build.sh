#!/usr/bin/env bash
set -euo pipefail
report_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
numerics_python=${HHL_NUMERICS_PYTHON:-python3}
pdf_python=${HHL_PDF_PYTHON:-python3}
tectonic_cmd=${HHL_TECTONIC:-tectonic}
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
"$numerics_python" "$report_dir/reproduce.py"
"$tectonic_cmd" -X compile --keep-logs "$report_dir/modern-qlsa-t-count.tex"
"$pdf_python" "$report_dir/finalize_pdf.py"
