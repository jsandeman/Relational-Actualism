import RA_D1_NativeConfinement

/-!
# RA_D1_NativeClosure_v1

Native Stage-C rewrite of the extension-classification and closure part of the
restored `RA_D1_Proofs.lean` baseline.

This file keeps only finite extension census and closure properties in native
motif language.
-/

noncomputable section

/-- Scores for all 15 single-step extensions of the symmetric branching motif. -/
def extensionScore_branchS : Fin 15 → ℤ
  | ⟨0,  _⟩ => 0
  | ⟨1,  _⟩ => 0
  | ⟨2,  _⟩ => -1
  | ⟨3,  _⟩ => 18
  | ⟨4,  _⟩ => 18
  | ⟨5,  _⟩ => 18
  | ⟨6,  _⟩ => 18
  | ⟨7,  _⟩ => -23
  | ⟨8,  _⟩ => -23
  | ⟨9,  _⟩ => -23
  | ⟨10, _⟩ => -23
  | ⟨11, _⟩ => -23
  | ⟨12, _⟩ => -23
  | ⟨13, _⟩ => -23
  | ⟨14, _⟩ => -23

/-- Scores for all 15 single-step extensions of the asymmetric branching motif. -/
def extensionScore_branchA : Fin 15 → ℤ
  | ⟨0,  _⟩ => 0
  | ⟨1,  _⟩ => 9
  | ⟨2,  _⟩ => 9
  | ⟨3,  _⟩ => 0
  | ⟨4,  _⟩ => -1
  | ⟨5,  _⟩ => 8
  | ⟨6,  _⟩ => 8
  | ⟨7,  _⟩ => 2
  | ⟨8,  _⟩ => 2
  | ⟨9,  _⟩ => 2
  | ⟨10, _⟩ => 2
  | ⟨11, _⟩ => 2
  | ⟨12, _⟩ => 2
  | ⟨13, _⟩ => 2
  | ⟨14, _⟩ => 2

/-- Scores for all 31 single-step extensions of the asymmetric transition state. -/
def extensionScore_transitionA : Fin 31 → ℤ
  | ⟨ 0, _⟩ =>     0
  | ⟨ 1, _⟩ =>     9
  | ⟨ 2, _⟩ =>     9
  | ⟨ 3, _⟩ =>     0
  | ⟨ 4, _⟩ =>    -1
  | ⟨ 5, _⟩ =>     8
  | ⟨ 6, _⟩ =>     8
  | ⟨ 7, _⟩ =>     2
  | ⟨ 8, _⟩ =>     2
  | ⟨ 9, _⟩ =>     2
  | ⟨10, _⟩ =>     2
  | ⟨11, _⟩ =>     2
  | ⟨12, _⟩ =>     2
  | ⟨13, _⟩ =>     2
  | ⟨14, _⟩ =>     2
  | ⟨15, _⟩ =>   -15
  | ⟨16, _⟩ =>   -15
  | ⟨17, _⟩ =>   -15
  | ⟨18, _⟩ =>   -15
  | ⟨19, _⟩ =>   -15
  | ⟨20, _⟩ =>   -15
  | ⟨21, _⟩ =>   -15
  | ⟨22, _⟩ =>   -15
  | ⟨23, _⟩ =>   -15
  | ⟨24, _⟩ =>   -15
  | ⟨25, _⟩ =>   -15
  | ⟨26, _⟩ =>   -15
  | ⟨27, _⟩ =>   -15
  | ⟨28, _⟩ =>   -15
  | ⟨29, _⟩ =>   -15
  | ⟨30, _⟩ =>   -15
  | ⟨n + 31, h⟩ => absurd h (by omega)

