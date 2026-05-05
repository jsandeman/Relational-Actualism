# RA Causal-DAG Motif-Commit Simulator v0.8 — Independent Certified Families Report

## Summary

v0.8 extends the support-family line from support-route redundancy to certification-witness redundancy.

The prior v0.7.2 correction showed that strict-parent rescue, family-internal resilience, and apples-to-apples loss deltas are different quantities. v0.8 uses that discipline and asks whether ledger/orientation certification failure can be rescued when support-family members carry member-distinct certificate fates.

## New simulator layer

New module:

```text
simulator/ra_causal_dag_independent_cert_families.py
```

The module compares:

```text
parent_shared
cut_level
independent_member
```

and sweeps:

```text
certificate_correlation ∈ [0, 1]
```

The independent-member regime is deliberately exploratory. It models certificate fates as a mixture between independent per-member failure and shared family-level failure, preserving severity as each certificate's marginal failure probability.

## Packet-local validation

```text
Ran 6 tests
OK
```

The tests verify:

```text
parent_shared certification fails all-or-none
independent_member can leave family alternatives when the strict parent certificate fails
full correlation matches shared-fate shape at severity 1
selector_stress is not counted as certification rescue
correlation sweep decreases rescue in a small controlled demo
end-to-end output generation
```

## Packet-local demo result

```text
actual_evaluations = 8,640
support_width_classes = [1, 2, 4]
certification_regimes = [cut_level, independent_member, parent_shared]
certificate_correlations = [0.0, 0.5, 1.0]
certification_rescues = 56
family_certification_resilience_events = 718
metric_artifact_risk_events = 0
mean_valid_apples_to_apples_loss_delta = -0.012731
```

## Interpretation

The packet-local run shows that certification rescue can appear only once the simulator gives family members member-level certificate fates. This is the intended v0.8 diagnostic.

The operational result should be interpreted carefully:

```text
support-family route redundancy
  ≠ certification-witness redundancy
```

and:

```text
member-distinct certificates are required before ledger/orientation failure can be rescued by a family member alternative.
```

## Lean bridge status

The Lean bridge is source-level pending local compile. I could not run Lean/Lake in this environment.

Source audit:

```text
sorry/admit/axiom = 0
```

The bridge is intentionally abstract and proof-light:

```text
DAGFamilyCertificateContext
DAGIndependentCertifiedFamilyReadyAt
GraphFamilyCertificateContext
GraphIndependentCertifiedFamilyReadyAt
```

with conversion theorems into the existing certified family readiness layer.

## Next canonical criteria

On canonical scale, check:

```text
independent_member certification_rescue_rate > parent_shared certification_rescue_rate
certification_rescue_rate decreases with certificate_correlation
selector_guardrail_passed remains true
the support-width classes remain > 1
```
