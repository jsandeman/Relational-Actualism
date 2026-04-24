import RA_O14_Uniqueness_Core_draft

/-!
# RA_BDG_Coefficient_Arithmetic

Arithmetic-only native wrapper for the BDG coefficient core.

This file keeps only the integer / binomial content needed for the active root.
Any external geometric, coupling, or continuum overlay belongs outside the
native root.
-/

def bdg_c0 : ℤ := 1
def bdg_c1 : ℤ := -1
def bdg_c2 : ℤ := 9
def bdg_c3 : ℤ := -16
def bdg_c4 : ℤ := 8

theorem bdg_birth_coefficient : bdg_c0 = 1 := rfl
theorem bdg_depth1_coefficient : bdg_c1 = -1 := rfl
theorem bdg_depth2_coefficient : bdg_c2 = 9 := rfl
theorem bdg_depth3_coefficient : bdg_c3 = -16 := rfl
theorem bdg_depth4_coefficient : bdg_c4 = 8 := rfl

theorem bdg_coefficient_vector :
    (bdg_c0, bdg_c1, bdg_c2, bdg_c3, bdg_c4) = (1, -1, 9, -16, 8) := by
  rfl

theorem yeats_moments_d4 :
    yeats_moment 0 = 1 ∧
    yeats_moment 1 = 10 ∧
    yeats_moment 2 = 35 ∧
    yeats_moment 3 = 84 := by
  exact ⟨yeats_r0, yeats_r1, yeats_r2, yeats_r3⟩

theorem boolean_interval_counts_core :
    Nat.choose 0 0 = 1 ∧
    Nat.choose 1 0 = 1 ∧ Nat.choose 1 1 = 1 ∧
    Nat.choose 2 0 = 1 ∧ Nat.choose 2 1 = 2 ∧ Nat.choose 2 2 = 1 ∧
    Nat.choose 3 0 = 1 ∧ Nat.choose 3 1 = 3 ∧ Nat.choose 3 2 = 3 ∧ Nat.choose 3 3 = 1 := by
  exact ⟨choose_0_0, choose_1_0, choose_1_1,
    choose_2_0, choose_2_1, choose_2_2,
    choose_3_0, choose_3_1, choose_3_2, choose_3_3⟩

theorem bdg_second_order_balance :
    bdg_c1 + bdg_c2 + bdg_c3 + bdg_c4 = 0 := by
  norm_num [bdg_c1, bdg_c2, bdg_c3, bdg_c4]

theorem bdg_hockey_stick_balance :
    4 * (1 : ℤ) - 6 * 10 + 4 * 35 - 84 = 0 := by
  exact hockey_stick_d4

theorem d4_arithmetic_core :
    (bdg_c0, bdg_c1, bdg_c2, bdg_c3, bdg_c4) = (1, -1, 9, -16, 8) ∧
    (bdg_c1 + bdg_c2 + bdg_c3 + bdg_c4 = 0) := by
  exact ⟨bdg_coefficient_vector, bdg_second_order_balance⟩

/-!
Native root note:

This module is the arithmetic core only. The active root should cite:
- `yeats_moments_d4`
- `boolean_interval_counts_core`
- `bdg_coefficient_vector`
- `bdg_second_order_balance`

and should not cite any coupling or continuum overlay declarations.
-/
