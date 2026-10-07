"""Actual spectral-norm errors versus first-order Trotter bounds.
Run on a compute node. Full dense matrices are used (no random-vector norm estimates).
"""
import argparse,concurrent.futures,csv,hashlib,json,math,os,platform,socket,sys,time,traceback
from pathlib import Path
import numpy as np
import scipy
from scipy import linalg as la
from scipy import sparse
HERE=Path(__file__).resolve().parent
BASE_SEED=20260909
TIMES=[.1,1.,4.]
REPS=[1,2,4,8,16,32]
RHOS=[.025,.1,.25,.5,.75,1.25]
TOL=5e-10

def configurations():
    cases=[]
    for family in ['fixed_band','random_matching','random_spd']:
        for N in [8,16,32,64,128,256,512]:
            for terms in [2,4,8]:
                for sample in range(16 if N<=128 else (8 if N==256 else 4)):
                    cases.append(dict(family=family,N=N,matching_terms=terms,sample=sample))
        for sample in range(2):
            cases.append(dict(family=family,N=1024,matching_terms=4,sample=sample))
    for q in [3,7,15,23,31]:cases.append(dict(family='poisson_2d',N=q*q,matching_terms=4,sample=0,grid=q))
    for N in [8,64,256,1024]:cases.append(dict(family='commuting',N=N,matching_terms=0,sample=0))
    for N in [8,64,256]:
        for amp in [1.,4.]:cases.append(dict(family='cancelling',N=N,matching_terms=0,sample=0,amplitude=amp))
    cases.append(dict(family='pauli',N=2,matching_terms=0,sample=0))
    for i,c in enumerate(cases):c.update(case_id=i,seed=BASE_SEED+i)
    return cases

def hnorm(a):
    ev=la.eigvalsh(a,check_finite=False)
    return float(max(abs(ev[0]),abs(ev[-1])))

def opnorm(a):
    # This is the full spectral norm through a Hermitian Gram matrix.
    gram=a.conj().T@a
    value=la.eigh(gram,eigvals_only=True,subset_by_index=[len(a)-1,len(a)-1],check_finite=False)[0]
    return float(np.sqrt(max(0,value)))

