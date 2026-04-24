import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic.NormNum

/-!
# RA_BDG_Coefficient_Arithmetic

Arithmetic native core extracted from `RA_O14_Uniqueness.lean`.

This file keeps only the Yeats-moment / binomial-inversion arithmetic.
All alpha/coupling overlays are intentionally excluded from the native root.
-/

def yeats_moment (k : ℕ) : ℕ :=
  (2*k + 3) * (2*k + 2) * (2*k + 1) / 6

theorem yeats_r0 : yeats_moment 0 = 1 := by native_decide
theorem yeats_r1 : yeats_moment 1 = 10 := by native_decide
theorem yeats_r2 : yeats_moment 2 = 35 := by native_decide
theorem yeats_r3 : yeats_moment 3 = 84 := by native_decide
theorem yeats_r4 : yeats_moment 4 = 165 := by native_decide

def r : ℕ → ℤ
  | 0 => 1
  | 1 => 10
  | 2 => 35
  | 3 => 84
  | _ => 0

theorem bdg_C_vector :
    ((1 : ℤ) * 1,
     (1 : ℤ) * 1 - 1 * 10,
     (1 : ℤ) * 1 - 2 * 10 + 1 * 35,
     (1 : ℤ) * 1 - 3 * 10 + 3 * 35 - 1 * 84) = (1, -9, 16, -8) := by
  norm_num

theorem bdg_action_vector :
    (-(1 : ℤ),
     -((1 : ℤ) * 1 - 1 * 10),
     -((1 : ℤ) * 1 - 2 * 10 + 1 * 35),
     -((1 : ℤ) * 1 - 3 * 10 + 3 * 35 - 1 * 84)) = (-1, 9, -16, 8) := by
  norm_num

theorem second_order : (-1 : ℤ) + 9 + (-16) + 8 = 0 := by
  norm_num

theorem yeats_eq_choose_k0 : yeats_moment 0 = Nat.choose 3 3 := by native_decide
theorem yeats_eq_choose_k1 : yeats_moment 1 = Nat.choose 5 3 := by native_decide
theorem yeats_eq_choose_k2 : yeats_moment 2 = Nat.choose 7 3 := by native_decide
theorem yeats_eq_choose_k3 : yeats_moment 3 = Nat.choose 9 3 := by native_decide
