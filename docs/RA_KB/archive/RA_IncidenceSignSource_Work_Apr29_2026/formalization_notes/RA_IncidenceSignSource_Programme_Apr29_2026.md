# RA Incidence Sign Source programme — Apr 29 2026

This note documents the next safe theorem rung after `RA_IncidenceCharge_v1.lean`.

The goal is to move from:

```text
supplied three incidence signs
  -> seven-value N1 charge
```

to:

```text
supplied deterministic frontier orientation chart
  -> IncidenceSignSource
  -> signed three-direction frame
  -> seven-value N1 charge ledger
```

This still does **not** prove the hard topological sign-source theorem.  Instead, it isolates the next missing object:

```text
FrontierOrientationChart
```

The next hard target is to derive that chart from RA-native oriented frontier topology, likely by connecting to the existing causal-orientation and D1 ledger-orientation Lean layers.

Lean source SHA-256:

```text
a0a486ba343e7ee2dfed98882ad261415dced799e1c303fc3b5b5fe70a78d947
```
