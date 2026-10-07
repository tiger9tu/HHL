"""Dalzell et al., arXiv:2211.12489v1, Tables III--V (Python >=3.11).

Finite numerical paper model, NOT a certified circuit upper bound. Source tables
suppress subleading synthesis terms and the numerical Q model drops O(sqrt(K)).
Self-contained snapshot of the task-04 Table-V model with logical width added.
f(p) returns T count; estimate(p) also returns peak logical circuit qubits.
State-only and optional full-vector tomography are separate output workloads.
"""
from decimal import Decimal as D, localcontext, ROUND_CEILING
import json
import sys

VERSION = 'clean-modern-qlsa-1.0.0'


def dec(x):
    if isinstance(x, bool):
        raise ValueError('boolean is not a numeric parameter')
    y = D(str(x))
    if not y.is_finite():
        raise ValueError('parameters must be finite')
    return y


def ceiling(x):
    return int(x.to_integral_value(rounding=ROUND_CEILING))


def log2(x):
    return x.ln()/D(2).ln()


def table_v(N, Q, d, epsilon_G, epsilon_h, epsilon_ar, epsilon_z,
            epsilon_tsp=None):
    """Literal Table-V T-count rows with Tables III/IV substituted.

    All arithmetic uses Decimal at the caller's precision. N must be a power
    of two. No solver schedule, retries, rounding or error allocation is hidden.
    The controlled row refers to the tomography sign circuit in Eq.(47).
    """
    if not isinstance(N, int) or N < 2 or N & (N-1):
        raise ValueError('table_v N must be a power of two >=2')
    ell=N.bit_length()-1
    Q,d=dec(Q),dec(d)
    if Q<=0 or d<=0:
        raise ValueError('Q and d must be positive')
    errors=[dec(x) for x in (epsilon_G,epsilon_h,epsilon_ar,epsilon_z)]
    if any(not 0<x<=1 for x in errors):
        raise ValueError('component errors must lie in (0,1]')
    eG,eh,ear,ez=errors
    aG,ah,aar,az=[log2(1/x) for x in errors]
    Tbe=(12*aG+56)*N*N-24*N-12*aG-32*ell-32
    Tcbe=Tbe+16*(N-1)
    Tsp=(12*ah+40)*N-12*ah-16*ell-40
    terms=dict(controlled_block_encoding=2*(Q+d)*Tcbe,
               rhs_preparation=4*(Q+d)*Tsp,
               adiabatic_rotations=12*Q*aar,
               adiabatic_other=Q*(24*ell+31),
               filter_rotations=3*d*az,
               filter_other=d*(32*ell-2))
    out=dict(T_BE=Tbe,T_controlled_BE=Tcbe,T_SP=Tsp,
             matrix_calls=2*(Q+d),rhs_calls=4*(Q+d),
             QLSS_terms=terms,T_QLSS=sum(terms.values()))
    if epsilon_tsp is not None:
        etsp=dec(epsilon_tsp)
        if not 0<etsp<=1:
            raise ValueError('epsilon_tsp must lie in (0,1]')
        out['T_controlled_QLSS']=(out['T_QLSS']+20*Q+3*d*az
                                 +12*(N-1)*log2(1/etsp)+16*(N-ell-1))
    return out


