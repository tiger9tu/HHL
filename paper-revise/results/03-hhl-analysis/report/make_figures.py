"""Plot the archived measurements; no new numerical experiments are performed."""
import csv,json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent; DATA=HERE.parent
rows=list(csv.DictReader((DATA/'summary.csv').open()))
raw=list(csv.DictReader((DATA/'samples.csv').open()))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})
styles={'fixed_band':('Fixed band','#245e94'),'random_matching':('Random matching','#c46427'),'poisson_2d':('Poisson','#24845b')}
def save(fig,name):
 fig.tight_layout(rect=getattr(fig,'_hhl_rect',(0,0,1,1)));fig.savefig(str(HERE/'figures'/name));plt.close(fig)
def selected(pat,L,t,r=None,N=None):
 return [a for a in rows if a['pattern']==pat and int(a['degree'])==L and float(a['t'])==t and (r is None or int(a['r'])==r) and (N is None or int(a['N'])==N)]
fig,axs=plt.subplots(2,2,figsize=(10,7))
for ax,(L,t) in zip(axs.flat,[(2,.1),(4,.1),(2,1.),(4,1.)]):
 for pat,(label,color) in list(styles.items())[:2]:
  a=sorted(selected(pat,L,t,N=64),key=lambda x:int(x['r']));x=[int(v['r']) for v in a]
  ax.plot(x,[float(v['median']) for v in a],'o-',color=color,label=label)
  ax.fill_between(x,[float(v['q05']) for v in a],[float(v['q95']) for v in a],color=color,alpha=.16)
 ax.set(xscale='log',yscale='log',xlabel='Product-formula steps r',ylabel='Operator error',title='N=64, L=%d, evolution time=%g'%(L,t));ax.set_xticks([1,2,4,8]);ax.set_xticklabels(['1','2','4','8']);ax.legend(fontsize=8)
save(fig,'step_sweeps.pdf')
fig,axs=plt.subplots(2,2,figsize=(10,7))
for ax,(L,t) in zip(axs.flat,[(2,.1),(4,.1),(2,1.),(4,1.)]):
 for pat,(label,color) in list(styles.items())[:2]:
  for r,ls in [(1,'-'),(2,'--'),(4,':'),(8,'-.')]:
   a=sorted(selected(pat,L,t,r=r),key=lambda x:int(x['N']))
   ax.plot([int(v['N']) for v in a],[float(v['median']) for v in a],ls,color=color,label='%s, r=%d'%(label,r))
 ax.set(xscale='log',yscale='log',xlabel='Matrix dimension N',ylabel='Median operator error',title='L=%d, evolution time=%g'%(L,t));pass
handles,labels=axs.flat[0].get_legend_handles_labels()
fig.legend(handles,labels,loc='lower center',ncol=4,fontsize=10,frameon=False)
fig._hhl_rect=(0,.10,1,1)
save(fig,'all_configurations.pdf')
fig,axs=plt.subplots(1,2,figsize=(10,3.9))
for pat,(label,color) in styles.items():
 a=[v for v in raw if v['pattern']==pat and int(v['degree'])==4 and float(v['t'])==1 and int(v['r'])==4]
 ns=sorted(set(int(v['N']) for v in a))
 for ax,key,ylabel in zip(axs,['C_comm','kappa'],['Commutator coefficient C','Spectral condition number']):
  vals=[np.array([float(v[key]) for v in a if int(v['N'])==n]) for n in ns]
  ax.plot(ns,[np.median(v) for v in vals],'o-',color=color,label=label)
  ax.fill_between(ns,[np.quantile(v,.05) for v in vals],[np.quantile(v,.95) for v in vals],color=color,alpha=.16)
  ax.set(xscale='log',yscale='log',xlabel='Matrix dimension N',ylabel=ylabel);ax.legend(fontsize=8)
save(fig,'family_parameters.pdf')
val=json.loads((DATA/'validation.json').read_text())['qpe_validation'];r=[x['r'] for x in val]
fig,axs=plt.subplots(1,2,figsize=(10,3.8))
axs[0].loglog(r,[x['conditioned_state_error'] for x in val],'o-',label='Measured successful-state error')
axs[0].loglog(r,[min(2,x['conditioned_error_bound']) for x in val],'s--',label='Analytic bound, capped at 2')
axs[0].set(xlabel='Steps per controlled evolution r',ylabel='Euclidean state distance');axs[0].legend(fontsize=8)
axs[1].loglog(r,[abs(x['actual_success']-x['ideal_success']) for x in val],'o-',color='#c46427')
axs[1].set(xlabel='Steps per controlled evolution r',ylabel='Absolute success-probability deviation')
save(fig,'hhl_validation.pdf')
pde=list(csv.DictReader((DATA/'pde-validation.csv').open()));n=[int(x['N']) for x in pde];h=np.array([float(x['h']) for x in pde]);err=np.array([float(x['normalized_solution_error']) for x in pde])
fig,axs=plt.subplots(1,2,figsize=(10,3.8))
axs[0].plot(n,[float(x['analytic_kappa']) for x in pde],'-',label='Analytic spectrum')
axs[0].plot(n,[float(x['kappa']) for x in pde],'o',mfc='none',label='Dense eigensolver');axs[0].set(xlabel='Matrix dimension N',ylabel='Condition number');axs[0].legend(fontsize=8)
axs[1].loglog(h,err,'o-',label='Normalized solution error')
axs[1].loglog(h,err[-1]*(h/h[-1])**2,'--',label='h² reference through finest point')
axs[1].set(xlabel='Grid spacing h',ylabel='Euclidean state distance');axs[1].legend(fontsize=8)
save(fig,'pde_validation.pdf')
# Data-driven tables prevent transcribing results or dropping the uncertainty definition.
with (HERE/'numerical_tables.tex').open('w') as f:
 f.write('\\begin{tabular}{rrrr}\\toprule $r$ & State error & Analytic bound & Success probability\\\\\\midrule\n')
 for v in val:f.write('%d & %.7g & %.7g & %.10f\\\\\n'%(v['r'],v['conditioned_state_error'],min(2,v['conditioned_error_bound']),v['actual_success']))
 f.write('\\bottomrule\\end{tabular}\n')
