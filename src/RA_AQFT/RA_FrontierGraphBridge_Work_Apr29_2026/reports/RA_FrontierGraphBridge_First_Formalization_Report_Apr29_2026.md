# RA Frontier/Graph Bridge — First Formalization Report

Generated: Apr 29 2026

## File

```text
src/RA_AQFT/RA_FrontierGraphBridge_v1.lean
```

SHA-256:

```text
6dc2682cb0fbe54cacf28dbe108a6aebab0d6bdc66d953de9d72cea53be33cc5
```

## Status

Static status before local Lean check:

```text
static_no_sorry_no_admit_no_axiom_build_pending
```

The file was statically checked for executable `sorry`, `admit`, and `axiom`; none are present. It has not been locally compiled in this environment.

## Imports

```lean
import RA_FrontierIncidence_v1
import RA_GraphCore
```

This means the file should be compiled via Lake, not as an isolated loose file.

## Main definitions

- `GraphVertex`
- `graphUniverseState`
- `topoOrderCausalOrder`
- `CutDownsetCertificate`
- `candidatePastOfCut`
- `cutBoundaryCharge`
- `boundaryLedgerOfCut`
- `GraphCutFrontierBridge`
- `GraphCutFrontierBridge.boundaryData`

## Main lemmas / theorem bridges

- `graph_edge_forward_in_topo_order`
- `cut_no_backward_edge_downset`
- `cutBoundaryCharge_zero`
- `zero_sevenCharge`
- `GraphCutFrontierBridge.boundaryCharge_zero`
- `GraphCutFrontierBridge.boundaryLedger_qN1_seven`

## Interpretation

This file re-expresses the existing graph-core cut theorem as a frontier-boundary ledger statement:

```text
local LLC on cut-left vertices
  ⇒ zero graph-core boundary flux
  ⇒ conserved frontier ledger
```

This is a bridge theorem layer, not the hard Selector Closure theorem.

## Compile instructions

Copy into the Lean source directory:

```bash
cp RA_FrontierGraphBridge_v1.lean src/RA_AQFT/
```

Add as a Lake root after the selector/frontier roots:

```lean
`RA_ActualizationSelector_v1,
`RA_FrontierIncidence_v1,
`RA_FrontierGraphBridge_v1,
```

Then run:

```bash
cd src/RA_AQFT
lake env lean RA_FrontierGraphBridge_v1.lean
lake build
```

## Caveats

- The file uses a conservative `topoOrderCausalOrder`, not yet the physical reachability order.
- The conversion from cut to candidate past requires an explicit `CutDownsetCertificate`.
- Nonzero local signed charges are not derived here; the bridge proves zero total cut flux under LLC.
- The next hard theorem is concrete reachability/Hasse-frontier construction.
