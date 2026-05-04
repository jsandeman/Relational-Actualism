# RA Hasse Frontier Maximal Programme — Apr 29 2026

## Purpose

`RA_HasseFrontier_Maximal_v1.lean` is the next theorem step after the compiled graph-native Hasse frontier scaffold.

The goal is to move from:

```text
HasseFrontierCover supplied as explicit data
```

toward:

```text
finite nonempty downset in a DAG
  → maximal reachable vertices
  → Hasse frontier cover
```

This matters for the Selector Closure programme because a candidate actualization should eventually be represented by graph-native closure/frontier structure rather than arbitrary parent-list or simulator-measure choices.

## What v1 proves

The file introduces:

```text
ReachableUpperPast
MaximalReachableAbove
MaximalFrontierCertificate
TopoMaxCertificate
TopoMaxFrontierCertificate
MaximalHasseBoundaryPackage
```

and proves:

```text
MaximalReachableAbove → IsHasseFrontier
MaximalFrontierCertificate → HasseFrontierCover
TopoMaxCertificate → MaximalReachableAbove
TopoMaxFrontierCertificate → MaximalFrontierCertificate
TopoMaxFrontierCertificate → HasseFrontierCover
```

It also packages the conserved-cut zero-flux ledger through the new maximal-frontier layer.

## What remains hard

The central finite-existence theorem is still open:

```text
finite nonempty candidate past
  → TopoMaxFrontierCertificate
```

The expected proof strategy is:

1. For a fixed `x` in a finite candidate past `P`, form the finite set:

   ```text
   { v | P.contains v ∧ Reachable x v }
   ```

2. This set is nonempty because `x` itself is reachable from `x`.
3. Choose a vertex `f` in that set maximizing `G.topo_order`.
4. Use strict topological increase under nontrivial reachability to prove that any reachable same-past vertex above `f` must equal `f`.
5. Therefore `f` is a Hasse-frontier vertex.

The v1 file proves step 4 conditionally: a topological maximum certificate implies maximality.

## Why this is RA-relevant

The theorem clarifies the distinction between:

```text
classification / frontier normal form
```

and:

```text
ontological quotienting of actual histories
```

It supports the no-hidden-multiplicity principle without merging distinct actual histories. If two parent-list descriptions are merely redundant descriptions of the same closure/frontier object, they should not acquire separate physical weight. But if they encode distinct actual link histories, they remain distinct.

The next proof step should therefore derive the maximal frontier from the actual graph, not impose it as an equivalence-class quotient.
