# RA AQFT Governance and CFC Integration Memo v2

## What this pass did
This pass converts the AQFT audit into an executable cleanup packet at the repository level.

It does two things:
1. fixes repo-governance ambiguity about which AQFT files are canonical; and
2. provides a direct integration patch for the single load-bearing CFC lemma
   in `RA_AQFT_Proofs_v10.lean` using the already-present Mathlib-only port
   `RA_CFC_Port.lean`.

## Main findings

### 1. The narrowest AQFT bottleneck is genuinely narrow
The finite-dimensional Unruh / frame-independence chain still centers on:
- `Matrix.cfc_conj_unitary`
- `log_unitary_conj`
- `relEnt_unitary_invariant`
- `vacuum_lorentz_invariant`
- `frame_independence`
- `rindler_stationarity`

The single live executable `sorry` in the canonical root is the CFC
conjugation lemma. That is the right place to concentrate effort.

### 2. The repo's current AQFT governance is muddled
The canonical root is `RA_AQFT_Proofs_v10.lean`, because that is the file named
in `lakefile.lean`'s default roots. But the same tree also contains:
- `RA_CFC_Port.lean`, a local Mathlib-only support port,
- `RA_AQFT_CFC_Patch.lean`, an older direct-LQI dependency sketch,
- `RA_AQFT_Proofs.lean`, a shadow file titled "v10.1 — CFC Integrated" even
  though it is nonroot and still contains multiple live executable `sorry`s.

Those files need explicit canonicality labeling.

### 3. The existing port header contains a real integration bug
In `RA_AQFT_Proofs_v10.lean`, the fields of `UnitaryMatrix` are:
- `hUU  : Uᴴ * U = 1`
- `hUU' : U * Uᴴ = 1`

So:
- `U.hUU` witnesses `U.mat.Isometry`
- `U.hUU'` witnesses `U.mat.conjTranspose.Isometry` after simplification

An integration recipe that swaps those two fields is wrong. This pass fixes
that in the support-port header and in the direct CFC integration patch.

## Best-effort code patch
The patched root imports `RA_CFC_Port` and replaces the live CFC `sorry` with:

```lean
  have hU_iso : U.mat.Isometry := by
    simpa [Matrix.Isometry] using U.hUU
  have hUct_iso : U.mat.conjTranspose.Isometry := by
    simpa [Matrix.Isometry, Matrix.conjTranspose_conjTranspose] using U.hUU'
  simpa using (Matrix.cfc_conj_isometry (A := M) (u := U.mat) f hU_iso hUct_iso)
```

This is the right shape given the local support port already in the tree.
However, this audit environment does not have `lean` or `lake`, so compile
verification still has to be done on the pinned toolchain in-repo.

## Recommended merge order
1. merge the governance comments in `lakefile.lean`
2. merge the corrected header note in `RA_CFC_Port.lean`
3. merge the archival warnings into `RA_AQFT_CFC_Patch.lean` and `RA_AQFT_Proofs.lean`
4. merge the `RA_AQFT_Proofs_v10.lean` integration patch
5. run `lake build`
6. only then relax the "current-Mathlib closure target" wording in Paper I

## What remains open after a successful build
Even if the CFC patch compiles cleanly, the AQFT story is still only partially closed.
Open layers remain:
- `vacuum_lorentz_invariant` as the imported QFT physics input
- `petz_monotonicity` via an LQI adapter
- the local-algebra / modular-flow AQFT frontier beyond the finite-dimensional theorem
