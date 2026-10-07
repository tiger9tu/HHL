"""Finite-dimensional validation; run with BLAS threads set to one."""
import csv, json, platform, hashlib, subprocess
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import expm, logm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
OUT = Path(__file__).resolve().parent
SEED = 20260908
norm = lambda a: float(np.linalg.norm(a, 2))

def synthetic(N, degree, rng, pattern):
    terms = []
    for j in range(degree):
        a = np.zeros((N,N))
        p = rng.permutation(N) if pattern == 'random_matching' else np.roll(np.arange(N), j)
        for u,v in zip(p[::2],p[1::2]):
            a[u,v] = a[v,u] = rng.uniform(-1,1)
        terms.append(a)
    scale = norm(sum(terms))
    return [a/scale for a in terms]

def poisson(m):
    # -Delta on unit square, zero Dirichlet BC; h^-2 cancels on normalization.
    N = m*m
    terms = [4*np.eye(N)] + [np.zeros((N,N)) for _ in range(4)]
    for y in range(m):
        for x in range(m):
            u = y*m+x
            if x+1<m:
                terms[1+x%2][u,u+1] = terms[1+x%2][u+1,u] = -1
            if y+1<m:
                terms[3+y%2][u,u+m] = terms[3+y%2][u+m,u] = -1
    scale = 4+4*np.cos(np.pi/(m+1))
    return [a/scale for a in terms]

def product(terms,t,r):
    u = np.eye(len(terms[0]),dtype=complex)
    for a in terms:
        u = u @ expm(1j*a*t/r)
    return np.linalg.matrix_power(u,r)

def metrics(terms):
    comm = [norm(a@b-b@a) for i,a in enumerate(terms) for b in terms[i+1:]]
    return sum(comm), comm

