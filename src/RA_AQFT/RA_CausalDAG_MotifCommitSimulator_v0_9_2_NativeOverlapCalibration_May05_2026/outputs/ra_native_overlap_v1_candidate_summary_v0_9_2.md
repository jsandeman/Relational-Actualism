# RA v0.9.2 Native Overlap Calibration / Family-Semantics Audit

This analysis audits whether native-overlap certification rescue is carried uniformly across support-family semantics, and calibrates native-overlap bins against the v0.8.1 external certificate-correlation baseline.

## Summary

- version: 0.9.2
- input_dir: ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/outputs
- external_correlation_dir: ../RA_CausalDAG_MotifCommitSimulator_v0_8_1_CertCorrelationAnalysis_May05_2026/outputs
- native_rows: 10
- aggregate_rows: 375
- component_rows: 480
- semantics_rows: 4
- calibration_rows: 10
- mapping_rows: 4
- selector_guardrail_passed: True
- candidate_primary_family_semantics: augmented_exact_k
- semantics_score_augmented_exact_k: 0.431375
- semantics_score_at_least_k: 0.0
- zero_baseline_count_augmented_exact_k: 0
- zero_baseline_count_at_least_k: 0
- mean_external_calibration_residual_abs: 0.046424
- max_external_calibration_residual_abs: 0.128791
- v1_recommendation: use augmented_exact_k as primary signal-carrier; retain at_least_k as monotone guardrail semantics

## Interpretation guardrail

v0.9.2 is analysis-only. It does not promote any overlap weighting or family semantics to a derived RA law. It identifies candidate semantics and calibration diagnostics for the next BDG-LLC/native-certificate anchoring step.

## Recommended v1.0 posture

use augmented_exact_k as primary signal-carrier; retain at_least_k as monotone guardrail semantics