def build_terms(c):
    N=c['N'];rng=np.random.RandomState(c['seed']);family=c['family'];terms=[]
    if family in ['fixed_band','random_matching','random_spd']:
        for j in range(c['matching_terms']):
            p=np.roll(np.arange(N),j) if family=='fixed_band' else rng.permutation(N)
            u=p[::2];v=p[1::2];weights=rng.uniform(-1,1,len(u))
            terms.append(sparse.csr_matrix((np.r_[weights,weights],(np.r_[u,v],np.r_[v,u])),shape=(N,N)))
        if family=='random_spd':
            off=sum(terms).toarray();shift=hnorm(off)+.25
            terms.insert(0,sparse.eye(N,format='csr')*shift)
    elif family=='poisson_2d':
        q=c['grid'];terms=[sparse.eye(N,format='csr')*4]
        for orientation in range(2):
            for parity in range(2):
                us=[];vs=[]
                for y in range(q):
                    for x in range(q):
                        if orientation==0 and x+1<q and x%2==parity:us.append(y*q+x);vs.append(y*q+x+1)
                        if orientation==1 and y+1<q and y%2==parity:us.append(y*q+x);vs.append((y+1)*q+x)
                terms.append(sparse.csr_matrix((-np.ones(2*len(us)),(us+vs,vs+us)),shape=(N,N)))
    elif family=='commuting':
        x=np.arange(N)/N*2*np.pi
        terms=[sparse.eye(N,format='csr')*.5,sparse.diags(.25+.1*np.sin(x),format='csr'),sparse.diags(.25+.1*np.cos(x),format='csr')]
    elif family=='cancelling':
        Z=sparse.diags(np.tile([1.,-1.],N//2),format='csr')*c['amplitude']
        u=np.arange(0,N,2);v=u+1
        X=sparse.csr_matrix((np.full(N,c['amplitude']),(np.r_[u,v],np.r_[v,u])),shape=(N,N))
        terms=[Z,X,-Z,-X,sparse.eye(N,format='csr')]
    else:
        terms=[sparse.diags([1.,-1.],format='csr'),sparse.csr_matrix([[0.,1.],[1.,0.]])]
    H=sum(terms).toarray();eig,vec=la.eigh(H,check_finite=False);scale=max(abs(eig[0]),abs(eig[-1]))
    terms=[a/scale for a in terms];H/=scale;eig/=scale
    assert all(np.max(np.diff(a.indptr))<=1 for a in terms)
    return terms,H,eig,vec,float(scale)

def components(terms):
    parts=[]
    for a in terms:
        coo=sparse.triu(a,1).tocoo()
        if coo.nnz:
            assert not np.any(a.diagonal())
            parts.append(('matching',coo.row,coo.col,coo.data))
        else:parts.append(('diagonal',a.diagonal()))
    return parts

def microstep(parts,h,N):
    P=np.eye(N,dtype=complex)
    for part in parts:
        if part[0]=='diagonal':P*=np.exp(1j*h*part[1])[None,:]
        else:
            _,u,v,w=part;left=P[:,u].copy();right=P[:,v].copy();cs=np.cos(h*w);ss=1j*np.sin(h*w)
            P[:,u]=left*cs+right*ss;P[:,v]=left*ss+right*cs
    return P

def effective_matrix(P,h):
    # Cayley transform of a unitary is Hermitian, with eigenvalues tan(theta/2).
    # Its Hermitian eigendecomposition reconstructs the principal logarithm.
    # Residuals and independent scipy.logm checks quantify numerical effects.
    N=len(P);I=np.eye(N)
    Kraw=-1j*la.solve(P+I,P-I,check_finite=False)
    skew=float(la.norm(Kraw-Kraw.conj().T,'fro'))
    K=(Kraw+Kraw.conj().T)/2
    k,Q=la.eigh(K,check_finite=False)
    theta=2*np.arctan(k)
    Hhat=(Q*(theta/h))@Q.conj().T
    reconstructed=(Q*np.exp(1j*theta))@Q.conj().T
    residual=float(la.norm(reconstructed-P,'fro'))
    return Hhat,dict(cayley_skew_fro=skew,log_reconstruction_fro=residual,phase_gap_to_pi=float(np.pi-np.max(np.abs(theta))))

def run_case(c):
    start=time.time();N=c['N'];terms,H,evals,evec,scale=build_terms(c);parts=components(terms)
    B=sum(float(np.max(np.abs(a.data))) if a.nnz else 0 for a in terms)
    comms=[]
    for i,a in enumerate(terms):
        for b in terms[i+1:]:
            comm=a@b-b@a
            comms.append(hnorm(1j*comm.toarray()) if comm.nnz else 0.)
    C=sum(comms);s=int(np.max(np.count_nonzero(H,axis=1)))
    base=dict(c,L=len(terms),s=s,B=B,C_comm=C,H_scale=scale,H_norm=float(max(abs(evals[0]),abs(evals[-1]))),lambda_min=float(evals[0]),kappa=float(max(abs(evals))/min(abs(evals))))
    settings=[('time_steps',t,r,None) for t in TIMES for r in REPS]
    settings += [('normalized_step',rho/B,1,rho) for rho in RHOS]
    cache={};exact_cache={};rows=[];checks=[]
    for mode,t,r,rho_target in settings:
        h=t/r;key=h.hex();rho=h*B;certified=rho<=.5+1e-14
        if key not in cache:
            P=microstep(parts,h,N);Hhat,diagnostic=effective_matrix(P,h)
            diagnostic['base_unitarity_fro']=float(la.norm(P.conj().T@P-np.eye(N),'fro'))
            EH=hnorm((Hhat+Hhat.conj().T)/2-H)
            cache[key]=(P,Hhat,EH,diagnostic)
        P,Hhat,EH,diagnostic=cache[key]
        if t.hex() not in exact_cache:exact_cache[t.hex()]=(evec*np.exp(1j*t*evals))@evec.T
        exact=exact_cache[t.hex()];S=np.linalg.matrix_power(P,r)
        EU=opnorm(S-exact);BUraw=t*t*C/(2*r);BU=min(2.,BUraw)
        BH=h*C if certified else None;BHr=h*C/(2*(1-rho)) if certified else None
        row=dict(base,sweep=mode,tau=t,r=r,h=h,rho=rho,rho_target=rho_target,matrix_bound_applicable=certified,operator_error=EU,operator_bound=BU,operator_bound_uncapped=BUraw,matrix_error=EH,matrix_bound=BH,matrix_bound_refined=BHr,operator_ratio=EU/BU if BU>0 else None,matrix_ratio=EH/BH if BH is not None and BH>0 else None,matrix_ratio_refined=EH/BHr if BHr is not None and BHr>0 else None,**diagnostic)
        row['operator_violation']=bool(EU>BU+TOL)
        row['matrix_violation']=bool(certified and EH>BHr+TOL)
        assert not row['operator_violation'],row
        assert not row['matrix_violation'],row
        if certified:
            assert diagnostic['log_reconstruction_fro']<1e-8,diagnostic
            assert diagnostic['phase_gap_to_pi']>2.63,diagnostic
        rows.append(row)
        # Independent numerical algorithms, not just reconstruction by the same formula.
        independent=(N<=16 and c['sample']==0) or (N==256 and c['family']=='random_matching' and c['matching_terms']==4 and c['sample']==0 and rho_target==.25)
        if independent:
            logref=la.logm(P)/(1j*h);logdiff=opnorm(Hhat-logref)
            svd=float(la.svdvals(S-exact)[0]);P_ref=np.eye(N,dtype=complex)
            for a in terms:P_ref=P_ref@la.expm(1j*a.toarray()*h)
            p_diff=opnorm(P-P_ref);u_ref=la.expm(1j*H*t);u_diff=opnorm(exact-u_ref)
            assert logdiff<1e-8 and abs(EU-svd)<1e-10 and p_diff<1e-10 and u_diff<1e-10
            checks.append(dict(case_id=c['case_id'],N=N,h=h,tau=t,r=r,logm_difference=logdiff,gram_vs_svd_difference=abs(EU-svd),block_vs_expm_difference=p_diff,spectral_vs_expm_difference=u_diff))
    result={'case':base,'rows':rows,'independent_checks':checks,'elapsed_seconds':time.time()-start,'hostname':socket.gethostname(),'status':'passed'}
    shard=HERE/'shards'/('%04d.json'%c['case_id']);tmp=shard.with_suffix('.tmp');tmp.write_text(json.dumps(result,allow_nan=False));tmp.replace(shard)
    return c['case_id'],len(rows),result['elapsed_seconds']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workers',type=int,default=1);ap.add_argument('--case-ids',type=str);ap.add_argument('--resume',action='store_true');args=ap.parse_args()
    (HERE/'shards').mkdir(exist_ok=True)
    allcases=configurations();(HERE/'configurations.json').write_text(json.dumps(allcases,indent=2)+'\n')
    cases=allcases
    if args.case_ids:
        ids=set(int(x) for x in args.case_ids.split(','));cases=[c for c in cases if c['case_id'] in ids]
    if args.resume:cases=[c for c in cases if not (HERE/'shards'/('%04d.json'%c['case_id'])).exists()]
    manifest={'started_unix':time.time(),'hostname':socket.gethostname(),'slurm_job_id':os.getenv('SLURM_JOB_ID'),'workers':args.workers,'blas_threads':os.getenv('OPENBLAS_NUM_THREADS'),'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'base_seed':BASE_SEED,'total_matrix_cases':len(allcases),'scheduled_cases':len(cases),'times':TIMES,'repetitions':REPS,'normalized_microsteps':RHOS,'comparison_absolute_tolerance':TOL}
    suffix=os.getenv('SLURM_JOB_ID','local');mp=HERE/('execution-'+suffix+'.json');mp.write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(manifest),flush=True)
    failed=[];completed=0
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        futures={pool.submit(run_case,c):c for c in cases}
        for future in concurrent.futures.as_completed(futures):
            c=futures[future]
            try:
                cid,n,seconds=future.result();completed+=1
                print('case=%d N=%d family=%s rows=%d seconds=%.3f done=%d/%d'%(cid,c['N'],c['family'],n,seconds,completed,len(cases)),flush=True)
            except Exception:
                msg=traceback.format_exc();failed.append(dict(case=c,traceback=msg));print(msg,flush=True)
    manifest.update(completed=completed,failed=len(failed),finished_unix=time.time());mp.write_text(json.dumps(manifest,indent=2)+'\n')
    if failed:(HERE/('failures-'+suffix+'.json')).write_text(json.dumps(failed,indent=2));sys.exit(1)

if __name__=='__main__':main()
