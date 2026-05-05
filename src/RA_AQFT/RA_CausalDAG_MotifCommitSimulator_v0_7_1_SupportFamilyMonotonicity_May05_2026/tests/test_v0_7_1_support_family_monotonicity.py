import unittest
from pathlib import Path
import tempfile
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulator.ra_causal_dag_simulator import CausalDAG, MotifCandidate, rows_to_csv
from simulator.ra_causal_dag_channel_workbench import ChannelSeparatedRunConfig, build_channel_seed_state, target_motifs_for_channel_severance
from simulator.ra_causal_dag_support_family_monotonicity import (
    SupportFamilyMonotonicityConfig,
    aggregate_monotonicity_rows,
    evaluate_support_family_monotonicity,
    family_includes_strict_cut,
    no_worse_audit_rows,
    run_support_family_monotonicity,
    support_family_by_semantics,
    write_predictions,
    write_state,
)


class SupportFamilyMonotonicityV071Tests(unittest.TestCase):
    def test_semantics_include_strict_cut_exactly_when_expected(self):
        dag = CausalDAG()
        a = dag.add_node()
        b = dag.add_node()
        c = dag.add_node()
        x = dag.add_node({a, b, c})
        motif = MotifCandidate("m", frozenset({x}), frozenset({a, b, c}), "renewal")
        exact = support_family_by_semantics(motif, 0.34, "exact_k")
        atleast = support_family_by_semantics(motif, 0.34, "at_least_k")
        augmented = support_family_by_semantics(motif, 0.34, "augmented_exact_k")
        self.assertFalse(family_includes_strict_cut(exact))
        self.assertTrue(family_includes_strict_cut(atleast))
        self.assertTrue(family_includes_strict_cut(augmented))

    def test_at_least_k_no_worse_when_strict_survives(self):
        config = ChannelSeparatedRunConfig(seeds=(17,), steps=12, max_targets=8)
        state = build_channel_seed_state(config, 17)
        motif = next(m for m in target_motifs_for_channel_severance(state.motifs, max_targets=8) if len(m.support_cut) > 1)
        ev = evaluate_support_family_monotonicity(
            state,
            motif,
            next(iter(motif.carrier)),
            threshold_fraction=0.25,
            family_semantics="at_least_k",
            certification_regime="cut_level",
            mode="edge_dropout",
            severity=0.0,
            seed=101,
        )
        self.assertTrue(ev["strict_after_ready"])
        self.assertTrue(ev["family_after_ready"])
        self.assertFalse(ev["no_worse_violation"])

    def test_augmented_exact_k_can_rescue_frontier_dropout(self):
        config = ChannelSeparatedRunConfig(seeds=(17,), steps=12, max_targets=8)
        state = build_channel_seed_state(config, 17)
        motif = next(m for m in target_motifs_for_channel_severance(state.motifs, max_targets=8) if len(m.support_cut) > 1)
        rows = []
        for severity in (0.25, 0.5, 0.75):
            rows.append(evaluate_support_family_monotonicity(
                state,
                motif,
                next(iter(motif.carrier)),
                threshold_fraction=0.25,
                family_semantics="augmented_exact_k",
                certification_regime="cut_level",
                mode="frontier_dropout",
                severity=severity,
                seed=101,
            ))
        self.assertTrue(any(bool(r["family_rescues_strict_loss"]) for r in rows))

    def test_parent_shared_certification_preserves_monotone_no_worse(self):
        config = SupportFamilyMonotonicityConfig(
            seeds=(17, 18),
            steps=10,
            max_targets=4,
            modes=("ledger_failure", "orientation_degradation"),
            threshold_fractions=(1.0, 0.5, 0.25),
            family_semantics=("at_least_k", "augmented_exact_k"),
            certification_regimes=("parent_shared",),
        )
        summary, _run_rows, _agg, audit, _cert, _width, _sample = run_support_family_monotonicity(config)
        self.assertEqual(summary["monotone_semantics_no_worse_violations"], 0)
        self.assertTrue(all(float(r["no_worse_violation_rate"]) == 0.0 for r in audit))

    def test_exact_k_can_have_no_worse_violations_under_cut_level_certification(self):
        config = SupportFamilyMonotonicityConfig(
            seeds=(17, 18, 19),
            steps=12,
            max_targets=6,
            modes=("ledger_failure", "orientation_degradation"),
            threshold_fractions=(0.25,),
            family_semantics=("exact_k",),
            certification_regimes=("cut_level",),
        )
        summary, _run_rows, aggregate, audit, cert, _width, _sample = run_support_family_monotonicity(config)
        self.assertGreater(summary["total_no_worse_violations"], 0)
        self.assertTrue(any(float(r["no_worse_violation_rate"]) > 0 for r in aggregate))
        self.assertTrue(cert)
        self.assertTrue(audit)

    def test_end_to_end_outputs(self):
        config = SupportFamilyMonotonicityConfig(
            seeds=(17, 18),
            steps=8,
            max_targets=4,
            sample_limit=50,
            threshold_fractions=(1.0, 0.5, 0.25),
        )
        summary, run_rows, aggregate, audit, cert, width, sample = run_support_family_monotonicity(config)
        self.assertGreater(summary["actual_evaluations"], 0)
        self.assertGreaterEqual(summary["support_width_count"], 1)
        self.assertTrue(aggregate)
        self.assertTrue(audit)
        self.assertTrue(width)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            rows_to_csv([summary], out / "summary.csv")
            rows_to_csv(aggregate, out / "aggregate.csv")
            write_predictions(summary, aggregate, audit, cert, out / "predictions.md")
            write_state(summary, run_rows, aggregate, audit, cert, width, sample, out / "state.json")
            self.assertTrue((out / "summary.csv").exists())
            self.assertTrue((out / "aggregate.csv").exists())
            self.assertTrue((out / "predictions.md").exists())
            self.assertTrue((out / "state.json").exists())


if __name__ == "__main__":
    unittest.main()
