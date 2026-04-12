"""
σ-Label Table and Empirical Σ_k Path Filters
=============================================

Stage 1: Build complete σ-label table for all resonances
Stage 2: Infer Σ_k empirically from known lifetimes

For each particle:
  1. Full quantum numbers (I, G, J, P, C, S, B, flavor)
  2. BDG profile (N, L)
  3. All admissible daughter channels
  4. Exit type classification (I/II/III/IV)
  5. Empirical Σ_eff from τ_obs vs τ_unfiltered
"""

import numpy as np
from math import factorial, exp
from collections import defaultdict

c_bdg = np.array([1, -1, 9, -16, 8])
hbar = 6.582e-22

def S_bdg(N): return c_bdg[0] + sum(c_bdg[k+1]*N[k] for k in range(4))

def has_single_step_exit(N, L):
    """Does this profile have any depth that gives S ≤ 0?"""
    for k in range(4):
        Nn = list(N); Nn[k] += 1
        while sum(Nn) > L + 2:
            for d in range(3,-1,-1):
                if Nn[d] > 0: Nn[d] -= 1; break
        if S_bdg(Nn) <= 0:
            return True, k+1  # returns the exit depth
    return False, None

def exit_prob_unfiltered(N, L, mu):
    """Exit probability assuming ALL channels are σ-allowed."""
    lam = [mu**(k+1)/factorial(k+1) for k in range(4)]
    lt = sum(lam)
    if lt < 1e-15: return 0.0
    pi = 1 - exp(-lt)
    pk = [l/lt for l in lam]
    pe = 0
    for k in range(4):
        Nn = list(N); Nn[k] += 1
        while sum(Nn) > L + 2:
            for d in range(3,-1,-1):
                if Nn[d] > 0: Nn[d] -= 1; break
        if S_bdg(Nn) <= 0:
            pe += pk[k]
    return pi * pe

# Daughter channels with quantum numbers and mass thresholds
daughters = {
    'ππ':    {'n': 2, 'I_range': [0,1,2], 'G': +1, 'S': 0, 'B': 0, 'threshold': 280},
    'πππ':   {'n': 3, 'I_range': [0,1],   'G': -1, 'S': 0, 'B': 0, 'threshold': 420},
    'ππππ':  {'n': 4, 'I_range': [0,1,2], 'G': +1, 'S': 0, 'B': 0, 'threshold': 560},
    'KK̄':   {'n': 2, 'I_range': [0,1],   'G': -1, 'S': 0, 'B': 0, 'threshold': 987},
    'Kπ':    {'n': 2, 'I_range': [0.5,1.5],'G': None,'S': 1,'B': 0, 'threshold': 634},
    'Kππ':   {'n': 3, 'I_range': [0.5,1.5],'G': None,'S': 1,'B': 0, 'threshold': 774},
    'ηπ':    {'n': 2, 'I_range': [1],      'G': +1, 'S': 0, 'B': 0, 'threshold': 688},
    'ηππ':   {'n': 3, 'I_range': [0,1],    'G': -1, 'S': 0, 'B': 0, 'threshold': 828},
    'Nπ':    {'n': 2, 'I_range': [0.5,1.5],'G': None,'S': 0,'B': 1, 'threshold': 1078},
    'Nππ':   {'n': 3, 'I_range': [0.5,1.5],'G': None,'S': 0,'B': 1, 'threshold': 1218},
    'Λπ':    {'n': 2, 'I_range': [1],      'G': None,'S':-1,'B': 1, 'threshold': 1256},
    'Σπ':    {'n': 2, 'I_range': [0,1,2],  'G': None,'S':-1,'B': 1, 'threshold': 1332},
    'ΛK':    {'n': 2, 'I_range': [0.5],    'G': None,'S': 0,'B': 1, 'threshold': 1610},
    'NK̄':   {'n': 2, 'I_range': [0,1],    'G': None,'S':-1,'B': 0, 'threshold': 1432},
    'γγ':    {'n': 2, 'I_range': [0],      'G': +1, 'S': 0, 'B': 0, 'threshold': 0},
    'πγ':    {'n': 2, 'I_range': [1],      'G': -1, 'S': 0, 'B': 0, 'threshold': 140},
}

