#!/usr/bin/env bash
set -euo pipefail
note_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
export OPENBLAS_NUM_THREADS=1
"${HHL_NUMERICS_PYTHON:-python3}" "$note_dir/check_bch.py"
"${HHL_TECTONIC:-tectonic}" -X compile "$note_dir/practical-trotter.tex" --keep-logs
"${HHL_PDF_PYTHON:-python3}" "$note_dir/finalize_pdf.py"
