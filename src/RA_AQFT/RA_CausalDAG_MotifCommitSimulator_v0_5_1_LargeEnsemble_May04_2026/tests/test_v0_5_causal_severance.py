import unittest

from simulator.ra_causal_dag_simulator import (
    CausalDAG,
    CausalSeveranceIntervention,
    GraphOrientationSupportCertifier,
    MotifCandidate,
    choose_prefix_fraction,
    degraded_ledger_metadata,
    degraded_orientation_metadata,
    evaluate_severance,
    generate_growth_demo,
    min_finality_depth,
    readiness_recovery_length,
    remove_edges,
    run_severance_workbench,
)


def orientation_metadata(past, q, site, *, qN1=7, ledger_ok=True):
    return {
        "candidate_past": sorted(past),
        "parents": sorted(q),
        "past_size": len(past),
        "bdg_local_ok": True,
        "ledger_local_ok": ledger_ok,
        "orientation_support_witness": {
            "candidate_past": sorted(past),
            "support_cut": sorted(q),
            "frontier_sufficient_for_motif": True,
            "local_ledger_compatible": ledger_ok,
            "carrier_represented_by_frontier": True,
            "closure": {
                "selector_compatible": True,
                "no_extra_random_labels": True,
                "no_particle_label_primitives": True,
                "qN1_signature": qN1,
                "local_conserved": True,
                "sign_links": [[y, site, 1] for y in sorted(q)],
            },
        },
    }


def simple_supported_motif():
    dag = CausalDAG()
    g = dag.add_node()
    x = dag.add_node([g])
    later = dag.add_node([x])
    past = dag.candidate_past_from_support([g])
    q = dag.support_cut_of_finite_hasse_frontier(past)
    motif = MotifCandidate("m", frozenset({x}), q, "renewal", priority=2, metadata=orientation_metadata(past, q, x))
    return dag, g, x, later, past, q, motif


class CausalSeveranceV05Tests(unittest.TestCase):
    def test_remove_edges_breaks_direct_support_readiness(self):
        dag, g, x, _later, _past, q, _motif = simple_supported_motif()
        severed = remove_edges(dag, [(g, x)])
        self.assertTrue(dag.ready_at(q, x))
        self.assertFalse(severed.ready_at(q, x))

    def test_readiness_recovery_length_reports_delay(self):
        dag, _g, x, later, _past, q, _motif = simple_supported_motif()
        rec = readiness_recovery_length(dag, q, x, delay_depth=1)
        self.assertEqual(rec, 1)  # later is one depth beyond x and satisfies the delayed support condition

    def test_degraded_orientation_metadata_loses_support_certification(self):
        dag, _g, x, _later, _past, q, motif = simple_supported_motif()
        degraded = MotifCandidate("m_bad", motif.carrier, q, "renewal", metadata=degraded_orientation_metadata(motif.metadata, 1.0))
        ev = GraphOrientationSupportCertifier(dag).evaluate(degraded, q)
        self.assertFalse(ev.supported)
        self.assertIn("orientation_qN1_seven", ev.failed_gates)

    def test_degraded_ledger_metadata_loses_support_certification(self):
        dag, _g, x, _later, _past, q, motif = simple_supported_motif()
        degraded = MotifCandidate("m_bad", motif.carrier, q, "renewal", metadata=degraded_ledger_metadata(motif.metadata, 1.0))
        ev = GraphOrientationSupportCertifier(dag).evaluate(degraded, q)
        self.assertFalse(ev.supported)
        self.assertIn("ledger_local_gate", ev.failed_gates)
        self.assertIn("orientation_local_ledger_compatible", ev.failed_gates)

    def test_evaluate_frontier_dropout_records_support_loss(self):
        dag, _g, x, _later, _past, _q, motif = simple_supported_motif()
        ev = evaluate_severance(dag, [motif], motif, x, CausalSeveranceIntervention("frontier_dropout", 1.0, seed=1))
        self.assertTrue(ev.lost_support)
        self.assertTrue(ev.lost_selected_commit)
        self.assertIn("dropped_support_vertices", ev.intervention_detail)

    def test_support_delay_records_readiness_loss_and_recovery(self):
        dag, _g, x, _later, _past, _q, motif = simple_supported_motif()
        ev = evaluate_severance(dag, [motif], motif, x, CausalSeveranceIntervention("support_delay", 0.2, seed=1))
        self.assertTrue(ev.lost_readiness)
        self.assertIsNotNone(ev.recovery_length)

    def test_min_finality_depth_available_for_unsevered_cut(self):
        dag, _g, _x, _later, _past, q, _motif = simple_supported_motif()
        self.assertIsNotNone(min_finality_depth(dag, q))

    def test_workbench_generates_fragility_profiles(self):
        dag, motifs, severance_rows, fragility_rows, finality_rows, recovery_rows = run_severance_workbench(steps=6, seed=9, orientation_defect_rate=0.0, defect_rate=0.0, max_targets=3)
        self.assertTrue(severance_rows)
        self.assertTrue(fragility_rows)
        self.assertTrue(finality_rows)
        self.assertIn("lost_selected_commit_rate", fragility_rows[0])
        self.assertIsInstance(recovery_rows, list)

    def test_choose_prefix_fraction_zero_is_empty(self):
        chosen = choose_prefix_fraction([1, 2, 3], 0.0, __import__("random").Random(1))
        self.assertEqual(chosen, ())


if __name__ == "__main__":
    unittest.main()
