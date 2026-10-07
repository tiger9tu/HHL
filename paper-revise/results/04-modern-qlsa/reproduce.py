"""Generate artifacts and validate ideal-model math; run from any directory."""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
from logical_model import evaluate

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]


def write(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n')


def quantity(unit, value=None, expression=None, note='Unresolved compilation input.'):
    result = dict(unit=unit, note=note, status='unknown')
    if value is not None:
        result.update(status='known', value=value)
    if expression is not None:
        result.update(status='symbolic', expression=expression)
    return result


def stage(r, optimal):
    Q, L = r['A_queries'], r.get('ell')
    def formula(g):
        if optimal:
            return '{} * g_A_{} + {} * g_b_{} + H_{}'.format(Q,g,2*Q,g,g)
        return '{} * g_Gt_{} + {} * g_projector_{} + {} * g_rotation_{} + g_endpoint_{}'.format(2*L,g,4*L,g,2*L,g,g)
    return dict(
        id='q_shortcut_04_'+('optimal' if optimal else 'norm_core'),
        branch='quantum', layer='logical', owner='04', scope='per_output', reuse_key='none',
        multiplicity=quantity('1', value=1, note='Alternative core import; task 05 composes once.'),
        statistic='upper_bound', statistic_note=r['statistic']+'; '+r['output_certificate']+'. Compiled costs unresolved.',
        covers=['q.core'], derived_from=[],
        assumptions=['A04-input','A04-access','A04-ideal','A04-compilation']+([] if optimal else ['A04-norm']),
        resources=dict(
            gate_basis='compiled Clifford+T; exclusive buckets, T includes adjoint',
            gates={g:quantity('gate',expression=formula(g)) for g in ['T','Clifford']},
            oracle_queries={key:quantity('query',value=r[key+'_queries'],note=r['statistic']+'; includes controlled and adjoint variants.') for key in ['A','b']},
            queries_expanded=False,
            depth=quantity('layer'), t_depth=quantity('layer'),
            logical_qubits_peak=quantity('logical_qubit'),
            schedule='See model.md. '+('Adaptive internal restarts included in query expectation; no termination cap or compiled schedule.' if optimal else 'One serial KR attempt including endpoint/herald operations; external retries excluded.')))


def validate_math(c):
    checks = []
    base = evaluate(c)
    assert base['effective_inverse_gap'] == 4
    checks.append('alpha/sigma_min normalization yields K=4, not kappa=3')
    for mode in ['unknown_norm_optimal','certified_norm_core']:
        cfg=json.loads((OUT/('model-input.json' if mode=='unknown_norm_optimal' else 'norm-core-input.json')).read_text())
        r=evaluate(cfg)
        tighter=copy.deepcopy(cfg); tighter['cq']['epsilon_trace_algorithm']/=10
        assert evaluate(tighter)['A_queries'] >= r['A_queries']
        larger=copy.deepcopy(cfg); larger['cq']['block_encoding_alpha']*=2
        assert evaluate(larger)['A_queries'] >= r['A_queries']
    checks.append('stricter precision and larger access normalization increase query bounds')
    for field,value in [('epsilon_trace_algorithm',0),('epsilon_trace_algorithm',float('nan')),('block_encoding_alpha',.5)]:
        bad=copy.deepcopy(c); bad['cq'][field]=value
        try:
            evaluate(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted')
    checks.append('invalid precision and normalization rejected')
    # Verify continuous spectral attenuation, not only the sampled spectrum.
    core=json.loads((OUT/'norm-core-input.json').read_text())
    for K in [1.01,2,4,20,100]:
        core['cq']['block_encoding_alpha']=max(.75,K/4)
        r=evaluate(core); k=r['effective_inverse_gap']; ell=r['ell']
        denom=math.log1p(2/(k-1)) # acosh((1+1/k^2)/(1-1/k^2))
        attenuation=1/math.cosh(ell*denom)
        assert attenuation <= r['eta_KR']*(1+1e-12)
    checks.append('Chebyshev minimax attenuation satisfies requested eta over full gapped interval')
    # Direct ideal reflection: independent dense linear algebra for the task03 matrix.
    import numpy as np
    A=np.array([[.65,.2],[.2,.35]])
    b=np.ones(2)/math.sqrt(2)
    x=np.linalg.solve(A,b); xn=np.linalg.norm(x)
    assert abs(xn-4/math.sqrt(5))<1e-12
    for ratio in [.5,1,2]:
        t=xn/ratio
        xt=np.r_[x,t]; xt/=np.linalg.norm(xt)
        e=np.array([0.,0.,1.])
        reflected=(2*np.outer(xt,xt)-np.eye(3)).dot(e)
        output=reflected[:2]
        assert np.linalg.norm(output/np.linalg.norm(output)-x/xn)<1e-12
        assert abs(np.dot(output,output)-(2*ratio/(1+ratio**2))**2)<1e-12
    checks.append('dense augmented ideal reflection recovers exact solution and success law for three norm ratios')
    return checks


def main():
    inputs=[json.loads((OUT/name).read_text()) for name in ['model-input.json','norm-core-input.json']]
    results=[evaluate(c) for c in inputs]
    for name,r in zip(['model-output.json','norm-core-output.json'],results):
        write(name,r)
    stages=[stage(r,i==0) for i,r in enumerate(results)]
    schema_path=OUT.parent/'01-framework/interface.schema.json'
    schema=json.loads(schema_path.read_text())
    import jsonschema
    validator=jsonschema.Draft7Validator({'$schema':schema['$schema'],'$ref':'#/definitions/stage','definitions':schema['definitions']})
    for s in stages:
        validator.validate(s)
    write('contract-stages.json',stages)
    with (OUT/'sensitivity.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['effective_inverse_gap','epsilon_trace_algorithm','expected_A_queries_upper_bound','expected_b_queries_upper_bound'])
        for k in [4,10,100,1000,10000]:
            for eps in [.01,.001,.0001]:
                c=copy.deepcopy(inputs[0]);c['cq']['block_encoding_alpha']=k/4;c['cq']['epsilon_trace_algorithm']=eps
                r=evaluate(c);w.writerow([r['effective_inverse_gap'],eps,r['A_queries'],r['b_queries']])
    checks=validate_math(inputs[0])
    import numpy as np
    write('validation.json',dict(checks=checks,stage_schema='passed, task01 v1.0.0 fragments only',
          scope='Analytic formula/domain checks and dense ideal reflection identity. No compiled circuit, QEC, full workload, or task02 acceptance validation.',
          benchmark_reconciled=False,qec_ready=False,python=platform.python_version(),numpy=np.__version__,jsonschema=jsonschema.__version__))
    paths=[ROOT/'paper-revise/prompts/paper-revise.md',ROOT/'tools/surface_code_opt.py',ROOT/'src/HHL/HamiltonianEvolution/Oracle/Oracle.qs']
    paths+=list((ROOT/'paper-revise/docs').glob('*.pdf'))+list((ROOT/'paper').glob('*.pdf'))
    paths+=list((OUT.parent/'01-framework').glob('*.md'))+[schema_path]
    paths+=list((ROOT/'paper-revise/prompts/tasks').glob('*.md'))
    paths += [OUT.parent/'03-hhl-analysis'/name for name in ['model-input.json','resource-model.md','audit-and-handoff.md','contract-stage.json']]
    paths+=list((OUT/'sources').glob('*.pdf'))+list(OUT.glob('*.py'))+list(OUT.glob('*input.json'))+list(OUT.glob('*.md'))
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths))}
    write('input-versions.json',dict(captured_utc='2026-09-09',git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip(),
          inputs_sha256=hashes,upstream_missing=[name for name in ['02-application','05-input-output'] if not (OUT.parent/name).exists()],
          command='python3 paper-revise/results/04-modern-qlsa/reproduce.py',python=platform.python_version()))
    print(json.dumps(dict(validation='passed',checks=len(checks),unknown_norm_A_queries=results[0]['A_queries'],norm_core_A_queries=results[1]['A_queries'],acceptance='pending task02 and task05; QEC inputs unresolved'),indent=2))


if __name__=='__main__':
    main()
