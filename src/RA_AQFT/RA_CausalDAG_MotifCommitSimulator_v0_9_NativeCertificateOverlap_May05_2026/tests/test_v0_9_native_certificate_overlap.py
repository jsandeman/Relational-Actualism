import unittest

from simulator.ra_causal_dag_native_cert_overlap import (
    NativeOverlapWeights,
    _jaccard,
    _bin_overlap,
    NativeCertificateOverlapConfig,
    run_native_certificate_overlap,
    overlap_signature_rows,
)


class NativeCertificateOverlapV09Tests(unittest.TestCase):
    def test_jaccard_bounds_and_identity(self):
        self.assertEqual(_jaccard({1, 2}, {1, 2}), 1.0)
        self.assertEqual(_jaccard({1}, {2}), 0.0)
        self.assertTrue(0.0 <= _jaccard({1, 2}, {2, 3}) <= 1.0)

    def test_overlap_bins(self):
        self.assertEqual(_bin_overlap(0.1), "low")
        self.assertEqual(_bin_overlap(0.5), "medium")
        self.assertEqual(_bin_overlap(0.9), "high")

    def test_weight_profiles_normalize(self):
        for p in ("balanced", "support_heavy", "certificate_heavy"):
            w = NativeOverlapWeights.from_profile(p).normalized()
            self.assertAlmostEqual(sum(w.values()), 1.0, places=9)
            self.assertEqual(set(w), {"support", "frontier", "orientation", "ledger", "causal_past", "bdg_kernel", "firewall"})

    def test_packet_demo_generates_nontrivial_overlap(self):
        config = NativeCertificateOverlapConfig(
            seeds=(17,), steps=8, max_targets=3, severance_seeds=(101,),
            severities=(0.0, 0.5, 1.0), modes=("ledger_failure", "orientation_degradation", "selector_stress"),
            threshold_fractions=(1.0, 0.5, 0.25), family_semantics=("at_least_k",),
            include_parent_shared_baseline=True, sample_limit=50,
        )
        summary, _runs, _agg, _comp, rescue, signature, selectors, _sample, _all = run_native_certificate_overlap(config)
        self.assertGreater(summary["actual_evaluations"], 0)
        self.assertGreaterEqual(summary["native_overlap_bin_count"], 1)
        self.assertTrue(summary["selector_guardrail_passed"])
        self.assertTrue(all(r["selector_guardrail_passed"] for r in selectors))
        self.assertTrue(rescue)
        self.assertTrue(signature)

    def test_overlap_signature_monotonicity_function(self):
        rows = []
        for bin_name, rescue_flags in [("low", [True, False, False, False]), ("medium", [False, False, False, False]), ("high", [False, False, False, False])]:
            for flag in rescue_flags:
                rows.append({
                    "native_certification_regime": "native_overlap_induced",
                    "certification_mode": True,
                    "severity": 0.5,
                    "mode": "ledger_failure",
                    "family_semantics": "at_least_k",
                    "native_overlap_bin": bin_name,
                    "induced_certificate_correlation": {"low":0.2,"medium":0.5,"high":0.8}[bin_name],
                    "certification_rescue_event": flag,
                    "family_certification_resilience_event": flag,
                    "family_internal_loss": not flag,
                })
        sig = overlap_signature_rows(rows)
        self.assertEqual(len(sig), 1)
        self.assertTrue(sig[0]["monotone_nonincreasing_by_overlap_bin"])


if __name__ == "__main__":
    unittest.main()
