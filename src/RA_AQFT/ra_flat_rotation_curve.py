import numpy as np
import matplotlib.pyplot as plt

# --- Fundamental Constants ---
G = 6.67430e-11        # Gravitational constant (m^3 kg^-1 s^-2)
c = 299792458          # Speed of light (m/s)
M_sun = 1.989e30       # Solar mass (kg)
kpc_to_m = 3.086e19    # Kiloparsecs to meters

# --- Galaxy Parameters (Milky Way Analog) ---
# Visible baryonic mass (stars + gas)
M_baryon = 6e10 * M_sun 

# Target flat rotation velocity at large radii (~220 km/s)
v_flat_target = 220000  # m/s

# --- Derive the DAG Elasticity Coupling (xi) ---
# From our derivation: v_flat = 2 * c * sqrt(xi)
# Therefore: xi = (v_flat / (2 * c))^2
xi = (v_flat_target / (2 * c))**2 
print(f"Calculated DAG Elasticity Coupling (xi): {xi:.2e}")

# --- Calculate Velocities ---
# Array of radii from 1 kpc to 50 kpc
r_kpc = np.linspace(1, 50, 500)
r_m = r_kpc * kpc_to_m

# 1. Newtonian Velocity (Baryon-driven)
# v_N = sqrt(GM/r)
v_newtonian = np.sqrt(G * M_baryon / r_m)

# 2. Topological Velocity (DAG Tension-driven)
# v_T = sqrt(4 * xi * c^2)
v_topological = np.ones_like(r_m) * np.sqrt(4 * xi * c**2)

# 3. Total RA Effective Velocity
# v_eff = sqrt(v_N^2 + v_T^2)
v_effective = np.sqrt(v_newtonian**2 + v_topological**2)

# --- Plotting ---
plt.figure(figsize=(10, 6))

# Plot components in km/s
plt.plot(r_kpc, v_newtonian / 1000, '--', color='blue', label='Newtonian (Baryons Only)')
plt.plot(r_kpc, v_topological / 1000, ':', color='red', label='Topological Tension (DAG Gradient)')
plt.plot(r_kpc, v_effective / 1000, '-', color='black', linewidth=2.5, label='Total RA Effective Velocity')

plt.title('Relational Actualism: Galactic Rotation Curve', fontsize=14)
plt.xlabel('Radius (kpc)', fontsize=12)
plt.ylabel('Orbital Velocity (km/s)', fontsize=12)
plt.ylim(0, 300)
plt.xlim(0, 50)
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()