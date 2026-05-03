-- RA_BDG_ActualizationRate.lean
-- Tier 3c: Lean formalization of the BDG-kernel positional actualization
-- rate construction (companion to bdg_actualization.py).
--
-- Construction (matches the Python module):
--   BDGProfile          := (N₁, N₂, N₃, N₄) ∈ ℕ⁴
--   bdg_action profile  := c₀ + c₁·N₁ + c₂·N₂ + c₃·N₃ + c₄·N₄
--                       where (c₀..c₄) = (1, -1, 9, -16, 8) (BDG d=4)
--   accepts profile     := bdg_action profile > 0
--   actualization_rate Γ_cand P_acc := Γ_cand · P_acc
--
-- Scope: this file formalizes the ARITHMETIC and ALGEBRAIC content of
-- the actualization-rate construction. The probability-theoretic
-- content — P_acc as a measure-theoretic acceptance probability over
-- Poisson-CSG profile distributions, and the saturation theorem
-- P_acc(μ) → 1 as μ → ∞ — is left abstract; P_acc is treated here as
-- a real parameter in [0, 1]. A future Tier 3d would lift the abstract
-- P_acc to a Mathlib-measure-theoretic construction.
--
-- Status: zero sorry / admit / axiom. Lake-build-confirmed.

import RA_BDG_Coefficient_Arithmetic
import Mathlib

namespace RA_BDG_ActualizationRate

/-! ## Section 1 — The BDG profile and action -/

/-- A BDG profile records the count of candidate vertices at each
    interval depth `k ∈ {1, 2, 3, 4}`. The depth-0 birth coefficient
    is the constant `c₀ = 1` and is not stored per profile. -/
structure BDGProfile where
  N1 : ℕ
  N2 : ℕ
  N3 : ℕ
  N4 : ℕ
  deriving DecidableEq

/-- The empty profile (no candidate vertices at any depth). -/
def BDGProfile.zero : BDGProfile := ⟨0, 0, 0, 0⟩

/-- The BDG action evaluated on a profile:
    S = c₀ + c₁·N₁ + c₂·N₂ + c₃·N₃ + c₄·N₄. -/
def bdg_action (p : BDGProfile) : ℤ :=
  bdg_c0 + bdg_c1 * p.N1 + bdg_c2 * p.N2 + bdg_c3 * p.N3 + bdg_c4 * p.N4

/-- The action evaluates to `1` at the empty profile (since only
    `c₀ = 1` contributes). -/
theorem bdg_action_zero : bdg_action BDGProfile.zero = 1 := by
  unfold bdg_action BDGProfile.zero bdg_c0 bdg_c1 bdg_c2 bdg_c3 bdg_c4
  decide

/-- Explicit per-depth decomposition of the action. -/
theorem bdg_action_eq (p : BDGProfile) :
    bdg_action p = 1 + (-1) * (p.N1 : ℤ) + 9 * (p.N2 : ℤ)
                     + (-16) * (p.N3 : ℤ) + 8 * (p.N4 : ℤ) := by
  unfold bdg_action bdg_c0 bdg_c1 bdg_c2 bdg_c3 bdg_c4
  ring

/-! ## Section 2 — The kernel acceptance predicate -/

/-- The BDG kernel acceptance predicate: a profile is accepted iff its
    action is strictly positive. -/
def accepts (p : BDGProfile) : Prop := bdg_action p > 0

instance (p : BDGProfile) : Decidable (accepts p) := by
  unfold accepts; infer_instance

/-- The empty profile is always accepted (S = c₀ = 1 > 0). -/
theorem accepts_zero : accepts BDGProfile.zero := by
  unfold accepts; rw [bdg_action_zero]; decide

/-- Worked rejection: `(N₁=10, ...)` gives `S = 1 − 10 = −9`, so the
    profile is rejected. Demonstrates that the c₁ < 0 coefficient
    actively suppresses depth-1-heavy profiles. -/
theorem rejects_depth1_heavy : ¬ accepts ⟨10, 0, 0, 0⟩ := by
  unfold accepts bdg_action bdg_c0 bdg_c1 bdg_c2 bdg_c3 bdg_c4
  decide

/-- Worked acceptance: `(0, 1, 0, 0)` gives `S = 1 + 9 = 10 > 0`,
    accepted. -/
theorem accepts_single_depth2 : accepts ⟨0, 1, 0, 0⟩ := by
  unfold accepts bdg_action bdg_c0 bdg_c1 bdg_c2 bdg_c3 bdg_c4
  decide

/-- Worked acceptance: `(0, 0, 0, 1)` gives `S = 1 + 8 = 9 > 0`. -/
theorem accepts_single_depth4 : accepts ⟨0, 0, 0, 1⟩ := by
  unfold accepts bdg_action bdg_c0 bdg_c1 bdg_c2 bdg_c3 bdg_c4
  decide

/-- Worked rejection: `(0, 0, 1, 0)` gives `S = 1 − 16 = −15 < 0`. -/
theorem rejects_single_depth3 : ¬ accepts ⟨0, 0, 1, 0⟩ := by
  unfold accepts bdg_action bdg_c0 bdg_c1 bdg_c2 bdg_c3 bdg_c4
  decide

/-! ## Section 3 — The actualization-rate construction -/

