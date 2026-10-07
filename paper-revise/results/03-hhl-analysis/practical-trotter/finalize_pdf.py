import hashlib,json
from pathlib import Path
import pymupdf as fitz
P=Path(__file__).resolve().parent
assert 'Overfull' not in (P/'practical-trotter.log').read_text()
d=fitz.open(P/'practical-trotter.pdf');text='\n'.join(p.get_text() for p in d)
assert '??' not in text
for term in ['Application-specific','BCH','References','2606.30738','software']:
    assert term in text,term
for page in d:
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines',[]):
            for s in l['spans']:
                r=fitz.Rect(s['bbox']);assert r.x0>=-1 and r.y0>=-1 and r.x1<=page.rect.width+1 and r.y1<=page.rect.height+1
out=P.parent/'Trotter-error-practical-method.pdf'
d.set_metadata(dict(d.metadata,title='Practical Trotter Error Estimation for HHL',subject='BCH effective-H error and application-specific numerical resource estimation'))
d.save(out,garbage=4,deflate=True)
record=dict(pages=len(d),overfull_boxes=False,unresolved_references=False,text_outside_page=False,pdf_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),section_sha256=hashlib.sha256((P/'method-section.tex').read_bytes()).hexdigest(),bch_check_passed=json.loads((P/'bch-validation.json').read_text())['passed'])
(P/'pdf-validation.json').write_text(json.dumps(record,indent=2)+'\n')
print(out,record)
