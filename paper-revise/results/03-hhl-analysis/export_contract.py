"""Export a task-01 v1.0.0 stage fragment; not a complete workload record."""
import hashlib,json
from pathlib import Path
from logical_model import evaluate
OUT=Path(__file__).resolve().parent

def q(unit,status,note,**kwargs):
    return dict(unit=unit,status=status,note=note,**kwargs)

def main():
    config=json.loads((OUT/'model-input.json').read_text()); result=evaluate(config); K=result['hs1_controlled_calls']
    sym=lambda unit,expr,note:q(unit,'symbolic',note,expression=expr)
    stage={
      'id':'q_hhl_core_03','branch':'quantum','layer':'logical','owner':'03',
      'scope':'per_output','reuse_key':'none',
      'multiplicity':q('1','known','One core invocation; task 05 applies attempted-circuit multiplicity exactly once.',value=1),
      'statistic':'upper_bound','statistic_note':'PF schedule is a deterministic sufficient bound. Compiled costs and non-HS core remain symbolic. No QPE accuracy certificate or end-to-end output guarantee is supplied.',
      'covers':['q.core'],'derived_from':[],
      'assumptions':['A03-commutator','A03-reference','A03-compilation'],
      'resources':{
        'gate_basis':'compiled Clifford+T; T includes T dagger; exclusive primitive buckets',
        'gates':{g:sym('gate',str(K)+' * g_HS1_'+g+' + g_nonHS_'+g,'Counts both QPE directions; excludes preparation, heralding measurement and readout.') for g in ['T','Clifford']},
        'oracle_queries':{'A':sym('query',str(K)+' * q_A_HS1','Queries per controlled term include compute and uncompute; instantiate the access model.')},
        'queries_expanded':False,
        'depth':sym('layer',str(K)+' * D_HS1 + D_nonHS','Serial upper bound after compiling each controlled term and non-HS core.'),
        't_depth':sym('layer',str(K)+' * DT_HS1 + DT_nonHS','Requires compiled dependency schedule; not inferred from T-count.'),
        'logical_qubits_peak':sym('logical_qubit','1 + 3 + 1 + W_core_peak','Example n_sys=1,m=3; W includes all simultaneously live extra core workspace.'),
        'schedule':'Serial controlled evolutions per R4 plus non-HS QPE/reciprocal/inverse-QPE; supply workspace lifetime and compilation artifact.'}}
    (OUT/'contract-stage.json').write_text(json.dumps(stage,indent=2)+'\n')
    schema_path=OUT.parent/'01-framework/interface.schema.json'; schema=json.loads(schema_path.read_text())
    import jsonschema
    fragment={'$schema':schema['$schema'],'$ref':'#/definitions/stage','definitions':schema['definitions']}
    jsonschema.Draft7Validator(fragment).validate(stage)
    # Behavioral model checks: stricter PF budget cannot reduce count; noncommuting vs commuting.
    tighter=json.loads(json.dumps(config)); tighter['pp']['epsilon_state_pf']/=2
    assert evaluate(tighter)['hs1_controlled_calls']>=K
    assert result['conditioned_state_pf_error_bound']<=config['pp']['epsilon_state_pf']
    commuting=json.loads(json.dumps(config)); commuting['cq']['commutator_bound']=0
    assert evaluate(commuting)['full_circuit_pf_error_bound']==0
    assert evaluate(commuting)['hs1_controlled_calls']==2*config['cq']['decomposition_terms']*config['cq']['clock_qubits']
    validation={'schema_version':'1.0.0','scope':'stage fragment structural validation; not a full-record lineage or accuracy certificate','schema_sha256':hashlib.sha256(schema_path.read_bytes()).hexdigest(),'stage_schema_validation':'passed','schedule_and_budget_checks':'passed'}
    (OUT/'contract-validation.json').write_text(json.dumps(validation,indent=2)+'\n')
    print(json.dumps(validation,indent=2))

if __name__=='__main__':main()
