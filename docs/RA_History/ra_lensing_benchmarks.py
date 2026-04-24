#!/usr/bin/env python3
"""
RA lensing benchmarks v1

This script computes two benchmark layers:
1. Solar-limb light deflection from the recovered dense-regime Schwarzschild sector.
2. A generic strong-lensing point-mass example to demonstrate calculational usefulness.

All numbers are translation-level consequences of the recovered Einstein sector,
not direct discrete RA-native derivations.
"""

from math import sqrt

# Constants
G = 6.67430e-11
c = 299792458.0
M_sun = 1.98847e30
R_sun = 6.957e8
pc = 3.085677581e16
arcsec_per_rad = 206264.80624709636

def solar_limb_deflection_arcsec() -> float:
    return 4 * G * M_sun / (R_sun * c**2) * arcsec_per_rad

def einstein_angle_arcsec(M_solar: float, D_l_Gpc: float, D_s_Gpc: float) -> tuple[float, float]:
    M = M_solar * M_sun
    D_l = D_l_Gpc * 1e9 * pc
    D_s = D_s_Gpc * 1e9 * pc
    D_ls = D_s - D_l
    theta_E = sqrt((4 * G * M / c**2) * (D_ls / (D_l * D_s)))
    theta_E_arcsec = theta_E * arcsec_per_rad
    R_E_kpc = D_l * theta_E / pc / 1000.0
    return theta_E_arcsec, R_E_kpc

def point_mass_images(u: float) -> tuple[float, float, float]:
    # u = beta/theta_E
    theta_plus = 0.5 * (u + sqrt(u*u + 4))
    theta_minus = 0.5 * (u - sqrt(u*u + 4))
    mu_tot = (u*u + 2) / (u * sqrt(u*u + 4))
    return theta_plus, theta_minus, mu_tot

if __name__ == "__main__":
    alpha = solar_limb_deflection_arcsec()
    theta_E, R_E = einstein_angle_arcsec(1e11, 1.0, 2.0)
    theta_plus, theta_minus, mu_tot = point_mass_images(0.5)

    print("RA LENSING BENCHMARKS v1")
    print("=" * 60)
    print("Dense-regime bridge consequences:")
    print(f"  Solar-limb light deflection  : {alpha:.6f} arcsec")
    print()
    print("Generic strong-lensing example (translation benchmark):")
    print("  Lens mass                    : 1.0e11 M_sun")
    print("  D_l, D_s                     : 1.0 Gpc, 2.0 Gpc")
    print(f"  Einstein angle              : {theta_E:.6f} arcsec")
    print(f"  Einstein radius (lens plane): {R_E:.6f} kpc")
    print()
    print("  Example source offset beta = 0.5 theta_E:")
    print(f"    theta_plus/theta_E        : {theta_plus:.6f}")
    print(f"    theta_minus/theta_E       : {theta_minus:.6f}")
    print(f"    total magnification       : {mu_tot:.6f}")
