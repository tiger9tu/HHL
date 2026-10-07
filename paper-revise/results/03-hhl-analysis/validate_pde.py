"""Manufactured-solution diagnostic; task 02 benchmark remains unspecified."""
import json
import numpy as np
from experiments import poisson, OUT, norm, dump_csv
rows=[]
for m in [3,5,7,9,11]:
    N=m*m; h=1/(m+1); terms=poisson(m); H=sum(terms)
    grid=np.arange(1,m+1)*h; X,Y=np.meshgrid(grid,grid)
    u=(np.sin(np.pi*X)*np.sin(np.pi*Y)+.1*np.sin(2*np.pi*X)*np.sin(3*np.pi*Y)).ravel()
    b=(2*np.pi**2*np.sin(np.pi*X)*np.sin(np.pi*Y)+1.3*np.pi**2*np.sin(2*np.pi*X)*np.sin(3*np.pi*Y)).ravel()
    alpha=(4+4*np.cos(np.pi/(m+1)))/h**2
    x=np.linalg.solve(H,b/alpha)
    lam=np.linalg.eigvalsh(H); k=lam[-1]/lam[0]; analytic=1/np.tan(np.pi/(2*(m+1)))**2
    residual=float(np.linalg.norm(H@x-b/alpha)/np.linalg.norm(b/alpha))
    state_error=float(np.linalg.norm(x/np.linalg.norm(x)-u/np.linalg.norm(u)))
    assert abs(k/analytic-1)<1e-12 and residual<1e-12
    rows.append(dict(m=m,N=N,h=h,s=int(np.max(np.count_nonzero(H,axis=1))),kappa=k,analytic_kappa=analytic,normalized_solution_error=state_error,relative_residual=residual))
assert rows[-1]['normalized_solution_error']<rows[0]['normalized_solution_error']
dump_csv('pde-validation.csv',rows)
print(json.dumps(rows,indent=2))
