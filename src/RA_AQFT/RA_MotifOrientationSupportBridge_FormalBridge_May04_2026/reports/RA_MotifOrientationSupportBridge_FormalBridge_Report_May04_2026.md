# RA Motif Orientation Support Bridge — Formal Report

Date: May 4, 2026

## Purpose

`RA_MotifOrientationSupportBridge` connects the compile-confirmed motif-commit and selector-closure layers to the existing graph-orientation closure scaffold. The bridge remains certificate-level: it names the support witnesses and conflict witnesses needed to treat orientation closure as an RA-native source of motif support, readiness, selected commitment, and unresolved incompatibility.

## RA-native ladder

```text
graph-native candidate past P
  → finite Hasse-frontier support cut
  → graph-orientation closure certificate
  → graph-oriented motif support witness W
  → W.certified Q
  → GraphOrientationSupports G M Q
  → GraphOrientationActualizationContext.toCommitContext
  → certified readiness at site x
  → orientation selector closure
  → selected commitment
  → strict commitment under selector completeness
```

## Central support witness

The central declaration is:

```lean
GraphOrientedMotifSupport M P
```

It packages:

```text
a graph-orientation closure certificate for P
carrier-in-candidate-past evidence for M
frontier sufficiency obligation
local ledger compatibility obligation
```

Certification is then:

```lean
GraphOrientedMotifSupport.certified W Q
```

which requires:

```text
frontier_sufficient_for_motif
local_ledger_compatible
closure.selector_compatible
closure.no_extra_random_labels
closure.nativeEvidence.no_particle_label_primitives
Q = supportCutOfFiniteHasseFrontier P
```

This prevents an arbitrary finite support cut from becoming motif support evidence merely because it was named.

## Key readiness bridge

```lean
GraphOrientedMotifSupport.ready_iff_frontier_reaches_site
```

Meaning:

```text
For a certified graph-oriented support witness,
readiness at site x is equivalent to reachability from every Hasse-frontier
support vertex of P to x.
```

This reuses the existing finite-Hasse-frontier readiness theorem from `RA_MotifCommitProtocol` while inserting orientation closure as the support-certification source.

## Orientation/sign-source inheritance

The bridge also exposes the deterministic orientation consequences already supplied by `RA_GraphOrientationClosure`:

```lean
GraphOrientedMotifSupport.signSource
GraphOrientedMotifSupport.signSource_eval
GraphOrientedMotifSupport.ledger_qN1_seven
```

This does not add a new charge ontology. It states that a graph-oriented motif support witness inherits the deterministic incidence-sign and seven-value N1 ledger surfaces already compiled upstream.

## Selector bridge

The module defines:

```lean
GraphOrientationActualizationContext
GraphOrientationActualizationContext.toCommitContext
GraphOrientationSelectorClosureAt
GraphOrientationSelectedCommitsAt
```

and proves:

```lean
GraphOrientationSelectedCommitsAt.has_oriented_frontier_witness
GraphOrientationSelectedCommitsAt.to_strict_commits_of_complete
```

Meaning:

```text
Selected orientation-context commitment carries a graph-oriented support witness
and Hasse-frontier reachability; under complete selector closure it recovers the
strict graph commit predicate.
```

## Incompatibility discipline

The bridge introduces:

```lean
GraphOrientationConflictWitness
GraphOrientationActualizationContext.incompatibility_is_witnessed
GraphOrientationActualizationContext.incompatible_symmetric
GraphOrientationUnresolvedIncompatibilityAt.has_conflict_witness
```

So incompatibility in this layer is not an ungrounded label. It must be supported by a native graph-orientation conflict witness supplied by the context.

## Guardrail

The module is not a completed derivation of orientation support from raw graph data. It is a certificate-level bridge. The hard future theorem is:

```text
finite causal graph + Hasse frontier + orientation closure + local ledger constraints
  → certified GraphOrientedMotifSupport
```

## Validation status

This packet was generated in an environment without Lean/Lake installed, so the module is not independently compiled here. Source audit:

```text
sorry: 0
admit: 0
axiom: 0
```

Local validation target:

```bash
lake env lean RA_MotifOrientationSupportBridge.lean
lake build
```
