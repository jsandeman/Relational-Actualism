import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real

namespace RA_NativeDimensionality

open Real

/-- 
In a causal set/DAG, the maximal antichain (macroscopic graph cut) 
scales as N^((d-1)/d), where N is the macroscopic volume.
We cast d to Real before subtraction to ensure analytic behavior.
--/
noncomputable def cut_scaling (d : ℕ) (N : ℝ) : ℝ :=
  N ^ (((d : ℝ) - 1) / (d : ℝ))

/-- 
The baseline ledger capacity required to support a d-dimensional 
topology is normalized to the d=4 baseline.
--/
noncomputable def required_capacity (d : ℕ) (N : ℝ) : ℝ :=
  cut_scaling d N / cut_scaling 4 N

/-- 
LEMMA: The 5D Combinatorial Explosion.
For a strictly macroscopic graph (N > 1), the relative severance 
cost of a 5D topology is strictly greater than 1.
--/
lemma explosion_of_d5 (N : ℝ) (hN : N > 1) : 
  required_capacity 5 N > 1 :=
by
  unfold required_capacity
  
  -- Evaluate the scaling functions completely before substitution
  have hd5 : cut_scaling 5 N = N ^ (4 / 5 : ℝ) := by
    unfold cut_scaling; norm_num
  have hd4 : cut_scaling 4 N = N ^ (3 / 4 : ℝ) := by
    unfold cut_scaling; norm_num
  rw [hd5, hd4]
  
  -- Merge the division into the exponent using rpow_sub (right-to-left)
  have hN_pos : N > 0 := by linarith
  rw [← Real.rpow_sub hN_pos (4/5) (3/4)]
  
  -- Simplify the exponent subtraction
  have h3 : (4 : ℝ) / 5 - 3 / 4 = 1 / 20 := by norm_num
  rw [h3]
  
  -- Base > 1 and Exponent > 0 means Result > 1
  exact Real.one_lt_rpow hN (by norm_num)

/-- 
THEOREM: Generalized Combinatorial Severance Cost.
For any dimension d > 4 and macroscopic volume N > 1, the ledger 
capacity required to support the graph cut strictly exceeds 1.
--/
theorem macroscopic_ledger_demand (d : ℕ) (N : ℝ) 
  (hN : N > 1) (hd : d > 4) : 
  required_capacity d N > 1 :=
by
  unfold required_capacity
  
  -- Evaluate the d=4 baseline completely
  have hd4 : cut_scaling 4 N = N ^ (3 / 4 : ℝ) := by
    unfold cut_scaling; norm_num
  rw [hd4]
  unfold cut_scaling
  
  -- Merge the division into the exponent
  have hN_pos : N > 0 := by linarith
  rw [← Real.rpow_sub hN_pos (((d : ℝ) - 1) / (d : ℝ)) (3/4)]
  
  -- Prove the resulting exponent is positive using field_simp to handle the fractions
  have h_exp_pos : (((d : ℝ) - 1) / (d : ℝ)) - 3 / 4 > 0 := by
    have hd_real : (d : ℝ) > 4 := by exact_mod_cast hd
    have hz : (d : ℝ) ≠ 0 := by linarith
    
    -- Algebraically reshape the fraction: (d-1)/d - 3/4 = (d-4)/4d
    have step1 : (((d : ℝ) - 1) / (d : ℝ)) - 3 / 4 = ((d : ℝ) - 4) / (4 * (d : ℝ)) := by
      field_simp [hz]
      ring
    rw [step1]
    
    -- Prove the numerator and denominator are both strictly positive
    have hnum : (d : ℝ) - 4 > 0 := by linarith
    have hden : 4 * (d : ℝ) > 0 := by linarith
    
    -- A positive divided by a positive is positive
    exact div_pos hnum hden
      
  exact Real.one_lt_rpow hN h_exp_pos

end RA_NativeDimensionality