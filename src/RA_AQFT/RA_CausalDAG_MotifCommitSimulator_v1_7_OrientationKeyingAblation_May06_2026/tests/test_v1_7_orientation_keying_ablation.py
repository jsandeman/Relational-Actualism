import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.ra_orientation_keying_ablation import (
    orientation_link_witness,
    all_pairs_mean_jaccard,
    parent_anchored_jaccard,
    family_orientation_overlap,
    run,
)


class TinyDAG:
    def __init__(self):
        self.parents = {0: set(), 1: {0}, 2: {0}, 3: {1, 2}}
        self.children = {0: {1, 2}, 1: {3}, 2: {3}, 3: set()}
        self.depth = {0: 0, 1: 1, 2: 1, 3: 2}


class OrientationKeyingAblationTests(unittest.TestCase):
    def test_member_indexed_changes_same_cut(self):
        dag = TinyDAG()
        cut = {1, 2}
        a = orientation_link_witness(dag, cut, 0, keying="member_indexed_edge_pair")
        b = orientation_link_witness(dag, cut, 1, keying="member_indexed_edge_pair")
        self.assertNotEqual(a, b)

    def test_no_member_keying_same_cut_stable(self):
        dag = TinyDAG()
        cut = {1, 2}
        a = orientation_link_witness(dag, cut, 0, keying="edge_pair_signed_no_member")
        b = orientation_link_witness(dag, cut, 1, keying="edge_pair_signed_no_member")
        self.assertEqual(a, b)

    def test_all_pairs_and_parent_anchored_differ(self):
        a = frozenset({"a", "b"})
        b = frozenset({"a", "c"})
        c = frozenset({"d"})
        witnesses = [a, b, c]
        self.assertNotEqual(all_pairs_mean_jaccard(witnesses), parent_anchored_jaccard(witnesses))

    def test_catalog_augmented_has_at_least_base_tokens(self):
        dag = TinyDAG()
        cuts = [frozenset({1}), frozenset({2})]
        base, _, base_tokens, _ = family_orientation_overlap(
            dag, cuts, keying="edge_pair_signed_no_member", trial_key="t", catalog_tokens=[]
        )
        aug, _, aug_tokens, _ = family_orientation_overlap(
            dag, cuts, keying="catalog_augmented_edge_pair", trial_key="t", catalog_tokens=["cat:a", "cat:b"]
        )
        self.assertGreaterEqual(aug_tokens, base_tokens)
        self.assertGreaterEqual(aug, 0.0)

    def test_end_to_end_if_v0_9_available(self):
        v09 = os.environ.get("RA_V0_9_SIMULATOR_DIR")
        if not v09:
            self.skipTest("RA_V0_9_SIMULATOR_DIR not set")
        with tempfile.TemporaryDirectory() as td:
            summary = run(
                v0_9_simulator_dir=Path(v09),
                native_manifest_dir=None,
                output_dir=Path(td),
                seed_start=17,
                seed_stop=18,
                steps=8,
                severance_seeds=(101,),
                modes=("orientation_degradation", "selector_stress"),
                severities=(0.5,),
                threshold_fractions=(0.5,),
                family_semantics=("augmented_exact_k",),
                max_targets=3,
                keyings=("member_indexed_edge_pair", "edge_pair_signed_no_member", "shuffled_overlap_control"),
            )
            self.assertGreater(summary["keyed_rows"], 0)
            self.assertTrue((Path(td) / "ra_v1_7_specificity_by_keying.csv").exists())


if __name__ == "__main__":
    unittest.main()
