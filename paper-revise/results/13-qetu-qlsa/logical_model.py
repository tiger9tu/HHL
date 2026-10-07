"""Task 13: sufficient QETU macro counts, with no invented compiler costs."""
import math


def estimate(K, B_sum, C_comm, epsilon_state=0.01, tau=0.5, stages=5):
    values = (K, B_sum, C_comm, epsilon_state, tau)
    if not all(math.isfinite(x) for x in values):
        raise ValueError('finite inputs required')
    if K < 1 or B_sum <= 0 or C_comm < 0 or not 0 < epsilon_state <= 0.1:
        raise ValueError('invalid spectral, decomposition or accuracy input')
    if tau != 0.5 or not isinstance(stages, int) or stages < 1:
        raise ValueError('this finite construction uses tau=0.5 and positive stage count')
    eps_matrix = epsilon_state / 2
    eps_filter = epsilon_state / 4
    eps_synthesis = epsilon_state / 4
    target = eps_matrix / (K * (2 + eps_matrix))
    g = math.sin(tau / (2*K))
    a = math.sin(1.25*tau)
    e = eps_filter / 32
    b = int(math.ceil(math.log(1/(g*e)) / g**2))
    j = min(b-1, int(math.ceil(math.sqrt(b*math.log(4*b/e)))))
    correction_order = max(0, int(math.ceil(math.log(e*g)/(2*math.log(a))))-1)
    scale = math.sqrt(b) + e
    c = 1/(tau*scale)
    eta = 3*e/scale
    sigma = c/(1+target)
    # Conservative normalization denominator sigma - eta - zeta.
    zeta = eps_synthesis * (sigma-eta)/(2+eps_synthesis)
    conditional_bound = 2*(eta+zeta)/(sigma-eta-zeta)
    if conditional_bound > eps_filter + eps_synthesis:
        raise ArithmeticError('conditional error allocation failed')
    r = max(1, int(math.ceil(2*tau*B_sum)),
            int(math.ceil(tau*B_sum+tau*C_comm/(2*target))))
    effective_bound = tau*C_comm/(2*(r-tau*B_sum))
    degree = 2*(2*j+1+2*correction_order)
    success = (sigma-eta-zeta)**2
    retry_delta = 0.002
    retry_cap = int(math.ceil(math.log(retry_delta)/math.log1p(-success)))
    return dict(K_HE=K, B_sum=B_sum, C_comm=C_comm, epsilon_state=epsilon_state,
                tau=tau, trotter_order=1, stages=stages,
                epsilon_matrix=eps_matrix, matrix_target=target,
                sine_gap=g, sine_upper=a, reciprocal_tolerance=e,
                reciprocal_b=b, reciprocal_j=j, correction_order=correction_order,
                polynomial_normalizer=scale, inverse_scale=c,
                polynomial_error_bound=eta, implementation_allowance=zeta,
                sigma_lower=sigma, conditional_error_bound=conditional_bound,
                degree=degree, controlled_forward_calls=degree//2,
                controlled_adjoint_calls=degree//2, phase_rotations=degree+1,
                controlled_shift_cliffords=degree,
                r_bound=r, effective_H_bound=effective_bound,
                controlled_fragment_exponentials=degree*r*stages,
                p_success_lower=success, expected_attempts_upper=1/success,
                retry_delta=retry_delta, capped_attempts=retry_cap,
                amplification_inverse_amplitude=1/math.sqrt(success),
                amplification_note='scaling parameter, not a finite query schedule',
                signal_ancillas=1, compiled_T_gates=None, compiled_depth=None,
                compiled_T_depth=None, logical_qubits_peak=None)


def correction_coefficients(order):
    """Taylor coefficients of v/arcsin(v) in powers of v^2."""
    arcsin = [1.0]
    for j in range(1, order+1):
        arcsin.append(arcsin[-1]*(2*j-1)**2/(2*j*(2*j+1)))
    q = [1.0]
    for j in range(1, order+1):
        q.append(-sum(arcsin[k]*q[j-k] for k in range(1, j+1)))
    return q


def polynomial_values(v, model):
    """Evaluate the certified construction; NumPy/SciPy only for diagnostics."""
    import numpy as np
    from scipy.stats import binom
    j = np.arange(model['reciprocal_j']+1)
    b = model['reciprocal_b']
    coeff = np.zeros(2*model['reciprocal_j']+2)
    coeff[2*j+1] = 4*(-1.)**j*binom.sf(b+j, 2*b, 0.5)
    R = np.polynomial.chebyshev.chebval(v, coeff)/model['polynomial_normalizer']
    q = np.polynomial.polynomial.polyval(
        np.asarray(v)**2, correction_coefficients(model['correction_order']))
    return R*q
