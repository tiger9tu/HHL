#!/usr/bin/env python3
"""Build a four-page introduction. Requires Python 3.11 and reportlab 4.4.3.
Example: PYTHONPATH=/tmp/hhl-pdf-deps python3.11 build_intro_pdf.py
"""
from pathlib import Path
import reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
OUT = HERE / 'framework-introduction.pdf'
fonts = Path('/usr/share/fonts/truetype')
for name, file in [('IntroSans','LiberationSans-Regular.ttf'),('IntroSansBold','LiberationSans-Bold.ttf'),('IntroSansItalic','LiberationSans-Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(fonts/file)))
pdfmetrics.registerFontFamily('IntroSans', normal='IntroSans', bold='IntroSansBold', italic='IntroSansItalic', boldItalic='IntroSansBold')
W,H=595.28,841.89
LEFT,RIGHT=46,549.28
WIDTH=RIGHT-LEFT
NAVY=HexColor('#142A43'); TEAL=HexColor('#007F83'); BLUE=HexColor('#386AB0')
INK=HexColor('#24384C'); MUTED=HexColor('#607386'); LINE=HexColor('#D5DFE7')
PALE=HexColor('#F1F5F8'); AQUA=HexColor('#EAF6F5')
styles={
 'body':ParagraphStyle('body',fontName='IntroSans',fontSize=10,leading=15,textColor=INK,spaceAfter=0),
 'small':ParagraphStyle('small',fontName='IntroSans',fontSize=8.2,leading=11.8,textColor=MUTED),
 'box':ParagraphStyle('box',fontName='IntroSans',fontSize=8.4,leading=12,textColor=INK,alignment=1),
 'equation':ParagraphStyle('equation',fontName='IntroSans',fontSize=10.5,leading=16,textColor=NAVY),
 'table':ParagraphStyle('table',fontName='IntroSans',fontSize=8.8,leading=12.5,textColor=INK),
 'ref':ParagraphStyle('ref',fontName='IntroSans',fontSize=7.8,leading=10.5,textColor=MUTED),
}
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1)
c.setTitle('A reusable framework for quantum–classical resource comparison')
c.setAuthor('HHL paper revision — framework introduction')
c.setSubject('Task definitions, resource interfaces, operational energy, and symbolic comparison')

def para(text,x,y,width=WIDTH,style='body'):
    p=Paragraph(text,styles[style]); _,height=p.wrap(width,1000)
    assert y-height>47, ('Page overflow',text[:50],y,height)
    p.drawOn(c,x,y-height)
    return y-height

def heading(title,y):
    c.setFillColor(NAVY);c.setFont('IntroSansBold',12.5);c.drawString(LEFT,y-14,title)
    return y-25

def page(num,kicker,title,subtitle):
    c.setFillColor(TEAL);c.rect(0,H-8,W,8,fill=1,stroke=0)
    c.setFont('IntroSansBold',8);c.setFillColor(TEAL);c.drawString(LEFT,H-42,kicker.upper())
    y=H-63
    title_style=ParagraphStyle('title',fontName='IntroSansBold',fontSize=25,leading=30,textColor=NAVY)
    p=Paragraph(title,title_style);_,height=p.wrap(WIDTH,100);p.drawOn(c,LEFT,y-height);y-=height+12
    y=para(subtitle,LEFT,y,style='small')-18
    c.setStrokeColor(LINE);c.line(LEFT,42,RIGHT,42)
    c.setFont('IntroSans',7.4);c.setFillColor(MUTED)
    c.drawString(LEFT,28,'HHL  /  Framework v1.0.0  /  9 September 2026')
    c.drawRightString(RIGHT,28,f'{num} / 4')
    return y

def equation(text,y):
    p=Paragraph(text,styles['equation']);_,h=p.wrap(WIDTH-24,1000)
    c.setFillColor(PALE);c.roundRect(LEFT,y-h-18,WIDTH,h+18,5,fill=1,stroke=0)
    para(text,LEFT+12,y-9,WIDTH-24,'equation')
    return y-h-29

def table(rows,widths,y):
    content=[[Paragraph(x,styles['table']) for x in row] for row in rows]
    t=Table(content,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),AQUA),('LINEBELOW',(0,0),(-1,0),0.6,TEAL),('LINEBELOW',(0,1),(-1,-1),0.4,LINE),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    _,h=t.wrap(WIDTH,1000);assert y-h>50;t.drawOn(c,LEFT,y-h)
    return y-h-17

