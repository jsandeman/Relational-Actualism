# RA Graph Orientation Chart Programme — Apr 29 2026

This note documents the next formal rung after `RA_IncidenceSignSource_v1.lean`.

## Purpose

`RA_IncidenceSignSource_v1` showed that a deterministic frontier orientation chart induces the incidence sign source needed for the seven-value N1 charge ledger.

`RA_GraphOrientationChart_v1.lean` moves one rung upward:

```text
graph-native orientation data
  -> FrontierOrientationChart
  -> IncidenceSignSource
  -> signed three-direction N1 frame
  -> seven-value charge ledger
```

The key point is methodological: incidence signs are no longer treated as sampled labels. They are deterministic functions of orientation data.

## What remains open

The file still receives `GraphOrientationData` as supplied data. The next hard theorem is:

```text
finite Hasse frontier
  + concrete RA causal-orientation asymmetry
  + D1 ledger-orientation preservation
  -> GraphOrientationClosure
```

That theorem should connect this scaffold to existing RA orientation files such as `RA_CausalOrientation_Core.lean` and `RA_D1_NativeLedgerOrientation_v1.lean`.

## Relation to the Selector Closure programme

This rung supports:

- RA-native actualization selector work,
- no primitive randomness,
- topological/incidence ledger derivation,
- edge-level signed N1 charge source,
- frontier/incidence normal form.

It does not yet prove the hard Selector Closure Theorem.
