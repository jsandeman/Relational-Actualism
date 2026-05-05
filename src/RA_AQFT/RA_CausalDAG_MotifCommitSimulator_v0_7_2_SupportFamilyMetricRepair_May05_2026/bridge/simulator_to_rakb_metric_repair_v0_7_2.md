# Simulator-to-RAKB Bridge — v0.7.2 Support-Family Metric Repair

This bridge note records the intended RAKB interpretation of v0.7.2.

## Core correction

v0.7.2 repairs the interpretation of certification-channel support-family metrics. The parent support cut and exact-k family members can live in different intervention-targeting domains when the parent cut is absent from `family.cuts`.

Therefore:

```text
strict_parent_loss_rate and family_internal_loss_rate are not automatically comparable.
```

The packet introduces:

```text
comparison_valid_strict_vs_family
metric_artifact_risk
family_internal_resilience_event
apples_to_apples_loss_delta
```

## RAKB claim intent

The proposed claims should be treated as simulation-methodology / analysis claims, not Nature-level claims.

The central corrected claim is:

```text
Certification-channel support-family resilience must be measured with family-internal and parent-in-family-aware metrics.
```

## Dependency interpretation

The packet depends on:

```text
RA-MOTIF-SUPPORT-FAMILY-001..002
RA-MOTIF-SUPPORT-FAMILY-MONO-001..002
RA-SIM-SUPPORT-FAMILY-001..003
RA-SIM-SUPPORT-FAMILY-MONO-001..003
```

It does not add a new Lean theorem. The Lean monotonicity layer already covers the formal family-inclusion no-worse principle.
