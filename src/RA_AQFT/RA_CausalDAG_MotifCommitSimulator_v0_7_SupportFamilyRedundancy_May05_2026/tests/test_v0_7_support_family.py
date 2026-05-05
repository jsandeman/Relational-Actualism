import unittest
from pathlib import Path
import tempfile

import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulator.ra_causal_dag_simulator import CausalDAG, MotifCandidate, remove_edges
from simulator.ra_causal_dag_channel_workbench import ChannelSeparatedRunConfig, build_channel_seed_state, target_motifs_for_channel_severance
from simulator.ra_causal_dag_support_family_workbench import (
    SupportFamilyRunConfig,
    evaluate_support_family,
    family_ready_at,
    run_support_family_ensemble,
    strict_ready_at,
    threshold_k,
    threshold_support_family,
    write_state,
    write_support_family_predictions,
)
from simulator.ra_causal_dag_simulator import rows_to_csv


class SupportFamilyV07Tests(unittest.TestCase):
    def test_threshold_k_bounds(self):
        self.assertEqual(threshold_k(4, 1.0), 4)
        self.assertEqual(threshold_k(4, 0.75), 3)
        self.assertEqual(threshold_k(4, 0.50), 2)
        self.assertEqual(threshold_k(4, 0.25), 1)
        self.assertEqual(threshold_k(0, 0.25), 0)

    def test_threshold_one_recovers_strict_single_cut(self):
        dag = CausalDAG()
        a = dag.add_node()
        b = dag.add_node()
        x = dag.add_node({a, b})
        motif = MotifCandidate("m", frozenset({x}), frozenset({a, b}), "renewal")
        family = threshold_support_family(motif, 1.0)
        self.assertEqual(family.family_size, 1)
        self.assertTrue(strict_ready_at(dag, motif.support_cut, x))
        self.assertEqual(strict_ready_at(dag, motif.support_cut, x), family_ready_at(dag, family, x))

    def test_threshold_family_can_rescue_strict_reachability_loss(self):
        dag = CausalDAG()
        a = dag.add_node()
        b = dag.add_node()
        x = dag.add_node({a, b})
        motif = MotifCandidate("m", frozenset({x}), frozenset({a, b}), "renewal")
        after = remove_edges(dag, ((a, x),))
        strict = strict_ready_at(after, motif.support_cut, x)
        family = threshold_support_family(motif, 0.5)  # singleton cuts {a}, {b}
        fam = family_ready_at(after, family, x)
        self.assertFalse(strict)
        self.assertTrue(fam)

    def test_support_diverse_state_has_width_above_one(self):
        config = ChannelSeparatedRunConfig(seeds=(17,), steps=12, max_targets=6)
        state = build_channel_seed_state(config, 17)
        widths = {len(m.support_cut) for m in target_motifs_for_channel_severance(state.motifs, max_targets=8)}
        self.assertTrue(any(w > 1 for w in widths))

    def test_family_evaluation_records_rescue(self):
        config = ChannelSeparatedRunConfig(seeds=(17,), steps=12, max_targets=8)
        state = build_channel_seed_state(config, 17)
        motif = next(m for m in target_motifs_for_channel_severance(state.motifs, max_targets=8) if len(m.support_cut) > 1)
        ev = evaluate_support_family(state, motif, next(iter(motif.carrier)), threshold_fraction=0.25, mode="frontier_dropout", severity=0.25, seed=101)
        self.assertIn(ev.mode, {"frontier_dropout"})
        self.assertGreaterEqual(ev.support_width, 2)
        self.assertGreaterEqual(ev.family_size, 1)

    def test_selector_stress_is_not_counted_as_support_family_rescue(self):
        config = ChannelSeparatedRunConfig(seeds=(17,), steps=12, max_targets=8)
        state = build_channel_seed_state(config, 17)
        motif = next(m for m in target_motifs_for_channel_severance(state.motifs, max_targets=8) if len(m.support_cut) > 1)
        ev = evaluate_support_family(state, motif, next(iter(motif.carrier)), threshold_fraction=0.25, mode="selector_stress", severity=0.5, seed=101)
        self.assertTrue(ev.family_after_ready)
        self.assertFalse(ev.family_rescues_strict_loss)

    def test_end_to_end_outputs(self):
        config = SupportFamilyRunConfig(seeds=(17, 18), steps=8, max_targets=4, sample_limit=100)
        summary, run_rows, aggregate, width_rows, curve_rows, signatures = run_support_family_ensemble(config)
        self.assertGreater(summary["actual_evaluations"], 0)
        self.assertGreaterEqual(summary["support_width_count"], 1)
        self.assertTrue(aggregate)
        self.assertTrue(width_rows)
        self.assertTrue(curve_rows)
        self.assertTrue(signatures)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            rows_to_csv([summary], out / "summary.csv")
            rows_to_csv(aggregate, out / "aggregate.csv")
            write_support_family_predictions(summary, aggregate, signatures, out / "predictions.md")
            write_state(summary, run_rows, aggregate, width_rows, curve_rows, signatures, out / "state.json")
            self.assertTrue((out / "summary.csv").exists())
            self.assertTrue((out / "aggregate.csv").exists())
            self.assertTrue((out / "predictions.md").exists())
            self.assertTrue((out / "state.json").exists())


if __name__ == "__main__":
    unittest.main()
