# RA Hasse Frontier Programme — April 29, 2026

## Purpose

`RA_HasseFrontier_v1.lean` is the next rung in the Selector Closure theorem ladder.  It begins replacing arbitrary parent-list descriptions with graph-native reachability, downset, and Hasse-frontier objects.

The guiding idea is:

```text
candidate actualization
  = graph-native candidate past / downset
  + maximal Hasse frontier
  + boundary/incidence ledger data
```

This is not a proof of the hard Selector Closure Theorem.  It is a normalization step: it makes explicit the graph object on which a future selector and charge/ledger sign-source should live.

## Main formal objects

The file defines:

```text
Step G a b
Reachable G a b
reachableCausalOrder G
HasseCandidatePast G
IsHasseFrontier P v
HasseFrontierCover P
frontierOfHassePast P cover
HasseBoundaryPackage P
cutHasseBoundaryPackage cover h_ledger
```

## Main lemmas

The file proves:

```text
step_topo_lt
reachable_trans
reachable_eq_or_topo_lt
step_reachable
graph_edge_reachable
cut_down_closed_reachable
cutReachabilityDownsetCertificate
hasse_frontier_in_past
hasse_frontier_maximal
cutHasseBoundary_qN1_seven
```

The crucial bridge theorem is:

```text
cut_down_closed_reachable
```

It upgrades the graph-core `CausalCut.no_backward` condition from one-step edges to full reachability.  This means a causal cut is a true downset for the concrete reachability order.

## What remains hard

The file still assumes a frontier-cover certificate:

```text
HasseFrontierCover P
```

The next theorem step should derive this from finiteness/nonemptiness of candidate pasts.  After that, the programme can move toward oriented frontier links and signed incidence coefficients.

Suggested next file:

```text
RA_HasseFrontier_Maximal_v1.lean
```

Targets:

1. Prove maximal-frontier existence for finite nonempty downsets.
2. Define Hasse boundary links / frontier incidence links.
3. Begin deriving signed incidence coefficients from oriented frontier data.
4. Connect the topological ledger rule to the graph-native frontier object.

## Theorem ladder status

```text
T1. Selector type                                  compiled
T2. Weak selector closure                          compiled
T3. Constraint closure implies selector            compiled
T4. No actual-history quotient                     compiled abstractly
T5. Candidate normal form                          compiled abstractly
T6. Frontier/incidence normal form                 compiled
T7. Graph-core frontier bridge                     compiled warning-free
T8. Hasse frontier / downset derivation            started here
T9. Incidence sign-source theorem                  open
T10. Hard Selector Closure Theorem                 open
```
