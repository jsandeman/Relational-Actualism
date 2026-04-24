-- RA_KvalRatio.lean
-- Three-angle kval ratio identity: ratio = 2/3
--
-- Pure trigonometric identity: for `kval θ k := 1 + √2 · cos(θ + 2πk/3)` on
-- three angles in arithmetic progression with common difference 2π/3,
--
--    (Σ_{k=0..2} kval² θ k) / (Σ_{k=0..2} kval θ k)² = 2/3.
--
-- All proofs from Mathlib trig + algebra. Zero sorry.
--
-- Apr 21, 2026 rename pass: file renamed from RA_Koide.lean. Theorem labels
-- replaced to remove SM framing. Mathematical content unchanged.
--
-- Author: Joshua F. Sandeman (March 2026)
-- Mathlib4 compatibility rewrite: April 8, 2026

import Mathlib

noncomputable section
open Real BigOperators Finset

-- ═══════════════════════════════════════════════════════════════
-- SECTION 0: DEFINITIONS
-- ═══════════════════════════════════════════════════════════════

def kval (θ : ℝ) (k : Fin 3) : ℝ :=
  1 + sqrt 2 * cos (θ + 2 * π * (k.val : ℝ) / 3)

-- ═══════════════════════════════════════════════════════════════
-- SECTION 1: TRIG VALUES via cos_add / sin_add (Mathlib4-safe)
-- ═══════════════════════════════════════════════════════════════

private lemma cos_2pi_div_3 : cos (2 * π / 3) = -(1 : ℝ) / 2 := by
  have h : (2 : ℝ) * π / 3 = π - π / 3 := by ring
  rw [h, cos_pi_sub, cos_pi_div_three]; ring

private lemma sin_2pi_div_3 : sin (2 * π / 3) = sqrt 3 / 2 := by
  have h : (2 : ℝ) * π / 3 = π - π / 3 := by ring
  rw [h, sin_pi_sub, sin_pi_div_three]

private lemma cos_4pi_div_3 : cos (4 * π / 3) = -(1 : ℝ) / 2 := by
  have h : (4 : ℝ) * π / 3 = π + π / 3 := by ring
  rw [h, Real.cos_add, cos_pi, sin_pi, cos_pi_div_three, sin_pi_div_three]; ring

private lemma sin_4pi_div_3 : sin (4 * π / 3) = -(sqrt 3 / 2) := by
  have h : (4 : ℝ) * π / 3 = π + π / 3 := by ring
  rw [h, Real.sin_add, cos_pi, sin_pi, cos_pi_div_three, sin_pi_div_three]; ring

private lemma angle_k1 : 2 * π * ((1 : Fin 3).val : ℝ) / 3 = 2 * π / 3 := by
  norm_num [Fin.val]
private lemma angle_k2 : 2 * π * ((2 : Fin 3).val : ℝ) / 3 = 4 * π / 3 := by
  norm_num [Fin.val]; ring

-- ═══════════════════════════════════════════════════════════════
-- SECTION 2: FIN 3 SUM IDENTITIES
-- ═══════════════════════════════════════════════════════════════

lemma sum_cos_roots :
    ∑ k : Fin 3, cos (2 * π * (k.val : ℝ) / 3) = 0 := by
  simp only [Fin.sum_univ_three]
  rw [show 2 * π * ((0 : Fin 3).val : ℝ) / 3 = 0 from by norm_num [Fin.val]]
  rw [angle_k1, angle_k2]
  rw [cos_zero, cos_2pi_div_3, cos_4pi_div_3]; ring

lemma sum_sin_roots :
    ∑ k : Fin 3, sin (2 * π * (k.val : ℝ) / 3) = 0 := by
  simp only [Fin.sum_univ_three]
  rw [show 2 * π * ((0 : Fin 3).val : ℝ) / 3 = 0 from by norm_num [Fin.val]]
  rw [angle_k1, angle_k2]
  rw [sin_zero, sin_2pi_div_3, sin_4pi_div_3]; ring

lemma sum_cos_sq_roots :
    ∑ k : Fin 3, cos (2 * π * (k.val : ℝ) / 3) ^ 2 = 3 / 2 := by
  simp only [Fin.sum_univ_three]
  rw [show 2 * π * ((0 : Fin 3).val : ℝ) / 3 = 0 from by norm_num [Fin.val]]
  rw [angle_k1, angle_k2]
  rw [cos_zero, cos_2pi_div_3, cos_4pi_div_3]; ring

lemma sum_sin_sq_roots :
    ∑ k : Fin 3, sin (2 * π * (k.val : ℝ) / 3) ^ 2 = 3 / 2 := by
  simp only [Fin.sum_univ_three]
  rw [show 2 * π * ((0 : Fin 3).val : ℝ) / 3 = 0 from by norm_num [Fin.val]]
  rw [angle_k1, angle_k2]
  rw [sin_zero, sin_2pi_div_3, sin_4pi_div_3]
  have h3 : (Real.sqrt 3) ^ 2 = 3 := sq_sqrt (by norm_num : (3 : ℝ) ≥ 0)
  nlinarith

