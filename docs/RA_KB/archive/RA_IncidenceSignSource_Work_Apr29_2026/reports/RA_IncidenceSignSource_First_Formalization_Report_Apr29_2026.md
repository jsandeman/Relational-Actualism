# RA Incidence Sign Source first formalization report — Apr 29 2026

`RA_IncidenceSignSource_v1.lean` is an exploratory formalization scaffold for the graph-native incidence sign-source problem.

## Imports

```lean
import RA_IncidenceCharge_v1
```

## Main definitions

```text
FrontierOrientationChart
signSourceOfOrientationChart
OrientedN1ThreeFrame
signedThreeFrameOfOrientationChart
OrientedIncidenceBoundary
threeDirectionalBoundaryOfOrientation
ledgerOfOrientedIncidenceBoundary
boundaryDataOfOrientedIncidenceBoundary
```

## Main lemmas

```text
signSourceOfOrientationChart_eval
orientationChart_sign_deterministic
signedThreeFrameOfOrientationChart_qN1_seven
threeDirectionalBoundaryOfOrientation_qN1_seven
ledgerOfOrientedIncidenceBoundary_qN1_seven
```

## Status

Static source scan:

```text
sorry: 0
admit: 0
axiom: 0
```

Local Lean compile remains pending.

## Interpretation

This file does not derive the physical sign-source. It shows that a deterministic frontier orientation chart is sufficient to construct the incidence sign-source and recover the seven-value signed N1 charge ledger.

The next theorem target is:

```text
finite Hasse frontier + RA-native causal/orientation data
  -> FrontierOrientationChart
```
