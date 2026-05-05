import unittest

from simulator.ra_causal_dag_simulator import (
    CausalSeveranceIntervention,
    evaluate_severance,
    generate_growth_demo,
    min_finality_depth,
    readiness_recovery_length,
    run_severance_workbench,
    summarize_fragility,
    summarize_severance_sweep,
    target_motifs_for_severance,
)


class TestCausalSeveranceWorkbenchV05(unittest.TestCase):
    def setUp(self):
        self.dag, self.motifs, self.rows, *_ = generate_growth_demo(
            steps=10,
            seed=23,
            defect_rate=0.0,
            orientation_defect_rate=0.0,
            conflict_witness_defect_rate=0.0,
            conflict_rate=0.0,
        )
        targets = target_motifs_for_severance(self.motifs, max_targets=5)
        self.assertTrue(targets)
        self.target = targets[0]
        self.site = max(self.target.carrier)

    def test_zero_severity_edge_dropout_preserves_target_decision(self):
        intervention = CausalSeveranceIntervention("edge_dropout", 0.0, seed=1)
        ev = evaluate_severance(self.dag, self.motifs, self.target, self.site, intervention)
        self.assertEqual(ev.before_supported, ev.after_supported)
        self.assertEqual(ev.before_ready, ev.after_ready)
        self.assertEqual(ev.before_strict_commits, ev.after_strict_commits)

    def test_frontier_dropout_can_destroy_support_or_readiness(self):
        intervention = CausalSeveranceIntervention("frontier_dropout", 1.0, seed=2)
        ev = evaluate_severance(self.dag, self.motifs, self.target, self.site, intervention)
        self.assertTrue(ev.lost_support or ev.lost_readiness or not ev.after_ready)
        self.assertIn("dropped_support_vertices", ev.intervention_detail)

    def test_support_delay_records_recovery_length_or_loss(self):
        intervention = CausalSeveranceIntervention("support_delay", 0.6, seed=3)
        ev = evaluate_severance(self.dag, self.motifs, self.target, self.site, intervention)
        self.assertFalse(ev.after_ready)
        self.assertIn("delay_depth", ev.intervention_detail)
        self.assertTrue(ev.recovery_length is None or ev.recovery_length >= 0)

    def test_orientation_degradation_can_remove_support_certification(self):
        intervention = CausalSeveranceIntervention("orientation_degradation", 1.0, seed=4)
        ev = evaluate_severance(self.dag, self.motifs, self.target, self.site, intervention)
        self.assertFalse(ev.after_supported)
        self.assertTrue(ev.lost_support or not ev.before_supported)

    def test_workbench_outputs_expected_tables(self):
        dag, motifs, rows, fragility_rows, finality_rows, recovery_rows = run_severance_workbench(
            steps=8,
            seed=29,
            defect_rate=0.0,
            orientation_defect_rate=0.0,
            max_targets=4,
        )
        self.assertGreater(len(dag.nodes), 1)
        self.assertGreater(len(motifs), 1)
        self.assertGreater(len(rows), 0)
        self.assertGreater(len(fragility_rows), 0)
        self.assertIsInstance(summarize_severance_sweep(rows), list)
        self.assertIsInstance(finality_rows, list)
        self.assertIsInstance(recovery_rows, list)

    def test_fragility_summary_groups_by_mode_severity_width(self):
        rows = [
            {"mode": "frontier_dropout", "severity": 1.0, "support_width": 1, "lost_support": True, "lost_readiness": True, "lost_strict_commit": True, "lost_selected_commit": True},
            {"mode": "frontier_dropout", "severity": 1.0, "support_width": 1, "lost_support": False, "lost_readiness": False, "lost_strict_commit": False, "lost_selected_commit": False},
        ]
        summary = summarize_fragility(rows)
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["samples"], 2)
        self.assertEqual(summary[0]["lost_strict_commit_rate"], 0.5)

    def test_finality_and_recovery_helpers_return_optional_depths(self):
        finality = min_finality_depth(self.dag, self.target.support_cut)
        recovery = readiness_recovery_length(self.dag, self.target.support_cut, self.site)
        self.assertTrue(finality is None or isinstance(finality, int))
        self.assertTrue(recovery is None or isinstance(recovery, int))


if __name__ == "__main__":
    unittest.main()
