import tempfile
from pathlib import Path
import pandas as pd
import unittest

from analysis.ra_support_width_family_confound import (
    _assign_tercile_bins,
    raw_specificity_gaps,
    rescue_by_width_matched_bins,
    orientation_gap_after_width_matching,
    shuffled_vs_graph_within_width,
    run_analysis,
)


def sample_rows():
    rows=[]
    for keying in ["edge_pair_signed_no_member", "shuffled_overlap_control"]:
        for width in [1,2]:
            for i, ov in enumerate([0.1,0.2,0.8,0.9]):
                rows.append({
                    "v1_7_keying": keying,
                    "mode": "orientation_degradation",
                    "family_semantics": "augmented_exact_k",
                    "v1_7_orientation_overlap_all_pairs": ov,
                    "certification_rescue_event": (width==2 and ov<0.5),
                    "support_width": width,
                    "family_size": width+1,
                    "selector_stress": False,
                })
    return pd.DataFrame(rows)

class V18ConfoundTests(unittest.TestCase):
    def test_bins_are_assigned_per_cell(self):
        df=_assign_tercile_bins(sample_rows())
        self.assertIn("orientation_bin", df.columns)
        self.assertTrue(set(df.orientation_bin).issubset({"low","medium","high"}))
        self.assertGreaterEqual(df.orientation_bin.nunique(), 3)

    def test_width_matched_gap_computable(self):
        df=_assign_tercile_bins(sample_rows())
        raw=raw_specificity_gaps(df)
        rbw=rescue_by_width_matched_bins(df)
        wg=orientation_gap_after_width_matching(rbw, raw)
        self.assertIn("width_matched_low_minus_high_gap", wg.columns)
        self.assertTrue((wg.matched_width_strata_count >= 1).any())

    def test_shuffled_comparison_pairs_graph_keying(self):
        df=_assign_tercile_bins(sample_rows())
        raw=raw_specificity_gaps(df)
        rbw=rescue_by_width_matched_bins(df)
        wg=orientation_gap_after_width_matching(rbw, raw)
        sg=shuffled_vs_graph_within_width(wg)
        self.assertGreaterEqual(len(sg), 1)
        self.assertIn("width_matched_gap_delta_graph_minus_shuffled", sg.columns)

    def test_end_to_end_writes_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            inp=Path(td)/"inp"; out=Path(td)/"out"; inp.mkdir(); out.mkdir()
            sample_rows().to_csv(inp/"ra_v1_7_keyed_trial_rows.csv", index=False)
            summary=run_analysis(inp,out)
            self.assertTrue((out/"ra_v1_8_confound_summary.csv").exists())
            self.assertTrue((out/"ra_v1_8_width_by_orientation_bin.csv").exists())
            self.assertEqual(summary.input_rows, len(sample_rows()))

if __name__ == "__main__":
    unittest.main()
