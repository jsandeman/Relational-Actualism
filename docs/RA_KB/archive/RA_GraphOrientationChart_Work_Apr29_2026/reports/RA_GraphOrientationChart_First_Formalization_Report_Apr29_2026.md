# RA Graph Orientation Chart — First Formalization Report

Generated: Apr 29 2026

## Artifact

`RA_GraphOrientationChart_v1.lean`

## Import chain

```lean
import RA_IncidenceSignSource_v1
```

Expected compiled predecessor chain:

```text
RA_ActualizationSelector_v1
  -> RA_FrontierIncidence_v1
  -> RA_FrontierGraphBridge_v1
  -> RA_HasseFrontier_v1
  -> RA_HasseFrontier_Maximal_v1
  -> RA_HasseFrontier_FiniteMax_v1
  -> RA_HasseFrontier_FiniteMaxExist_v1
  -> RA_IncidenceCharge_v1
  -> RA_IncidenceSignSource_v1
```

## Definitions introduced

- `OrientationPolarity`
- `OrientationPolarity.toSign`
- `GraphOrientationData`
- `orientationChartOfGraphData`
- `signSourceOfGraphOrientationData`
- `GraphOrientedN1Boundary`
- `orientedIncidenceBoundaryOfGraphData`
- `threeDirectionalBoundaryOfGraphData`
- `ledgerOfGraphOrientedBoundary`
- `boundaryDataOfGraphOrientedBoundary`
- `GraphOrientationClosure`
- `signSourceOfGraphOrientationClosure`

## Main lemmas/theorems

- `orientationChartOfGraphData_eval`
- `orientationChartOfGraphData_coherent`
- `signSourceOfGraphOrientationData_eval`
- `graphOrientation_sign_deterministic`
- `threeDirectionalBoundaryOfGraphData_qN1_seven`
- `ledgerOfGraphOrientedBoundary_qN1_seven`
- `signSourceOfGraphOrientationClosure_eval`

## Static scan

The generated file contains no executable `sorry`, `admit`, or `axiom` declarations by text scan.

## Status

Recommended pre-build status:

```text
static_no_sorry_no_admit_no_axiom_build_pending
```

After local Lean/Lake success:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
```

## Conceptual status

This file is a scaffold. It does not derive the physical graph orientation yet. It shows that once RA-native graph orientation data is supplied, the sign-source and seven-value charge ledger are deterministic.