def box(x,top,w,h,title,body,color=TEAL):
    c.setFillColor(white);c.setStrokeColor(LINE);c.roundRect(x,top-h,w,h,6,fill=1,stroke=1)
    c.setFillColor(color);c.rect(x+1,top-h+7,3,h-14,fill=1,stroke=0)
    para('<b>'+title+'</b><br/>'+body,x+10,top-9,w-20,'box')

def arrow(x1,y1,x2,y2,color=TEAL):
    import math
    c.setStrokeColor(color);c.setFillColor(color);c.setLineWidth(1)
    c.line(x1,y1,x2,y2)
    a=math.atan2(y2-y1,x2-x1);s=4
    p=c.beginPath();p.moveTo(x2,y2);p.lineTo(x2-s*math.cos(a-.5),y2-s*math.sin(a-.5));p.lineTo(x2-s*math.cos(a+.5),y2-s*math.sin(a+.5));p.close();c.drawPath(p,fill=1,stroke=0)

# PAGE 1
Y=page(1,'Overview','Compare the same answer,<br/>across the full computation.','A reusable framework for time, space and operational energy — with linear-system solvers as case studies.')
Y=para('The framework connects algorithmic work to physical execution through explicit interfaces. HHL, a modern quantum linear-system algorithm, and an eligible classical solver can each be evaluated against one shared task. The result is a conditional resource comparison, with feasibility and uncertainty attached.',LEFT,Y)-18
# Fixed vector workflow, with a visibly separate host bypass.
top=Y
box(LEFT,top,WIDTH,49,'Shared task · pp','Input and access model · requested output · accuracy and success · reuse')
branchTop=top-77
qX,qW=LEFT,286
cX,cW=LEFT+306,WIDTH-306
para('<b>QUANTUM CONFIGURATION · cq</b>',qX,branchTop+14,qW,'small')
para('<b>CLASSICAL CONFIGURATION · cc</b>',cX,branchTop+14,cW,'small')
box(qX,branchTop,qW,49,'Logical algorithm','Gates · queries · depth · logical qubits')
box(cX,branchTop,cW,119,'Classical workload + I/O','Operations by precision<br/>Memory capacity and traffic<br/>Synchronization<br/>Preprocessing and output',BLUE)
arrow(qX+qW-8,top-49,qX+qW-8,branchTop)
arrow(cX+cW-8,top-49,cX+cW-8,branchTop,BLUE)
box(qX,branchTop-70,qW,49,'Input / output composition','Preparation · oracle expansion · readout · repetitions')
arrow(qX+qW/2,branchTop-49,qX+qW/2,branchTop-70)
box(qX,branchTop-146,168,63,'QEC schedule','Physical qubits<br/>Syndrome code cycles')
box(qX+181,branchTop-146,105,63,'Host work','Operations<br/>Bytes moved')
arrow(qX+80,branchTop-119,qX+80,branchTop-146)
arrow(qX+230,branchTop-119,qX+230,branchTop-146)
box(qX,branchTop-238,qW,53,'Quantum hardware + host','Schedule · cycle duration · attributed power')
arrow(qX+80,branchTop-209,qX+80,branchTop-238)
arrow(qX+230,branchTop-209,qX+230,branchTop-238)
box(cX,branchTop-238,cW,53,'Classical hardware','Schedule · throughput<br/>Bandwidth · attributed power',BLUE)
arrow(cX+cW/2,branchTop-119,cX+cW/2,branchTop-238,BLUE)
para('work counts / bytes',cX+7,branchTop-179,cW-14,'small')
box(LEFT,branchTop-320,WIDTH,48,'Compare feasible configurations','Seconds · typed peak space · joules · uncertainty')
arrow(qX+qW/2,branchTop-291,qX+qW/2,branchTop-320)
arrow(cX+cW/2,branchTop-291,cX+cW/2,branchTop-320,BLUE)
Y=branchTop-382
para('QEC = quantum error correction. Host processing bypasses QEC and joins physical scheduling. Every branch includes the costs needed to make the requested output available.',LEFT,Y,style='small')
c.showPage()

