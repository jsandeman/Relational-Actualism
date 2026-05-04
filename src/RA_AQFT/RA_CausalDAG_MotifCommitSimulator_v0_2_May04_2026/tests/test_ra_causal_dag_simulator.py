import unittest

from simulator.ra_causal_dag_simulator import (
    CausalDAG,
    CommitContext,
    GraphSupportCertifier,
    MotifCandidate,
    MotifCommitProtocol,
    generate_growth_demo,
    make_context,
    run_parameter_sweep,
)


class TestRACausalDAGSimulatorV02(unittest.TestCase):
    def diamond(self):
        dag = CausalDAG()
        n0 = dag.add_node()
        n1 = dag.add_node([n0])
        n2 = dag.add_node([n0])
        n3 = dag.add_node([n1, n2])
        return dag, n0, n1, n2, n3

    def test_hasse_frontier_of_downset(self):
        dag, n0, n1, n2, _n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        self.assertEqual(dag.hasse_frontier(past), frozenset({n1, n2}))

    def test_ready_at_and_future_monotonicity(self):
        dag, n0, n1, _n2, n3 = self.diamond()
        cut = frozenset({n0})
        self.assertTrue(dag.ready_at(cut, n1))
        self.assertTrue(dag.reachable(n1, n3))
        self.assertTrue(dag.ready_at(cut, n3))

    def test_graph_support_certifier_accepts_hasse_frontier_cut(self):
        dag, n0, n1, n2, n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        cut = dag.support_cut_of_finite_hasse_frontier(past)
        motif = MotifCandidate(
            "M",
            frozenset({n3}),
            cut,
            kind="renewal",
            metadata={"candidate_past": sorted(past)},
        )
        certifier = GraphSupportCertifier(dag)
        evaluation = certifier.evaluate(motif, cut)
        self.assertTrue(evaluation.supported)
        self.assertEqual(evaluation.failed_gates, ())

    def test_graph_support_certifier_rejects_non_hasse_cut(self):
        dag, n0, n1, n2, n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        wrong_cut = frozenset({n0, n1})
        motif = MotifCandidate(
            "BadCut",
            frozenset({n3}),
            wrong_cut,
            kind="renewal",
            metadata={"candidate_past": sorted(past)},
        )
        certifier = GraphSupportCertifier(dag)
        evaluation = certifier.evaluate(motif, wrong_cut)
        self.assertFalse(evaluation.supported)
        self.assertIn("support_cut_is_hasse_frontier", evaluation.failed_gates)

    def test_graph_support_certifier_rejects_ledger_gate_failure(self):
        dag, n0, n1, n2, n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        cut = dag.support_cut_of_finite_hasse_frontier(past)
        motif = MotifCandidate(
            "LedgerBad",
            frozenset({n3}),
            cut,
            kind="renewal",
            metadata={"candidate_past": sorted(past), "ledger_local_ok": False},
        )
        certifier = GraphSupportCertifier(dag)
        evaluation = certifier.evaluate(motif, cut)
        self.assertFalse(evaluation.supported)
        self.assertIn("ledger_local_gate", evaluation.failed_gates)

    def test_incompatible_ready_motifs_block_each_other_when_both_certified(self):
        dag, n0, n1, n2, n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        cut = dag.support_cut_of_finite_hasse_frontier(past)
        a = MotifCandidate("A", frozenset({n3}), cut, exclusion_domain="choice", metadata={"candidate_past": sorted(past)})
        b = MotifCandidate("B", frozenset({n3}), cut, exclusion_domain="choice", metadata={"candidate_past": sorted(past)})
        protocol = MotifCommitProtocol(dag, [a, b], make_context(dag))
        da = protocol.decision(a, n3)
        db = protocol.decision(b, n3)
        self.assertTrue(da.supported)
        self.assertTrue(db.supported)
        self.assertTrue(da.ready)
        self.assertTrue(db.ready)
        self.assertFalse(da.commits)
        self.assertFalse(db.commits)
        self.assertEqual(da.blocked_by, ("B",))
        self.assertEqual(db.blocked_by, ("A",))

    def test_uncertified_competitor_does_not_block_certified_motif(self):
        dag, n0, n1, n2, n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        cut = dag.support_cut_of_finite_hasse_frontier(past)
        good = MotifCandidate("Good", frozenset({n3}), cut, exclusion_domain="choice", metadata={"candidate_past": sorted(past)})
        bad = MotifCandidate(
            "Bad",
            frozenset({n3}),
            cut,
            exclusion_domain="choice",
            metadata={"candidate_past": sorted(past), "orientation_closure_ok": False},
        )
        protocol = MotifCommitProtocol(dag, [good, bad], make_context(dag))
        dg = protocol.decision(good, n3)
        db = protocol.decision(bad, n3)
        self.assertTrue(dg.supported)
        self.assertFalse(db.supported)
        self.assertTrue(dg.commits)
        self.assertFalse(db.commits)
        self.assertEqual(dg.blocked_by, ())

    def test_unique_ready_motif_commits_with_certifier(self):
        dag, n0, n1, n2, n3 = self.diamond()
        past = frozenset({n0, n1, n2})
        cut = dag.support_cut_of_finite_hasse_frontier(past)
        m = MotifCandidate("M", frozenset({n3}), cut, metadata={"candidate_past": sorted(past)})
        protocol = MotifCommitProtocol(dag, [m], make_context(dag))
        decision = protocol.decision(m, n3)
        self.assertTrue(decision.supported)
        self.assertTrue(decision.ready)
        self.assertTrue(decision.commits)

    def test_depth_finality(self):
        dag, n0, n1, n2, n3 = self.diamond()
        self.assertTrue(dag.finalized_at_depth(frozenset({n0}), 1))
        self.assertTrue(dag.finalized_at_depth(frozenset({n1, n2}), dag.depth[n3]))

    def test_demo_and_sweep_run(self):
        dag, motifs, rows, support_rows = generate_growth_demo(steps=8, seed=5, defect_rate=0.2)
        self.assertEqual(len(dag.nodes), 9)
        self.assertTrue(motifs)
        self.assertEqual(len(rows), 8)
        self.assertTrue(support_rows)
        sweep = run_parameter_sweep(seeds=(1,), conflict_rates=(0.0, 0.3), defect_rates=(0.0,), steps=6)
        self.assertEqual(len(sweep), 2)

    def test_default_context_remains_available(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        m = MotifCandidate("M", frozenset({n3}), cut)
        protocol = MotifCommitProtocol(dag, [m], CommitContext())
        self.assertTrue(protocol.decision(m, n3).commits)


if __name__ == "__main__":
    unittest.main()
