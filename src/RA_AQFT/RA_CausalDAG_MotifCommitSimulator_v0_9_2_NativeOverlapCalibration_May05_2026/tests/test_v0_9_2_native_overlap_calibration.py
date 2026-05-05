from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from analysis.ra_native_overlap_calibration_audit import (
    calibration_curve,
    inverse_external_correlation,
    ledger_atleastk_zero_baseline_audit,
    run_analysis,
    semantics_signal_carriers,
)


def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


class NativeOverlapCalibrationV092Tests(unittest.TestCase):
    def test_inverse_external_correlation_nearest(self):
        corr, resid = inverse_external_correlation([(0.0, 0.25), (0.5, 0.10), (1.0, 0.0)], 0.11)
        self.assertEqual(corr, 0.5)
        self.assertLess(resid, 0.02)

    def test_signal_carrier_detects_augmented_gap(self):
        rows = [
            {"mode":"ledger_failure","family_semantics":"augmented_exact_k","native_overlap_bin":"low","samples":"10","mean_induced_certificate_correlation":"0.2","certification_rescue_rate":"0.30","family_certification_resilience_rate":"0.5","family_internal_loss_rate":"0.5"},
            {"mode":"ledger_failure","family_semantics":"augmented_exact_k","native_overlap_bin":"high","samples":"10","mean_induced_certificate_correlation":"0.9","certification_rescue_rate":"0.00","family_certification_resilience_rate":"0.4","family_internal_loss_rate":"0.6"},
        ]
        out = semantics_signal_carriers(rows)
        self.assertEqual(out[0]["signal_status"], "strong_low_overlap_rescue_signal")

    def test_ledger_atleastk_zero_baseline_detected(self):
        native = [
            {"mode":"ledger_failure","family_semantics":"at_least_k","native_overlap_bin":"low","samples":"10","mean_induced_certificate_correlation":"0.2","certification_rescue_rate":"0.0","family_certification_resilience_rate":"0.5","family_internal_loss_rate":"0.5"},
            {"mode":"ledger_failure","family_semantics":"at_least_k","native_overlap_bin":"high","samples":"10","mean_induced_certificate_correlation":"0.9","certification_rescue_rate":"0.0","family_certification_resilience_rate":"0.4","family_internal_loss_rate":"0.6"},
        ]
        rows = ledger_atleastk_zero_baseline_audit(native, [])
        summary = [r for r in rows if r["audit_scope"] == "native_bin_summary"][0]
        self.assertTrue(summary["zero_baseline"])

    def test_end_to_end_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inp = root/'in'; ext = root/'ext'; out = root/'out'
            native_fields = ["mode","family_semantics","native_overlap_bin","samples","mean_induced_certificate_correlation","certification_rescue_rate","family_certification_resilience_rate","family_internal_loss_rate"]
            native = [
                {"mode":"ledger_failure","family_semantics":"at_least_k","native_overlap_bin":"low","samples":"10","mean_induced_certificate_correlation":"0.2","certification_rescue_rate":"0.0","family_certification_resilience_rate":"0.4","family_internal_loss_rate":"0.6"},
                {"mode":"ledger_failure","family_semantics":"at_least_k","native_overlap_bin":"high","samples":"10","mean_induced_certificate_correlation":"0.9","certification_rescue_rate":"0.0","family_certification_resilience_rate":"0.4","family_internal_loss_rate":"0.6"},
                {"mode":"ledger_failure","family_semantics":"augmented_exact_k","native_overlap_bin":"low","samples":"10","mean_induced_certificate_correlation":"0.2","certification_rescue_rate":"0.3","family_certification_resilience_rate":"0.6","family_internal_loss_rate":"0.4"},
                {"mode":"ledger_failure","family_semantics":"augmented_exact_k","native_overlap_bin":"high","samples":"10","mean_induced_certificate_correlation":"0.9","certification_rescue_rate":"0.0","family_certification_resilience_rate":"0.4","family_internal_loss_rate":"0.6"},
            ]
            write_csv(inp/'ra_cert_rescue_by_native_overlap_v0_9.csv', native, native_fields)
            agg_fields = ["mode","family_semantics","samples","support_width_count","mean_support_width","mean_family_size"]
            write_csv(inp/'ra_native_certificate_overlap_aggregate_v0_9.csv', [
                {"mode":"ledger_failure","family_semantics":"augmented_exact_k","samples":"20","support_width_count":"3","mean_support_width":"2.5","mean_family_size":"4"}
            ], agg_fields)
            comp_fields = ["mode","family_semantics","severity","threshold_fraction","support_width","samples","mean_weighted_native_overlap","mean_induced_certificate_correlation","certification_rescue_rate"]
            write_csv(inp/'ra_witness_overlap_components_v0_9.csv', [
                {"mode":"ledger_failure","family_semantics":"at_least_k","severity":"0.5","threshold_fraction":"0.25","support_width":"2","samples":"5","mean_weighted_native_overlap":"0.5","mean_induced_certificate_correlation":"0.5","certification_rescue_rate":"0.0"}
            ], comp_fields)
            write_csv(inp/'ra_native_certificate_overlap_selector_guardrail_v0_9.csv', [{"selector_guardrail_passed":"true"}], ["selector_guardrail_passed"])
            ext_fields = ["mode","family_semantics","severity","threshold_fraction","certificate_correlation","samples","certification_rescue_rate"]
            write_csv(ext/'ra_cert_rescue_decay_curve_v0_8_1.csv', [
                {"mode":"ledger_failure","family_semantics":"augmented_exact_k","severity":"0.5","threshold_fraction":"0.25","certificate_correlation":"0.0","samples":"10","certification_rescue_rate":"0.25"},
                {"mode":"ledger_failure","family_semantics":"augmented_exact_k","severity":"0.5","threshold_fraction":"0.25","certificate_correlation":"1.0","samples":"10","certification_rescue_rate":"0.0"},
            ], ext_fields)
            summary = run_analysis(inp, ext, out)
            self.assertEqual(summary["candidate_primary_family_semantics"], "augmented_exact_k")
            self.assertTrue((out/'ra_native_overlap_v1_candidate_summary_v0_9_2.md').exists())

if __name__ == "__main__":
    unittest.main()
