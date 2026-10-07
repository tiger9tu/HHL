"""Callable Shortcut + stored-real-data block-encoding T-count estimator.

Usage: python3 t_count.py parameters.json
API: f(p) -> modeled expected logical T gates per solution-state preparation.
No numpy, Q#, quantum compiler, or network needed. See t-count-model.md.
"""
import json
import math
import sys

VERSION = '04-T-count-v1.0.0'


def real(x, name, low, high=None):
    if isinstance(x, bool) or not isinstance(x, (float, int)) or not math.isfinite(x):
        raise ValueError(name + ' must be finite numeric')
    if x < low or (high is not None and x > high):
        raise ValueError(name + ' is outside the supported range')
    return float(x)


def integer(x, name, low=0):
    y = real(x, name, low)
    if int(y) != y:
        raise ValueError(name + ' must be integer')
    return int(y)


def mcx_t(controls):
    """Exact clean-ancilla ladder: 2c-3 Toffolis, 7 T each (c>=2)."""
    c = integer(controls, 'controls')
    return 0 if c < 2 else 7*(2*c-3)


def be_resources(n, angle_bits, rotation_t):
    """Clader v1 Tables 1/3, minimum-count select-swap, plus control allowance.

    Control allowance is our conservative construction count (not Table 1).
    R is T gates per synthesized one-qubit rotation, not rotation count.
    """
    n=integer(n,'n',1); t=integer(angle_bits,'angle_bits',1)
    R=integer(rotation_t,'rotation_t',1); D=2**n
    words=(D-1)*t+D  # (D-1) angle words + D sign bits
    A=8*(2*t+3)*D-16*t*(n+1)+4*R*n*t-24
    b=8*(t+1)*(D-1)+2*t*n*R-8*t*n
    # Gate then ungate both state-preparation data trees (4 registers);
    # gate/ungate one RHS tree (2 registers). Exact Fredkin = 7 T.
    cA=A+28*words+7*n
    cb=b+14*words
    W=D*(t+1)+3*n-t+1
    return dict(dimension=D,index_qubits=n,angle_bits=t,rotation_T=R,
                data_tree_bits=words,A_uncontrolled_T=A,b_uncontrolled_T=b,
                A_controlled_T=cA,b_controlled_T=cb,
                A_control_allowance_T=28*words+7*n,
                b_control_allowance_T=14*words,
                published_uncontrolled_BE_qubits=W)


def shortcut_queries(K, epsilon_algorithm, policy='auto'):
    """Dalzell Algorithm 3 Eq118; Costa Eq19 only within its inherited domain."""
    K=real(K,'K',1); e=real(epsilon_algorithm,'epsilon_algorithm',1e-15,.1)
    K=max(3.,K)  # harmless loose gap promise; avoid K=1 special case
    logK=math.log(K)
    # log((K^2+1)/2), without forming K^2
    S=3+2*(2*logK+math.log1p(K**-2)-math.log(2))
    mu=.25
    eta=mu/(math.sqrt(S)+mu)
    eta_kp=e*math.sqrt(1-mu*mu)/(mu*math.sqrt(1-e*e))
    dkr=2*int(math.ceil(K*math.log(2/eta)/2))
    dkp=2*int(math.ceil(K*math.log(2/eta_kp)/2))
    attempts_kr=((1+eta)/(1-eta))**2*(logK+1)
    attempts_kp=1/(1-mu*mu)
    exact=dkr*attempts_kr+dkp*attempts_kp
    simple=K*(6*logK+6+1.07*math.log(1/e))+6+3*logK if K<=1e6 else None
    if policy not in ['auto','eq19','eq118']:
        raise ValueError('query_bound must be auto, eq19, or eq118')
    if policy=='eq19' and simple is None:
        raise ValueError('Eq19 inherits 3 <= K <= 1e6; use auto or eq118')
    use_simple=(policy=='eq19' or (policy=='auto' and simple is not None))
    return dict(K=K,epsilon_algorithm=e,eta_KR=eta,eta_KP=eta_kp,
                degree_KR=dkr,degree_KP=dkp,expected_KR_attempts_bound=attempts_kr,
                expected_KP_attempts_bound=attempts_kp,
                cycle_success_lower_bound=1/attempts_kr,
                eq118_expected_A_queries_bound=exact,eq19_expected_A_queries_bound=simple,
                expected_A_queries_bound=simple if use_simple else exact,
                bound_used='Costa Eq19' if use_simple else 'Dalzell Eq118')


