import tempfile
from pathlib import Path
import pandas as pd
from analysis.ra_v181_compliant_witness_coverage import load_normalized_inputs, write_outputs


def make_b2(out: Path):
    pd.DataFrame([
        dict(run_seed=1,motif='m',motif_kind='k',site=1,threshold_fraction=.5,family_semantics='augmented_exact_k',support_width=2,family_size=3,active_all_pairs_orientation_jaccard=0.1,active_parent_anchored_orientation_jaccard=0.1,active_orientation_overlap_bin='low'),
        dict(run_seed=1,motif='n',motif_kind='k',site=2,threshold_fraction=.5,family_semantics='augmented_exact_k',support_width=2,family_size=3,active_all_pairs_orientation_jaccard=0.9,active_parent_anchored_orientation_jaccard=0.9,active_orientation_overlap_bin='high'),
    ]).to_csv(out/'ra_trackB2_active_graph_orientation_overlap.csv', index=False)


def test_joint_estimability_detected_for_b2():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td); make_b2(d)
        df=load_normalized_inputs([d])
        summary=write_outputs(df,d/'out')
        assert summary.estimable_joint_strata == 1
        assert summary.orientation_rescue_claim_made is False


def test_v17_normalization_assigns_bins():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td)
        pd.DataFrame([
            dict(seed=1,mode='orientation_degradation',severity=.5,support_width=2,threshold_fraction=.5,family_semantics='augmented_exact_k',family_size=3,v1_7_keying='edge_pair_signed_no_member',v1_7_orientation_overlap_all_pairs=x,v1_7_orientation_overlap_parent_anchored=x,v1_7_trial_key=str(i))
            for i,x in enumerate([0.0,.1,.2,.8,.9,1.0])
        ]).to_csv(d/'ra_v1_7_keyed_trial_rows.csv',index=False)
        df=load_normalized_inputs([d])
        assert set(df.orientation_bin) == {'low','medium','high'}


def test_non_estimable_when_only_low_medium():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td)
        pd.DataFrame([
            dict(run_seed=1,motif='m',motif_kind='k',site=i,threshold_fraction=.5,family_semantics='at_least_k',support_width=1+i%2,family_size=1+i%2,active_all_pairs_orientation_jaccard=0.0,active_parent_anchored_orientation_jaccard=0.0,active_orientation_overlap_bin='low' if i<2 else 'medium')
            for i in range(4)
        ]).to_csv(d/'ra_trackB2_active_graph_orientation_overlap.csv', index=False)
        df=load_normalized_inputs([d])
        summary=write_outputs(df,d/'out')
        assert summary.estimable_joint_strata == 0
