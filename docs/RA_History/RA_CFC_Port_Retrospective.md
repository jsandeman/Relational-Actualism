# CFC Port — Retrospective and Next-Session Plan

**Date:** April 19, 2026
**Status:** Port attempt failed; reverted to pre-session state.

## What happened

The goal was to close the `Matrix.cfc_conj_unitary` sorry in
`RA_AQFT_Proofs_v10.lean` by porting the LQI (Lean-QuantumInfo) proof
chain from `QuantumInfo/ForMathlib/Isometry.lean` into a standalone
Mathlib-only file `RA_CFC_Port.lean`.

The port failed to compile because **Mathlib's matrix CFC API has
drifted substantially** since LQI was written. Specifically:

| LQI idiom (what we ported) | Current Mathlib equivalent |
|---|---|
| `Matrix.IsHermitian.cfc` (bundled via `hA`) | `cfc f A` (unbundled; predicate via `cfc_tac`) |
| `import Mathlib.LinearAlgebra.Matrix.HermitianFunctionalCalculus` | Deprecated; broken redirect |
| `cfc_apply_of_not_predicate` | Renamed/reorganized (exact name TBD) |
| `Matrix.IsHermitian.cfc.eq_1` | Auto-generated eq lemma not available |

The toolchain mismatch we identified earlier (LQI builds on v4.23-rc2;
RA is on v4.29) was a warning sign I undercounted. Porting by
mechanical-copy-with-minor-fixes was never going to work against ~5
Mathlib minor-version drift.

## What to do next session

**Goal:** close `Matrix.cfc_conj_unitary` using *current* Mathlib
primitives, not LQI's.

**Step 1 (Joshua's local Lean):** Run the following `#check`s and paste
the output. This establishes the current API surface.

```lean
import Mathlib

-- The unbundled cfc function
#check @cfc
#check @cfcHom

-- Matrix-specific CFC lemmas
#check @Matrix.IsHermitian.spectral_theorem
#check @Matrix.IsHermitian.spectral_theorem'

-- The "cfc of not-predicate = 0" lemma (current name unknown)
example (A : Matrix (Fin 2) (Fin 2) ℂ) (f : ℝ → ℝ)
    (h : ¬ IsSelfAdjoint A) : cfc f A = 0 := by
  exact?  -- let Lean find the lemma

-- Star-algebra homomorphisms preserve CFC
#check @cfcHom_comp
#check @cfc_comp

-- Is there a direct cfc-conj lemma for unitaries?
example {n : Type*} [Fintype n] [DecidableEq n]
    (U : Matrix.unitaryGroup n ℂ) (M : Matrix n n ℂ) (f : ℝ → ℝ) :
    cfc f ((U : Matrix n n ℂ) * M * (U : Matrix n n ℂ)ᴴ) =
    (U : Matrix n n ℂ) * cfc f M * (U : Matrix n n ℂ)ᴴ := by
  exact?  -- might already exist in Mathlib
```

If the last `example` finds a Mathlib lemma directly, we're done — just
invoke it in `RA_AQFT_Proofs_v10.lean`. No port file needed.

If no direct lemma exists, the proof sketch using modern API is:

```lean
-- Case split on IsSelfAdjoint M
by_cases hM : IsSelfAdjoint M
case pos =>
  -- Use spectral theorem + direct computation
  -- U * M * Uᴴ is also IsSelfAdjoint
  -- and has the same spectrum as M
  -- so cfc f (U * M * Uᴴ) evaluates via the diagonalization
  sorry
case neg =>
  -- Both sides are 0
  -- ¬IsSelfAdjoint M → ¬IsSelfAdjoint (U * M * Uᴴ)
  -- so cfc_apply_of_not_isSelfAdjoint applies on both sides
  sorry
```

**Step 2 (Claude):** Given the `#check` output, write a targeted proof
that uses actual current Mathlib lemma names. Much shorter than the LQI
port (~30 lines, not ~200).

**Step 3:** Compile. Iterate with specific error-driven fixes if needed.

## Archived

`RA_CFC_Port.lean` is preserved in `/mnt/user-data/outputs/` as a
reference showing LQI's proof approach. It does not compile against
current Mathlib. Do not add to the lakefile.

## Current state (post-revert)

Same as session start:
- `RA_AQFT_Proofs_v10.lean` has the 1 CFC sorry (line 287)
- lakefile has 8 roots (no `RA_CFC_Port`)
- Build should succeed (as before today)

## Lesson

Narration-based planning from log files (my pre-session summary)
overcounted the ease of the port. Direct inspection of Mathlib's
current API — before proposing proof strategies — would have caught
this. Stage A of the audit was supposed to establish this discipline;
Stage CFC jumped past it.

For the next CFC attempt: `#check` first, propose proof after.
