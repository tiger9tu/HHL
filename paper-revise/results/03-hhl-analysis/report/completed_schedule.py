"""Exact integer schedule for the completed consistent-microstep theorem."""
import json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent

def schedule(kappa,L,B,C,epsilon,delta):
    assert kappa>=1 and L>=1 and B>=0 and C>=0 and 0<epsilon<=.5 and 0<delta<1
    tau=math.pi/4;dH=epsilon/(16*kappa)
    r=math.ceil(max(1,2*B*tau,C*tau/dH));h=tau/r
    K=4*kappa;e=epsilon/2;dlam=e/(8*K);beta=dlam**2
    m=math.ceil(math.log2(32/dlam));M=2**m
    R=math.ceil((32/9)*math.log(1/beta));R+=int(R%2==0)
    calls=2*L*R*r*(M-1)
    error=2*kappa*dH/(1-kappa*dH)+e+epsilon/8
    assert h*B<=.5+1e-14 and h*C<=dH+1e-14 and error<epsilon
    return dict(scope='completed consistent-microstep median-QPE theorem; not the earlier direct-unitary adapter',r_base=r,h=h,clock_bits_per_register=m,clock_registers=R,phase_bins=M,hs1_calls_per_attempt=calls,ideal_success_lower_bound=1/(256*kappa*kappa),implemented_success_lower_bound=1/(400*kappa*kappa),expected_hs1_calls_upper_bound=400*kappa*kappa*calls,attempt_cap=math.ceil(400*kappa*kappa*math.log(1/delta)),state_error_upper_bound_with_implementation_margin=error,implementation_operator_error_budget=epsilon/(64*K),compiled_T_count=None)

if __name__=='__main__':
    inp=dict(kappa=3,L=3,B=17/15,C=8/75,epsilon=.25,delta=.01)
    result=schedule(**inp)
    (HERE/'completed-model-example.json').write_text(json.dumps({'input':inp,'output':result},indent=2)+'\n')
    stricter=dict(inp,epsilon=inp['epsilon']/2)
    assert schedule(**stricter)['hs1_calls_per_attempt']>=result['hs1_calls_per_attempt']
    print(json.dumps(result,indent=2))
