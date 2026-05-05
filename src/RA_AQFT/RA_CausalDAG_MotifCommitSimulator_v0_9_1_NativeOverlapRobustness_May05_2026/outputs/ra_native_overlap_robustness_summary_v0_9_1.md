# RA v0.9.1 Native Certificate-Overlap Robustness Summary

This analysis audits whether the v0.9 native witness-overlap signature survives component ablation and overlap-weight variation.

## Summary metrics

- version: 0.9.1
- input_dir: ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/outputs
- external_correlation_dir: ../RA_CausalDAG_MotifCommitSimulator_v0_8_1_CertCorrelationAnalysis_May05_2026/outputs
- component_rows: 480
- native_overlap_rows: 10
- ablation_rows: 48
- weight_sensitivity_rows: 36
- ablation_monotone_pass_rate: 1.0
- weight_sensitivity_monotone_pass_rate: 1.0
- balanced_low_high_gap_mean: 0.05756916666666667
- balanced_low_high_gap_min: 0.0
- balanced_low_high_gap_max: 0.175109
- endpoint_rescue_max_delta_native_minus_parent: 0.5
- endpoint_resilience_max_delta_native_minus_parent: 0.666667
- selector_guardrail_passed: True
- selector_rows: 2

## Top component-attribution rows

- mode=ledger_failure semantics=at_least_k component=support score=0.0
- mode=ledger_failure semantics=at_least_k component=frontier score=0.0
- mode=ledger_failure semantics=at_least_k component=orientation score=0.0
- mode=ledger_failure semantics=at_least_k component=ledger score=0.0
- mode=ledger_failure semantics=at_least_k component=causal_past score=0.0
- mode=ledger_failure semantics=at_least_k component=bdg_kernel score=0.0
- mode=ledger_failure semantics=at_least_k component=firewall score=0.0
- mode=ledger_failure semantics=augmented_exact_k component=support score=0.0

## Interpretation guardrail

This packet is analysis-only. It does not promote the overlap weights to a derived RA law. Its role is to test whether the v0.9 native-overlap signature is robust enough to guide the next native/BDG-LLC anchoring step.