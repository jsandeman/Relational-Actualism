#!/usr/bin/env python3
"""
ra_source_law_reference.py

Reference scaffold for the RA weak-field source-law audit.

This file does three things:

1. Prints the current suite-primary weak-field source-law dictionary.
2. Evaluates the safe dense-regime benchmarks:
   - Solar-limb light deflection
   - Mercury perihelion advance
   - Generic thin-lens point-mass example
3. Checks the operator/sign ambiguity for power-law actualization profiles.

This is a reference implementation and audit scaffold, not a new proof.
"""

from __future__ import annotations
import math

# --- constants ---
G = 6.67430e-11
c = 299792458.0
M_sun = 1.98847e30
R_sun = 6.957e8
ARCSEC_PER_RAD = 206264.80624709636
pc = 3.085677581e16

# Mercury
a_mercury = 57.909e9
e_mercury = 0.205630
P_mercury_days = 87.9691
century_days = 36525.0

def light_deflection_arcsec(M: float, b: float, gamma: float = 1.0) -> float:
    alpha = 2.0 * (1.0 + gamma) * G * M / (b * c**2)
    return alpha * ARCSEC_PER_RAD

def perihelion_advance_arcsec_century(M: float, a: float, e: float, beta: float = 1.0, gamma: float = 1.0) -> float:
    dphi = ((2.0 + 2.0 * gamma - beta) / 3.0) * 6.0 * math.pi * G * M / (a * (1.0 - e**2) * c**2)
    arcsec_orbit = dphi * ARCSEC_PER_RAD
    return arcsec_orbit * (century_days / P_mercury_days)

def einstein_angle_arcsec(M_solar: float, D_l_Gpc: float, D_s_Gpc: float) -> tuple[float, float]:
    M = M_solar * M_sun
    D_l = D_l_Gpc * 1e9 * pc
    D_s = D_s_Gpc * 1e9 * pc
    D_ls = D_s - D_l
    theta_E = math.sqrt((4.0 * G * M / c**2) * (D_ls / (D_l * D_s)))
    theta_E_arcsec = theta_E * ARCSEC_PER_RAD
    R_E_kpc = D_l * theta_E / pc / 1000.0
    return theta_E_arcsec, R_E_kpc

def point_mass_images(u: float) -> tuple[float, float, float]:
    theta_plus = 0.5 * (u + math.sqrt(u*u + 4.0))
    theta_minus = 0.5 * (u - math.sqrt(u*u + 4.0))
    mu_tot = (u*u + 2.0) / (u * math.sqrt(u*u + 4.0))
    return theta_plus, theta_minus, mu_tot

def radial_laplacian_log_power(p: float, spatial_dim: int) -> str:
    coeff = p * (2 - spatial_dim)
    sign = "positive" if coeff > 0 else "zero" if coeff == 0 else "negative"
    return f"{coeff:+.0f}/r^2 ({sign})"

def main() -> None:
    print("=" * 72)
    print("RELATIONAL ACTUALISM — SOURCE-LAW REFERENCE SCAFFOLD v1")
    print("=" * 72)
    print()
    print("CANONICAL REGIME DICTIONARY")
    print("-" * 72)
    print("Covariant bridge : G_{μν} = 8πG P_act[T_{μν}],  Λ = 0")
    print("Dense regime     : ρ_A := P_act[T_00]/c^2, with ρ_A ≈ ρ_m under equilibration")
    print("Effective sparse : ∇²Φ = 4πG ρ_A + 𝒟_λ[λ]")
    print("Historical source: A_RA(x) remains an open covariant lensing variable")
    print()

    print("DENSE-REGIME BENCHMARKS")
    print("-" * 72)
    alpha = light_deflection_arcsec(M_sun, R_sun, gamma=1.0)
    mercury = perihelion_advance_arcsec_century(M_sun, a_mercury, e_mercury, beta=1.0, gamma=1.0)
    theta_E, R_E = einstein_angle_arcsec(1e11, 1.0, 2.0)
    theta_plus, theta_minus, mu_tot = point_mass_images(0.5)

    print(f"Solar-limb light deflection  : {alpha:.6f} arcsec")
    print(f"Mercury perihelion advance   : {mercury:.6f} arcsec/century")
    print(f"Einstein angle (1e11 M_sun)  : {theta_E:.6f} arcsec")
    print(f"Einstein radius              : {R_E:.6f} kpc")
    print(f"Image pair for beta=0.5θ_E   : θ+/θ_E={theta_plus:.6f}, θ-/θ_E={theta_minus:.6f}")
    print(f"Total magnification          : {mu_tot:.6f}")
    print()

    print("OPERATOR / SIGN CHECK FOR λ(r) ∝ r^-2")
    print("-" * 72)
    p = 2.0
    for d in (1, 2, 3):
        print(f"Spatial dimension d={d}:  ∇_d² ln λ = {radial_laplacian_log_power(p, d)}")
    print()
    print("Interpretation:")
    print("For λ(r) ∝ r^-2, the correction is positive only under a 1D second-derivative")
    print("reading, zero in standard 2D cylindrical radial form, and negative in 3D")
    print("spherical radial form. So the halo operator/sign/geometry is not yet canonical.")
    print()
    print("AUDIT VERDICT")
    print("-" * 72)
    print("Safe now  : dense-regime GR recovery and its Solar-system / thin-lens consequences.")
    print("Effective : halo correction as a sparse-regime ansatz.")
    print("Open      : coefficient-level halo closure and mixed-regime cluster lensing.")
    print("=" * 72)

if __name__ == "__main__":
    main()
