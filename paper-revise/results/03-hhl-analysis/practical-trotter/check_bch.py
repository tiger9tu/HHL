"""Small independent check of the positive-time BCH sign and local order."""
import json
from pathlib import Path
import numpy as np
from scipy.linalg import expm,logm,norm
P=Path(__file__).resolve().parent
rng=np.random.RandomState(20260909)
terms=[]
for _ in range(3):
    a=rng.randn(4,4)+1j*rng.randn(4,4);a=(a+a.conj().T)/2;terms.append(a/norm(a,2))
H=sum(terms);K=.5j*sum(a@b-b@a for i,a in enumerate(terms) for b in terms[i+1:])
rows=[]
for h in [.04,.02,.01,.005]:
    U=np.eye(4,dtype=complex)
    for a in terms:U=U@expm(1j*h*a)
    delta=logm(U)/(1j*h)-H
    rows.append(dict(h=h,coefficient_difference=float(norm(delta/h-K,2)),leading_remainder=float(norm(delta-h*K,2))))
orders=[float(np.log(rows[i]['leading_remainder']/rows[i+1]['leading_remainder'])/np.log(2)) for i in range(3)]
assert all(1.95<x<2.05 for x in orders)
assert rows[-1]['coefficient_difference']<rows[0]['coefficient_difference']/7
record=dict(seed=20260909,N=4,fragments=3,convention='ordered product exp(+i h Ha)',rows=rows,remainder_orders=orders,passed=True)
(P/'bch-validation.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
