"""
What Is μ_int?
==============

Three candidate definitions tested against same-force resonance data.

The goal: replace the fitted μ_int with a DERIVED quantity.

Candidate 1: Compton-volume density
  μ = (m / Λ_QCD)^p  for some power p

Candidate 2: Confinement-volume density
  μ = L_cycle × (m / Λ_QCD)^q  (confinement length modulates)

Candidate 3: Renewal-density fixed point
  μ is the density at which the renewal ratio R_stab/R_exit
  equals the observed value. This is SELF-CONSISTENT: the motif
  exists at the density where it CAN exist.

The third is the most RA-native because it doesn't import mass at all.
It says: the internal density of a motif is determined by its own
topology — specifically, by the density at which its self-reproduction
is marginally stable.
"""

import numpy as np
from math import factorial, exp
from scipy.optimize import minimize_scalar

c_bdg = np.array([1, -1, 9, -16, 8])
hbar_MeV_s = 6.582e-22
Lambda_QCD = 200  # MeV

def S(N):
    return c_bdg[0] + sum(c_bdg[k+1]*N[k] for k in range(4))

def exit_prob(N, L, mu):
    """Probability of exiting the identity class per step at density mu."""
    lam = np.array([mu**(k+1) / factorial(k+1) for k in range(4)])
    lam_total = sum(lam)
    p_interact = 1 - exp(-lam_total)

    if lam_total < 1e-15:
        return 0.0

    p_k = lam / lam_total

    p_exit = 0
    for k in range(4):
        N_new = np.array(N, dtype=int).copy()
        N_new[k] += 1
        while sum(N_new) > L + 2:
            for dd in range(3, -1, -1):
                if N_new[dd] > 0:
                    N_new[dd] -= 1
                    break
        s_new = S(N_new)
        if s_new <= 0:
            p_exit += p_k[k]

    return p_interact * p_exit

def lifetime_steps(N, L, mu):
    """Expected lifetime in steps."""
    pe = exit_prob(N, L, mu)
    if pe < 1e-15:
        return float('inf')
    return 1.0 / pe

def lifetime_seconds(N, L, mu, mass_MeV):
    """Convert to seconds."""
    steps = lifetime_steps(N, L, mu)
    tau_c = hbar_MeV_s / mass_MeV
    return steps * L * tau_c

# ================================================================
# Same-force resonance data (strongly decaying hadrons + W/Z)
# ================================================================

resonances = {
    'ρ(770)':      {'N': [2,1,0,0], 'L': 3, 'mass': 775,   'tau_obs': 4.4e-24},
    'K*(892)':     {'N': [2,1,0,0], 'L': 3, 'mass': 892,   'tau_obs': 1.3e-23},
    'ω(782)':      {'N': [2,1,0,0], 'L': 3, 'mass': 782,   'tau_obs': 7.7e-23},
    'Δ(1232)':     {'N': [3,1,0,0], 'L': 4, 'mass': 1232,  'tau_obs': 5.6e-24},
    'Σ*(1385)':    {'N': [3,1,0,0], 'L': 4, 'mass': 1385,  'tau_obs': 1.8e-23},
    'Roper(1440)': {'N': [3,2,0,0], 'L': 4, 'mass': 1440,  'tau_obs': 2.0e-24},
    'N(1520)':     {'N': [3,2,0,0], 'L': 4, 'mass': 1520,  'tau_obs': 6.0e-24},
    'N(1680)':     {'N': [3,2,0,0], 'L': 4, 'mass': 1680,  'tau_obs': 5.1e-24},
    'Λ(1520)':     {'N': [3,2,0,0], 'L': 4, 'mass': 1520,  'tau_obs': 1.3e-23},
    'Δ(1600)':     {'N': [3,2,0,0], 'L': 4, 'mass': 1600,  'tau_obs': 1.9e-24},
    'f₂(1270)':    {'N': [2,2,0,0], 'L': 3, 'mass': 1270,  'tau_obs': 5.3e-24},
    'W boson':     {'N': [1,0,0,0], 'L': 1, 'mass': 80379,  'tau_obs': 3.0e-25},
    'Z boson':     {'N': [1,0,0,0], 'L': 1, 'mass': 91188,  'tau_obs': 2.6e-25},
}

