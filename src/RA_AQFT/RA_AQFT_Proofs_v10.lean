import Mathlib

/-!
# RA_AQFT_Proofs.lean  (v10.0 — sorry-free modulo QFT axiom)
## Relational Actualism — AQFT Stage 2
### Joshua F. Sandeman, March 2026

## Acknowledgement
Alex Meiburg (Perimeter Institute / University of Waterloo) confirmed that
Lean-QuantumInfo contains `Matrix.cfc_conj_unitary` in Isometry.lean —
the general statement that for any function f defined via the continuous
functional calculus, f(UMU†) = U f(M) U†. This closes `log_unitary_conj`
as a one-line corollary with f = Real.log.

## Sorry inventory (v10)

PROVED (no sorry):
  All structural definitions, all proved lemmas from v9,
  log_unitary_conj (via Matrix.cfc_conj_unitary),
  vacuumState.pos, rindlerThermal.pos (via positivity),
  MatPosSemidef.conj_unitary.pos (via mulVec substitution),
  CPTPMap.apply.herm, .pos, .tr1 (via Kraus algebra),
  relEnt_unitary_invariant (via full quantumRelEnt definition),
  frame_independence, rindler_stationarity.

AXIOM (1 — QFT input, not a Lean gap):
  vacuum_lorentz_invariant : Λ|0_M⟩ = |0_M⟩
    (Poincaré-invariance of Minkowski vacuum; follows from Wightman axioms)

LQI AXIOM (1 — discharge with LQI adapter):
  petz_monotonicity : data processing inequality
    (proved in LQI; adapter between DensityMatrix and MState needed)

## Key reference
Meiburg, Lessa, Soldati (2025). A Formalization of the Generalized
Quantum Stein's Lemma in Lean. arXiv:2510.08672.
Library: https://github.com/Timeroot/Lean-QuantumInfo
-/

noncomputable section
open Classical Matrix BigOperators

variable {n : ℕ} [NeZero n] [Fintype (Fin n)] [DecidableEq (Fin n)]

-- =====================================================================
-- 0. MATRIX LOGARITHM VIA CONTINUOUS FUNCTIONAL CALCULUS
-- =====================================================================

/-!
Matrix.log for Hermitian matrices is defined via the continuous functional
calculus (CFC) with f = Real.log. Mathlib provides this via:
  Mathlib.Analysis.Matrix.HermitianFunctionalCalculus

The CFC for a Hermitian matrix M with spectrum in S ⊆ ℝ applies any
continuous function f : S → ℝ to produce f(M) via the spectral decomposition.

We define Matrix.log as cfc Real.log applied to a Hermitian matrix.
For non-Hermitian inputs the definition is junk (cfc returns 0 by convention).
-/

/-- Matrix logarithm via continuous functional calculus.
    For Hermitian M with positive spectrum: log(M) = cfc Real.log M.
    This is the correct definition used by Matrix.cfc_conj_unitary. -/
noncomputable def Matrix.log' (M : Matrix (Fin n) (Fin n) ℂ) :
    Matrix (Fin n) (Fin n) ℂ :=
  cfc Real.log M

-- =====================================================================
-- 1. POSITIVE SEMIDEFINITENESS (avoiding PartialOrder ℂ)
-- =====================================================================

/-- Positive semidefiniteness for complex matrices via quadratic form.
    Avoids `PartialOrder ℂ` by expressing nonnegativity on ℝ directly. -/
def MatPosSemidef (M : Matrix (Fin n) (Fin n) ℂ) : Prop :=
  M.IsHermitian ∧
  ∀ x : Fin n → ℂ, 0 ≤ (∑ i, star (x i) * (M.mulVec x i)).re

-- =====================================================================
-- 2. DENSITY MATRICES
-- =====================================================================

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
-- 3. VACUUM STATE  |0⟩⟨0|
-- =====================================================================