def _estimate(p):
    allowed={'N','kappa','epsilon_state','delta','frobenius_over_spectral',
             'effective_inverse_gap','adiabatic_constant'}
    if set(p)-allowed:
        raise ValueError('unknown parameters: '+str(sorted(set(p)-allowed)))
    Nq=dec(p['N'])
    if Nq!=Nq.to_integral_value() or Nq<2:
        raise ValueError('N must be an integer >=2')
    N=int(Nq);ell=(N-1).bit_length();L=1<<ell
    k=dec(p['kappa']);eps=dec(p.get('epsilon_state','0.01'));delta=dec(p.get('delta','0.01'))
    C=dec(p.get('adiabatic_constant',2000))
    if k<1 or not 0<eps<=D('0.1') or not 0<delta<1 or C<=0:
        raise ValueError('require kappa>=1, 0<epsilon_state<=0.1, 0<delta<1, C>0')
    if 'effective_inverse_gap' in p and 'frobenius_over_spectral' in p:
        raise ValueError('specify inverse gap OR Frobenius/spectral ratio')
    rho=dec(p['frobenius_over_spectral']) if 'frobenius_over_spectral' in p else D(L).sqrt()
    if rho<1:
        raise ValueError('Frobenius/spectral ratio must be >=1')
    K=dec(p['effective_inverse_gap']) if 'effective_inverse_gap' in p else k*rho
    if K<1:
        raise ValueError('effective inverse gap must be >=1')
    # Eq.(66), with the paper's default assumed C=2000; omitted term NOT bounded.
    Q=ceiling(2*C*K)
    share=eps/5
    eps_qsp=share
    # Eq.(67), rounded up to an even filter degree; this is an explicit adapter choice.
    d=2*ceiling(K*(2/eps_qsp).ln())
    eG=share/(2*(Q+d));eh=share/(4*(Q+d))
    ear=share/(4*Q);ez=share/(2*d)  # use 2d from Eq.(64), not d in Eq.(65)
    tab=table_v(L,Q,d,eG,eh,ear,ez)
    attempts=1
    while D(2)**(-attempts)>delta:
        attempts+=1
    per_run=ceiling(tab['T_QLSS'])
    # Raw formula is noninteger. Ceiling is a reporting convention, not certification.
    return dict(model_version=VERSION,parameters=p,N=N,padded_dimension=L,ell=ell,
                kappa=k,frobenius_over_spectral=None if 'effective_inverse_gap' in p else rho,
                effective_inverse_gap=K,adiabatic_constant=C,Q=Q,d=d,
                precision=dict(epsilon_qsp=eps_qsp,epsilon_G=eG,epsilon_h=eh,
                               epsilon_ar=ear,epsilon_z=ez),
                equation_64_error=eps_qsp+2*(Q+d)*eG+4*(Q+d)*eh+4*Q*ear+2*d*ez,
                **tab,T_per_attempt_ceiling=per_run,retry_cap=attempts,
                ideal_retry_failure_bound=D(2)**(-attempts),
                T_retry_budget=attempts*per_run,
                expected_T_upper_under_half_success_model=2*per_run,
                statistic='Table-V model, rounded per attempt and multiplied by a retry cap',
                certified_upper_bound=False,
                assumptions=['kappa denotes ordinary spectral condition bound; Frobenius normalization explicit',
                             'C=2000 by default is the paper numerical assumption for general matrices',
                             'Q=2CK drops the paper O(sqrt(K)) term',
                             'Tables III/IV omit double/triple logarithmic synthesis terms',
                             'R_T=3 log2(1/error) is the paper synthesis model, not a compiled certificate',
                             'five equal Eq.(64) error contributions and even degree ceiling are adapter choices',
                             'retry cap assumes independent attempts with success probability >=1/2; not recertified after circuit errors'],
                excludes=['tomography','interior point iterations','classical preprocessing','QEC'])


