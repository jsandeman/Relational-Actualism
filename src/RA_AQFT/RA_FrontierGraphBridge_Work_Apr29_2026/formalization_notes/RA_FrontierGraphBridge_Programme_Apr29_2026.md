# RA Frontier/Graph Bridge Programme — Apr 29 2026

This note records the next theorem step after the compile-confirmed selector and frontier/incidence scaffolds.

## Purpose

The previous formalization files established:

- `RA_ActualizationSelector_v1.lean`: abstract selector vocabulary and weak selector closure.
- `RA_FrontierIncidence_v1.lean`: abstract candidate past, frontier, incidence sign, boundary ledger, and weak frontier selector closure.

`RA_FrontierGraphBridge_v1.lean` begins the bridge from that abstract vocabulary to the concrete graph-core layer:

- `ActualizationGraph`
- `CausalCut`
- `satisfies_local_ledger`
- `boundary_flux`
- `RA_graph_cut_theorem`

## Conceptual result

The graph-cut theorem can be re-expressed as a frontier-boundary ledger statement:

```text
local LLC on the left side of a causal cut
  ⇒ zero net charge flux across the cut
  ⇒ conserved boundary ledger at the frontier/cut layer
```

This does not yet derive nonzero charge signs. It shows that the existing graph-core LLC theorem already lands naturally in the frontier/incidence language.

## Why this matters for Selector Closure

The Selector Closure theorem needs a concrete boundary object. This bridge suggests the object is:

```text
candidate past / downset
  + Hasse-style frontier
  + boundary incidence / ledger data
```

The new file still uses a conservative topological-order bridge and explicit downset certificates. The next hard step is to replace those certificates with the actual reachability/Hasse-frontier construction derived from the finite DAG.

## Theorem ladder position

```text
T1. Selector type                                compiled
T2. Weak selector closure                        compiled
T3. Constraint closure implies selector          compiled
T4. No actual-history quotient                   compiled abstractly
T5. Candidate normal form                        compiled abstractly
T6. Frontier/incidence normal form               compiled abstractly
T7. Graph-core frontier bridge                   new scaffold
T8. Concrete Hasse frontier / reachability       next hard target
T9. Incidence sign-source theorem                open
T10. Hard Selector Closure Theorem               open
```

## What remains open

1. Define concrete reachability in `ActualizationGraph`.
2. Define candidate past as causal closure of a one-vertex extension.
3. Define Hasse frontier as maximal elements of that closure.
4. Prove graph-cut/frontier compatibility without explicit downset certificates.
5. Derive signed incidence values on the local frontier.
6. Connect signed N1 boundary readout to the seven-value charge signature.
7. Prove uniqueness of the RA-native actualization selector below saturation.
