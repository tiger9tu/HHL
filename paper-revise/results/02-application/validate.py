#!/usr/bin/env python3
"""Independent analytic identities, dense spectral checks and matrix-free CG diagnostics."""
import csv
import json
import platform
from pathlib import Path
import numpy as np
from generate import instance,matvec,parameters
HERE=Path(__file__).resolve().parent

def cg(a,b,l0,c,allowance):
    x=np.zeros_like(b); r=b.copy(); d=r.copy(); rr=float(r@r)
    for k in range(1,10*len(b)+1):
        ad=matvec(a,d); step=rr/float(d@ad); x+=step*d; r-=step*ad
        new=float(r@r)
        if np.linalg.norm(c)*np.linalg.norm(r)/l0<=allowance/2:
            true=b-matvec(a,x)
            if np.linalg.norm(c)*np.linalg.norm(true)/l0<=allowance: return x,k
            r=true; d=r.copy(); rr=float(r@r); continue
        d=r+(new/rr)*d; rr=new
    raise AssertionError('CG failed')

rows=[]
for m in (3,7,15,31,63,127):
  for beta in (0.,1.,9.,99.):
    p,a=instance(m,beta); h=p['h']; n=p['N']; c=a['c']; b=a['b']
    y=np.tile(np.arange(1,m+1)*h,m)
    tau=beta*h*h*y*y*(1-y)
    defect=matvec(a,a['sampled_solution'])-b
    assert np.max(np.abs(defect-tau))<2e-9
    assert len(a['data'])==p['nnz']
    assert abs(float(c@a['sampled_solution'])-p['scalar_sampled_exact'])<1e-14
    u,k=cg(a,b,p['lambda_min_lower'],c,1e-10)
    r=b-matvec(a,u); cert=float(np.linalg.norm(c)*np.linalg.norm(r)/p['lambda_min_lower'])
    error=abs(float(c@u)-p['scalar_continuum'])
    assert error<=p['disc_bound']+cert+1e-13
    record=dict(m=m,beta=beta,iterations=k,scalar=float(c@u),continuum_error=error,
                disc_bound=p['disc_bound'],residual_scalar_bound=cert,mesh_admissible=p['mesh_admissible'])
    if m<=7:
        A=np.zeros((n,n)); A[a['rows'],a['indices']]=a['data']
        assert np.max(abs(A-A.T))==0
        ev=np.linalg.eigvalsh(A); kap=float(ev[-1]/ev[0])
        assert ev[0]>=p['lambda_min_lower']*(1-1e-12)
        assert p['kappa_lower']*(1-1e-12)<=kap<=p['kappa_upper']*(1+1e-12)
        Pdata=instance(m,0)[1]; P=np.zeros_like(A); P[Pdata['rows'],Pdata['indices']]=Pdata['data']
        w,V=np.linalg.eigh(P); inv=(V/np.sqrt(w))@V.T
        pe=np.linalg.eigvalsh(inv@A@inv)
        assert pe[0]>=1-1e-10 and pe[-1]<=1+beta+1e-10
        direct=np.linalg.solve(A,b)
        assert abs(float(c@(direct-u)))<=cert+1e-12
        eta=2.0**(-p['fixed_fraction_bits_sufficient'])
        rounded_B=np.round((h*h*A)/eta)*eta
        rounded_d=np.round((h*h*b)/eta)*eta
        rounded_x=np.linalg.solve(rounded_B,rounded_d)
        assert abs(float(c@(rounded_x-direct)))<=p['representation_error_bound']+1e-12
        # Padded positive identity block must preserve the scalar exactly.
        D=p['padded_dimension']; padded=np.eye(D)*4*(1+beta)
        padded[:n,:n]=h*h*A
        padded_x=np.linalg.solve(padded,np.pad(h*h*b,(0,D-n),mode='constant'))
        assert abs(float(c@(padded_x[:n]-direct)))<1e-12
        record.update(kappa_measured=kap,preconditioned_kappa_measured=float(pe[-1]/pe[0]))
    rows.append(record)
for bad in ((2,9,1e-4),(3,-1,1e-4),(3,1,0)):
    try: parameters(*bad)
    except ValueError: pass
    else: raise AssertionError('invalid input accepted')
(HERE/'validation.json').write_text(json.dumps(dict(python=platform.python_version(),numpy=np.__version__,
    status='passed',cases=rows,scope='FP64 numerical diagnostics; analytic proof in specification.md; no timing or interval certification'),indent=2)+'\n')
sweep=[]
for m in (15,31,63,127,255,511,1023,4095,16383):
 for beta in (0.,1.,9.,99.):
  for eps in (1e-2,1e-4,1e-6):
   sweep.append(parameters(m,beta,eps))
with (HERE/'parameters.csv').open('w') as f:
    writer=csv.DictWriter(f,fieldnames=list(sweep[0])); writer.writeheader(); writer.writerows(sweep)
print('Passed {} solve cases, tiny spectral/preconditioner checks, 3 invalid inputs; wrote {} analytic sweep rows'.format(len(rows),len(sweep)))
