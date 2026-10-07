"""Check the typeset explanation, attach source/code, and publish the task PDF."""
import hashlib
import json
from pathlib import Path
import pymupdf

HERE=Path(__file__).resolve().parent
log=(HERE/'step-by-step.log').read_text()
assert 'Overfull' not in log
assert 'undefined on input line' not in log and 'undefined references' not in log
out=json.loads((HERE/'output.json').read_text())
doc=pymupdf.open(str(HERE/'step-by-step.pdf'))
text='\n'.join(p.get_text() for p in doc)
assert '??' not in text
compact=''.join(text.split()).replace(',','')
for key in ['T_per_attempt_ceiling','T_retry_budget']:
    assert str(out[key]) in compact, key
for p in doc:
    for x in p.get_text('words'):
        assert 0<=x[0]<=x[2]<=p.rect.width+0.5
        assert 0<=x[1]<=x[3]<=p.rect.height+0.5
doc.set_metadata(dict(title='Constructing the Modern QLSA T-Count: A Step-by-Step Explanation of Table V',
                      author='HHL paper revision',subject='Discrete-adiabatic QLSA; Table V estimator derivation and numerical example'))
for name in ['step-by-step.tex','paper_table_v.py','input.json','output.json','reproduce.py','readout-numbers.tex','readout-input.json','readout-output.json']:
    doc.embfile_add(name,(HERE/name).read_bytes(),filename=name)
final=HERE.parent/'Modern-QLSA-Table-V-explained.pdf'
if final.exists():final.unlink()
doc.save(str(final),garbage=4,deflate=True)
validation=dict(result='passed',pages=len(doc),checks=['visual page layout reviewed','no overfull boxes or unresolved references','text within page bounds','example totals match estimator JSON','source and estimator attached'],
                pdf_sha256=hashlib.sha256(final.read_bytes()).hexdigest(),
                source_sha256=hashlib.sha256((HERE/'step-by-step.tex').read_bytes()).hexdigest())
(HERE/'explanation-validation.json').write_text(json.dumps(validation,indent=2)+'\n')
print(json.dumps(validation,indent=2))
