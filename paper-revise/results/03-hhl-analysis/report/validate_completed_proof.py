"""Finite checks of the added proof; not simulations of the exponentially large joint clock state."""
import csv,json,math
from pathlib import Path
import numpy as np
from scipy.linalg import expm,logm
from scipy.stats import binom
HERE=Path(__file__).resolve().parent
norm=lambda a:float(np.linalg.norm(a,2))
rng=np.random.RandomState(20260909)
log_checks=[]
for N in [2,4,8,16]:
 for sample in range(8):
  edges=[]
  for _ in range(3):
   a=np.zeros((N,N));perm=rng.permutation(N)
   for i,j in zip(perm[::2],perm[1::2]):a[i,j]=a[j,i]=rng.uniform(-.15,.15)
   edges.append(a)
  terms=[np.eye(N)]+edges;H=sum(terms);scale=norm(H);terms=[a/scale for a in terms];H=sum(terms)
  eig=np.linalg.eigvalsh(H);kap=1/eig[0];eps=.2
  B=sum(norm(a) for a in terms);C=sum(norm(a@b-b@a) for i,a in enumerate(terms) for b in terms[i+1:])
  tau=np.pi/4;dH=eps/(16*kap);r=max(1,int(np.ceil(max(2*B*tau,C*tau/dH))));h=tau/r
  P=np.eye(N,dtype=complex)
  for a in terms:P=P@expm(1j*a*h)
  Hhat=logm(P)/(1j*h);error=norm(Hhat-H)
  assert h*B<=.5+1e-14 and error<=h*C+2e-12
  assert norm(Hhat-Hhat.conj().T)<1e-11
  b=rng.normal(size=N);b/=np.linalg.norm(b)
  x=np.linalg.solve(H,b);y=np.linalg.solve(Hhat,b)
  state_error=float(np.linalg.norm(x/np.linalg.norm(x)-y/np.linalg.norm(y)))
  perturb_bound=2*kap*error/(1-kap*error)
  assert state_error<=perturb_bound+1e-12 and state_error<eps/4
  for power in [1,2,4]:
   assert norm(np.linalg.matrix_power(P,r*power)-expm(1j*Hhat*tau*power))<2e-11
  log_checks.append(dict(N=N,sample=sample,kappa=kap,B=B,C=C,h=h,r_base=r,effective_error=error,effective_bound=h*C,state_error=state_error,state_bound=perturb_bound))
qpe_checks=[]
for K in [4,8,12]:
 for eps in [.25,.5]:
  e=eps/2;dlam=e/(8*K);beta=dlam*dlam;M=2**int(np.ceil(np.log2(32/dlam)))
  R=int(np.ceil((32/9)*np.log(1/beta)));R+=int(R%2==0)
  k=np.arange(M);z=4*np.where(k<M/2,k/M,k/M-1);order=np.argsort(z);zs=z[order]
  for lam in [1/K,1.371/K,.431,.731,1.]:
   phase=lam/4;d=(phase-k/M+.5)%1-.5
   prob=(np.sinc(M*d)/np.sinc(d))**2;prob/=prob.sum()
   tail=float(prob[np.abs(z-lam)>dlam].sum());assert tail<1/8
   F=np.cumsum(prob[order]);F=np.clip(F,0,1);F[-1]=1
   med_cdf=binom.sf((R-1)//2,R,F)
   med_prob=np.diff(np.r_[0,med_cdf]);assert med_prob.min()>-1e-14
   med_tail=float(med_prob[np.abs(zs-lam)>dlam].sum());assert med_tail<=beta+1e-13
   c=1/(2*K);f=c/np.maximum(zs,1/(2*K));exact=c/lam
   branch_error=float(np.sqrt(np.sum(med_prob*(f-exact)**2)))
   bound=2*K*dlam*exact+np.sqrt(beta);assert branch_error<=bound+1e-12
   qpe_checks.append(dict(K=K,epsilon=eps,lambda_J=lam,M=M,median_repetitions=R,single_qpe_bad_probability=tail,median_bad_probability=med_tail,beta_bound=beta,branch_error=branch_error,branch_error_bound=bound))
for name,rows in [('effective-proof-checks.csv',log_checks),('median-qpe-checks.csv',qpe_checks)]:
 with (HERE/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
result={'seed':20260909,'effective_matrix_cases':len(log_checks),'qpe_eigenphase_cases':len(qpe_checks),'max_effective_error_to_bound':max(x['effective_error']/x['effective_bound'] for x in log_checks if x['effective_bound']>0),'max_single_qpe_bad_probability':max(x['single_qpe_bad_probability'] for x in qpe_checks),'max_median_bad_probability':max(x['median_bad_probability'] for x in qpe_checks),'passed':True,'scope':'dense logarithm and inverse perturbation; exact scalar QPE and median distributions; no full coherent median-circuit simulation'}
(HERE/'completed-proof-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