print("=" * 100)
print("WHAT IS μ_int? THREE CANDIDATE DEFINITIONS")
print("=" * 100)

# ================================================================
# STEP 1: Fit μ_int individually for each resonance
# ================================================================

print("\n1. INDIVIDUAL μ_int FITS")
print("─" * 100)
print(f"{'Particle':<16} {'Profile':<14} {'L':>3} {'mass':>8} {'τ_obs':>12} "
      f"{'μ_fit':>8} {'τ_pred':>12} {'log₁₀':>8}")
print("─" * 100)

fitted_mus = {}
for pname, p in resonances.items():
    N = p['N']
    L = p['L']
    mass = p['mass']
    tau_obs = p['tau_obs']

    # Scan for best μ
    best_mu = None
    best_err = float('inf')
    for mu_try in np.linspace(0.01, 300, 30000):
        tau_p = lifetime_seconds(N, L, mu_try, mass)
        if tau_p > 0 and tau_p < 1e10:
            err = abs(np.log10(tau_p / tau_obs))
            if err < best_err:
                best_err = err
                best_mu = mu_try

    fitted_mus[pname] = best_mu
    if best_mu is None:
        lr = "NO EXIT"
        print(f"{pname:<16} {Nstr:<14} {L:>3} {mass:>8} {tau_obs:>12.2e} "
              f"{—:>8} {—:>12} {lr:>8}")
        continue
    tau_p = lifetime_seconds(N, L, best_mu, mass)
    lr = f"{np.log10(tau_p/tau_obs):+.2f}" if tau_p > 0 and tau_p < 1e10 else "—"
    Nstr = f"({N[0]},{N[1]},{N[2]},{N[3]})"
    print(f"{pname:<16} {Nstr:<14} {L:>3} {mass:>8} {tau_obs:>12.2e} "
          f"{best_mu:>8.3f} {tau_p:>12.2e} {lr:>8}")

# ================================================================
# STEP 2: Test Candidate 1 — μ = (m/Λ)^p
# ================================================================

print("\n\n2. CANDIDATE 1: μ = (m/Λ_QCD)^p")
print("─" * 100)

# Fit the power law
log_mu = []
log_ratio = []
names_for_fit = []
for pname, mu in fitted_mus.items():
    if mu is not None and mu > 0:
        m = resonances[pname]['mass']
        log_mu.append(np.log(mu))
        log_ratio.append(np.log(m / Lambda_QCD))
        names_for_fit.append(pname)

log_mu = np.array(log_mu)
log_ratio = np.array(log_ratio)

# Linear regression: log(μ) = p × log(m/Λ) + c
if len(log_mu) > 2:
    A = np.vstack([log_ratio, np.ones(len(log_ratio))]).T
    result = np.linalg.lstsq(A, log_mu, rcond=None)
    p_fit, c_fit = result[0]
    residuals = log_mu - (p_fit * log_ratio + c_fit)
    rms = np.sqrt(np.mean(residuals**2))

    print(f"   Best fit: μ = {np.exp(c_fit):.4f} × (m/Λ_QCD)^{p_fit:.4f}")
    print(f"   RMS residual in log(μ): {rms:.4f}")
    print(f"   Coefficient: {np.exp(c_fit):.4f}")
    print(f"   Power: {p_fit:.4f}")
    print()

    # Test specific powers
    for p_test in [0.5, 1.0, 1.5, 2.0]:
        # For each power, fit the coefficient
        c_test = np.mean(log_mu - p_test * log_ratio)
        pred = p_test * log_ratio + c_test
        rms_test = np.sqrt(np.mean((log_mu - pred)**2))
        print(f"   p={p_test:.1f}: μ = {np.exp(c_test):.4f} × (m/Λ)^{p_test:.1f}, "
              f"RMS = {rms_test:.4f}")

