# RA Causal-DAG Motif-Commit Simulator v0.9.1 — Native Overlap Robustness / Ablation

Date: May 5, 2026

This packet is a **pure analysis layer** over v0.9 Native Certificate Overlap. It introduces no new Lean module and does not alter simulator semantics.

## Purpose

v0.9 showed that certification rescue decreases as native certificate-witness overlap increases. v0.9.1 audits whether that signature is robust under alternate interpretations of the overlap components already emitted by v0.9.

The RA-native hypothesis under audit remains:

```text
certification rescue decreases as native certificate-witness overlap increases
```

v0.9.1 asks:

1. does the low/medium/high native-overlap signature survive weight-profile variation?
2. which native witness-overlap components contribute most to the low/high rescue gap?
3. do high-overlap native rows retain the certification-rescue endpoint relation to the parent-shared baseline?
4. does selector stress remain outside support/certification-family rescue?

## New analysis module

```text
analysis/ra_native_overlap_robustness_analysis.py
```

This module reads v0.9 output CSVs, especially:

```text
ra_witness_overlap_components_v0_9.csv
ra_cert_rescue_by_native_overlap_v0_9.csv
ra_overlap_vs_external_correlation_comparison_v0_9.csv
ra_native_certificate_overlap_selector_guardrail_v0_9.csv
```

and computes derived diagnostics.

This module does **not** rerun v0.9. It reweights and re-bins v0.9's component-overlap rows to audit robustness of the native-overlap proxy signature.

## Outputs

```text
ra_native_overlap_robustness_summary_v0_9_1.csv
ra_native_overlap_component_ablation_v0_9_1.csv
ra_native_overlap_weight_sensitivity_v0_9_1.csv
ra_native_overlap_signal_attribution_v0_9_1.csv
ra_native_overlap_external_correlation_alignment_v0_9_1.csv
ra_native_overlap_crn_endpoint_audit_v0_9_1.csv
ra_native_overlap_robustness_summary_v0_9_1.md
ra_native_overlap_robustness_state_v0_9_1.json
```

## Packet-local validation

Unit tests:

```text
Ran 4 tests
OK
```

Packet-local analysis over the packet-local v0.9 demo outputs:

```text
component_rows = 480
ablation_monotone_pass_rate = 1.0
weight_sensitivity_monotone_pass_rate = 1.0
balanced_low_high_gap_mean = 0.076667
selector_guardrail_passed = True
```

The packet-local outputs are not canonical; they validate analysis machinery.

## Usage

Run against canonical v0.9 outputs:

```bash
python scripts/run_native_overlap_robustness_v0_9_1.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/outputs \
  --output-dir outputs
```

Optional external-correlation comparison using v0.8.1 outputs:

```bash
python scripts/run_native_overlap_robustness_v0_9_1.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/outputs \
  --external-correlation-dir ../RA_CausalDAG_MotifCommitSimulator_v0_8_1_CertCorrelationAnalysis_May05_2026/outputs \
  --output-dir outputs
```

## Interpretation guardrail

The overlap weights and component ablations are operational diagnostics. They should not be treated as a derived BDG–LLC law. Their role is to test whether the v0.9 native-overlap proxy is robust enough to guide the next native/BDG–LLC anchoring step.
