import csv
import tempfile
import unittest
from pathlib import Path

from analysis.ra_native_overlap_robustness_analysis import (
    component_ablation,
    run_analysis,
    weighted_overlap,
    BASE_WEIGHTS,
)


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w=csv.DictWriter(f, fieldnames=fieldnames); w.writeheader(); w.writerows(rows)


class NativeOverlapRobustnessTests(unittest.TestCase):
    def test_weighted_overlap_uses_components(self):
        row={"mean_support_overlap":"0.0","mean_frontier_overlap":"0.0","mean_orientation_overlap":"1.0","mean_ledger_overlap":"1.0","mean_causal_past_overlap":"0.0","mean_bdg_kernel_overlap":"0.0","mean_firewall_overlap":"0.0"}
        self.assertGreater(weighted_overlap(row, {"orientation":1,"ledger":1}), 0.9)
        self.assertLess(weighted_overlap(row, {"support":1,"frontier":1}), 0.1)

    def test_component_ablation_identifies_component(self):
        rows=[]
        for ov, rate in [(0.1,0.4),(0.5,0.2),(0.95,0.0)]:
            rows.append({"mode":"ledger_failure","family_semantics":"at_least_k","samples":"100","certification_rescue_rate":str(rate),
                         "mean_support_overlap":str(ov),"mean_frontier_overlap":str(ov),"mean_orientation_overlap":str(ov),"mean_ledger_overlap":str(ov),"mean_causal_past_overlap":str(ov),"mean_bdg_kernel_overlap":str(ov),"mean_firewall_overlap":str(ov)})
        out=component_ablation(rows)
        base=[r for r in out if r["ablated_component"]=="none"][0]
        drop=[r for r in out if r["ablated_component"]=="ledger"][0]
        self.assertTrue(base["monotone_low_to_high"])
        self.assertEqual(base["low_high_gap"], 0.4)
        self.assertIn("low_high_gap", drop)

    def test_run_analysis_outputs_files(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)/"input"; out=Path(td)/"out"
            field=["mode","family_semantics","severity","threshold_fraction","support_width","samples","mean_weighted_native_overlap","mean_induced_certificate_correlation","certification_rescue_rate","mean_support_overlap","mean_frontier_overlap","mean_orientation_overlap","mean_ledger_overlap","mean_causal_past_overlap","mean_bdg_kernel_overlap","mean_firewall_overlap"]
            rows=[]
            for b, rate, led in [("low",0.3,0.1),("medium",0.1,0.5),("high",0.0,0.95)]:
                rows.append({"mode":"ledger_failure","family_semantics":"at_least_k","severity":"0.5","threshold_fraction":"0.25","support_width":"2","samples":"100","mean_weighted_native_overlap":str(led),"mean_induced_certificate_correlation":str(led),"certification_rescue_rate":str(rate),"mean_support_overlap":"0.1","mean_frontier_overlap":"0.1","mean_orientation_overlap":"0.1","mean_ledger_overlap":str(led),"mean_causal_past_overlap":"0.1","mean_bdg_kernel_overlap":"0.1","mean_firewall_overlap":"0.1"})
            write_csv(base/"ra_witness_overlap_components_v0_9.csv", rows, field)
            write_csv(base/"ra_cert_rescue_by_native_overlap_v0_9.csv", [
                {"mode":"ledger_failure","family_semantics":"at_least_k","native_overlap_bin":"low","samples":"100","mean_induced_certificate_correlation":"0.1","certification_rescue_rate":"0.3","family_certification_resilience_rate":"0.8","family_internal_loss_rate":"0.2"}],
                ["mode","family_semantics","native_overlap_bin","samples","mean_induced_certificate_correlation","certification_rescue_rate","family_certification_resilience_rate","family_internal_loss_rate"])
            write_csv(base/"ra_native_certificate_overlap_selector_guardrail_v0_9.csv", [{"native_certification_regime":"native","family_semantics":"at_least_k","samples":"10","certification_rescue_rate":"0","family_certification_resilience_rate":"0","selector_guardrail_passed":"True"}], ["native_certification_regime","family_semantics","samples","certification_rescue_rate","family_certification_resilience_rate","selector_guardrail_passed"])
            write_csv(base/"ra_overlap_vs_external_correlation_comparison_v0_9.csv", [{"mode":"ledger_failure","family_semantics":"at_least_k","severity":"0.5","threshold_fraction":"0.25","native_overlap_bin":"high","native_mean_induced_certificate_correlation":"1.0","native_certification_rescue_rate":"0.0","parent_shared_certification_rescue_rate":"0.0","native_minus_parent_rescue":"0.0","native_family_certification_resilience_rate":"0.5","parent_shared_family_certification_resilience_rate":"0.5","native_minus_parent_resilience":"0.0"}], ["mode","family_semantics","severity","threshold_fraction","native_overlap_bin","native_mean_induced_certificate_correlation","native_certification_rescue_rate","parent_shared_certification_rescue_rate","native_minus_parent_rescue","native_family_certification_resilience_rate","parent_shared_family_certification_resilience_rate","native_minus_parent_resilience"])
            summary=run_analysis(base,out)
            self.assertTrue((out/"ra_native_overlap_component_ablation_v0_9_1.csv").exists())
            self.assertTrue((out/"ra_native_overlap_robustness_summary_v0_9_1.md").exists())
            self.assertTrue(summary["selector_guardrail_passed"])

    def test_external_alignment_optional(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td)/"input"; out=Path(td)/"out"; ext=Path(td)/"ext"
            # Re-use minimal setup from previous test, but include external AUC.
            field=["mode","family_semantics","severity","threshold_fraction","support_width","samples","mean_weighted_native_overlap","mean_induced_certificate_correlation","certification_rescue_rate","mean_support_overlap","mean_frontier_overlap","mean_orientation_overlap","mean_ledger_overlap","mean_causal_past_overlap","mean_bdg_kernel_overlap","mean_firewall_overlap"]
            write_csv(base/"ra_witness_overlap_components_v0_9.csv", [{"mode":"ledger_failure","family_semantics":"at_least_k","severity":"0.5","threshold_fraction":"0.25","support_width":"2","samples":"100","mean_weighted_native_overlap":"0.2","mean_induced_certificate_correlation":"0.2","certification_rescue_rate":"0.3","mean_support_overlap":"0.2","mean_frontier_overlap":"0.2","mean_orientation_overlap":"0.2","mean_ledger_overlap":"0.2","mean_causal_past_overlap":"0.2","mean_bdg_kernel_overlap":"0.2","mean_firewall_overlap":"0.2"}], field)
            write_csv(base/"ra_cert_rescue_by_native_overlap_v0_9.csv", [{"mode":"ledger_failure","family_semantics":"at_least_k","native_overlap_bin":"low","samples":"100","mean_induced_certificate_correlation":"0.2","certification_rescue_rate":"0.3","family_certification_resilience_rate":"0.8","family_internal_loss_rate":"0.2"}], ["mode","family_semantics","native_overlap_bin","samples","mean_induced_certificate_correlation","certification_rescue_rate","family_certification_resilience_rate","family_internal_loss_rate"])
            write_csv(base/"ra_native_certificate_overlap_selector_guardrail_v0_9.csv", [], ["native_certification_regime","family_semantics","samples","certification_rescue_rate","family_certification_resilience_rate","selector_guardrail_passed"])
            write_csv(base/"ra_overlap_vs_external_correlation_comparison_v0_9.csv", [], ["mode","family_semantics","severity","threshold_fraction","native_overlap_bin","native_certification_rescue_rate","parent_shared_certification_rescue_rate","native_family_certification_resilience_rate","parent_shared_family_certification_resilience_rate"])
            write_csv(ext/"ra_cert_resilience_auc_by_mode_v0_8_1.csv", [{"mode":"ledger_failure","family_semantics":"at_least_k","curve_count":"1","all_monotone_nonincreasing":"true","mean_rescue_auc":"0.2","mean_resilience_auc":"0.5","mean_rescue_decay":"0.3","max_rescue_decay":"0.3","mean_start_rescue_rate":"0.3","mean_end_rescue_rate":"0","mean_half_decay_correlation":"0.5"}], ["mode","family_semantics","curve_count","all_monotone_nonincreasing","mean_rescue_auc","mean_resilience_auc","mean_rescue_decay","max_rescue_decay","mean_start_rescue_rate","mean_end_rescue_rate","mean_half_decay_correlation"])
            run_analysis(base,out,ext)
            with (out/"ra_native_overlap_external_correlation_alignment_v0_9_1.csv").open() as f:
                rows=list(csv.DictReader(f))
            self.assertEqual(rows[0]["external_available"], "True")

if __name__ == "__main__":
    unittest.main()