# PAGE 2
Y=page(2,'Model interfaces','Three inputs. Explicit contracts.','Keep the problem, algorithmic work and hardware performance separately identifiable.')
Y=table([
 ['<b>Input</b>','<b>What it specifies</b>'],
 ['<b>pp</b><br/>Problem parameters','Original matrix dimension N, matrix class, row/column sparsity and condition number κ; input representation and location; right-hand side; output, accuracy, success and reuse. No scaling relation between N, κ and sparsity is implicit.'],
 ['<b>cq</b><br/>Quantum configuration','Algorithm, compilation and synthesis, input/output protocol, precision, error correction, factories, device and host hardware, limits and optimization policy.'],
 ['<b>cc</b><br/>Classical configuration','Solver and preconditioner, precision, input/output protocol, node and accelerator configuration, memory, network, limits and optimization policy.'],
 ],[108,WIDTH-108],Y)
Y=equation('F<sub>q</sub>(pp, cq), F<sub>c</sub>(pp, cc) → (time, space, energy, feasibility, uncertainty)',Y)
Y=heading('What each model hands to the next',Y)
Y=table([
 ['<b>Layer</b>','<b>Resource contract and units</b>'],
 ['Logical quantum','Gate counts in an exclusive basis; diagnostic oracle queries; depth in layers; peak logical qubits per invocation.'],
 ['Input / output','Complete executable workload: preparation, implemented oracles, measurements, resets, repetition counts and host work.'],
 ['Fault tolerance','Scheduled syndrome-extraction cycles and peak physical qubits, including factories, storage, routing and stalls; achieved workload failure bound.'],
 ['Classical work','Operation counts by kind and precision; peak memory in bytes; traffic in bytes per named interface; synchronization.'],
 ['Physical execution','Makespan in seconds; energy in joules; peak capacity by resource type; feasibility against hardware limits.'],
 ],[108,WIDTH-108],Y)
Y=heading('Composition without double counting',Y)
para('Each cost has one owner and a declared scope: setup, per output or batch. Apply repetition once. After an oracle is expanded into gates, its query count is diagnostic. After QEC produces a total cycle count, its repetition and code-distance factors are already included. Derivation links describe transformations, not extra costs to add.',LEFT,Y)
c.showPage()

# PAGE 3
Y=page(3,'Comparison rules','Make the assumptions visible.','A resource estimate is meaningful only together with its output contract, schedule and system boundary.')
Y=heading('01  Match the requested output and its reliability',Y)
Y=para('A classical solution vector, a normalized quantum state and a scalar observable are different deliverables. Specify one output y = f(x), its error metric and the probability of meeting it. Convert local state, residual or approximation errors to that output metric before combining them.',LEFT,Y)-10
Y=equation('Pr[d<sub>out</sub>(ŷ, f(x)) ≤ ε<sub>out</sub>] ≥ 1 − δ<sub>total</sub>',Y)
Y=heading('02  Charge setup and reuse consistently',Y)
Y=para('Include required preprocessing, loading, oracle construction, factorization, preparation and extraction. Reuse setup only while its inputs remain valid. For B sequential outputs sharing one setup, amortized time or energy equals the batch total divided by B. Report first-output latency separately; peak memory and qubit capacity are never divided by B.',LEFT,Y)-16
Y=heading('03  Separate work counts from elapsed time',Y)
Y=para('Circuit depth, gate count and physical cycle count carry different meanings. Classical instruction counts also require a throughput, memory and synchronization model. Schedules determine overlap and peak occupancy. A T count alone does not fix runtime; processor frequency does not specify sustained floating-point performance. [2, 3]',LEFT,Y)-16
Y=heading('04  Use a common operational energy boundary',Y)
Y=equation('E = ∫ P<sub>attributed</sub>(t) dt &nbsp;&nbsp; [joules]',Y)
Y=para('Include the attributed electrical cost of quantum cooling, control, decoding and hosts, or classical compute, memory and networking, plus consistently allocated facility overhead. Power in W/qubit is a model parameter. Do not add cooling or facility factors to measurements that already include them. Declare gross or incremental energy; embodied energy is a separate metric.',LEFT,Y)-16
Y=heading('05  Propagate uncertainty through the whole pipeline',Y)
Y=para('Vary correlated inputs together, including conditioning, success probability, hardware errors, bandwidth and power. Recompute scheduling, QEC choices and feasibility under a declared fixed or reoptimized configuration policy. Keep unsupported assumptions distinct from measurements and rigorous bounds.',LEFT,Y)-14
para('<b>Interpretation:</b> compare seconds and joules for the same workload and statistic. Report space as a vector of qubits and memory bytes. An advantage region requires both machines to be feasible and the uncertainty to support the comparison.',LEFT,Y)
c.showPage()

