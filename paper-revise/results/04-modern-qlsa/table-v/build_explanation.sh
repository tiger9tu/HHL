#!/usr/bin/env bash
set -euo pipefail
report_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
python_cmd=${HHL_PYTHON:-python3.11}
pdf_python=${HHL_PDF_PYTHON:-$python_cmd}
tectonic_cmd=${HHL_TECTONIC:-tectonic}
"$python_cmd" "$report_dir/reproduce.py"
"$tectonic_cmd" -X compile --keep-logs "$report_dir/step-by-step.tex"
"$pdf_python" "$report_dir/finalize_explanation.py"
