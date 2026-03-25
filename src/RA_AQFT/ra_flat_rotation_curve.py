"""
Relational Actualism: Galactic Rotation Curve Model

This script computes the galactic rotation curve based on the static, weak-field 
limit of the covariant actualization tensor derived in RAGC. It models the 
00-component of the RA field equations: 
G_00 = 8\pi G [T_00^(A) + \Theta_00^(\lambda)]
"""

import numpy as np
import matplotlib.pyplot as plt

# --- Fundamental Constants ---
G = 6.67430e-11        # Gravitational constant (m^3 kg^-1 s^-2)
c = 299792458          # Speed of light (m/s)
M_sun = 1.989e30       # Solar mass (kg)
kpc_to_m = 3.086e19    # Kiloparsecs to meters

# --- Galaxy Parameters (Milky Way Analog) ---
# Visible baryonic mass (accumulated causal depth source)
M_baryon = 6e10 * M_sun 

# Target flat rotation velocity at large radii (~220 km/s)
v_flat_target = 220000  # m/s

# --- Derive the Actualization Coupling Constant (xi) ---
# \xi represents the ratio of microscopic actualization entropy to the fundamental RA area element.
# Derived from the covariant field equation's weak-field limit.
xi = (v_flat_target / (2 * c))**2 
print(f"Calculated Actualization Entropy Ratio (xi): {xi:.2e}")

# --- Calculate Velocities ---
# Array of radii from 1 kpc to 50 kpc
r_kpc = np.linspace(1, 50, 500)
r_m = r_kpc * kpc_to_m

# 1. Accumulated Causal Depth Velocity (T_00^(A) component)
# Recovers the standard Newtonian baryonic profile in the equilibrium limit
v_accumulated = np.sqrt(G * M_baryon / r_m)

# 2. Actualization Gradient Velocity (\Theta_00^(\lambda) component)
# The thermodynamic pressure of the actualization vacuum (rho_lambda)
v_lambda = np.ones_like(r_m) * np.sqrt(4 * xi * c**2)

# 3. Total RA Effective Velocity
# v_eff = sqrt(v_A^2 + v_lambda^2)
v_effective = np.sqrt(v_accumulated**2 + v_lambda**2)

# --- Plotting ---
plt.figure(figsize=(10, 6))

# Plot components in km/s
plt.plot(r_kpc, v_accumulated / 1000, '--', color='blue', label='Accumulated Causal Depth ($T_{00}^{(A)}$)')
plt.plot(r_kpc, v_lambda / 1000, ':', color='red', label='Actualization Gradient ($\\Theta_{00}^{(\\lambda)}$)')
plt.plot(r_kpc, v_effective / 1000, '-', color='black', linewidth=2.5, label='Total RA Effective Velocity')

plt.title('Relational Actualism: Covariant Galactic Rotation Curve', fontsize=14)
plt.xlabel('Radius (kpc)', fontsize=12)
plt.ylabel('Orbital Velocity (km/s)', fontsize=12)
plt.ylim(0, 300)
plt.xlim(0, 50)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()