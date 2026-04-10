# RA Session Log — April 8, 2026 (Evening Session)
## Sorry Closure & Full Lake Build

**Duration:** ~3 hours
**Goal:** Close all closable sorry tags and achieve a clean `lake build` across all 7 Lean files.
**Result:** 4 sorry → 1 sorry. Full 7/7 build successful. 163 theorems compiled clean in Lean 4.29.

---

## Starting State

From the earlier recovery session (same day), the project had:
- 7 Lean files, 163 theorems, **4 mechanical sorry tags**:
  1. `bdg_causal_invariance` in RA_AmpLocality.lean (List.Perm induction)
  2. `sum_outgoing_decompose` in RA_GraphCore.lean (Finset.sum_biUnion)
  3. `sum_incoming_decompose` in RA_GraphCore.lean (Finset.sum_biUnion)
  4. `Matrix.cfc_conj_unitary` in RA_AQFT_Proofs_v10.lean (LQI dependency)
- Files had not been compile-tested against the current Mathlib4 version

---

## Phase 1: RA_AmpLocality.lean — O01/O02 Sorry Closure

### Strategy
The `bdg_causal_invariance` sorry required showing that a `List.foldl` of multiplicative
complex amplitudes is permutation-invariant. The proof uses:
- A private helper `foldl_mul_perm` proved by `induction hp generalizing a` on `List.Perm`
- The `swap` case: `change` to make definitional foldl reduction explicit, then `congr 1; ring`
- The `cons` case: apply IH to the updated accumulator `(a * f x)`
- The `trans` case: compose the two IHs

### Compile-Fix Iterations (5 rounds)

**Round 1:** Original file used individual Mathlib imports (`Mathlib.Data.Complex.Exponential`, etc.)
which no longer exist at those paths.
- Fix: `import Mathlib` (single import)

**Round 2:** Two `DecidablePred` errors on `causal_past` and `causal_interval` filters;
`bdg_amplitude` needed `noncomputable`; `ext n` failed on ℤ; `norm_cast` was a no-op;
some `simp` calls closed goals before manual tactic steps.
- Fix: Added `attribute [instance] CausalDAG.decidable_precedes`
- Fix: `noncomputable def bdg_amplitude`
- Fix: Simplified `bdg_amplitude_locality` proof to `rw [... , hpast]` (collapsed elaborate chain)
- Fix: Rewrote `interval_subset_past` and `interval_eq_interval_past` with explicit `simp only`
- Fix: Removed redundant `norm_cast`
- Fix: Prefixed unused hypotheses with `_` (`_hu`, `_hcausal`)

**Round 3:** `ext u` in `bdg_increment_depends_on_past_only` hit ℕ (from `.card`) instead of Finset.
- Fix: Rewrote entire proof using `suffices` + `Finset.filter_congr` + `interval_eq_interval_past`
  rewrites, avoiding the problematic `congr 1; ext u` chain on `.card`

**Round 4:** "No goals to be solved" — the two `rw [interval_eq_interval_past ...]` calls
already closed the `filter_congr` goal; remaining `congr 1; ext w; simp; tauto` was redundant.
- Fix: Deleted the redundant closing tactics (4 lines)

**Round 5:** ✅ **Compiled clean. Zero sorry. Zero errors.**

### What This Establishes
- **O01 (amplitude locality):** `bdg_amplitude_locality` — proved as theorem of discrete DAG dynamics
- **O02 (causal invariance):** `bdg_causal_invariance` — unconditional for BDG, via `foldl_mul_perm`
- **L07 upgrade:** conditional → unconditional (amplitude_locality axiom replaced by theorem)

---

## Phase 2: RA_GraphCore.lean — L02 Sorry Closure

### Strategy
Two Finset helper lemmas needed for the Graph Cut Theorem:
- `sum_outgoing_decompose`: exchange double sum via `Finset.sum_biUnion`, split via `Finset.sum_union`
- `sum_incoming_decompose`: same exchange, then show `dst_in_VL = internal` by `no_backward`

Key helper lemmas introduced:
- `outgoing_pairwise_disjoint` / `incoming_pairwise_disjoint` (edges from distinct vertices are disjoint)
- `biUnion_outgoing_eq_src_in_VL` / `biUnion_incoming_eq_dst_in_VL` (biUnion = filtered edge set)
- `src_in_VL_eq_internal_union_boundary` (partition by dst membership)
- `dst_in_VL_eq_internal` (by `no_backward` — all incoming to V_L have src ∈ V_L)

### Compile-Fix Iterations (1 round)

**Round 1:** Two one-line fixes:
1. `absurd` arguments swapped — `Disjoint V_L V_R` gives `∈ V_L → ∉ V_R`, not reverse
2. `.symm` removed — `satisfies_local_ledger` already gives `outgoing = incoming` (matching goal)

**Round 2:** ✅ **Compiled clean. Zero sorry. Zero errors.**

### What This Establishes
- **L01 (LLC):** definitional — `satisfies_local_ledger`
- **L02 (Graph Cut Theorem):** `RA_graph_cut_theorem` — fully proved
- **L03 (Markov Blanket):** structural definition with shielding axioms

---

## Phase 3: RA_Koide.lean — L09 Compile Fix

