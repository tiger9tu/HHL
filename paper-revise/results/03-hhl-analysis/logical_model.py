"""Internal schedule helper; task-01 export is in export_contract.py: certified first-order PF schedule, per HHL trial.
No oracle implementation, QPE accuracy theorem, or gate synthesis is inferred.
"""
import json, math, sys

def evaluate(record):
    pp,cq=record['pp'],record['cq']
    N,L=pp['N'],cq['decomposition_terms']
    m=cq['clock_qubits']; C=cq['commutator_bound']; base=cq['base_evolution_time']
    eps=pp['epsilon_state_pf']; p=cq['reference_success_lower_bound']
    if not isinstance(N,int) or N<2 or not isinstance(L,int) or L<1 or not isinstance(m,int) or m<1:
        raise ValueError('Positive integer dimensions required')
    if not (math.isfinite(C) and C>=0 and math.isfinite(base) and base>0 and 0<eps<1 and 0<p<=1):
        raise ValueError('Invalid bound, time, error, or success budget')
    times=[base*2**j for j in range(m)]; total=sum(times)
    eta=eps*math.sqrt(p)/2
    steps=[max(1,math.ceil(C*total*t/eta)) for t in times]
    eta_bound=C*sum(t*t/r for t,r in zip(times,steps))
    count=2*L*sum(steps)
    p_actual=max(0,math.sqrt(p)-eta_bound)**2
    result={'status':'partial_model_application_and_compilation_pending','scope':'per_attempt_including_QPE_and_inverse_QPE; PF_error_only',
        'evolution_time_units':'inverse units of normalized H; not seconds','steps_by_clock_bit':steps,
        'hs1_controlled_calls':count,'full_circuit_pf_error_bound':eta_bound,
        'conditioned_state_pf_error_bound':2*eta_bound/math.sqrt(p),
        'success_lower_bound_after_pf':p_actual,'expected_attempts_per_success_upper_bound':1/p_actual,
        'gate_counts':None,'logical_depth':None,'logical_qubits':None,
        'qec_included':False,'physical_resources_included':False,
        'state_preparation_included':False,'output_measurement_included':False,
        'repetitions_applied':False,'qpe_accuracy_certified':False}
    costs=cq.get('controlled_hs1_cost')
    if costs is not None:
        result['gate_counts']={g:count*v for g,v in costs['gate_counts'].items()}
        result['logical_depth']=count*costs['serial_depth']
        result['logical_qubits']=math.ceil(math.log2(N))+m+1+costs['extra_workspace_qubits']
        result['scope']+='; counts_simulation_only; add_QFT_reciprocal_and_IO'
    return result

if __name__=='__main__':
    with open(sys.argv[1]) as f: config=json.load(f)
    print(json.dumps(evaluate(config),indent=2))