def dump_csv(name, rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def qpe_state(A,terms,r):
    N=len(A); M=8; b=np.ones(N)/np.sqrt(N); tbase=2*np.pi
    state=np.zeros((M,N),complex); state[0]=b
    # Hadamards on clock |0> produce uniform state. Controlled powers then inverse DFT.
    state=np.tile(b,(M,1)).astype(complex)/np.sqrt(M)
    us=[expm(1j*A*tbase*2**j) if terms is None else product(terms,tbase*2**j,r) for j in range(3)]
    for j,u in enumerate(us):
        for k in range(M):
            if (k>>j)&1: state[k]=u@state[k]
    state=np.fft.fft(state,axis=0)/np.sqrt(M)
    weights=np.zeros(M); weights[1:]=np.minimum(1,.25/(np.arange(1,M)/M))
    state*=weights[:,None]
    state=np.fft.ifft(state,axis=0)*np.sqrt(M)
    for j in range(2,-1,-1):
        for k in range(M):
            if (k>>j)&1: state[k]=us[j].conj().T@state[k]
    # Only comparing circuits: final clock Hadamards are a common unitary, but apply them for solution check.
    h=np.array([[1,1],[1,-1]])/np.sqrt(2); H=np.kron(np.kron(h,h),h)
    state=H@state
    p=float(np.linalg.norm(state)**2)
    return state/np.sqrt(p),p

def validate():
    Z=np.diag([1.,-1.]); X=np.array([[0.,1.],[1.,0.]])
    vals={}
    for t in [.2,.1]:
        u=product([Z,X],t,1)
        vals['ZX_t_'+str(t)]={'effective_error':norm(logm(u)/(1j*t)-Z-X),'old_B18_rhs':t,'unitary_error':norm(u-expm(1j*(Z+X)*t))}
    terms=[2*Z,2*X,-2*Z,-2*X,np.eye(2)]
    vals['cancelling_decomposition']={'t':.001,'N':2,'L':5,'A':'identity','effective_error':norm(logm(product(terms,.001,1))/.001/1j-np.eye(2))}
    assert vals['cancelling_decomposition']['effective_error']>.001
    # Commuting regression and real second-order vs repository coefficient ordering.
    assert norm(product([Z,2*Z],1,4)-expm(3j*Z))<1e-12
    terms=[Z,X,np.diag([.3,.7])]
    def order_error(dt,wrong):
        seq=[(0,.5),(1,.5),(2,1),(0,.5),(1,.5)] if wrong else [(0,.5),(1,.5),(2,1),(1,.5),(0,.5)]
        u=np.eye(2,dtype=complex)
        for j,c in seq: u=u@expm(1j*terms[j]*dt*c)
        return norm(u-expm(1j*sum(terms)*dt))
    vals['local_order_ratios']={str(w):order_error(.04,w)/order_error(.02,w) for w in [False,True]}
    assert vals['local_order_ratios']['False']>7.8
    assert 3.8<vals['local_order_ratios']['True']<4.2
    # Exact-grid SPD example: eigs .25,.75; kappa=3; inverse rotation C=.25.
    A=.5*np.eye(2)+.15*Z+.2*X; terms=[.5*np.eye(2),.15*Z,.2*X]
    ideal,p=qpe_state(A,None,1); x=np.linalg.solve(A,np.ones(2)/np.sqrt(2)); x/=np.linalg.norm(x)
    target=np.zeros_like(ideal); target[0]=x
    assert np.linalg.norm(ideal-target)<1e-12
    C,_=metrics(terms); q=[]
    for r in [16,64,256,4096]:
        got,pg=qpe_state(A,terms,r)
        eta=C*sum((2*np.pi*2**j)**2 for j in range(3))/r
        error=float(np.linalg.norm(got-ideal)); bound=2*eta/np.sqrt(p)
        assert error<=bound+1e-12
        q.append({'r':r,'conditioned_state_error':error,'ideal_success':p,'actual_success':pg,'full_circuit_eta_bound':eta,'conditioned_error_bound':bound})
    vals['qpe_validation']=q
    assert q[-1]['conditioned_state_error']<q[0]['conditioned_state_error']
    (OUT/'validation.json').write_text(json.dumps(vals,indent=2)+'\n')

def main():
    rows=[]; commrows=[]; case=0
    for pattern in ['fixed_band','random_matching','poisson_2d']:
        configs=[(m*m,4,m) for m in [3,5,7,9,11]] if pattern=='poisson_2d' else [(n,d,None) for n in [8,16,32,64,128] for d in [2,4]]
        for N,degree,m in configs:
            for sample in range(1 if m else 24):
                seed=SEED+case; case+=1; rng=np.random.RandomState(seed)
                terms=poisson(m) if m else synthetic(N,degree,rng,pattern)
                A=sum(terms); C,comms=metrics(terms); ev=np.linalg.eigvalsh(A)
                kappa=max(abs(ev))/min(abs(ev))
                assert all(np.max(np.count_nonzero(a,axis=1))<=1 for a in terms)
                for pair,c in enumerate(comms): commrows.append(dict(case=case,pattern=pattern,N=N,degree=degree,seed=seed,pair=pair,commutator_norm=c))
                for t in [.1,1.]:
                    exact=expm(1j*A*t)
                    for r in [1,2,4,8]:
                        u=product(terms,t,r); error=norm(u-exact); bound=t*t*C/(2*r)
                        unitary=norm(u.conj().T@u-np.eye(N))
                        assert error<=bound+2e-12
                        assert unitary<2e-12
                        rows.append(dict(case=case,pattern=pattern,N=N,degree=degree,s=int(np.max(np.count_nonzero(A,axis=1))),L=len(terms),sample=sample,seed=seed,t=t,r=r,H_norm=norm(A),kappa=kappa,C_comm=C,error=error,bound=bound,ratio=error/bound if bound else 0,unitarity_residual=unitary))
    dump_csv('samples.csv',rows); dump_csv('commutators.csv',commrows)
    summaries=[]; boot=np.random.RandomState(SEED+999999)
    keys=sorted(set((x['pattern'],x['N'],x['degree'],x['t'],x['r']) for x in rows))
    for key in keys:
        group=[x for x in rows if (x['pattern'],x['N'],x['degree'],x['t'],x['r'])==key]; v=np.array([x['error'] for x in group]); n=len(v)
        ci=np.quantile(np.mean(boot.choice(v,(2000,n)),axis=1),[.025,.975]) if n>1 else [None,None]
        summaries.append(dict(zip(['pattern','N','degree','t','r'],key),samples=n,mean=float(v.mean()),median=float(np.median(v)),q05=float(np.quantile(v,.05)),q95=float(np.quantile(v,.95)),maximum=float(v.max()),mean_ci_low=ci[0],mean_ci_high=ci[1],max_bound_ratio=max(x['ratio'] for x in group)))
    dump_csv('summary.csv',summaries)
    fig,ax=plt.subplots(1,3,figsize=(15,4.4))
    for pattern in ['fixed_band','random_matching','poisson_2d']:
        group=[x for x in summaries if x['pattern']==pattern and x['degree']==4 and x['t']==1 and x['r']==4]
        ns=[x['N'] for x in group]; med=[x['median'] for x in group]
        ax[0].plot(ns,med,'o-',label=pattern)
        ax[0].fill_between(ns,[x['q05'] for x in group],[x['q95'] for x in group],alpha=.15)
    ax[0].set(xlabel='Matrix dimension N',ylabel='Operator error ||S_r(1) - exp(iH)||_2',xscale='log',yscale='log',title='r=4; median and 5–95% range'); ax[0].legend(fontsize=8)
    for pattern in ['fixed_band','random_matching']:
        v=[x['ratio'] for x in rows if x['pattern']==pattern and x['N']==64 and x['degree']==4 and x['t']==1 and x['r']==4]
        ax[1].hist(v,bins=np.linspace(0,1,11),alpha=.5,label=pattern)
        c=[x['commutator_norm'] for x in commrows if x['pattern']==pattern and x['N']==64 and x['degree']==4]
        ax[2].hist(c,bins=np.linspace(0,2,21),alpha=.5,label=pattern)
    ax[1].set(xlabel='Error / [t² C_comm / (2r)]',ylabel='Matrix sample count',title='N=64, four matching terms, t=1, r=4');ax[1].legend(fontsize=8)
    ax[2].set(xlabel='Pair commutator norm ||[H_j,H_k]||_2',ylabel='Pair count (clustered by matrix)',title='N=64; 24 matrices × 6 pairs / ensemble');ax[2].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(str(OUT/'figure9.pdf'));fig.savefig(str(OUT/'figure9.png'),dpi=160);plt.close(fig)
    validate()
    manifest={'base_seed':SEED,'bootstrap_seed':SEED+999999,'bootstrap_replicates':2000,'matrix_samples':case,'measurements':len(rows),'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'matplotlib':matplotlib.__version__,'git_head':subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),'max_bound_ratio':max(x['ratio'] for x in rows),'max_unitarity_residual':max(x['unitarity_residual'] for x in rows),'sha256':{}}
    root=OUT.parents[2]
    paths=list((root/'num').glob('*'))+list((root/'src/HHL').rglob('*.qs'))+list((root/'paper').glob('*.pdf'))+list((root/'paper-revise/docs').glob('*.pdf'))+[root/'tools/surface_code_opt.py',Path(__file__).resolve()]
    for p in paths:
        if p.is_file():manifest['sha256'][str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({k:v for k,v in manifest.items() if k!='sha256'},indent=2))

if __name__=='__main__': main()
