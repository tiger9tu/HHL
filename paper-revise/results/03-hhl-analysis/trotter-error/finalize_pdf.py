"""Check and publish the standalone Trotter-error PDF."""
import hashlib,json
from pathlib import Path
import pymupdf as fitz
HERE=Path(__file__).resolve().parent
source=HERE/'trotter-error-estimation.pdf'
target=HERE.parent/'Trotter-error-estimation.pdf'
log=(HERE/'trotter-error-estimation.log').read_text()
study=json.loads((HERE/'experiments/results.json').read_text())
assert study['matrix_cases']==850 and study['measurements']==20400
assert study['operator_violations']==0 and study['effective_matrix_violations']==0
assert 'Overfull' not in log
pdf=fitz.open(source)
text='\n'.join(page.get_text() for page in pdf)
assert '??' not in text
for word in ['Theorem 1','Theorem 2','References','0.1001110486','0.2008868159','20,400','Branch wrapping']:
    assert word in text,word
for page in pdf:
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                r=fitz.Rect(span['bbox'])
                assert r.x0>=-1 and r.y0>=-1 and r.x1<=page.rect.width+1 and r.y1<=page.rect.height+1,span['text']
pdf.set_metadata(dict(pdf.metadata,title='Trotter Error Estimation for HHL',subject='Complete derivations of unitary and effective-matrix Trotter errors',author='HHL paper revision'))
pdf.save(target,garbage=4,deflate=True)
record={'pages':len(pdf),'unresolved_references':False,'overfull_boxes':False,'text_outside_page':False,'pdf_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'tex_sha256':hashlib.sha256((HERE/'trotter-error-estimation.tex').read_bytes()).hexdigest(),'compiler':'Tectonic 0.17.0','numerical_examples_passed':json.loads((HERE/'numerical-validation.json').read_text())['passed']}
record.update(experiment_measurements=study['measurements'],experiment_bound_violations=0,experiment_results_sha256=hashlib.sha256((HERE/'experiments/results.json').read_bytes()).hexdigest(),experiment_section_sha256=hashlib.sha256((HERE/'experiments-section.tex').read_bytes()).hexdigest())
(HERE/'pdf-validation.json').write_text(json.dumps(record,indent=2)+'\n')
print('Created %s (%d pages)'%(target,len(pdf)))
