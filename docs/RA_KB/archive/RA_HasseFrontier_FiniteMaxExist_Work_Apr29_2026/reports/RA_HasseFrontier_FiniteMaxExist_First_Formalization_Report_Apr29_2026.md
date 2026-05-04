# RA_HasseFrontier_FiniteMaxExist_v1 — First Formalization Report

## Status

Generated as the next Lean scaffold in the Selector Closure theorem ladder after the successful build of `RA_HasseFrontier_FiniteMax_v1.lean`.

Static scan:

```text
sorry: 0
admit: 0
axiom: 0
```

Local Lean compile is pending user verification.

## Conceptual advance

Earlier files supplied frontier-cover and finite-maximum certificates.  This file uses finite graph data to derive the topological-maximum certificate directly from an exact finite enumeration of the reachable upper past.

The core constructor is:

```lean
noncomputable def topoMaxFromReachableUpperPastFinset
```

which takes:

```text
F : ReachableUpperPastFinset P x
hx : P.contains x
```

and constructs:

```text
TopoMaxFromFinsetData F
```

by taking the maximum of the finite set of `topo_order` values.

## Relation to Selector Closure

This file moves the theorem ladder from a supplied-certificate statement toward a graph-native existence result:

```text
finite DAG structure
  → finite reachable-upper-past enumeration
  → maximal Hasse frontier
  → frontier boundary package
```

The hard Selector Closure Theorem remains open, but the frontier-existence layer is now sharply isolated.

## Next target

The next file should attack the incidence-sign problem:

```text
RA_IncidenceLedger_v1.lean
```

with definitions for oriented frontier links, incidence signs, N1 boundary projection, and the conditional seven-value signed charge theorem.