# PAGE 4
Y=page(4,'Symbolic example','From one observable to resource cost.','An accounting illustration only: no hardware constants or numerical crossover are assumed.')
Y=para('Let μ = &lt;x|O|x&gt; for normalized |x&gt;, with Hermitian O and outcomes in [−1, 1]. If each prepared state has trace-distance error at most η, the observable bias is at most 2η. Choose 2η + ε<sub>stat</sub> ≤ ε<sub>out</sub>. Independent accepted samples obey the Hoeffding bound [1, 4]:',LEFT,Y)-9
Y=equation('M ≥ ceil[2 ε<sub>stat</sub><super>−2</super> ln(2/δ<sub>stat</sub>)]',Y)
Y=para('A trial resets and prepares the input, runs the solver and checks a success flag; let its gate vector be g<sub>try</sub>. Each success adds observable readout and cleanup g<sub>obs</sub>. For independent trials with constant success probability p &gt; 0, an uncapped run needs M/p trials in expectation:',LEFT,Y)-9
Y=equation('E[G] = (M/p) g<sub>try</sub> + M g<sub>obs</sub>',Y)
Y=para('A deadline guarantee instead needs an attempt cap K with Pr[Binomial(K, p) &lt; M] ≤ δ<sub>retry</sub>. Reserve K trials and M readouts. If c<sub>try</sub> and c<sub>obs</sub> include all QEC cycles and stalls, and τ<sub>cyc</sub> is seconds per cycle, a serialized upper bound is:',LEFT,Y)-9
Y=equation('t<sub>q</sub><super>ub</super> = t<sub>q,setup</sub> + τ<sub>cyc</sub>(K c<sub>try</sub> + M c<sub>obs</sub>) + t<sub>q,host</sub><br/>δ<sub>stat</sub> + δ<sub>retry</sub> + δ<sub>qec</sub> + δ<sub>other</sub> ≤ δ<sub>total</sub>',Y)
Y=para('For a classical solver of the same μ, let k iterations each require F<sub>it</sub> operations and V<sub>it</sub> bytes at a named interface. With sustained rates f<sub>eff</sub> and b<sub>eff</sub>, a deliberately serialized compute/transfer model gives:',LEFT,Y)-9
Y=equation('t<sub>c</sub> = t<sub>c,setup</sub> + k(F<sub>it</sub>/f<sub>eff</sub> + V<sub>it</sub>/b<sub>eff</sub>) + t<sub>c,output</sub>',Y)
Y=para('For constant attributed run power, E = E<sub>setup</sub> + P<sub>run</sub> t<sub>run</sub>. Keep setup outside the run window. Expected costs, reserved upper bounds and measured runtimes must remain clearly labeled when compared.',LEFT,Y)-14
Y=heading('Primary references',Y)
refs=[
 '[1] Harrow, Hassidim &amp; Lloyd (2009). Quantum algorithm for solving linear systems of equations. <link href="https://arxiv.org/abs/0811.3171v3" color="#007F83">arXiv:0811.3171v3</link>.',
 '[2] Litinski (2019). A Game of Surface Codes. <link href="https://arxiv.org/abs/1808.02892v3" color="#007F83">Quantum 3, 128</link>.',
 '[3] Williams, Waterman &amp; Patterson (2009). Roofline. <link href="https://doi.org/10.1145/1498765.1498785" color="#007F83">CACM 52(4), 65–76</link>.',
 '[4] Hoeffding (1963). Probability Inequalities for Sums of Bounded Random Variables. <link href="https://doi.org/10.1080/01621459.1963.10500830" color="#007F83">JASA 58(301), 13–30</link>.',
]
for ref in refs:Y=para(ref,LEFT,Y,style='ref')-4
c.showPage();c.save()
print(OUT)
