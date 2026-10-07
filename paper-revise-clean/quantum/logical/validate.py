"""Small independent formula checks and regressions for the clean logical model."""
from decimal import Decimal as D, localcontext
import json
from modern_qlsa import estimate, f, table_v


def main():
    p=dict(N=1024,kappa=100,epsilon_state='0.01',delta='0.01')
    s=estimate(p);r=estimate(dict(p,include_readout=True))
    assert f(p)==86705344699164751
    assert r['T_total']==271767176507565562710978575
    assert s['logical_qubits_peak']==4192280
    assert r['logical_qubits_peak']==4192281
    assert r['readout']['samples_per_family']==9688792223
    assert r['readout']['T_magnitude_samples']+r['readout']['T_sign_samples']==r['T_total']
    assert r['readout']['retry_multiplier_applied']==1
    assert D(r['readout']['output_error_model'])<=D('0.010000000000000000000000000001')
    assert r['qec_input']['T_count']==r['T_total']!=r['T_retry_budget']
    assert r['qec_input']['logical_qubits']==r['logical_qubits_peak']
    # Width is a simultaneous allocation; changing repetition count cannot change it.
    more=estimate(dict(p,delta='0.000001'))
    assert more['T_total']>s['T_total'] and more['logical_qubits_peak']==s['logical_qubits_peak']
    padded=estimate(dict(p,N=1025));exact=estimate(dict(p,N=2048))
    assert padded['padded_dimension']==2048
    assert padded['logical_qubits_peak']==exact['logical_qubits_peak']
    # Source Tables III--V hand example, with logarithms exactly equal to two.
    with localcontext() as c:
        c.prec=80
        a=table_v(2,3,2,'.25','.25','.25','.25','.25')
        assert a['T_BE']==184 and a['T_controlled_BE']==200 and a['T_SP']==48
        assert a['T_QLSS']==3269 and a['T_controlled_QLSS']==3365
    for change in [dict(N=1),dict(kappa=0),dict(sparsity=5),dict(include_readout='true'),
                   dict(epsilon_readout='.01'),dict(include_readout=True,delta_readout=1)]:
        try:estimate(dict(p,**change))
        except ValueError:pass
        else:raise AssertionError('invalid or unsupported parameter accepted')
    print(json.dumps(dict(result='passed',checks=[
        'previous state and tomography T counts preserved',
        'Tables III/V logical widths match hand arithmetic',
        'tomography costs exclusive, retry not double counted, error budget respected',
        'QEC fields use selected workload rather than baseline',
        'serial retries preserve width and non-power-of-two dimensions pad consistently',
        'primitive counts and both Table V rows match independent small example',
        'unsupported/invalid parameters rejected']),indent=2))


if __name__=='__main__':main()
