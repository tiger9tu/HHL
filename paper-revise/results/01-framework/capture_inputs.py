#!/usr/bin/env python3
"""Capture input hashes and regenerate PDF extracts with pypdf 3.17.4."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--pypdf-path', help='Optional directory containing pypdf and dependencies')
args = parser.parse_args()
if args.pypdf_path:
    sys.path.insert(0, args.pypdf_path)
import pypdf
inputs = [ROOT/'paper-revise/prompts/paper-revise.md',
          ROOT/'paper-revise/prompts/tasks/README.md',
          ROOT/'paper-revise/prompts/tasks/01-framework.md',
          ROOT/'tools/surface_code_opt.py', ROOT/'src/HHL/HHL.qs',
          ROOT/'src/test/GateCountTest.qs', ROOT/'num/hhl.m', ROOT/'README.md']
inputs += sorted((ROOT/'paper-revise/docs').glob('*.pdf'))
inputs += sorted((ROOT/'paper').glob('*.pdf'))
extracts = HERE/'source-extracts'
extracts.mkdir(exist_ok=True)
records = []
for path in inputs:
    record = {'path':str(path.relative_to(ROOT)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if path.suffix == '.pdf':
        reader = pypdf.PdfReader(path)
        text = '\n'.join('\n--- PDF page {} ---\n{}'.format(i+1, page.extract_text()) for i,page in enumerate(reader.pages))
        (extracts/(path.stem+'.txt')).write_text(text)
        record['pdf_pages'] = len(reader.pages)
    records.append(record)
manifest = {'captured_date_utc':'2026-09-08',
            'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip(),
            'python':sys.version.split()[0], 'pypdf':pypdf.__version__,
            'command':'python3 paper-revise/results/01-framework/capture_inputs.py --pypdf-path /tmp/hhl-framework-pypdf-3',
            'notes':'Working-tree hashes are authoritative; existing user prompt edits were preserved.',
            'inputs':records}
(HERE/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Captured {} inputs and PDF extracts'.format(len(records)))
