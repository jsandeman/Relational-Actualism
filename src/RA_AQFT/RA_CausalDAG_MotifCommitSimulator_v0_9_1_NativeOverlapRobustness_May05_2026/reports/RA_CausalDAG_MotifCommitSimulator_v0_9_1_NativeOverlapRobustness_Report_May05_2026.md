# RA Causal-DAG Motif-Commit Simulator v0.9.1 — Native Overlap Robustness / Ablation Report

## Status

v0.9.1 is an analysis-only robustness packet over v0.9 Native Certificate Overlap. It does not introduce a new Lean module and does not change the simulator's motif-commit, support-family, or certified-family semantics.

## Motivation

v0.9 canonical results showed that certification rescue decreases as native certificate-witness overlap increases. v0.9.1 audits that result by reweighting and ablating the overlap components in the v0.9 witness-overlap output tables.

## Analysis source

```text
analysis/ra_native_overlap_robustness_analysis.py
```

Inputs:

```text
ra_witness_overlap_components_v0_9.csv
ra_cert_rescue_by_native_overlap_v0_9.csv
ra_overlap_vs_external_correlation_comparison_v0_9.csv
ra_native_certificate_overlap_selector_guardrail_v0_9.csv
```

Outputs:

```text
component ablation
weight sensitivity
signal attribution
external-correlation alignment
endpoint audit
summary MD/CSV/JSON
```

## Packet-local validation

Unit tests passed:

```text
Ran 4 tests
OK
```

Packet-local analysis over the v0.9 demo outputs:

```text
component_rows = 480
ablation_monotone_pass_rate = 1.0
weight_sensitivity_monotone_pass_rate = 1.0
balanced_low_high_gap_mean = 0.076667
selector_guardrail_passed = True
```

These are validation-scale results, not canonical claims.

## Main diagnostic meanings

### Component ablation

The analysis removes one overlap component at a time and recomputes native-overlap bins. If removing a component weakens the low/high rescue gap, that component receives a positive importance score.

### Weight sensitivity

The analysis applies alternate profiles such as ledger-heavy, orientation-heavy, support/frontier-heavy, causal-past-heavy, and BDG/firewall-heavy profiles. This asks whether the monotone overlap/rescue relation survives reasonable reweightings.

### Endpoint audit

High-overlap native rows are compared with parent-shared baseline rows. Certification-rescue equality is the primary endpoint check; downstream marginal-rate residuals are reported separately.

### Selector guardrail

Selector-stress rows should not produce support/certification-family rescue. v0.9.1 reports this as a guardrail result.

## RAKB posture

The included RAKB proposals are marked pending canonical run. Promote only after running v0.9.1 against the committed canonical v0.9 outputs.

## Methodological caution

The v0.9.1 analysis is a robustness audit over simulator-native overlap proxies. It is not a BDG–LLC derivation of certificate overlap. Its best use is to guide the next anchoring step by identifying which native-overlap components appear to carry the certification-rescue signature.
