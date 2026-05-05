# RA Causal-DAG Motif-Commit Simulator v0.8.1 — Certified-Support-Family Correlation Analysis

This packet is an **analysis-only** layer over v0.8 Independent Certified Support Families.

It does not change simulator semantics and introduces no new Lean module.  It consumes v0.8 outputs and extracts the RA-native certification-correlation signature:

```text
member-distinct / weakly correlated certification witnesses
  -> certification-channel resilience

fully shared certification fate
  -> parent-shared failure shape
```

## Inputs

Expected v0.8 output files:

```text
ra_independent_cert_family_aggregate_v0_8.csv
ra_certification_correlation_sweep_v0_8.csv
ra_certification_resilience_by_regime_v0_8.csv
ra_independent_cert_family_by_width_v0_8.csv
ra_independent_cert_selector_guardrail_v0_8.csv
ra_independent_cert_family_summary_v0_8.csv
```

## Outputs

```text
ra_cert_rescue_decay_curve_v0_8_1.csv
ra_cert_correlation_sensitivity_v0_8_1.csv
ra_cert_endpoint_equivalence_v0_8_1.csv
ra_cert_resilience_auc_by_mode_v0_8_1.csv
ra_cert_rescue_by_width_and_threshold_v0_8_1.csv
ra_cert_selector_guardrail_v0_8_1.csv
ra_cert_correlation_signature_summary_v0_8_1.md
ra_cert_correlation_analysis_state_v0_8_1.json
```

## Canonical run command

Run this against the canonical v0.8 output directory:

```bash
python scripts/run_cert_correlation_analysis_v0_8_1.py \
  --input-dir ../RA_CausalDAG_MotifCommitSimulator_v0_8_IndependentCertifiedFamilies_May05_2026/outputs \
  --output-dir outputs
```

The packet-local outputs are generated from the v0.8 demo files shipped in the prior packet, not from Joshua's 4,032,000-evaluation canonical run.

## Diagnostic criteria

The canonical v0.8 run reported the cleanest signature so far:

```text
certificate_correlation:       0.00 -> 0.25 -> 0.50 -> 0.75 -> 1.00
certification_rescue_rate:     0.221 -> 0.176 -> 0.121 -> 0.091 -> 0.000
```

v0.8.1 makes that pattern auditable through:

```text
monotone_nonincreasing
endpoint_parent_shared_equivalence
rescue_auc_normalized
rescue_decay
half_decay_correlation
width-conditioned rescue curves
selector-stress guardrail checks
```

## RAKB status recommendation

Do not promote the v0.8.1 claims from packet-local outputs.  Run the analysis on the canonical v0.8 outputs, then promote only the confirmed correlation-signature claims.

Suggested canonical criteria:

```text
monotone rescue decay holds for the certified-support-family signature curves;
certificate_correlation=1.0 matches parent-shared certification shape;
selector-stress guardrail remains true;
width/threshold-conditioned curves remain interpretable.
```
