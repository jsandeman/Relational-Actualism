# RA Hasse Frontier Maximal v1 — First Formalization Report

## Summary

`RA_HasseFrontier_Maximal_v1.lean` is a conservative scaffold for the next stage of the Selector Closure theorem ladder.

It imports:

```lean
import RA_HasseFrontier_v1
```

and formalizes the certificate layer needed to derive Hasse-frontier covers from topological maximality in finite candidate pasts.

## Status

Static scan result:

```text
sorry: 0
admit: 0
axiom: 0
```

Local Lean compile status before user check:

```text
build pending
```

Suggested initial RAKB status:

```text
static_no_sorry_no_admit_no_axiom_build_pending
```

After successful local build, update to:

```text
lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
```

## Main definitions

```text
ReachableUpperPast
MaximalReachableAbove
MaximalFrontierCertificate
TopoMaxCertificate
TopoMaxFrontierCertificate
MaximalHasseBoundaryPackage
```

## Main lemmas

```text
reachableUpperPast_self
maximalReachableAbove_isFrontier
coverOfMaximalCertificate
frontierOfMaximalCertificate
maximalCertificate_frontier_in_past
maximalCertificate_frontier_maximal
maximalReachableAboveOfTopoMax
maximalCertificateOfTopoMax
coverOfTopoMaxCertificate
frontierOfTopoMaxCertificate
boundaryDataOfMaximalHassePackage
cutBoundaryPackageFromMaximal
cutBoundaryFromMaximal_qN1_seven
```

## Conceptual role

This file proves that topological maximality certificates are enough to produce Hasse-frontier covers. It does not yet prove that such certificates exist for all finite nonempty candidate pasts. That proof is the next theorem target.

## Theorem ladder position

```text
T1. Selector type                                  compiled
T2. Weak selector closure                          compiled
T3. Constraint closure implies selector            compiled
T4. No actual-history quotient                     compiled abstractly
T5. Candidate normal form                          compiled abstractly
T6. Frontier/incidence normal form                 compiled
T7. Graph-core frontier bridge                     compiled warning-free
T8. Hasse frontier / downset derivation            compiled previous scaffold
T8b. Maximal frontier certificate bridge           this file
T9. Finite maximal frontier existence              next hard target
T10. Incidence sign-source theorem                 open
T11. Hard Selector Closure Theorem                 open
```