lemma sum_cos_sin_roots :
    ∑ k : Fin 3,
      cos (2 * π * (k.val : ℝ) / 3) * sin (2 * π * (k.val : ℝ) / 3) = 0 := by
  simp only [Fin.sum_univ_three]
  rw [show 2 * π * ((0 : Fin 3).val : ℝ) / 3 = 0 from by norm_num [Fin.val]]
  rw [angle_k1, angle_k2]
  rw [cos_zero, sin_zero, cos_2pi_div_3, sin_2pi_div_3, cos_4pi_div_3, sin_4pi_div_3]
  ring

-- ═══════════════════════════════════════════════════════════════
-- SECTION 3: THREE-ANGLE COS SUM IDENTITIES (θ-shifted form)
-- ═══════════════════════════════════════════════════════════════

theorem three_angle_cos_sum_zero (θ : ℝ) :
    ∑ k : Fin 3, cos (θ + 2 * π * (k.val : ℝ) / 3) = 0 := by
  simp_rw [cos_add, Finset.sum_sub_distrib, ← Finset.mul_sum]
  rw [sum_cos_roots, sum_sin_roots]; ring

theorem three_angle_cos_sq_sum (θ : ℝ) :
    ∑ k : Fin 3, cos (θ + 2 * π * (k.val : ℝ) / 3) ^ 2 = 3 / 2 := by
  have expand : ∀ k : Fin 3,
      cos (θ + 2 * π * (k.val : ℝ) / 3) ^ 2 =
      cos θ ^ 2 * cos (2 * π * (k.val : ℝ) / 3) ^ 2 -
      2 * cos θ * sin θ *
        cos (2 * π * (k.val : ℝ) / 3) * sin (2 * π * (k.val : ℝ) / 3) +
      sin θ ^ 2 * sin (2 * π * (k.val : ℝ) / 3) ^ 2 :=
    fun k => by rw [cos_add]; ring
  simp_rw [expand, Finset.sum_add_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum]
  simp_rw [show ∀ k : Fin 3,
      2 * cos θ * sin θ * cos (2 * π * (k.val : ℝ) / 3) *
        sin (2 * π * (k.val : ℝ) / 3) =
      (2 * cos θ * sin θ) *
        (cos (2 * π * (k.val : ℝ) / 3) * sin (2 * π * (k.val : ℝ) / 3)) from
    fun k => by ring]
  rw [← Finset.mul_sum, sum_cos_sq_roots, sum_sin_sq_roots, sum_cos_sin_roots]
  linarith [sin_sq_add_cos_sq θ]

-- ═══════════════════════════════════════════════════════════════
-- SECTION 4: KVAL RATIO = 2/3
-- ═══════════════════════════════════════════════════════════════

theorem three_angle_kval_sum (θ : ℝ) : ∑ k : Fin 3, kval θ k = 3 := by
  simp only [kval, Finset.sum_add_distrib, ← Finset.mul_sum]
  rw [three_angle_cos_sum_zero θ, mul_zero, add_zero]
  simp [Finset.sum_const]

theorem three_angle_kval_sq_sum (θ : ℝ) : ∑ k : Fin 3, kval θ k ^ 2 = 6 := by
  have hs2 : sqrt 2 * sqrt 2 = 2 := mul_self_sqrt (by norm_num)
  have expand : ∀ k : Fin 3,
      kval θ k ^ 2 =
      1 + 2 * sqrt 2 * cos (θ + 2 * π * (k.val : ℝ) / 3) +
      2 * cos (θ + 2 * π * (k.val : ℝ) / 3) ^ 2 :=
    fun k => by unfold kval; nlinarith [hs2, sq_nonneg (cos (θ + 2 * π * (k.val : ℝ) / 3))]
  simp_rw [expand, Finset.sum_add_distrib]
  simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
  rw [← Finset.mul_sum, ← Finset.mul_sum]
  rw [three_angle_cos_sum_zero θ, three_angle_cos_sq_sum θ]
  norm_num

/-- **L09 — Scaled three-angle kval ratio = 2/3**: exact algebraic identity
    for all m₀ > 0 and θ ∈ ℝ. The unscaled version `kval_ratio_two_thirds`
    is the underlying pure-trig statement; this scaled form is a consequence
    of homogeneity and is included for direct application to ratios with
    a common multiplicative scale m₀. -/
theorem scaled_kval_ratio_two_thirds (m₀ θ : ℝ) (hm₀ : 0 < m₀) :
    (∑ k : Fin 3, m₀ * kval θ k ^ 2) /
    (∑ k : Fin 3, sqrt m₀ * kval θ k) ^ 2 = 2 / 3 := by
  have h_num : ∑ k : Fin 3, m₀ * kval θ k ^ 2 = m₀ * 6 := by
    rw [← Finset.mul_sum, three_angle_kval_sq_sum]
  have h_den : (∑ k : Fin 3, sqrt m₀ * kval θ k) ^ 2 = m₀ * 9 := by
    rw [← Finset.mul_sum, mul_pow, sq_sqrt hm₀.le, three_angle_kval_sum]; norm_num
  rw [h_num, h_den]; field_simp; norm_num

theorem kval_ratio_two_thirds (θ : ℝ) :
    (∑ k : Fin 3, kval θ k ^ 2) / (∑ k : Fin 3, kval θ k) ^ 2 = 2 / 3 := by
  rw [three_angle_kval_sq_sum, three_angle_kval_sum]; norm_num

end
