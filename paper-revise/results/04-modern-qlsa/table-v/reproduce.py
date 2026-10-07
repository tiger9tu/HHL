"""Reproduce Table-V examples and verify transcription/parameter adapter."""
from decimal import Decimal as D, localcontext
import hashlib
import json
from pathlib import Path
import platform
from paper_table_v import table_v, estimate, f, _estimate

HERE=Path(__file__).resolve().parent

def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2)+'\n')

p=json.loads((HERE/'input.json').read_text())
out=estimate(p)
write('output.json',out)
checks=[]
with localcontext() as c:
    c.prec=80
    # Hand calculation: log2(1/(1/4))=2; N=2, Q=3, d=2.
    x=table_v(2,3,2,'0.25','0.25','0.25','0.25','0.25')
    assert x['T_BE']==184 and x['T_controlled_BE']==200 and x['T_SP']==48
    assert x['T_QLSS']==3269 and x['T_controlled_QLSS']==3365
checks.append('Tables III--V: both columns match independent hand calculation')
assert out['Q']==12800000 and out['d']==44210
assert out['matrix_calls']=='25688420' and out['rhs_calls']=='51376840'
assert D(out['equation_64_error'])==D('0.01')
assert out['retry_cap']==7 and out['T_retry_budget']==7*out['T_per_attempt_ceiling']
assert f(p)==86705344699164751
checks.append('normalization, query multiplicities, Eq.(64) allocation, example count and retries')
for precision in [40,100]:
    with localcontext() as c:
        c.prec=precision
        assert _estimate(p)['T_retry_budget']==out['T_retry_budget']
checks.append('integer result stable at 40, 80 and 100 decimal digits')
for value,expected in [('0.5',1),('0.25',2),('0.125',3),('0.01',7)]:
    assert estimate(dict(p,delta=value))['retry_cap']==expected
checks.append('retry cap includes exact power-of-two boundaries')
for change in [dict(N=1),dict(kappa=0),dict(delta=0),dict(epsilon_state='NaN'),
               dict(frobenius_over_spectral=2,effective_inverse_gap=100)]:
    try:estimate(dict(p,**change))
    except ValueError:pass
    else:raise AssertionError('invalid input accepted')
checks.append('invalid inputs and ambiguous normalization rejected')
rp=dict(p,include_readout=True,epsilon_readout='0.01',delta_readout='0.01')
ro=estimate(rp);rd=ro['readout']
write('readout-input.json',rp);write('readout-output.json',ro)
assert estimate(dict(p,include_readout=False))['T_total']==out['T_retry_budget']
assert f(rp)==rd['T_total']
assert rd['T_total']==rd['samples_per_family']*(rd['T_plain_per_execution']+rd['T_controlled_per_execution'])
assert rd['T_total']==rd['T_one_solver_execution']+rd['T_additional_after_one_execution']
assert rd['retry_multiplier_applied']==1
assert D(rd['epsilon_state_used'])<D(p['epsilon_state'])
assert abs(D(rd['output_error_model'])-D('0.01'))<D('1e-70')
assert D(rd['proposition_4_lhs'])<D('0.5')
# Total-output error changes only the tomography adapter; no hidden modification of baseline.
assert ro['T_retry_budget']==out['T_retry_budget']
assert estimate(dict(rp,epsilon_readout='0.005'))['T_total']>ro['T_total']
assert estimate(dict(rp,delta_readout='0.001'))['readout']['samples_per_family']>rd['samples_per_family']
for change in [dict(include_readout='yes'),dict(epsilon_readout='0.01'),
               dict(include_readout=True,epsilon_readout=0),dict(include_readout=True,delta_readout=1)]:
    try:estimate(dict(p,**change))
    except ValueError:pass
    else:raise AssertionError('invalid readout input accepted')
checks.append('optional tomography: error budget, exclusive costs, no double retry, monotonicity and invalid inputs')
with localcontext() as c:
    c.prec=80
    k=rd['samples_per_family'];e=D(rd['epsilon_sampling']);dr=D(rd['delta_readout'])
    raw=D('57.5')*1024*(D(6144)/dr).ln()/(e*e*(1-e*e/4))
    assert k-1<raw<=k
checks.append('tomography repetition ceiling independently checked')
(HERE/'readout-numbers.tex').write_text(
    '\\newcommand{\\ReadoutSamples}{'+format(rd['samples_per_family'],',').replace(',',r'\,')+'}\n'+
    '\\newcommand{\\ReadoutTotal}{'+format(rd['T_total'],',').replace(',',r'\,')+'}\n')
print('Readout:',rd['samples_per_family'],'samples per family;',rd['T_total'],'T gates')
alternatives=[]
for label,change in [('K_is_100',dict(effective_inverse_gap=100)),
                     ('larger_analytic_C_only',dict(adiabatic_constant=15307))]:
    x=estimate(dict(p,**change));x['scenario']=label;alternatives.append(x)
write('alternatives.json',alternatives)
write('validation.json',dict(result='passed',checks=checks,python=platform.python_version(),
                            scope='Formula transcription and numerical adapter, not full circuit certification'))
paths=[HERE/'paper_table_v.py',HERE/'reproduce.py',HERE/'input.json',HERE.parent/'sources/2211.12489v1.pdf']
write('manifest.json',dict(source='https://arxiv.org/pdf/2211.12489v1#page=22',
                         sha256={str(x.relative_to(HERE.parent)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}))
print(json.dumps({k:out[k] for k in ['Q','d','matrix_calls','T_controlled_BE','T_per_attempt_ceiling','retry_cap','T_retry_budget']},indent=2))
print('Validation: '+str(len(checks))+' groups passed')
