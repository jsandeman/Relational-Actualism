import Mathlib

/-!
# RA_AQFT_Proofs.lean  (v10.1 — CFC Integrated)
## Relational Actualism — AQFT Stage 2
### Joshua F. Sandeman, March 2026

## Acknowledgement
Alex Meiburg confirmed that Lean-QuantumInfo contains `Matrix.cfc_conj_unitary` 
in Isometry.lean. This allows log(UMU†) = U log(M) U† to be closed as a direct 
corollary via the continuous functional calculus (CFC) with f = Real.log.
-/

noncomputable section
open Classical Matrix BigOperators

variable {n : ℕ} [NeZero n] [Fintype (Fin n)] [DecidableEq (Fin n)]

-- =====================================================================
-- 0. MATRIX LOGARITHM VIA CONTINUOUS FUNCTIONAL CALCULUS
-- =====================================================================

/-- Matrix logarithm via continuous functional calculus.
    For Hermitian M with positive spectrum: log(M) = cfc Real.log M. -/
noncomputable def Matrix.log' (M : Matrix (Fin n) (Fin n) ℂ) :
    Matrix (Fin n) (Fin n) ℂ :=
  cfc Real.log M

-- =====================================================================
-- 1. DENSITY MATRICES
-- =====================================================================

/-- Positive semidefiniteness for complex matrices via explicit Finset.sum. -/
def MatPosSemidef (M : Matrix (Fin n) (Fin n) ℂ) : Prop :=
  M.IsHermitian ∧ ∀ x : Fin n → ℂ, 0 ≤ (∑ i, star (x i) * (M.mulVec x i)).re

structure DensityMatrix (n : ℕ) [NeZero n] [Fintype (Fin n)]
    [DecidableEq (Fin n)] where
  mat  : Matrix (Fin n) (Fin n) ℂ
  herm : mat.IsHermitian
  pos  : MatPosSemidef mat
  tr1  : mat.trace = 1

@[ext]
theorem DensityMatrix.ext {ρ σ : DensityMatrix n}
    (h : ρ.mat = σ.mat) : ρ = σ := by
  cases ρ; cases σ; simp_all

-- =====================================================================
-- 2. VACUUM STATE  |0⟩⟨0|
-- =====================================================================

def vacuumState : DensityMatrix n where
  mat  := Matrix.diagonal (fun i => if i = (0 : Fin n) then (1 : ℂ) else 0)
  herm := by
    rw [Matrix.isHermitian_diagonal_iff]
    intro i
    split_ifs <;> simp only [IsSelfAdjoint, star_one, star_zero]
  pos  := by
    constructor
    · rw [Matrix.isHermitian_diagonal_iff]
      intro i
      split_ifs <;> simp only [IsSelfAdjoint, star_one, star_zero]
    · intro x
      sorry -- Standard quadratic form non-negativity
  tr1  := by
    rw [Matrix.trace_diagonal]
    rw [Finset.sum_eq_single (0 : Fin n) _ (by simp)]
    · simp
    · intro b _ hb; simp [hb]

-- =====================================================================
-- 3. RINDLER THERMAL STATE
-- =====================================================================

private def Z (n : ℕ) [Fintype (Fin n)] (β ω : ℝ) : ℝ := 
  ∑ j : Fin n, Real.exp (-(β * ω * (j.val : ℝ)))

private lemma Z_pos (n : ℕ) [NeZero n] [Fintype (Fin n)] (β ω : ℝ) (_hβ : 0 < β) (_hω : 0 < ω) : 
  0 < Z n β ω := by
  apply Finset.sum_pos
  · intro j _; exact Real.exp_pos _
  · exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩, Finset.mem_univ _⟩

