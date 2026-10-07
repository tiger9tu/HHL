"""Finite sufficient Clifford+T budget for capped Shortcut state preparation.

All schedule/count arithmetic is exact integer or Fraction arithmetic. No fitted
synthesis constant, big-O term, floating-point ceiling, or number-theory hypothesis.
See modern-qlsa-t-count.tex for the constructive protocol and correctness proof.
"""
from fractions import Fraction as F
import json
import sys

VERSION='04-sufficient-T-v2.0.0'


def frac(x):
    if isinstance(x,bool):
        raise ValueError('booleans are not parameters')
    return F(str(x))


def ceilq(x):
    x=F(x)
    return -(-x.numerator//x.denominator)


def clog2(x):
    """Exact ceil(log2(x)) for positive rational x."""
    x=F(x)
    if x<=0:
        raise ValueError('log argument must be positive')
    a,b=x.numerator,x.denominator
    k=a.bit_length()-b.bit_length()
    if (a <= b*(1<<k)) if k>=0 else (a*(1<<(-k)) <= b):
        return k
    return k+1


def pow2(k):
    return F(1<<k) if k>=0 else F(1,1<<(-k))


def mcx(c):
    return 0 if c<2 else 7*(2*c-3)


def schedule(p):
    allowed={'N','kappa','epsilon_state','delta','rho_upper','effective_inverse_gap','instance_id'}
    if set(p)-allowed:
        raise ValueError('unknown parameter(s): '+str(sorted(set(p)-allowed)))
    Nq=frac(p['N'])
    if Nq.denominator!=1 or Nq<2:
        raise ValueError('N must be an integer >=2')
    N=int(Nq);n=(N-1).bit_length();D=1<<n
    k=frac(p['kappa']);eps=frac(p.get('epsilon_state','0.01'));delta=frac(p.get('delta','0.01'))
    if k<1 or not 0<eps<=F(1,10) or not 0<delta<=F(1,10):
        raise ValueError('require kappa>=1 and 0<epsilon_state,delta<=0.1')
    if 'rho_upper' in p and 'effective_inverse_gap' in p:
        raise ValueError('choose rho_upper OR effective_inverse_gap')
    rho=frac(p.get('rho_upper',1<<((n+1)//2)))
    if rho<1:
        raise ValueError('rho_upper must be >=1')
    supplied_K=frac(p['effective_inverse_gap']) if 'effective_inverse_gap' in p else k*rho
    if supplied_K<1:
        raise ValueError('inverse gap must be >=1')
    K=max(F(3),supplied_K)
    h=clog2(K)
    eta=F(1,8*(3+4*h));eta_kp=eps/2
    # ln(x)<=ceil(log2(x)) when x>=1, so these are sufficient even degrees.
    dkr=2*ceilq(K*clog2(2/eta)/2)
    dkp=2*ceilq(K*clog2(2/eta_kp)/2)
    r=((1-eta)/(1+eta))**2/F(h+1)
    delta_s=delta/4
    C=ceilq(F(clog2(1/delta_s))/r)
    Q=C*(dkr+dkp)
    gamma=min(eps*(1-delta_s)/64,delta/16)
    # Matrix/RHS angle-rounding errors: 3*pi*n*Q*2^-t <12*n*Q*2^-t.
    t=max(1,clog2(F(12*n*Q)/gamma))
    L=(D-1)*t+D
    A0=8*(2*t+3)*D-16*t*(n+1)-24
    b0=8*(t+1)*(D-1)-8*t*n
    cA0=A0+28*L+7*n
    cb0=b0+14*L
    W=D*(t+1)+3*n-t+1+2*L+n+8
    structural_slot=cA0+2*cb0+6*mcx(n+1)+2*mcx(W)
    rotations_slot=8*n*t+5
    H=Q*rotations_slot
    # Each axial rotation is injected at most J times. Every phase resource
    # is prepared with at most P attempts of an exact Clifford+Toffoli circuit.
    J=max(1,clog2(F(H)/gamma))
    P=16*max(1,clog2(F(H*J)/gamma))
    b=max(1,clog2(F(4*H*J)/gamma))
    resource_T=7+2*b*mcx(b+2)
    rotation_T=J*P*resource_T
    structural_T=Q*structural_slot
    injection_T=H*rotation_T
    # Norm log-grid and dyadic mixture probabilities, both generated classically.
    norm_bits=max(1,clog2(F(8*h*Q*Q)/(gamma*gamma)))
    mixture_bits=max(1,clog2(F(4*C)/gamma))
    e=5*gamma
    state_bound=eps/2+2*e/(1-delta_s-e)
    abort_bound=delta_s+e
    assert state_bound<=eps and abort_bound<=delta
    return dict(N=N,n=n,D=D,kappa=k,rho_upper=None if 'effective_inverse_gap' in p else rho,K=K,h=h,
                epsilon_state=eps,delta=delta,eta_KR=eta,eta_KP=eta_kp,
                degree_KR=dkr,degree_KP=dkp,cycle_success_lower=r,
                solver_abort_allowance=delta_s,cycle_cap=C,query_cap=Q,
                gamma=gamma,angle_bits=t,data_tree_bits=L,workspace_envelope=W,
                structural_T_per_slot=structural_slot,rotations_per_slot=rotations_slot,
                rotation_slots=H,injection_cap=J,resource_attempt_cap=P,
                resource_bits=b,resource_attempt_T=resource_T,rotation_T_upper=rotation_T,
                structural_T=structural_T,injection_T=injection_T,
                T_upper=structural_T+injection_T,
                norm_log_grid_bits=norm_bits,norm_mixture_bits=mixture_bits,
                trace_error_upper=state_bound,abort_probability_upper=abort_bound,
                logical_qubit_allocation=3*W+2*(n+1)+4*b+30)


def f(p):
    """Integer worst-path T budget; successful ensemble error <=eps, abort<=delta."""
    return schedule(p)['T_upper']


def estimate(p):
    s=schedule(p)
    out={k:(str(v) if isinstance(v,F) else v) for k,v in s.items()}
    out.update(model_version=VERSION,scope='one normalized solution state',
               statistic='deterministic sufficient T cap, including heralded synthesis attempts',
               assumptions=['certified gap/normalization for a real nonsingular input',
                            'ideal logical Clifford, T, measurement and reset operations',
                            'certified classical angle/phase preprocessing; cost excluded'],
               excludes=['classical preprocessing and memory','scientific output extraction','QEC'],
               reference='modern-qlsa-t-count.tex',parameters=p)
    return out


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python3 upper_bound.py input.json')
    with open(sys.argv[1]) as handle:
        print(json.dumps(estimate(json.load(handle)),indent=2))
