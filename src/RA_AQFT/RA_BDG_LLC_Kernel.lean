-- RA_BDG_LLC_Kernel.lean
-- Joint kernel of (trace, BDG, LLC) on MacroSpace = Fin 5 → ℝ has dimension 2.
--
-- Setup:
--   MacroSpace := Fin 5 → ℝ  (one slot per BDG depth: 0..4)
--   traceMap   : extracts x₀
--   bdgMap     : Σ c_R k · x_k where c_R = (1, -1, 9, -16, 8)
--   llcMap     : Σ l_R k · x_k where l_R = (0, 1, -1, 1, -1)
--   bdg_llc_kernel := ker(traceMap) ⊓ ker(bdgMap) ⊓ ker(llcMap)
--
-- KERNEL BASIS (exact rational, verified):
--   v1 = (0, 7, 15, 8, 0)  — parametrised by x₃
--   v2 = (0, 1, -7, 0, 8)  — parametrised by x₄
--
-- PROOF STRATEGY: explicit linear isomorphism  bdg_llc_kernel ≃ₗ[ℝ] ℝ²
--   proj: x ↦ (x₃, x₄)
--   lift: (a,b) ↦ (0, (7a+b)/8, (15a-7b)/8, a, b)
--
-- Apr 21, 2026 rename pass: file renamed from RA_Spin2_Macro.lean. SM/GR
-- framing ("emergent massless spin-2 DOF", "graviton polarizations") stripped
-- to native description. Mathematical content unchanged: the joint kernel of
-- the three BDG-native linear constraints on the 5D macro state space has
-- dimension 2.

import Mathlib

open BigOperators

noncomputable section

abbrev MacroSpace := Fin 5 → ℝ

def traceMap : MacroSpace →ₗ[ℝ] ℝ where
  toFun δN := δN 0
  map_add' := by simp
  map_smul' := by simp

def c_R : Fin 5 → ℝ
  | 0 => 1 | 1 => -1 | 2 => 9 | 3 => -16 | 4 => 8

def bdgMap : MacroSpace →ₗ[ℝ] ℝ where
  toFun δN := ∑ k, c_R k * δN k
  map_add' x y := by
    simp only [Pi.add_apply]; rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl; intro k _; ring
  map_smul' c x := by
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro k _; ring

def l_R : Fin 5 → ℝ
  | 0 => 0 | 1 => 1 | 2 => -1 | 3 => 1 | 4 => -1

def llcMap : MacroSpace →ₗ[ℝ] ℝ where
  toFun δN := ∑ k, l_R k * δN k
  map_add' x y := by
    simp only [Pi.add_apply]; rw [← Finset.sum_add_distrib]
    apply Finset.sum_congr rfl; intro k _; ring
  map_smul' c x := by
    simp only [Pi.smul_apply, smul_eq_mul, RingHom.id_apply]
    rw [Finset.mul_sum]; apply Finset.sum_congr rfl; intro k _; ring

def bdg_llc_kernel : Submodule ℝ MacroSpace :=
  LinearMap.ker traceMap ⊓ LinearMap.ker bdgMap ⊓ LinearMap.ker llcMap

-- Membership iff: x₀=0, Σc_k x_k=0, Σl_k x_k=0
lemma mem_bdg_llc_kernel {x : MacroSpace} :
    x ∈ bdg_llc_kernel ↔
    x 0 = 0 ∧ (∑ k, c_R k * x k) = 0 ∧ (∑ k, l_R k * x k) = 0 := by
  simp only [bdg_llc_kernel, Submodule.mem_inf, LinearMap.mem_ker,
             traceMap, bdgMap, llcMap, LinearMap.coe_mk, AddHom.coe_mk]
  tauto

-- Expand Fin 5 sums
private lemma fin5_sum (f g : Fin 5 → ℝ) :
    ∑ k : Fin 5, f k * g k =
    f 0 * g 0 + f 1 * g 1 + f 2 * g 2 + f 3 * g 3 + f 4 * g 4 := by
  simp [Fin.sum_univ_five]

