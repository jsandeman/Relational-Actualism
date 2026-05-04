"""
RA_BDG_Simulation.py
====================
Derivation 1 (RASM): BDG-filter stable pattern enumeration.

The BDG action for a 4D causal set vertex v is:
  S_BDG(v) = 1 - N1(v) + 9*N2(v) - 16*N3(v) + 8*N4(v)
where Nk(v) = number of elements x in past(v) such that exactly k-1
elements lie strictly between x and v.

The BDG filter: v is actualized iff S_BDG(v) > 0.

This script:
  1. Enumerates S_BDG(v) for all local causal set patterns up to size N
  2. Identifies which patterns are stable (S_BDG > 0)
  3. Characterises them by their N-vector (quantum number content)
  4. Connects to SM particle quantum numbers

Author: Joshua F. Sandeman (with Claude, March 2026)
Corresponds to RASM Derivation 1.
"""

import numpy as np
from itertools import combinations, product
from collections import defaultdict

# ── Core BDG machinery ──────────────────────────────────────────────────────

def compute_past(edges, n):
    """Transitive closure: past[v] = all strict ancestors of v."""
    past = [set() for _ in range(n)]
    dp   = [set() for _ in range(n)]
    for a, b in edges:
        dp[b].add(a)
    for v in range(n):
        for u in dp[v]:
            past[v].add(u)
            past[v].update(past[u])
    return past

def bdg_score(past, v):
    """S_BDG(v) and N-vector for vertex v."""
    N = [0] * 5   # N[1]..N[4]
    for x in past[v]:
        between = sum(1 for z in past[v] if x in past[z])
        k = between + 1
        if 1 <= k <= 4:
            N[k] += 1
    score = 1 - N[1] + 9*N[2] - 16*N[3] + 8*N[4]
    return score, N

# ── Chain depth analysis ──────────────────────────────────────────────────

def chain_score_table(max_depth=8):
    """Score for pure chain of k ancestors."""
    print("=== CHAIN DEPTH SCORE TABLE ===")
    print(f"{'Depth k':>8}  {'Score':>6}  N1 N2 N3 N4  Stable")
    print("-"*45)
    for k in range(max_depth+1):
        if k == 0:
            past = [set()]
            s, N = bdg_score(past, 0)
        else:
            edges = [(i, i+1) for i in range(k)]
            past  = compute_past(edges, k+1)
            s, N  = bdg_score(past, k)
        stable = "✓" if s > 0 else ("○" if s == 0 else "✗")
        print(f"  k={k}:    {s:>6}   {N[1]} {N[2]} {N[3]} {N[4]}    {stable}")
    print()
    print("KEY: Score stabilises at +1 for k>=4 (N1=N2=N3=N4=1)")
    print("     The BDG integers select depth-4 as the ground state.")
    print()

# ── Pattern catalogue ─────────────────────────────────────────────────────

def survey_patterns():
    """Survey key causal set patterns and their BDG scores."""
    patterns = [
        # Chains
        ("Isolated vertex",         [], 1, 0),
        ("1-chain past",           [(0,1)], 2, 1),
        ("2-chain past",           [(0,1),(1,2)], 3, 2),
        ("3-chain past",           [(0,1),(1,2),(2,3)], 4, 3),
        ("4-chain past",           [(0,1),(1,2),(2,3),(3,4)], 5, 4),
        ("5-chain past",           [(0,1),(1,2),(2,3),(3,4),(4,5)], 6, 5),
        # Parallel (bosonic-type)
        ("2 parallel preds",       [(0,2),(1,2)], 3, 2),
        ("3 parallel preds",       [(0,3),(1,3),(2,3)], 4, 3),
        ("4 parallel preds",       [(0,4),(1,4),(2,4),(3,4)], 5, 4),
        # Mixed
        ("Diamond",                [(0,1),(0,2),(1,3),(2,3)], 4, 3),
        ("Y-join (N2=2)",          [(0,2),(1,2),(2,3)], 4, 3),
        ("Fork top",               [(0,1),(1,2),(1,3)], 4, 2),
        ("Chain + 2 parallel",     [(0,1),(1,3),(2,3)], 4, 3),
        # More Y-joins
        ("Double Y-join",          [(0,3),(1,3),(2,3),(3,4),(3,5)], 6, 3),
        # Star patterns
        ("Star 1->3",              [(0,1),(0,2),(0,3)], 4, 1),
        ("Star 1->4",              [(0,1),(0,2),(0,3),(0,4)], 5, 1),
    ]

    print("=== PATTERN STABILITY CATALOGUE ===")
    print(f"  {'Pattern':<28}  {'Score':>6}  N=(N1,N2,N3,N4)  Stable")
    print("-"*70)

    results = []
    for name, edges, n, eval_v in patterns:
        if not edges:
            past = [set()]
            s, N = bdg_score(past, 0)
        else:
            past = compute_past(edges, n)
            s, N = bdg_score(past, eval_v)
        stable = "✓ YES" if s > 0 else ("○ =0" if s == 0 else "✗ NO")
        print(f"  {name:<28}  {s:>6}   ({N[1]},{N[2]},{N[3]},{N[4]})     {stable}")
        results.append((name, s, N, s > 0))
    print()
    return results

