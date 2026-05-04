# RA Hasse Frontier FiniteMax — First Formalization Report

Date: 2026-04-29

`RA_HasseFrontier_FiniteMax_v1.lean` introduces the finite-enumeration certificate layer needed to derive topological-maximum frontier data.

## Static scan

```text
sorry: 0
admit: 0
axiom: 0
sha256: 8914ecba7f9b35ceb0eb4c5eb350bbec3c4115ede3421e868d8f3c10aa948a9e
```

## Main definitions

```text
ReachableUpperPastFinset
TopoMaxFromFinsetData
FiniteTopoMaxFrontierData
FiniteMaxHasseBoundaryPackage
```

## Main bridge definitions / theorems

```text
topoMaxCertificateOfFinsetData
topoMaxFrontierCertificateOfFiniteData
maximalCertificateOfFiniteData
coverOfFiniteData
frontierOfFiniteData
cutBoundaryPackageFromFiniteData
cutBoundaryFromFiniteData_qN1_seven
```

## What remains open

The file does not yet derive finite maxima. The next target is:

```text
finite exact enumeration + nonempty upper past
  → TopoMaxFromFinsetData
```

Once that is proved, Hasse-frontier covers will be closer to being derived from finite graph structure rather than supplied as certificate data.
