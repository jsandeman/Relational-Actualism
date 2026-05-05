import tempfile
import unittest
from pathlib import Path

import pandas as pd

from analysis.ra_cert_correlation_analysis import (
    CertCorrelationAnalysisConfig,
    compute_decay_curve,
    compute_sensitivity,
    compute_endpoint_equivalence,
    write_outputs,
)


def synthetic_frames(tmp: Path):
    rows = []
    for mode in ["ledger_failure", "orientation_degradation"]:
        for sem in ["at_least_k"]:
            for corr, rate in [(0.0, 0.22), (0.25, 0.17), (0.5, 0.12), (0.75, 0.08), (1.0, 0.0)]:
                rows.append({
                    "mode": mode,
                    "family_semantics": sem,
                    "certification_regime": "independent_member",
                    "severity": 0.5,
                    "threshold_fraction": 0.25,
                    "certificate_correlation": corr,
                    "samples": 100,
                    "family_size_mean": 4.0,
                    "strict_parent_cert_failure_rate": 0.6,
                    "certification_rescue_rate": rate,
                    "family_certification_resilience_rate": rate + 0.2,
                    "family_internal_loss_rate": 1.0 - rate,
                    "family_internal_survival_rate": rate,
                    "mean_certified_family_member_count": 1.0 + rate,
                    "metric_artifact_risk_rate": 0.0,
                })
    corr = pd.DataFrame(rows)
    agg_rows = []
    for mode in ["ledger_failure", "orientation_degradation"]:
        for regime in ["independent_member", "parent_shared"]:
            corrs = [1.0] if regime == "independent_member" else [0.0, 0.5, 1.0]
            for c in corrs:
                agg_rows.append({
                    "mode": mode,
                    "family_semantics": "at_least_k",
                    "certification_regime": regime,
                    "severity": 0.5,
                    "threshold_fraction": 0.25,
                    "certificate_correlation": c,
                    "samples": 100,
                    "certification_rescue_rate": 0.0,
                    "family_certification_resilience_rate": 0.2,
                    "family_internal_loss_rate": 0.8,
                    "strict_parent_loss_rate": 0.5,
                })
    by_width = corr.copy()
    by_width["support_width"] = 4
    by_width["family_size_mean"] = 11
    guard = pd.DataFrame([{
        "mode": "selector_stress",
        "selector_guardrail_passed": True,
        "certification_rescue_rate": 0.0,
        "family_certification_resilience_rate": 0.0,
    }])
    return {
        "summary": pd.DataFrame(),
        "runs": pd.DataFrame(),
        "aggregate": pd.DataFrame(agg_rows),
        "correlation_sweep": corr,
        "resilience_by_regime": pd.DataFrame(),
        "by_width": by_width,
        "selector_guardrail": guard,
    }


class CertCorrelationAnalysisTests(unittest.TestCase):
    def test_sensitivity_detects_monotone_decay(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = CertCorrelationAnalysisConfig(input_dir=Path(d), output_dir=Path(d) / "out")
            decay = compute_decay_curve(synthetic_frames(Path(d)), cfg)
            sens = compute_sensitivity(decay, cfg)
            self.assertGreater(len(sens), 0)
            self.assertTrue((sens["monotone_nonincreasing"] == "true").all())
            self.assertTrue((sens["rescue_decay"] > 0).all())

    def test_endpoint_equivalence_matches_parent_shared(self):
        with tempfile.TemporaryDirectory() as d:
            cfg = CertCorrelationAnalysisConfig(input_dir=Path(d), output_dir=Path(d) / "out")
            frames = synthetic_frames(Path(d))
            decay = compute_decay_curve(frames, cfg)
            endpoint = compute_endpoint_equivalence(frames, decay, cfg)
            self.assertGreater(len(endpoint), 0)
            self.assertTrue((endpoint["endpoint_equivalent_within_tolerance"] == "true").all())
            self.assertEqual(float(endpoint["max_abs_endpoint_delta"].max()), 0.0)

    def test_end_to_end_writes_expected_files(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            inp = root / "inp"
            out = root / "out"
            inp.mkdir()
            frames = synthetic_frames(root)
            frames["correlation_sweep"].to_csv(inp / "ra_certification_correlation_sweep_v0_8.csv", index=False)
            frames["aggregate"].to_csv(inp / "ra_independent_cert_family_aggregate_v0_8.csv", index=False)
            frames["by_width"].to_csv(inp / "ra_independent_cert_family_by_width_v0_8.csv", index=False)
            frames["selector_guardrail"].to_csv(inp / "ra_independent_cert_selector_guardrail_v0_8.csv", index=False)
            paths = write_outputs(CertCorrelationAnalysisConfig(input_dir=inp, output_dir=out))
            for p in paths.__dict__.values():
                self.assertTrue(Path(p).exists(), p)
            md = paths.summary_md.read_text()
            self.assertIn("certification", md.lower())
            self.assertIn("monotone", md.lower())

    def test_nonmonotone_curve_is_flagged(self):
        with tempfile.TemporaryDirectory() as d:
            frames = synthetic_frames(Path(d))
            mask = (frames["correlation_sweep"]["mode"] == "ledger_failure") & (frames["correlation_sweep"]["certificate_correlation"] == 0.25)
            frames["correlation_sweep"].loc[mask, "certification_rescue_rate"] = 0.5
            cfg = CertCorrelationAnalysisConfig(input_dir=Path(d), output_dir=Path(d) / "out")
            decay = compute_decay_curve(frames, cfg)
            sens = compute_sensitivity(decay, cfg)
            self.assertIn("false", set(sens["monotone_nonincreasing"]))


if __name__ == "__main__":
    unittest.main()