def daughter_admissible(parent, daughter_name):
    """Check if daughter channel is allowed by conservation laws."""
    d = daughters[daughter_name]
    p = parent

    # Baryon number conservation
    if p['B'] != d['B']:
        return False

    # Strangeness conservation (strong decays)
    if p.get('decay_force', 'strong') == 'strong':
        if abs(p['S']) != abs(d['S']):
            return False

    # G-parity conservation (only for non-strange, I-definite states)
    if p.get('G') is not None and d['G'] is not None:
        if p['S'] == 0 and d['S'] == 0:
            if p['G'] != d['G']:
                return False

    # Isospin compatibility (daughter I must be reachable)
    # Simplified: check if parent I is in daughter's allowed range
    if p['I'] not in d['I_range'] and not any(
        abs(p['I'] - di) <= 1 for di in d['I_range']
    ):
        return False

    # Kinematic threshold
    if p['mass'] < d['threshold']:
        return False

    return True

# ================================================================
# THE COMPLETE RESONANCE TABLE
# ================================================================

resonances = {
    # ── Light unflavored mesons ──
    'π⁰':       {'N':[2,0,0,0],'L':3,'mass':135, 'tau':8.5e-17, 'I':1,'G':-1,'S':0,'B':0,'J':0,'P':-1,'C':+1,'flavor':'ud','decay_force':'EM'},
    'π±':       {'N':[2,0,0,0],'L':3,'mass':140, 'tau':2.6e-8,  'I':1,'G':-1,'S':0,'B':0,'J':0,'P':-1,'C':None,'flavor':'ud','decay_force':'weak'},
    'η':        {'N':[2,1,0,0],'L':3,'mass':548, 'tau':5.0e-19, 'I':0,'G':+1,'S':0,'B':0,'J':0,'P':-1,'C':+1,'flavor':'ud/ss','decay_force':'EM'},
    'ρ(770)':   {'N':[2,1,0,0],'L':3,'mass':775, 'tau':4.4e-24, 'I':1,'G':+1,'S':0,'B':0,'J':1,'P':-1,'C':-1,'flavor':'ud','decay_force':'strong'},
    'ω(782)':   {'N':[2,1,0,0],'L':3,'mass':782, 'tau':7.7e-23, 'I':0,'G':-1,'S':0,'B':0,'J':1,'P':-1,'C':-1,'flavor':'ud','decay_force':'strong'},
    'η\'(958)': {'N':[2,1,0,0],'L':3,'mass':958, 'tau':3.3e-21, 'I':0,'G':+1,'S':0,'B':0,'J':0,'P':-1,'C':+1,'flavor':'ud/ss','decay_force':'strong'},
    'φ(1020)':  {'N':[2,2,0,0],'L':3,'mass':1020,'tau':1.5e-22, 'I':0,'G':-1,'S':0,'B':0,'J':1,'P':-1,'C':-1,'flavor':'ss','decay_force':'strong'},
    'f₀(980)':  {'N':[2,1,0,0],'L':3,'mass':980, 'tau':2.5e-23, 'I':0,'G':+1,'S':0,'B':0,'J':0,'P':+1,'C':+1,'flavor':'ud/ss','decay_force':'strong'},
    'a₀(980)':  {'N':[2,1,0,0],'L':3,'mass':980, 'tau':7.5e-23, 'I':1,'G':-1,'S':0,'B':0,'J':0,'P':+1,'C':+1,'flavor':'ud','decay_force':'strong'},
    'f₂(1270)': {'N':[2,2,0,0],'L':3,'mass':1275,'tau':5.3e-24, 'I':0,'G':+1,'S':0,'B':0,'J':2,'P':+1,'C':+1,'flavor':'ud','decay_force':'strong'},

    # ── Strange mesons ──
    'K*(892)':  {'N':[2,1,0,0],'L':3,'mass':892, 'tau':1.3e-23, 'I':0.5,'G':None,'S':1,'B':0,'J':1,'P':-1,'C':None,'flavor':'us','decay_force':'strong'},
    'K₁(1270)': {'N':[2,2,0,0],'L':3,'mass':1270,'tau':1.2e-23, 'I':0.5,'G':None,'S':1,'B':0,'J':1,'P':+1,'C':None,'flavor':'us','decay_force':'strong'},

    # ── Non-strange baryons ──
    'Δ(1232)':  {'N':[3,1,0,0],'L':4,'mass':1232,'tau':5.6e-24, 'I':1.5,'G':None,'S':0,'B':1,'J':1.5,'P':+1,'C':None,'flavor':'uud','decay_force':'strong'},
    'N(1440)':  {'N':[3,2,0,0],'L':4,'mass':1440,'tau':2.0e-24, 'I':0.5,'G':None,'S':0,'B':1,'J':0.5,'P':+1,'C':None,'flavor':'uud','decay_force':'strong'},
    'N(1520)':  {'N':[3,2,0,0],'L':4,'mass':1520,'tau':6.0e-24, 'I':0.5,'G':None,'S':0,'B':1,'J':1.5,'P':-1,'C':None,'flavor':'uud','decay_force':'strong'},
    'N(1535)':  {'N':[3,2,0,0],'L':4,'mass':1535,'tau':4.4e-24, 'I':0.5,'G':None,'S':0,'B':1,'J':0.5,'P':-1,'C':None,'flavor':'uud','decay_force':'strong'},
    'N(1680)':  {'N':[3,2,0,0],'L':4,'mass':1680,'tau':5.1e-24, 'I':0.5,'G':None,'S':0,'B':1,'J':2.5,'P':+1,'C':None,'flavor':'uud','decay_force':'strong'},
    'Δ(1600)':  {'N':[3,2,0,0],'L':4,'mass':1600,'tau':1.9e-24, 'I':1.5,'G':None,'S':0,'B':1,'J':1.5,'P':+1,'C':None,'flavor':'uud','decay_force':'strong'},
    'Δ(1620)':  {'N':[3,2,0,0],'L':4,'mass':1620,'tau':4.4e-24, 'I':1.5,'G':None,'S':0,'B':1,'J':0.5,'P':-1,'C':None,'flavor':'uud','decay_force':'strong'},

    # ── Strange baryons ──
    'Σ*(1385)': {'N':[3,1,0,0],'L':4,'mass':1385,'tau':1.8e-23, 'I':1,'G':None,'S':-1,'B':1,'J':1.5,'P':+1,'C':None,'flavor':'uds','decay_force':'strong'},
    'Λ(1520)':  {'N':[3,2,0,0],'L':4,'mass':1520,'tau':1.3e-23, 'I':0,'G':None,'S':-1,'B':1,'J':1.5,'P':-1,'C':None,'flavor':'uds','decay_force':'strong'},
    'Σ(1670)':  {'N':[3,2,0,0],'L':4,'mass':1670,'tau':4.4e-24, 'I':1,'G':None,'S':-1,'B':1,'J':1.5,'P':-1,'C':None,'flavor':'uds','decay_force':'strong'},
    'Ξ*(1530)': {'N':[3,1,0,0],'L':4,'mass':1530,'tau':6.7e-23, 'I':0.5,'G':None,'S':-2,'B':1,'J':1.5,'P':+1,'C':None,'flavor':'uss','decay_force':'strong'},

    # ── Gauge bosons ──
    'W':        {'N':[1,0,0,0],'L':1,'mass':80379,'tau':3.0e-25, 'I':0,'G':None,'S':0,'B':0,'J':1,'P':None,'C':None,'flavor':'gauge','decay_force':'weak'},
    'Z':        {'N':[1,0,0,0],'L':1,'mass':91188,'tau':2.6e-25, 'I':0,'G':None,'S':0,'B':0,'J':1,'P':None,'C':None,'flavor':'gauge','decay_force':'weak'},
    'Higgs':    {'N':[0,1,0,0],'L':1,'mass':125250,'tau':1.6e-22,'I':0,'G':None,'S':0,'B':0,'J':0,'P':+1,'C':+1,'flavor':'scalar','decay_force':'Yukawa'},
}