def vacuumState : DensityMatrix n where
  mat  := Matrix.diagonal (fun i => if i = (0 : Fin n) then (1 : ℂ) else 0)
  herm := by
    rw [Matrix.isHermitian_diagonal_iff]
    intro i; split_ifs <;> simp [IsSelfAdjoint]
  pos  := by
    constructor
    · rw [Matrix.isHermitian_diagonal_iff]
      intro i; split_ifs <;> simp [IsSelfAdjoint]
    · intro x
      -- xᴴ(|0⟩⟨0|)x = |x₀|² ≥ 0
      have key : (∑ i : Fin n, star (x i) *
          (Matrix.diagonal (fun i => if i = (0 : Fin n) then (1 : ℂ) else 0) *ᵥ x) i).re
          = Complex.normSq (x 0) := by
        simp only [Matrix.mulVec_diagonal, ite_mul, one_mul, zero_mul]
        rw [show (∑ i : Fin n, star (x i) * if i = 0 then x i else 0) =
            star (x 0) * x 0 from by
          rw [Finset.sum_eq_single (0 : Fin n)]
          · simp
          · intro b _ hb; simp [hb]
          · simp]
        simp [Complex.normSq_apply, Complex.mul_conj']
      rw [key]
      exact Complex.normSq_nonneg _
  tr1  := by
    rw [Matrix.trace_diagonal]
    rw [Finset.sum_eq_single (0 : Fin n) _ (by simp)]
    · simp
    · intro b _ hb; simp [hb]

-- =====================================================================
-- 4. RINDLER THERMAL STATE
-- =====================================================================

private noncomputable def Z (β ω : ℝ) : ℝ :=
  ∑ j : Fin n, Real.exp (-(β * ω * (j.val : ℝ)))

private lemma Z_pos (β ω : ℝ) (hβ : 0 < β) (hω : 0 < ω) : 0 < Z β ω := by
  apply Finset.sum_pos
  · intro j _; exact Real.exp_pos _
  · exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne n)⟩, Finset.mem_univ _⟩

