"""Aggregate complete Slurm results and plot actual errors against analytic bounds."""
import csv,hashlib,json,math
from collections import defaultdict
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
FIG=HERE/'figures';FIG.mkdir(exist_ok=True)
LABEL={'fixed_band':'Fixed band','random_matching':'Random matching','random_spd':'Random SPD','poisson_2d':'Poisson','commuting':'Commuting','cancelling':'Cancelling','pauli':'Pauli'}
COLOR={'fixed_band':'#315d91','random_matching':'#c46721','random_spd':'#22875c','poisson_2d':'#8558a6','commuting':'#7a7a7a','cancelling':'#c84958','pauli':'#303030'}
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42})

def save(fig,name):
    fig.tight_layout();fig.savefig(str(FIG/(name+'.pdf')));fig.savefig(str(FIG/(name+'.png')),dpi=150);plt.close(fig)

def csvsave(name,rows):
    fields=[]
    for row in rows:
        for k in row:
            if k not in fields:fields.append(k)
    with (HERE/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)

def ratio_stats(rows,key):
    x=np.array([r[key] for r in rows if r.get(key) is not None])
    return dict(count=len(x),median=float(np.median(x)),q05=float(np.quantile(x,.05)),q95=float(np.quantile(x,.95)),maximum=float(x.max())) if len(x) else dict(count=0)

def find(rows,family,N,terms,tau=1):
    return [x for x in rows if x['family']==family and x['N']==N and x['matching_terms']==terms and x['sweep']=='time_steps' and x['tau']==tau]

