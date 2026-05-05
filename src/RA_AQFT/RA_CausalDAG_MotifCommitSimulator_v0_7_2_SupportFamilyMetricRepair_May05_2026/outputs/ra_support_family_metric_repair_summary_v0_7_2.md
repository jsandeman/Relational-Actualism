# RA Support-Family Metric Repair — v0.7.2

This analysis layer repairs the v0.7/v0.7.1 metric interpretation. It separates strict-parent rescue from family-internal survival and flags invalid cross-domain comparisons.

## Scale

- run_count: 100
- steps: 32
- actual_evaluations: 1728000
- support_width_classes: [1, 2, 3, 4]
- comparison_valid_rate: 0.981875
- metric_artifact_risk_rate: 0.0145

## Corrected interpretation

`strict_parent_loss_rate` and `family_internal_loss_rate` are not automatically comparable. In cut-level certification modes, exact-k families with the parent cut absent from family.cuts put the strict parent and the family members in different targeting domains.

The correct family-internal question is whether some family member remains certified-ready under family-targeted stress. The correct strict-rescue question is whether the strict parent cut fails while a family member survives. These are distinct diagnostics.

## Highest family-internal certification survival rows

- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.25 threshold=0.25 width=2 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.25 threshold=0.25 width=3 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.25 threshold=0.25 width=4 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.25 threshold=0.5 width=2 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.25 threshold=0.5 width=3 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.25 threshold=0.5 width=4 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.25 threshold=0.75 width=4 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.5 threshold=0.25 width=2 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.5 threshold=0.25 width=3 survival=1.0 loss=0.0 risk=0.0
- mode=ledger_failure semantics=at_least_k regime=cut_level sev=0.5 threshold=0.25 width=4 survival=1.0 loss=0.0 risk=0.0

## Invalid strict-vs-family comparison flags

- mode=ledger_failure semantics=exact_k severity=0.25 threshold=0.25 samples_at_risk=1346 widths=[2, 3, 4]
- mode=ledger_failure semantics=exact_k severity=0.25 threshold=0.5 samples_at_risk=1346 widths=[2, 3, 4]
- mode=ledger_failure semantics=exact_k severity=0.5 threshold=0.25 samples_at_risk=1346 widths=[2, 3, 4]
- mode=ledger_failure semantics=exact_k severity=0.5 threshold=0.5 samples_at_risk=1346 widths=[2, 3, 4]
- mode=ledger_failure semantics=exact_k severity=0.75 threshold=0.25 samples_at_risk=1346 widths=[2, 3, 4]
- mode=ledger_failure semantics=exact_k severity=0.75 threshold=0.5 samples_at_risk=1346 widths=[2, 3, 4]
- mode=ledger_failure semantics=exact_k severity=1.0 threshold=0.25 samples_at_risk=1346 widths=[2, 3, 4]
- mode=ledger_failure semantics=exact_k severity=1.0 threshold=0.5 samples_at_risk=1346 widths=[2, 3, 4]
- mode=orientation_degradation semantics=exact_k severity=0.25 threshold=0.25 samples_at_risk=1346 widths=[2, 3, 4]
- mode=orientation_degradation semantics=exact_k severity=0.25 threshold=0.5 samples_at_risk=1346 widths=[2, 3, 4]

## RAKB caution

The corrected claim is not that exact-k support families amplify certification failure. The corrected claim is that cross-threshold comparisons require width-stratified, parent-in-family-aware, apples-to-apples metrics. Certification resilience is a family-internal diagnostic unless the parent cut and family members share the same targeting domain.
