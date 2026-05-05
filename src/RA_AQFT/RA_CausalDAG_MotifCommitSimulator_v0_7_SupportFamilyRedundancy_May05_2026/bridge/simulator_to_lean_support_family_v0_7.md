# Simulator-to-Lean Bridge — v0.7 Support-Family Redundancy

## Lean declarations

```text
GraphSupportCutFamily
GraphFamilyReadyAt
GraphCertifiedFamilyReadyAt
GraphFamilyCommitsAt
GraphFamilyReadyAt_singleton_iff
```

## Simulator objects

```text
SupportCutFamily
threshold_support_family
family_ready_at
strict_ready_at
evaluate_support_family
```

## Correspondence

```text
GraphSupportCut G
  ↔ SupportCut = frozenset[node_id]

GraphSupportCutFamily G
  ↔ SupportCutFamily.cuts

GraphFamilyReadyAt G F x
  ↔ family_ready_at(dag, family, site)

GraphSingletonSupportCutFamily Q
  ↔ threshold_support_family(motif, 1.0), when family size is one

GraphFamilyCommitsAt
  ↔ support-family survival proxy in v0.7 outputs
```

The simulator uses threshold subfamilies as one concrete support-family generator. This is not the only possible RA-native family semantics.

## Main semantic distinction

```text
Strict support cut:
  all vertices in one Q are required

Support-cut family:
  at least one certified Qᵢ in F is ready
```

This is the formal reason v0.7 can treat support breadth as genuine redundancy, while v0.6 support width alone remained a conjunctive exposure surface.
