# RA Hasse Frontier Maximal — Compile Confirmed

Date: 2026-04-29

`RA_HasseFrontier_Maximal_v1.lean` compiled successfully in the user's RA Lean/Lake environment after replacing the certificate constructor declaration from `theorem` to `def`.

## Status

```text
RA_HasseFrontier_Maximal_v1.lean
status: lean_env_compile_confirmed_no_sorry_no_admit_no_axiom
sha256: 4fa79cefe81ebe79bdb80a5ba295521d948941c4f1cbfe188975b8dedf3a5358
```

## Theorem-ladder role

This file proves the certificate bridge:

```text
TopoMaxCertificate
  → MaximalReachableAbove
  → MaximalFrontierCertificate
  → HasseFrontierCover
```

It does not yet derive `TopoMaxCertificate` from finite candidate-past data. That is the next file, `RA_HasseFrontier_FiniteMax_v1.lean`.

## RAKB implication

Update `ART-SEL-LEAN-RA_HasseFrontier_Maximal_v1` from build-pending to compile-confirmed. Keep the epistemic status as formalization scaffold, not a closed Selector Closure theorem.
