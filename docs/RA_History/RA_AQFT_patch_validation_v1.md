# AQFT Patch Validation Note v1

## Static validation performed
This environment does not have `lean` or `lake`, so no build validation was possible.

I therefore performed static validation only:
- the canonical AQFT root now imports `RA_CFC_Port`
- the live CFC `sorry` body in `RA_AQFT_Proofs_v10.lean` is replaced by a proof term using `Matrix.cfc_conj_isometry`
- the remaining occurrences of the token `sorry` in the patched root are comment text only
- canonicality notes were added to the nonroot AQFT files

## Still required in-repo
Run `lake build` on the pinned toolchain:
- Lean 4.29.0
- mathlib rev `8f1377de1fe0f57f74d9e3eddb3e1ed2e30a9cf9`

Only after that build passes should the paper wording be upgraded from
"narrow closure target" to stronger closure language.