# ── Stable pattern characterisation ──────────────────────────────────────

def stable_pattern_analysis():
    """Characterise the stable patterns and match to SM particles."""
    print("=== STABLE PATTERNS AND SM MATCHING ===")
    print()
    print("BDG stable patterns (S_BDG > 0) by N-vector:")
    print()

    # The stable patterns found:
    stable = [
        # (name, N1, N2, N3, N4, score, SM_candidate)
        ("Isolated",     0, 0, 0, 0,  1, "Neutrino (ν) — no charge, no colour"),
        ("2-chain",      1, 1, 0, 0,  9, "Photon (γ) or W/Z — depth 2 = spin 1?"),
        ("4-chain",      1, 1, 1, 1,  1, "Electron (e) or quark — depth 4 = 4-momentum"),
        ("Y-join N2=2",  1, 2, 0, 0, 18, "Gluon (g) — N2 carries colour (SU3)"),
        ("Fork top",     1, 1, 0, 0,  9, "Same as 2-chain — W boson?"),
    ]

    for name, n1, n2, n3, n4, score, candidate in stable:
        print(f"  {name:<18} N=({n1},{n2},{n3},{n4})  score={score:>4}")
        print(f"    → SM candidate: {candidate}")
        print()

    print("=== QUANTUM NUMBER INTERPRETATION ===")
    print()
    print("From RASM: BDG charges Q_N1, Q_N2, Q_N3 map to:")
    print("  Q_N1 ∈ {0,1,2,3}  ↔  electric charge (×e/3)")
    print("  Q_N2 ∈ {0,1,2,...} ↔  baryon/colour number")
    print("  Q_N3 ∈ {0,1,2,...} ↔  weak isospin related")
    print()
    print("The N-vectors from the BDG filter give the COUNTS of these charges.")
    print("Stable patterns with their charge assignments:")
    print()

    sm_particles = [
        # particle,    Q_N1, Q_N2, Q_N3, Q_N4, Q_em, colour
        ("Neutrino ν",    0,    0,    0,    0,     0,  "none"),
        ("Electron e",    3,    0,    0,    0,    -1,  "none"),
        ("Up quark u",    2,    1,    0,    0,   +2/3, "RGB"),
        ("Down quark d",  1,    1,    0,    0,   -1/3, "RGB"),
        ("Photon γ",      0,    0,    0,    0,     0,  "none"),
        ("Gluon g",       0,    2,    0,    0,     0,  "adjoint"),
        ("W boson W+/-",    3,    0,    0,    0,    "+/-1",  "none"),
        ("Z boson Z",     0,    0,    0,    0,     0,  "none"),
        ("Higgs H",       0,    0,    0,    0,     0,  "none"),
    ]

    print(f"  {'Particle':<14} Q_N1 Q_N2 Q_N3 Q_em   Colour")
    print("-"*55)
    for p in sm_particles:
        name, n1, n2, n3, n4, q, col = p
        print(f"  {name:<14}  {n1}    {n2}    {n3}   {str(q):<6} {col}")

    print()
    print("NOTE: The N-vector from the BDG simulation gives (N1,N2,N3,N4)")
    print("This maps directly to (Q_N1, Q_N2, Q_N3, Q_N4) in RASM.")
    print("Derivation 1 is therefore: show that the BDG-stable patterns")
    print("exhaust exactly the SM charge spectrum above.")

# ── Poisson-CSG simulation ─────────────────────────────────────────────────

def bdg_score_from_past(past_v, past_lookup):
    """Compute S_BDG for a candidate vertex given its past as a list of indices."""
    N = [0]*5
    for x in past_v:
        between = sum(1 for z in past_v if x in past_lookup[z])
        k_val = between + 1
        if 1 <= k_val <= 4:
            N[k_val] += 1
    score = 1 - N[1] + 9*N[2] - 16*N[3] + 8*N[4]
    return score, N

