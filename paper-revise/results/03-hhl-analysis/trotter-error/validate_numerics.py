"""Recheck the two deterministic examples printed in the note."""
import json
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm,logm
HERE=Path(__file__).resolve().parent
norm=lambda a:float(np.linalg.norm(a,2))
X=np.array([[0.,1.],[1.,0.]])
Z=np.diag([1.,-1.]);H=X+Z
B=norm(X)+norm(Z);C=norm(Z@X-X@Z)
rows=[]
for h in [.1,.2]:
    P=expm(1j*Z*h)@expm(1j*X*h)
    effective=logm(P)/(1j*h)
    error_u=norm(P-expm(1j*H*h));error_h=norm(effective-H)
    refined=h*C/(2*(1-h*B))
    assert h*B<=.5
    assert error_u<=h*h*C/2+1e-12
    assert error_h<=refined+1e-12 and refined<=h*C+1e-12
    assert norm(effective-effective.conj().T)<1e-12
    rows.append(dict(h=h,B=B,C_comm=C,unitary_error=error_u,unitary_bound=h*h*C/2,matrix_error=error_h,matrix_bound_refined=refined,matrix_bound=h*C))
result=dict(numpy=np.__version__,scipy=scipy.__version__,cases=rows,passed=True)
(HERE/'numerical-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
