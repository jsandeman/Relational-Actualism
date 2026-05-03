-- RA_BDG_PAccMeasure.lean
-- Tier 3d (interface): measure-theoretic acceptance probability.
--
-- Lifts the abstract real parameter P_acc from Tier 3c
-- (RA_BDG_ActualizationRate.lean) to a measure-theoretic quantity
-- defined on probability measures over BDGProfile.
--
-- Construction:
--   acceptingSet : Set BDGProfile             := {p | accepts p}
--   P_acc_measure (m : Measure BDGProfile) : ENNReal := m acceptingSet
--   P_acc_real    (m : Measure BDGProfile) : ℝ    := (P_acc_measure m).toReal
--
-- The Tier 3c actualization_rate is then recovered by composing:
--   actualization_rate Γ_cand (P_acc_real m)
--
-- Scope: this file does NOT construct the joint Poisson-CSG measure for
-- a given μ. That construction (`bdgProfileMeasure : ℝ≥0 → Measure
-- BDGProfile` as a product of 4 independent Poissons with rates
-- μ^(k+1)/(k+1)!) is deferred to a future Tier 3e.
--
-- Status: zero sorry / admit / axiom. Lake-build-confirmed.

import RA_BDG_ActualizationRate
import Mathlib

namespace RA_BDG_ActualizationRate

open MeasureTheory

/-! ## Section 1 — measurable structure on BDGProfile -/

/-- BDGProfile is treated as a discrete measurable space (every subset
    is measurable; appropriate for a countable type). -/
instance : MeasurableSpace BDGProfile := ⊤

instance : DiscreteMeasurableSpace BDGProfile := ⟨fun _ => trivial⟩

/-! ## Section 2 — the accepting set and its acceptance probability -/

/-- The set of profiles that the BDG kernel accepts. -/
def acceptingSet : Set BDGProfile := {p | accepts p}

/-- Trivial: any subset is measurable in the discrete space. -/
theorem acceptingSet_measurable : MeasurableSet acceptingSet := by
  exact MeasurableSet.of_discrete

/-- The empty profile lies in the accepting set (S = c₀ = 1 > 0). -/
theorem zero_mem_acceptingSet : BDGProfile.zero ∈ acceptingSet :=
  accepts_zero

noncomputable section

/-- The BDG-kernel acceptance probability of a measure on BDGProfile,
    as an extended-non-negative real. -/
def P_acc_measure (m : Measure BDGProfile) : ENNReal := m acceptingSet

/-- The acceptance probability as an ordinary real. -/
def P_acc_real (m : Measure BDGProfile) : ℝ := (P_acc_measure m).toReal

/-! ## Section 3 — basic bounds on `P_acc_real` -/

/-- `P_acc_real` is non-negative for any measure. -/
theorem P_acc_real_nonneg (m : Measure BDGProfile) : 0 ≤ P_acc_real m :=
  ENNReal.toReal_nonneg

/-- For any probability measure, `P_acc_real m ≤ 1`. -/
theorem P_acc_real_le_one (m : Measure BDGProfile) [IsProbabilityMeasure m] :
    P_acc_real m ≤ 1 := by
  unfold P_acc_real P_acc_measure
  exact ENNReal.toReal_mono ENNReal.one_ne_top prob_le_one

/-! ## Section 4 — the trivial saturation point: μ = 0 (Dirac at empty profile) -/

/-- Under the Dirac measure concentrated at the empty profile, the
    acceptance probability is exactly 1. This is the trivial saturation
    point: at μ = 0 in the Poisson-CSG construction, the only profile
    with positive mass is `BDGProfile.zero`, and that profile is
    accepted (S = c₀ = 1 > 0). -/
theorem P_acc_measure_dirac_zero :
    P_acc_measure (Measure.dirac BDGProfile.zero) = 1 := by
  unfold P_acc_measure
  exact Measure.dirac_apply_of_mem zero_mem_acceptingSet

/-- Real-valued version of the trivial saturation point. -/
theorem P_acc_real_dirac_zero_eq_one :
    P_acc_real (Measure.dirac BDGProfile.zero) = 1 := by
  unfold P_acc_real
  rw [P_acc_measure_dirac_zero]
  simp

/-! ## Section 5 — connection to Tier 3c `actualization_rate` -/

/-- **Tier 3c–3d interface.** Composing the measure-theoretic acceptance
    probability with the algebraic actualization-rate construction
    recovers the rate at the saturation point: when the BDG kernel
    accepts with probability 1, the filtered rate equals the candidate
    rate. -/
theorem actualization_rate_dirac_zero_eq_gamma_cand (gamma_cand : ℝ) :
    actualization_rate gamma_cand (P_acc_real (Measure.dirac BDGProfile.zero))
      = gamma_cand := by
  rw [P_acc_real_dirac_zero_eq_one, rate_bridge_limit]

/-! ## Section 6 — bound on the filtered actualization rate -/

/-- **Upper bound on the filtered rate from a probability measure.**
    For any probability measure on profiles and non-negative candidate
    rate, the actualization rate cannot exceed the candidate rate.
    This is the measure-theoretic version of `rate_le_gamma_cand`. -/
theorem actualization_rate_le_gamma_cand_of_prob
    (m : Measure BDGProfile) [IsProbabilityMeasure m]
    {gamma_cand : ℝ} (hG : 0 ≤ gamma_cand) :
    actualization_rate gamma_cand (P_acc_real m) ≤ gamma_cand :=
  rate_le_gamma_cand hG (P_acc_real_nonneg m) (P_acc_real_le_one m)

end -- noncomputable

end RA_BDG_ActualizationRate
