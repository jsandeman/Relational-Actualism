import unittest
from simulator.ra_causal_dag_channel_workbench import (
    ChannelIntervention,
    ChannelSeparatedRunConfig,
    build_channel_seed_state,
    evaluate_channel_severance,
    generate_support_diverse_growth_state,
    mode_separability,
    run_channel_ensemble,
    summarize_channel_aggregate,
    summarize_mode_signatures,
    target_motifs_for_channel_severance,
)
from simulator.ra_causal_dag_simulator import motif_site


class ChannelSeparationV06Tests(unittest.TestCase):
    def test_support_diverse_generator_produces_width_above_one(self):
        dag, motifs = generate_support_diverse_growth_state(steps=28, seed=19, target_frontier_min=6, branch_probability=0.55, wide_join_probability=0.90)
        widths = {len(m.support_cut) for m in motifs if m.kind == "renewal" and m.support_cut}
        self.assertGreaterEqual(max(widths), 2)
        self.assertGreaterEqual(len(widths), 2)

    def test_frontier_dropout_is_availability_not_certification_loss(self):
        cfg = ChannelSeparatedRunConfig(seeds=(17,), steps=20, max_targets=8)
        state = build_channel_seed_state(cfg, 17)
        motif = target_motifs_for_channel_severance(state.motifs, max_targets=8)[0]
        ev = evaluate_channel_severance(state, motif, motif_site(motif), ChannelIntervention("frontier_dropout", 1.0, seed=101))
        self.assertTrue(ev.lost_support_availability)
        self.assertFalse(ev.lost_support_certification)
        self.assertTrue(ev.lost_operational_readiness)

    def test_ledger_failure_is_certification_not_causal_reachability_loss(self):
        cfg = ChannelSeparatedRunConfig(seeds=(17,), steps=20, max_targets=8)
        state = build_channel_seed_state(cfg, 17)
        motif = target_motifs_for_channel_severance(state.motifs, max_targets=8)[0]
        ev = evaluate_channel_severance(state, motif, motif_site(motif), ChannelIntervention("ledger_failure", 1.0, seed=101))
        self.assertTrue(ev.ledger_gate_loss)
        self.assertTrue(ev.lost_support_certification)
        self.assertFalse(ev.lost_causal_reachability)

    def test_orientation_degradation_is_graded_across_ensemble(self):
        cfg_low = ChannelSeparatedRunConfig(seeds=tuple(range(17, 21)), steps=16, max_targets=6, severities=(0.25,), modes=("orientation_degradation",), sample_limit=0)
        cfg_high = ChannelSeparatedRunConfig(seeds=tuple(range(17, 21)), steps=16, max_targets=6, severities=(1.0,), modes=("orientation_degradation",), sample_limit=0)
        low_summary, _, low_agg, *_ = run_channel_ensemble(cfg_low)
        high_summary, _, high_agg, *_ = run_channel_ensemble(cfg_high)
        self.assertGreater(low_summary["actual_evaluations"], 0)
        low_rate = float(low_agg[0]["orientation_gate_loss_rate"])
        high_rate = float(high_agg[0]["orientation_gate_loss_rate"])
        self.assertLess(low_rate, high_rate)
        self.assertGreater(high_rate, 0.9)

    def test_mode_signatures_are_no_longer_degenerate_for_frontier_ledger_orientation(self):
        cfg = ChannelSeparatedRunConfig(seeds=tuple(range(17, 21)), steps=16, max_targets=6, severities=(0.5, 1.0), sample_limit=0)
        _, _, aggregate, _, signatures, separability, _ = run_channel_ensemble(cfg)
        sig = {r["mode"]: r["classification"] for r in signatures}
        self.assertEqual(sig["frontier_dropout"], "frontier_availability_channel")
        self.assertEqual(sig["ledger_failure"], "ledger_certification_channel")
        self.assertEqual(sig["orientation_degradation"], "orientation_witness_certification_channel")
        pair = [r for r in separability if {r["mode_a"], r["mode_b"]} == {"frontier_dropout", "ledger_failure"}][0]
        self.assertGreater(float(pair["euclidean_distance"]), 0.0)
        pair2 = [r for r in separability if {r["mode_a"], r["mode_b"]} == {"ledger_failure", "orientation_degradation"}][0]
        self.assertGreater(float(pair2["euclidean_distance"]), 0.0)

    def test_summary_contains_support_width_diversity(self):
        cfg = ChannelSeparatedRunConfig(seeds=tuple(range(17, 19)), steps=16, max_targets=6, sample_limit=50)
        summary, run_rows, aggregate, width_rows, signatures, separability, sample_rows = run_channel_ensemble(cfg)
        self.assertGreater(summary["support_width_count"], 1)
        self.assertGreater(len(width_rows), 0)
        self.assertGreater(len(signatures), 0)
        self.assertGreater(len(separability), 0)
        self.assertLessEqual(len(sample_rows), 50)


if __name__ == "__main__":
    unittest.main()