-- ═══════════════════════════════════════════════════════════════
-- The explicit linear isomorphism  bdg_llc_kernel ≃ₗ[ℝ] Fin 2 → ℝ
-- ═══════════════════════════════════════════════════════════════

private def projMap : bdg_llc_kernel →ₗ[ℝ] (Fin 2 → ℝ) where
  toFun p := ![p.1 3, p.1 4]
  map_add' p q := by
    funext i; fin_cases i <;>
      simp [Matrix.cons_val_zero, Matrix.cons_val_one, Pi.add_apply]
  map_smul' r p := by
    funext i; fin_cases i <;>
      simp [Matrix.cons_val_zero, Matrix.cons_val_one, Pi.smul_apply, smul_eq_mul]

private def liftMap : (Fin 2 → ℝ) →ₗ[ℝ] bdg_llc_kernel where
  toFun ab :=
    ⟨![(0 : ℝ), (7 * ab 0 + ab 1) / 8, (15 * ab 0 - 7 * ab 1) / 8, ab 0, ab 1], by
      rw [mem_bdg_llc_kernel]
      refine ⟨by simp [Matrix.cons_val_zero], ?_, ?_⟩
      · rw [fin5_sum]; simp only [c_R]
        simp [Matrix.cons_val_zero, Matrix.cons_val_one]; ring
      · rw [fin5_sum]; simp only [l_R]
        simp [Matrix.cons_val_zero, Matrix.cons_val_one]; ring⟩
  map_add' ab cd := by
    apply Subtype.ext; funext i; fin_cases i <;>
      simp [Matrix.cons_val_zero, Matrix.cons_val_one,
            Pi.add_apply] <;> ring
  map_smul' r ab := by
    apply Subtype.ext; funext i; fin_cases i <;>
      simp [Matrix.cons_val_zero, Matrix.cons_val_one,
            Pi.smul_apply, smul_eq_mul] <;> ring

private lemma proj_lift_id : Function.LeftInverse projMap liftMap := by
  intro ab
  simp only [projMap, liftMap, LinearMap.coe_mk, AddHom.coe_mk]
  funext i; fin_cases i <;>
    simp [Matrix.cons_val_zero, Matrix.cons_val_one]

private lemma lift_proj_id : Function.LeftInverse liftMap projMap := by
  intro ⟨p, hp⟩
  apply Subtype.ext
  rw [mem_bdg_llc_kernel] at hp
  obtain ⟨h0, hb, hl⟩ := hp
  rw [fin5_sum] at hb hl
  simp only [c_R] at hb; simp only [l_R] at hl
  simp only [liftMap, projMap, LinearMap.coe_mk, AddHom.coe_mk]
  funext i; fin_cases i <;>
    simp [Matrix.cons_val_zero, Matrix.cons_val_one] <;>
    linarith

private def bdg_llc_kernel_iso_R2 : bdg_llc_kernel ≃ₗ[ℝ] (Fin 2 → ℝ) :=
  { projMap with
    invFun    := liftMap
    left_inv  := lift_proj_id
    right_inv := proj_lift_id }

/-- **L-kernel — joint BDG/LLC kernel has dimension 2** (zero sorry).
    The joint kernel of the trace, BDG, and LLC linear maps on the 5D macro
    state space `MacroSpace = Fin 5 → ℝ` is exactly 2-dimensional.
    Proof: explicit linear isomorphism `bdg_llc_kernel ≃ₗ[ℝ] (Fin 2 → ℝ)`. -/
theorem bdg_llc_kernel_finrank_two :
    Module.finrank ℝ bdg_llc_kernel = 2 := by
  have h := LinearEquiv.finrank_eq bdg_llc_kernel_iso_R2
  simp at h
  exact h

-- ═══════════════════════════════════════════════════════════════
-- Zero sorry tags. Joint BDG/LLC kernel dimension fully verified.
-- ═══════════════════════════════════════════════════════════════

end