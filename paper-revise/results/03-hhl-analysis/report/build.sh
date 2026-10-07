#!/usr/bin/env bash
set -euo pipefail
report_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
plot_python=${HHL_PLOT_PYTHON:-python3}
pdf_python=${HHL_PDF_PYTHON:-python3}
tectonic_cmd=${HHL_TECTONIC:-tectonic}
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
"$plot_python" "$report_dir/validate_completed_proof.py"
"$plot_python" "$report_dir/completed_schedule.py"
"$plot_python" "$report_dir/make_figures.py"
"$tectonic_cmd" -X compile "$report_dir/hhl-logical-scaling.tex" --keep-logs
"$pdf_python" "$report_dir/finalize_pdf.py"