# ================================================================
# STAGE 1: σ-LABEL TABLE
# ================================================================

print("=" * 120)
print("STAGE 1: COMPLETE σ-LABEL TABLE")
print("=" * 120)
print()
print(f"{'Particle':<14} {'Profile':<12} {'S_BDG':>5} {'I':>4} {'G':>4} {'S':>3} {'B':>3} "
      f"{'J^P':>6} {'Flavor':<8} {'Force':<8} {'τ_obs':>10} {'Exit?':>6}")
print("─" * 120)

for pname, p in sorted(resonances.items(), key=lambda x: x[1]['tau']):
    N = p['N']
    s = S_bdg(N)
    has_exit, exit_depth = has_single_step_exit(N, p['L'])

    G_str = f"{p['G']:+d}" if p['G'] is not None else "—"
    P_str = f"{'+' if p['P']==1 else '-'}" if p['P'] is not None else "?"
    JP = f"{p['J']}{P_str}"
    ex = f"d{exit_depth}" if has_exit else "NONE"

    print(f"{pname:<14} ({N[0]},{N[1]},{N[2]},{N[3]}){'':<4} {s:>5} "
          f"{p['I']:>4} {G_str:>4} {p['S']:>3} {p['B']:>3} "
          f"{JP:>6} {p['flavor']:<8} {p['decay_force']:<8} {p['tau']:>10.1e} {ex:>6}")

