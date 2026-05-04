import RA_O14_ArithmeticCore
import RA_D1_NativeDimensionality

namespace RA_Complexity

open RA_NativeDimensionality

/--
The Internal Core (Assembly Depth):
A living or complex system is defined by its deep sequential history. 
We model the core as a motif dominated by N4 (persistent sequential depth),
representing the "assembly depth" or memory of the system.
--/
def internal_core (depth : Nat) : MotifVector :=
  [1, 0, 0, depth]

/--
The Causal Firewall (Markov Blanket equivalent):
The firewall is a specific boundary motif that sits between the internal core 
and the environment. Its function is to intercept environmental potentia drag (ρ).
It must possess enough native branching capacity (N2) to absorb the negative 
penalty of ρ without transferring that instability to the core.
--/
def shielded_system (ρ blanket_capacity depth : Nat) : MotifVector :=
  -- The blanket absorbs ρ on N1, uses blanket_capacity on N2 to remain solvent,
  -- and protects the deep sequential core (N4).
  [1 + ρ, blanket_capacity, 0, depth]

/--
THEOREM: The Causal Firewall Threshold (Native RA Version).
If a complex system is exposed to massive environmental noise (ρ), its internal 
core can only avoid causal severance (S_BDG ≤ 0) if it is wrapped in a blanket 
whose structural capacity (9 * blanket_capacity) strictly exceeds the environmental 
drag relative to its depth.
--/
theorem causal_firewall_persistence (ρ blanket_capacity depth : Nat) 
  (h_shield : 9 * blanket_capacity + 8 * depth > ρ) :
  evaluate_kernel bdg_coeffs (shielded_system ρ blanket_capacity depth) > 0 :=
by
  unfold shielded_system bdg_coeffs evaluate_kernel
  
  -- The BDG evaluation natively computes to:
  -- 1(1) - 1(1+ρ) + 9(blanket_capacity) - 16(0) + 8(depth)
  -- = 9 * blanket_capacity + 8 * depth - ρ
  simp
  
  -- Because the shield + depth capacity > ρ, the system remains strictly positive (solvent).
  omega

/--
LEMMA: Unshielded Collapse (The Fate of Boltzmann Brains).
If a deep internal core is exposed to environmental noise without an adequate 
firewall (blanket_capacity = 0, ρ ≥ 8 * depth), the structure instantly 
severs. Deep complexity cannot survive without a boundary.
--/
lemma unshielded_collapse (ρ depth : Nat) (h_overwhelmed : ρ ≥ 8 * depth) :
  evaluate_kernel bdg_coeffs (shielded_system ρ 0 depth) ≤ 0 :=
by
  unfold shielded_system bdg_coeffs evaluate_kernel
  simp
  -- Now that depth is correctly preserved in the equation, omega handles the 
  -- algebraic threshold (ρ ≥ 8 * depth) flawlessly.
  omega

end RA_Complexity