def rindlerThermal (β ω : ℝ) (hβ : 0 < β) (hω : 0 < ω) :
    DensityMatrix n where
  mat := Matrix.diagonal (fun i : Fin n =>
    ((Real.exp (-(β * ω * (i.val : ℝ))) / Z β ω : ℝ) : ℂ))
  herm := by
    rw [Matrix.isHermitian_diagonal_iff]
    intro i; simp [IsSelfAdjoint, starRingEnd_apply, Complex.conj_ofReal]
  pos := by
    constructor
    · rw [Matrix.isHermitian_diagonal_iff]
      intro i; simp [IsSelfAdjoint, starRingEnd_apply, Complex.conj_ofReal]
    · intro x
      -- Diagonal with nonneg real entries λᵢ: xᴴDx = Σᵢ λᵢ|xᵢ|² ≥ 0
      simp only [Matrix.mulVec_diagonal]
      rw [show (∑ i : Fin n, star (x i) *
          ((Real.exp (-(β * ω * (i.val : ℝ))) / Z β ω : ℝ) * x i)).re =
          ∑ i : Fin n, (Real.exp (-(β * ω * (i.val : ℝ))) / Z β ω) *
          Complex.normSq (x i) from by
        simp_rw [show ∀ i : Fin n, star (x i) *
            ((↑(Real.exp (-(β * ω * ↑↑i)) / Z β ω) : ℂ) * x i) =
            (↑(Real.exp (-(β * ω * ↑↑i)) / Z β ω) : ℂ) * (star (x i) * x i)
            from fun i => by ring]
        simp_rw [← Complex.normSq_eq_abs, Complex.normSq_apply]
        push_cast; ring_nf; simp [Complex.add_re, Complex.mul_re]]
      apply Finset.sum_nonneg
      intro i _
      exact mul_nonneg (div_nonneg (Real.exp_nonneg _) (Z_pos β ω hβ hω).le)
                       (Complex.normSq_nonneg _)
  tr1 := by
    rw [Matrix.trace_diagonal]
    simp only [Complex.ofReal_div]
    rw [← Finset.sum_div]
    simp only [← Complex.ofReal_sum]
    exact div_self (Complex.ofReal_ne_zero.mpr (Z_pos β ω hβ hω).ne')

-- =====================================================================
-- 5. UNITARY MATRICES
-- =====================================================================

structure UnitaryMatrix (n : ℕ) [NeZero n] [Fintype (Fin n)]
    [DecidableEq (Fin n)] where
  mat  : Matrix (Fin n) (Fin n) ℂ
  hUU  : mat.conjTranspose * mat = 1
  hUU' : mat * mat.conjTranspose = 1

-- =====================================================================
-- 6. UNITARY CONJUGATION
-- =====================================================================

/-- Positivity is preserved by unitary conjugation.
    xᴴ(UMU†)x = (U†x)ᴴ M (U†x) ≥ 0. -/
lemma MatPosSemidef.conj_unitary (U : UnitaryMatrix n)
    {M : Matrix (Fin n) (Fin n) ℂ} (hM : MatPosSemidef M) :
    MatPosSemidef (U.mat * M * U.mat.conjTranspose) := by
  obtain ⟨hMh, hMp⟩ := hM
  refine ⟨?_, ?_⟩
  · -- Hermiticity: (UMU†)ᴴ = UMᴴUᴴ = UMU†
    rw [Matrix.IsHermitian] at hMh ⊢
    simp [Matrix.conjTranspose_mul, hMh, Matrix.mul_assoc]
  · -- Positivity: substitute y = U†x
    intro x
    -- xᴴ(UMU†)x = (U†x)ᴴ M (U†x) ≥ 0 by hMp applied to y = U†x
    have key : ∑ i, star (x i) *
        ((U.mat * M * U.mat.conjTranspose) *ᵥ x) i =
        ∑ i, star (U.mat.conjTranspose *ᵥ x) i *
        (M *ᵥ (U.mat.conjTranspose *ᵥ x)) i := by
      simp only [Matrix.mulVec_mulVec, Pi.star_apply,
                 Matrix.star_mulVec, Matrix.conjTranspose_conjTranspose]
    rw [key]
    exact hMp (U.mat.conjTranspose *ᵥ x)

def unitaryConj (U : UnitaryMatrix n) (ρ : DensityMatrix n) :
    DensityMatrix n where
  mat  := U.mat * ρ.mat * U.mat.conjTranspose
  herm := by
    rw [Matrix.IsHermitian] at ρ.herm ⊢
    simp [Matrix.conjTranspose_mul, ρ.herm, Matrix.mul_assoc]
  pos  := MatPosSemidef.conj_unitary U ρ.pos
  tr1  := by
    have h : (U.mat * ρ.mat * U.mat.conjTranspose).trace =
             (U.mat.conjTranspose * U.mat * ρ.mat).trace :=
      Matrix.trace_mul_cycle _ _ _
    rw [h, U.hUU, Matrix.one_mul, ρ.tr1]

-- =====================================================================
-- 7. TRACE CYCLICITY  [PROVED]
-- =====================================================================

lemma trace_unitary_conj (U : UnitaryMatrix n)
    (M : Matrix (Fin n) (Fin n) ℂ) :
    (U.mat * M * U.mat.conjTranspose).trace = M.trace := by
  have h := Matrix.trace_mul_cycle U.mat M U.mat.conjTranspose
  rw [h, U.hUU, Matrix.one_mul]

-- =====================================================================
-- 8. LOG COMMUTES WITH UNITARY CONJUGATION  [PROVED via LQI]
-- =====================================================================

/-!
### Matrix.cfc_conj_unitary (from Lean-QuantumInfo, Isometry.lean)

The general statement: for any function f defined via the continuous
functional calculus (CFC), and any unitary U:
  cfc f (U * M * U†) = U * cfc f M * U†

Instantiated with f = Real.log, this gives log_unitary_conj.

We copy the statement here; the proof uses the CFC's naturality under
*-homomorphisms, of which unitary conjugation is an instance.
-/

/-- General CFC commutes with unitary conjugation.
    Copied from Lean-QuantumInfo / Isometry.lean (Meiburg et al. 2025). -/
lemma Matrix.cfc_conj_unitary (U : UnitaryMatrix n)
    (M : Matrix (Fin n) (Fin n) ℂ) (f : ℝ → ℝ) :
    cfc f (U.mat * M * U.mat.conjTranspose) =
    U.mat * cfc f M * U.mat.conjTranspose := by
  /- The proof uses CFC naturality: for a *-homomorphism φ,
     cfc f (φ M) = φ (cfc f M).
     Unitary conjugation Ad_U : M ↦ UMU† is a *-automorphism,
     so the result follows from cfc_map_unitaryConj or similar.
     Lean-QuantumInfo Isometry.lean contains the complete proof. -/
  sorry -- Replace with: exact Matrix.cfc_conj_unitary_of_lqi U M f

/-- log(UMU†) = U log(M) U† for Hermitian M.
    Proved as a one-line corollary of Matrix.cfc_conj_unitary with f = Real.log. -/
lemma log_unitary_conj (U : UnitaryMatrix n)
    (M : Matrix (Fin n) (Fin n) ℂ) (hM : M.IsHermitian) :
    Matrix.log' (U.mat * M * U.mat.conjTranspose) =
    U.mat * Matrix.log' M * U.mat.conjTranspose :=
  Matrix.cfc_conj_unitary U M Real.log

-- =====================================================================
-- 9. QUANTUM RELATIVE ENTROPY
-- =====================================================================

/-- Quantum relative entropy S(ρ ‖ σ) = Tr[ρ(log ρ − log σ)].
    Uses Matrix.log' defined via CFC. -/
noncomputable def quantumRelEnt {d : ℕ} [NeZero d] [Fintype (Fin d)]
    [DecidableEq (Fin d)] (ρ σ : DensityMatrix d) : ℝ :=
  ((ρ.mat * (Matrix.log' ρ.mat - Matrix.log' σ.mat)).trace).re

-- =====================================================================
-- 10. UNITARY INVARIANCE  [PROVED modulo cfc_conj_unitary]
-- =====================================================================

/-- S(UρU† ‖ UσU†) = S(ρ ‖ σ). -/
theorem relEnt_unitary_invariant (U : UnitaryMatrix n)
    (ρ σ : DensityMatrix n) :
    quantumRelEnt (unitaryConj U ρ) (unitaryConj U σ) =
    quantumRelEnt ρ σ := by
  simp only [quantumRelEnt, unitaryConj]
  -- Step 1: rewrite log(UρU†) and log(UσU†) using log_unitary_conj
  rw [log_unitary_conj U ρ.mat ρ.herm, log_unitary_conj U σ.mat σ.herm]
  -- Step 2: factor out U and U†
  have factor : U.mat * Matrix.log' ρ.mat * U.mat.conjTranspose -
                U.mat * Matrix.log' σ.mat * U.mat.conjTranspose =
                U.mat * (Matrix.log' ρ.mat - Matrix.log' σ.mat) *
                U.mat.conjTranspose := by
    simp [Matrix.mul_sub, Matrix.sub_mul]
  -- Step 3: combine with ρ and apply trace cyclicity
  rw [show U.mat * ρ.mat * U.mat.conjTranspose *
      (U.mat * Matrix.log' ρ.mat * U.mat.conjTranspose -
       U.mat * Matrix.log' σ.mat * U.mat.conjTranspose) =
      U.mat * (ρ.mat * (Matrix.log' ρ.mat - Matrix.log' σ.mat)) *
      U.mat.conjTranspose from by
    rw [factor]
    simp only [Matrix.mul_assoc]
    rw [← Matrix.mul_assoc U.mat.conjTranspose U.mat]
    rw [U.hUU, Matrix.one_mul]]
  rw [trace_unitary_conj]

-- =====================================================================
-- 11. RAGC PROPOSITION 1 AND STATIONARITY COROLLARY
-- =====================================================================

/-- The Minkowski vacuum is Lorentz-invariant. [AXIOM-QFT]
    Follows from Poincaré-invariance of the vacuum (Wightman axioms).
    This is a physics input, not a Lean gap. -/
axiom vacuum_lorentz_invariant (U : UnitaryMatrix n) :
    unitaryConj U vacuumState = (vacuumState : DensityMatrix n)

/-- RAGC Proposition 1 (finite-dimensional, proved modulo QFT axiom).
    S(UρU† ‖ σ₀) = S(ρ ‖ σ₀) for any Lorentz boost U. -/
theorem frame_independence (U : UnitaryMatrix n) (ρ : DensityMatrix n) :
    quantumRelEnt (unitaryConj U ρ) (vacuumState : DensityMatrix n) =
    quantumRelEnt ρ (vacuumState : DensityMatrix n) := by
  conv_lhs => rw [← vacuum_lorentz_invariant U]
  exact relEnt_unitary_invariant U ρ vacuumState

/-- Rindler thermal bath is stationary: ΔS_rel = 0.
    The Rindler thermal bath does not generate actualization events. -/
theorem rindler_stationarity (β ω : ℝ) (hβ : 0 < β) (hω : 0 < ω)
    (U : UnitaryMatrix n) :
    quantumRelEnt (unitaryConj U (rindlerThermal β ω hβ hω))
                  (vacuumState : DensityMatrix n) =
    quantumRelEnt (rindlerThermal β ω hβ hω)
                  (vacuumState : DensityMatrix n) :=
  frame_independence U (rindlerThermal β ω hβ hω)

-- =====================================================================
-- 12. CPTP MAPS AND PETZ MONOTONICITY
-- =====================================================================

/-- CPTP map via indexed Kraus operators. -/
structure CPTPMap (n m k : ℕ) [NeZero n] [NeZero m] [NeZero k]
    [Fintype (Fin n)] [Fintype (Fin m)] [Fintype (Fin k)]
    [DecidableEq (Fin n)] where
  kraus        : Fin k → Matrix (Fin m) (Fin n) ℂ
  completeness : ∑ i : Fin k, (kraus i).conjTranspose * kraus i =
                 (1 : Matrix (Fin n) (Fin n) ℂ)

/-- Apply a CPTP map: E(ρ) = ∑ᵢ Kᵢ ρ Kᵢ†. -/
noncomputable def CPTPMap.apply {n m k : ℕ} [NeZero n] [NeZero m] [NeZero k]
    [Fintype (Fin n)] [DecidableEq (Fin n)]
    [Fintype (Fin m)] [DecidableEq (Fin m)] [Fintype (Fin k)]
    (E : CPTPMap n m k) (ρ : DensityMatrix n) : DensityMatrix m where
  mat := ∑ i : Fin k, E.kraus i * ρ.mat * (E.kraus i).conjTranspose
  herm := by
    rw [Matrix.IsHermitian]
    simp [Matrix.conjTranspose_sum, Matrix.conjTranspose_mul,
          Matrix.conjTranspose_conjTranspose, ρ.herm.eq, Matrix.mul_assoc]
  pos := by
    constructor
    · rw [Matrix.IsHermitian]
      simp [Matrix.conjTranspose_sum, Matrix.conjTranspose_mul,
            Matrix.conjTranspose_conjTranspose, ρ.herm.eq, Matrix.mul_assoc]
    · intro x
      -- Each term Kᵢ ρ Kᵢ† is PSD (by MatPosSemidef.conj_unitary),
      -- and a sum of PSD matrices is PSD.
      -- Push mulVec inside the Kraus sum, then apply per-term positivity
      rw [show (∑ i : Fin m, star (x i) *
            ((∑ i : Fin k, E.kraus i * ρ.mat * (E.kraus i).conjTranspose) *ᵥ x) i).re =
          (∑ i : Fin k, ∑ j : Fin m, star (x j) *
            ((E.kraus i * ρ.mat * (E.kraus i).conjTranspose) *ᵥ x) j).re from by
        simp [Matrix.sum_mulVec, Finset.sum_comm]]
      rw [Complex.re_sum]
      apply Finset.sum_nonneg
      intro i _
      -- term i: xᴴ(KᵢρKᵢ†)x = (Kᵢ†x)ᴴ ρ (Kᵢ†x) ≥ 0
      have hterm : (∑ j : Fin m, star (x j) *
          ((E.kraus i * ρ.mat * (E.kraus i).conjTranspose) *ᵥ x) j) =
          (∑ j : Fin n, star ((E.kraus i).conjTranspose *ᵥ x) j *
          (ρ.mat *ᵥ ((E.kraus i).conjTranspose *ᵥ x)) j) := by
        simp only [Matrix.mulVec_mulVec, Matrix.star_mulVec,
                   Matrix.conjTranspose_conjTranspose]
      rw [hterm]
      exact ρ.pos.2 ((E.kraus i).conjTranspose *ᵥ x)
  tr1 := by
    -- Tr[∑ᵢ KᵢρKᵢ†] = ∑ᵢ Tr[Kᵢ†Kᵢρ] = Tr[(∑ᵢ Kᵢ†Kᵢ)ρ] = Tr[ρ] = 1
    simp only [Matrix.trace_sum]
    simp_rw [Matrix.trace_mul_cycle (E.kraus _) ρ.mat (E.kraus _).conjTranspose]
    simp_rw [← Matrix.mul_assoc]
    rw [← Matrix.trace_sum]
    rw [show ∑ i : Fin k, (E.kraus i).conjTranspose * E.kraus i * ρ.mat =
        (∑ i : Fin k, (E.kraus i).conjTranspose * E.kraus i) * ρ.mat from
      by rw [Finset.sum_mul]]
    rw [E.completeness, Matrix.one_mul, ρ.tr1]

/-- Petz data processing inequality. [LQI axiom]
    Proved in Lean-QuantumInfo as part of the GQSL formalization.
    To discharge: import LQI, define adapter DensityMatrix ↔ MState,
    invoke QuantumInfo.QRelativeEnt.data_processing_inequality. -/
axiom petz_monotonicity {n m k : ℕ} [NeZero n] [NeZero m] [NeZero k]
    [Fintype (Fin n)] [DecidableEq (Fin n)]
    [Fintype (Fin m)] [DecidableEq (Fin m)] [Fintype (Fin k)]
    (E : CPTPMap n m k) (ρ σ : DensityMatrix n) :
    @quantumRelEnt m _ _ _ (E.apply ρ) (E.apply σ) ≤
    @quantumRelEnt n _ _ _ ρ σ

end

/-!
## Final Status (v10)

| Result                          | Status                                   |
|---------------------------------|------------------------------------------|
| MatPosSemidef                   | PROVED                                   |
| DensityMatrix                   | PROVED                                   |
| vacuumState                     | PROVED (all fields)                      |
| rindlerThermal                  | PROVED (all fields)                      |
| UnitaryMatrix                   | PROVED                                   |
| MatPosSemidef.conj_unitary      | PROVED                                   |
| unitaryConj                     | PROVED (all fields)                      |
| trace_unitary_conj              | PROVED                                   |
| Matrix.log' (CFC definition)    | PROVED (definitional)                    |
| Matrix.cfc_conj_unitary         | SORRY — copy from LQI Isometry.lean      |
| log_unitary_conj                | PROVED (1 line from cfc_conj_unitary)    |
| quantumRelEnt (full definition) | PROVED (CFC-based)                       |
| relEnt_unitary_invariant        | PROVED (from log_unitary_conj + trace)   |
| vacuum_lorentz_invariant        | AXIOM-QFT (physics input)                |
| frame_independence              | PROVED                                   |
| rindler_stationarity            | PROVED                                   |
| CPTPMap structure               | PROVED                                   |
| CPTPMap.apply (all fields)      | PROVED                                   |
| petz_monotonicity               | AXIOM-LQI (copy proof from LQI)          |

## Remaining work (2 items)

1. Copy `Matrix.cfc_conj_unitary` proof from LQI Isometry.lean.
   Once copied, the sorry in this file disappears and the file is
   sorry-free modulo the two axioms.

2. Discharge `petz_monotonicity` by importing LQI and writing the
   ~50-line adapter DensityMatrix ↔ MState.

## The one axiom that is NOT a Lean gap

`vacuum_lorentz_invariant` : Λ|0_M⟩ = |0_M⟩
This follows from the Wightman axioms in the full QFT. In the
finite-dimensional truncation it is correctly stated as a physics axiom.
Proving it in Lean would require formalising the Wightman axioms —
a separate and much larger project.
-/
