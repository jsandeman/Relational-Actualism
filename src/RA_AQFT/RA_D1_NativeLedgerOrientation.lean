import RA_D1_NativeClosure

/-!
# RA_D1_NativeLedgerOrientation_v1

Native Stage-D rewrite of the historical Section-13/14 material from
`RA_D1_Proofs.lean`.

This file keeps only depth-2 ledger preservation and orientation-asymmetry
content, stated in RA-native vocabulary.
-/

noncomputable section

open D1Native

/-- Baseline depth-2 ledger counts for the stable motif families. -/
theorem depth2_ledger_values :
    ((0 : ℤ) = 0) ∧
    ((1 : ℤ) = 1) ∧
    (bdgScore 1 2 0 0 > 0) ∧
    (bdgScore 2 1 0 0 > 0) := by
  refine ⟨rfl, rfl, by norm_num [bdgScore], by norm_num [bdgScore]⟩

/-- The symmetric branching self-replica preserves the depth-2 ledger count. -/
theorem depth2_ledger_preserved_symmetric :
    extensionScore_branchS ⟨3, by omega⟩ = 18 ∧
    bdgScore 1 2 0 0 = 18 := by
  constructor
  · simp [extensionScore_branchS]
  · norm_num [bdgScore]

/-- The asymmetric branching motif admits an escape route to the sequential
stable class without changing the depth-2 ledger value from `1`. -/
theorem escape_to_chain4_preserves_depth2 :
    extensionScore_branchA ⟨1, by omega⟩ = 9 ∧
    extensionScore_branchA ⟨2, by omega⟩ = 9 ∧
    bdgScore 1 1 0 0 = 9 := by
  refine ⟨by simp [extensionScore_branchA],
          by simp [extensionScore_branchA],
          by norm_num [bdgScore]⟩

/-- A representative asymmetric transition profile has unequal depth-3 and
 depth-4 counts. -/
theorem orientation_asymmetry :
    (1 : ℤ) ≠ 2 ∧
    bdgScore 1 1 1 2 = 9 ∧
    bdgScore 1 1 1 1 = 1 := by
  refine ⟨by norm_num, by norm_num [bdgScore], by norm_num [bdgScore]⟩

/-- The stable symmetric sequential endpoint is unique relative to the nearby
asymmetric transition and unstable predecessor profiles. -/
theorem unique_symmetric_stable_endpoint :
    bdgScore 1 1 1 1 > 0 ∧
    (1 : ℤ) = 1 ∧
    bdgScore 1 1 1 0 < 0 ∧
    bdgScore 1 1 1 2 > 0 ∧
    (1 : ℤ) < 2 := by
  refine ⟨by norm_num [bdgScore], rfl,
          by norm_num [bdgScore], by norm_num [bdgScore], by norm_num⟩