noncomputable section

/-- The Tier-3b actualization rate:
    `λ_pos := Γ_cand · P_acc`,
    where `Γ_cand` is the candidate-generation rate (per unit time)
    and `P_acc ∈ [0, 1]` is the BDG-kernel acceptance probability. -/
def actualization_rate (gamma_cand p_acc : ℝ) : ℝ :=
  gamma_cand * p_acc

/-! ### Bridge and limit theorems -/

/-- **Bridge limit.** When the kernel saturates (`P_acc = 1`) the
    BDG-filtered rate equals the candidate rate; this is the Tier-3a
    bridge-interpretation special case. -/
theorem rate_bridge_limit (gamma_cand : ℝ) :
    actualization_rate gamma_cand 1 = gamma_cand := by
  unfold actualization_rate; ring

/-- **Strong-suppression limit.** When `P_acc = 0` the rate vanishes.
    (Note: this limit is not achieved by any positive `μ` in the d=4
    BDG kernel — `P_acc(μ) ≥ 0.4` over the strongly-selective trough.) -/
theorem rate_strong_suppression_limit (gamma_cand : ℝ) :
    actualization_rate gamma_cand 0 = 0 := by
  unfold actualization_rate; ring

/-- **Vanishing-environment limit.** With no environmental candidates
    (`Γ_cand = 0`), the rate vanishes regardless of acceptance. -/
theorem rate_zero_environment (p_acc : ℝ) :
    actualization_rate 0 p_acc = 0 := by
  unfold actualization_rate; ring

/-! ### Algebraic structure -/

/-- The rate is **non-negative** whenever both arguments are. -/
theorem rate_nonneg {gamma_cand p_acc : ℝ}
    (hG : 0 ≤ gamma_cand) (hp : 0 ≤ p_acc) :
    0 ≤ actualization_rate gamma_cand p_acc := by
  unfold actualization_rate; exact mul_nonneg hG hp

/-- The rate is **monotone increasing in `P_acc`** when `Γ_cand ≥ 0`.
    Equivalently: improving the kernel acceptance never decreases the
    rate at fixed candidate generation. -/
theorem rate_monotone_in_pacc {gamma_cand p1 p2 : ℝ}
    (hG : 0 ≤ gamma_cand) (hp : p1 ≤ p2) :
    actualization_rate gamma_cand p1 ≤ actualization_rate gamma_cand p2 := by
  unfold actualization_rate
  exact mul_le_mul_of_nonneg_left hp hG

/-- The rate is **monotone increasing in `Γ_cand`** when `P_acc ≥ 0`. -/
theorem rate_monotone_in_gamma {g1 g2 p_acc : ℝ}
    (hp : 0 ≤ p_acc) (hG : g1 ≤ g2) :
    actualization_rate g1 p_acc ≤ actualization_rate g2 p_acc := by
  unfold actualization_rate
  exact mul_le_mul_of_nonneg_right hG hp

/-- The rate is **linear in `Γ_cand`** (additive). -/
theorem rate_linear_in_gamma (g1 g2 p_acc : ℝ) :
    actualization_rate (g1 + g2) p_acc =
    actualization_rate g1 p_acc + actualization_rate g2 p_acc := by
  unfold actualization_rate; ring

/-- The rate is **linear in `P_acc`** (additive). -/
theorem rate_linear_in_pacc (gamma_cand p1 p2 : ℝ) :
    actualization_rate gamma_cand (p1 + p2) =
    actualization_rate gamma_cand p1 + actualization_rate gamma_cand p2 := by
  unfold actualization_rate; ring

/-- The rate is **homogeneous of degree 1** under uniform scaling. -/
theorem rate_scaling (c gamma_cand p_acc : ℝ) :
    actualization_rate (c * gamma_cand) p_acc =
    c * actualization_rate gamma_cand p_acc := by
  unfold actualization_rate; ring

/-! ### Bound from `P_acc ∈ [0, 1]` -/

/-- **Upper bound.** When `0 ≤ P_acc ≤ 1` and `Γ_cand ≥ 0`, the
    actualization rate is bounded above by the candidate rate.
    This is the formal version of the Tier-3a observation that BDG
    filtering can only suppress (never amplify) decoherence.
    (`_hp_lo` is documentary; the upper bound proof only needs `p_acc ≤ 1`.) -/
theorem rate_le_gamma_cand {gamma_cand p_acc : ℝ}
    (hG : 0 ≤ gamma_cand) (_hp_lo : 0 ≤ p_acc) (hp_hi : p_acc ≤ 1) :
    actualization_rate gamma_cand p_acc ≤ gamma_cand := by
  unfold actualization_rate
  calc gamma_cand * p_acc
      ≤ gamma_cand * 1 := mul_le_mul_of_nonneg_left hp_hi hG
    _ = gamma_cand     := mul_one _

/-- **Lower bound.** Same hypotheses give the trivial lower bound. -/
theorem rate_ge_zero {gamma_cand p_acc : ℝ}
    (hG : 0 ≤ gamma_cand) (hp : 0 ≤ p_acc) :
    0 ≤ actualization_rate gamma_cand p_acc :=
  rate_nonneg hG hp

end -- noncomputable

end RA_BDG_ActualizationRate
