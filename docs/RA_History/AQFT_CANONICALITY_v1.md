# AQFT Canonicality and Governance Note v1

## Canonical files
- `RA_AQFT_Proofs_v10.lean` — canonical AQFT root in the default build.
- `RA_CFC_Port.lean` — supporting Mathlib-only port for the CFC conjugation chain.

## Noncanonical / archival files
- `RA_AQFT_Proofs.lean` — shadow file; nonroot; multiple live executable `sorry`s.
- `RA_AQFT_CFC_Patch.lean` — early Lean-QuantumInfo dependency sketch; not the preferred v4.29 path.

## Narrow closure target
The load-bearing library gap for the Unruh / frame-independence chain is the
CFC conjugation lemma used in `Matrix.cfc_conj_unitary`. The proposed patch
imports `RA_CFC_Port.lean` and discharges that lemma through
`Matrix.cfc_conj_isometry`.

## Important field-order correction
In `RA_AQFT_Proofs_v10.lean`:
- `U.hUU  : U.mat.conjTranspose * U.mat = 1`, so it witnesses `U.mat.Isometry`.
- `U.hUU' : U.mat * U.mat.conjTranspose = 1`, so after simplification it witnesses
  `U.mat.conjTranspose.Isometry`.

Any integration recipe that swaps these two fields is wrong.

## What remains open after the patch
- compile verification on the pinned Lean/mathlib toolchain
- `vacuum_lorentz_invariant` as the physics input
- `petz_monotonicity` via an LQI adapter
- the local-algebra / modular-flow AQFT layer beyond the finite-dimensional theorem
