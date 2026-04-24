/-
  RA_CFC_Port.lean  (Lean 4.29 / Mathlib current)

  Self-contained port of the `Matrix.cfc_conj_unitary` proof chain from
  Lean-QuantumInfo (commit 2e4e7e9f, file QuantumInfo/ForMathlib/Isometry.lean),
  extracted to avoid adding Lean-QuantumInfo as a lakefile dependency.

  Rationale: LQI's highest known-building toolchain is v4.23.0-rc2; its
  latest main commit (9b74fd9) currently fails on v4.28.0. RA's toolchain
  is v4.29. Porting just the five theorems needed to close the sorry at
  `Matrix.cfc_conj_unitary` in RA_AQFT_Proofs_v10.lean sidesteps the
  toolchain mismatch entirely.

  ORIGINAL SOURCE ATTRIBUTION:
  Copyright (c) 2025 Alex Meiburg. All rights reserved.
  Released under MIT license.
  Authors: Alex Meiburg
  Source: https://github.com/Timeroot/Lean-QuantumInfo
          QuantumInfo/ForMathlib/Isometry.lean @ 2e4e7e9f

  Theorems ported (with naming to avoid collision with RA_AQFT_Proofs_v10.lean's
  existing Matrix.cfc_conj_unitary lemma, which uses RA's UnitaryMatrix type):

  - Matrix.Isometry                           (def)
  - Matrix.mem_unitaryGroup_iff_isometry      (theorem)
  - Matrix.IsHermitian.cfc_eq_any_isometry    (theorem)
  - Matrix.cfc_conj_isometry' (private, Hermitian helper)
  - Matrix.cfc_conj_isometry                  (theorem) ← RA's call site
  - Matrix.cfc_conj_unitaryGroup              (theorem, unitaryGroup form)
  - Matrix.cfc_conj_unitaryGroup'             (theorem, conjTranspose form)

  Note: LQI names its final theorems Matrix.cfc_conj_unitary / Matrix.cfc_conj_unitary';
  we rename to cfc_conj_unitaryGroup / cfc_conj_unitaryGroup' to avoid clashing with
  RA's existing Matrix.cfc_conj_unitary (which uses RA's custom UnitaryMatrix type,
  not Mathlib's Matrix.unitaryGroup). The workhorse for RA is Matrix.cfc_conj_isometry,
  which takes only two Isometry hypotheses and does not reference unitaryGroup at all.

  Theorems NOT ported (not needed by the CFC chain — available in LQI if wanted):
  - eigenvalue_ext, cfc_eq_any_unitary, cfc_reindex
  - submatrix_one_isometry, reindex_one_isometry, reindex_eq_conj,
    permMatrix_mem_unitaryGroup
  - commute_euclideanLin, directSumDecomposition, exists_unitary, exists_cfc
  - iSup_mono_bot, orthogonalFamily_eigenspace_inf_eigenspace'

  Canonical role in the present RA repo:
  this file is a supporting Mathlib-only port meant to be imported by the
  canonical AQFT root RA_AQFT_Proofs_v10.lean. It is not itself a default
  root theorem file, but it is the preferred closure path for the remaining
  CFC lemma on the v4.29 toolchain.

  Integration recipe for RA_AQFT_Proofs_v10.lean:
  Audit note: in RA_AQFT_Proofs_v10.lean the correct field order is
  `U.hUU` for `U.mat.Isometry` and `U.hUU'` for `U.mat.conjTranspose.Isometry`.
  Earlier scratch examples that swap these are wrong.

  Replace the sorry in RA's existing Matrix.cfc_conj_unitary with a call to
  Matrix.cfc_conj_isometry from this port. RA's UnitaryMatrix bundles both
  U * Uᴴ = 1 and Uᴴ * U = 1 (under field names like hUU, hUU'); use whichever
  field gives each direction. Example:

      lemma Matrix.cfc_conj_unitary (U : UnitaryMatrix n)
          (M : Matrix (Fin n) (Fin n) ℂ) (f : ℝ → ℝ) :
          cfc f (U.mat * M * U.mat.conjTranspose) =
            U.mat * cfc f M * U.mat.conjTranspose := by
        apply Matrix.cfc_conj_isometry f
        · -- U.mat.Isometry  i.e.  U.matᴴ * U.mat = 1
          exact U.hUU    -- in RA_AQFT_Proofs_v10.lean: hUU = Uᴴ * U = 1
        · -- U.mat.conjTransposeᴴ * U.mat.conjTranspose = 1
          --   i.e. U.mat * U.matᴴ = 1 after conjTranspose_conjTranspose
          simpa [Matrix.Isometry, Matrix.conjTranspose_conjTranspose] using U.hUU'
-/

-- Imports: HermitianFunctionalCalculus transitively pulls in
-- Matrix.Hermitian (isHermitian_mul_mul_conjTranspose, isHermitian_conjTranspose_mul_mul),
-- Matrix.Spectrum (eigenvectorUnitary, eigenvalues, spectral_theorem),
-- UnitaryGroup, and the generic CFC machinery (cfc, cfc_apply_of_not_predicate).
-- If anything is missing at compile time on RA's Lean 4.29, add:
--   import Mathlib.Analysis.InnerProductSpace.JointEigenspace  (probably not needed)
-- or fall back to `import Mathlib` (slower but guaranteed).
import Mathlib.LinearAlgebra.Matrix.HermitianFunctionalCalculus

open scoped Matrix

namespace Matrix

variable {d d₂ R : Type*}
variable [Fintype d] [DecidableEq d] [Fintype d₂] [DecidableEq d₂]
variable [CommRing R] [StarRing R]
variable {𝕜 : Type*} [RCLike 𝕜] {A B : Matrix d d 𝕜}

/-- An isometry is a matrix `A` such that `AᴴA = 1`. Compare with a unitary,
which requires `AAᴴ = AᴴA = 1`. It is common to claim that, in a finite-dimensional
vector space, a two-sided isometry (`A.Isometry ∧ Aᴴ.Isometry`) must be square and
therefore unitary; this does not work out so well here, since a `Matrix m n R`
can be a two-sided isometry but cannot be a `unitary` since the rows and columns
are indexed by different labels. -/
def Isometry (A : Matrix d d₂ R) : Prop :=
  Aᴴ * A = 1

theorem mem_unitaryGroup_iff_isometry (A : Matrix d d R) :
    A ∈ unitaryGroup d R ↔ A.Isometry ∧ Aᴴ.Isometry := by
  rw [Isometry, Isometry, conjTranspose_conjTranspose]
  rfl

/-- Generalizes `Matrix.IsHermitian.cfc.eq_1`, which gives a definition for the matrix
CFC in terms of `Matrix.IsHermitian.eigenvalues` and `Matrix.IsHermitian.eigenvectorUnitary`,
to show that the CFC works similarly for _any_ diagonalization by a two-sided isometry. -/
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
  dsimp only at *; clear hV hD
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
  have := IsHermitian.cfc_eq_any_isometry
    (A := u * A * uᴴ) (D := D) (n := d₂) (m := d) (U := U') ?_ ?_ ?_ ?_ f; rotate_left
  · simpa using isHermitian_conjTranspose_mul_mul uᴴ hA
  · dsimp [U']
    rw [conjTranspose_mul, Matrix.mul_assoc]
    nth_rw 2 [← Matrix.mul_assoc]
    rw [show _ * _ᴴ = 1 from hA.eigenvectorUnitary.2.2, Matrix.one_mul]
    simpa [Isometry] using hu₂
  · dsimp [U']
    rw [conjTranspose_mul, Matrix.mul_assoc]
    nth_rw 2 [← Matrix.mul_assoc]
    rw [hu₁, Matrix.one_mul]
    exact hA.eigenvectorUnitary.2.1
  · rw [hA.spectral_theorem]
    simp [U', Matrix.mul_assoc]
    rfl
  rw [Matrix.IsHermitian.cfc_eq, this]
  rw [hA.cfc_eq, Matrix.IsHermitian.cfc.eq_1]
  simp only [Matrix.mul_assoc, conjTranspose_mul, star_eq_conjTranspose, U', D]
  exact isHermitian_mul_mul_conjTranspose _ hA

theorem cfc_conj_isometry (f : ℝ → ℝ) {u : Matrix d₂ d 𝕜}
    (hu₁ : u.Isometry) (hu₂ : uᴴ.Isometry) :
    cfc f (u * A * uᴴ) = u * (cfc f A) * uᴴ := by
  by_cases hA : A.IsHermitian
  · exact cfc_conj_isometry' hA f hu₁ hu₂
  rw [cfc_apply_of_not_predicate, cfc_apply_of_not_predicate]
  · simp
  · exact hA
  · contrapose! hA
    convert isHermitian_conjTranspose_mul_mul u hA
    have hu₃ : uᴴ * u = 1 := by simpa [Isometry] using hu₁
    simp only [Matrix.mul_assoc, hu₃]
    simp [← Matrix.mul_assoc, hu₃]

/-- The main target: conjugation by a unitary matrix commutes with the continuous
functional calculus. This is a key step in the proof of frame-independence of
quantum relative entropy.

Renamed from LQI's `Matrix.cfc_conj_unitary` to avoid collision with the lemma
of the same name in RA_AQFT_Proofs_v10.lean, which uses RA's custom
`UnitaryMatrix` type. See the integration recipe at the top of this file. -/
theorem cfc_conj_unitaryGroup (f : ℝ → ℝ) (u : unitaryGroup d 𝕜) :
    cfc f (u * A * u⁻¹) = u * (cfc f A) * u⁻¹ := by
  have hu := u.prop
  rw [mem_unitaryGroup_iff_isometry] at hu
  exact Matrix.cfc_conj_isometry f hu.left hu.right

/-- conjTranspose form of `cfc_conj_unitaryGroup`. Same content, alternate algebraic form. -/
theorem cfc_conj_unitaryGroup' (f : ℝ → ℝ) (u : unitaryGroup d 𝕜) :
    cfc f (uᴴ * A * u.val) = uᴴ * (cfc f A) * u.val := by
  simpa only [inv_inv] using cfc_conj_unitaryGroup f u⁻¹

end Matrix
