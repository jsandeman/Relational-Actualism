# RA v1.0 Native Certificate Anchoring Summary

This v1.0 analysis consolidates the native certificate-overlap track. It does not add a new rescue law; it packages native witness-component surfaces and records the v1.0 modeling posture.

## Summary

- version: 1.0
- component_rows: 480
- native_overlap_profile_rows: 10
- native_overlap_bins: ['high', 'low', 'medium']
- native_overlap_bin_count: 3
- primary_family_semantics: augmented_exact_k
- guardrail_family_semantics: at_least_k
- primary_signal_rows: 2
- primary_signal_monotone_count: 2
- primary_mean_rescue_gap: 0.215688
- guardrail_signal_rows: 2
- guardrail_monotone_count: 2
- guardrail_mean_rescue_gap: 0.157785
- calibration_rows: 4
- selector_guardrail_passed: True
- v1_posture: component_anchored_proxy_ready_for_BDG_LLC_native_formalization

## Primary signal semantics

`augmented_exact_k` is the primary signal-carrier semantics because it preserves the parent support structure while adding focused alternatives and tends to populate low/medium/high native-overlap bins.

- mode=ledger_failure bins=low;medium;high gap=0.217501 monotone=True
- mode=orientation_degradation bins=low;medium;high gap=0.213874 monotone=True

## Guardrail semantics

`at_least_k` remains the monotone guardrail semantics. Missing low-overlap bins should be treated as bin-population structure, not as zero-rescue failure.

- mode=ledger_failure bins=medium;high gap=0.156531 monotone=True
- mode=orientation_degradation bins=medium;high gap=0.15904 monotone=True

## Calibration posture

Native-overlap bins are qualitative structural bins. They align directionally with the external v0.8.1 certificate-correlation curve, but they are not asserted as exact external-correlation values.

- calibration rows: 4

## BDG-LLC / native-certificate caution

The current simulator components are operational proxies for native support/frontier/orientation/ledger/causal-past/kernel/firewall evidence. v1.0 prepares formal surfaces for anchoring these components, but does not yet derive the overlap weights or rescue law from the BDG-LLC action.
