# Simulator-to-RAKB Bridge: v0.8.1 Certification-Correlation Analysis

This bridge maps v0.8.1 outputs to proposed RAKB claims.

## Core analysis artifacts

```text
ra_cert_rescue_decay_curve_v0_8_1.csv
  pointwise correlation-rescue curves

ra_cert_correlation_sensitivity_v0_8_1.csv
  monotonicity, decay, slope, half-decay point, AUC

ra_cert_endpoint_equivalence_v0_8_1.csv
  comparison of independent_member at correlation=1.0 with parent_shared certification

ra_cert_resilience_auc_by_mode_v0_8_1.csv
  mode-level aggregate curve strength

ra_cert_rescue_by_width_and_threshold_v0_8_1.csv
  width- and threshold-conditioned signatures

ra_cert_selector_guardrail_v0_8_1.csv
  selector-stress separation guardrail
```

## Proposed claims

```text
RA-SIM-CERT-CORRELATION-001
  Certification rescue decays as certificate-correlation increases.

RA-SIM-CERT-CORRELATION-002
  The correlation=1.0 endpoint recovers the parent-shared certification failure shape.

RA-SIM-CERT-CORRELATION-003
  Rescue AUC and sensitivity metrics quantify certification-witness redundancy.

RA-SIM-CERT-CORRELATION-004
  Selector stress remains outside certification-family rescue.
```

## Promotion rule

Use packet-local outputs only as demonstration artifacts.  Promote claims only after re-running v0.8.1 on the canonical v0.8 output directory.
