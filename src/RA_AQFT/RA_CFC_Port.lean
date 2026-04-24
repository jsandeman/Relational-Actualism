import Mathlib

/-!
  RA_CFC_Port_v2_minimal.lean

  Minimal AQFT support port for the current RA toolchain.

  This version fixes two concrete problems exposed by `lake build`:
  1. the previous file imported the wrong module path for the matrix CFC API;
  2. it tried to port an unnecessary general layer (`unitaryGroup`, non-Hermitian fallback)
     even though RA_AQFT_Proofs_v10 only needs the Hermitian case used by
     `log_unitary_conj`.

  The only exported theorem needed by RA_AQFT_Proofs_v10 is:

      Matrix.cfc_conj_isometry

  in the Hermitian case.
-/

noncomputable section
open Classical Matrix BigOperators
open scoped Matrix

namespace Matrix

variable {d d₂ R : Type*}
variable [Fintype d] [DecidableEq d] [Fintype d₂] [DecidableEq d₂]
variable [CommRing R] [StarRing R]
variable {𝕜 : Type*} [RCLike 𝕜] {A : Matrix d d 𝕜}

/-- An isometry is a matrix `A` such that `Aᴴ * A = 1`. -/
def Isometry (A : Matrix d d₂ R) : Prop :=
  Aᴴ * A = 1

/--
Generalizes `Matrix.IsHermitian.cfc` to any diagonalization by a two-sided isometry.
This is the load-bearing finite-dimensional statement used in the AQFT bridge.
-/
theorem IsHermitian.cfc_eq_any_isometry {n m 𝕜 : Type*} [RCLike 𝕜]
    [Fintype n] [DecidableEq n] [Fintype m] [DecidableEq m]
    {A : Matrix n n 𝕜} (hA : A.IsHermitian) {U : Matrix n m 𝕜}
    (hU₁ : U * Uᴴ = 1) (hU₂ : Uᴴ * U = 1) {D : m → ℝ}
    (hUD : A = (U * diagonal (RCLike.ofReal ∘ D) : Matrix _ _ _) * Uᴴ) (f : ℝ → ℝ) :
    hA.cfc f = (U * diagonal (RCLike.ofReal ∘ f ∘ D) : Matrix _ _ _) * Uᴴ := by
  rw [Matrix.IsHermitian.cfc]
  have hUV := hA.spectral_theorem
  set V := hA.eigenvectorUnitary with hV; clear_value V
  set D2 := hA.eigenvalues with hD; clear_value D2
  rcases V with ⟨V, hV₁, hV₂⟩
  clear hV hD
  subst A; clear hA
  have h_diag_eq : diagonal (RCLike.ofReal ∘ D) * (Uᴴ * V) =
      (Uᴴ * V) * diagonal (RCLike.ofReal ∘ D2) := by
    have h_mul : (Uᴴ * U * diagonal (RCLike.ofReal ∘ D) * Uᴴ : Matrix m n 𝕜) * V =
        Uᴴ * V * (diagonal (RCLike.ofReal ∘ D2) * star V * V) := by
      simp only [Matrix.mul_assoc, hUV]
    simp_all [Matrix.mul_assoc]
  have h_diag_eq_f : diagonal (RCLike.ofReal ∘ f ∘ D) * (Uᴴ * V) =
      (Uᴴ * V) * diagonal (RCLike.ofReal ∘ f ∘ D2) := by
    ext i j
    simp_all only [diagonal_mul, Function.comp_apply, mul_diagonal]
    replace h_diag_eq := congr_fun (congr_fun h_diag_eq i) j
    by_cases hi : D i = D2 j <;> simp_all [mul_comm]
  have h_final : U * diagonal (RCLike.ofReal ∘ f ∘ D) * Uᴴ * V =
      V * diagonal (RCLike.ofReal ∘ f ∘ D2) := by
    have h_final : U * diagonal (RCLike.ofReal ∘ f ∘ D) * (Uᴴ * V) =
        U * (Uᴴ * V) * diagonal (RCLike.ofReal ∘ f ∘ D2) := by
      rw [Matrix.mul_assoc, h_diag_eq_f, Matrix.mul_assoc]
    rw [Matrix.mul_assoc, Matrix.mul_assoc]
    simp_all +decide [← Matrix.mul_assoc]
  rw [← h_final, Matrix.mul_assoc]
  rw [hV₂, mul_one]

private theorem cfc_conj_isometry' (hA : A.IsHermitian) (f : ℝ → ℝ) {u : Matrix d₂ d 𝕜}
    (hu₁ : u.Isometry) (hu₂ : uᴴ.Isometry) :
    cfc f (u * A * uᴴ) = u * (cfc f A) * uᴴ := by
  let D := hA.eigenvalues
  let U' := u * hA.eigenvectorUnitary.val
  have hAu : (u * A * uᴴ).IsHermitian := by
    simpa using isHermitian_conjTranspose_mul_mul uᴴ hA
  have hU1 : U' * U'ᴴ = 1 := by
    dsimp [U']
    rw [conjTranspose_mul, Matrix.mul_assoc]
    nth_rw 2 [← Matrix.mul_assoc]
    rw [show _ * _ᴴ = 1 from hA.eigenvectorUnitary.2.2, Matrix.one_mul]
    simpa [Isometry] using hu₂
  have hU2 : U'ᴴ * U' = 1 := by
    dsimp [U']
    rw [conjTranspose_mul, Matrix.mul_assoc]
    nth_rw 2 [← Matrix.mul_assoc]
    rw [hu₁, Matrix.one_mul]
    exact hA.eigenvectorUnitary.2.1
  have hUD : u * A * uᴴ = (U' * diagonal (RCLike.ofReal ∘ D) : Matrix _ _ _) * U'ᴴ := by
    refine (congrArg (fun X => u * X * uᴴ) hA.spectral_theorem).trans ?_
    simp [U', D, Matrix.mul_assoc, conjTranspose_mul]
  have h_any := IsHermitian.cfc_eq_any_isometry
    (A := u * A * uᴴ) (D := D) (n := d₂) (m := d) (U := U') hAu hU1 hU2 hUD f
  rw [hAu.cfc_eq, h_any, hA.cfc_eq]
  simp [Matrix.IsHermitian.cfc, U', D, Matrix.mul_assoc, conjTranspose_mul]

/--
The only theorem RA_AQFT_Proofs_v10 currently needs:
for Hermitian `A`, conjugation by a two-sided isometry commutes with the real CFC.
-/
theorem cfc_conj_isometry (hA : A.IsHermitian) (f : ℝ → ℝ) {u : Matrix d₂ d 𝕜}
    (hu₁ : u.Isometry) (hu₂ : uᴴ.Isometry) :
    cfc f (u * A * uᴴ) = u * (cfc f A) * uᴴ := by
  exact cfc_conj_isometry' hA f hu₁ hu₂

end Matrix
