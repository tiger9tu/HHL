"""Reuse task-03 measurements and record task-02 input conversion."""
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from logical_model import estimate

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESULTS = HERE.parent


def dump(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')


def main():
    source = RESULTS/'03-hhl-analysis/trotter-error/experiments/errors.csv'
    rows = [r for r in csv.DictReader(source.open()) if r['family']=='poisson_2d']
    table, full = [], []
    for N in sorted(set(int(r['N']) for r in rows)):
        case = [r for r in rows if int(r['N'])==N]
        first = case[0]
        model = estimate(float(first['kappa']), float(first['B']), float(first['C_comm']))
        candidates = []
        for row in case:
            count = model['tau']/float(row['h'])
            # Keep the exact tested h; don't assume monotonicity at a new step.
            if (row['matrix_bound_applicable']=='True' and
                    abs(count-round(count)) < 1e-8 and count >= 1 and
                    float(row['matrix_error'])+5e-10 <= model['matrix_target']):
                candidates.append((int(round(count)), row))
        selected = min(candidates, key=lambda x:x[0]) if candidates else None
        table.append(dict(N=N, case_id=int(first['case_id']),
                          K_HE=model['K_HE'], C_comm=model['C_comm'],
                          matrix_target=model['matrix_target'],
                          r_bound=model['r_bound'],
                          r_measured=selected[0] if selected else '',
                          selected_matrix_error=float(selected[1]['matrix_error']) if selected else '',
                          minimum_tested_h=min(float(r['h']) for r in case),
                          degree=model['degree'],
                          fragment_exponentials_bound=model['controlled_fragment_exponentials'],
                          expected_attempts_upper=model['expected_attempts_upper']))
        full.append(dict(case_id=int(first['case_id']), N=N, model=model,
                         measured_step_selection=selected[1] if selected else None,
                         measurement_note='FP64 diagnostic with 5e-10 comparison allowance; not interval certification'))
    with (HERE/'reused-poisson-costs.csv').open('w') as f:
        writer = csv.DictWriter(f, fieldnames=list(table[0]))
        writer.writeheader(); writer.writerows(table)
    dump('poisson-models.json', full)

    # Read the current task-02 handoff rather than freezing its numerical defaults.
    metadata = json.loads((RESULTS/'02-application/instance.json').read_text())
    if metadata['version'] != '02-smooth-diffusion-v1' or not metadata['mesh_admissible']:
        raise ValueError('expected an admissible task-02 smooth-diffusion handoff')
    m, beta, eps_out = metadata['m'], metadata['beta'], metadata['epsilon']
    h = 1/(m+1); N=m*m; C=1+beta
    lambda0 = 8/h**2*math.sin(math.pi*h/2)**2
    F_bound = 3*C+9*beta/16
    c_norm=h*h*math.sqrt(N)
    X_max=math.sqrt(N)*F_bound/lambda0
    state_allowance=eps_out/(4*c_norm*X_max)
    assert N == metadata['N']
    assert math.isclose(lambda0, metadata['lambda_min_lower'], rel_tol=1e-12)
    assert math.isclose(X_max, metadata['solution_norm_upper'], rel_tol=1e-12)
    dump('application-input.json', dict(
        instance_id='02-smooth-diffusion-v1', m=m, N=N, beta=beta,
        dimension_padded=2**int(math.ceil(math.log(N,2))),
        epsilon_output=eps_out, lambda0=lambda0,
        alpha_HE_original_A=8*C/h**2, K_HE=8*C/(h*h*lambda0),
        K_BE_scenario=20*C/(h*h*lambda0),
        c_output_norm=c_norm, X_max_bound=X_max,
        phase_aligned_state_allowance=state_allowance,
        trotter_matrix_allowance=(state_allowance/2)/((8*C/(h*h*lambda0))*(2+state_allowance/2)),
        trotter_calibration=None, compiled_microstep_cost=None,
        status='derived application inputs; no matched Trotter data or finite gate estimate',
        metadata_top_level_keys=sorted(metadata.keys())))
    inputs = [
        'paper-revise/prompts/tasks/13-qetu-qlsa.md',
        'paper-revise/prompts/tasks/README.md',
        'paper-revise/prompts/paper-revise.md',
        'paper-revise/results/01-framework/interface.md',
        'paper-revise/results/02-application/specification.md',
        'paper-revise/results/02-application/instance.json',
        'paper-revise/results/03-hhl-analysis/practical-trotter/method-section.tex',
        'paper-revise/results/03-hhl-analysis/trotter-error/trotter-error-estimation.tex',
        'paper-revise/results/03-hhl-analysis/trotter-error/experiments/errors.csv',
        'paper-revise/results/03-hhl-analysis/trotter-error/experiments/run_experiments.py',
        'paper-revise/results/03-hhl-analysis/trotter-error/experiments/configurations.json',
        'paper-revise/results/04-modern-qlsa/model.md',
        'src/HHL/HamiltonianEvolution/TrotterSuzuki/TrotterSuzuki.qs',
        'num/trotter.m', 'num/epsA.m',
        'paper-revise/docs/comment1.pdf', 'paper-revise/docs/comment2.pdf',
        'paper/Explore_Practical_Quantum_Speedup_for_Quantum_Linear_System_of_Equations (1).pdf']
    inputs += [str(p.relative_to(ROOT)) for p in (HERE/'sources').glob('*.pdf')]
    dump('input-versions.json', dict(date_utc='2026-09-09', python=platform.python_version(),
         sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
         commands=['python reproduce.py', 'python validate.py'],
         conventions='dimensionless normalized H; counts are per attempted filter unless labeled'))
    print(json.dumps(dict(poisson_cases=len(table), application_state_allowance=state_allowance)))


if __name__=='__main__':
    main()
