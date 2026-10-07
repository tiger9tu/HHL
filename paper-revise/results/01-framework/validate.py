#!/usr/bin/env python3
"""Validate contract structure and resource lineage; not a scientific model verifier."""
import argparse
import copy
import json
import math
from pathlib import Path
import jsonschema

HERE = Path(__file__).resolve().parent
SCHEMA = json.loads((HERE / 'interface.schema.json').read_text())

def require(test, message):
    if not test:
        raise ValueError(message)

def known(q):
    return q.get('value') if q.get('status') == 'known' else None

def quantities(x):
    if isinstance(x, dict):
        if {'unit', 'status', 'note'}.issubset(x):
            yield x
        else:
            for y in x.values():
                yield from quantities(y)
    elif isinstance(x, list):
        for y in x:
            yield from quantities(y)

def validate(record):
    jsonschema.Draft7Validator(SCHEMA).validate(record)
    require(all(q['status'] != 'known' or math.isfinite(q['value']) for q in quantities(record)), 'nonfinite quantity')
    stages = record['stages']
    ids = [x['id'] for x in stages]
    require(len(ids) == len(set(ids)), 'duplicate stage IDs')
    byid = {x['id']: x for x in stages}
    aids = [x['id'] for x in record['assumptions']]
    require(len(aids) == len(set(aids)), 'duplicate assumption IDs')
    primitive = {'quantum': set(), 'classical': set()}
    for s in stages:
        require(len(s['covers']) == len(set(s['covers'])), 'duplicate coverage in '+s['id'])
        require(set(s['assumptions']) <= set(aids), 'unknown assumption reference')
        deps = s['derived_from']
        require(len(deps) == len(set(deps)), 'duplicate dependency')
        require(all(x in byid for x in deps), 'unknown dependency')
        require(s['id'] not in deps, 'self dependency')
        if deps:
            require(known(s['multiplicity']) == 1, 'derived stage must consume repetitions exactly once')
            union = set()
            for dep in deps:
                d = byid[dep]
                require(d['branch'] == s['branch'], 'cross-branch cost dependency')
                require(not union.intersection(d['covers']), 'overlapping dependency coverage')
                union.update(d['covers'])
            require(union == set(s['covers']), 'derived coverage must equal its dependency union')
        else:
            require(s['layer'] in ['logical', 'classical_work'], 'physical layer needs upstream workload')
            require(not primitive[s['branch']].intersection(s['covers']), 'double-counted primitive cost')
            primitive[s['branch']].update(s['covers'])
        if s['layer'] == 'logical':
            require(s['branch'] == 'quantum', 'logical stage must be quantum')
        if s['layer'] == 'qec':
            require(s['branch'] == 'quantum', 'QEC stage must be quantum')
            require(all(byid[d]['layer'] == 'logical' for d in deps), 'QEC consumes logical stages only')
            if record['status'] == 'evaluated':
                require(all(byid[d]['resources']['queries_expanded'] for d in deps), 'unexpanded oracle queries')
        if s['layer'] == 'hardware':
            require(all(byid[d]['layer'] in ['qec','classical_work','hardware'] for d in deps), 'hardware requires physical or host workload')
            require(s['resources']['boundary_id'] == record['boundary']['id'], 'energy boundary mismatch')
        if s['statistic'] == 'quantile':
            require('quantile' in s['statistic_note'].lower(), 'quantile level must be identified in note')
    visiting, done = set(), set()
    def visit(sid):
        require(sid not in visiting, 'cyclic resource lineage')
        if sid in done:
            return
        visiting.add(sid)
        for d in byid[sid]['derived_from']:
            visit(d)
        visiting.remove(sid)
        done.add(sid)
    for sid in ids:
        visit(sid)
    # Partial producers may omit physical totals. Any supplied terminal total must be complete.
    consumed = {d for s in stages for d in s['derived_from']}
    for branch in primitive:
        totals = [s for s in stages if s['branch'] == branch and s['layer'] == 'hardware' and s['id'] not in consumed]
        if totals:
            require(len(totals) == 1, 'use one terminal total per branch; alternatives need separate records')
            require(set(totals[0]['covers']) == primitive[branch], 'terminal total omits workload costs')
        if record['status'] == 'evaluated':
            require(bool(totals), 'evaluated comparison needs both branch totals')
    pp = record['pp']
    for name in ['N','s_row','s_col']:
        val = known(pp[name])
        require(val is None or (val >= 1 and val == int(val)), name+' must be a positive integer')
    n = known(pp['N'])
    for name in ['s_row','s_col']:
        val = known(pp[name])
        require(n is None or val is None or val <= n, name+' exceeds N')
    kappa = known(pp['kappa_2'])
    require(kappa is None or kappa >= 1, 'kappa_2 below one')
    b = known(pp['reuse']['outputs'])
    require(b is None or (b >= 1 and b == int(b)), 'outputs must be a positive integer')
    delta = known(pp['output']['delta_total'])
    require(delta is None or 0 < delta < 1, 'invalid total failure probability')
    eps = known(pp['output']['epsilon'])
    require(eps is None or eps > 0, 'epsilon must be positive')
    for budget in record['budgets']:
        val = known(budget['value'])
        if budget['kind'] == 'failure_probability':
            require(val is None or val <= 1, 'failure budget exceeds one')
    for branch in ['quantum', 'classical']:
        for kind, target in [('failure_probability', delta), ('output_error', eps)]:
            budgets = [b for b in record['budgets'] if b['branch'] == branch and b['kind'] == kind]
            matching = [b for b in budgets if b['scope'] == pp['output']['success_scope']]
            if target is not None and matching and all(known(b['value']) is not None for b in matching):
                require(sum(known(b['value']) for b in matching) <= target, 'budget exceeds target')
            if record['status'] == 'evaluated':
                require(bool(matching) and len(matching) == len(budgets), 'evaluated budgets require matching target scope on both branches')
    if record['status'] == 'evaluated':
        require(all(f['status'] != 'unresolved' for f in record['feasibility'].values()), 'unresolved feasibility')
        require(all(q['status'] == 'known' for q in quantities(record)), 'evaluated record contains unresolved quantities')
    return True