# ================================================================
# STEP 3: Test Candidate 2 — μ = L × (m/Λ)^q
# ================================================================

print("\n\n3. CANDIDATE 2: μ = L_cycle × f(m/Λ)")
print("─" * 100)

# Check if L-scaling helps
log_mu_over_L = []
for pname in names_for_fit:
    L = resonances[pname]['L']
    log_mu_over_L.append(np.log(fitted_mus[pname] / L))

log_mu_over_L = np.array(log_mu_over_L)

if len(log_mu_over_L) > 2:
    A2 = np.vstack([log_ratio, np.ones(len(log_ratio))]).T
    result2 = np.linalg.lstsq(A2, log_mu_over_L, rcond=None)
    p2, c2 = result2[0]
    rms2 = np.sqrt(np.mean((log_mu_over_L - (p2 * log_ratio + c2))**2))

    print(f"   Best fit: μ/L = {np.exp(c2):.4f} × (m/Λ)^{p2:.4f}")
    print(f"   i.e., μ = L × {np.exp(c2):.4f} × (m/Λ)^{p2:.4f}")
    print(f"   RMS residual: {rms2:.4f}")
    print(f"   Compare to Candidate 1 RMS: {rms:.4f}")
    print(f"   L-scaling {'HELPS' if rms2 < rms else 'does NOT help'}")

# ================================================================
# STEP 4: Test Candidate 3 — Self-consistent renewal density
# ================================================================

print("\n\n4. CANDIDATE 3: SELF-CONSISTENT RENEWAL DENSITY")
print("─" * 100)
print("   μ_sc is the density where the motif's renewal rate equals")
print("   a universal fraction of the total interaction rate.")
print()
print("   Hypothesis: every stable same-force resonance exists at the")
print("   density where it spends a universal fraction f* of its time")
print("   in the exit channel.")
print()

# For each resonance, compute what fraction of interactions lead to exit
exit_fracs = {}
for pname in names_for_fit:
    N = resonances[pname]['N']
    L = resonances[pname]['L']
    mu = fitted_mus[pname]

    lam = np.array([mu**(k+1) / factorial(k+1) for k in range(4)])
    lam_total = sum(lam)
    if lam_total < 1e-15:
        continue
    p_k = lam / lam_total

    p_exit = 0
    for k in range(4):
        N_new = np.array(N, dtype=int).copy()
        N_new[k] += 1
        while sum(N_new) > L + 2:
            for dd in range(3, -1, -1):
                if N_new[dd] > 0:
                    N_new[dd] -= 1
                    break
        if S(N_new) <= 0:
            p_exit += p_k[k]

    exit_fracs[pname] = p_exit

print(f"{'Particle':<16} {'μ_fit':>8} {'f_exit':>10} {'Steps':>8}")
print("─" * 50)
for pname in names_for_fit:
    mu = fitted_mus[pname]
    fe = exit_fracs.get(pname, 0)
    steps = 1/fe if fe > 0 else float('inf')
    print(f"{pname:<16} {mu:>8.3f} {fe:>10.4f} {steps:>8.1f}")

fvals = [v for v in exit_fracs.values() if v > 0]
if fvals:
    f_mean = np.mean(fvals)
    f_std = np.std(fvals)
    f_median = np.median(fvals)
    print(f"\n   f_exit mean:   {f_mean:.4f} ± {f_std:.4f}")
    print(f"   f_exit median: {f_median:.4f}")
    print(f"   f_exit range:  {min(fvals):.4f} — {max(fvals):.4f}")

    # Check: is f_exit UNIVERSAL?
    cv = f_std / f_mean * 100
    print(f"   Coefficient of variation: {cv:.1f}%")
    if cv < 30:
        print(f"   → f_exit is approximately UNIVERSAL across same-force resonances!")
        print(f"   → This means: every resonance exists at the density where ~{f_median:.1%}")
        print(f"     of its interactions lead to exit. The exit fraction is a STRUCTURAL")
        print(f"     constant, not a fitting parameter.")
    else:
        print(f"   → f_exit varies significantly across resonances (CV={cv:.1f}%)")