### Strategy
The recovered Koide file (from March 29 chat) used trig lemma names that no longer exist
in the current Mathlib4 (`cos_pi_add`, `sin_pi_add`), and had `Fin.val` normalization
mismatches (`2*π*2/3` vs `4*π/3`).

Complete rewrite using only stable Mathlib4 trig API:
- Derived `cos_2pi_div_3`, `sin_2pi_div_3` via `cos_pi_sub`, `sin_pi_sub` (π − π/3)
- Derived `cos_4pi_div_3`, `sin_4pi_div_3` via `Real.cos_add`, `Real.sin_add` (π + π/3)
- Added explicit `angle_k1`, `angle_k2` conversion lemmas for Fin.val → angle normalization
- All five primitive sum identities (cos, sin, cos², sin², cos·sin) proved from these

### Compile-Fix Iterations (2 rounds)

**Round 1:** Two errors:
1. `sq_sqrt` pattern `√3^2` doesn't match `(√3/2)^2` in `sum_sin_sq_roots`
   - Fix: `have h3 : √3^2 = 3 := sq_sqrt ...; nlinarith`
2. `simp only [kval]` didn't unfold + `linear_combination` scope issue with `k`
   - Fix: `unfold kval; nlinarith [hs2, sq_nonneg ...]`

**Round 2:** ✅ **Compiled clean. Zero sorry. Zero errors.**

### What This Establishes
- **L09 (Koide K = 2/3):** `koide_K_eq_two_thirds` and `majorana_K_eq_two_thirds`
- Full algebraic proof valid for all θ ∈ ℝ, all m₀ > 0

---

## Phase 4: RA_D1_Proofs.lean — Alias Verification

The file with L10/L11/L12 aliases (added in the earlier recovery session) compiled
on first attempt with only harmless unused-variable warnings.

✅ **Compiled clean. Zero sorry. Zero errors.**

---

## Phase 5: Full `lake build` — All 7 Files

First full build revealed RA_Spin2_Macro.lean had Mathlib4 drift:
- `Matrix.cons_val'` renamed (unknown constant)
- Multiple `noncomputable` markers needed

### Spin2 Fixes (2 rounds)

**Round 1:** Replaced all `Matrix.cons_val'` with `Matrix.vecHead` + `Matrix.vecTail`.
Added `noncomputable` to `liftMap` and `physIso`. Changed to `import Mathlib`.
- Result: `projMap` also needed `noncomputable`

**Round 2:** Wrapped entire file in `noncomputable section ... end`.
- Result: ✅ **Compiled clean.** Warnings only (unused vecHead/vecTail simp args — harmless).

### Final `lake build` Result

```
Build completed successfully (8269 jobs).
```

All 7 files compiled. All warnings are cosmetic (unused variables, unused simp args).
The only `sorry` warning is the known LQI adapter in RA_AQFT_Proofs_v10.lean.

---

## Updated Lakefile

Cleaned up lakefile.lean:
- **Added:** `RA_GraphCore`, `RA_Koide`
- **Removed:** `RA_Involutions`, `RA_SteinChen`, `RA_Threshold` (Gemini tautologies),
  `RA_AQFT_Proofs_v2` (superseded by v10), `RA_Alpha_EM_Proof` (superseded by O14)
- **Kept:** `RA_D1_Proofs`, `RA_AQFT_Proofs_v10`, `RA_AmpLocality`, `RA_Spin2_Macro`, `RA_O14_Uniqueness`
- **Optional:** LQI dependency commented out (uncomment to close final sorry)

---

## Final State

| File | Theorems | Sorry | Session Change |
|---|---|---|---|
| RA_D1_Proofs.lean | 76 | 0 | Verified clean |
| RA_GraphCore.lean | 5 | 0 | **2 sorry closed** |
| RA_Koide.lean | 16 | 0 | **Rewritten for Mathlib4** |
| RA_AmpLocality.lean | 5 | 0 | **1 sorry closed** |
| RA_AQFT_Proofs_v10.lean | 9 | 1 | Unchanged (LQI dep) |
| RA_O14_Uniqueness.lean | 50 | 0 | Verified clean |
| RA_Spin2_Macro.lean | 2 | 0 | **Fixed for Mathlib4** |
| **Total** | **163** | **1** | **3 sorry closed, 7/7 clean build** |

### Honest Claim
163 theorems, 1 mechanical sorry (external LQI library dependency), 0 unintentional sorry,
2 physics axioms (amplitude_locality is now a THEOREM not an axiom for BDG dynamics).
All compiled clean in Lean 4.29.0 with current Mathlib4.

### Output Files Produced
- `/mnt/user-data/outputs/RA_AmpLocality.lean` — O01+O02 sorry-free
- `/mnt/user-data/outputs/RA_GraphCore_v2.lean` → rename to `RA_GraphCore.lean` — L02 sorry-free
- `/mnt/user-data/outputs/RA_Koide.lean` — L09 Mathlib4-compatible
- `/mnt/user-data/outputs/RA_Spin2_Macro.lean` — O10s Mathlib4-compatible
- `/mnt/user-data/outputs/RA_AQFT_CFC_Patch.lean` — documentation for LQI sorry closure
- `/mnt/user-data/outputs/lakefile.lean` — cleaned up

---

*Session log produced by Claude (Opus 4.6), April 8, 2026.*
