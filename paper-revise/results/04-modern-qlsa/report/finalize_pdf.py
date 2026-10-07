"""Validate the typeset report and attach a portable reproduction archive."""
import hashlib
import json
from pathlib import Path
import zipfile
import fitz

HERE=Path(__file__).resolve().parent
BASE=HERE.parent.parent
pdf=HERE/'modern-qlsa-t-count.pdf'
log=(HERE/'modern-qlsa-t-count.log').read_text()
assert 'Overfull' not in log, 'Typesetting overflow'
assert 'undefined references' not in log and 'undefined on input line' not in log
files=[p for p in HERE.iterdir() if p.suffix in {'.py','.tex','.json','.csv','.md','.sh'} and p.name!='pdf-validation.json']
files.extend([HERE.parent/'t_count.py',HERE.parent/'t-count-model.md',BASE/'02-application/instance.json'])
# Source PDFs/HTML are not redistributed. Their hashes remain in input-manifest.
archive=HERE/'reproduction.zip'
with zipfile.ZipFile(str(archive),'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(files):
        z.write(str(p),str(p.relative_to(BASE)))
doc=fitz.open(str(pdf))
full='\n'.join(page.get_text() for page in doc)
assert '??' not in full, 'Unresolved reference in PDF'
assert '86721425529887187200' in full and '1939962858931170627439820' in full
outside=[]
for i,page in enumerate(doc):
    for w in page.get_text('words'):
        if not (0<=w[0]<=w[2]<=page.rect.width+0.5 and 0<=w[1]<=w[3]<=page.rect.height+0.5):
            outside.append([i+1,list(w[:5])])
assert not outside, str(outside)
doc.set_metadata(dict(title='Finite T-Gate Upper Bounds for a Modern Quantum Linear-System Solver',
                      author='HHL paper revision',subject='Sufficient logical T count; normalized solution state; explicit error and abort bounds',
                      keywords='QLSA; Shortcut; block encoding; T count; upper bound'))
doc.embfile_add('reproduction.zip',archive.read_bytes(),filename='reproduction.zip',desc='Estimator, report source, inputs, outputs, tests and build scripts')
final=HERE.parent/'Modern-QLSA-T-count-report.pdf'
if final.exists():final.unlink()
doc.save(str(final),garbage=4,deflate=True)
pages=len(doc)
preview=HERE/'preview.png'
doc[0].get_pixmap(matrix=fitz.Matrix(1.15,1.15)).save(str(preview))
doc.close()
record=dict(result='passed',pages=pages,checks=['no unresolved references','no overfull TeX boxes','all words within page bounds','both exact example counts present','embedded reproduction ZIP'],
            pdf_sha256=hashlib.sha256(final.read_bytes()).hexdigest(),archive_sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),
            pdf=str(final.relative_to(BASE)),pymupdf=fitz.VersionBind)
(HERE/'pdf-validation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
