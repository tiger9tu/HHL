"""Generate exact sufficient counts, checks and publication tables."""
import csv
import hashlib
import json
import math
from pathlib import Path
import platform
import sys
from fractions import Fraction as F
from upper_bound import VERSION,clog2,pow2,ceilq,schedule,estimate,f

HERE=Path(__file__).resolve().parent


def write(name,value):
    (HERE/name).write_text(json.dumps(value,indent=2)+'\n')


def app_input():
    a=json.loads((HERE.parent.parent/'02-application/instance.json').read_text())
    m=a['m'];beta=F(str(a['beta']));C=1+beta;h=F(1,m+1)
    N=m*m;D=1<<((N-1).bit_length())
    nodes=m+2*beta*h*F(m*(m+1),2)+(beta*h)**2*F(m*(m+1)*(2*m+1),6)
    M=m-1
    mids=M+2*beta*h*(F(M*(M+1),2)+F(M,2))+(beta*h)**2*(F(M*(M+1)*(2*M+1),6)+F(M*(M+1),2)+F(M,4))
    frob2=(18*m-2)*nodes+2*m*mids+(D-N)*(4*C)**2
    # No floating point square root is used for a theorem input.
    alpha=1
    while F(alpha*alpha)<frob2:alpha*=2
    lo=alpha//2;hi=alpha
    while lo+1<hi:
        mid=(lo+hi)//2
        if F(mid*mid)>=frob2:hi=mid
        else:lo=mid
    alpha=hi
    # Rational certified pi bracket and sin(x)>=x-x^3/6 on [0,pi/2].
    pi_lo=F('3.14159265358979323846264338327950288')
    pi_hi=F('3.14159265358979323846264338327950289')
    sinlo=pi_lo*h/2-(pi_hi*h/2)**3/6
    gap=8*sinlo**2
    p=dict(instance_id=a['version']+'-normalized-state-only',N=N,kappa=str(8*C/gap),
           effective_inverse_gap=str(F(alpha)/gap),epsilon_state='0.00001',delta='0.01')
    meta=dict(m=m,beta=str(beta),frobenius_squared=str(frob2),frobenius_integer_upper=alpha,
              scaled_gap_lower=str(gap),scalar_output_covered=False)
    return p,meta


