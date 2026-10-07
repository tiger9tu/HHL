#!/usr/bin/env python3
"""Deterministic NumPy-only task-02 diffusion generator and metadata (v1.0)."""
import argparse
import json
import math
from pathlib import Path
import numpy as np

VERSION = '02-smooth-diffusion-v1'

def parameters(m=127, beta=9.0, epsilon=1e-4):
    if not isinstance(m, int) or isinstance(m, bool) or m < 3:
        raise ValueError('m must be an integer >= 3')
    if not math.isfinite(beta) or beta < 0 or not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError('finite beta >= 0 and epsilon > 0 required')
    h=1.0/(m+1); n=m*m; C=1+beta
    l0=8/h**2*math.sin(math.pi*h/2)**2
    k0=1/math.tan(math.pi*h/2)**2
    # c=h^2 1, truncation |tau| <= beta*h^2*4/27.
    disc=5*(2*h*h-h**4)/144 + beta*h**4*n*4/(27*l0)
    F=3*C+9*beta/16 # conservative pointwise |f| bound
    X=math.sqrt(n)*F/l0
    p=1
    while True:
        eta=2.0**(-p); den=h*h*l0-5*eta
        bound=h*h*math.sqrt(n)*(math.sqrt(n)+5*X)*eta/den if den>0 else float('inf')
        if bound <= epsilon/8: break
        p+=1
    return dict(version=VERSION,m=m,N=n,h=h,beta=beta,contrast=C,epsilon=epsilon,
        delta_total=.01,s_row=5,s_col=5,nnz=5*n-4*m,
        lambda_min_lower=l0,lambda_max_upper=C*8/h**2*math.cos(math.pi*h/2)**2,
        kappa_lower=max(1,k0/C),kappa_upper=C*k0,kappa_poisson=k0,
        disc_bound=disc,mesh_admissible=disc<=epsilon/4,
        solver_allowance=epsilon/4,representation_allowance=epsilon/8,
        readout_allowance=epsilon/4,arithmetic_allowance=epsilon/8,
        fixed_fraction_bits_sufficient=p,representation_error_bound=bound,
        rhs_abs_upper=F,solution_norm_upper=X,block_alpha_scaled_sparse=20*C,
        padded_dimension=2**int(math.ceil(math.log(n,2))),
        scalar_continuum=5/144,scalar_sampled_exact=5*(1-h*h)**2/144)

def instance(m=127,beta=9.0,epsilon=1e-4):
    p=parameters(m,beta,epsilon); h=p['h']
    z=np.arange(1,m+1,dtype=float)*h
    x,y=np.meshgrid(z,z,indexing='ij'); qx=x*(1-x); qy=y*(1-y)
    U=qx*qy*(1+x*y)
    ux=qy*((1-2*x)*(1+x*y)+qx*y)
    uxx=qy*(-2*(1+x*y)+2*(1-2*x)*y)
    uyy=qx*(-2*(1+x*y)+2*(1-2*y)*x)
    b=(-(1+beta*x)*(uxx+uyy)-beta*ux).ravel()
    rows=[]; cols=[]; vals=[]
    for i in range(m):
        for j in range(m):
            row=i*m+j; diag=0.; entries=[]
            for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                w=(1+beta*(i+1+di/2)*h)/h**2
                diag+=w
                if 0<=i+di<m and 0<=j+dj<m:
                    entries.append(((i+di)*m+j+dj,-w))
            entries.append((row,diag))
            for col,v in sorted(entries):
                rows.append(row); cols.append(col); vals.append(v)
    rows=np.array(rows,dtype=np.int64); cols=np.array(cols,dtype=np.int64)
    vals=np.array(vals,dtype=float)
    indptr=np.concatenate(([0],np.cumsum(np.bincount(rows,minlength=m*m)))).astype(np.int64)
    return p,dict(rows=rows,indices=cols,data=vals,indptr=indptr,b=b,
                  c=np.full(m*m,h*h),sampled_solution=U.ravel())

def matvec(a,v):
    return np.bincount(a['rows'],weights=a['data']*v[a['indices']],minlength=len(v))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--m',type=int,default=127)
    parser.add_argument('--beta',type=float,default=9)
    parser.add_argument('--epsilon',type=float,default=1e-4)
    parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'instance')
    parser.add_argument('--metadata-only',action='store_true',help='No O(N) allocation')
    args=parser.parse_args()
    p=parameters(args.m,args.beta,args.epsilon)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    if not args.metadata_only:
        if args.m>1023: parser.error('small generator capped at m=1023; use --metadata-only')
        p,a=instance(args.m,args.beta,args.epsilon)
        np.savez_compressed(str(args.out)+'.npz',**a)
        p['rhs_norm_measured']=float(np.linalg.norm(a['b']))
    Path(str(args.out)+'.json').write_text(json.dumps(p,indent=2)+'\n')
    print(json.dumps(p,indent=2))
if __name__=='__main__': main()
