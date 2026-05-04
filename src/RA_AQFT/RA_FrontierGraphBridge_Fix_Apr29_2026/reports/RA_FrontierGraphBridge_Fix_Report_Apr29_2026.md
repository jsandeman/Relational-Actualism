# RA Frontier/Graph Bridge v1 — Lean Fix Report

Date: 2026-04-29

This packet fixes the first local compile errors reported for `RA_FrontierGraphBridge_v1.lean`.

## Fix 1 — finite graph vertex type

Original code attempted to build the `UniverseState.vertexFinite` field inline with:

```lean
vertexFinite := Fintype.ofFinset G.V.attach (...)
```

Lean inferred the wrong ambient type and expected a `Finset Vertex`, while `G.V.attach` has the subtype finset for vertices satisfying membership in `G.V`.

The fix separates the finite-subtype instance:

```lean
noncomputable def graphVertexFintype (G : _root_.ActualizationGraph) :
    Fintype (GraphVertex G) :=
  { elems := G.V.attach
    complete := by
      intro x
      simp }
```

and then constructs the `UniverseState` explicitly:

```lean
noncomputable def graphUniverseState (G : _root_.ActualizationGraph) : UniverseState :=
  ⟨GraphVertex G, graphVertexFintype G⟩
```

## Fix 2 — boundary ledger theorem name collision

The theorem:

```lean
GraphCutFrontierBridge.boundaryLedger_qN1_seven
```

called `boundaryLedger_qN1_seven` unqualified. Lean resolved this to the graph-bridge theorem currently being defined rather than the earlier frontier/incidence theorem.

The fix avoids the name collision by using the `BoundaryLedger` field directly:

```lean
(GraphCutFrontierBridge.boundaryLedger B h_ledger).qN1_seven
```

## Conceptual status

No conceptual content changed. This is only a Lean elaboration/name-resolution repair. The file remains a conservative graph-cut/frontier bridge scaffold.

## Local compile command

```bash
cd src/RA_AQFT
lake env lean RA_FrontierGraphBridge_v1.lean
lake build
```