/-- Scores for all 63 single-step extensions of the symmetric transition state. -/
def extensionScore_transitionS : Fin 63 → ℤ
  | ⟨ 0, _⟩ =>     0
  | ⟨ 1, _⟩ =>     0
  | ⟨ 2, _⟩ =>    -1
  | ⟨ 3, _⟩ =>    18
  | ⟨ 4, _⟩ =>    18
  | ⟨ 5, _⟩ =>    18
  | ⟨ 6, _⟩ =>    18
  | ⟨ 7, _⟩ =>   -23
  | ⟨ 8, _⟩ =>   -23
  | ⟨ 9, _⟩ =>   -23
  | ⟨10, _⟩ =>   -23
  | ⟨11, _⟩ =>   -23
  | ⟨12, _⟩ =>   -23
  | ⟨13, _⟩ =>   -23
  | ⟨14, _⟩ =>   -23
  | ⟨15, _⟩ =>     9
  | ⟨16, _⟩ =>     9
  | ⟨17, _⟩ =>     9
  | ⟨18, _⟩ =>     9
  | ⟨19, _⟩ =>     9
  | ⟨20, _⟩ =>     9
  | ⟨21, _⟩ =>     9
  | ⟨22, _⟩ =>     9
  | ⟨23, _⟩ =>     9
  | ⟨24, _⟩ =>     9
  | ⟨25, _⟩ =>     9
  | ⟨26, _⟩ =>     9
  | ⟨27, _⟩ =>     9
  | ⟨28, _⟩ =>     9
  | ⟨29, _⟩ =>     9
  | ⟨30, _⟩ =>     9
  | ⟨31, _⟩ =>     1
  | ⟨32, _⟩ =>     1
  | ⟨33, _⟩ =>     1
  | ⟨34, _⟩ =>     1
  | ⟨35, _⟩ =>     1
  | ⟨36, _⟩ =>     1
  | ⟨37, _⟩ =>     1
  | ⟨38, _⟩ =>     1
  | ⟨39, _⟩ =>     1
  | ⟨40, _⟩ =>     1
  | ⟨41, _⟩ =>     1
  | ⟨42, _⟩ =>     1
  | ⟨43, _⟩ =>     1
  | ⟨44, _⟩ =>     1
  | ⟨45, _⟩ =>     1
  | ⟨46, _⟩ =>     1
  | ⟨47, _⟩ =>     1
  | ⟨48, _⟩ =>     1
  | ⟨49, _⟩ =>     1
  | ⟨50, _⟩ =>     1
  | ⟨51, _⟩ =>     1
  | ⟨52, _⟩ =>     1
  | ⟨53, _⟩ =>     1
  | ⟨54, _⟩ =>     1
  | ⟨55, _⟩ =>     1
  | ⟨56, _⟩ =>     1
  | ⟨57, _⟩ =>     1
  | ⟨58, _⟩ =>     1
  | ⟨59, _⟩ =>     1
  | ⟨60, _⟩ =>     1
  | ⟨61, _⟩ =>     1
  | ⟨62, _⟩ =>     1
  | ⟨n + 63, h⟩ => absurd h (by omega)

/-- Single-step extension census for the symmetric branching motif. -/
theorem single_step_extension_classified_symmetric (m : Fin 15) :
    extensionScore_branchS m ≤ 0 ∨ extensionScore_branchS m = 18 := by
  fin_cases m <;> simp [extensionScore_branchS]

/-- Single-step extension census for the asymmetric branching motif. -/
theorem single_step_extension_classified_asymmetric (m : Fin 15) :
    extensionScore_branchA m ≤ 0 ∨
    extensionScore_branchA m = 9 ∨
    extensionScore_branchA m = 8 ∨
    extensionScore_branchA m = 2 := by
  fin_cases m <;> simp [extensionScore_branchA]

/-- Transition-state extension census for the asymmetric transition state. -/
theorem transition_state_extension_classified_asymmetric (m : Fin 31) :
    extensionScore_transitionA m ≤ 0 ∨
    extensionScore_transitionA m = 9 ∨
    extensionScore_transitionA m = 8 ∨
    extensionScore_transitionA m = 2 := by
  fin_cases m <;> simp [extensionScore_transitionA]

/-- Transition-state extension census for the symmetric transition state. -/
theorem transition_state_extension_classified_symmetric (m : Fin 63) :
    extensionScore_transitionS m ≤ 0 ∨
    extensionScore_transitionS m = 18 ∨
    extensionScore_transitionS m = 9 ∨
    extensionScore_transitionS m = 1 := by
  fin_cases m <;> simp [extensionScore_transitionS]

/-- Closure of the native motif universe under the branching single-step extension
operation. -/
theorem closure_under_admissible_extension :
    (∀ m : Fin 15, extensionScore_branchS m ≤ 0 ∨ extensionScore_branchS m = 18) ∧
    (∀ m : Fin 15,
      extensionScore_branchA m ≤ 0 ∨
      extensionScore_branchA m = 9 ∨
      extensionScore_branchA m = 8 ∨
      extensionScore_branchA m = 2) ∧
    (∀ m : Fin 31,
      extensionScore_transitionA m ≤ 0 ∨
      extensionScore_transitionA m = 9 ∨
      extensionScore_transitionA m = 8 ∨
      extensionScore_transitionA m = 2) ∧
    (∀ m : Fin 63,
      extensionScore_transitionS m ≤ 0 ∨
      extensionScore_transitionS m = 18 ∨
      extensionScore_transitionS m = 9 ∨
      extensionScore_transitionS m = 1) :=
  ⟨single_step_extension_classified_symmetric,
   single_step_extension_classified_asymmetric,
   transition_state_extension_classified_asymmetric,
   transition_state_extension_classified_symmetric⟩

/-- The threshold score for a one-parent, zero-deeper-history endpoint. -/
theorem boundary_case_score :
    bdgScore 1 0 0 0 = 0 := by
  norm_num [bdgScore]

/-- Boundary cases are threshold cases: neither positive nor negative. -/
theorem boundary_case_threshold :
    ¬ (bdgScore 1 0 0 0 > 0) ∧ ¬ (bdgScore 1 0 0 0 < 0) := by
  constructor <;> norm_num [bdgScore]

/-- The boundary score sits strictly between representative filtered and stable
scores. -/
theorem boundary_case_between_filter_and_stable :
    bdgScore 1 1 2 0 < bdgScore 1 0 0 0 ∧
    bdgScore 1 0 0 0 < bdgScore 2 1 0 0 := by
  constructor <;> norm_num [bdgScore]
