import csv
import tempfile
import unittest
from pathlib import Path

from analysis.ra_concrete_graph_orientation_extraction import (
    ConcreteDAG,
    make_chain,
    make_balanced_branch,
    make_corpus,
    downward_closed_cuts,
    family_around_cut,
    support_witness,
    orientation_link_witness,
    ledger_witness,
    jaccard,
    family_mean_jaccard,
    build_concrete_components,
    run,
)


class ConcreteDAGTests(unittest.TestCase):
    def test_chain_topology(self):
        g = make_chain(5)
        self.assertEqual(len(g.vertices), 5)
        self.assertEqual(len(g.edges), 4)
        self.assertEqual(g.parents_of(0), frozenset())
        self.assertEqual(g.parents_of(1), frozenset({0}))
        self.assertEqual(g.children_of(0), frozenset({1}))
        self.assertEqual(g.depth_of(4), 4)
        self.assertEqual(g.ancestors_of(3), frozenset({0, 1, 2}))

    def test_branch_topology(self):
        g = make_balanced_branch(depth=2, branch_factor=2)
        self.assertEqual(len(g.vertices), 7)  # 1 + 2 + 4
        self.assertEqual(len(g.children_of(0)), 2)
        self.assertEqual(g.depth_of(0), 0)

    def test_corpus_diversity(self):
        corpus = make_corpus()
        self.assertGreater(len(corpus), 30)
        labels = {g.label for g in corpus}
        self.assertGreater(len(labels), 20)

    def test_orientation_link_keys_are_edge_based_not_vertex_based(self):
        """Critical decoupling test: orientation witness keys differ from
        support witness keys even when they describe the same cut.
        """
        g = make_chain(5)
        cut = frozenset({0, 1, 2})
        sup = support_witness(g, cut)
        ori = orientation_link_witness(g, cut, member_idx=0)
        self.assertGreater(len(sup), 0)
        self.assertGreater(len(ori), 0)
        # Orientation keys carry "olink:" prefix and edges; support carries "support:" + vertex.
        for k in ori:
            self.assertTrue(k.startswith("olink:"))
            self.assertIn("->", k)
        for k in sup:
            self.assertTrue(k.startswith("support:"))
            self.assertNotIn("->", k)
        self.assertEqual(sup & ori, frozenset())

    def test_orientation_link_varies_with_member_index(self):
        """Two siblings with different member_idx should produce different
        orientation witnesses (sign flip), making per-member overlap distinct.
        """
        g = make_chain(5)
        cut = frozenset({1, 2})
        a = orientation_link_witness(g, cut, member_idx=0)
        b = orientation_link_witness(g, cut, member_idx=1)
        self.assertNotEqual(a, b)

    def test_jaccard_basic(self):
        self.assertEqual(jaccard(frozenset({"a"}), frozenset({"a"})), 1.0)
        self.assertEqual(jaccard(frozenset({"a"}), frozenset({"b"})), 0.0)
        self.assertAlmostEqual(jaccard(frozenset({"a", "b"}), frozenset({"a", "c"})), 1 / 3)


class FamilyAndOverlapTests(unittest.TestCase):
    def test_family_includes_parent_first(self):
        g = make_chain(6)
        cuts = downward_closed_cuts(g, max_size=4)
        members = family_around_cut(g, cuts[2], n_members=10)
        self.assertEqual(members[0], cuts[2])
        self.assertEqual(len(members), 10)

    def test_orientation_overlap_decouples_from_support_overlap(self):
        """Across families on chain graphs, orientation-link Jaccard differs
        from support Jaccard when sign-flipping members are present.
        """
        g = make_chain(8)
        cuts = downward_closed_cuts(g, max_size=5)
        family = family_around_cut(g, cuts[2], n_members=8)
        sup_w = [support_witness(g, c) for c in family]
        ori_w = [orientation_link_witness(g, c, mi) for mi, c in enumerate(family)]
        sup_overlap = family_mean_jaccard(sup_w)
        ori_overlap = family_mean_jaccard(ori_w)
        # They should not be exactly equal (different keying schemes).
        self.assertNotEqual(sup_overlap, ori_overlap)


class EndToEndTests(unittest.TestCase):
    def _make_synthetic_v1_0_csv(self, path: Path):
        rows = []
        for mode in ["ledger_failure", "orientation_degradation", "selector_stress"]:
            for sem in ["at_least_k", "augmented_exact_k"]:
                for sev in [0.0, 0.5, 1.0]:
                    for thr in [0.25, 0.5, 0.75, 1.0]:
                        for sw in [1, 2, 3, 4]:
                            rows.append({
                                "mode": mode,
                                "family_semantics": sem,
                                "severity": sev,
                                "threshold_fraction": thr,
                                "support_width": sw,
                                "samples": 100,
                                "certification_rescue_rate": 0.1 if mode == "orientation_degradation" else 0.05,
                                "support_overlap": 0.7,
                                "frontier_overlap": 0.7,
                                "orientation_overlap": 0.7,
                                "ledger_overlap": 0.85,
                                "causal_past_overlap": 0.8,
                                "bdg_kernel_overlap": 0.78,
                                "firewall_overlap": 0.75,
                            })
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            for r in rows:
                w.writerow(r)

    def test_run_writes_outputs_and_summary(self):
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in"
            out = Path(td) / "out"
            self._make_synthetic_v1_0_csv(inp / "ra_native_certificate_components_v1_0.csv")
            summary = run(inp, out)
            self.assertEqual(summary["version"], "v1.5")
            self.assertGreater(summary["concrete_component_rows"], 0)
            self.assertTrue((out / "ra_concrete_components_v1_5.csv").exists())
            self.assertTrue((out / "ra_concrete_orientation_witness_summary_v1_5.md").exists())
            # Decoupling should resolve at least one comparison as decoupled.
            self.assertGreater(summary["decoupled_count"], 0)


if __name__ == "__main__":
    unittest.main()
