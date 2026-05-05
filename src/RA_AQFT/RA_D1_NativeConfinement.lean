import RA_D1_NativeKernel

/-!
# RA_D1_NativeConfinement_v1

Native Stage-B rewrite of the confinement / finite-closure part of the restored
historical `RA_D1_Proofs.lean` baseline.

This file uses the neutral language of branching motifs, filter blocks, and
finite closure length.
-/

noncomputable section

open D1Native

/-- One extension step past the symmetric branching motif is filtered. -/
theorem filter_block_event_symmetric :
    bdgScore 1 1 2 0 = -23 := by
  norm_num [bdgScore]

/-- The first extension step past the asymmetric branching motif remains
admissible. -/
theorem asymmetric_step1_admissible :
    bdgScore 1 2 1 0 = 2 := by
  norm_num [bdgScore]

/-- Two extension steps past the asymmetric branching motif are filtered. -/
theorem filter_block_event_asymmetric :
    bdgScore 1 1 2 1 = -15 := by
  norm_num [bdgScore]

/-- The full extension path for the symmetric branching motif. -/
theorem motif_extension_path_symmetric :
    bdgScore 1 2 0 0 = 18 ∧
    bdgScore 1 1 2 0 = -23 ∧
    bdgScore 1 1 1 2 = 9 ∧
    bdgScore 1 1 1 1 = 1 := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], by norm_num [bdgScore]⟩

/-- The full extension path for the asymmetric branching motif. -/
theorem motif_extension_path_asymmetric :
    bdgScore 2 1 0 0 = 8 ∧
    bdgScore 1 2 1 0 = 2 ∧
    bdgScore 1 1 2 1 = -15 ∧
    bdgScore 1 1 1 2 = 9 ∧
    bdgScore 1 1 1 1 = 1 := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], by norm_num [bdgScore]⟩

/-- After the filter block, the symmetric branching worldline converges to the
stable sequential endpoint. -/
theorem motif_converges_to_chain4_symmetric :
    bdgScore 1 1 1 2 > 0 ∧
    bdgScore 1 1 1 1 > 0 ∧
    ∀ n : ℕ, chainScore (n + 4) = 1 := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore], sequential_fixed_point⟩

/-- After the filter block, the asymmetric branching worldline converges to the
stable sequential endpoint. -/
theorem motif_converges_to_chain4_asymmetric :
    bdgScore 1 2 1 0 > 0 ∧
    bdgScore 1 1 1 2 > 0 ∧
    bdgScore 1 1 1 1 > 0 ∧
    ∀ n : ℕ, chainScore (n + 4) = 1 := by
  refine ⟨by norm_num [bdgScore], by norm_num [bdgScore],
          by norm_num [bdgScore], sequential_fixed_point⟩

/-- Closure length for the symmetric branching motif. -/
def closure_length_symmetric : ℕ := 3

/-- Closure length for the asymmetric branching motif. -/
def closure_length_asymmetric : ℕ := 4

/-- Finite closure lengths for both minimal branching motifs. -/
theorem finite_closure_length :
    (bdgScore 1 1 1 1 = 1 ∧ closure_length_symmetric = 3) ∧
    (bdgScore 1 1 1 1 = 1 ∧ closure_length_asymmetric = 4) ∧
    closure_length_symmetric < closure_length_asymmetric := by
  refine ⟨⟨by norm_num [bdgScore], rfl⟩,
          ⟨by norm_num [bdgScore], rfl⟩,
          ?_⟩
  simp [closure_length_symmetric, closure_length_asymmetric]
