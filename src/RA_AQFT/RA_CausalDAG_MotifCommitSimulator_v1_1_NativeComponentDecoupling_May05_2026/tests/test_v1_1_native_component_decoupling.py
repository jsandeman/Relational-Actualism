
import tempfile
from pathlib import Path
import unittest
import pandas as pd

from analysis.ra_native_component_decoupling import (
    component_decoupling_audit,
    orientation_specificity_by_mode,
    component_partial_correlation,
    run_decoupling_analysis,
)


def synthetic(confounded=True):
    rows = []
    for mode in ["ledger_failure", "orientation_degradation"]:
        for sem in ["augmented_exact_k", "at_least_k"]:
            for width in [1,2,3,4]:
                support = 1.0 if width == 1 else 1.0 / width
                frontier = support
                if confounded:
                    orientation = support
                else:
                    orientation = 0.2 + 0.2 * width if mode == "orientation_degradation" else support
                ledger = 0.9 - 0.1 * width if mode == "ledger_failure" else 0.5
                rescue = (1.0 - orientation) if mode == "orientation_degradation" else (1.0 - ledger)
                rows.append({
                    "mode": mode,
                    "family_semantics": sem,
                    "severity": 0.5,
                    "threshold_fraction": 0.25,
                    "support_width": width,
                    "samples": 10,
                    "mean_weighted_native_overlap": 0.5,
                    "mean_induced_certificate_correlation": 0.5,
                    "certification_rescue_rate": rescue,
                    "primary_signal_semantics": "augmented_exact_k",
                    "guardrail_semantics": "at_least_k",
                    "anchoring_status": "test",
                    "support_overlap": support,
                    "frontier_overlap": frontier,
                    "orientation_overlap": orientation,
                    "ledger_overlap": ledger,
                    "causal_past_overlap": 0.4,
                    "bdg_kernel_overlap": 0.4,
                    "firewall_overlap": 0.4,
                })
    return pd.DataFrame(rows)


class NativeComponentDecouplingTests(unittest.TestCase):
    def test_confounded_triplet_detected(self):
        df = synthetic(confounded=True)
        out = component_decoupling_audit(df)
        triplet = out[out.component_a == "support_frontier_orientation_triplet"].iloc[0]
        self.assertEqual(triplet.decoupling_status, "orientation_confounded_with_support_frontier")

    def test_decoupled_orientation_detected(self):
        df = synthetic(confounded=False)
        out = component_decoupling_audit(df)
        triplet = out[out.component_a == "support_frontier_orientation_triplet"].iloc[0]
        self.assertEqual(triplet.decoupling_status, "orientation_surface_has_independent_variation")

    def test_specificity_flags_orientation_confounding(self):
        df = synthetic(confounded=True)
        spec = orientation_specificity_by_mode(df)
        row = spec[(spec["mode"] == "orientation_degradation") & (spec.family_semantics == "augmented_exact_k")].iloc[0]
        self.assertEqual(row.specificity_status, "orientation_confounded_with_support_frontier")

    def test_partial_correlation_has_no_orientation_variation_when_confounded(self):
        df = synthetic(confounded=True)
        pc = component_partial_correlation(df)
        row = pc[(pc["mode"] == "orientation_degradation") & (pc.component == "orientation_overlap")].iloc[0]
        self.assertEqual(row.partial_status, "no_independent_component_variation_after_support_frontier_control")

    def test_end_to_end_outputs(self):
        df = synthetic(confounded=True)
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "inputs"
            out = Path(td) / "outputs"
            inp.mkdir()
            df.to_csv(inp / "ra_native_certificate_components_v1_0.csv", index=False)
            state = run_decoupling_analysis(inp, out)
            self.assertTrue((out / "ra_component_decoupling_audit_v1_1.csv").exists())
            self.assertTrue((out / "ra_native_component_decoupling_summary_v1_1.md").exists())
            self.assertEqual(state["summary"]["v1_1_posture"], "ledger_attribution_clean_orientation_attribution_still_confounded")

if __name__ == "__main__":
    unittest.main()
