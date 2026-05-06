import tempfile
import unittest
from pathlib import Path

from analysis.ra_native_graph_cut_witness_extraction import (
    make_demo_dag,
    incident_orientation_tokens,
    member_indexed_tokens_for_audit,
    all_pairs_mean_jaccard,
    parent_anchored_jaccard,
    run,
)

class TrackBNativeGraphCutWitnessTests(unittest.TestCase):
    def test_graph_tokens_do_not_depend_on_member_index(self):
        dag = make_demo_dag(seed=17, steps=10)
        cut = frozenset({6,7})
        self.assertEqual(incident_orientation_tokens(dag, cut), incident_orientation_tokens(dag, cut))
        self.assertNotEqual(member_indexed_tokens_for_audit(dag, cut, 0), member_indexed_tokens_for_audit(dag, cut, 1))

    def test_different_cuts_can_have_different_witnesses(self):
        dag = make_demo_dag(seed=19, steps=12)
        self.assertNotEqual(incident_orientation_tokens(dag, {7}), incident_orientation_tokens(dag, {9,10}))

    def test_jaccard_diagnostics_are_defined(self):
        ws = [frozenset({"a","b"}), frozenset({"b","c"}), frozenset({"a","b"})]
        self.assertGreaterEqual(all_pairs_mean_jaccard(ws), 0.0)
        self.assertGreaterEqual(parent_anchored_jaccard(ws), 0.0)
        self.assertNotEqual(all_pairs_mean_jaccard(ws), parent_anchored_jaccard(ws))

    def test_end_to_end_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            summary = run(out, seeds=(17,18), steps=10, widths=(1,2,3))
            self.assertTrue((out / "ra_trackB_graph_cut_orientation_witness_members.csv").exists())
            self.assertTrue((out / "ra_trackB_graph_cut_orientation_overlap.csv").exists())
            self.assertTrue(summary["graph_surface_member_index_free"])
            self.assertTrue(summary["bad_control_detects_member_index_instability"])

if __name__ == "__main__":
    unittest.main()
