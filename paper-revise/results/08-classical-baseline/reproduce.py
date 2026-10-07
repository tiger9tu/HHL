"""Reproduce analytical outputs and validation; does not run HPCG or a solver."""
import csv,hashlib,json,math,platform,subprocess,sys
from pathlib import Path
from cg_hpcg import paper_count,project
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def dump(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')
hw=json.loads((HERE/'hardware.json').read_text())
i=json.loads((HERE/'model-input.json').read_text())
c=paper_count(i['N'],i['kappa'],i['s'],i['epsilon'],i['rounding'])
dump('model-output.json',dict(logical=c,physical=[project(c,h) for h in hw['profiles']]))
checks=[]
# Known hand-computable case kappa=2, epsilon=2/e^2 -> paper iterations=2.
a=paper_count(100,2,5,2/math.exp(2),'paper')
assert math.isclose(a['iterations_paper'],2,rel_tol=1e-14)
assert math.isclose(a['nflops'],6800,rel_tol=1e-14)
for N in (1,10,1024,2**40):
 for s in (1,min(5,N)):
  a=paper_count(N,100,s,.001)
  assert a['nflops']==a['iterations_ceiled']*(4*N*s+14*N)
  assert a['nflops']>=a['nflops_paper'] and a['nflops']-a['nflops_paper']<a['flops_per_iteration']
checks+=['paper D1 hand-computable example','integer count and rounding error less than one iteration']
fake=dict(id='unit',hpcg_pflop_s=2,power_kW=3)
r=project(dict(nflops=4e15,N=1),fake)
assert r['core_time_s']==2 and r['core_energy_J']==6000
assert project(c,hw['profiles'][0],.5)['core_time_s']==2*project(c,hw['profiles'][0])['core_time_s']
assert project(c,hw['profiles'][0],power_multiplier=2)['core_energy_J']==2*project(c,hw['profiles'][0])['core_energy_J']
assert project(c,hw['profiles'][0],memory_limit_bytes=1)['capacity_status']=='infeasible_even_one_vector'
checks+=['PFLOP/s -> FLOP/s','kW -> W and J -> kWh','rate/power sensitivity','capacity lower-bound rejection']
invalid=[(0,10,1,.1), (10,.5,1,.1),(10,10,11,.1),(10,10,1,0),(10,10,1,1),(10,float('nan'),1,.1),(True,1,1,.1)]
for x in invalid:
 try:paper_count(*x)
 except ValueError: pass
 else:raise AssertionError(x)
checks.append('seven invalid-input rejections')
rows=[]
for h in hw['profiles']:
 for N in (2**20,2**30,2**40,2**100):
  a=paper_count(N,100,5,.001)
  r=project(a,h)
  rows.append(dict(N=N,kappa=100,s=5,epsilon=.001,nflops=a['nflops'],**r))
with (HERE/'scaling.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
rows=[]
for h in hw['profiles']:
 for rate in (.25,.5,1.,2.):
  for power in (.7,1.,1.3):
   rows.append(project(c,h,rate,power))
with (HERE/'sensitivity.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
# Reference-normalized hardware table independent of any problem-size feasibility.
tex=[]
for h in hw['profiles']:
 r=project(dict(nflops=10**18,N=1),h)
 tex.append('%s & %.3f & %.3f & %.3f & %.3f \\\\'%(h['name'],h['hpcg_pflop_s'],h['power_kW']/1000,r['core_time_s'],r['core_energy_kWh']))
(HERE/'report/hardware-table.tex').write_text(r'\begin{tabular}{lrrrr}\toprule System & HPCG (PF/s) & Power (MW) & Time (s) & Energy (kWh) \\\midrule'+'\n'+'\n'.join(tex)+'\n'+r'\bottomrule\end{tabular}'+'\n')
# Task-02 conversion is analytical and conditional on the paper error claim.
m=127; beta=9; N=m*m; h=1/(m+1); eps_out=1e-4
lam0=8/h**2*math.sin(math.pi*h/2)**2
F=3*(1+beta)+9*beta/16
kap=(1+beta)/math.tan(math.pi*h/2)**2
eps_d1=(eps_out/4)*lam0/(h*h*N*F)
mesh=5*(2*h*h-h**4)/144+beta*h**4*N*(4/27)/lam0
assert mesh<=eps_out/4
adapter=paper_count(N,kap,5,eps_d1)
dump('task02-adapter.json',dict(instance_id='02-smooth-diffusion-v1:m127:beta9:epsilon0.0001',
    original_kappa_status='unknown; using task-02 upper bound as scenario',
    m=m,beta=beta,epsilon_out=eps_out,epsilon_algebraic=eps_out/4,lambda0=lam0,
    source_bound_F=F,mesh_bound=mesh,mesh_admissible=True,logical=adapter,
    setup_status='generation from compact host description not costed by D1',
    output_status='continuum J=5/144; known answer; no unrestricted advantage',
    accuracy_status='conditional analytical conversion; paper convergence claim and FP64 certification not validated'))
checks.append('task-02 mesh admissibility and separate output/solver tolerance')
# Source manifest captures the current prompt and inputs, excluding historical archive.
paths=[ROOT/'paper-revise/prompts/tasks/08-classical-baseline.md',ROOT/'paper-revise/prompts/tasks/README.md',ROOT/'paper-revise/prompts/paper-revise.md',ROOT/'paper-revise/results/01-framework/interface.md',ROOT/'paper-revise/results/01-framework/interface.schema.json',ROOT/'paper-revise/results/02-application/specification.md',ROOT/'paper-revise/results/02-application/benchmark-pp.json',ROOT/'tools/heatmap.ipynb']
paths+=list((ROOT/'paper').glob('*.pdf'))+list((ROOT/'paper-revise/docs').glob('*.pdf'))
paths+=list((HERE/'sources').glob('*'))+list(HERE.glob('*.py'))+list(HERE.glob('*.md'))+[HERE/'hardware.json',HERE/'model-input.json']+list((HERE/'report').glob('*.tex'))
dump('input-versions.json',dict(git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip(),sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()},missing_handoffs=['05-input-output','07-hardware-energy']))
dump('validation.json',dict(status='passed',checks=checks,python=platform.python_version(),scaling_rows=16,sensitivity_rows=48,solver_executed=False,HPCG_executed=False,accuracy_certificate_validated=False))
print('Passed analytical/unit checks; wrote 16 scaling and 48 sensitivity scenarios.')
