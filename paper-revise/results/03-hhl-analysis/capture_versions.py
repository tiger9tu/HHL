"""Capture the exact upstream contract and local deliverable versions."""
import hashlib,json,platform,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
paths=list((OUT.parent/'01-framework').glob('*.md'))+list((OUT.parent/'01-framework').glob('*.json'))+list((ROOT/'paper-revise/prompts/tasks').glob('*.md'))
paths+=list(OUT.glob('*.py'))+list(OUT.glob('*.md'))+list(OUT.glob('*.csv'))+[OUT/'requirements-tested.txt']
obj={'git_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip(),'date_utc':'2026-09-08','task01_contract':'1.0.0','task02_results_present':(OUT.parent/'02-application').exists(),'python':platform.python_version(),'sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}}
(OUT/'input-versions.json').write_text(json.dumps(obj,indent=2)+'\n')
print('Captured %d files; task02 results present: %s'%(len(obj['sha256']),obj['task02_results_present']))