def validate():
    tests=[]
    for a in range(1,200):
        for b in [1,3,17,128]:
            x=F(a,b);c=clog2(x)
            assert pow2(c-1)<x<=pow2(c)
    tests.append('exact rational logarithmic ceilings, including powers of two and subunit inputs')
    for N,k,e,d in [(2,1,'0.1','0.1'),(16,320,'0.001','0.01'),(1024,100,'0.01','0.01'),(10000,1000000,'0.000001','0.0001')]:
        s=schedule(dict(N=N,kappa=k,epsilon_state=e,delta=d));g=s['gamma'];Q=s['query_cap'];C=s['cycle_cap'];H=s['rotation_slots'];J=s['injection_cap'];P=s['resource_attempt_cap'];b=s['resource_bits']
        assert s['cycle_success_lower']*C>=clog2(1/s['solver_abort_allowance'])
        assert pow2(-clog2(1/s['solver_abort_allowance']))<=s['solver_abort_allowance']
        assert 12*s['n']*Q*pow2(-s['angle_bits'])<=g
        assert 2*s['h']*Q*Q*pow2(-s['norm_log_grid_bits'])<=g*g/4
        assert 2*C*pow2(-s['norm_mixture_bits'])<=g/2
        assert H*pow2(-J)<=g
        assert H*J*pow2(-P//16)<=g
        assert 2*H*J*pow2(-b)<=g
        assert s['trace_error_upper']<=F(e) and s['abort_probability_upper']<=F(d)
        assert s['T_upper']==s['structural_T']+s['injection_T']
    tests.append('all six cap/error inequalities verified with exact rational arithmetic at four parameter points')
    # Prefix-cube comparator: disjoint cubes, no carry approximation.
    for b in range(1,7):
        M=1<<b
        for threshold in range(M+1):
            for j in range(M):
                if threshold==M:active=1
                else:
                    active=sum(1 for bit in range(b) if ((threshold>>bit)&1) and
                               (j>>(bit+1))==(threshold>>(bit+1)) and not ((j>>bit)&1))
                assert active==int(j<threshold)
    tests.append('complete prefix-comparator truth tables through six bits, including thresholds 0 and 2^b')
    import numpy as np
    worst=0
    for b in [2,3,4,5]:
        M=1<<b
        for theta in np.linspace(-math.pi,math.pi,33):
            c=int(round(M*math.cos(theta)));ss=int(round(M*math.sin(theta)))
            # Sum actual uniform branch/address amplitudes surviving flag=1,
            # then Hadamard/postselect branch+address zero.
            out=np.zeros(2,dtype=complex)
            for branch in range(4):
                for j in range(M):
                    passes=(branch==0 or branch==1 and j<abs(c) or branch==2 and j<abs(ss))
                    if not passes:continue
                    target=int(branch in [1,2])
                    phase=1 if branch==0 else (1 if c>=0 else -1) if branch==1 else 1j*(1 if ss>=0 else -1)
                    out[target]+=phase/(4*M)
            want=np.array([1,(c+1j*ss)/M])/4
            assert np.linalg.norm(out-want)<1e-12
            success=float(np.vdot(out,out).real)
            assert success>=1/16-1e-14
            state=out/np.linalg.norm(out)
            ideal=np.array([1,np.exp(1j*theta)])/math.sqrt(2)
            distance=float(np.linalg.norm(state-ideal));worst=max(worst,distance*M)
            assert distance<=2/M+1e-12
    tests.append('132 explicit phase-resource branch sums: amplitudes, success>=1/16, state error<=2/2^b')
    for theta in [.2,1.1,-2.3]:
        psi=np.array([math.sqrt(.3),1j*math.sqrt(.7)])
        for fails in range(5):
            out=psi.copy()
            for j in range(fails):out=np.diag([np.exp(1j*(2**j)*theta),1]).dot(out)
            out=np.diag([1,np.exp(1j*(2**fails)*theta)]).dot(out)
            desired=np.diag([1,np.exp(1j*theta)]).dot(psi)
            assert abs(abs(np.vdot(out,desired))-1)<1e-12
    tests.append('angle-doubling injection recovers desired gate after zero through four failed outcomes')
    # Direct finite log-grid Holder inequality check, endpoints included.
    for s in [0,.00001,.1,1,10]:
        for step in [.000001,.001,.1]:
            diff=abs(math.acos(math.exp(-s-step))-math.acos(math.exp(-s)))
            assert diff<=math.sqrt(2*step)+1e-12
    tests.append('endpoint-inclusive numerical checks of the proved norm-angle Holder bound')
    p=dict(N=256,kappa=100,epsilon_state='0.01',delta='0.01')
    base=f(p)
    for change in [dict(N=1024),dict(kappa=1000),dict(epsilon_state='0.001'),dict(delta='0.001')]:
        assert f(dict(p,**change))>=base
    for change in [dict(N=1),dict(kappa=0),dict(epsilon_state=0),dict(delta='nan'),dict(rho_upper=2,effective_inverse_gap=10)]:
        try:schedule(dict(p,**change))
        except (ValueError,OverflowError):pass
        else:raise AssertionError('invalid input accepted')
    tests.append('resource monotonicity and rejection of invalid/ambiguous inputs')
    return tests,worst


def main():
    p=dict(instance_id='generic-real-stored-data',N=1024,kappa=100,epsilon_state='0.01',delta='0.01')
    ap,meta=app_input()
    write('input.json',p);write('application-input.json',ap);write('application-normalization.json',meta)
    results=[estimate(p),estimate(ap)]
    write('output.json',results[0]);write('application-output.json',results[1])
    checks,worst=validate()
    write('validation.json',dict(result='passed',checks=checks,python=platform.python_version(),max_phase_resource_error_times_2_to_b=worst,
          scope='Exact schedule inequalities and small component simulations; mathematical proof is in the report, not inferred from sampling.'))
    with (HERE/'sensitivity.csv').open('w') as handle:
        w=csv.writer(handle);w.writerow(['N','kappa','epsilon_state','delta','K','query_cap','rotation_T_upper','T_upper'])
        for N in [16,256,1024,16384]:
            for k in [10,100,1000]:
                for eps in ['0.01','0.001']:
                    x=estimate(dict(N=N,kappa=k,epsilon_state=eps,delta='0.01'))
                    w.writerow([N,k,eps,'.01',x['K'],x['query_cap'],x['rotation_T_upper'],x['T_upper']])
    rows=[]
    for title,x in zip(['Generic example','Diffusion matrix'],results):
        s=schedule(x['parameters'])
        rows.append('{} & {} & {:.5g} & {} & {} & {} \\\\'.format(title,s['N'],float(s['K']),s['angle_bits'],s['resource_bits'],s['injection_cap']))
    (HERE/'parameter-table.tex').write_text('\n'.join(rows)+'\n\\bottomrule\n')
    (HERE/'numbers.tex').write_text('\\newcommand{\\GenericT}{'+str(results[0]['T_upper'])+'}\n'+
        '\\newcommand{\\ApplicationT}{'+str(results[1]['T_upper'])+'}\n'+
        '\\newcommand{\\GenericQ}{'+str(results[0]['query_cap'])+'}\n')
    paths=[HERE/'upper_bound.py',HERE/'reproduce.py',HERE.parent/'t_count.py',HERE.parent/'t-count-model.md',HERE.parent.parent/'02-application/instance.json']
    paths+=list((HERE.parent/'sources').glob('*.pdf'))+list((HERE.parent/'sources').glob('*.html'))
    write('input-manifest.json',dict(version=VERSION,date_utc='2026-09-14',inputs_sha256={str(x.relative_to(HERE.parent.parent)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}))
    print(json.dumps(dict(checks=len(checks),generic_T=results[0]['T_upper'],diffusion_T=results[1]['T_upper']),indent=2))


if __name__=='__main__':main()
