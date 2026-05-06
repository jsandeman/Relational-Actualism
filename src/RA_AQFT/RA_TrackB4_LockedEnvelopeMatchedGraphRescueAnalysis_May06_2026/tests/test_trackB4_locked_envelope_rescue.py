from pathlib import Path
import tempfile
import pandas as pd

from analysis.ra_trackB4_locked_envelope_rescue import (
    make_demo_rows, normalize_rows, locked_envelope, assign_fixed_bins,
    joint_stratum_gaps, run_analysis, LOCKED_KEYING, CONTROL_KEYING,
)


def test_demo_rows_include_locked_and_control():
    df = make_demo_rows()
    assert LOCKED_KEYING in set(df['keying'])
    assert CONTROL_KEYING in set(df['keying'])
    assert 'certification_rescue_event' in df.columns


def test_locked_envelope_filter_excludes_other_semantics():
    df = make_demo_rows()
    extra = df.iloc[:1].copy()
    extra['family_semantics'] = 'at_least_k'
    both = pd.concat([df, extra], ignore_index=True)
    norm = normalize_rows(both)
    env = locked_envelope(norm)
    assert set(env['family_semantics']) == {'augmented_exact_k'}
    assert set(env['threshold_fraction']) == {0.25}


def test_joint_strata_estimable_on_demo():
    df = assign_fixed_bins(normalize_rows(make_demo_rows()))
    joint = joint_stratum_gaps(df, min_rows_per_bin=10)
    assert joint['estimable_joint_stratum'].any()


def test_end_to_end_outputs():
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        p=td/'demo.csv'
        make_demo_rows().to_csv(p,index=False)
        out=td/'out'
        summary=run_analysis([], out, [p], min_rows_per_bin=10)
        assert summary.locked_envelope_rows > 0
        assert (out/'ra_trackB4_graph_vs_shuffled_controls.csv').exists()
        assert summary.orientation_rescue_claim_made is False