# ================================================================
# STAGE 1b: DAUGHTER ADMISSIBILITY FOR ALL PARTICLES
# ================================================================

print(f"\n\n{'='*120}")
print("STAGE 1b: DAUGHTER ADMISSIBILITY MATRIX")
print(f"{'='*120}")

# Select key daughter channels
key_daughters = ['ππ', 'πππ', 'KK̄', 'Kπ', 'ηπ', 'Nπ', 'Nππ', 'Λπ', 'Σπ', 'γγ']

print(f"\n{'Particle':<14}", end="")
for dn in key_daughters:
    print(f" {dn:>5}", end="")
print(f"  {'Dominant channel':<20} {'n-body':>6}")
print("─" * 120)

for pname, p in sorted(resonances.items(), key=lambda x: x[1]['tau']):
    print(f"{pname:<14}", end="")
    allowed = []
    for dn in key_daughters:
        ok = daughter_admissible(p, dn)
        print(f" {'✓':>5}" if ok else f" {'·':>5}", end="")
        if ok:
            allowed.append((dn, daughters[dn]['n']))

    # Find dominant (lowest n-body allowed)
    if allowed:
        min_n = min(a[1] for a in allowed)
        dominant = [a[0] for a in allowed if a[1] == min_n]
        dom_str = '/'.join(dominant)
        print(f"  {dom_str:<20} {min_n:>6}")
    else:
        print(f"  {'(none strong)':20} {'—':>6}")

# ================================================================
# STAGE 2: EMPIRICAL Σ_eff FROM τ_obs vs τ_unfiltered
# ================================================================

print(f"\n\n{'='*120}")
print("STAGE 2: EMPIRICAL Σ_eff (σ-FILTER EFFECTIVENESS)")
print(f"{'='*120}")
print()
print("For each particle, compute:")
print("  τ_unfiltered = lifetime if ALL exit channels were open (Σ=1)")
print("  Σ_eff = τ_unfiltered / τ_obs")
print("  Σ_eff < 1 means the particle is MORE stable than unfiltered prediction")
print("  Σ_eff > 1 means something is wrong (shouldn't happen for strong decays)")
print()

