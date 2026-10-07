"""Independent mathematical/circuit-matrix checks; no new application sweep."""
import importlib.util
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import scipy
import scipy.linalg as la
from logical_model import estimate, correction_coefficients, polynomial_values

HERE=Path(__file__).resolve().parent
source=HERE.parent/'03-hhl-analysis/trotter-error/experiments/run_experiments.py'
spec=importlib.util.spec_from_file_location('original_trotter',str(source))
original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)


def normed(x):
    return x/la.norm(x)


def main():
    checks=[]
    for K in (1., 3., 8.):
        m=estimate(K,1.2,0.1)
        v=np.linspace(-1,1,10001)
        F=polynomial_values(v,m)
        global_max=float(np.max(abs(F)))
        assert global_max <= 1+1e-10
        x=np.linspace(-1,1,1001)
        assert np.max(abs(polynomial_values(1-2*x*x,m)-polynomial_values(1-2*(-x)**2,m))) < 1e-12
        v=np.linspace(m['sine_gap'],m['sine_upper'],5001)
        err=float(np.max(abs(polynomial_values(v,m)-1/(m['polynomial_normalizer']*np.arcsin(v)))))
        assert err <= m['polynomial_error_bound']+1e-10
        q=np.polynomial.polynomial.polyval(v*v,correction_coefficients(m['correction_order']))
        tail=float(np.max(abs(q-v/np.arcsin(v))))
        assert tail <= m['sine_upper']**(2*m['correction_order']+2)+1e-14
        assert m['effective_H_bound'] <= m['matrix_target']*(1+1e-12)
        assert m['epsilon_matrix']+m['conditional_error_bound'] <= m['epsilon_state']
        checks.append(dict(K=K,degree=m['degree'],global_grid_max=global_max,
                           spectral_grid_error=err,analytic_error_bound=m['polynomial_error_bound'],
                           correction_tail=tail))
    inverse_checks=[]
    configs=json.loads((source.parent/'configurations.json').read_text())
    models=json.loads((HERE/'poisson-models.json').read_text())
    for entry in models[:2]:
        config=next(c for c in configs if c['case_id']==entry['case_id'])
        terms,H,eig,vec,scale=original.build_terms(config)
        model=entry['model'];r=model['r_bound'];h=model['tau']/r
        P=original.microstep(original.components(terms),h,H.shape[0])
        Hhat=la.logm(P)/(1j*h)
        herm=float(la.norm(Hhat-Hhat.conj().T,2))
        Hhat=(Hhat+Hhat.conj().T)/2
        delta=float(la.norm(Hhat-H,2))
        b=normed(1+np.arange(H.shape[0],dtype=float)/H.shape[0])
        y=la.solve(H,b);yh=la.solve(Hhat,b)
        matrix_state_error=float(la.norm(normed(yh)-normed(y)))
        perturb_bound=2*model['K_HE']*delta/(1-model['K_HE']*delta)
        assert herm < 1e-9
        assert delta <= model['effective_H_bound']+1e-9
        assert matrix_state_error <= perturb_bound+1e-9
        ev,Q=la.eigh(Hhat)
        z=Q.dot(polynomial_values(np.sin(model['tau']*ev),model)*Q.conj().T.dot(b))
        state_error=float(la.norm(normed(z)-normed(y)))
        assert state_error <= model['epsilon_state']
        assert la.norm(z)**2 >= model['p_success_lower']-1e-10
        U=la.expm(-1j*np.pi/2*np.eye(len(H))).dot(np.linalg.matrix_power(P.conj().T,r))
        Uexpected=la.expm(-1j*(np.pi/2*np.eye(len(H))+model['tau']*Hhat))
        identity_error=float(la.norm(U-Uexpected,2))
        assert identity_error < 1e-8
        inverse_checks.append(dict(N=len(H),r=r,matrix_error=delta,
             matrix_state_error=matrix_state_error,perturbation_bound=perturb_bound,
             inverse_filter_state_error=state_error,success=float(la.norm(z)**2),
             shared_effective_signal_error=identity_error))
    rejected=0
    for args in ((0,1,.1), (2,-1,.1), (2,1,-.1), (float('nan'),1,.1)):
        try: estimate(*args)
        except ValueError: rejected+=1
    assert rejected==4
    commuting=estimate(3,1,0)
    assert commuting['effective_H_bound']==0
    out=dict(status='passed',numpy=np.__version__,scipy=scipy.__version__,
        polynomial_checks=checks,inverse_checks=inverse_checks,
        rejected_invalid_inputs=rejected,
        limitations='Dense grid/matrix FP64 diagnostics; no synthesized phase circuit or scalar readout validation')
    (HERE/'validation.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    artifacts={str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest()
               for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts
               and p.name != 'artifact-manifest.json'}
    (HERE/'artifact-manifest.json').write_text(json.dumps(
        dict(sha256=artifacts, regeneration='python reproduce.py; python validate.py'),
        indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    main()