def self_test(example):
    validate(example)
    cases = []
    def case(name, mutate):
        x = copy.deepcopy(example)
        mutate(x)
        cases.append((name, x))
    case('wrong cycle units', lambda x: x['stages'][4]['resources']['code_cycles'].update(unit='s'))
    case('unknown is not zero', lambda x: x['pp']['N'].update(status='unknown', value=0))
    case('duplicate primitive cost', lambda x: x['stages'][3]['covers'].append('q.core'))
    case('double-applied repetitions', lambda x: x['stages'][4]['multiplicity'].update(status='known', value=2, expression='2'))
    # Ensure the multiplicity semantic guard is exercised after structural validation as well.
    x = copy.deepcopy(example)
    x['stages'][4]['multiplicity'] = dict(status='known',value=2,unit='1',note='invalid duplicate repetition')
    cases.append(('derived multiplicity semantic guard', x))
    case('missing output work', lambda x: x['stages'][-1]['covers'].remove('c.output'))
    case('incompatible boundary', lambda x: x['stages'][-1]['resources'].update(boundary_id='chip-only'))
    case('unresolved numerical result', lambda x: x.update(status='evaluated'))
    case('invalid condition number', lambda x: x['pp'].update(kappa_2=dict(status='known',value=0,unit='1',note='invalid')))
    for name, bad in cases:
        try:
            validate(bad)
        except (ValueError, jsonschema.ValidationError):
            print('REJECTED:', name)
        else:
            raise AssertionError('invalid fixture accepted: '+name)
    print('PASS: symbolic example and {} rejection cases'.format(len(cases)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', nargs='?', default=str(HERE/'symbolic-example.json'))
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    jsonschema.Draft7Validator.check_schema(SCHEMA)
    record = json.loads(Path(args.record).read_text())
    validate(record)
    print('VALID:', args.record, '(structure and accounting only)')
    if args.self_test:
        self_test(record)
