"""Task-local ideal-oracle resource bounds; no implicit gate or hardware prices.

Reference: Dalzell, arXiv:2406.12086v2, Theorems 1 and 4.
Python 3.6+, standard library only. Counts are per indicated solver invocation.
"""
import json
import math
import sys


def number(x, name, lower, upper=None):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
        raise ValueError(name + ' must be finite numeric')
    if x < lower or (upper is not None and x > upper):
        raise ValueError(name + ' outside supported range')
    return x


def evaluate(c):
    pp, cq = c['pp'], c['cq']
    N = number(pp['N'], 'N', 1)
    if int(N) != N:
        raise ValueError('N must be an integer')
    for key in ['s_row', 's_col']:
        s = number(pp[key], key, 1, N)
        if int(s) != s:
            raise ValueError(key + ' must be integer')
    kappa = number(pp['kappa_2'], 'kappa_2', 1)
    norm = number(cq['operator_norm'], 'operator_norm', 1e-300)
    alpha = number(cq['block_encoding_alpha'], 'block_encoding_alpha', norm)
    # Requires certified norm, condition and alpha bounds as explained in model.md.
    K = alpha / norm * kappa
    number(K, 'effective inverse gap', 1)
    eps = number(cq['epsilon_trace_algorithm'], 'epsilon_trace_algorithm', 1e-15, .1)
    n_pad = int(N).bit_length()  # ceil(log2(N+1)), reserves augmentation basis state
    base = dict(model_version='04-v1.0.0', effective_inverse_gap=K,
                original_kappa_2=kappa, n_padded=n_pad,
                epsilon_trace_algorithm=eps, queries_expanded=False,
                compiled_T_count=None, compiled_Clifford_count=None,
                depth=None, t_depth=None, logical_qubits_peak=None,
                qec_ready=False, benchmark_reconciled=False)
    if cq['mode'] == 'unknown_norm_optimal':
        # Avoid degenerate J=0 path in Algorithm 4. A larger gap bound is valid.
        K = max(2.0, K)
        Q = 56*K + 1.05*K*(.5*math.log1p(-eps*eps)-math.log(eps)) + 2.78*math.log(K)**3 + 3.17
        base.update(algorithm='Dalzell v2 Algorithm 4 / Theorem 4 Eq. 133',
                    theorem_gap_bound=K, statistic='upper bound on expectation',
                    A_queries=Q, b_queries=2*Q,
                    internal_retries_included=True,
                    output_certificate='trace distance of ensemble, ideal access',
                    norm_setup_separable=False)
    elif cq['mode'] == 'certified_norm_core':
        beta = number(cq['norm_ratio_bound'], 'norm_ratio_bound', 1)
        if not cq.get('norm_certificate'):
            raise ValueError('norm_certificate is required')
        eta = eps / math.sqrt(1+beta*beta)
        # Eq. 6 sufficient degree avoids unstable acosh ratio near K=1.
        ell = int(math.ceil(K*math.log(2/eta)/2))
        sin_min = 2/(beta+1/beta)
        p = (sin_min*(1-eta)/(1+eta))**2
        base.update(algorithm='Dalzell v2 Algorithm 1 / Theorem 1',
                    statistic='deterministic sufficient circuit per attempt',
                    eta_KR=eta, ell=ell, polynomial_degree=2*ell,
                    A_controlled_forward=ell, A_controlled_adjoint=ell,
                    b_controlled_forward=2*ell, b_controlled_adjoint=2*ell,
                    A_queries=2*ell, b_queries=4*ell,
                    qsvt_projector_NOTs=4*ell, qsvt_single_qubit_rotations=2*ell,
                    success_probability_lower_bound_ideal=p,
                    trace_error_bound_ideal=eta*math.sqrt(1+beta*beta),
                    expected_attempts_upper_bound_ideal=1/p,
                    internal_retries_included=False,
                    output_certificate='conditional pure-state trace distance, ideal access',
                    norm_setup_separable=True,
                    ancilla_statement='Theorem 1 quotes a+3; see model.md circuit discrepancy')
    else:
        raise ValueError('unsupported mode')
    return base


if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        result = evaluate(json.load(f))
    print(json.dumps(result, indent=2, allow_nan=False))
