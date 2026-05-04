import unittest

from simulator.ra_causal_dag_simulator import (
    CausalDAG,
    CommitContext,
    GraphSupportCertifier,
    MotifCandidate,
    MotifCommitProtocol,
    SelectorPolicy,
    make_context,
)


def metadata(dag, support):
    past = dag.candidate_past_from_support(support)
    return {
        "candidate_past": sorted(past),
        "bdg_local_ok": True,
        "ledger_local_ok": True,
        "orientation_closure_ok": True,
    }


class TestRACausalDAGSimulatorV03(unittest.TestCase):
    def diamond(self):
        dag = CausalDAG()
        n0 = dag.add_node()
        n1 = dag.add_node([n0])
        n2 = dag.add_node([n0])
        n3 = dag.add_node([n1, n2])
        return dag, n0, n1, n2, n3

    def motif(self, dag, name, carrier, cut, domain=None, priority=0, **meta_overrides):
        md = metadata(dag, cut)
        md.update(meta_overrides)
        return MotifCandidate(
            name=name,
            carrier=frozenset({carrier}),
            support_cut=frozenset(cut),
            kind="alternative" if domain else "renewal",
            exclusion_domain=domain,
            priority=priority,
            metadata=md,
        )

    def protocol(self, dag, motifs):
        return MotifCommitProtocol(dag, motifs, make_context(dag))

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

    def test_strict_incompatible_ready_motifs_block_each_other(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = self.motif(dag, "A", n3, cut, domain="choice", priority=1)
        b = self.motif(dag, "B", n3, cut, domain="choice", priority=1)
        protocol = self.protocol(dag, [a, b])
        da = protocol.decision(a, n3)
        db = protocol.decision(b, n3)
        self.assertTrue(da.supported)
        self.assertTrue(da.ready)
        self.assertFalse(da.commits)
        self.assertEqual(da.blocked_by, ("B",))
        self.assertFalse(db.commits)
        self.assertEqual(db.blocked_by, ("A",))

    def test_selector_none_reproduces_strict_blocking(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = self.motif(dag, "A", n3, cut, domain="choice", priority=1)
        b = self.motif(dag, "B", n3, cut, domain="choice", priority=1)
        protocol = self.protocol(dag, [a, b])
        closure = protocol.selector_closure_at(n3, SelectorPolicy(mode="none"))
        self.assertEqual(closure.selected, ("A", "B"))
        self.assertFalse(protocol.selected_decision(a, n3, closure=closure).commits)
        self.assertFalse(protocol.selected_decision(b, n3, closure=closure).commits)

    def test_greedy_selector_resolves_conflict_by_priority(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = self.motif(dag, "A", n3, cut, domain="choice", priority=2)
        b = self.motif(dag, "B", n3, cut, domain="choice", priority=1)
        protocol = self.protocol(dag, [a, b])
        closure = protocol.selector_closure_at(n3, SelectorPolicy(mode="greedy", tie_policy="lexicographic"))
        self.assertEqual(closure.selected, ("A",))
        self.assertEqual(closure.rejected, ("B",))
        self.assertTrue(protocol.selected_decision(a, n3, closure=closure).commits)
        self.assertFalse(protocol.selected_decision(b, n3, closure=closure).commits)
        self.assertEqual(protocol.selected_decision(b, n3, closure=closure).selector_reason, "rejected_by_selector")

    def test_stalemate_policy_refuses_name_tiebreak(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = self.motif(dag, "A", n3, cut, domain="choice", priority=1)
        b = self.motif(dag, "B", n3, cut, domain="choice", priority=1)
        protocol = self.protocol(dag, [a, b])
        closure = protocol.selector_closure_at(n3, SelectorPolicy(mode="greedy", tie_policy="stalemate"))
        self.assertEqual(closure.selected, ())
        self.assertEqual(closure.stalemates, ("A", "B"))
        self.assertEqual(protocol.selected_decision(a, n3, closure=closure).selector_reason, "selector_stalemate")
        self.assertFalse(protocol.selected_decision(a, n3, closure=closure).commits)

    def test_lexicographic_policy_breaks_equal_priority_tie(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = self.motif(dag, "A", n3, cut, domain="choice", priority=1)
        b = self.motif(dag, "B", n3, cut, domain="choice", priority=1)
        protocol = self.protocol(dag, [a, b])
        closure = protocol.selector_closure_at(n3, SelectorPolicy(mode="greedy", tie_policy="lexicographic"))
        # The total order uses ascending name after priority/support/kind, so A wins.
        self.assertEqual(closure.selected, ("A",))
        self.assertTrue(protocol.selected_decision(a, n3, closure=closure).commits)
        self.assertFalse(protocol.selected_decision(b, n3, closure=closure).commits)

    def test_unsupported_competitor_does_not_block_supported_motif(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = self.motif(dag, "A", n3, cut, domain="choice", priority=1)
        b = self.motif(dag, "B", n3, cut, domain="choice", priority=1, ledger_local_ok=False)
        protocol = self.protocol(dag, [a, b])
        da = protocol.decision(a, n3)
        db = protocol.decision(b, n3)
        self.assertTrue(da.supported)
        self.assertTrue(da.commits)
        self.assertFalse(db.supported)
        self.assertIn("ledger_local_gate", db.support_failures)

    def test_support_certifier_rejects_wrong_hasse_cut(self):
        dag, n0, n1, n2, n3 = self.diamond()
        past = dag.candidate_past_from_support({n1, n2})
        wrong_cut = frozenset({n0})
        m = MotifCandidate(
            name="M",
            carrier=frozenset({n3}),
            support_cut=wrong_cut,
            metadata={"candidate_past": sorted(past)},
        )
        report = GraphSupportCertifier(dag).evaluate(m, wrong_cut)
        self.assertFalse(report.supported)
        self.assertIn("support_cut_is_hasse_frontier", report.failed_gates)

    def test_selector_component_records_suppression(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        a = self.motif(dag, "A", n3, cut, domain="choice", priority=3)
        b = self.motif(dag, "B", n3, cut, domain="choice", priority=1)
        protocol = self.protocol(dag, [a, b])
        closure = protocol.selector_closure_at(n3, SelectorPolicy(mode="greedy"))
        self.assertEqual(closure.selected, ("A",))
        self.assertEqual(closure.rejected, ("B",))
        self.assertEqual(closure.components[0].reason, "greedy_compatible_subset_selected")

    def test_depth_finality(self):
        dag, n0, n1, n2, n3 = self.diamond()
        self.assertTrue(dag.finalized_at_depth(frozenset({n0}), 1))
        self.assertTrue(dag.finalized_at_depth(frozenset({n1, n2}), dag.depth[n3]))

    def test_default_exact_support_still_available(self):
        dag, _n0, n1, n2, n3 = self.diamond()
        cut = frozenset({n1, n2})
        m = MotifCandidate("M", frozenset({n3}), cut)
        protocol = MotifCommitProtocol(dag, [m], CommitContext())
        decision = protocol.decision(m, n3)
        self.assertTrue(decision.supported)
        self.assertTrue(decision.ready)
        self.assertTrue(decision.commits)


if __name__ == "__main__":
    unittest.main()
