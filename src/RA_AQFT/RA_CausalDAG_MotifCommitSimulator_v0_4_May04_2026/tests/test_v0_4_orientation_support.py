import unittest

from simulator.ra_causal_dag_simulator import (
    CausalDAG,
    GraphOrientationSupportCertifier,
    MotifCandidate,
    MotifCommitProtocol,
    OrientationActualizationContext,
    SelectorPolicy,
    make_context,
    generate_growth_demo,
)


def basic_dag_and_support():
    dag = CausalDAG()
    g = dag.add_node()
    x = dag.add_node([g])
    past = dag.candidate_past_from_support([g])
    q = dag.support_cut_of_finite_hasse_frontier(past)
    return dag, g, x, past, q


def orientation_metadata(past, q, site, *, qN1=7, sign_links=None, frontier_ok=True, ledger_ok=True):
    if sign_links is None:
        sign_links = [[y, site, 1] for y in sorted(q)]
    return {
        "candidate_past": sorted(past),
        "parents": sorted(q),
        "past_size": len(past),
        "bdg_local_ok": True,
        "ledger_local_ok": True,
        "orientation_support_witness": {
            "candidate_past": sorted(past),
            "support_cut": sorted(q),
            "frontier_sufficient_for_motif": frontier_ok,
            "local_ledger_compatible": ledger_ok,
            "carrier_represented_by_frontier": True,
            "closure": {
                "selector_compatible": True,
                "no_extra_random_labels": True,
                "no_particle_label_primitives": True,
                "qN1_signature": qN1,
                "local_conserved": True,
                "sign_links": sign_links,
            },
        },
    }


class OrientationSupportV04Tests(unittest.TestCase):
    def test_orientation_witness_required_blocks_missing_witness(self):
        dag, _g, x, past, q = basic_dag_and_support()
        motif = MotifCandidate("m", frozenset({x}), q, "renewal", metadata={"candidate_past": sorted(past), "bdg_local_ok": True, "ledger_local_ok": True})
        certifier = GraphOrientationSupportCertifier(dag)
        ev = certifier.evaluate(motif, q)
        self.assertFalse(ev.supported)
        self.assertIn("orientation_witness_declared", ev.failed_gates)

    def test_orientation_witness_allows_certified_support(self):
        dag, _g, x, past, q = basic_dag_and_support()
        motif = MotifCandidate("m", frozenset({x}), q, "renewal", metadata=orientation_metadata(past, q, x))
        certifier = GraphOrientationSupportCertifier(dag)
        ev = certifier.evaluate(motif, q)
        self.assertTrue(ev.supported, ev.failed_gates)
        self.assertIn("orientation_qN1_seven", ev.passed_gates)

    def test_non_seven_qN1_blocks_support(self):
        dag, _g, x, past, q = basic_dag_and_support()
        motif = MotifCandidate("m", frozenset({x}), q, "renewal", metadata=orientation_metadata(past, q, x, qN1=5))
        ev = GraphOrientationSupportCertifier(dag).evaluate(motif, q)
        self.assertFalse(ev.supported)
        self.assertIn("orientation_qN1_seven", ev.failed_gates)

    def test_missing_sign_source_blocks_support(self):
        dag, _g, x, past, q = basic_dag_and_support()
        motif = MotifCandidate("m", frozenset({x}), q, "renewal", metadata=orientation_metadata(past, q, x, sign_links=[]))
        ev = GraphOrientationSupportCertifier(dag).evaluate(motif, q)
        self.assertFalse(ev.supported)
        self.assertIn("orientation_sign_source_covers_support", ev.failed_gates)

    def test_orientation_conflict_witness_blocks_strict_commit(self):
        dag, _g, x, past, q = basic_dag_and_support()
        meta_a = orientation_metadata(past, q, x); meta_a["orientation_conflict_domain"] = "d"
        meta_b = orientation_metadata(past, q, x); meta_b["orientation_conflict_domain"] = "d"
        a = MotifCandidate("a", frozenset({x}), q, "alternative", exclusion_domain="d", metadata=meta_a)
        b = MotifCandidate("b", frozenset({x}), q, "alternative", exclusion_domain="d", metadata=meta_b)
        ctx = OrientationActualizationContext(GraphOrientationSupportCertifier(dag))
        protocol = MotifCommitProtocol(dag, [a, b], ctx)
        da = protocol.decision(a, x)
        self.assertFalse(da.commits)
        self.assertEqual(da.blocked_by, ("b",))
        self.assertIsNotNone(ctx.conflict_witness(a, b))

    def test_unsupported_incompatible_competitor_does_not_block(self):
        dag, _g, x, past, q = basic_dag_and_support()
        meta_a = orientation_metadata(past, q, x); meta_a["orientation_conflict_domain"] = "d"
        meta_b = orientation_metadata(past, q, x, qN1=5); meta_b["orientation_conflict_domain"] = "d"
        a = MotifCandidate("a", frozenset({x}), q, "alternative", exclusion_domain="d", metadata=meta_a)
        b = MotifCandidate("b", frozenset({x}), q, "alternative", exclusion_domain="d", metadata=meta_b)
        protocol = MotifCommitProtocol(dag, [a, b], make_context(dag))
        self.assertTrue(protocol.decision(a, x).commits)
        self.assertFalse(protocol.decision(b, x).supported)

    def test_selector_stalemate_records_unresolved_equal_rank_conflict(self):
        dag, _g, x, past, q = basic_dag_and_support()
        meta_a = orientation_metadata(past, q, x); meta_a["orientation_conflict_domain"] = "d"
        meta_b = orientation_metadata(past, q, x); meta_b["orientation_conflict_domain"] = "d"
        a = MotifCandidate("a", frozenset({x}), q, "alternative", exclusion_domain="d", priority=1, metadata=meta_a)
        b = MotifCandidate("b", frozenset({x}), q, "alternative", exclusion_domain="d", priority=1, metadata=meta_b)
        protocol = MotifCommitProtocol(dag, [a, b], make_context(dag))
        closure = protocol.selector_closure_at(x, SelectorPolicy("greedy", "stalemate"))
        self.assertEqual(set(closure.stalemates), {"a", "b"})

    def test_demo_runs_and_reports_orientation_failures(self):
        dag, motifs, rows, support_rows, selector_rows, orientation_rows, conflict_rows = generate_growth_demo(steps=8, seed=5, orientation_defect_rate=0.2)
        self.assertGreaterEqual(len(dag.nodes), 9)
        self.assertTrue(rows)
        self.assertTrue(support_rows)
        self.assertTrue(orientation_rows)
        self.assertIsInstance(conflict_rows, list)


if __name__ == "__main__":
    unittest.main()