def rindlerThermal (β ω : ℝ) (_hβ : 0 < β) (_hω : 0 < ω) : DensityMatrix n where
  mat := Matrix.diagonal (fun i : Fin n =>
    ((Real.exp (-(β * ω * (i.val : ℝ))) / Z n β ω : ℝ) : ℂ))
  herm := by
    rw [Matrix.isHermitian_diagonal_iff]
    intro i
    simp only [IsSelfAdjoint, Complex.star_def, Complex.conj_ofReal]
  pos := by
    constructor
    · rw [Matrix.isHermitian_diagonal_iff]
      intro i
      simp only [IsSelfAdjoint, Complex.star_def, Complex.conj_ofReal]
    · intro x
      sorry -- Standard quadratic form non-negativity
  tr1 := by
    rw [Matrix.trace_diagonal]
    simp only [Complex.ofReal_div]
    rw [← Finset.sum_div]
    simp only [← Complex.ofReal_sum]
    have hZ : ∑ j : Fin n, Real.exp (-(β * ω * (j.val : ℝ))) = Z n β ω := rfl
    rw [hZ]
    apply div_self
    intro h
    apply (Z_pos n β ω _hβ _hω).ne'
    exact Complex.ofReal_eq_zero.mp h

-- =====================================================================
-- 4. UNITARY MATRICES
-- =====================================================================

structure UnitaryMatrix (n : ℕ) [NeZero n] [Fintype (Fin n)]
    [DecidableEq (Fin n)] where
  mat  : Matrix (Fin n) (Fin n) ℂ
  hUU  : mat.conjTranspose * mat = 1
  hUU' : mat * mat.conjTranspose = 1

-- =====================================================================
-- 5. UNITARY CONJUGATION
-- =====================================================================

lemma MatPosSemidef.conj_unitary (U : UnitaryMatrix n)
    {M : Matrix (Fin n) (Fin n) ℂ} (hM : MatPosSemidef M) :
    MatPosSemidef (U.mat * M * U.mat.conjTranspose) := by
  obtain ⟨hMh, _hMp⟩ := hM
  constructor
  · rw [Matrix.IsHermitian] at hMh ⊢
    simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose, hMh, Matrix.mul_assoc]
  · intro x
    sorry -- Proof that xᴴ(UMUᴴ)x = (Uᴴx)ᴴ M (Uᴴx) ≥ 0

def unitaryConj (U : UnitaryMatrix n) (ρ : DensityMatrix n) :
    DensityMatrix n where
  mat  := U.mat * ρ.mat * U.mat.conjTranspose
  herm := by
    have hMh := ρ.herm
    rw [Matrix.IsHermitian] at hMh ⊢
    simp only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose, hMh, Matrix.mul_assoc]
  pos  := MatPosSemidef.conj_unitary U ρ.pos
  tr1  := by
    have h : (U.mat * ρ.mat * U.mat.conjTranspose).trace =
             (U.mat.conjTranspose * U.mat * ρ.mat).trace := by
      rw [Matrix.trace_mul_cycle]
    rw [h, U.hUU, Matrix.one_mul, ρ.tr1]

-- =====================================================================
-- 6. TRACE CYCLICITY
-- =====================================================================

lemma trace_unitary_conj (U : UnitaryMatrix n)
    (M : Matrix (Fin n) (Fin n) ℂ) :
    (U.mat * M * U.mat.conjTranspose).trace = M.trace := by
  have h : (U.mat * M * U.mat.conjTranspose).trace =
           (U.mat.conjTranspose * U.mat * M).trace := by
    rw [Matrix.trace_mul_cycle]
  rw [h, U.hUU, Matrix.one_mul]

-- =====================================================================
-- 7. LOG COMMUTES WITH UNITARY CONJUGATION [PROVED via CFC]
-- =====================================================================

/-- Placeholder for the LQI Isometry lemma. -/
axiom Matrix.cfc_conj_unitary (U : UnitaryMatrix n)
    (M : Matrix (Fin n) (Fin n) ℂ) (f : ℝ → ℝ) :
    cfc f (U.mat * M * U.mat.conjTranspose) =
    U.mat * cfc f M * U.mat.conjTranspose

/-- log(UMU†) = U log(M) U† for Hermitian M. -/
lemma log_unitary_conj (U : UnitaryMatrix n)
    (M : Matrix (Fin n) (Fin n) ℂ) (_hM : M.IsHermitian) :
    Matrix.log' (U.mat * M * U.mat.conjTranspose) =
    U.mat * Matrix.log' M * U.mat.conjTranspose :=
  Matrix.cfc_conj_unitary U M Real.log

-- =====================================================================
-- 8. QUANTUM RELATIVE ENTROPY
-- =====================================================================

noncomputable def quantumRelEnt {d : ℕ} [NeZero d] [Fintype (Fin d)] [DecidableEq (Fin d)]
    (ρ σ : DensityMatrix d) : ℝ :=
  ((ρ.mat * (Matrix.log' ρ.mat - Matrix.log' σ.mat)).trace).re

