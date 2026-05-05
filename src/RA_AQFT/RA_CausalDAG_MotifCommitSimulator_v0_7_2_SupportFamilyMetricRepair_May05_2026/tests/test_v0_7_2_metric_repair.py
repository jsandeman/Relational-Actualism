#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from simulator.ra_causal_dag_support_family_metric_repair import (
    MetricRepairConfig,
    enrich_metric_repair_row,
    run_metric_repair,
)
from simulator.ra_causal_dag_support_family_monotonicity import support_family_by_semantics
from simulator.ra_causal_dag_simulator import MotifCandidate


class SupportFamilyMetricRepairV072Tests(unittest.TestCase):
    def test_cut_level_certification_parent_absent_is_flagged_incomparable(self) -> None:
        row = {
            "mode": "ledger_failure",
            "certification_regime": "cut_level",
            "family_includes_strict_cut": False,
            "strict_before_ready": True,
            "strict_after_ready": True,
            "family_before_ready": True,
            "family_after_ready": False,
            "severity": 0.75,
            "family_size": 3,
            "uncertified_cut_count": 3,
        }
        enriched = enrich_metric_repair_row(row)
        self.assertFalse(enriched["comparison_valid_strict_vs_family"])
        self.assertTrue(enriched["metric_artifact_risk"])
        self.assertEqual(enriched["targeting_domain"], "family_member_domain_excludes_parent")
        self.assertEqual(enriched["apples_to_apples_loss_delta"], "")

    def test_parent_shared_certification_is_comparable(self) -> None:
        row = {
            "mode": "orientation_degradation",
            "certification_regime": "parent_shared",
            "family_includes_strict_cut": False,
            "strict_before_ready": True,
            "strict_after_ready": False,
            "family_before_ready": True,
            "family_after_ready": False,
            "severity": 0.75,
            "family_size": 4,
            "uncertified_cut_count": 4,
        }
        enriched = enrich_metric_repair_row(row)
        self.assertTrue(enriched["comparison_valid_strict_vs_family"])
        self.assertFalse(enriched["metric_artifact_risk"])
        self.assertEqual(enriched["targeting_domain"], "shared_parent_certificate")
        self.assertEqual(enriched["apples_to_apples_loss_delta"], 0)

    def test_exact_k_family_omits_parent_cut_when_k_less_than_width(self) -> None:
        motif = MotifCandidate(name="M", carrier=frozenset({10}), support_cut=frozenset({1, 2, 3, 4}), kind="test")
        family = support_family_by_semantics(motif, 0.25, "exact_k")
        self.assertEqual(family.threshold_k, 1)
        self.assertNotIn(motif.support_cut, family.cuts)

    def test_at_least_k_family_includes_parent_cut(self) -> None:
        motif = MotifCandidate(name="M", carrier=frozenset({10}), support_cut=frozenset({1, 2, 3, 4}), kind="test")
        family = support_family_by_semantics(motif, 0.25, "at_least_k")
        self.assertIn(motif.support_cut, family.cuts)

    def test_demo_run_generates_metric_artifact_flags(self) -> None:
        cfg = MetricRepairConfig(
            seeds=(17,),
            steps=8,
            severance_seeds=(101,),
            severities=(0.0, 0.75),
            modes=("ledger_failure",),
            threshold_fractions=(1.0, 0.25),
            family_semantics=("exact_k", "at_least_k"),
            certification_regimes=("cut_level", "parent_shared"),
            max_targets=4,
            sample_limit=20,
        )
        summary, runs, apples, width, targeting, cert, flags, sample = run_metric_repair(cfg)
        self.assertGreater(summary["actual_evaluations"], 0)
        self.assertGreaterEqual(summary["support_width_count"], 1)
        self.assertTrue(any(r["metric_artifact_risk_rate"] > 0 for r in apples))
        self.assertTrue(any(r["comparison_valid_rate"] < 1 for r in apples))
        self.assertTrue(flags)

    def test_support_channel_comparison_remains_valid(self) -> None:
        row = {
            "mode": "edge_dropout",
            "certification_regime": "cut_level",
            "family_includes_strict_cut": False,
            "strict_before_ready": True,
            "strict_after_ready": False,
            "family_before_ready": True,
            "family_after_ready": True,
            "severity": 0.5,
            "family_size": 4,
            "uncertified_cut_count": 0,
        }
        enriched = enrich_metric_repair_row(row)
        self.assertTrue(enriched["comparison_valid_strict_vs_family"])
        self.assertFalse(enriched["metric_artifact_risk"])
        self.assertTrue(enriched["strict_rescue_rate_event"])
        self.assertEqual(enriched["targeting_domain"], "causal_reachability_domain")


if __name__ == "__main__":
    unittest.main()