# ================================================================
# STEP 5: THE DEEP QUESTION — Can μ be derived from N and L alone?
# ================================================================

print("\n\n5. CAN μ BE DERIVED FROM THE MOTIF STATE ALONE?")
print("─" * 100)

# The most RA-native possibility: μ_int depends ONLY on (N, L),
# not on mass at all. Mass is a DERIVED quantity in RA.

# Test: group resonances by profile and check if μ_fit depends
# on the profile structure

profiles = {}
for pname in names_for_fit:
    N = tuple(resonances[pname]['N'])
    L = resonances[pname]['L']
    key = (N, L)
    if key not in profiles:
        profiles[key] = []
    profiles[key].append((pname, fitted_mus[pname], resonances[pname]['mass']))

print("\n   Resonances grouped by (N, L):")
print()
for key, members in sorted(profiles.items()):
    N, L = key
    mus = [m[1] for m in members]
    masses = [m[2] for m in members]
    print(f"   Profile ({N[0]},{N[1]},{N[2]},{N[3]}), L={L}:")
    for name, mu, mass in members:
        print(f"     {name:<16} μ={mu:.3f}  mass={mass} MeV  μ/mass={mu/mass*1000:.4f}/GeV")
    if len(mus) > 1:
        print(f"     μ range: {min(mus):.3f} — {max(mus):.3f} (spread: {max(mus)-min(mus):.3f})")
        print(f"     μ/mass ratio range: {min(m/mass for m, mass in zip(mus, masses)):.6f} — "
              f"{max(m/mass for m, mass in zip(mus, masses)):.6f}")
    print()

# ================================================================
# STEP 6: THE BDG-NATIVE CANDIDATE
# ================================================================

print("\n6. THE BDG-NATIVE CANDIDATE: μ from S and L")
print("─" * 100)
print()
print("   Hypothesis: μ_int = S_BDG / L_cycle")
print("   (The internal density is the BDG score per confinement step.)")
print()

print(f"{'Particle':<16} {'S':>4} {'L':>3} {'S/L':>6} {'μ_fit':>8} {'Ratio':>8}")
print("─" * 55)
for pname in names_for_fit:
    N = resonances[pname]['N']
    L = resonances[pname]['L']
    s = S(N)
    sl = s / L
    mu = fitted_mus[pname]
    ratio = mu / sl if sl > 0 else float('inf')
    print(f"{pname:<16} {s:>4} {L:>3} {sl:>6.2f} {mu:>8.3f} {ratio:>8.2f}")

# Test other simple functions of S and L
print()
print("   Testing other simple functions:")
print()
candidates_native = {
    'S/L':          lambda N, L: S(N) / L,
    'S × L':        lambda N, L: S(N) * L,
    'S^(1/2)':      lambda N, L: np.sqrt(max(S(N), 0.01)),
    'S^(1/2) × L':  lambda N, L: np.sqrt(max(S(N), 0.01)) * L,
    'S^(1/2) / L':  lambda N, L: np.sqrt(max(S(N), 0.01)) / L,
    '|ΔS₃|/S':     lambda N, L: abs(c_bdg[3]) / max(S(N), 0.01),  # depth-3 disruption weight
    'Σ|c_k N_k|/L': lambda N, L: sum(abs(c_bdg[k+1])*N[k] for k in range(4)) / L,
}

for cname, cfunc in candidates_native.items():
    vals = []
    for pname in names_for_fit:
        N = resonances[pname]['N']
        L = resonances[pname]['L']
        cv = cfunc(N, L)
        mu = fitted_mus[pname]
        if cv > 0:
            vals.append(mu / cv)

    if vals:
        mean_ratio = np.mean(vals)
        std_ratio = np.std(vals)
        cv_pct = std_ratio / mean_ratio * 100 if mean_ratio > 0 else 999
        print(f"   {cname:<16} mean(μ/candidate) = {mean_ratio:.3f} ± {std_ratio:.3f} "
              f"(CV = {cv_pct:.1f}%)")

