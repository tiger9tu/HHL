"""Task 08 / September 20: manuscript D1 -> HPCG time -> power x time.

Arithmetic projection only. Not an ISA instruction counter or certified solver.
Standard library; all rates are whole-configuration published HPCG scores.
"""
import argparse
import json
import math
from pathlib import Path
HERE=Path(__file__).resolve().parent


def positive_int(value, name):
    if isinstance(value,bool) or not isinstance(value,int) or value<1:
        raise ValueError(name+' must be a positive integer')


def finite(value, name, lower=0, strict=True):
    if isinstance(value,bool) or not isinstance(value,(int,float)) or not math.isfinite(value):
        raise ValueError(name+' must be finite')
    if (strict and value<=lower) or (not strict and value<lower):
        raise ValueError(name+' outside allowed range')


def paper_count(N,kappa,s,epsilon,rounding='ceil'):
    positive_int(N,'N');positive_int(s,'s')
    if s>N: raise ValueError('s must not exceed N')
    finite(kappa,'kappa',1,False);finite(epsilon,'epsilon')
    if epsilon>=1: raise ValueError('epsilon must be below 1')
    if rounding not in ('ceil','paper'): raise ValueError('rounding must be ceil or paper')
    # Difference of logarithms avoids overflow in 2/epsilon.
    raw_k=.5*kappa*(math.log(2)-math.log(epsilon))
    if not math.isfinite(raw_k): raise ValueError('iteration estimate overflows')
    per=4*N*s+14*N
    chosen_k=math.ceil(raw_k) if rounding=='ceil' else raw_k
    raw=raw_k*per
    selected=chosen_k*per
    if not math.isfinite(raw): raise ValueError('FLOP estimate overflows')
    return dict(N=N,kappa_original=kappa,s=s,epsilon_relative_solution=epsilon,
        model_version='08-cg-paper-hpcg-v1',formula='D1: (kappa/2)*ln(2/epsilon)*(4*N*s+14*N)',
        algorithm='Paper CG-family baseline; Figure 13 is CGLS/CGNR despite CGNE caption',
        two_matvec_flops=4*N*s,vector_update_flops=6*N,coefficient_flops=8*N,
        flops_per_iteration=per,iterations_paper=raw_k,iterations_ceiled=math.ceil(raw_k),
        rounding=rounding,nflops_paper=raw,nflops=selected,
        precision='FP64 assumed for HPCG transfer; paper formula has no bit-width parameter',
        count_status='paper arithmetic model, not exact executed instruction count or validated convergence certificate')


def project(count,profile,rate_multiplier=1.0,power_multiplier=1.0,memory_limit_bytes=None):
    finite(profile['hpcg_pflop_s'],'HPCG rate');finite(profile['power_kW'],'power')
    finite(rate_multiplier,'rate_multiplier');finite(power_multiplier,'power_multiplier')
    if memory_limit_bytes is not None: positive_int(memory_limit_bytes,'memory_limit_bytes')
    rate=profile['hpcg_pflop_s']*1e15*rate_multiplier
    power=profile['power_kW']*1e3*power_multiplier
    t=count['nflops']/rate;e=t*power
    one_vector=8*count['N']
    # Lower-bound rejection only: passing cannot certify total solver memory.
    capacity='unresolved'
    if memory_limit_bytes is not None and one_vector>memory_limit_bytes:
        capacity='infeasible_even_one_vector'
    return dict(hardware=profile['id'],hpcg_pflop_s=profile['hpcg_pflop_s'],
        published_power_kW=profile['power_kW'],effective_flop_s=rate,assumed_power_W=power,
        rate_multiplier=rate_multiplier,power_multiplier=power_multiplier,
        core_time_s=t,core_time_h=t/3600,core_energy_J=e,core_energy_kWh=e/3.6e6,
        J_per_flop=power/rate,one_vector_lower_bound_bytes=one_vector,
        memory_limit_bytes=memory_limit_bytes,capacity_status=capacity,
        measurement_status='projection; HPCG score and TOP500 power are not paired workload measurements',
        scope='solver core only; setup/input/output/facility coverage unresolved',
        end_to_end_time_s=None,end_to_end_energy_J=None,eligible_for_advantage_claim=False)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,default=HERE/'model-input.json')
    p.add_argument('--hardware',type=Path,default=HERE/'hardware.json')
    p.add_argument('--rounding',choices=['ceil','paper'])
    p.add_argument('--rate-multiplier',type=float,default=1.)
    p.add_argument('--power-multiplier',type=float,default=1.)
    p.add_argument('--memory-limit-bytes',type=int)
    args=p.parse_args();inp=json.loads(args.input.read_text());hw=json.loads(args.hardware.read_text())
    count=paper_count(inp['N'],inp['kappa'],inp['s'],inp['epsilon'],args.rounding or inp.get('rounding','ceil'))
    result=dict(logical=count,physical=[project(count,h,args.rate_multiplier,args.power_multiplier,args.memory_limit_bytes) for h in hw['profiles']])
    print(json.dumps(result,indent=2,allow_nan=False))
if __name__=='__main__': main()
