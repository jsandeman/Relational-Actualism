from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from simulator.ra_causal_dag_independent_cert_families import (
    IndependentCertifiedFamilyConfig,
    _certification_failure_state,
    evaluate_independent_certified_family,
    run_independent_certified_families,
)
from simulator.ra_causal_dag_channel_workbench import build_channel_seed_state, target_motifs_for_channel_severance
from simulator.ra_causal_dag_support_family_monotonicity import support_family_by_semantics
from simulator.ra_causal_dag_simulator import motif_site


class IndependentCertifiedFamiliesV08Tests(unittest.TestCase):
    def _state_and_wide_motif(self):
        cfg = IndependentCertifiedFamilyConfig(seeds=(17,), steps=16, max_targets=8)
        state = build_channel_seed_state(cfg.channel_config(17), 17)
        targets = target_motifs_for_channel_severance(state.motifs, max_targets=8)
        wide = [m for m in targets if len(m.support_cut) >= 2]
        self.assertTrue(wide, "test setup should expose a width >= 2 motif")
        return cfg, state, wide[0]

    def test_parent_shared_certification_fails_all_or_none(self):
        _cfg, _state, motif = self._state_and_wide_motif()
        site = motif_site(motif)
        family = support_family_by_semantics(motif, 0.5, "at_least_k")
        st = _certification_failure_state(
            motif, family, site,
            mode="ledger_failure", severity=1.0, seed=101,
            certification_regime="parent_shared", certificate_correlation=0.0,
        )
        self.assertTrue(st.strict_parent_uncertified)
        self.assertEqual(len(st.uncertified_family_cuts), family.family_size)

    def test_independent_member_can_leave_family_cut_when_parent_fails(self):
        _cfg, state, motif = self._state_and_wide_motif()
        site = motif_site(motif)
        saw_rescue_shape = False
        for seed in range(100, 250):
            row = evaluate_independent_certified_family(
                state, motif, site,
                threshold_fraction=0.5,
                family_semantics="at_least_k",
                certification_regime="independent_member",
                certificate_correlation=0.0,
                mode="ledger_failure",
                severity=0.5,
                seed=seed,
            )
            if row["strict_parent_cert_failed"] and row["family_after_ready"]:
                saw_rescue_shape = True
                break
        self.assertTrue(saw_rescue_shape, "independent member certificates should permit parent-fail/family-survive rows")

    def test_full_correlation_matches_shared_failure_shape(self):
        _cfg, state, motif = self._state_and_wide_motif()
        site = motif_site(motif)
        row = evaluate_independent_certified_family(
            state, motif, site,
            threshold_fraction=0.5,
            family_semantics="at_least_k",
            certification_regime="independent_member",
            certificate_correlation=1.0,
            mode="orientation_degradation",
            severity=1.0,
            seed=101,
        )
        self.assertTrue(row["strict_parent_cert_failed"])
        self.assertFalse(row["family_after_ready"])
        self.assertFalse(row["certification_rescue_event"])

    def test_selector_stress_not_counted_as_certification_rescue(self):
        _cfg, state, motif = self._state_and_wide_motif()
        site = motif_site(motif)
        row = evaluate_independent_certified_family(
            state, motif, site,
            threshold_fraction=0.5,
            family_semantics="at_least_k",
            certification_regime="independent_member",
            certificate_correlation=0.0,
            mode="selector_stress",
            severity=1.0,
            seed=101,
        )
        self.assertFalse(row["certification_rescue_event"])
        self.assertFalse(row["family_certification_resilience_event"])

    def test_correlation_sweep_decreases_rescue_in_demo(self):
        cfg = IndependentCertifiedFamilyConfig(
            seeds=(17, 18), steps=12, max_targets=6,
            modes=("ledger_failure", "orientation_degradation"),
            severities=(0.5,), threshold_fractions=(0.5,),
            family_semantics=("at_least_k",),
            certification_regimes=("independent_member",),
            certificate_correlations=(0.0, 1.0),
            sample_limit=10,
        )
        summary, _runs, _agg, corr, _regimes, _widths, _selectors, _sample, _all = run_independent_certified_families(cfg)
        by_corr = {float(r["certificate_correlation"]): float(r["certification_rescue_rate"]) for r in corr if r["mode"] == "ledger_failure"}
        self.assertGreaterEqual(by_corr[0.0], by_corr[1.0])
        self.assertGreaterEqual(summary["support_width_count"], 1)

    def test_end_to_end_outputs_nonempty(self):
        cfg = IndependentCertifiedFamilyConfig(
            seeds=(17,), steps=8, max_targets=4,
            modes=("ledger_failure", "selector_stress"),
            severities=(0.0, 0.5), threshold_fractions=(1.0, 0.5),
            family_semantics=("at_least_k",),
            certification_regimes=("parent_shared", "independent_member"),
            certificate_correlations=(0.0, 1.0),
            sample_limit=20,
        )
        summary, runs, aggregate, corr, regimes, widths, selectors, sample, all_rows = run_independent_certified_families(cfg)
        self.assertGreater(summary["actual_evaluations"], 0)
        self.assertTrue(runs)
        self.assertTrue(aggregate)
        self.assertTrue(corr)
        self.assertTrue(regimes)
        self.assertTrue(widths)
        self.assertTrue(selectors)
        self.assertTrue(sample)
        self.assertTrue(all_rows)


if __name__ == "__main__":
    unittest.main()
