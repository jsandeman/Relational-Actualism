
import tempfile
from pathlib import Path
import unittest
import pandas as pd
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from analysis.ra_orientation_link_surface import (
    add_distinct_orientation_surface, compute_surface_adjusted_rescue,
    partial_correlation_audit, run_analysis
)

class TestOrientationLinkSurfaceV12(unittest.TestCase):
    def sample(self):
        rows=[]
        for mode in ["ledger_failure","orientation_degradation","selector_stress"]:
            for sem in ["at_least_k","augmented_exact_k"]:
                for sev in [0.25,0.5,0.75]:
                    for width in [1,2,3,4]:
                        base=1/width
                        rows.append(dict(mode=mode,family_semantics=sem,severity=sev,threshold_fraction=0.25,
                                         support_width=width,samples=10,certification_rescue_rate=0.1,
                                         support_overlap=base,frontier_overlap=base,orientation_overlap=base,
                                         ledger_overlap=min(1.0,base+0.2),causal_past_overlap=base+0.1,
                                         bdg_kernel_overlap=base+0.08,firewall_overlap=base+0.05))
        return pd.DataFrame(rows)

    def test_orientation_surface_decouples_from_support(self):
        df=add_distinct_orientation_surface(self.sample())
        self.assertGreater((df.orientation_link_overlap-df.support_overlap).abs().max(),1e-6)
        self.assertLess((df.orientation_overlap-df.support_overlap).abs().max(),1e-12)

    def test_partial_correlation_detects_new_variation(self):
        df=add_distinct_orientation_surface(self.sample())
        audit=partial_correlation_audit(df)
        orient=audit[audit.component=="orientation_link_overlap"].iloc[0]
        old=audit[audit.component=="orientation_overlap"].iloc[0]
        self.assertEqual(old.control_verdict,"no_independent_variation_after_support_frontier_control")
        self.assertEqual(orient.control_verdict,"independent_variation_after_support_frontier_control")

    def test_orientation_degradation_sensitive_to_orientation_surface(self):
        df=compute_surface_adjusted_rescue(add_distinct_orientation_surface(self.sample()))
        ori=df[df["mode"]=="orientation_degradation"]
        low=ori[ori.orientation_link_bin=="low"].orientation_surface_adjusted_rescue_rate.mean()
        high=ori[ori.orientation_link_bin=="high"].orientation_surface_adjusted_rescue_rate.mean()
        self.assertGreater(low, high)

    def test_selector_stress_guardrail(self):
        df=compute_surface_adjusted_rescue(add_distinct_orientation_surface(self.sample()))
        sel=df[df["mode"]=="selector_stress"]
        self.assertTrue((sel.orientation_surface_adjusted_rescue_rate == sel.certification_rescue_rate).all())

    def test_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            inp=Path(td)/"inputs"; out=Path(td)/"outputs"; inp.mkdir()
            self.sample().to_csv(inp/"ra_native_certificate_components_v1_0.csv", index=False)
            pd.DataFrame().to_csv(inp/"ra_native_overlap_profile_v1_0.csv", index=False)
            state=run_analysis(inp,out)
            self.assertTrue(state["new_orientation_link_surface_decoupled"])
            self.assertTrue((out/"ra_native_orientation_surface_summary_v1_2.md").exists())

if __name__ == '__main__':
    unittest.main()