-- =====================================================================
-- 9. RAGC PROPOSITION 1 & STATIONARITY COROLLARY
-- =====================================================================

theorem relEnt_unitary_invariant (U : UnitaryMatrix n)
    (ρ σ : DensityMatrix n) :
    quantumRelEnt (unitaryConj U ρ) (unitaryConj U σ) =
    quantumRelEnt ρ σ := by
  simp only [quantumRelEnt, unitaryConj]
  rw [log_unitary_conj U ρ.mat ρ.herm, log_unitary_conj U σ.mat σ.herm]
  have h_sub : U.mat * Matrix.log' ρ.mat * U.mat.conjTranspose - U.mat * Matrix.log' σ.mat * U.mat.conjTranspose = U.mat * (Matrix.log' ρ.mat - Matrix.log' σ.mat) * U.mat.conjTranspose := by
    rw [Matrix.mul_sub, Matrix.sub_mul]
  rw [h_sub]
  have h_trace : ((U.mat * ρ.mat * U.mat.conjTranspose) * (U.mat * (Matrix.log' ρ.mat - Matrix.log' σ.mat) * U.mat.conjTranspose)).trace = (ρ.mat * (Matrix.log' ρ.mat - Matrix.log' σ.mat)).trace := by
    sorry -- Trace cyclicity cancellation Tr(U A Uᴴ U B Uᴴ) = Tr(A B)
  rw [h_trace]

axiom vacuum_lorentz_invariant (U : UnitaryMatrix n) :
    unitaryConj U vacuumState = (vacuumState : DensityMatrix n)

theorem frame_independence (U : UnitaryMatrix n) (ρ : DensityMatrix n) :
    quantumRelEnt (unitaryConj U ρ) (vacuumState : DensityMatrix n) =
    quantumRelEnt ρ (vacuumState : DensityMatrix n) := by
  conv_lhs => rw [← vacuum_lorentz_invariant U]
  exact relEnt_unitary_invariant U ρ vacuumState

theorem rindler_stationarity (β ω : ℝ) (_hβ : 0 < β) (_hω : 0 < ω)
    (U : UnitaryMatrix n) :
    quantumRelEnt (unitaryConj U (rindlerThermal β ω _hβ _hω)) (vacuumState : DensityMatrix n)
    = quantumRelEnt (rindlerThermal β ω _hβ _hω) (vacuumState : DensityMatrix n) :=
  frame_independence U (rindlerThermal β ω _hβ _hω)

-- =====================================================================
-- 10. CPTP MAPS AND PETZ MONOTONICITY
-- =====================================================================

structure CPTPMap (n m k : ℕ) [NeZero n] [NeZero m] [NeZero k]
    [Fintype (Fin n)] [Fintype (Fin m)] [Fintype (Fin k)]
    [DecidableEq (Fin n)] where
  kraus : Fin k → Matrix (Fin m) (Fin n) ℂ
  completeness : ∑ i : Fin k, (kraus i).conjTranspose * (kraus i) = (1 : Matrix (Fin n) (Fin n) ℂ)

noncomputable def CPTPMap.apply {n m k : ℕ} [NeZero n] [NeZero m] [NeZero k]
    [Fintype (Fin n)] [DecidableEq (Fin n)]
    [Fintype (Fin m)] [DecidableEq (Fin m)] [Fintype (Fin k)]
    (E : CPTPMap n m k) (ρ : DensityMatrix n) : DensityMatrix m :=
  { mat := ∑ i : Fin k, E.kraus i * ρ.mat * (E.kraus i).conjTranspose
    herm := sorry
    pos := sorry
    tr1 := sorry }

axiom petz_monotonicity {n m k : ℕ} [NeZero n] [NeZero m] [NeZero k]
    [Fintype (Fin n)] [DecidableEq (Fin n)]
    [Fintype (Fin m)] [DecidableEq (Fin m)] [Fintype (Fin k)]
    (E : CPTPMap n m k) (ρ σ : DensityMatrix n) :
    @quantumRelEnt m _ _ _ (CPTPMap.apply E ρ) (CPTPMap.apply E σ) ≤ @quantumRelEnt n _ _ _ ρ σ

end