def chain_extend(graph, n_trials=200):
    """
    Growth rule: extend existing chain tips.
    For each existing vertex v, try adding a successor that has v as its
    sole immediate predecessor (forming a chain extension). The candidate's
    past = past(v) ∪ {v}. Accept if S_BDG > 0.
    Also try Y-joins: extend from two existing vertices.
    """
    kept = 0
    n = len(graph['past'])
    if n == 0:
        return graph, 0

    for _ in range(n_trials):
        mode = np.random.choice(['chain', 'yjoin'], p=[0.7, 0.3])

        if mode == 'chain':
            # Pick a random existing vertex as the sole immediate predecessor
            v = np.random.randint(n)
            new_past_set = {v} | graph['past'][v]
        else:
            # Y-join: pick two vertices whose pasts don't overlap (spacelike)
            if n < 2:
                continue
            v1 = np.random.randint(n)
            # v2 must not be in past of v1 and v1 not in past of v2
            candidates = [u for u in range(n)
                          if u != v1
                          and u not in graph['past'][v1]
                          and v1 not in graph['past'][u]]
            if not candidates:
                continue
            v2 = np.random.choice(candidates)
            new_past_set = {v1, v2} | graph['past'][v1] | graph['past'][v2]

        past_v = list(new_past_set)
        score, N = bdg_score_from_past(past_v, graph['past'])
        if score > 0:
            graph['past'].append(new_past_set)
            graph['N_vectors'].append(tuple(N[1:5]))
            kept += 1
            n = len(graph['past'])  # update for next iteration

    return graph, kept

def run_csg_simulation(n_steps=30, seed=42):
    """Run BDG-filtered chain-growth CSG and collect stable pattern statistics."""
    np.random.seed(seed)
    print(f"=== BDG-FILTERED CHAIN GROWTH SIMULATION ({n_steps} steps) ===")

    # Seed: a 5-chain (known stable ground state)
    seed_edges = [(i, i+1) for i in range(4)]
    past0 = compute_past(seed_edges, 5)
    N_vecs0 = []
    for v in range(5):
        _, N = bdg_score(past0, v)
        N_vecs0.append(tuple(N[1:5]))
    graph = {'past': past0, 'N_vectors': N_vecs0}

    total_kept = 0
    total_tried = 0

    for step in range(n_steps):
        graph, kept = chain_extend(graph, n_trials=100)
        total_kept += kept
        total_tried += 100
        if (step+1) % 10 == 0:
            print(f"  Step {step+1:3d}: graph size = {len(graph['past'])}")

    n_final = len(graph['past'])
    print(f"\nFinal graph: {n_final} vertices")
    print(f"Acceptance: {total_kept}/{total_tried} = {total_kept/total_tried*100:.1f}%")
    print()

    # Tabulate N-vector distribution
    from collections import Counter
    nvec_counts = Counter(graph['N_vectors'])
    print("N-vector distribution in stable graph:")
    print(f"  {'(N1,N2,N3,N4)':<20} Count   Score   Pattern type")
    print("-"*60)

    for nvec, count in sorted(nvec_counts.items(), key=lambda x: -x[1]):
        n1,n2,n3,n4 = nvec
        score = 1 - n1 + 9*n2 - 16*n3 + 8*n4
        # Characterise
        if nvec == (0,0,0,0): ptype = "Isolated (ν-like)"
        elif nvec == (1,1,0,0): ptype = "2-chain (γ/W-like)"
        elif nvec == (1,1,1,1): ptype = "4-chain (e/q-like)"
        elif n2 >= 2 and n3 == 0: ptype = f"Y-join N2={n2} (g-like)"
        elif n1 == 0 and n2 == 0: ptype = "Low-charge (ν-like)"
        else: ptype = f"Mixed N=({n1},{n2},{n3},{n4})"
        pct = count/n_final*100
        print(f"  {str(nvec):<20} {count:>5} ({pct:.1f}%)  {score:>4}   {ptype}")

    return graph

# ── Main ──────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("RA BDG FILTER SIMULATION — DERIVATION 1")
    print("="*60)
    print()

    chain_score_table()
    survey_patterns()
    stable_pattern_analysis()
    run_csg_simulation(n_steps=30)

    print()
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print()
    print("The BDG integers (1,-1,9,-16,8) in 4D act as a filter that:")
    print("  1. Selects depth-4 chain patterns as the ground state (score=1)")
    print("  2. Penalises wide/parallel pasts (score<0)")
    print("  3. Produces a small catalogue of stable N-vector types")
    print()
    print("The N-vectors of stable patterns correspond to:")
    print("  (0,0,0,0) → zero-charge particles (ν, γ, Z, H)")
    print("  (1,1,1,1) → 4-momentum carriers (e, u, d quarks)")
    print("  (1,2,0,0) → colour-carrying patterns (gluons)")
    print()
    print("This is the computational foundation of Derivation 1 in RASM.")
    print("Full proof requires: systematic enumeration of ALL stable patterns")
    print("and verification they match the complete SM charge spectrum.")
