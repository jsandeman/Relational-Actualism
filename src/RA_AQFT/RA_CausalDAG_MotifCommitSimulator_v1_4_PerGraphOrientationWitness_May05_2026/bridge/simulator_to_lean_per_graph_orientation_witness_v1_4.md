# Simulator-to-Lean Bridge: v1.4 Per-Graph Orientation Witness

Simulator rows build per-graph/member token sets. Lean represents the same idea abstractly through `DAGPerGraphOrientationWitnessContext` and `GraphPerGraphOrientationWitnessContext`.

The bridge theorem direction is:

```text
per-graph/member orientation witness
  -> native orientation catalog evidence
  -> orientation-link surface
  -> generic orientation component
```

No numerical overlap or rescue law is asserted in Lean.
