-- RA_O14_ArithmeticCore_v1.lean
-- Arithmetic core extracted from the restored baseline `RA_O14_Uniqueness.lean`.
--
-- This draft keeps only the genuinely RA-native arithmetic / combinatorial spine:
--   * Yeats-moment arithmetic
--   * Boolean-lattice / Nat.choose identities
--   * d=4 binomial inversion to the BDG integers
--   * second-order cancellation identities
--   * arithmetic consistency checks
--
-- It deliberately retires the historical `137` and `alpha_s` overlay sections from
-- the active root.

import Mathlib.Data.Nat.Choose.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic.NormNum

/-- The Yeats moment sequence for d = 4:
    r_k = (2k+3)(2k+2)(2k+1)/6. -/
def yeats_moment (k : ℕ) : ℕ :=
  (2 * k + 3) * (2 * k + 2) * (2 * k + 1) / 6

theorem yeats_r0 : yeats_moment 0 = 1 := by native_decide
theorem yeats_r1 : yeats_moment 1 = 10 := by native_decide
theorem yeats_r2 : yeats_moment 2 = 35 := by native_decide
theorem yeats_r3 : yeats_moment 3 = 84 := by native_decide
theorem yeats_r4 : yeats_moment 4 = 165 := by native_decide

/-- Concrete Boolean-lattice / choose identities used in the d = 4 inversion. -/
theorem choose_0_0 : Nat.choose 0 0 = 1 := by native_decide
theorem choose_1_0 : Nat.choose 1 0 = 1 := by native_decide
theorem choose_1_1 : Nat.choose 1 1 = 1 := by native_decide
theorem choose_2_0 : Nat.choose 2 0 = 1 := by native_decide
theorem choose_2_1 : Nat.choose 2 1 = 2 := by native_decide
theorem choose_2_2 : Nat.choose 2 2 = 1 := by native_decide
theorem choose_3_0 : Nat.choose 3 0 = 1 := by native_decide
theorem choose_3_1 : Nat.choose 3 1 = 3 := by native_decide
theorem choose_3_2 : Nat.choose 3 2 = 3 := by native_decide
theorem choose_3_3 : Nat.choose 3 3 = 1 := by native_decide
theorem choose_4_1 : Nat.choose 4 1 = 4 := by native_decide
theorem choose_4_2 : Nat.choose 4 2 = 6 := by native_decide
theorem choose_4_3 : Nat.choose 4 3 = 4 := by native_decide
theorem choose_4_4 : Nat.choose 4 4 = 1 := by native_decide

/-- The Yeats moments as integers on the d = 4 range. -/
def r : ℕ → ℤ
  | 0 => 1
  | 1 => 10
  | 2 => 35
  | 3 => 84
  | _ => 0

/-- The d = 4 binomial-inversion coefficients C₁ … C₄. -/
theorem C1_eq : (1 : ℤ) * 1 = 1 := by norm_num
theorem C2_eq : (1 : ℤ) * 1 - 1 * 10 = -9 := by norm_num
theorem C3_eq : (1 : ℤ) * 1 - 2 * 10 + 1 * 35 = 16 := by norm_num
theorem C4_eq : (1 : ℤ) * 1 - 3 * 10 + 3 * 35 - 1 * 84 = -8 := by norm_num

/-- The complete d = 4 BDG coefficient vector after inversion. -/
theorem bdg_C_vector :
    ((1 : ℤ) * 1,
     (1 : ℤ) * 1 - 1 * 10,
     (1 : ℤ) * 1 - 2 * 10 + 1 * 35,
     (1 : ℤ) * 1 - 3 * 10 + 3 * 35 - 1 * 84) =
    (1, -9, 16, -8) := by
  norm_num

/-- The BDG action coefficients for d = 4. -/
theorem bdg_action_vector :
    (-(1 : ℤ),
     -((1 : ℤ) * 1 - 1 * 10),
     -((1 : ℤ) * 1 - 2 * 10 + 1 * 35),
     -((1 : ℤ) * 1 - 3 * 10 + 3 * 35 - 1 * 84)) =
    (-1, 9, -16, 8) := by
  norm_num

/-- The second-order cancellation identity on the d = 4 action coefficients. -/
theorem second_order : (-1 : ℤ) + 9 + (-16) + 8 = 0 := by norm_num

theorem sum_C_zero : (1 : ℤ) + (-9) + 16 + (-8) = 0 := by norm_num

theorem hockey_stick_d4 : 4 * (1 : ℤ) - 6 * 10 + 4 * 35 - 1 * 84 = 0 := by
  norm_num

/-- Consistency of the explicit integer table `r` with the Yeats formula. -/
theorem r_eq_0 : r 0 = 1 := rfl
theorem r_eq_1 : r 1 = 10 := rfl
theorem r_eq_2 : r 2 = 35 := rfl
theorem r_eq_3 : r 3 = 84 := rfl

theorem r_is_yeats_0 : (r 0 : ℤ) = ↑(yeats_moment 0) := by
  rw [r_eq_0, yeats_r0]
  norm_num

theorem r_is_yeats_1 : (r 1 : ℤ) = ↑(yeats_moment 1) := by
  rw [r_eq_1, yeats_r1]
  norm_num

theorem r_is_yeats_2 : (r 2 : ℤ) = ↑(yeats_moment 2) := by
  rw [r_eq_2, yeats_r2]
  norm_num

theorem r_is_yeats_3 : (r 3 : ℤ) = ↑(yeats_moment 3) := by
  rw [r_eq_3, yeats_r3]
  norm_num

/-- Small polynomial identities retained from the arithmetic core. -/
theorem P_at_zero : (1 : ℤ) = 1 := rfl
theorem P_at_one : (1 : ℤ) - 1 + 9 - 16 + 8 = 1 := by norm_num
theorem R4_at_one : (8 : ℤ) - 8 + 1 = 1 := by norm_num

/-- Cross-dimensional arithmetic checks retained as arithmetic diagnostics. -/
theorem hockey_stick_d2 : 3 * (1 : ℤ) - 3 * 3 + 1 * 6 = 0 := by norm_num

theorem hockey_stick_d6 :
    5 * (1 : ℤ) - 10 * 35 + 10 * 210 - 5 * 715 + 1 * 1820 = 0 := by
  norm_num

theorem hockey_stick_d8 :
    6 * (1 : ℤ) - 15 * 126 + 20 * 1287 - 15 * 6188 + 6 * 20349 - 1 * 53130 = 0 := by
  norm_num

/-- Arithmetic identification of the d = 4 Yeats moments with choose values on the
BDG range k = 0,1,2,3. -/
theorem yeats_eq_choose_k0 : yeats_moment 0 = Nat.choose 3 3 := by native_decide
theorem yeats_eq_choose_k1 : yeats_moment 1 = Nat.choose 5 3 := by native_decide
theorem yeats_eq_choose_k2 : yeats_moment 2 = Nat.choose 7 3 := by native_decide
theorem yeats_eq_choose_k3 : yeats_moment 3 = Nat.choose 9 3 := by native_decide
