# Bandwidth-Partition Ratio: Derived from BDG
## λ̄_m/λ̄_exp = Ω_b(1+f₀)/(1−Ω_b(1+f₀)) = 0.463
### April 9, 2026

---

## Result

The bandwidth-partition ratio appearing in the RA Hubble tension
prediction is NOT a free parameter. It equals:

**λ̄_m/λ̄_exp = Ω_b(1+f₀) / (1 − Ω_b(1+f₀)) = 0.463**

where:
- f₀ = 5.42 (DERIVED from BDG integers: W_other/W_baryon × α_s(2m_p) = 17.32 × 0.312)
- Ω_b = 0.0493 (Planck 2018; initial condition set at Big Bang nucleation)

## Derivation

At cosmological scales, the total actualization bandwidth λ_total is
partitioned between matter-sourcing events (λ_m) and expansion-driving
events (λ_exp):

  λ_total = λ_m + λ_exp

The matter fraction of the total bandwidth equals the effective matter
density as a fraction of critical density:

  λ_m/λ_total = Ω_m^RA = Ω_b × (1 + f₀)

This is because:
1. Each baryon sources the metric with weight 1 (direct actualization)
2. Each baryon ALSO sources additional metric weight f₀ through the
   BDG bandwidth enhancement (the non-baryon path weights in the
   Poisson-CSG at μ=1)
3. f₀ = 5.42 plays the role that Ω_CDM/Ω_b plays in ΛCDM
4. In RA, there is no dark energy (Λ=0 structurally); the "expansion
   bandwidth" is the intrinsic growth rate of the causal graph

Therefore:
  Ω_m^RA = 0.0493 × 6.42 = 0.3165
  λ_m/λ_exp = 0.3165 / 0.6835 = 0.463

## Comparison with KBC calibration

The KBC void calibration gave λ̄_m/λ̄_exp ≈ 0.42, assuming |δ_KBC| = 0.20.
The 10% discrepancy is absorbed by the ±15-20% uncertainty on δ_KBC:

  For the derived ratio 0.463:
  |δ| needed for H_local = 73.0 km/s/Mpc:  0.179
  |δ| needed for H_local = 73.5 km/s/Mpc:  0.195

Both are within the observational uncertainty on δ_KBC.

## Hubble tension prediction (now parameter-free)

  H_local = H_CMB × (1 + 0.463 × |δ|)

  H_CMB = 67.4 km/s/Mpc (Planck 2018)
  |δ|   = independently measurable by DESI

  At |δ| = 0.18:  H = 73.0 km/s/Mpc
  At |δ| = 0.20:  H = 73.6 km/s/Mpc
  At |δ| = 0.30:  H = 76.8 km/s/Mpc (Eridanus prediction)

## What's derived vs what's observed

  DERIVED (from BDG, zero free parameters):
    f₀ = 5.42  (bandwidth enhancement factor)
    λ̄_m/λ̄_exp = Ω_b(1+f₀)/(1−Ω_b(1+f₀))  (the formula itself)

  OBSERVED (initial condition, not derivable from RA):
    Ω_b = 0.0493  (baryon asymmetry, set at Big Bang causal severance)

  INDEPENDENTLY MEASURABLE:
    |δ|  (void density contrast, from DESI/large-scale structure surveys)

## Key insight

The bandwidth partition is a COSMOLOGICAL-scale quantity, not a
Planck-scale quantity. Computing it at μ=1 (Planck density) gives the
wrong answer because the universe today is at μ << 1. The correct
approach is: the BDG integers determine f₀ (the enhancement factor);
Ω_b (the initial condition) determines how much baryon density there
is to enhance; and the ratio follows.

This removes the last calibrated parameter from the RA Hubble tension
prediction. The prediction is now: given the void density contrast δ
(measurable), the local Hubble constant follows with zero free
parameters.
