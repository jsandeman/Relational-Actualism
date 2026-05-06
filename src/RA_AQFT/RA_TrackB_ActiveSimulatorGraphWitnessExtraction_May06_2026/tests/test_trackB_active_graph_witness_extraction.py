import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

import ra_active_graph_witness_extraction as mod


class TinyDag:
    parents = {0: set(), 1: {0}, 2: {0}, 3: {1, 2}}
    children = {0: {1, 2}, 1: {3}, 2: {3}, 3: set()}
    depth = {0: 0, 1: 1, 2: 1, 3: 2}


class TrackB2ActiveGraphWitnessTests(unittest.TestCase):
    def test_graph_tokens_are_member_index_free(self):
        dag = TinyDag()
        cut = frozenset({1, 2})
        a = mod.active_graph_cut_orientation_tokens(dag, cut)
        b = mod.active_graph_cut_orientation_tokens(dag, cut)
        self.assertEqual(a, b)
        self.assertTrue(all(":m" not in tok for tok in a))

    def test_member_indexed_control_is_unstable(self):
        toks = {"x", "y"}
        self.assertNotEqual(mod.member_indexed_control_tokens(toks, 0), mod.member_indexed_control_tokens(toks, 1))

    def test_all_pairs_and_parent_anchored_jaccard_can_differ(self):
        ws = [frozenset({"a", "b"}), frozenset({"a"}), frozenset({"b"})]
        self.assertNotEqual(mod.all_pairs_mean_jaccard(ws), mod.parent_anchored_jaccard(ws))

    def test_bins(self):
        self.assertEqual(mod._bin_overlap(0.1), "low")
        self.assertEqual(mod._bin_overlap(0.5), "medium")
        self.assertEqual(mod._bin_overlap(0.9), "high")

    def test_end_to_end_against_v09_if_available(self):
        simdir = os.environ.get("RA_V09_SIMULATOR_DIR")
        if not simdir:
            self.skipTest("RA_V09_SIMULATOR_DIR not set")
        cfg = mod.ActiveExtractorConfig(seeds=(17,), steps=12, max_targets=3, threshold_fractions=(1.0,0.5), family_semantics=("at_least_k",))
        with tempfile.TemporaryDirectory() as td:
            summary = mod.run(Path(td), Path(simdir), cfg)
            self.assertGreater(summary["witness_rows"], 0)
            self.assertTrue(summary["graph_surface_member_index_free"])
            self.assertFalse(summary["orientation_rescue_claim_made"])


if __name__ == "__main__":
    unittest.main()
