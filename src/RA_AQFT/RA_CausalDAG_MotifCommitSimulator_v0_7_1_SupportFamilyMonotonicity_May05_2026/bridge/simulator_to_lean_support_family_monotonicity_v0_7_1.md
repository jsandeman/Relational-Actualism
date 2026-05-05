# Simulator-to-Lean Bridge — v0.7.1 Support-Family Monotonicity

Lean bridge:

```text
RA_MotifSupportFamilyMonotonicity.lean
```

Simulator module:

```text
simulator/ra_causal_dag_support_family_monotonicity.py
```

## Formal predicate correspondence

```text
DAGFamilyIncluded / GraphFamilyIncluded
  ↔ family_semantics includes all cuts from the base family

DAGFamilyReadyAt.mono_family / GraphFamilyReadyAt.mono_family
  ↔ no-worse behavior when a family is augmented by adding cuts

DAGCertifiedFamilyReadyAt.mono_family / GraphCertifiedFamilyReadyAt.mono_family
  ↔ certified readiness persists under family inclusion when the same witnessing cut remains certified

DAGFamilyCommitsAt.mono_family / GraphFamilyCommitsAt.mono_family
  ↔ family commitment persists under family inclusion when the same committed cut remains in the augmented family
```

## Simulator semantics

```text
exact_k
  Not generally an inclusion-based augmentation; it can remove the strict cut.

at_least_k
  Inclusion-based augmentation: lowering k adds cuts and preserves the full cut.

augmented_exact_k
  Minimal inclusion-based augmentation: exact-k plus the full strict cut.
```

## Certification regimes

```text
cut_level
  member cuts can fail independently.  This explores certification-surface amplification.

parent_shared
  one parent certificate gates all cuts.  This separates support-route redundancy from certification-level redundancy.
```

## Key caution

The formal monotonicity theorem is about family inclusion.  Exact-k threshold families are not generally monotone in this sense, so exact-k simulator behavior should not be treated as a no-worse redundancy theorem.