# Use a UNIVERSAL physical μ for each mass scale
# From the ρ calibration: μ_ρ = 4.71 at m = 775 MeV
# μ(m) = μ_ρ × (m / m_ρ) for mesons
# For baryons, use Δ calibration: μ_Δ = 4.71 at m = 1232 MeV
mu_rho = 4.71
mu_delta = 4.71

print(f"{'Particle':<14} {'Profile':<12} {'μ_phys':>7} {'p_exit':>9} {'τ_unfilt':>11} "
      f"{'τ_obs':>11} {'Σ_eff':>8} {'Type':>6} {'Dominant':>12} {'n-body':>6}")
print("─" * 120)

type_data = defaultdict(list)

for pname, p in sorted(resonances.items(), key=lambda x: x[1]['tau']):
    N = p['N']
    L = p['L']
    mass = p['mass']
    tau_obs = p['tau']
    tau_c = hbar / mass

    # Only analyze strong decays for now
    if p['decay_force'] not in ['strong']:
        continue

    # Physical μ
    if p['B'] == 0:  # meson
        mu = mu_rho * (mass / 775)
    else:  # baryon
        mu = mu_delta * (mass / 1232)

    # Unfiltered exit probability
    pe = exit_prob_unfiltered(N, L, mu)

    if pe < 1e-15:
        tau_unfilt = float('inf')
        sigma_eff = 0
    else:
        tau_steps = 1.0 / pe
        tau_unfilt = tau_steps * L * tau_c
        sigma_eff = tau_unfilt / tau_obs

    # Find dominant daughter
    allowed = []
    for dn in daughters:
        if daughter_admissible(p, dn):
            allowed.append((dn, daughters[dn]['n']))
    if allowed:
        min_n = min(a[1] for a in allowed)
        dominant = '/'.join(a[0] for a in allowed if a[1] == min_n)
    else:
        min_n = 0
        dominant = '—'

    # Classify exit type
    has_exit, _ = has_single_step_exit(N, L)
    if not has_exit:
        etype = 'IV'
    elif min_n >= 3 and p.get('G') == -1:
        etype = 'III'
    elif p['S'] != 0 or (p['flavor'] in ['us', 'uds', 'uss']):
        etype = 'II'
    else:
        etype = 'I'

    tu = f"{tau_unfilt:.2e}" if tau_unfilt < 1e10 else "∞"
    se = f"{sigma_eff:.4f}" if sigma_eff > 0 else "—"

    print(f"{pname:<14} ({N[0]},{N[1]},{N[2]},{N[3]}){'':<4} {mu:>7.2f} {pe:>9.6f} "
          f"{tu:>11} {tau_obs:>11.1e} {se:>8} {etype:>6} {dominant:>12} {min_n:>6}")

    if sigma_eff > 0:
        type_data[etype].append({'name': pname, 'sigma': sigma_eff, 'n_body': min_n,
                                  'tau_obs': tau_obs, 'tau_unfilt': tau_unfilt})

# ================================================================
# STAGE 2b: Σ_eff STATISTICS BY EXIT TYPE
# ================================================================

print(f"\n\n{'='*120}")
print("STAGE 2b: Σ_eff STATISTICS BY EXIT TYPE")
print(f"{'='*120}")

for etype in ['I', 'II', 'III', 'IV']:
    data = type_data.get(etype, [])
    if not data:
        print(f"\n  Type {etype}: no data")
        continue

    sigmas = [d['sigma'] for d in data]
    names = [d['name'] for d in data]

    print(f"\n  Type {etype} ({len(data)} particles):")
    print(f"    Σ_eff range: {min(sigmas):.4f} — {max(sigmas):.4f}")
    print(f"    Σ_eff mean:  {np.mean(sigmas):.4f} ± {np.std(sigmas):.4f}")
    print(f"    Σ_eff median: {np.median(sigmas):.4f}")

    for d in sorted(data, key=lambda x: x['sigma']):
        print(f"      {d['name']:<14} Σ={d['sigma']:.4f}  n-body={d['n_body']}  "
              f"τ_obs={d['tau_obs']:.1e}")

