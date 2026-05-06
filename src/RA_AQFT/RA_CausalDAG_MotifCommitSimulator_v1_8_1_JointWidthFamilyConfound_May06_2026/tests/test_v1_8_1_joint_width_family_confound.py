import tempfile
import unittest
from pathlib import Path
import pandas as pd

from analysis.ra_joint_width_family_confound import run_analysis, load_keyed_rows, aggregate_matched_gaps, matched_stratum_gaps, raw_specificity_gaps


def make_rows(path: Path):
    rows=[]
    keyings=["edge_pair_signed_no_member","shuffled_overlap_control"]
    # create two widths and family sizes where graph has residual after joint matching,
    # while shuffled gap shrinks inside joint strata.
    for keying in keyings:
        for width,fsize in [(2,3),(3,7)]:
            for bin_label, ov in [("low",0.1),("high",0.9)]:
                for i in range(6):
                    if keying == "edge_pair_signed_no_member":
                        rescue = (bin_label == "low" and i < 4) or (bin_label == "high" and i < 1)
                    else:
                        rescue = (i < 2)  # equal low/high inside strata
                    rows.append({
                        "v1_7_keying": keying,
                        "mode": "orientation_degradation",
                        "family_semantics": "augmented_exact_k",
                        "severity": 0.5,
                        "threshold_fraction": 0.5,
                        "v1_7_orientation_overlap_all_pairs": ov + 0.001*i,
                        "certification_rescue_event": rescue,
                        "support_width": width,
                        "family_size": fsize,
                        "selector_stress": False,
                    })
    # selector stress guardrail rows
    for keying in keyings:
        for ov in [0.1,0.5,0.9]:
            rows.append({
                "v1_7_keying": keying,
                "mode": "selector_stress",
                "family_semantics": "augmented_exact_k",
                "severity": 0.5,
                "threshold_fraction": 0.5,
                "v1_7_orientation_overlap_all_pairs": ov,
                "certification_rescue_event": False,
                "support_width": 2,
                "family_size": 3,
                "selector_stress": True,
            })
    df=pd.DataFrame(rows)
    df.to_csv(path/"ra_v1_7_keyed_trial_rows.csv", index=False)


class JointWidthFamilyConfoundTests(unittest.TestCase):
    def test_load_assigns_bins(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); make_rows(p)
            df=load_keyed_rows(p)
            self.assertIn("orientation_bin", df.columns)
            self.assertTrue(set(df["orientation_bin"]).issubset({"low","medium","high"}))

    def test_joint_matching_detects_graph_vs_shuffled_difference(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); make_rows(p)
            out=p/"out"
            s=run_analysis(p,out)
            gvs=pd.read_csv(out/"ra_v1_8_1_graph_vs_shuffled_joint_matched.csv")
            row=gvs[(gvs["graph_keying"]=="edge_pair_signed_no_member") & (gvs["mode"]=="orientation_degradation")].iloc[0]
            self.assertEqual(row["interpretation"], "graph_differs_from_shuffled_after_joint_matching")
            self.assertTrue(abs(row["joint_matched_gap_delta_graph_minus_shuffled"])>0.1)
            self.assertTrue(s.selector_guardrail_passed)

    def test_outputs_exist(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); make_rows(p); out=p/"out"
            run_analysis(p,out)
            expected=[
                "ra_v1_8_1_raw_specificity_gaps.csv",
                "ra_v1_8_1_width_matched_gap.csv",
                "ra_v1_8_1_joint_stratum_gaps.csv",
                "ra_v1_8_1_joint_width_family_matched_gap.csv",
                "ra_v1_8_1_graph_vs_shuffled_joint_matched.csv",
                "ra_v1_8_1_estimability_by_stratum.csv",
                "ra_v1_8_1_orientation_gap_decomposition.csv",
                "ra_v1_8_1_joint_confound_summary.md",
            ]
            for name in expected:
                self.assertTrue((out/name).exists(), name)

    def test_insufficient_joint_strata_status(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)
            rows=[]
            # high and low bins only occur in different family sizes -> raw gap estimable, joint gap not.
            for fsize, ov, rescue in [(3,0.1,True),(7,0.9,False)]:
                for i in range(6):
                    rows.append({
                        "v1_7_keying":"edge_pair_signed_no_member",
                        "mode":"orientation_degradation",
                        "family_semantics":"at_least_k",
                        "severity":0.5,"threshold_fraction":0.5,
                        "v1_7_orientation_overlap_all_pairs":ov+0.001*i,
                        "certification_rescue_event":rescue,
                        "support_width":2,"family_size":fsize,
                        "selector_stress":False,
                    })
            pd.DataFrame(rows).to_csv(p/"ra_v1_7_keyed_trial_rows.csv", index=False)
            out=p/"out"; run_analysis(p,out)
            joint=pd.read_csv(out/"ra_v1_8_1_joint_width_family_matched_gap.csv")
            self.assertIn("insufficient_joint_matched_low_high_bins", set(joint["status"]))

if __name__ == "__main__":
    unittest.main()
