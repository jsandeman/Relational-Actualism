"""
Verify Heraclitus's w₀, wₐ interpolation claim:
  t_trans ≈ 0.575, α ≈ 1.6 → w₀ ≈ -0.72, wₐ ≈ -0.93
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize, minimize_scalar, brentq
from scipy.interpolate import interp1d

def a_transition(t, t_trans, alpha_trans):
    """Scale factor: EdS→Milne transition."""
    if t < 0.001:
        return 0.001
    fv = t**alpha_trans / (t**alpha_trans + t_trans**alpha_trans)
    p = 2.0/3.0 + (1.0/3.0) * fv
    return t**p

def d_L_transition(z, t_trans, alpha_trans, N_int=2000):
    """Luminosity distance for EdS→Milne transition."""
    a_now = a_transition(1.0, t_trans, alpha_trans)
    
    def z_eq(t):
        return a_now / a_transition(t, t_trans, alpha_trans) - 1 - z
    
    try:
        t_e = brentq(z_eq, 0.0005, 0.9999)
    except:
        return 0
    
    ts = np.linspace(t_e, 1.0, N_int)
    dt = ts[1] - ts[0]
    d_C = sum(dt / a_transition(t, t_trans, alpha_trans) for t in ts)
    return (1 + z) * d_C

def d_L_lcdm(z, Om=0.31, OL=0.69):
    def integrand(zp):
        return 1.0 / np.sqrt(Om * (1+zp)**3 + OL)
    d_C, _ = quad(integrand, 0, z)
    return (1 + z) * d_C

def d_L_w0wa(z, Om, w0, wa):
    ODE = 1 - Om
    def integrand(zp):
        ap = 1/(1+zp)
        rho_DE = ODE * (1+zp)**(3*(1+w0+wa)) * np.exp(-3*wa*zp/(1+zp))
        E2 = Om * (1+zp)**3 + rho_DE
        if E2 <= 0: return 1e10
        return 1.0 / np.sqrt(E2)
    d_C, _ = quad(integrand, 0, z)
    return (1 + z) * d_C

# Redshift points for fitting
z_fit = np.array([0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 
                   0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5])

print("=" * 80)
print("VERIFYING HERACLITUS w₀, wₐ CLAIM")
print("=" * 80)

# ================================================================
# 1. VERIFY THE SPECIFIC POINT: t_trans=0.575, α=1.6
# ================================================================

t_tr = 0.575
a_tr = 1.6

print(f"\n1. Testing t_trans={t_tr}, α={a_tr}")
print("─" * 60)

d_model = np.array([d_L_transition(z, t_tr, a_tr) for z in z_fit])
valid = d_model > 0
z_v = z_fit[valid]
d_v = d_model[valid]

ref_idx = np.argmin(np.abs(z_v - 0.5))
d_v_norm = d_v / d_v[ref_idx]

# Fit with w₀-wₐ
def chi2_w0wa(params):
    w0, wa = params
    Om = 0.31
    try:
        dm = np.array([d_L_w0wa(z, Om, w0, wa) for z in z_v])
        if np.any(np.isnan(dm)) or np.any(dm <= 0): return 1e10
        dm_n = dm / d_L_w0wa(z_v[ref_idx], Om, w0, wa)
        return np.sum((d_v_norm - dm_n)**2)
    except: return 1e10

# Fine grid search
best_w0, best_wa, best_c2 = -1, 0, 1e10
for w0 in np.arange(-1.5, 0.0, 0.02):
    for wa in np.arange(-3.0, 1.0, 0.02):
        c2 = chi2_w0wa([w0, wa])
        if c2 < best_c2:
            best_c2 = c2; best_w0 = w0; best_wa = wa

res = minimize(chi2_w0wa, [best_w0, best_wa], method='Nelder-Mead',
               options={'xatol': 0.0001, 'fatol': 1e-12})

# Also fit Ω_Λ
def chi2_OL(OL):
    Om = 1 - OL
    if Om < 0.01: return 1e10
    dm = np.array([d_L_lcdm(z, Om, OL) for z in z_v])
    dm_n = dm / d_L_lcdm(z_v[ref_idx], Om, OL)
    return np.sum((d_v_norm - dm_n)**2)

res_OL = minimize_scalar(chi2_OL, bounds=(0.3, 0.95), method='bounded')

print(f"  w₀ = {res.x[0]:+.4f}  (Heraclitus claims: -0.72)")
print(f"  wₐ = {res.x[1]:+.4f}  (Heraclitus claims: -0.93)")
print(f"  Ω_Λ(eq) = {res_OL.x:.4f}")
print(f"  χ² = {res.fun:.8f}")

# ================================================================
# 2. FINE SCAN AROUND HERACLITUS'S POINT
# ================================================================

print(f"\n\n2. FINE SCAN: t_trans × α NEAR HERACLITUS'S POINT")
print("─" * 60)

print(f"  {'t_trans':>8} {'α':>6} {'w₀':>8} {'wₐ':>8} {'Ω_Λ':>8} {'χ²':>12}")
print("  " + "─" * 56)

for t_tr in [0.50, 0.525, 0.55, 0.575, 0.60, 0.625, 0.65]:
    for a_tr in [1.2, 1.4, 1.6, 1.8, 2.0]:
        dm = np.array([d_L_transition(z, t_tr, a_tr) for z in z_fit])
        v = dm > 0
        if np.sum(v) < 8: continue
        zv = z_fit[v]; dv = dm[v]
        ri = np.argmin(np.abs(zv - 0.5))
        dn = dv / dv[ri]
        
        def c2(params):
            w0, wa = params
            try:
                d = np.array([d_L_w0wa(z, 0.31, w0, wa) for z in zv])
                if np.any(np.isnan(d)) or np.any(d<=0): return 1e10
                return np.sum((dn - d/d_L_w0wa(zv[ri], 0.31, w0, wa))**2)
            except: return 1e10
        
        bw, bwa, bc = -1, 0, 1e10
        for w0 in np.arange(-1.5, 0.0, 0.05):
            for wa in np.arange(-2.0, 1.0, 0.05):
                c = c2([w0, wa])
                if c < bc: bc = c; bw = w0; bwa = wa
        
        r = minimize(c2, [bw, bwa], method='Nelder-Mead',
                     options={'xatol': 0.001, 'fatol': 1e-10})
        
        def c2_ol(OL):
            Om = 1-OL
            if Om < 0.01: return 1e10
            d = np.array([d_L_lcdm(z, Om, OL) for z in zv])
            return np.sum((dn - d/d_L_lcdm(zv[ri], Om, OL))**2)
        
        r_ol = minimize_scalar(c2_ol, bounds=(0.3, 0.95), method='bounded')
        
        mark = " ★" if abs(r.x[0]+0.70)<0.1 and abs(r.x[1]+0.90)<0.2 else ""
        print(f"  {t_tr:>8.3f} {a_tr:>6.1f} {r.x[0]:>+8.3f} {r.x[1]:>+8.3f} "
              f"{r_ol.x:>8.4f} {r.fun:>12.8f}{mark}")

# ================================================================
# 3. COMPARISON WITH DESI
# ================================================================

print(f"""

3. COMPARISON WITH DESI
{'='*60}

  DESI DR2 (2025):
    w₀ = -0.70 ± 0.10
    wₐ = -0.90 ± 0.30

  Heraclitus claim (t_trans=0.575, α=1.6):
    w₀ = {res.x[0]:+.3f}
    wₐ = {res.x[1]:+.3f}

  See table above for nearby parameter values.
  
  If confirmed: the RA EdS→Milne transition with ONE parameter
  (t_trans, or equivalently the epoch when voids begin to
  dominate) reproduces BOTH w₀ AND wₐ in the DESI range.
""")
