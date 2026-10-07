"""Generate modern-QLSA logical resource data. Python >=3.11, standard library.

Default: the N=1024, kappa=100, epsilon=delta=.01 example in both output modes.
--input accepts one parameter object or a list, and respects each readout flag.
--sweep adds a small parameter sweep, with both modes for every point.
"""
import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
from modern_qlsa import VERSION, estimate

HERE=Path(__file__).resolve().parent


def default_cases():
    p=dict(N=1024,kappa=100,epsilon_state='0.01',delta='0.01')
    return [dict(p,include_readout=False),dict(p,include_readout=True)]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,help='JSON parameter object or list')
    parser.add_argument('--output-dir',type=Path,default=HERE/'data')
    parser.add_argument('--sweep',action='store_true',help='add N/kappa/accuracy sweep in both modes')
    args=parser.parse_args()
    if args.input:
        values=json.loads(args.input.read_text())
        cases=values if isinstance(values,list) else [values]
    else:
        cases=default_cases()
    if args.sweep:
        for N in [256,1024,4096]:
            for k in [10,100,1000]:
                for eps in ['0.01','0.001']:
                    for readout in [False,True]:
                        p=dict(N=N,kappa=k,epsilon_state=eps,delta='0.01',include_readout=readout)
                        if p not in cases:cases.append(p)
    if not cases or any(not isinstance(p,dict) for p in cases):
        parser.error('input must be a parameter object or nonempty list of objects')
    # Validate/evaluate the complete batch before writing outputs.
    results=[estimate(p) for p in cases]
    out=args.output_dir;out.mkdir(parents=True,exist_ok=True)
    def write(name,obj):
        (out/name).write_text(json.dumps(obj,indent=2)+'\n')
    write('inputs.json',cases);write('resources.json',results)
    columns=['case','algorithm','N','padded_dimension','kappa','effective_inverse_gap',
             'include_readout','epsilon_state_requested','epsilon_state_used',
             'epsilon_output_target','failure_target','Q','d','matrix_calls_per_plain_execution',
             'plain_circuit_T','controlled_circuit_T','executions_plain','executions_controlled',
             'T_count','logical_qubits_peak','output_scope','certified_upper_bound']
    with (out/'resources.csv').open('w',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=columns);writer.writeheader()
        for index,r in enumerate(results):
            p=r['parameters'];ro=r['readout']
            Q,d=(ro['Q'],ro['d']) if ro else (r['Q'],r['d'])
            writer.writerow(dict(case=index,algorithm=r['algorithm'],N=r['N'],padded_dimension=r['padded_dimension'],
                kappa=r['kappa'],effective_inverse_gap=r['effective_inverse_gap'],include_readout=r['include_readout'],
                epsilon_state_requested=p.get('epsilon_state','0.01'),
                epsilon_state_used=ro['epsilon_state_used'] if ro else p.get('epsilon_state','0.01'),
                epsilon_output_target=ro['epsilon_output_target'] if ro else p.get('epsilon_state','0.01'),
                failure_target=ro['delta_readout'] if ro else p.get('delta','0.01'),Q=Q,d=d,
                matrix_calls_per_plain_execution=2*(Q+d),
                plain_circuit_T=ro['T_plain_per_execution'] if ro else r['T_per_attempt_ceiling'],
                controlled_circuit_T=ro['T_controlled_per_execution'] if ro else '',
                executions_plain=ro['samples_per_family'] if ro else r['retry_cap'],
                executions_controlled=ro['samples_per_family'] if ro else 0,
                T_count=r['T_total'],logical_qubits_peak=r['logical_qubits_peak'],
                output_scope=r['output_scope'],certified_upper_bound=False))
    source_paths=[HERE/'modern_qlsa.py',HERE/'generate_data.py',HERE/'README.md',HERE/'validate.py']
    write('manifest.json',dict(model_version=VERSION,generated_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(),reference='https://arxiv.org/pdf/2211.12489v1',
        source_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in source_paths},
        output_sha256={name:hashlib.sha256((out/name).read_bytes()).hexdigest()
                       for name in ['inputs.json','resources.json','resources.csv']},
        count=len(results)))
    for r in results:
        print('N={}, kappa={}, readout={}: T={}, logical qubits={}'.format(
            r['N'],r['kappa'],r['include_readout'],r['T_total'],r['logical_qubits_peak']))


if __name__=='__main__':main()
