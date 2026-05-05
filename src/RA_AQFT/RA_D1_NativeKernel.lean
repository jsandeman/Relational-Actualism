import Mathlib

/-!
# RA_D1_NativeKernel_v1

Native Stage-A rewrite of the D1 kernel from the restored historical
`RA_D1_Proofs.lean` baseline.

This file keeps only the RA-native arithmetic and motif-classification spine:

- BDG score arithmetic in d = 4
- sequential fixed-point behavior of depth profiles
- minimal branching motif classes

It deliberately avoids SM/QFT labels in theorem names and statements.

Wrapped in `namespace D1Native` to avoid `chainScore`/`bdgScore`/
`chain_score_via_bdg_*` collision with `RA_D1_Core`, which redundantly
defines the same kernel arithmetic. Downstream files that need these
identifiers unqualified should `open D1Native` after importing this file.
See RA-ISSUE-LEAN-CHAINSCORE-001 for context.
-/

noncomputable section

namespace D1Native

/-- The d = 4 BDG score on a depth-profile `(N₁,N₂,N₃,N₄)`. -/
def bdgScore (N1 N2 N3 N4 : ℤ) : ℤ :=
  1 + (-1) * N1 + 9 * N2 + (-16) * N3 + 8 * N4

/-- Recovery of the d = 4 coefficient arithmetic from unit depth profiles. -/
lemma bdg_depth0 : bdgScore 0 0 0 0 = 1 := by norm_num [bdgScore]
lemma bdg_depth1 : bdgScore 1 0 0 0 = 0 := by norm_num [bdgScore]
lemma bdg_depth2 : bdgScore 0 1 0 0 = 10 := by norm_num [bdgScore]
lemma bdg_depth3 : bdgScore 0 0 1 0 = -15 := by norm_num [bdgScore]
lemma bdg_depth4 : bdgScore 0 0 0 1 = 9 := by norm_num [bdgScore]

/-- The score at the tip of a purely sequential depth profile. -/
def chainScore : ℕ → ℤ
  | 0 => 1
  | 1 => 0
  | 2 => 9
  | 3 => -7
  | _ => 1

lemma chain_score_via_bdg_0 : bdgScore 0 0 0 0 = chainScore 0 := by norm_num [bdgScore, chainScore]
lemma chain_score_via_bdg_2 : bdgScore 1 1 0 0 = chainScore 2 := by norm_num [bdgScore, chainScore]
lemma chain_score_via_bdg_3 : bdgScore 1 1 1 0 = chainScore 3 := by norm_num [bdgScore, chainScore]
lemma chain_score_via_bdg_4 : bdgScore 1 1 1 1 = chainScore 4 := by norm_num [bdgScore, chainScore]

/-- Once the BDG window saturates, the sequential score is fixed permanently. -/
theorem sequential_fixed_point : ∀ n : ℕ, chainScore (n + 4) = 1 :=
  fun _ => rfl

/-- The positive sequential depths are exactly `0`, `2`, and all `k ≥ 4`. -/
theorem positive_depths (k : ℕ) :
    0 < chainScore k ↔ k ≠ 1 ∧ k ≠ 3 := by
  match k with
  | 0 => simp [chainScore]
  | 1 => simp [chainScore]
  | 2 => simp [chainScore]
  | 3 => simp [chainScore]
  | n + 4 =>
      simp only [chainScore]
      omega

/-- The unstable sequential depths are exactly `1` and `3`. -/
theorem unstable_depths (k : ℕ) :
    chainScore k ≤ 0 ↔ k = 1 ∨ k = 3 := by
  match k with
  | 0 => simp [chainScore]
  | 1 => simp [chainScore]
  | 2 => simp [chainScore]
  | 3 => simp [chainScore]
  | n + 4 =>
      simp only [chainScore]
      omega

/-- The symmetric minimal branching profile has positive BDG score. -/
theorem minimal_branching_profile_symmetric :
    bdgScore 1 2 0 0 = 18 := by
  norm_num [bdgScore]

/-- The asymmetric minimal branching profile has positive BDG score. -/
theorem minimal_branching_profile_asymmetric :
    bdgScore 2 1 0 0 = 8 := by
  norm_num [bdgScore]

/-- Both minimal branching motifs lie in the admissible regime. -/
theorem minimal_branching_class :
    bdgScore 1 2 0 0 > 0 ∧ bdgScore 2 1 0 0 > 0 := by
  constructor <;> norm_num [bdgScore]

/-- Consolidated kernel-level stability window for the sequential and minimal
branching motif classes. -/
theorem branching_stability_window :
    chainScore 0 > 0 ∧
    chainScore 2 > 0 ∧
    (∀ k, 4 ≤ k → chainScore k > 0) ∧
    chainScore 1 = 0 ∧
    chainScore 3 < 0 ∧
    bdgScore 1 2 0 0 > 0 ∧
    bdgScore 2 1 0 0 > 0 := by
  refine ⟨by norm_num [chainScore],
          by norm_num [chainScore],
          ?_,
          by simp [chainScore],
          by simp [chainScore],
          by norm_num [bdgScore],
          by norm_num [bdgScore]⟩
  intro k hk
  obtain ⟨n, rfl⟩ := Nat.exists_eq_add_of_le hk
  rw [show 4 + n = n + 4 from add_comm 4 n, sequential_fixed_point]
  norm_num

end D1Native