def main():
    configs=json.loads((HERE/'configurations.json').read_text());rows=[];checks=[];cases=[]
    for c in configs:
        p=HERE/'shards'/('%04d.json'%c['case_id'])
        if not p.exists():raise RuntimeError('Incomplete experiment: missing '+str(p))
        obj=json.loads(p.read_text());assert obj['status']=='passed'
        rows.extend(obj['rows']);checks.extend(obj['independent_checks']);cases.append(obj['case'])
    assert len(rows)==24*len(configs)
    csvsave('errors.csv',rows);csvsave('matrix-cases.csv',cases);csvsave('independent-validation.csv',checks)
    groups=defaultdict(list)
    for row in rows:
        key=(row['family'],row['N'],row['matching_terms'],row.get('amplitude'),row['sweep'],row['tau'] if row['sweep']=='time_steps' else row['rho_target'],row['r'])
        groups[key].append(row)
    boot=np.random.RandomState(20261909);summaries=[]
    for key,group in sorted(groups.items(),key=lambda v:str(v[0])):
        for metric in ['operator_error','matrix_error','operator_bound','matrix_bound','matrix_bound_refined']:
            values=np.array([a[metric] for a in group if a[metric] is not None]);n=len(values)
            if n==0:continue
            stochastic=key[0] in ['fixed_band','random_matching','random_spd']
            ci=np.quantile(np.mean(boot.choice(values,(2000,n)),axis=1),[.025,.975]) if stochastic and n>=2 else [None,None]
            summaries.append(dict(family=key[0],N=key[1],matching_terms=key[2],amplitude=key[3],sweep=key[4],time_or_rho=key[5],r=key[6],metric=metric,samples=n,mean=float(values.mean()),median=float(np.median(values)),q05=float(np.quantile(values,.05)),q95=float(np.quantile(values,.95)),maximum=float(values.max()),mean_ci_low=ci[0],mean_ci_high=ci[1]))
    csvsave('summary.csv',summaries)
    cert=[a for a in rows if a['matrix_bound_applicable']];nonzero=[a for a in rows if a['C_comm']>0]
    comm=[a for a in rows if a['C_comm']==0]
    uncertainty=[]
    for a in cert:
        d=a['log_reconstruction_fro'];rho=2*np.sin((np.pi-a['phase_gap_to_pi'])/2)+d
        if rho<1:uncertainty.append(d/(a['h']*(1-rho)))
    stats={'matrix_cases':len(cases),'measurements':len(rows),'operator_comparisons':len(rows),'effective_matrix_certified_comparisons':len(cert),'effective_matrix_outside_sufficient_condition':len(rows)-len(cert),'operator_violations':sum(a['operator_violation'] for a in rows),'effective_matrix_violations':sum(a['matrix_violation'] for a in cert),'operator_ratio':ratio_stats(nonzero,'operator_ratio'),'operator_unsaturated_ratio':ratio_stats([a for a in nonzero if a['operator_bound_uncapped']<2],'operator_ratio'),'effective_coarse_ratio':ratio_stats(cert,'matrix_ratio'),'effective_refined_ratio':ratio_stats(cert,'matrix_ratio_refined'),'max_base_unitarity_fro':max(a['base_unitarity_fro'] for a in rows),'max_certified_log_reconstruction_fro':max(a['log_reconstruction_fro'] for a in cert),'max_certified_log_distance_diagnostic':max(uncertainty),'min_certified_phase_gap':min(a['phase_gap_to_pi'] for a in cert),'independent_algorithm_comparisons':len(checks),'max_independent_logm_difference':max(a['logm_difference'] for a in checks),'max_gram_vs_svd_difference':max(a['gram_vs_svd_difference'] for a in checks),'max_block_vs_expm_difference':max(a['block_vs_expm_difference'] for a in checks),'max_spectral_vs_expm_difference':max(a['spectral_vs_expm_difference'] for a in checks),'commuting_rows':len(comm),'max_commuting_operator_error':max(a['operator_error'] for a in comm),'max_certified_commuting_matrix_error':max(a['matrix_error'] for a in comm if a['matrix_bound_applicable']),'bootstrap_seed':20261909,'bootstrap_replicates':2000,'absolute_comparison_tolerance':5e-10,'families':{f:sum(c['family']==f for c in cases) for f in LABEL},'max_dimension':max(c['N'] for c in cases)}
    (HERE/'results.json').write_text(json.dumps(stats,indent=2)+'\n')
    # Figure 1: every nonzero-bound comparison, with family-specific colors.
    fig,axs=plt.subplots(1,2,figsize=(9.4,4.2))
    for f in LABEL:
        a=[r for r in rows if r['family']==f and r['operator_bound']>0]
        axs[0].scatter([r['operator_bound'] for r in a],[r['operator_error'] for r in a],s=5,alpha=.23,color=COLOR[f],label=LABEL[f],rasterized=True)
        a=[r for r in cert if r['family']==f and r['matrix_bound_refined']>0]
        axs[1].scatter([r['matrix_bound_refined'] for r in a],[r['matrix_error'] for r in a],s=5,alpha=.23,color=COLOR[f],label=LABEL[f],rasterized=True)
    for ax,title in zip(axs,['Operator error: all step sizes','Effective H: only hB <= 1/2']):
        ax.set(xscale='log',yscale='log',xlabel='Analytic error bound',ylabel='Measured spectral-norm error',title=title)
        xlim=ax.get_xlim();ylim=ax.get_ylim();lo=min(xlim[0],ylim[0]);hi=max(xlim[1],ylim[1]);ax.plot([lo,hi],[lo,hi],'k--',lw=1,label='Error = bound');ax.legend(fontsize=7,loc='upper left')
    save(fig,'actual_vs_bound')
    # Figure 2: paired operator/effective curves at fixed tau=1.
    fig,axs=plt.subplots(2,2,figsize=(9.4,7.4))
    for col,(f,N,L) in enumerate([('random_matching',128,4),('poisson_2d',225,4)]):
        group=find(rows,f,N,L);rs=sorted(set(a['r'] for a in group))
        for row,metric,bounds in [(0,'operator_error',['operator_bound']),(1,'matrix_error',['matrix_bound_refined','matrix_bound'])]:
            ax=axs[row,col];parts=[[a for a in group if a['r']==r] for r in rs]
            vals=[np.array([a[metric] for a in g]) for g in parts]
            ax.plot(rs,[np.median(x) for x in vals],'o-',color=COLOR[f],label='Actual error (median)')
            if f!='poisson_2d':ax.fill_between(rs,[np.quantile(x,.05) for x in vals],[np.quantile(x,.95) for x in vals],alpha=.15,color=COLOR[f])
            for bound,style,label in zip(bounds,['--',':'],['Operator bound' if row==0 else 'Refined matrix bound','Coarse matrix bound']):
                data=[(r,g) for r,g in zip(rs,parts) if all(a[bound] is not None for a in g)]
                ax.plot([r for r,g in data],[np.median([a[bound] for a in g]) for r,g in data],style,color='black',label=label)
            ax.set(xscale='log',yscale='log',xlabel='Trotter steps r',ylabel='Operator error' if row==0 else 'Effective-matrix error',title='%s, N=%d, time=1'%(LABEL[f],N))
            ax.set_xticks(rs);ax.set_xticklabels([str(r) for r in rs]);ax.legend(fontsize=8)
    save(fig,'step_convergence')
    # Figure 3: direct approach to the sufficient branch threshold.
    fig,axs=plt.subplots(1,2,figsize=(9.4,4.2))
    for f,N in [('fixed_band',128),('random_matching',128),('random_spd',128),('poisson_2d',225),('pauli',2)]:
        a=[r for r in rows if r['family']==f and r['N']==N and r['sweep']=='normalized_step' and (r['matching_terms']==4 or f=='pauli')]
        rho=sorted(set(r['rho_target'] for r in a));med_u=[];med_h=[]
        for x in rho:
            subset=[r for r in a if r['rho_target']==x]
            med_u.append(np.median([r['operator_error']/(r['h']**2*r['C_comm']/2) for r in subset]))
            med_h.append(np.median([r['matrix_error']/(r['h']*r['C_comm']) for r in subset]))
        axs[0].plot(rho,med_u,'o-',label=LABEL[f],color=COLOR[f]);axs[1].plot(rho,med_h,'o-',label=LABEL[f],color=COLOR[f])
    axs[0].axhline(1,color='black',ls='--',label='Operator bound')
    x=np.linspace(.01,.5,100);axs[1].plot(x,1/(2*(1-x)),'k--',label='Refined bound / (h C)');axs[1].plot([.01,.5],[1,1],'k:',label='Coarse bound / (h C)')
    for ax in axs:
        ax.set(xlabel='Normalized microstep h B');ax.axvline(.5,color='#777777',lw=.8);ax.legend(fontsize=7)
    axs[0].set(ylabel='Actual operator error / local bound',title='One microstep: operator bound always valid')
    axs[1].axvspan(.5,1.25,color='#eeeeee',zorder=-1);axs[1].set(ylabel='Actual effective-H error / (h C)',title='Matrix bound stated only for hB <= 1/2')
    save(fig,'branch_condition_sweep')
    # Figure 4: scaling with size; medians/bands use exactly the same matrix samples.
    fig,axs=plt.subplots(1,2,figsize=(9.4,4.2))
    for f in ['fixed_band','random_matching','random_spd','poisson_2d']:
        group=[r for r in rows if r['family']==f and r['matching_terms']==4 and r['sweep']=='time_steps' and r['tau']==1 and r['r']==16]
        ns=sorted(set(r['N'] for r in group));parts=[[r for r in group if r['N']==N] for N in ns]
        for ax,key,bound in zip(axs,['operator_error','matrix_error'],['operator_bound','matrix_bound_refined']):
            ax.plot(ns,[np.median([r[key] for r in g]) for g in parts],'o-',color=COLOR[f],label=LABEL[f])
            ax.fill_between(ns,[np.quantile([r[key] for r in g],.05) for g in parts],[np.quantile([r[key] for r in g],.95) for g in parts],color=COLOR[f],alpha=.1)
            bs=[(N,g) for N,g in zip(ns,parts) if all(r[bound] is not None for r in g)]
            ax.plot([N for N,g in bs],[np.median([r[bound] for r in g]) for N,g in bs],'--',color=COLOR[f])
    for ax,title in zip(axs,['Operator error','Effective-matrix error']):
        ax.set(xscale='log',yscale='log',xlabel='Matrix dimension N',ylabel=title,title='Time=1, r=16; solid actual, dashed bound');ax.legend(fontsize=7)
    save(fig,'dimension_sweep')
    # Figure 5: one observation per synthetic matrix, avoiding repeated-step pseudoreplication.
    fig,axs=plt.subplots(1,2,figsize=(9.4,4))
    for terms,color in [(2,'#315d91'),(4,'#c46721'),(8,'#22875c')]:
        a=[r for r in rows if r['family'] in ['fixed_band','random_matching','random_spd'] and r['matching_terms']==terms and r['sweep']=='time_steps' and r['tau']==1 and r['r']==16]
        for ax,key in zip(axs,['operator_ratio','matrix_ratio_refined']):
            vals=[r[key] for r in a if r[key] is not None]
            ax.hist(vals,bins=np.linspace(0,1,21),alpha=.45,label='%d matching terms (n=%d)'%(terms,len(vals)),color=color)
    for ax,title in zip(axs,['Operator error / bound','Effective-H error / refined bound']):
        ax.set(xlabel=title,ylabel='Matrix count',title='Time=1, r=16');ax.legend(fontsize=8)
    save(fig,'ratio_distributions')
    # Exact diagonal control that distinguishes the microstep generator from a wrapped global logarithm.
    branch=[];lam=np.array([.5,1.]);tau=4.
    for r in [1,2,4,8,16,32,64,128]:
        h=tau/r;p=np.exp(1j*h*lam);s=p**r
        branch.append(dict(N=2,tau=tau,r=r,h=h,B=1,C_comm=0,certified=h<=.5,operator_error=float(np.max(abs(s-np.exp(1j*tau*lam)))),microstep_matrix_error=float(np.max(abs(np.angle(p)/h-lam))),global_principal_log_error=float(np.max(abs(np.angle(s)/tau-lam)))))
    csvsave('global-log-diagnostic.csv',branch)
    # Tables for the PDF, generated directly from complete data.
    with (HERE/'experiment-tables.tex').open('w') as f:
        f.write('\\begin{tabular}{lrr}\\toprule Family & Matrices & Measurements\\\\\\midrule\n')
        for fam,n in stats['families'].items():f.write('%s & %d & %d\\\\\n'%(LABEL[fam],n,n*24))
        f.write('\\midrule Total & %d & %d\\\\\\bottomrule\\end{tabular}\n'%(len(cases),len(rows)))
    with (HERE/'ratio-table.tex').open('w') as f:
        f.write('\\begin{tabular}{lrrrr}\\toprule Error/bound ratio & Count & Median & 95th percentile & Maximum\\\\\\midrule\n')
        for label,key in [('Operator (capped bound)','operator_ratio'),('Operator (unsaturated)','operator_unsaturated_ratio'),('Effective H (coarse)','effective_coarse_ratio'),('Effective H (refined)','effective_refined_ratio')]:
            a=stats[key];f.write('%s & %d & %.5f & %.5f & %.8f\\\\\n'%(label,a['count'],a['median'],a['q95'],a['maximum']))
        f.write('\\bottomrule\\end{tabular}\n')
    with (HERE/'selected-values.tex').open('w') as f:
        f.write('\\begin{tabular}{llrrrr}\\toprule Family & $r$ & Actual $E_U$ & Bound $E_U$ & Actual $E_H$ & Bound $E_H$\\\\\\midrule\n')
        for fam,N in [('random_matching',128),('poisson_2d',225)]:
            for r in [4,8,16,32]:
                g=[a for a in find(rows,fam,N,4) if a['r']==r]
                f.write('%s & %d & %.5g & %.5g & %.5g & %.5g\\\\\n'%(LABEL[fam],r,np.median([a['operator_error'] for a in g]),np.median([a['operator_bound'] for a in g]),np.median([a['matrix_error'] for a in g]),np.median([a['matrix_bound_refined'] for a in g])))
        f.write('\\bottomrule\\end{tabular}\n')
    print(json.dumps(stats,indent=2))

if __name__=='__main__':main()
