# RA Causal-DAG Motif-Commit Simulator v0.9.2 — Native Overlap Calibration / Family-Semantics Audit

This packet is a pure analysis-layer follow-up to v0.9 and v0.9.1. It adds no Lean module and makes no simulator semantic changes.

## Purpose

v0.9 showed that certification rescue decreases as native certificate-witness overlap increases. v0.9.1 showed that the signal survives component ablation and overlap-weight perturbation, but it also revealed a family-semantics asymmetry: the strongest signal is carried by `augmented_exact_k`, while some `at_least_k` slices, especially `ledger_failure / at_least_k`, collapse to zero rescue.

v0.9.2 audits that asymmetry and calibrates native-overlap bins against the v0.8.1 external certificate-correlation baseline.

## Inputs

Expected v0.9 files:

- `ra_cert_rescue_by_native_overlap_v0_9.csv`
- `ra_native_certificate_overlap_aggregate_v0_9.csv`
- `ra_witness_overlap_components_v0_9.csv`
- `ra_native_certificate_overlap_selector_guardrail_v0_9.csv`

Optional v0.8.1 file:

- `ra_cert_rescue_decay_curve_v0_8_1.csv`

## Outputs

- `ra_native_overlap_semantics_audit_v0_9_2.csv`
- `ra_ledger_atleastk_zero_baseline_audit_v0_9_2.csv`
- `ra_native_overlap_calibration_curve_v0_9_2.csv`
- `ra_native_vs_external_correlation_mapping_v0_9_2.csv`
- `ra_family_semantics_signal_carriers_v0_9_2.csv`
- `ra_native_overlap_v1_candidate_summary_v0_9_2.csv`
- `ra_native_overlap_v1_candidate_summary_v0_9_2.md`
- `ra_native_overlap_calibration_state_v0_9_2.json`

## Canonical run

```bash
python scripts/run_native_overlap_calibration_v0_9_2.py   --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/outputs   --external-correlation-dir ../RA_CausalDAG_MotifCommitSimulator_v0_8_1_CertCorrelationAnalysis_May05_2026/outputs   --output-dir outputs
```

## Interpretive guardrail

v0.9.2 does not turn native-overlap weights or a support-family semantics into a derived RA law. It identifies which semantics and diagnostics are the best candidates for the later BDG–LLC/native-certificate anchoring step.