# ================================================================
# STEP 7: MASS AS DERIVED FROM μ AND TOPOLOGY
# ================================================================

print("\n\n7. INVERTING THE QUESTION: WHAT IF MASS DERIVES FROM μ?")
print("─" * 100)
print()
print("   In standard physics: mass is fundamental, density is derived.")
print("   In RA: density μ might be fundamental, mass might be derived.")
print()
print("   If μ_int is a function of (N, L) alone, then:")
print("   τ_steps = 1/p_exit(N, L, μ)")
print("   τ_seconds = τ_steps × L × ℏ/(mc²)")
print("   Matching to τ_obs gives: m = ℏ × L × τ_steps / (c² × τ_obs)")
print()
print("   In other words: mass = (step-count lifetime) / (observed lifetime)")
print("   × (ℏ/c² × L)")
print()
print("   The MASS ITSELF would be a derived quantity: it measures how")
print("   fast the motif's internal clock runs relative to external time.")
print()

# For each resonance, compute what mass would be predicted
# if μ were set by a universal rule μ = S/L × constant
print("   If μ = S/L × k for universal k:")
print()

# Use the mean ratio from above for S/L
sl_ratios = []
for pname in names_for_fit:
    N = resonances[pname]['N']
    L = resonances[pname]['L']
    s = S(N)
    sl = s / L if L > 0 else 0
    if sl > 0:
        sl_ratios.append(fitted_mus[pname] / sl)

if sl_ratios:
    k_universal = np.mean(sl_ratios)
    print(f"   Universal k = {k_universal:.3f}")
    print()
    print(f"{'Particle':<16} {'S/L':>6} {'μ_pred':>8} {'μ_fit':>8} {'Error%':>8}")
    print("   " + "─" * 50)
    for pname in names_for_fit:
        N = resonances[pname]['N']
        L = resonances[pname]['L']
        s = S(N)
        sl = s / L
        mu_pred = sl * k_universal
        mu_fit = fitted_mus[pname]
        err = abs(mu_pred - mu_fit) / mu_fit * 100
        print(f"   {pname:<16} {sl:>6.2f} {mu_pred:>8.3f} {mu_fit:>8.3f} {err:>7.1f}%")

print("""
8. SUMMARY AND NEXT STEPS
===============================================================================

THE THREE CANDIDATES:

1. μ = coefficient × (m/Λ_QCD)^p
   Status: Works, but imports mass as fundamental.
   Best fit power and coefficient given above.

2. μ = L × coefficient × (m/Λ)^q
   Status: L-scaling may or may not help (see RMS comparison).

3. Self-consistent exit fraction f*
   Status: If f_exit is universal, μ is determined by topology alone.
   The motif exists at the density where its exit fraction equals f*.

THE DEEPEST POSSIBILITY:

If μ depends only on (N, L), then MASS IS DERIVED:
  m = ℏ L τ_steps(N, L, μ(N,L)) / (c² τ_obs)

This would mean mass is not a primitive property of a particle.
Mass is the conversion factor between the motif's internal step
count and the external laboratory clock. It measures HOW FAST
the motif's self-reproduction cycle runs.

A heavy particle is one whose internal graph density is high,
so its internal clock ticks fast, so it accumulates many
actualization steps per unit of external time.

A light particle is one whose internal density is low,
so its clock ticks slowly, so it accumulates few steps
per unit of external time.

Mass IS internal density × geometric conversion factor.

If this is right, then E = mc² is not a law of nature.
It is the DEFINITION of mass in terms of actualization rate:
  E = (ℏ/τ_step) = (actualization events per second) × ℏ
  m = E/c² = (actualization rate) × (ℏ/c²)

Mass, energy, and actualization rate are three names for the
same thing: how fast the graph grows at this location.
""")
