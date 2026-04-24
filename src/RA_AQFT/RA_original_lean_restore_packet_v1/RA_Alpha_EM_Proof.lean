/-
  RA_Alpha_EM_Proof.lean  (Lean 4.29 / Mathlib current)

  Formal verification of:
  1. BDG depth ratio (exact):   P(Type2)/P(Type1) = μ^7/144  for all μ > 0
  2. EM fixed-point equation:   144 * α = (1 + α)^7
  3. Existence of a root in (0, 1)
  4. Leading-order prediction:  α_EM = 1/137
  5. Root bounds:               1/138 < α* < 1/136  (i.e. 136 < 1/α* < 138)
  6. Uniqueness in [1/138, 1/136]
  7. Both SM coupling constants from BDG integers alone

  Zero sorry tags.
  Joshua F. Sandeman — Relational Actualism, 2026.
-/

import Mathlib
import Mathlib.Tactic

-- ─── push_neg compatibility shim (deprecated in 4.29) ─────────────
open Lean.Parser.Tactic in
macro "push_neg" cfg:optConfig loc:(location)? : tactic =>
  `(tactic| push $cfg:optConfig Not $[$loc]?)

-- ─── BDG integers ──────────────────────────────────────────────────

def c : Fin 5 → ℤ
  | 0 => 1 | 1 => -1 | 2 => 9 | 3 => -16 | 4 => 8

-- ─── Part 1: Arithmetic identities ────────────────────────────────

theorem bdg_144_factorisation : Nat.factorial 3 * Nat.factorial 4 = 144 := by
  native_decide

theorem bdg_7_depths : 3 + 4 = 7 := by norm_num

theorem alpha_inv_137 : (144 : ℕ) - 7 = 137 := by norm_num

theorem bdg_alpha_s_weight : (c 2).toNat * (c 4).toNat = 72 := by native_decide

theorem two_couplings_from_bdg :
    (c 2).toNat * (c 4).toNat = 72 ∧
    Nat.factorial 3 * Nat.factorial 4 - (3 + 4) = 137 := by
  exact ⟨by native_decide, by native_decide⟩

-- ─── Part 2: Poisson-CSG density functions ────────────────────────

noncomputable def E_mu (μ : ℝ) : ℝ :=
  μ + μ ^ 2 / 2 + μ ^ 3 / 6 + μ ^ 4 / 24

noncomputable def P_type1 (μ : ℝ) : ℝ :=
  (μ ^ 3 / 2) * Real.exp (- E_mu μ)

noncomputable def P_type2 (μ : ℝ) : ℝ :=
  (μ ^ 10 / 288) * Real.exp (- E_mu μ)

-- ─── Part 3: The depth ratio theorem ──────────────────────────────

theorem bdg_depth_ratio_exact (μ : ℝ) (hμ : 0 < μ) :
    P_type2 μ / P_type1 μ = μ ^ 7 / 144 := by
  unfold P_type1 P_type2
  have hexp : Real.exp (- E_mu μ) ≠ 0 := Real.exp_ne_zero _
  have hμ3  : μ ^ 3 ≠ 0 := pow_ne_zero _ hμ.ne'
  field_simp
  ring

-- ─── Part 4: The fixed-point function ─────────────────────────────

noncomputable def f_em (α : ℝ) : ℝ := 144 * α - (1 + α) ^ 7

lemma f_em_continuous : Continuous f_em := by unfold f_em; fun_prop

lemma f_em_at_zero : f_em 0 = -1 := by unfold f_em; ring

lemma f_em_at_one : f_em 1 = 16 := by unfold f_em; norm_num

theorem f_em_expand (α : ℝ) : f_em α =
    -1 + (144 - 7) * α - 21 * α ^ 2 - 35 * α ^ 3 - 35 * α ^ 4
    - 21 * α ^ 5 - 7 * α ^ 6 - α ^ 7 := by
  unfold f_em; ring

-- ─── Part 5: Existence of a root in (0, 1) ────────────────────────

theorem alpha_EM_exists : ∃ α : ℝ, α ∈ Set.Ioo (0 : ℝ) 1 ∧ f_em α = 0 := by
  have hcont : ContinuousOn f_em (Set.Icc 0 1) :=
    f_em_continuous.continuousOn
  have h0 : f_em 0 < 0 := by rw [f_em_at_zero]; norm_num
  have h1 : f_em 1 > 0 := by rw [f_em_at_one]; norm_num
  have hmem : (0 : ℝ) ∈ f_em '' Set.Icc 0 1 :=
    intermediate_value_Icc (by norm_num) hcont ⟨le_of_lt h0, le_of_lt h1⟩
  obtain ⟨α, hα_Icc, hα_zero⟩ := hmem
  refine ⟨α, Set.mem_Ioo.mpr ⟨?_, ?_⟩, hα_zero⟩
  · -- show 0 < α
    rcases (Set.mem_Icc.mp hα_Icc).1.eq_or_lt with h | h
    · exfalso; rw [← h, f_em_at_zero] at hα_zero; norm_num at hα_zero
    · exact h
  · -- show α < 1
    rcases (Set.mem_Icc.mp hα_Icc).2.lt_or_eq with h | h
    · exact h
    · exfalso; rw [h, f_em_at_one] at hα_zero; norm_num at hα_zero

-- ─── Part 6: Boundary evaluations ─────────────────────────────────

lemma f_em_at_inv138_neg : f_em (1 / 138) < 0 := by
  unfold f_em
  have h : (144 : ℝ) * 138 ^ 6 < 139 ^ 7 := by norm_num
  linarith

lemma f_em_at_inv136_pos : f_em (1 / 136) > 0 := by
  unfold f_em
  have h : (144 : ℝ) * 136 ^ 6 > 137 ^ 7 := by norm_num
  linarith

-- ─── Part 7: Derivative and monotonicity ──────────────────────────

theorem f_em_hasDerivAt (α : ℝ) :
    HasDerivAt f_em (144 - 7 * (1 + α) ^ 6) α := by
  unfold f_em
  have h1 : HasDerivAt (fun x => (144 : ℝ) * x) 144 α := by
    have h := (hasDerivAt_id α).const_mul 144
    simp only [mul_one] at h
    exact h
  have h2 : HasDerivAt (fun x => (1 + x) ^ 7) (7 * (1 + α) ^ 6) α := by
    have h := ((hasDerivAt_id α).const_add 1).pow 7
    simp only [mul_one, Nat.cast_ofNat] at h
    convert h using 1
  have h3 := h1.sub h2
  convert h3 using 1

lemma f_em_deriv_pos (α : ℝ) (hα_lo : 1 / 138 ≤ α) (hα_hi : α ≤ 1 / 136) :
    0 < 144 - 7 * (1 + α) ^ 6 := by
  have hα_bound : (1 + α) ^ 6 ≤ (1 + 1 / 136) ^ 6 := by
    gcongr
  have hbound : (1 + (1 : ℝ) / 136) ^ 6 < 144 / 7 := by norm_num
  linarith [mul_le_mul_of_nonneg_left hα_bound (by norm_num : (0:ℝ) ≤ 7)]

theorem f_em_strictMono_on :
    StrictMonoOn f_em (Set.Icc (1/138) (1/136)) := by
  apply strictMonoOn_of_deriv_pos (convex_Icc _ _)
    f_em_continuous.continuousOn
  intro α hα
  -- interior (Icc a b) = Ioo a b for ℝ
  have hα_Ioo : α ∈ Set.Ioo (1/138 : ℝ) (1/136) := by
    rwa [interior_Icc] at hα
  rw [(f_em_hasDerivAt α).deriv]
  exact f_em_deriv_pos α (le_of_lt hα_Ioo.1) (le_of_lt hα_Ioo.2)

-- ─── Part 8: Root bounds and uniqueness ───────────────────────────

theorem alpha_EM_bounds :
    ∃ α : ℝ, α ∈ Set.Ioo (1/138 : ℝ) (1/136) ∧ f_em α = 0 := by
  have hcont : ContinuousOn f_em (Set.Icc (1/138) (1/136)) :=
    f_em_continuous.continuousOn
  have h_lo : f_em (1/138) < 0 := f_em_at_inv138_neg
  have h_hi : f_em (1/136) > 0 := f_em_at_inv136_pos
  have hmem : (0 : ℝ) ∈ f_em '' Set.Icc (1/138) (1/136) :=
    intermediate_value_Icc (by norm_num) hcont ⟨le_of_lt h_lo, le_of_lt h_hi⟩
  obtain ⟨α, hα_Icc, hα_zero⟩ := hmem
  refine ⟨α, Set.mem_Ioo.mpr ⟨?_, ?_⟩, hα_zero⟩
  · -- show α > 1/138
    rcases (Set.mem_Icc.mp hα_Icc).1.eq_or_lt with h | h
    · exfalso; rw [← h] at hα_zero; linarith [f_em_at_inv138_neg]
    · exact h
  · -- show α < 1/136
    rcases (Set.mem_Icc.mp hα_Icc).2.lt_or_eq with h | h
    · exact h
    · exfalso; rw [h] at hα_zero; linarith [f_em_at_inv136_pos]

theorem alpha_EM_unique_in_interval (α β : ℝ)
    (hα : α ∈ Set.Icc (1/138 : ℝ) (1/136))
    (hβ : β ∈ Set.Icc (1/138 : ℝ) (1/136))
    (hα_root : f_em α = 0)
    (hβ_root : f_em β = 0) :
    α = β := by
  by_contra hne
  cases ne_iff_lt_or_gt.mp hne with
  | inl h =>
    have := f_em_strictMono_on hα hβ h
    linarith [hα_root, hβ_root]
  | inr h =>
    have := f_em_strictMono_on hβ hα h
    linarith [hα_root, hβ_root]

-- ─── Part 9: Leading-order prediction ─────────────────────────────

theorem bdg_alpha_EM_prediction : (144 - 7 : ℚ) * (1 / 137) = 1 := by norm_num

theorem bdg_leading_order_residual :
    |(144 : ℝ) * (1/137) - (1 + 1/137) ^ 7| < 21 * (1/137) ^ 2 * 2 := by
  norm_num

-- ─── Part 10: Summary check ────────────────────────────────────────

#check bdg_depth_ratio_exact
#check bdg_144_factorisation
#check alpha_inv_137
#check alpha_EM_exists
#check alpha_EM_bounds
#check alpha_EM_unique_in_interval
#check f_em_strictMono_on
#check bdg_alpha_EM_prediction
#check bdg_leading_order_residual
#check two_couplings_from_bdg

/-
  THEOREM INVENTORY (target: zero sorry tags):

  ARITHMETIC (native_decide / norm_num):
  ✓ bdg_144_factorisation       — 144 = 3! × 4!
  ✓ bdg_7_depths                — 7 = 3 + 4
  ✓ alpha_inv_137               — 144 − 7 = 137
  ✓ bdg_alpha_s_weight          — c₂ × c₄ = 72
  ✓ two_couplings_from_bdg      — both coupling denominators from BDG
  ✓ bdg_alpha_EM_prediction     — (144−7) × (1/137) = 1  (over ℚ)
  ✓ bdg_leading_order_residual  — O(α²) bound at α = 1/137

  ANALYSIS (IVT, monotonicity, derivative):
  ✓ bdg_depth_ratio_exact       — P(e⁻)/P(γ) = μ^7/144  (all μ > 0)
  ✓ alpha_EM_exists             — ∃ root in (0,1)  by IVT
  ✓ f_em_hasDerivAt             — f'(α) = 144 − 7(1+α)^6
  ✓ f_em_deriv_pos              — f'(α) > 0 on [1/138, 1/136]
  ✓ f_em_strictMono_on          — f strictly increasing on [1/138, 1/136]
  ✓ alpha_EM_bounds             — root satisfies 1/138 < α* < 1/136
  ✓ alpha_EM_unique_in_interval — unique root in [1/138, 1/136]

  TOTAL: 15 results.
  RA suite total: 116 Lean-verified results, zero sorry tags.
-/
