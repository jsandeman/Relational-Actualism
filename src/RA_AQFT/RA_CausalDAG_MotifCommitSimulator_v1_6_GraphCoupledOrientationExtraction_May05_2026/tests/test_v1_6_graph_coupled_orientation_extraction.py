import tempfile
import unittest
from pathlib import Path

from analysis.ra_graph_coupled_orientation_extraction import (
    graph_coupled_orientation_link_witness,
    family_mean_jaccard,
    family_parent_anchored_jaccard,
    family_all_pairs_mean_jaccard,
    aggregate_per_cell,
    decoupling_audit,
    partial_correlation,
    specificity_audit,
    run,
)


class _FakeDAG:
    """Minimal DAG mimicking the v0.9 simulator's CausalDAG surface."""
    def __init__(self, edges):
        self.parents = {}
        self.children = {}
        for p, c in edges:
            self.parents.setdefault(c, set()).add(p)
            self.children.setdefault(p, set()).add(c)
            self.parents.setdefault(p, set())
            self.children.setdefault(c, set())
        # Topo depth
        self.depth = {}
        for v in self._topo_sort():
            ps = self.parents.get(v, set())
            self.depth[v] = 0 if not ps else 1 + max(self.depth[p] for p in ps)

    def _topo_sort(self):
        order = []
        seen = set()
        verts = set(self.parents) | set(self.children)
        while len(order) < len(verts):
            for v in sorted(verts):
                if v in seen: continue
                if self.parents.get(v, set()) <= seen:
                    order.append(v); seen.add(v); break
            else:
                break
        return order


class GraphCoupledExtractionTests(unittest.TestCase):
    def test_orientation_witness_keys_are_edge_based(self):
        dag = _FakeDAG([(0, 1), (1, 2), (2, 3)])
        w = graph_coupled_orientation_link_witness(dag, [1, 2], member_idx=0)
        # Should contain edge keys for (0,1), (1,2), (2,3) with prefixes
        for k in w:
            self.assertTrue(k.startswith("olink:"))
            self.assertIn("->", k)

    def test_orientation_witness_varies_with_member(self):
        dag = _FakeDAG([(0, 1), (1, 2)])
        a = graph_coupled_orientation_link_witness(dag, [1, 2], 0)
        b = graph_coupled_orientation_link_witness(dag, [1, 2], 1)
        self.assertNotEqual(a, b)

    def test_family_mean_jaccard_is_all_pairs(self):
        dag = _FakeDAG([(0, 1), (1, 2), (2, 3), (3, 4)])
        cuts = [frozenset({1, 2}), frozenset({1, 2, 3}), frozenset({1})]
        ws = [graph_coupled_orientation_link_witness(dag, c, mi) for mi, c in enumerate(cuts)]
        j = family_mean_jaccard(ws)
        self.assertEqual(j, family_all_pairs_mean_jaccard(ws))
        self.assertIsInstance(j, float)
        self.assertGreaterEqual(j, 0.0)
        self.assertLessEqual(j, 1.0)

    def test_parent_anchored_jaccard_is_separate_diagnostic(self):
        dag = _FakeDAG([(0, 1), (1, 2), (2, 3), (3, 4), (1, 4)])
        cuts = [frozenset({1, 2}), frozenset({2, 3}), frozenset({1, 4})]
        ws = [graph_coupled_orientation_link_witness(dag, c, mi) for mi, c in enumerate(cuts)]
        self.assertIsInstance(family_parent_anchored_jaccard(ws), float)
        self.assertIsInstance(family_all_pairs_mean_jaccard(ws), float)

    def test_aggregate_and_audit_run_on_synthetic_rows(self):
        rows = []
        for mode in ["ledger_failure", "orientation_degradation", "selector_stress"]:
            for sem in ["at_least_k", "augmented_exact_k"]:
                for sev in [0.0, 0.5, 1.0]:
                    for thr in [0.5]:
                        for sw in [1, 2, 3]:
                            rows.append({
                                "mode": mode, "family_semantics": sem,
                                "severity": sev, "threshold_fraction": thr,
                                "support_width": sw,
                                "certification_rescue_rate": 0.1 if mode == "orientation_degradation" else 0.05,
                                "v1_6_graph_coupled_orientation_link_overlap": 0.3 + 0.1 * sw,
                                "support_overlap": 0.7,
                                "frontier_overlap": 0.7,
                                "orientation_overlap": 0.7,
                                "ledger_overlap": 0.85,
                            })
        per_cell = aggregate_per_cell(rows)
        self.assertGreater(len(per_cell), 0)
        decoupling = decoupling_audit(per_cell)
        self.assertGreater(len(decoupling), 0)
        spec = specificity_audit(per_cell)
        self.assertGreater(len(spec), 0)
        pcorr = partial_correlation(per_cell)
        self.assertGreater(len(pcorr), 0)


class EndToEndIntegrationTests(unittest.TestCase):
    """Smoke-test the full simulator-coupled run on a tiny config."""
    def test_run_minimum_config_against_v0_9_simulator(self):
        v0_9_dir = Path(__file__).resolve().parents[2] / \
            "RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026" / "simulator"
        if not v0_9_dir.exists():
            self.skipTest(f"v0.9 simulator dir not found at {v0_9_dir}")
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            summary = run(
                v0_9_simulator_dir=v0_9_dir,
                output_dir=out,
                seed_start=17, seed_stop=18,    # 1 seed
                severance_seeds=(101,),
                modes=("orientation_degradation",),
                severities=(0.5,),
                threshold_fractions=(0.5,),
                family_semantics=("augmented_exact_k",),
                max_targets=2,
            )
            self.assertEqual(summary["version"], "v1.6")
            self.assertGreater(summary["n_trials"], 0)
            self.assertTrue(summary["v1_6_disconnection_closed"])
            self.assertTrue((out / "ra_v1_6_trial_rows.csv").exists())


if __name__ == "__main__":
    unittest.main()
