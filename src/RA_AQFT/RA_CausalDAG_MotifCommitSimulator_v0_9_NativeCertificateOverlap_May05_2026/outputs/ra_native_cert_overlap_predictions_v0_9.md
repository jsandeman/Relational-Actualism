# RA Native Certificate Overlap — v0.9

This workbench replaces the external v0.8 certificate-correlation knob with a native overlap calculation over support-family member certificate witnesses.

## Scale

- run_count: 100
- steps: 32
- actual_evaluations: 480000
- support_width_classes: [1, 2, 3, 4]
- native_overlap_bins: ['high', 'low', 'medium']
- induced_certificate_correlation range: 0.178704..1.0

## Highest native-overlap-induced certification rescue rows

- mode=ledger_failure semantics=augmented_exact_k bin=low corr_mean=0.250781: cert_rescue=0.218192 resilience=0.59933 loss=0.40067
- mode=orientation_degradation semantics=augmented_exact_k bin=low corr_mean=0.250781: cert_rescue=0.214565 resilience=0.597098 loss=0.402902
- mode=orientation_degradation semantics=at_least_k bin=medium corr_mean=0.489153: cert_rescue=0.159731 resilience=0.535379 loss=0.464621
- mode=ledger_failure semantics=at_least_k bin=medium corr_mean=0.489153: cert_rescue=0.157222 resilience=0.53125 loss=0.46875
- mode=orientation_degradation semantics=augmented_exact_k bin=medium corr_mean=0.498448: cert_rescue=0.138116 resilience=0.522126 loss=0.477874
- mode=ledger_failure semantics=augmented_exact_k bin=medium corr_mean=0.498448: cert_rescue=0.13766 resilience=0.509808 loss=0.490192
- mode=ledger_failure semantics=at_least_k bin=high corr_mean=0.9978: cert_rescue=0.000691 resilience=0.374962 loss=0.625038
- mode=ledger_failure semantics=augmented_exact_k bin=high corr_mean=0.9978: cert_rescue=0.000691 resilience=0.374962 loss=0.625038
- mode=orientation_degradation semantics=at_least_k bin=high corr_mean=0.9978: cert_rescue=0.000691 resilience=0.391124 loss=0.608876
- mode=orientation_degradation semantics=augmented_exact_k bin=high corr_mean=0.9978: cert_rescue=0.000691 resilience=0.391124 loss=0.608876

## Overlap signature

- signature rows: 4
- monotone non-increasing by overlap bin: 4
- No non-monotone overlap-bin signatures with at least two populated bins were observed.

## Selector guardrail

- Selector stress produced no certification-rescue or family-certification-resilience events.

## RAKB caution

The native-overlap calculation is an operational bridge, not yet a derived BDG-LLC law. The intended RA-native claim is structural: certification-level resilience should depend on member-witness distinctness, and native overlap is a candidate proxy for shared failure fate.