def _with_readout(p):
    """Optional full real-vector tomography; reuse failed-flag samples as in paper."""
    original_parameters=dict(p)
    p=dict(p)
    enabled=p.pop('include_readout',False)
    if not isinstance(enabled,bool):
        raise ValueError('include_readout must be a boolean')
    xi_input=p.pop('epsilon_readout',None)
    delta_input=p.pop('delta_readout',None)
    if not enabled and (xi_input is not None or delta_input is not None):
        raise ValueError('readout parameters require include_readout=True')
    base=_estimate(p)
    base.update(parameters=original_parameters,include_readout=enabled,T_total=base['T_retry_budget'],
                output_scope='normalized quantum solution state',readout=None)
    if not enabled:
        return base
    xi=dec(xi_input if xi_input is not None else p.get('epsilon_state','0.01'))
    delta=dec(delta_input if delta_input is not None else p.get('delta','0.01'))
    if not 0<xi<=D('0.1') or not 0<delta<1:
        raise ValueError('require 0<epsilon_readout<=0.1 and 0<delta_readout<1')
    L=base['padded_dimension']
    # Our total-output allocation: 90% sampling, 5% solver, 5% reference prep.
    sampling=D('0.9')*xi
    core_eps=min(dec(p.get('epsilon_state','0.01')),D('0.05')*xi/D('1.58'))
    tsp=D('0.05')*xi/(D('1.58')*D(L).sqrt())
    core=_estimate(dict(p,epsilon_state=str(core_eps)))
    prec=core['precision']
    costs=table_v(L,core['Q'],core['d'],prec['epsilon_G'],prec['epsilon_h'],
                  prec['epsilon_ar'],prec['epsilon_z'],tsp)
    samples=ceiling(D('57.5')*L*(D(6)*L/delta).ln() /
                    (sampling*sampling*(1-sampling*sampling/4)))
    plain=ceiling(costs['T_QLSS']);controlled=ceiling(costs['T_controlled_QLSS'])
    applicability=sampling+D(2*L).sqrt()*tsp+D(2).sqrt()*core_eps
    if applicability>D('0.5'):
        raise ValueError('Proposition 4 applicability condition violated')
    total=samples*(plain+controlled)
    base.update(output_scope='classical approximation to the full real normalized solution vector',
                T_total=total,
                statistic='Table-V model with full-vector tomography; no separate retry multiplier',
                excludes=['solution norm recovery','scientific scalar readout','interior point iterations','classical preprocessing and reconstruction','QEC'])
    base['readout']=dict(mode='paper_full_vector_tomography',epsilon_output_target=xi,
        delta_readout=delta,epsilon_sampling=sampling,epsilon_state_used=core_eps,
        epsilon_tsp=tsp,output_error_model=sampling+D('1.58')*D(L).sqrt()*tsp+D('1.58')*core_eps,
        proposition_4_lhs=applicability,samples_per_family=samples,total_circuit_executions=2*samples,
        Q=core['Q'],d=core['d'],precision=prec,T_plain_per_execution=plain,
        T_controlled_per_execution=controlled,T_magnitude_samples=samples*plain,
        T_sign_samples=samples*controlled,T_one_solver_execution=plain,
        T_additional_after_one_execution=(samples-1)*plain+samples*controlled,
        T_total=total,retry_multiplier_applied=1)
    base['assumptions'] += [
        'optional readout is the paper full real-vector tomography, not scalar readout',
        '90/5/5 output-error split is our adapter choice; solver precision may be tightened',
        'tomography sample formula already includes unsuccessful solver flags; no factor 7 or 1/p added',
        'readout probability/error claim inherits source ideal-success and synthesis-model assumptions',
        'top-level Q,d,precision,T_retry_budget describe the unchanged state-only baseline; readout fields describe the retuned workload']
    return base


def estimate(p):
    with localcontext() as ctx:
        ctx.prec=80
        out=_with_readout(p)
        L=out['padded_dimension'];ell=out['ell']
        n_be=4*L*L-3*L+2*ell-1
        n_cbe=n_be+L
        n_qlss=n_cbe+5
        n_controlled=n_cbe+6
        peak=n_controlled if out['include_readout'] else n_qlss
        out.update(logical_qubits_peak=peak,
                   logical_qubits_by_circuit=dict(block_encoding=n_be,
                       controlled_block_encoding=n_cbe,rhs_preparation=4*L+ell-6,
                       qlss=n_qlss,controlled_qlss=n_controlled),
                   execution_policy='serial attempts/samples with reused circuit workspace',
                   algorithm='discrete_adiabatic_qlsa_with_eigenstate_filtering',
                   access_model='dense_minimum_depth_frobenius_block_encoding',
                   qec_input=dict(T_count=out['T_total'],logical_qubits=peak,
                       T_depth=None,Clifford_count=None,measurement_depth=None,
                       count_statistic=out['statistic'],certified_upper_bound=False),
                   source='https://arxiv.org/pdf/2211.12489v1',
                   qubit_scope='logical circuit allocation only; excludes QEC, routing allocation and magic-state factories')
    def clean(x):
        if isinstance(x,D):return str(x)
        if isinstance(x,dict):return {k:clean(v) for k,v in x.items()}
        if isinstance(x,list):return [clean(v) for v in x]
        return x
    return clean(out)


def f(p):
    """Return selected T estimate: state preparation, or optional full-vector readout."""
    return estimate(p)['T_total']


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Usage: python3.11 modern_qlsa.py input.json')
    with open(sys.argv[1]) as handle:
        print(json.dumps(estimate(json.load(handle)),indent=2))
