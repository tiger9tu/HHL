"""Reproduce the current T-count model and independent validation artifacts."""
import copy
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
from t_count import VERSION, be_resources, estimate, f, mcx_t, shortcut_queries

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def write(name, obj):
    (HERE/name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')


def application_parameters():
    a=json.loads((HERE.parent/'02-application/instance.json').read_text())
    m=a['m']; beta=a['beta']; h=a['h']; C=1+beta; N=m*m; D=2**((N-1).bit_length())
    sum_i=m*(m+1)/2
    sum_i2=m*(m+1)*(2*m+1)/6
    nodes=m+2*beta*h*sum_i+(beta*h)**2*sum_i2
    M=m-1
    mid_sum=M*(M+1)/2+M/2
    mid_sum2=M*(M+1)*(2*M+1)/6+M*(M+1)/2+M/4
    edges=M+2*beta*h*mid_sum+(beta*h)**2*mid_sum2
    alpha=math.sqrt((18*m-2)*nodes+2*m*edges+(D-N)*(4*C)**2)
    gap=h*h*a['lambda_min_lower']
    c_norm=h*h*m
    epsilon_proxy=a['solver_allowance']/(c_norm*a['solution_norm_upper']*math.sqrt(2))
    p=dict(instance_id=a['version']+'-stored-data-state-budget-proxy',N=N,
           kappa=8*C/gap,effective_inverse_gap=alpha/gap,
           epsilon_state=epsilon_proxy,delta_retry=.002,query_bound='auto',
           rotation_synthesis_offset=10)
    provenance=dict(benchmark=a['version'],m=m,beta=beta,padded_dimension=D,
                    frobenius_norm_scaled_padded=alpha,scaled_gap_lower=gap,
                    spectrum_norm_upper=8*C,scalar_cost_complete=False,
                    state_budget_note='Phase-aligned vector allowance / sqrt(2); global-phase/readout certificate still required.')
    return p,provenance


def dense_checks():
    """Small construction checks; no simulation of the complete stochastic solver."""
    import numpy as np
    reports=[]
    for m,beta in [(3,0),(3,9),(5,9)]:
        h=1/(m+1);N=m*m;D=2**((N-1).bit_length());C=1+beta
        B=np.eye(D)*4*C
        for i in range(m):
            for j in range(m):
                u=i*m+j; ai=1+beta*(i+1)*h
                B[u,u]=4*ai
                if i+1<m:
                    B[u,u+m]=B[u+m,u]=-(1+beta*(i+1.5)*h)
                if j+1<m:
                    B[u,u+1]=B[u+1,u]=-ai
        sf=(18*m-2)*sum((1+beta*i*h)**2 for i in range(1,m+1))
        sf+=2*m*sum((1+beta*(i+.5)*h)**2 for i in range(1,m))
        sf+=(D-N)*(4*C)**2
        assert abs(np.linalg.norm(B,'fro')**2-sf)<1e-10*sf
        assert np.linalg.eigvalsh(B)[0] >= 8*math.sin(math.pi*h/2)**2-1e-12
        reports.append('analytic padded Frobenius norm and spectral-gap bound: m={}, beta={}'.format(m,beta))
    # Explicit doubled-system A_t block encoding using only one controlled U_A.
    B=np.array([[.65,.2],[.2,.35]])
    B=B/np.linalg.norm(B,'fro')
    vals,V=np.linalg.eigh(np.eye(2)-B.dot(B))
    root=(V*np.sqrt(vals)).dot(V.T)
    UA=np.block([[B,root],[root,-B]])
    b=np.array([1.,2.])/math.sqrt(5)
    x=np.linalg.solve(B,b)
    I=np.eye(2)
    for ratio in [.5,1.,2.]:
        t=np.linalg.norm(x)/ratio
        # Direct sums are by augmentation branch. Ancillas order: extra, A ancilla.
        rot=np.array([[1/t,-math.sqrt(1-1/t**2)],[math.sqrt(1-1/t**2),1/t]])
        top=np.kron(I,UA)
        bottom=np.kron(rot,np.eye(4))
        U=np.block([[top,np.zeros((8,8))],[np.zeros((8,8)),bottom]])
        good=[0,1,8,9]
        At=U[np.ix_(good,good)]
        desired=np.block([[B,np.zeros((2,2))],[np.zeros((2,2)),I/t]])
        assert np.linalg.norm(U.T.dot(U)-np.eye(16))<1e-12
        assert np.linalg.norm(At-desired)<1e-12
        bp=np.r_[b,[1.,0.]]/math.sqrt(2)
        xt=np.linalg.solve(At,bp);xt/=np.linalg.norm(xt)
        e=np.array([0.,0.,1.,0.])
        out=(2*np.outer(xt,xt)-np.eye(4)).dot(e)[:2]
        assert np.linalg.norm(out/np.linalg.norm(out)-x/np.linalg.norm(x))<1e-12
        assert abs(np.dot(out,out)-(2*ratio/(1+ratio**2))**2)<1e-12
    reports.append('unitary/block, solution and success checks for doubled identity augmentation, three norm ratios')
    return reports


def validate():
    checks=[]
    # Independent expansion of Clader Table4 lambda=0 versus Table1.
    for n in [1,2,4,10]:
        for t,R in [(10,32),(40,128)]:
            D=2**n
            table4=8*(t+1)*(D+D)-8*t+8*D+4*t*n*R-16*t*n-8*t-24
            r=be_resources(n,t,R)
            assert r['A_uncontrolled_T']==table4
            assert r['A_controlled_T']>=table4
    checks.append('Clader Table1 count equals independently expanded Table4 at lambda=0')
    # Clean-ancilla ladder truth table, including full uncomputation.
    for c in range(2,7):
        assert mcx_t(c)==7*(2*c-3)
        for mask in range(2**c):
            bits=[(mask>>i)&1 for i in range(c)]
            for target in [0,1]:
                anc=[0]*max(0,c-2); gate_count=0; out=target
                if c==2:
                    out^=bits[0]&bits[1];gate_count=1
                else:
                    anc[0]^=bits[0]&bits[1];gate_count+=1
                    for j in range(1,c-2):
                        anc[j]^=anc[j-1]&bits[j+1];gate_count+=1
                    out^=anc[-1]&bits[-1];gate_count+=1
                    for j in reversed(range(1,c-2)):
                        anc[j]^=anc[j-1]&bits[j+1];gate_count+=1
                    anc[0]^=bits[0]&bits[1];gate_count+=1
                assert out==(target^int(all(bits))) and not any(anc)
                assert 7*gate_count==mcx_t(c)
    checks.append('multi-control ladder truth tables and ancilla cleanup, 2 through 6 controls')
    for K in [3,20,320,1e4,1e6]:
        q=shortcut_queries(K,.001)
        assert q['eq19_expected_A_queries_bound'] >= q['eq118_expected_A_queries_bound']
    assert shortcut_queries(1e6+1,.001)['bound_used']=='Dalzell Eq118'
    checks.append('Eq19 versus finite bound and mandatory switch outside published domain')
    p=dict(N=64,kappa=20,epsilon_state=.01,query_bound='eq118')
    base=estimate(p)
    for changes in [dict(N=128),dict(kappa=40),dict(epsilon_state=.001),dict(rotation_synthesis_offset=20)]:
        c=dict(p,**changes);assert f(c)>=base['T_count']
    checks.append('monotonic resource sensitivity with fixed Eq118 policy')
    for changes in [dict(N=1),dict(kappa=float('nan')),dict(epsilon_state=0),
                    dict(frobenius_over_spectral=100),dict(rotation_T_override=50),
                    dict(effective_inverse_gap=2e6,query_bound='eq19'),
                    dict(frobenius_over_spectral=2,effective_inverse_gap=100),dict(unknown=1)]:
        try:
            estimate(dict(p,**changes))
        except ValueError:
            pass
        else:
            raise AssertionError('invalid input accepted: '+str(changes))
    checks.append('invalid inputs, ambiguous normalization and unsupported Eq19 extrapolation rejected')
    for N,k in [(2,1),(16,100),(1024,1e4),(16129,1e6)]:
        r=estimate(dict(N=N,kappa=k,epsilon_state=.001));pr=r['precision'];q=r['query_model']
        assert pr['BE_unitary_error_design_bound']<=pr['unitary_tolerance_per_component']*(1+1e-12)
        assert math.exp(pr['ideal_cycle_cap']*math.log1p(-q['cycle_success_lower_bound']))<=pr['delta_retry']*(1+1e-12)
        assert abs(sum(r['components'].values())-r['T_count'])<=1e-12*r['T_count']
        assert r['capped_T_allocation_model']>=r['T_count']
    checks.append('precision allocation, ideal delivery cap and disjoint T accounting')
    checks+=dense_checks()
    return checks


def export_stage(r):
    def q(unit,value=None,note='Unresolved full compiled schedule.'):
        out=dict(unit=unit,status='unknown',note=note)
        if value is not None:out.update(status='known',value=value)
        return out
    return dict(id='q_shortcut_T_04',owner='04',branch='quantum',layer='logical',
        scope='per_output',reuse_key='none',multiplicity=q('1',1,'One delivered-state model; external scientific readout absent.'),
        statistic='expected',statistic_note='Modeled expected T cost using analytic upper bound on ideal queries; not a certified implemented expectation or full output guarantee.',
        covers=['q.core'],derived_from=[],assumptions=['A04T-access','A04T-query','A04T-controls','A04T-synthesis'],
        resources=dict(gate_basis='Clifford+T; T includes adjoint; measurements/reset not counted as T',
            gates=dict(T=q('gate',r['T_count'],'Analytic query bound times explicit T-cost envelope, with modeled synthesis.'),Clifford=q('gate')),
            oracle_queries=dict(A=q('query',r['query_model']['expected_A_queries_bound'],'Diagnostic, already expanded into T cost.'),
                                b=q('query',2*r['query_model']['expected_A_queries_bound'],'Diagnostic, already expanded into T cost.')),
            queries_expanded=True,depth=q('layer'),t_depth=q('layer'),
            logical_qubits_peak=q('logical_qubit',r['conservative_logical_qubit_allocation'],'Conservative allocation, no aggressive ancilla recycling; not QEC qubits.'),
            schedule='See t-count-model.md. Expected ideal Algorithm3 queries; Clifford counts and physical schedule unresolved.'))


def main():
    p=json.loads((HERE/'t-count-input.json').read_text())
    r=estimate(p);write('t-count-output.json',r)
    ap,meta=application_parameters();write('t-count-application-input.json',ap)
    ar=estimate(ap);ar['application_provenance']=meta;write('t-count-application-output.json',ar)
    with (HERE/'t-count-sensitivity.csv').open('w') as handle:
        w=csv.writer(handle);w.writerow(['N','kappa','epsilon_state','synthesis_offset','K','query_bound','T_count','BE_controlled_T','slot_T'])
        for N in [16,256,1024,16384]:
            for k in [10,100,1000]:
                for e in [.01,.001]:
                    for offset in [0,10,20]:
                        x=estimate(dict(N=N,kappa=k,epsilon_state=e,query_bound='eq118',rotation_synthesis_offset=offset))
                        w.writerow([N,k,e,offset,x['query_model']['K'],x['query_model']['bound_used'],x['T_count'],x['block_encoding']['A_controlled_T'],x['per_query_slot_T']])
    checks=validate()
    schema_path=HERE.parent/'01-framework/interface.schema.json'
    schema=json.loads(schema_path.read_text())
    import jsonschema
    validator=jsonschema.Draft7Validator({'$schema':schema['$schema'],'$ref':'#/definitions/stage','definitions':schema['definitions']})
    for name,result in [('t-count-stage.json',r),('t-count-application-stage.json',ar)]:
        s=export_stage(result);validator.validate(s);write(name,s)
    checks.append('both task01 v1.0.0 stage fragments validate structurally')
    import numpy as np
    write('t-count-validation.json',dict(checks=checks,result='passed',python=platform.python_version(),numpy=np.__version__,jsonschema=jsonschema.__version__,
            limitations='No stochastic full circuit, rotation synthesis, signed scalar readout or QEC validation.'))
    paths=[HERE/'t_count.py',HERE/'reproduce_t_count.py',HERE/'t-count-model.md',HERE/'t-count-input.json',
           HERE.parent/'02-application/instance.json',HERE.parent/'02-application/specification.md',schema_path]
    paths+=list((HERE/'sources').glob('*.pdf'))+list((HERE/'sources').glob('*.html'))
    write('t-count-manifest.json',dict(model_version=VERSION,captured_utc='2026-09-10',
          git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip(),
          command='python3 paper-revise/results/04-modern-qlsa/reproduce_t_count.py',
          inputs_sha256={str(path.relative_to(ROOT)):hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
          instance_id=ap['instance_id'],task05_available=(HERE.parent/'05-input-output').exists()))
    print(json.dumps(dict(validation='passed',checks=len(checks),generic_T=r['T_count'],application_state_T=ar['T_count'],
                         application_K=ar['query_model']['K'],application_query_bound=ar['query_model']['bound_used']),indent=2))


if __name__=='__main__':main()