# ================================================================
# STAGE 2c: THE PATTERN
# ================================================================

print(f"\n\n{'='*120}")
print("STAGE 2c: THE EMERGING PATTERN")
print(f"{'='*120}")
print("""
SUMMARY OF Σ_eff BY EXIT TYPE:

TYPE I (Direct exit, no σ constraint):
  Expected: Σ ≈ 1.0 (unfiltered prediction matches observation)
  These are the REFERENCE particles. Their unfiltered exit rate
  should match the observed lifetime.

TYPE II (Flavor rearrangement):
  Expected: Σ < 1 (σ suppresses exit by requiring flavor change)
  The suppression factor measures the cost of rearranging strangeness
  or other flavor labels during the exit process.

TYPE III (G-parity multi-step):
  Expected: Σ << 1 (σ forces multi-step path)
  The suppression factor measures the cost of taking a 3-body path
  when 2-body is forbidden by G-parity.

TYPE IV (OZI / topology-protected):
  Expected: Σ ≈ 0 (no single-step exit)
  The suppression is maximal because the topology itself blocks exit.

THE HIERARCHY:
  Σ(I) ≈ 1 > Σ(II) ~ 0.1-0.5 > Σ(III) ~ 0.01-0.1 > Σ(IV) ~ 0

If this hierarchy holds across the data, then:
  - Selection rules ARE Σ-filters on topology-space exit paths
  - The filter strength correlates with exit type
  - Lifetime = (unfiltered lifetime) / Σ_eff
  - And Σ_eff is determined by the motif's σ-labels
""")

# ================================================================
# STAGE 2d: WITHIN TYPE I — UNIVERSALITY TEST
# ================================================================

print(f"{'='*120}")
print("STAGE 2d: WITHIN TYPE I — IS Σ_eff UNIVERSAL?")
print(f"{'='*120}")
print()
print("If Type I particles have Σ ≈ 1 universally, then the")
print("unfiltered model IS the correct model for direct decays,")
print("and ALL suppression comes from σ-filtering alone.")
print()

type_i = type_data.get('I', [])
if type_i:
    for d in sorted(type_i, key=lambda x: x['tau_obs']):
        ratio = d['sigma']
        match = "✓" if 0.3 < ratio < 3.0 else "✗"
        print(f"  {d['name']:<14} Σ={ratio:.4f} {match}")

    sigs = [d['sigma'] for d in type_i]
    print(f"\n  Mean: {np.mean(sigs):.3f} ± {np.std(sigs):.3f}")
    print(f"  CV: {np.std(sigs)/np.mean(sigs)*100:.0f}%")
    print(f"  Within factor 3: {sum(1 for s in sigs if 0.3<s<3)}/{len(sigs)}")

# ================================================================
# STAGE 2e: CROSS-TYPE COMPARISON
# ================================================================

print(f"\n\n{'='*120}")
print("STAGE 2e: CROSS-TYPE Σ_eff COMPARISON")
print(f"{'='*120}")

all_data = []
for etype in ['I', 'II', 'III', 'IV']:
    for d in type_data.get(etype, []):
        all_data.append({**d, 'type': etype})

if all_data:
    all_data.sort(key=lambda x: -x['sigma'])
    print(f"\n{'Particle':<14} {'Type':>6} {'Σ_eff':>10} {'log₁₀(Σ)':>10} {'n-body':>7} {'τ_obs':>11}")
    print("─" * 65)
    for d in all_data:
        ls = f"{np.log10(d['sigma']):+.2f}" if d['sigma'] > 0 else "—"
        print(f"{d['name']:<14} {d['type']:>6} {d['sigma']:>10.4f} {ls:>10} "
              f"{d['n_body']:>7} {d['tau_obs']:>11.1e}")

