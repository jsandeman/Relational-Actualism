# RA Hasse Frontier FiniteMaxExist Programme — Apr 29 2026

This note records the next theorem rung in the Selector Closure programme.

## Purpose

`RA_HasseFrontier_FiniteMax_v1.lean` packaged finite enumeration data and a supplied topological maximum.  The new file `RA_HasseFrontier_FiniteMaxExist_v1.lean` begins discharging that certificate layer.

The central move is:

```text
finite actualization graph
  → exact finite enumeration of reachable upper pasts
  → finite topological maximum by Finset.max'
  → TopoMaxFromFinsetData
  → FiniteTopoMaxFrontierData
  → HasseFrontierCover
```

This is the first point where the Hasse-frontier cover is derived from finite graph data rather than supplied as a global certificate.

## What is proven

The file defines and proves/constructs:

```text
reachableUpperPastFinsetOfFiniteGraph
topoMaxFromReachableUpperPastFinset
finiteTopoMaxFrontierDataOfFiniteGraph
topoMaxFrontierCertificateOfFiniteGraph
maximalCertificateOfFiniteGraph
coverOfFiniteGraph
frontierOfFiniteGraph
cutBoundaryPackageFromFiniteGraph
cutBoundaryFromFiniteGraph_qN1_seven
```

The proof is intentionally modest: it uses the finite subtype of vertices carried by `ActualizationGraph`, filters it to the exact reachable upper past, maps each vertex to `topo_order`, and takes a maximum value over the finite set of natural numbers.

## What remains open

This closes the finite maximum existence rung, but it does not yet derive nonzero charge signs.  The next theorem target is the incidence-sign theorem:

```text
finite Hasse frontier
  + oriented boundary/incidence structure
  → signed N1 edge contributions
  → seven-value charge as topological boundary projection
```

This is the point where the actualization-selector programme and the topological ledger/charge rule should begin to merge.
