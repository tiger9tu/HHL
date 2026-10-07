#!/usr/bin/env python3
"""Regenerate local diagnostics, default instance, pp fragment, and provenance."""
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):
    os.environ[key]='1'
import numpy as np
import jsonschema
from generate import parameters
subprocess.check_call([sys.executable,str(HERE/'validate.py')])
subprocess.check_call([sys.executable,str(HERE/'generate.py'),'--out',str(HERE/'instance')],stdout=subprocess.DEVNULL)
p=parameters()
def q(v,note='Derived in specification.md; dimensionless.'):
    return dict(unit='1',status='known',value=v,note=note)
pp=dict(instance_id='02-smooth-diffusion-v1:m127:beta9:epsilon0.0001',
    matrix_class='Real symmetric positive definite; original unscaled A',
    matrix_representation='Analytic conservative five-point stencil; optional generated CSR',
    input_access='Compact formulas equally available; charge construction, reversible oracles and preparation; no QRAM supplied',
    input_location='Compact specification in host memory on both branches; arrays not prebuilt',
    rhs='b_ij=f(ih,jh), polynomial source in specification.md; nonzero; no random seed',
    N=q(p['N']),s_row=q(5),s_col=q(5),
    kappa_2=dict(unit='1',status='unknown',note='Original kappa is bounded, not evaluated: see kappa_original_lower/upper.'),
    scaling='Dimensionless A with h^-2 factors; B=h^2 A,d=h^2 b preserve x; pad B with 4C identity if needed',
    output=dict(definition='J=integral_Omega u; discrete approximation c^T A^-1 b, c=h^2 ones',unit='1',
        metric='Absolute scalar error divided by fixed reference scale 1',epsilon=q(p['epsilon'],'Chosen common continuum tolerance'),
        normalization='Unnormalized temperature integral; norm and signed overlap recovery required for state solvers',
        delta_total=q(.01,'Requested per-output failure bound, not measured'),
        reference_solution='Exact continuum J=5/144; discrete references require original-residual certificate; known-answer shortcut must be allowed',
        success_scope='per_output'),
    reuse=dict(outputs=q(1,'One scalar, one RHS'),groups='One cold setup and one output',
        invalidation='m,beta,source,observable,access,precision or hardware changes; identical output can be cached'),
    parameters={k:q(v) for k,v in dict(m=p['m'],h=p['h'],beta=p['beta'],contrast=p['contrast'],
        nnz=p['nnz'],kappa_original_lower=p['kappa_lower'],kappa_original_upper=p['kappa_upper'],
        lambda_min_lower=p['lambda_min_lower'],mesh_error_upper=p['disc_bound'],
        epsilon_discretization=p['epsilon']/4,epsilon_solve=p['epsilon']/4,
        epsilon_representation=p['epsilon']/8,epsilon_readout=p['epsilon']/4,
        epsilon_arithmetic=p['epsilon']/8).items()})
schema=json.loads((ROOT/'paper-revise/results/01-framework/interface.schema.json').read_text())
fragment_schema={'$ref':'#/definitions/pp','definitions':schema['definitions']}
jsonschema.Draft7Validator(fragment_schema).validate(pp)
(HERE/'benchmark-pp.json').write_text(json.dumps(pp,indent=2)+'\n')
inputs=[ROOT/'paper-revise/prompts/tasks/02-application.md',ROOT/'paper-revise/prompts/tasks/README.md',
    ROOT/'paper-revise/prompts/paper-revise.md',ROOT/'num/genSparse.m',ROOT/'src/HHL/HHL.qs',
    ROOT/'src/HHL/HamiltonianEvolution/Oracle/Oracle.qs',
    ROOT/'paper-revise/results/08-classical-baseline/model-and-benchmark.md',
    ROOT/'paper-revise/results/08-classical-baseline/benchmark.py']
inputs+=list((ROOT/'paper-revise/results/01-framework').glob('*.md'))
inputs+=[ROOT/'paper-revise/results/01-framework/interface.schema.json']
inputs+=list((ROOT/'paper-revise/docs').glob('*.pdf'))+list((ROOT/'paper').glob('*.pdf'))
inputs+=list(HERE.glob('*.py'))
manifest=dict(git_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT)).decode().strip(),
    python=platform.python_version(),numpy=np.__version__,jsonschema=jsonschema.__version__,
    command='python3 paper-revise/results/02-application/reproduce.py',
    scope='Numerical diagnostics, schema pp validation, analytical parameter sweep; no performance measurements',
    files=[dict(path=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(inputs)])
(HERE/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Default mesh admissible; pp fragment passes task-01 Draft 7 schema; provenance captured.')
