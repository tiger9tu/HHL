"""Validate the compiled report and attach a reproducibility archive to the final PDF."""
import hashlib,io,json,zipfile
from pathlib import Path
import pymupdf as fitz
HERE=Path(__file__).resolve().parent
DATA=HERE.parent
source=HERE/'hhl-logical-scaling.pdf'
output=DATA/'HHL-logical-scaling-analysis.pdf'
doc=fitz.open(source)
text='\n'.join(page.get_text() for page in doc)
assert '??' not in text, 'Unresolved cross-reference'
assert len(doc)>=15
for expected in ['3,880','485','417852','Postselection','Reproduction']:
    assert expected in text,expected
for number in range(1,8):
    assert 'Figure %d:'%number in text,'Missing figure caption %d'%number
log=(HERE/'hhl-logical-scaling.log').read_text()
assert 'Overfull' not in log,'Typesetting overflow must be resolved before publication'
outside=[]
for i,page in enumerate(doc):
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                rect=fitz.Rect(span['bbox'])
                if rect.x0 < -1 or rect.y0 < -1 or rect.x1 > page.rect.width+1 or rect.y1 > page.rect.height+1:
                    outside.append([i+1,span['text']])
assert not outside,outside
files=[]
for pattern in ['*.py','*.csv','*.json','*.md','requirements-tested.txt']:
    files.extend(DATA.glob(pattern))
files.extend([DATA/'figure9.pdf'])
for pattern in ['*.py','*.tex','*.sh','*.csv','completed-*.json','README.md']:
    files.extend(HERE.glob(pattern))
files.extend((HERE/'figures').glob('*.pdf'))
schema=DATA.parent/'01-framework/interface.schema.json'
files.append(schema)
files=sorted(set(p for p in files if p.is_file()))
archive=io.BytesIO()
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
    for p in files:
        name=str(p.relative_to(DATA.parent))
        zi=zipfile.ZipInfo(name,date_time=(2026,9,9,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(zi,p.read_bytes())
doc.embfile_add('hhl-logical-scaling-reproducibility.zip',archive.getvalue(),filename='hhl-logical-scaling-reproducibility.zip',desc='Archived data, scripts, source, figures and the task-01 schema; see report Appendix B.')
doc.set_metadata(dict(doc.metadata,title='HHL Logical Scaling Analysis',subject='Corrected derivations, logical resources, and numerical validation',author='HHL paper revision — Task 03',keywords='HHL; product formula; commutator bound; phase estimation; logical resources'))
doc.save(output,garbage=4,deflate=True)
check=fitz.open(output)
assert len(check)==len(doc) and check.embfile_count()==1
assert hashlib.sha256(check.embfile_get(0)).digest()==hashlib.sha256(archive.getvalue()).digest()
validation={'pages':len(check),'figure_captions':7,'embedded_archives':check.embfile_count(),'embedded_files':len(files),'unresolved_references':False,'overfull_boxes':False,'text_outside_page':outside,'pdf_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'source_sha256':{str(p.relative_to(DATA.parent)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files},'pdf_engine':'Tectonic 0.17.0','pdf_postprocessor':'PyMuPDF '+fitz.VersionBind}
(HERE/'pdf-validation.json').write_text(json.dumps(validation,indent=2)+'\n')
print('Wrote %s (%d pages, seven figures, %d embedded source/data files)'%(output,len(check),len(files)))
