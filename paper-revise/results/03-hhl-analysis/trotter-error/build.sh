#!/usr/bin/env bash
set -euo pipefail
note_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
numerics_python=${HHL_NUMERICS_PYTHON:-python3}
pdf_python=${HHL_PDF_PYTHON:-python3}
tectonic_cmd=${HHL_TECTONIC:-tectonic}
export OPENBLAS_NUM_THREADS=1
"$numerics_python" "$note_dir/validate_numerics.py"
"$numerics_python" "$note_dir/experiments/analyze_results.py"
"$numerics_python" "$note_dir/experiments/write_findings.py"
"$tectonic_cmd" -X compile "$note_dir/trotter-error-estimation.tex" --keep-logs
"$pdf_python" "$note_dir/finalize_pdf.py"
