"""Create report prose from measured data; no matrix computations."""
import csv,json,math,statistics
from pathlib import Path
P=Path(__file__).resolve().parent
s=json.loads((P/'results.json').read_text());rows=list(csv.DictReader((P/'errors.csv').open()))
slopes={}
for f,n in [('random_matching',128),('poisson_2d',225)]:
    slopes[f]={}
    for key in ['operator_error','matrix_error']:
        values=[statistics.median(float(a[key]) for a in rows if a['family']==f and int(a['N'])==n and a['matching_terms']=='4' and a['sweep']=='time_steps' and float(a['tau'])==1 and int(a['r'])==r) for r in [16,32]]
        slopes[f][key]=math.log(values[0]/values[1],2)
ratios=[]
for a in rows:
    if a['matrix_bound_applicable']=='True' and float(a['C_comm'])>0:
        d=float(a['log_reconstruction_fro']);nu=2*math.sin((math.pi-float(a['phase_gap_to_pi']))/2)+d
        diagnostic=d/(float(a['h'])*(1-nu))
        slack=float(a['matrix_bound_refined'])-float(a['matrix_error'])
        ratios.append(diagnostic/slack)
extra=dict(two_point_orders=slopes,max_log_reconstruction_diagnostic_over_bound_slack=max(ratios))
(P/'additional-checks.json').write_text(json.dumps(extra,indent=2)+'\n')
t=r'''\subsection{Measured results and interpretation}
There were \textbf{no operator-bound violations in 20,400 comparisons} and \textbf{no effective-H-bound violations in 13,194 applicable comparisons}, at the stated numerical tolerance. The remaining 7,206 effective-H measurements lie outside $hB\leq1/2$ and are not counted as theorem tests. Zero-commutator controls contribute 96 operator comparisons and 64 applicable effective-H comparisons; their errors are at roundoff level.

\begin{center}\small\input{experiments/ratio-table.tex}\end{center}
The table excludes zero denominators. The median measured error is 41.6\%% of the capped operator bound, 38.3\%% of the refined effective-H bound, and 21.8\%% of the coarse effective-H bound. The maximum ratios are approximately 0.99999946, 0.99686747 and 0.50345923, respectively. Thus the operator and refined matrix bounds can be nearly tight in this sweep. The coarse matrix estimate is more conservative. These percentiles depend on the selected families and settings.

\begin{center}\small\input{experiments/selected-values.tex}\end{center}
This table uses $\tau=1$, four matching terms, $N=128$ for random matching (16-sample medians) and $N=225$ for Poisson. The effective-H column uses the refined bound; all tabulated comparisons satisfy the sufficient condition. Doubling $r$ from 16 to 32 approximately halves both measured errors. The two-point orders $\log_2(E_{16}/E_{32})$ are %.6f and %.6f for random-matching operator and effective-H errors, and %.6f and %.6f for Poisson. This is consistent with first-order convergence at fixed time, $E_U=O(\tau^2/r)$ and $E_H=O(\tau/r)$, with the decomposition coefficient retained. It is not an empirical proof of a universal dimension scaling.

The 553 independent cross-algorithm comparisons have maximum logarithm difference $1.18\times10^{-12}$, Gram/SVD norm difference $4.45\times10^{-15}$, block/dense-exponential difference $1.18\times10^{-15}$, and spectral/dense exact-evolution difference $6.16\times10^{-13}$. Across all measurements the maximum base-unitarity Frobenius residual is $2.11\times10^{-14}$. Within the effective-H domain, the maximum logarithm-reconstruction residual is $4.31\times10^{-11}$ and the minimum eigenphase gap from $\pm\pi$ is 2.6427 radians. Maximum commuting errors are $9.91\times10^{-15}$ (operator) and $6.67\times10^{-16}$ (applicable effective H).

For an additional conditioning diagnostic, let $\widetilde P=Q\operatorname{diag}(e^{\ii\theta_j})Q^\dagger$, $d=\norm{\widetilde P-P}_F$, and $\nu=\max_j|e^{\ii\theta_j}-1|+d$. The same logarithm-series argument gives a reconstruction-distance diagnostic $d/[h(1-\nu)]$ when $\nu<1$. Its maximum over applicable cases is $2.60\times10^{-9}$, and its maximum ratio to the observed positive bound slack is %.6f. This check supports numerical separation from the bounds; it is not an interval-arithmetic certificate for every floating-point operation.
'''%(slopes['random_matching']['operator_error'],slopes['random_matching']['matrix_error'],slopes['poisson_2d']['operator_error'],slopes['poisson_2d']['matrix_error'],max(ratios))
(P/'measured-findings.tex').write_text(t)
