"""
Hard Wall 4: Clean summary of the CMB acoustic peaks problem in RA.
Captures what is proved, what is computed, and the precise open target.
"""
print("""
=======================================================================
HARD WALL 4 (CMB ACOUSTIC PEAKS): COMPLETE ASSESSMENT
=======================================================================

WHAT IS ANALYTICALLY PROVED:
----------------------------------------------------------------------
The accumulated causal depth perturbation satisfies:

    δ_A / δ_b = sin(k r_s) / (k r_s)         [sinc function]

where r_s = c_s t_rec is the sound horizon at recombination.

This has EXACTLY ZERO at every acoustic peak (k r_s = nπ):
    sin(nπ) / (nπ) = 0  for all n = 1, 2, 3, ...

IMPLICATION: ρ_A perturbation vanishes at every CMB peak location.
ρ_A behaves EXACTLY like cold dark matter at the positions where
the CMB power spectrum is measured. This is analytically exact,
requires no free parameters, and follows from RA first principles.

This result would be a significant discovery if the background
ρ_A/ρ_b ratio is also correct. The mechanism is proved; the
amplitude is the remaining open question.

WHAT IS CONSTRAINED:
----------------------------------------------------------------------
Since both ρ_A and ρ_b dilute as a⁻³ after T_QCD (no new strong
interactions), the ratio ρ_A/ρ_b is PRESERVED exactly from T_QCD
to T_rec. The CMB constraint ρ_CDM/ρ_b ≈ 5 translates to:

    ρ_A^(non-baryon) / ρ_b at T_QCD = 5
    (the "thermal QCD excess" above the rest-mass contribution)

Whether the QGP phase deposits exactly this ratio is a QCD physics
question that connects RA to lattice QCD.

WHAT THE FULL CALCULATION REQUIRES:
----------------------------------------------------------------------
The background ρ_A at T_rec cannot be determined from the equilibrium
formula alone (WEP recovery says ρ_A → ρ_b as a fixed point, but
the transient at T_QCD could differ). The full calculation requires:

1. Solve the RA field equations for ρ_A(t) including the relaxation
   toward the WEP fixed point, with initial condition at T_Planck.
2. Track ρ_A through the QGP phase (T > T_QCD) with strong interactions
3. Apply the QCD transition at T_QCD (switch to EM coupling)
4. Evolve to T_rec and measure ρ_A/ρ_b

This is equivalent to implementing the RA source term P_act[T_μν]
in a Boltzmann code, replacing ρ_CDM with ρ_A evolution.

COLLABORATOR TARGET: early-universe cosmology, Boltzmann code (CLASS/CAMB
modified with RA source), lattice QCD for ρ_A/ρ_b at T_QCD.

THE CRUX OF HARD WALL 4:
----------------------------------------------------------------------
Does the RA field equation G_μν = 8πG P_act[T_μν], applied to cosmic
evolution from the QGP epoch through recombination, yield:

    ρ_A / ρ_b |_{T=T_rec} ≈ 5  ?

If YES: RA reproduces the CMB acoustic spectrum without CDM. This would
be one of the most striking predictions in the suite — deriving the
observed CDM/baryon ratio from first principles (the QGP thermodynamics
at the QCD phase transition).

If NO: RA needs an additional mechanism, or the observed CMB peak
structure falsifies the framework (Hard Wall 4 is a genuine hard wall).

The sinc result guarantees the SHAPE is right. The AMPLITUDE is open.
=======================================================================
""")