with (HERE/'pde_table.tex').open('w') as f:
 f.write('\\begin{tabular}{rrrr}\\toprule $N$ & $\\kappa_2$ & State error & Relative residual\\\\\\midrule\n')
 for v in pde:f.write('%s & %.7g & %.7g & %.3g\\\\\n'%(v['N'],float(v['kappa']),float(v['normalized_solution_error']),float(v['relative_residual'])))
 f.write('\\bottomrule\\end{tabular}\n')
with (HERE/'uncertainty_table.tex').open('w') as f:
 f.write('\\begin{tabular}{lrrrr}\\toprule Family & $N$ & Mean error & 95\\%% mean CI & Max error\\\\\\midrule\n'.replace('95\\%%','95\\%'))
 for pat in ['fixed_band','random_matching']:
  for v in sorted(selected(pat,4,1.,r=4),key=lambda x:int(x['N'])):
   f.write('%s & %s & %.5f & [%.5f, %.5f] & %.5f\\\\\n'%(styles[pat][0],v['N'],float(v['mean']),float(v['mean_ci_low']),float(v['mean_ci_high']),float(v['maximum'])))
 f.write('\\bottomrule\\end{tabular}\n')
print('Generated main figures and tables from archived CSV/JSON data.')
# All deterministic PDE evolution measurements, distinguished from discretization errors.
fig,axs=plt.subplots(1,2,figsize=(9,3.8))
for ax,t in zip(axs,[.1,1.]):
 for N in [9,25,49,81,121]:
  a=sorted(selected('poisson_2d',4,t,N=N),key=lambda x:int(x['r']))
  ax.loglog([int(v['r']) for v in a],[float(v['median']) for v in a],'o-',label='N=%d'%N)
 ax.set(xlabel='Product-formula steps r',ylabel='Operator error',title='Poisson; evolution time=%g'%t)
 ax.set_xticks([1,2,4,8]);ax.set_xticklabels(['1','2','4','8']);ax.legend(fontsize=8)
save(fig,'pde_evolution_sweeps.pdf')
# Reflow the archived Figure 9 panels to make their labels readable on an A4 page.
fig=plt.figure(figsize=(8,6.5));gs=fig.add_gridspec(2,2);axes=[fig.add_subplot(gs[0,:]),fig.add_subplot(gs[1,0]),fig.add_subplot(gs[1,1])]
for pat,(label,color) in styles.items():
 a=sorted(selected(pat,4,1.,r=4),key=lambda x:int(x['N']));ns=[int(v['N']) for v in a]
 axes[0].plot(ns,[float(v['median']) for v in a],'o-',label=label,color=color)
 axes[0].fill_between(ns,[float(v['q05']) for v in a],[float(v['q95']) for v in a],color=color,alpha=.16)
axes[0].set(xscale='log',yscale='log',xlabel='Matrix dimension N',ylabel='Operator error',title='(a) Evolution time=1, r=4');axes[0].legend(fontsize=9,ncol=3)
comm=list(csv.DictReader((DATA/'commutators.csv').open()))
for pat,(label,color) in list(styles.items())[:2]:
 a=[v for v in raw if v['pattern']==pat and int(v['N'])==64 and int(v['degree'])==4 and float(v['t'])==1 and int(v['r'])==4]
 axes[1].hist([float(v['ratio']) for v in a],bins=np.linspace(0,1,11),alpha=.5,label=label,color=color)
 c=[float(v['commutator_norm']) for v in comm if v['pattern']==pat and int(v['N'])==64 and int(v['degree'])==4]
 axes[2].hist(c,bins=np.linspace(0,2,21),alpha=.5,label=label,color=color)
axes[1].set(xlabel='Error / deterministic bound',ylabel='Matrix count',title='(b) N=64, L=4, time=1, r=4')
axes[2].set(xlabel='Pair-commutator norm',ylabel='Pair count (dependent within matrix)',title='(c) N=64, L=4')
for ax in axes[1:]:ax.legend(fontsize=8)
save(fig,'overview.pdf')
print('Completed all seven report figure files and three data tables.')
