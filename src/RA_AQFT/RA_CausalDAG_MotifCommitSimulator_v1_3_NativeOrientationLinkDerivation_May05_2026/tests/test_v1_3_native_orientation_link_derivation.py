from pathlib import Path
import tempfile
import unittest
import pandas as pd
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from ra_native_orientation_link_derivation import (
    parse_lean_declarations, add_native_orientation_surface, add_native_adjusted_rescue,
    partial_correlation_audit, run_analysis
)

class NativeOrientationLinkDerivationTests(unittest.TestCase):
    def make_components(self):
        rows=[]
        for mode in ["orientation_degradation","ledger_failure","selector_stress"]:
            for sem in ["augmented_exact_k","at_least_k"]:
                for sev in [0.25,0.75]:
                    for width in [1,2,3,4]:
                        rows.append({
                            "mode":mode,"family_semantics":sem,"severity":sev,"threshold_fraction":0.25,
                            "support_width":width,"samples":10,"mean_weighted_native_overlap":0.5,
                            "mean_induced_certificate_correlation":0.5,"certification_rescue_rate":0.1,
                            "primary_signal_semantics":"augmented_exact_k","guardrail_semantics":"at_least_k",
                            "anchoring_status":"test","support_overlap":1/width,"frontier_overlap":1/width,
                            "orientation_overlap":1/width,"ledger_overlap":0.25+0.1*width,
                            "causal_past_overlap":0.3,"bdg_kernel_overlap":0.4,"firewall_overlap":0.5,
                        })
        return pd.DataFrame(rows)

    def make_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"RA_CausalOrientation_Core.lean"
            p.write_text('''theorem one_way_precedence : True := by trivial\ntheorem forward_winding_stable : True := by trivial\ntheorem reverse_winding_filtered : True := by trivial\n''')
            q=Path(td)/"RA_D1_NativeLedgerOrientation.lean"
            q.write_text('''theorem orientation_asymmetry : True := by trivial\ntheorem depth2_ledger_preserved_symmetric : True := by trivial\n''')
            return parse_lean_declarations([p,q])

    def test_manifest_extracts_native_orientation_names(self):
        m=self.make_manifest()
        self.assertIn("one_way_precedence", set(m["declaration"]))
        self.assertTrue((m["role"] == "orientation_link").any())

    def test_native_orientation_surface_decouples_from_support(self):
        df=self.make_components()
        m=self.make_manifest()
        out=add_native_orientation_surface(df,m)
        self.assertGreater((out["native_orientation_link_overlap"]-out["support_overlap"]).abs().max(), 0.05)
        self.assertLess((out["orientation_overlap"]-out["support_overlap"]).abs().max(), 1e-12)

    def test_partial_correlation_detects_independent_native_surface(self):
        out=add_native_adjusted_rescue(add_native_orientation_surface(self.make_components(), self.make_manifest()))
        audit=partial_correlation_audit(out)
        verdict=dict(zip(audit["component"], audit["control_verdict"]))
        self.assertEqual(verdict["orientation_overlap"], "no_independent_variation_after_support_frontier_control")
        self.assertEqual(verdict["native_orientation_link_overlap"], "independent_variation_after_support_frontier_control")

    def test_end_to_end_outputs(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); inp=root/"inputs"; out=root/"outputs"; lean=root/"lean"
            inp.mkdir(); lean.mkdir()
            self.make_components().to_csv(inp/"ra_native_certificate_components_v1_0.csv", index=False)
            (lean/"RA_CausalOrientation_Core.lean").write_text('theorem one_way_precedence : True := by trivial\ntheorem forward_winding_stable : True := by trivial\n')
            (lean/"RA_D1_NativeLedgerOrientation.lean").write_text('theorem orientation_asymmetry : True := by trivial\ntheorem depth2_ledger_preserved_symmetric : True := by trivial\n')
            state=run_analysis(inp,out,lean)
            self.assertTrue((out/"ra_native_orientation_link_surface_v1_3.csv").exists())
            self.assertTrue(state["summary"]["native_orientation_surface_decoupled"])

if __name__ == "__main__":
    unittest.main()