def estimate(p):
    allowed={'N','kappa','epsilon_state','frobenius_over_spectral','effective_inverse_gap','delta_retry',
             'query_bound','rotation_synthesis_offset','rotation_T_override',
             'rotation_override_certificate','angle_bits_min','instance_id'}
    extra=set(p)-allowed
    if extra:
        raise ValueError('unknown parameters: '+', '.join(sorted(extra)))
    N=integer(p['N'],'N',2)
    n=(N-1).bit_length(); D=2**n
    k=real(p['kappa'],'kappa',1)
    eps=real(p.get('epsilon_state',.01),'epsilon_state',2e-15,.1)
    rho=real(p.get('frobenius_over_spectral',math.sqrt(D)),
             'frobenius_over_spectral',1,math.sqrt(D)*(1+1e-12))
    delta=real(p.get('delta_retry',.002),'delta_retry',1e-15,.1)
    if 'effective_inverse_gap' in p and 'frobenius_over_spectral' in p:
        raise ValueError('supply effective_inverse_gap OR frobenius_over_spectral, not both')
    K=real(p['effective_inverse_gap'],'effective_inverse_gap',1) if 'effective_inverse_gap' in p else k*rho
    q=shortcut_queries(K,eps/2,p.get('query_bound','auto'))
    Q=q['expected_A_queries_bound']
    # A cycle is one fresh random norm guess + KR + (on success) KP.
    # Bounding every cycle by both full sequences is conservative.
    cap=int(math.ceil(math.log(delta)/math.log1p(-q['cycle_success_lower_bound'])))
    Qcap=cap*(q['degree_KR']+q['degree_KP'])
    # Four error allowances per query slot: A, b, b†, wrapper/QSVT rotations.
    # The prefactor also leaves slack for conditioning on capped delivery.
    nu=(eps/2)*(1-delta)/(32*Qcap)
    t=max(1,integer(p.get('angle_bits_min',1),'angle_bits_min',1),
          int(math.ceil(math.log2(2*math.pi*n/nu))))
    rotation_tol=nu/(8*t*n)
    offset=integer(p.get('rotation_synthesis_offset',10),'rotation_synthesis_offset')
    R=int(math.ceil(3*math.log2(1/rotation_tol)+offset))
    synthesis='modeled ceil(3 log2(1/delta_rotation) + offset); not a certified synthesis bound'
    if 'rotation_T_override' in p:
        if not p.get('rotation_override_certificate'):
            raise ValueError('rotation_T_override requires rotation_override_certificate')
        R=integer(p['rotation_T_override'],'rotation_T_override',1)
        synthesis='user-supplied uniform rotation bound; certificate not independently verified'
    be=be_resources(n,t,R)
    n_pad=n+1
    # Conservative implementation upper envelope, no ancilla recycling assumed:
    # original W, two extra data trees, augmentation/control flags.
    W=be['published_uncontrolled_BE_qubits']+2*be['data_tree_bits']+n+8
    # G_t: cA+cb+cb† and controlled Ry; a conservative six-test allowance
    # includes augmentation, projection and preparation/herald endpoints.
    # QSVT uses two projector-NOTs and one phase rotation per query.
    # Reserve a further 2R for optional Frobenius rescaling/augmentation details.
    parts=dict(matrix_queries_T=Q*be['A_controlled_T'],
               rhs_queries_T=2*Q*be['b_controlled_T'],
               system_tests_T=Q*6*mcx_t(n_pad),
               qsvt_projectors_T=Q*2*mcx_t(W),
               wrapper_and_qsvt_rotations_T=Q*5*R)
    slot=(be['A_controlled_T']+2*be['b_controlled_T']+
          6*mcx_t(n_pad)+2*mcx_t(W)+5*R)
    total=Q*slot
    return dict(model_version=VERSION,parameters=p,
                statistic='modeled expected logical T count per delivered normalized solution state',
                T_count=total,T_count_ceiling=int(math.ceil(total)),
                per_query_slot_T=slot,components=parts,block_encoding=be,query_model=q,
                normalization=dict(original_N=N,padded_dimension=D,kappa_bound=k,
                    frobenius_over_spectral_bound=None if 'effective_inverse_gap' in p else rho,
                    rho_source=('bypassed by certified direct inverse-gap input' if 'effective_inverse_gap' in p else
                        'supplied bound' if 'frobenius_over_spectral' in p else 'sqrt(D) worst case'),
                    effective_inverse_gap=q['K']),
                precision=dict(epsilon_state_requested=eps,epsilon_algorithm=eps/2,
                    implementation_allowance=eps/2,delta_retry=delta,
                    ideal_cycle_cap=cap,query_slots_cap=Qcap,unitary_tolerance_per_component=nu,
                    angle_rounding_bound=math.pi*n*2.**(-t),
                    rotation_tolerance=rotation_tol,
                    BE_unitary_error_design_bound=math.pi*n*2.**(-t)+4*t*n*rotation_tol,
                    rotation_synthesis_model=synthesis,rotation_synthesis_offset=offset),
                capped_T_allocation_model=Qcap*slot,
                conservative_logical_qubit_allocation=3*W+2*n_pad+20,
                logical_depth=None,T_depth=None,qec_ready=False,
                certified_end_to_end=False,
                excludes=['classical table/phase generation and storage','scientific scalar readout and norm recovery',
                          'QEC and physical overhead'],
                notes=['Internal ideal solver retries included once in Q; no extra 1/p factor.',
                       'Clader minimum-count Frobenius BE; does not exploit sparse/PDE structure.',
                       'Expected query bound is rigorous under ideal access; total T is a resource model.',
                       'Norm-guess discretization, phase generation, and implemented adaptive success require certification.',
                       'Ceiling of an expectation is not a high-probability resource cap.'])


def f(p):
    """Return modeled expected logical T count. estimate(p) returns the audit trail."""
    return estimate(p)['T_count']


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python3 t_count.py parameters.json')
    with open(sys.argv[1]) as handle:
        result=estimate(json.load(handle))
    print(json.dumps(result,indent=2,allow_nan=False))
