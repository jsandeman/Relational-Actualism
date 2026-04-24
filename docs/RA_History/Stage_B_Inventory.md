# Stage B — Python Scripts Inventory

**Started:** April 19, 2026
**Discipline:** Pure cataloging — no interpretation, no assessment of
correctness. Each entry answers: what does the script claim to do
(from its own docstrings/comments), what does it actually import/call,
what does it produce, and what claimed result does it support (if any,
per the author)?

**Status tags used:**
- `canonical` — current, load-bearing for a paper claim
- `canonical, needs_work` — current but incomplete
- `superseded` — replaced by a newer script; content archived only
- `historical` — early exploration, not currently referenced
- `exploratory` — proof-of-concept or scaffolding
- `unknown` — awaiting Joshua's confirmation
- `ARCHIVED` — removed from canonical set (see Archive Sub-Pass below)

---

## Archive Sub-Pass — April 20, 2026

Executed after 25 scripts catalogued. Goal: remove clearly obsolete
or broken scripts from the canonical set before resuming Stage B.

### Scripts to archive (5 items)

| # | Script | Reason | Tag |
|---|--------|--------|-----|
| 1 | `d3i_RA_RG.py` | Byte-identical duplicate of `d3i_complete.py` (MD5 match). Keeping the `_complete` filename as canonical. | SUPERSEDED |
| 2 | `Yeats_BDG_MCMC.py` | Sign error in C_K array (missing signs at k=1,3). Numba `nk_totals` race condition. Doesn't actually verify Yeats moments it claims to verify. Superseded by `D1_BDG_MCMC_simulation.py` which uses correct signs. | SUPERSEDED |
| 3 | `RA_CSG.py` | Two `__main__` blocks. `NameError: count_bdg_intervals undefined` on execution. Computes path counts `sum(A^k)` labeled as BDG N_k — these are different quantities. Broken as written AND conceptually wrong. | BROKEN |
| 4 | `mobius_uniqueness.py` | Explicit `Match: False` in output. Formula `C_k = (-1)^(k+1) Γ(k+2)/Γ(2)` produces [1,-3,13,-71,465] not [1,-1,9,-16,8]. | HISTORICAL |
| 5 | `uniqueness_compute.py` | Proposed self-consistency criterion (E[N_k \| S>0] = E[N_k]) is minimized by trivial filters (all c_k=0); BDG is not a local minimum. The criterion does not select BDG. | HISTORICAL |

### Suggested archive layout (local):

```
scripts/
├── archive/                              ← create this directory
│   ├── d3i_RA_RG.py                      ← Entry 15, duplicate
│   ├── Yeats_BDG_MCMC.py                 ← Entry 19, signs + race
│   ├── RA_CSG.py                         ← Entry 20, broken
│   ├── mobius_uniqueness.py              ← Entry 21, Match: False
│   └── uniqueness_compute.py             ← Entry 22, criterion wrong
└── [remaining canonical scripts]
```

A `archive_obsolete_scripts.sh` helper is in `/mnt/user-data/outputs/`
you can review and adapt to your local layout. Does not delete
anything — just moves to `archive/`.

### NOT archived, but flagged for narrative repair

Five scripts from entries 1–25 have real computational content with
docstring/ASSESSMENT text that overstates or misrepresents the output.
These stay in the canonical set; repair is editorial, not structural.

| # | Script | Repair needed |
|---|--------|---------------|
| R1 | `d3_alpha_s_proof.py` (Entry 13) | "COMPLETE PROOF" framing in docstring; α_s (m_Z) = 1/√72 is a CV-tier identification, not a proved theorem |
| R2 | `d3i_complete.py` (Entry 16, now sole copy after archiving Entry 15) | Docstring claims f₀ = 5.38 / 0.6% error; actual output is 5.29 / 2.35% |
| R3 | `o14_proof.py` (Entry 23) | Step D claim "Σ C_i = 0 is specific to d=4 moments" is false (holds for all even d at K=d/2+2 by hockey-stick). Replace with D4U02 modular-barrier argument as the d=4 selector |
| R4 | `bdg_multicoupling.py` (Entry 25) | ASSESSMENT paragraph claims "W/Z bosons within ~1 OOM" (both are 1.6 OOM off) and "cross-force hierarchy" predicted (model actually predicts ~same lifetime for neutron, pion, rho). Keep the 6 strong-resonance results; rewrite the assessment |
| R5 | `D1_BDG_MCMC_simulation.py` (Entry 18) | G_F label — script computes G_F but labels output as G_F/√2 (per Entry 18 Flag 3) |

These aren't archive candidates because the underlying computations are
doing real work; the prose misrepresents the match quality. Prose fixes
needed before Stage C cites them.

### Questions still open on archive decisions

- **Entry 11 `d2_two_phases.py`**: catalogue flagged as `needs_work` —
  two phases identified (0.60/0.40) don't match any observed 2-phase
  structure. Keep as exploratory, or archive?
- **Entry 14 `vwyler_proof.py`**: V_eff(μ=1)=1 computation is correct
  arithmetic, but the "μ=1 is critical point" framing is misleading
  (not a critical point; V_eff(0.5)=1.25, V_eff(2)=35). Keep canonical
  or `canonical, needs_work`?

I haven't auto-archived these two — they're your call.

---

## Entry 1: `assembly_mapper.py`

**Status:** `needs_work`
**Lines:** 59 — **In scripts.txt:** ❌ — **Target:** Paper IV

- Stated purpose: convert SMILES → NetworkX graph, print max Cronin-Walker
  A(M) = N_bonds − 1.
- No RA-specific computation (no BDG, σ-filter, LLC). Dead imports
  (`numpy`, `Draw`). Hardcoded one molecule. Not evidence for any
  specific Paper IV claim.

---

## Entry 2: `born_rule_derivation.py`

**Status:** `needs_work`
**Lines:** 352 — **In scripts.txt:** ✅ — **Target:** Paper I

- Stated purpose: derive P(snap at x) = |ψ(x)|² from kinematic snap +
  competing Poisson processes.
- **Key flag:** Section 3 "verification" is computational identity
  (`rate = lam0·psi²`, `snap = rate/∫rate`, checks `snap ≈ psi²` after
  ψ-normalization).
- Section 4 two-detector case recovers the 0.70/0.30 input amplitudes
  — self-consistency, not independent check.
- Premise `rate ∝ |ψ|²` asserted in prose citing QFT locality, not derived.
- Summary table marks many items DERIVED/DISSOLVED/EXPLAINED that are
  discursive claims.

---

## Entry 3: `ra_flat_rotation_curve.py`

**Status:** `needs_work`
**Lines:** 65 — **In scripts.txt:** ✅ — **Target:** Paper III (DM)

- Stated purpose: rotation curve from RAGC weak-field limit.
- **Key flag:** `xi = (v_flat_target/(2c))²` → `v_lambda = v_flat_target`
  by construction. Flat curve at 220 km/s follows algebraically.
- Comment claims ξ "derived from the covariant field equation's weak-field
  limit" — derivation not in script.
- No comparison to rotation curve data; matplotlib plot only.

---

## Entry 4: `bullet_cluster.py`

**Status:** `needs_work`
**Lines:** 366 — **In scripts.txt:** ✅ — **Target:** Paper III (DM)

- Stated purpose: test λ-gradient mechanism against Bullet Cluster data.
- **Good epistemic hygiene:** self-tags final verdict "FRAMEWORK CONSISTENT,
  NOT YET PROVED" and lists 3 hard walls explicitly.
- Core per-baryon rates (n_star=1e57, Γ_star=1e14, Γ_gas_pre=1e6) are
  hand-chosen order-of-magnitude estimates, not derived.
- Unified equation ∇²Φ = 4πG[ρ_A + ρ_λ] proposed, not derived from P_act.

---

## Entry 5: `casimir_benchmark.py` (v2)

**Status:** `needs_work`
**Lines:** 331 — **In scripts.txt:** ✅ — **Target:** Paper I / Paper III
(AQFT)

- Stated purpose: reproduce Casimir, verify RA prescription, D2/D3 content.
- **Key flag:** Casimir result plugged in (`u = -π²ℏc/(720d⁴)` is textbook
  zeta-regularized value). Tracelessness is algebraic from the definition.
- Section 2 "conservation check" is prose only; no differentiation performed.
- Vacuum suppression is definitional (subtracting vacuum from itself).
- Numerical benchmark reproduces the standard experiment-matching value
  because the RA prescription is constructed to preserve it.

---

## Entry 6: `rindler_relative_entropy.py`

**Status:** `needs_work` — **load-bearing for IC46**
**Lines:** 531 — **In scripts.txt:** ✅ — **Target:** Paper I §6.6

- Stated purpose: verify frame-independence of actualization criterion
  via relative entropy.
- **Key flag:** Core analytical proof imports `Λ|0_M⟩ = |0_M⟩` as
  "STANDARD" — this IS the `vacuum_lorentz_invariant` axiom flagged in
  IC46. Proof inherits the IC46 gap.
- Section 6 numerical boost test self-flagged inadequate (finite-truncation
  artefact, squeeze-transformation can't be represented in 4 levels).
- Replacement test verifies only generic unitary invariance of relative
  entropy — standard math result, not Rindler-specific.
- Stationarity is algebraic consequence of (vacuum invariance) + (unitary
  invariance), not independent verification.

---

## Entry 7: `RA_RASM_Verification.py`

**Status:** `canonical, needs_work` (per Joshua, Apr 19)
**Lines:** 155 — **In scripts.txt:** ✅ — **Target:** Paper II (RASM)

### Stated purpose
"Systematic numerical verification of RASM v1.7"

### Epistemic hygiene
- **Explicit NATIVE vs HYBRID tagging throughout.** Section 4 header
  verbatim: "[α_EM and α_s are external inputs, not BDG-derived]".
  This is the cleanest self-identification of external inputs among
  the canonical scripts.

### Inputs (all hardcoded from PDG)
- Lepton/quark masses, neutrino Δm², CKM elements V_us, V_cb
- Couplings: α_EM = 1/137.035999084, α_s(M_Z) = 0.118
- Hardcoded neutrino angle: `thNu = -0.47787`

### Dependencies
`numpy`, `scipy.optimize` (`fsolve`, `brentq`), `scipy.integrate.quad`

### Reproducibility
Deterministic (no randomness).

### Flags

1. **NATIVE identities are trigonometric/DFT facts, not RA physics.**
   `sum_k cos(θ+2πk/3)=0`, `phi_1 = √6/2·e^(-iθ)` are math identities
   true for any θ. Their role is to confirm the Koide parametrization's
   algebraic consequences, not to establish physics.
2. **θ_lep = 2/9 is asserted, not derived.** Script verifies that the
   θ extracted by fitting (m_e, m_μ) matches 2/9; the prediction θ=2/9
   itself is not derived in this file.
3. **m_τ "prediction" is a Koide-fit consequence.** `fsolve` fits m₀, θ
   from (m_e, m_μ) alone; the predicted m_τ is then 0.1% accurate.
   Tests Koide's known empirical accuracy; does not derive it.
4. **Neutrino Section 7 depends on hardcoded `thNu = -0.47787`.**
   Σm_ν ~ 59 meV "prediction" is contingent on this angle. Origin of
   -0.47787 not shown in file.
5. **Wyler formula claim.** `w1920 = (9/(8π⁴))·(π⁵/1920)^(1/4)` matches
   α_EM to 0.00006%. The specific denominator 1920 = 2⁴·5! is identified;
   its derivation from BDG not in this file.
6. **Section 4 uses imported SM Casimirs** (C₂ = 4/3 for color, etc.)
   with hardcoded matching scale and fit target α_s(1.66GeV)/π = 0.08880.
7. **Joshua's Apr 19 assessment fits well for this script.** PDG values,
   α_EM, α_s, C₂ Casimirs are all external inputs; explicitly tagged.

---

## Entry 8: `RA_D1_Proof.py` (v3)

**Status:** `canonical, needs_work` (per Joshua, Apr 19)
**Lines:** 256 — **In scripts.txt:** ✅ — **Target:** Paper II §2
(five-topology classification)

### Stated purpose
"Computational Proof of RASM Derivation 1" — three theorems.

### Key distinction from RA_RASM_Verification.py
**This script's computational core is genuinely RA-native.** No QFT, no
GR, no PDG data. Only BDG integers + DAG combinatorics. The SM
interpretation is an overlay at the end, not in the computation.

### Inputs
- BDG = (1, -1, 9, -16, 8) hardcoded
- `n_max` via CLI, default 6

### Dependencies
Pure stdlib: `sys`, `itertools.combinations`, `itertools.permutations`,
`collections.defaultdict`. No numpy, no scipy.

### Reproducibility
Deterministic.

### Three theorems (as stated in docstring)
- **D1a (PROVED algebraically):** BDG-stable chain depths in 4D are
  exactly k ∈ {0, 2, 4}.
- **D1b (PROVED by enumeration):** Minimum topological N-vectors are
  (1,2,0,0) and (2,1,0,0).
- **D1c (CONJECTURAL):** Neither topological type has a BDG-stable
  self-similar chain extension. Explicitly self-flagged.

### Flags

1. **D1a is bounded exhaustive check.** Chain scores at k=0..10
   computed. At k=0,2,4: scores +1, +9, +1. At k=1,3: -1, -7. The
   `assert set(stable) == {(0,0,0,0),(1,1,0,0),(1,1,1,1)}` line
   mechanizes the claim. Sound.
2. **D1b is bounded enumeration.** At n_max=6, enumerates all
   weakly-connected DAGs up to 6 vertices. The final assert
   `all(sz >= 5 for nv, sz in min_size.items() if nv not in minimal)`
   confirms no topological N-vector other than (1,2,0,0) and (2,1,0,0)
   appears at size ≤ 4. With n_max=6, this is a genuine bounded claim.
3. **`canonical_form` uses O(n!) permutation enumeration.** 720 perms
   per graph at n=6. Correct for isomorphism but slow.
4. **D1c tests one specific extension type (chain append at tip) for
   two specific base patterns.** The conjectural claim is stronger — no
   self-similar extension stabilizes — and is not fully tested.
5. **Physical interpretation section is overlay, not derivation.**
   Verbatim: "Sequential → leptons, photons, W/Z/H" and "Topological →
   quarks, gluons". The SM mapping is asserted. If stripped, the
   computational core is RA-native.
6. **Cross-reference to Lean.** `RA_D1_Proofs.lean` is tagged 124
   extension cases Lean-verified. Cross-check against this Python
   enumeration is a Stage C task.

---

## Entry 9: `RA_BDG_Simulation.py`

**Status:** `canonical, needs_work` (per Joshua, Apr 19)
**Lines:** 318 — **In scripts.txt:** ✅ — **Target:** Paper II
(RASM Derivation 1)

### Stated purpose
"Derivation 1 (RASM): BDG-filter stable pattern enumeration."

### Structure
Four sections: chain score table, hand-picked pattern catalog (16
patterns), SM particle-matching block, Monte Carlo CSG simulation.

### Inputs
- BDG integers hardcoded
- 16 hand-picked pattern edge lists
- CSG simulation: seed=42, 70/30 chain/Y-join split, 100 trials/step,
  30 steps, seed pattern is a 5-chain

### Dependencies
`numpy` (random), `itertools`, `collections`.

### Reproducibility
`np.random.seed(42)` fixed. Simulation reproducible.

### Flags

1. **Substantive overlap with `RA_D1_Proof.py`.** Both compute chain
   scores for k=0..8. D1_Proof handles this rigorously as a theorem;
   this script does it as part of a tabular survey. Stage C question:
   which is canonical? Redundant verification or divergent purposes?
2. **16-pattern survey is non-exhaustive.** Edge lists are hand-picked;
   selection criterion not stated.
3. **`stable_pattern_analysis()` overlays SM identifications directly.**
   Lines 126–138: `(0,0,0,0) → Neutrino`, `(1,1,0,0) → Photon or W/Z —
   depth 2 = spin 1?`, etc. Question marks and "Photon or W/Z" hedging
   show these are speculations, not derivations.
4. **SM charge-assignment table has internal inconsistencies.** With
   the stated mapping `Q_em = Q_N1 × e/3`:
   - Electron `Q_N1=3, Q_em=-1`: mapping gives `+1`, not `-1`. Sign
     mismatch.
   - W boson `Q_N1=3, Q_em=±1`: same Q_N1 as electron, ambiguous signs.
   - Neutrino, photon, Z, Higgs all have `Q_N1=Q_N2=Q_N3=0` — same BDG
     signature for four distinct particles.
   The charge-assignment scheme as written doesn't consistently produce
   the SM spectrum.
5. **Pattern labeling error: "Double Y-join"** has edges creating a
   3-in-2-out fan, not a standard Y-join. Terminology issue, not
   correctness issue.
6. **CSG simulation parameters (mode probabilities, seed pattern)
   are hardcoded, not derived.** The resulting N-vector distribution
   is a sample from an ad-hoc growth process.
7. **Self-flagged scope limit (verbatim):** "Full proof requires:
   systematic enumeration of ALL stable patterns and verification they
   match the complete SM charge spectrum." Acknowledges the goal is
   not achieved in the script.

---


## Entry 10: `d2_two_phases.py`

**Status:** `needs_work`
**Lines:** ~220 — **In scripts.txt:** likely ✅ — **Target:** Paper II (QCD
confinement at μ=1), Paper III (CMB acoustic peaks via ρ_A)

- Stated purpose: confirm two-phase structure of BDG-filtered Poisson-CSG
  at the μ=1 transition; state (self-labeled) conjecture identifying this
  with QCD confinement; advance qualitative CMB acoustic peak argument.
- **Real computational content:** Monte Carlo Poisson sampling with
  λ = (μ, μ², μ³, μ⁴), BDG score `1 - n1 + 9*n2 - 16*n3 + 8*n4` applied,
  survival rate P(S>0) and N₁-entropy computed exactly. 500k samples, seed
  42. The Poisson-CSG statistics and BDG score computation are correct
  and RA-native.
- **Flag 1 — "Elementary" stipulation.** Code defines elementary = (N₁≤2)
  ∧ (N₂≤2), labeled "PIP-constrained." Derivation of this criterion not
  in script. The headline claim "elementary fraction > 0.5 below μ=1" is
  sensitive to this stipulation.
- **Flag 2 — QCD identification is self-labeled CONJECTURE.** Good
  epistemic hygiene: docstring explicitly says "Conjecture supported by
  qualitative argument; quantitative derivation requires Hard Wall 1
  (BDG-filter MCMC for V_coh)."
- **Flag 3 — CMB acoustic-peak argument self-critiqued.** Script walks
  through a mechanism (ρ_A non-oscillating, plays CDM role), then
  identifies a quantitative problem ("If ρ_A >> ρ_λ at recombination,
  then RA would predict WAY TOO MUCH CDM-equivalent density — the even
  peaks would be suppressed, not enhanced"), then admits "RESOLUTION
  NEEDED." The framework-HAS-a-mechanism claim survives; the magnitude
  claim does not.
- **Flag 4 — Erdős-Rényi framing is heuristic.** The μ=1 transition is
  called "the Erdős-Rényi giant-component threshold applied to the causal
  graph." ER applies to undirected random graphs without a filter; the
  BDG-filtered Poisson-CSG is neither. Analogy, not derivation.
- **Flag 5 — μ=0.70 "today in baryons" is an input.** The claim that μ
  has evolved from >>1 at nucleation to ~0.70 today in baryons is not
  derived in this script — it's asserted as context.

---

## Entry 11: `d3_alpha_s_BDG.py`

**Status:** `needs_work`
**Lines:** 17 — **In scripts.txt:** likely ✅ — **Target:** RASM, Paper II
(α_EM, α_s, f_0)

- Stated purpose: print Wyler formula for α_EM and BDG formula for
  α_s(m_Z) = 1/√(c₂·c₄).
- **Real computational content:** Wyler formula `(c₂/(2^(d-1)π^d)) ·
  (π^D/(2^d·D!))^(1/d)` with c₂=9, d=4, D=5. Reproduces 1/137.036 to
  ~0.0001% (numerically verified: 137.036082 vs PDG 137.036). α_s =
  1/√72 = 0.117851 vs PDG 0.118000 (0.13% match).
- **Flag 1 — Wyler formula requires π.** This is the classic Wyler (1969)
  geometric-group-theoretic construction. π is a continuum object; its
  appearance means the formula is not native to DAG+BDG+LLC primitives.
  The accuracy is striking, but it's a HYBRID identification, not a
  from-scratch derivation.
- **Flag 2 — α_s = 1/√72 is arithmetic from BDG coefficients.** This part
  is structurally clean IF one accepts the physical identification that
  the c₂·c₄ product sets the α_s scale at μ=1. That identification is in
  `d3_alpha_s_proof.py` — see Entry 12.
- **Flag 3 — f_0 computation is off.** Script prints `f₀ = 17.32 × 0.31
  ≈ 5.37` with target 5.416. Actual: 17.32 × 0.31 = 5.3692 — 0.9% off,
  not 0.07% (the memory-edit-claimed match). The precise match requires
  QCD running — see Entry 13.

---

## Entry 12: `d3_alpha_s_proof.py`

**Status:** `canonical` per memory edit #6 ("Scripts d3_alpha_s_proof.py
at outputs")
**Lines:** 26 — **In scripts.txt:** likely ✅ — **Target:** RASM
(α_s(m_Z) = 1/√72 claim)

- Stated purpose: "COMPLETE PROOF: alpha_s(m_Z) = 1/sqrt(c2·c4)."
- **What the script actually does:** three `assert` statements on BDG
  coefficient identities, followed by `1/math.sqrt(c2*c4)` arithmetic
  and a print statement.
- **Flag 1 — "COMPLETE PROOF" is overstated.** The Lean-like structure
  in the docstring (Lemmas 1–3, Steps 1–3, "QED") is narrated, not
  verified in code. The three assertions test:
  - `c₀+c₁ = 0` ✓ (Lemma 1 basis — verified)
  - `c₀+2c₁+c₂ = c₄` ✓ (Lemma 2 basis — verified, both = 8)
  - `c₁+c₂+c₃+c₄ = 0` ✓ (stated as "Lemma 3 basis: sum(c_k)=0")
- **Flag 2 — Inconsistency: docstring "Σc_k=0" vs assertion "c₁+c₂+c₃+c₄=0".**
  The assertion sums c₁..c₄, not c₀..c₄. Full Σ_{k=0}^{4} c_k = 1, NOT 0.
  The "second-order operator" argument cited in the docstring requires
  a specific sum structure that the assertion tests, but the docstring
  labels it imprecisely.
- **Flag 3 — E[S_virtual]=1 at μ=1 is asserted in docstring, not tested.**
  This is the key probabilistic claim linking the BDG coefficient
  arithmetic to the physical α_s identification. No Monte Carlo or
  analytic verification in code.
- **Flag 4 — Physical identifications are stipulated.** The chain
  "S_photon = c₂" (photon ↔ depth-2), "S_quark = c₄" (quark ↔ depth-4),
  "amplitude = √(path weight)" are asserted in the docstring. These are
  QFT-style moves; they are not verified from DAG+BDG+LLC in the code.
  The "proof" is really: given these identifications + given the BDG
  coefficient identities, 1/√72 follows arithmetically. The identifications
  are the work; they're elsewhere (if anywhere).
- **Verdict:** The arithmetic is correct. The framing ("COMPLETE PROOF")
  overstates what the code establishes. Under the Apr 17 framing
  discipline, this is a consistency check of arithmetic + stipulated
  physical identifications, not a proof from primitives.

---

## Entry 13: `qcd_running_proof.py`

**Status:** `needs_work`
**Lines:** ~30 — **In scripts.txt:** likely ✅ — **Target:** f_0 (Paper III
baryon/DM ratio)

- Stated purpose: compute `alpha_s(2 m_p = 1877 MeV) = 0.312` from FLAG
  2021 lattice anchor + 2-loop running, then confirm `f_0 = 17.3151 ×
  alpha_s(2m_p) ≈ 5.42`.
- **Real computational content:** scipy `solve_ivp` integration of the
  2-loop QCD β-function `β₀(n_f) = (33−2n_f)/6`, `β₁(n_f) = (306−38n_f)/24`
  from 2 GeV down to 2 m_p ≈ 1877 MeV with initial condition
  `alpha_s(2 GeV) = 0.3024` (FLAG 2021, 4-loop lattice anchor), n_f = 3.
  Standard QCD running; the RGE and β-coefficients are textbook.
- **Flag 1 — Entirely QCD machinery, not RA-native.** β-function coefficients
  are standard perturbative QCD. Lattice anchor is external input. RGE
  integration is a QCD-field-theoretic construct. None of this traces to
  DAG + BDG + LLC. Under the Apr 17 framing discipline this is a HYBRID
  calculation: it uses QCD running with a QCD-lattice input to obtain the
  numerical factor that the BDG combinatorial identity 17.32 is multiplied
  against.
- **Flag 2 — BDG prediction for α_s(m_Z) is printed but NOT used.** Line:
  `alpha_s_mZ_BDG = 1/math.sqrt(72)`. It's computed and displayed, then
  ignored. The RGE integration starts from FLAG's 0.3024 at 2 GeV, not
  from 1/√72 run down from m_Z.
- **Flag 3 — Missing cross-check.** If BDG's α_s(m_Z) = 0.1179 is correct,
  running it forward to 2 GeV via QCD RGE should give ≈ FLAG's 0.3024.
  The ratio 0.3024 / 0.1179 = 2.566 is consistent with standard QCD
  running from m_Z to 2 GeV (factor ≈ 2.5–2.6 via 2-loop RGE with n_f
  varying across quark thresholds). Informal agreement, but the script
  does not verify this consistency — it would be a 5-line addition.
- **Flag 4 — The factor 17.32 is imported from Paper II.** W_other/W_baryon =
  17.32 (structural claim per memory edit). Not computed in this script.
  f_0 match is (BDG structural factor) × (QCD-running α_s evaluated at
  a stipulated scale), not a BDG-from-primitives result.

---
## Entry 14: `vwyler_proof.py`

**Status:** `canonical, narrative_repair` (Apr 20 sub-pass v2
reclassification. Arithmetic is correct and closes a real gap in Entry
12's chain; narrative needs R6 repair for the "critical point at μ=1"
misconception.)
**Lines:** 12 — **In scripts.txt:** likely ✅ — **Target:** RASM / Paper II
(closes "V_eff(μ=1) = 1" subclaim used in α_s = 1/√72 argument)

- Stated purpose (docstring): "V_eff(mu=1)=1: proof that the BDG Wyler
  volume factor is unity at mu=1."
- **Code content:** one assertion `c₁+c₂+c₃+c₄ == 0`, one definition
  `V_eff_at_1 = c₀ + c₁+c₂+c₃+c₄`, one assertion `V_eff_at_1 == 1`, then
  the `T = c₂ × V_eff(1) × c₄ = 72` arithmetic and `α_s = 1/√72` print.
- **This script closes a real gap from Entry 12.** `d3_alpha_s_proof.py`
  asserted in its docstring "Lemma 3: E[S_virtual]_{μ=1} = 1 [from
  sum(c_k)=0, second-order operator]" but did not verify that claim in
  code. `vwyler_proof.py` makes the identity explicit:
  `V_eff(1) := c₀ + Σ_{k=1}^{4} c_k = 1 + 0 = 1`.
- **Independent MC verification (500k samples, Poisson(μ^k) with μ=1):**
  E[S|μ=1] = 1.006, consistent with V_eff(1) = 1 under the Poisson
  expectation identity E[N_k] = μ^k.
- **Flag 1 — "d'Alembertian: Σc_k = 0" comment is more precise here.**
  The comment on the assertion correctly refers to the partial sum
  `c₁+c₂+c₃+c₄ = 0`. This resolves the docstring-vs-code inconsistency
  flagged in Entry 12. Under Benincasa-Dowker 2010 this partial sum =
  0 is the condition making the discrete d'Alembertian converge to the
  continuum ∂² operator; that is genuine BDG literature, not stipulation.
- **Flag 2 — V_eff is evaluated only at μ=1.** Script does not define
  V_eff(μ) as a function; only computes the value at μ=1. The full
  polynomial V_eff(μ) = c₀ + c₁μ + c₂μ² + c₃μ³ + c₄μ⁴ is not flat
  (e.g., V_eff(0.5) = 1.25, V_eff(1.5) = 6.25, V_eff(2) = 35). So
  "V_eff(1) = 1" is a point value, not a generic property. μ=1 is
  *not* a critical point of V_eff — its derivative at μ=1 is
  c₁+2c₂+3c₃+4c₄ = -1+18-48+32 = 1, not 0.
- **Flag 3 — Poisson-expectation step implicit.** Under E[N_k] = μ^k with
  N_k ~ Poisson(μ^k), the BDG polynomial value coincides with E[S|μ].
  The script computes the polynomial value; the identification with
  E[S] is implicit via the Poisson mean identity, not stated.
- **Flag 4 — Physical identifications still stipulated.** The chain
  "T = c₂ × V_eff × c₄ is path weight photon→quark" and "amplitude =
  √(path weight)" are asserted in the comment on line defining `T`.
  Same framing-discipline caveat as Entry 12. What this script genuinely
  adds is the V_eff(1)=1 step; it does not close the physical-
  identification gap.
- **Verdict:** tighter and more disciplined than `d3_alpha_s_proof.py`.
  Adds one verified arithmetic step to the α_s chain (V_eff(1) = 1 via
  d'Alembertian condition). Still requires the external photon↔c₂,
  quark↔c₄, amplitude=√weight identifications to reach α_s = 1/√72.

---

## Entry 15: `d3i_RA_RG.py`

**Status:** `ARCHIVED — SUPERSEDED` (Apr 20, 2026. Byte-identical duplicate
of Entry 16 `d3i_complete.py`. Kept `_complete` filename as canonical.)
**Lines:** ~65 — **In scripts.txt:** likely ✅ — **Target:** RASM / Paper II
(α_s RG two-state model, IR/UV fixed points, Q_eff chain for f_0)

- **CRITICAL: this file is byte-identical to `d3i_complete.py`** (Entry
  16). Same MD5 hash `2a1eeae8e4b992f8e888137270898b07`. One is a
  duplicate, rename, or copy-paste of the other. Only one should be
  canonical; the other is `superseded` or should be deleted.
- Stated purpose (shared docstring): present the RA RG two-state model
  with UV fixed point α_s(μ→∞) = 1/√72 and IR fixed point α_s(μ→0) = 1/3,
  and chain to f_0 = 17.32 · α_s(Q_eff).
- **Real computational content:**
  - `S_eff(μ) = (1-e^{-μ})·c₄ + e^{-μ}·c₀` — two-state interpolation
    between c₀=1 (IR) and c₄=8 (UV)
  - Gives α_s(∞) = 1/√(9·8) = 1/√72 and α_s(0) = 1/√(9·1) = 1/3 by
    direct substitution
  - QCD 1-loop RGE integration from 2 GeV downward to locate Q_IR such
    that `α_s^{QCD}(Q_IR) = 1/3`; result Q_IR = 1.303 GeV
  - Defines `Λ_QCD_RA := Q_IR / L = Q_IR / 4 = 0.3257 GeV`, compared
    against PDG Λ_QCD(nf=3) ≈ 0.332 GeV (2% off)
  - `Q_eff := L · W_baryon · Λ_QCD_RA = 4 · 1.5 · 0.3257 = 1.9545 GeV`
  - `f_0 = 17.3151 · α_s(Q_eff)` produces 5.2888 (Planck 5.416, **2.35%
    diff**)
- **Flag 1 — Docstring vs output mismatch.** Docstring header claims
  "5. f_0 = 17.32 · α_s(Q_eff) = 5.38  (Planck 5.416, 0.6%)". Actual
  script output: f_0 = 5.2888, **2.35% diff, not 0.6%**. The 0.6% match
  comes from a different script (Entry 16 d1_BDG_string_tension.py) that
  uses a different Q_eff. Docstring describes that other script's result.
- **Flag 2 — UV/IR "fixed points" are definitional endpoints of the
  two-state interpolator, not RG fixed points.** The two-state model
  `S_eff(μ) = (1-e^{-μ})·c₄ + e^{-μ}·c₀` interpolates between
  S_eff(0)=c₀ and S_eff(∞)=c₄ by construction. Evaluating 1/√(c₂·S_eff)
  at μ→0 and μ→∞ gives 1/√(c₂·c₀)=1/3 and 1/√(c₂·c₄)=1/√72 by
  substitution, not as fixed points of an RG flow equation. These are
  limits of a postulated interpolator, not solutions of β(α_s)=0.
  "Proved" in the docstring overstates this.
- **Flag 3 — Λ_QCD_RA is defined circularly against QCD running.**
  `Q_IR` is found by running QCD's 1-loop RGE from the FLAG lattice
  anchor α_s(2 GeV)=0.3024 downward until α_s = 1/3. Then
  Λ_QCD_RA := Q_IR/L. This defines Λ_QCD_RA in terms of the QCD RGE
  solution, not BDG primitives. The match to PDG's Λ_QCD(nf=3)=0.332 is
  approximate (2% off) and is essentially a restatement of: "the scale
  where QCD running gives α_s=1/3, divided by 4, happens to land near
  the standard Λ_QCD."
- **Flag 4 — `W_baryon = 1.5` stipulated.** Docstring calls it "proved
  from BDG combinatorics" but no computation of W_baryon appears in the
  script. It is hardcoded as `W_baryon = 1.5`. The 3/2 value is a
  memory-claim from other work; not verified here.
- **Flag 5 — The Q_eff = 2·m_p "identity" is approximate, not exact.**
  Docstring claims "Q_eff = L · W_baryon · Λ_QCD = 4 · (3/2) · Λ_QCD =
  6·Λ_QCD = 6·m₀ = 2·m_p [exact via m₀ = m_p/3, Koide]". In the actual
  run, Q_eff = 1.9545 GeV vs 2·m_p = 1.8766 GeV — **4.2% diff, not
  exact**. The "exact" modifier in the docstring is wrong for this
  computational path.
- **Verdict:** Structural chain (two-state model, endpoint evaluations,
  QCD-running-based Q_IR definition) is computationally correct, but
  the docstring numerical claims (0.6%, "exact") don't match the script's
  own output. Either the script changed without the docstring being
  updated, or the docstring was copy-pasted from Entry 16. This is the
  kind of artifact drift the Stage A/B/C audit is supposed to catch.

---

## Entry 16: `d3i_complete.py`

**Status:** `duplicate` (byte-identical to Entry 15)
**Lines:** ~65 — **In scripts.txt:** likely ✅

- **Same MD5 as `d3i_RA_RG.py`** (`2a1eeae8e4b992f8e888137270898b07`).
  Identical docstring, identical code, identical output. See Entry 15
  for full analysis.
- **Action recommendation:** resolve which is canonical, delete or
  supersede the other. Keeping two identical copies in the canonical
  script set creates maintenance risk — future edits could apply to
  one but not the other, creating real divergence.

---

## Entry 17: `d1_BDG_string_tension.py`

**Status:** `unknown` (pending tag — produces the 0.58% f_0 match the
d3i docstring claims)
**Lines:** ~60 — **In scripts.txt:** likely ✅ — **Target:** RASM / Paper II
(m_p ↔ Λ_QCD via BDG string tension, f_0 = 5.38 match)

- Stated purpose: present BDG Nambu-Goto string-tension model giving
  m_p = √(c₄ · σ_BDG) = √(c₄) · Λ_QCD, and chain to f_0 = 17.32 ·
  α_s(Q_eff).
- **Real computational content:**
  - Takes m_p = 938.272 MeV as **input** (PDG value)
  - Computes Λ_RA := m_p_PDG / √c₄ = 938.272/√8 = 331.73 MeV, compared
    against PDG Λ_QCD(nf=3) ≈ 332.0 MeV (0.08% match)
  - σ_RA := Λ_RA² = 0.11 GeV² (PDG quenched lattice ≈ 0.18 GeV²;
    qualitative match flagged as "consistent" since quenched > unquenched)
  - Q_eff := 2·√c₄·Λ_RA = 2·m_p = 1.8765 GeV (by construction, since Λ
    was defined as m_p/√c₄)
  - QCD 1-loop RGE runs FLAG 2021 lattice anchor α_s(2 GeV)=0.3024 down
    to Q_eff, giving α_s(Q_eff) = 0.3110
  - f_0 = 17.3151 · 0.3110 = 5.3847 (Planck 5.416, **0.58% diff**)
- **Flag 1 — Direction-of-derivation issue, fully explicit in code.**
  The formula is `m_p = √c₄ · Λ_QCD`. In the code the INPUT is
  `m_p_PDG = 938.272` (line: `m_p_PDG = 938.272  # MeV (input / to be
  predicted by D1)`). Λ_RA is then computed from m_p. This is m_p →
  Λ_QCD, not Λ_QCD → m_p. The 0.08% match between Λ_RA (from m_p input)
  and PDG's Λ_QCD is one numerical fact in one direction; reading this
  as "m_p predicted to 0.08%" is reading the same identity in the reverse
  direction, but the prediction direction requires independent input for
  Λ_QCD or σ. Script docstring is honest about this: "When D1 MCMC gives
  sigma: m_p = √(c₄ · σ) predicted, zero external inputs." That MCMC is
  not performed in this script; it is flagged as open.
- **Flag 2 — Q_eff = 2·m_p is by construction.** Because Λ_RA := m_p/√c₄
  and Q_eff := 2·√c₄·Λ_RA, it follows algebraically that Q_eff = 2·m_p.
  So the match "Q_eff (1876.5 MeV) = 2·m_p (1876.5 MeV)" is a tautology
  given the Λ definition — not an independent prediction. This resolves
  the Entry 15 discrepancy: the d1 script *forces* Q_eff = 2·m_p by
  definition; the d3i script *derives* Q_eff independently from QCD
  running and misses 2·m_p by 4.2%.
- **Flag 3 — The 0.58% f_0 match is genuine at the numerical level,
  given the inputs.** Granted m_p, √c₄, and FLAG lattice anchor,
  QCD RGE integration down to Q_eff=2·m_p gives α_s(2·m_p)=0.311, and
  17.32·0.311 = 5.38 vs 5.416 (0.58%). The 17.32 and √c₄ are BDG-native;
  m_p and the FLAG anchor are QCD/PDG inputs; RGE running is standard
  QCD.
- **Flag 4 — "c₄ = 8 = dim(SU(3)) = number of gluon transverse modes"
  identification.** Docstring asserts c₄ = 8 is the adjoint-representation
  dimension of SU(3) (number of gluons). This is numerically correct
  (dim SU(3) = 3² − 1 = 8) but is an IDENTIFICATION of a BDG coefficient
  with a Lie-algebra dimension. Under Apr 17 framing discipline, this
  requires derivation: why does the BDG coefficient at depth 4 equal
  dim(SU(3))? No derivation in script.
- **Flag 5 — σ = Λ² assumption.** "Each [gluon] mode contributes Λ_QCD²
  to m_p²" is the physical postulate that gives m_p² = c₄·Λ². This is
  a Nambu-Goto string assumption (flat-space string tension ~ Λ²) plus
  the gluon-mode identification from Flag 4. Postulated, not derived.
- **Verdict:** Produces the 5.38 / 0.58% match in memory edit #6. The
  f_0 match is genuine given (a) m_p from PDG as input, (b) FLAG lattice
  anchor, (c) c₄=dim(SU(3)) identification, (d) σ=Λ² string assumption,
  (e) the 17.32 from Paper II. The script does not predict m_p from BDG
  primitives — it takes m_p and recovers a known combinatorial relation.
  The MCMC that would make this prediction-like is explicitly flagged
  as open.

---

## Entry 18: `D1_BDG_MCMC_simulation.py`

**Status:** `unknown` (pending tag — docstring flags multiple load-bearing
RAGC/RASM results)
**Lines:** ~200 — **In scripts.txt:** likely ✅ — **Target:** RAGC
Derivation 1 (D1), Paper II / RASM (σ → m_p, G_F tree-level, self-dual
point, phase diagram)

- Stated purpose (docstring): "BDG-filtered Poisson-CSG: full simulation
  and physical quantity extraction. L1 CONFIRMED: σ = Λ_QCD² … G_F
  (tree level): G_F/√2 = 1.163e-5 GeV⁻² (PDG: 1.166e-5, 0.3% error)."
- **Real computational content:**
  - `compute_bdg_statistics(μ)`: Monte Carlo Poisson-CSG with N_k ~
    Poisson(μ^k / k!), applies BDG filter S = Σ c_k·N_k with signed
    coefficients (1,−1,9,−16,8), reports P_acc and ⟨S|acc⟩. Signs are
    correct in this file.
  - `run_phase_diagram()`: scans 15 μ values from 0.001 to 10, seed 42,
    500k samples each.
  - `string_tension_analysis()`: reads ⟨S|acc⟩ at low μ, identifies it
    as σ/Λ², then computes m_p_pred = √(c₄·σ).
  - `compute_GF()`: tree-level EW formula from α_EM(m_Z), sin²θ_W, m_W.
  - `self_dual_analysis()`: reports V_eff(μ=1) = 1 and endpoint α_s.
- **Flag 1 — "L1 CONFIRMED: ⟨S|acc⟩ → c₀ = 1" is a tautology.**
  Verified independently (2M samples/μ): ⟨S|acc⟩ = 1.00000 at μ=0.001,
  1.00029 at μ=0.005, 1.00091 at μ=0.01. As μ→0, Poisson concentrates
  on N_k=0 for all k, giving S = c₀ = 1 > 0 → accepted with probability
  →1 and score exactly 1. The MC is confirming that c₀ equals c₀. This
  is not evidence for σ/Λ² = c₀ as a physical relation — σ/Λ² = c₀ is
  an IDENTIFICATION made in the `string_tension_analysis` function.
  Real content: "we define σ := ⟨S|acc⟩(μ→0) · Λ²" and observe the
  numerical value, not "σ = Λ² is derived."
- **Flag 2 — Direction-of-derivation mirrors Entry 17 with Λ_QCD as
  input.** Script hardcodes `Lambda_QCD = 0.332` (PDG input). Computes
  σ_RA := 1 · Λ_QCD² = 0.110 GeV². Then m_p_pred := √(c₄·σ_RA) = √8 ·
  0.332 = 0.939 GeV, matching PDG to 0.08%. This is the *inverse*
  direction of `d1_BDG_string_tension.py` (Entry 17), which uses m_p as
  input to get Λ. Same numerical relation √c₄ · Λ_QCD = m_p, same 0.08%
  match, different hardcoded anchor. Either direction: one of {m_p,
  Λ_QCD} is PDG-input; the other is "predicted." Neither closes the
  chain to BDG primitives.
- **Flag 3 — G_F label vs. content mismatch, not a value error.** Script
  prints `G_F/√2 (RA, tree) = 1.163e-5 GeV⁻²` and compares to
  `G_F/√2 (PDG) = 1.166e-5`, reporting 0.3% match. **The LABEL is wrong.**
  The formula π·α₂/(√2·m_W²) is the standard expression for **G_F
  itself**, not G_F/√2. G_F/√2 is half that, ≈ 8.25×10⁻⁶.
  - PDG value `GF_PDG = 1.1663788e-5` at the top of the file is PDG's
    **G_F**, not G_F/√2. The variable and comparison work out because
    both sides use the same mislabeling.
  - The numerical match to PDG's G_F at 0.3% is real, given α_EM(m_Z),
    sin²θ_W, and m_W as inputs. The script effectively verifies the
    standard SM relation G_F = π·α₂/(√2·m_W²) with empirical EW inputs.
  - But the label `G_F/√2` on printed output and in the memory claim
    "G_F/√2 = 1.163e-5 GeV⁻² (PDG: 1.166e-5, 0.3% error)" is incorrect.
    Documentation fix, not a physics fix.
- **Flag 4 — G_F computation uses empirical inputs, not BDG primitives.**
  `alpha_EM_mZ = 1/127.9` (EM running to m_Z), `sin2_tW = 0.23122`
  (measured), `m_W = 80.379` (PDG). Docstring's note acknowledges:
  "sin²θ_W from BDG (GUT→EW running). m_W from PDG; BDG EW scale
  derivation is open target." So the 0.3% match is a tree-level EW
  consistency check with PDG inputs, not a BDG-from-primitives
  prediction of G_F. This is stated honestly in the note.
- **Flag 5 — P_acc "minimum at μ=1" is approximate.** Script asserts
  "P_acc(μ=1) ≈ 0.548 [simulation, minimum of P_acc curve]." Fine-grained
  scan (2M samples/μ): P_acc(0.9)=0.553, P_acc(1.0)=0.548, P_acc(1.1)
  =0.547, P_acc(1.2)=0.549. Minimum is broad and lies slightly above
  μ=1 (around μ≈1.0–1.1). The μ=1 "self-dual point" identification is
  near the minimum but not at an exactly determined extremum. Related
  to Entry 14's note that V_eff(μ) is not flat at μ=1.
- **Flag 6 — `self_dual_analysis` uses the Entry 15/16 two-state model,
  not the Poisson-CSG computed elsewhere in this file.** `V_eff(μ=1)=1`
  here comes from `(1-e⁻¹)·c₄ + e⁻¹·c₀` = 0.632·8 + 0.368·1 = 5.42,
  not 1. Let me recheck — actually wait: the function definition is
  `V_eff(mu) = (1 - exp(-mu)) * c4 + exp(-mu) * c0`. At μ=1:
  (1-0.368)·8 + 0.368·1 = 5.056 + 0.368 = **5.42**, not 1. But the
  script's `self_dual_analysis` prints `V_eff(μ=1)=5.424`. Actually
  verified: the self-dual value reported is consistent with this
  definition. The Entry 14 V_eff(1)=1 is a *different* V_eff: the
  full Poisson-CSG moment Σ c_k·E[N_k]. Two scripts use the same symbol
  V_eff for two different quantities. Cross-file ambiguity worth flagging.
- **Verdict:** Three substantive results asserted:
  (a) **σ = Λ² is tautology + identification** (numerically trivial MC +
  definitional equation). Does not close "derive Λ_QCD from BDG without
  external input" — script docstring is honest about this under
  "REMAINING OPEN."
  (b) **m_p = √(c₄)·Λ_QCD to 0.08%** is a genuine BDG-integer arithmetic
  identity (c₄=8) composed with Λ_QCD PDG input. Same content as Entry
  17, reverse direction.
  (c) **G_F to 0.3%** is a tree-level SM consistency check with PDG EW
  inputs; label `G_F/√2` should be `G_F`.
  The docstring's own "REMAINING OPEN" list correctly identifies the
  gaps (Λ_QCD from BDG, m_W from BDG, α_EM from μ→0 path weight). This
  is the most epistemically honest docstring so far in the catalogue,
  even though the printed "L1 CONFIRMED ✓" could mislead a reader.

---

## Entry 19: `Yeats_BDG_MCMC.py`

**Status:** `ARCHIVED — SUPERSEDED` (Apr 20, 2026. Sign error in C_K
array, Numba race condition, does not verify Yeats moments it claims
to verify. Superseded by `D1_BDG_MCMC_simulation.py` which uses correct
signs.)
**Lines:** ~115 — **In scripts.txt:** unknown — **Target:** unclear;
possibly Yeats 2025 moment verification or O14 numerical support

- Stated purpose: "BDG/Yeats Chord Multiplicities. C_K = [1, 1, 9, 16, 8]"
  Uses Numba JIT + parallel for 4D Minkowski Alexandrov interval
  sprinkling. Claims to extract ⟨N_k⟩ at μ=1 over 10⁸ samples.
- **CRITICAL Flag 1 — BDG coefficients are wrong.** Line 8:
  `C_K = np.array([1, 1, 9, 16, 8], dtype=np.float64)`. **Missing signs
  at k=1 (should be −1) and k=3 (should be −16).** The filter
  S = Σ c_k · N_k cannot be computed with these coefficients — the
  alternating-sign structure that generates the whole BDG-filter
  mechanism is absent.
  - The script doesn't actually *use* the filter — it only computes
    ⟨N_k⟩ counts for k=0..4 and their products with |c_k|. So the sign
    error doesn't propagate into a filter computation here.
  - But labeling these values as "BDG/Yeats Chord Multiplicities" when
    they are actually absolute values of the BDG coefficients is
    misleading. Yeats 2025 moments r_k = (1, 10, 35, 84, 165) are a
    *different* sequence — they're the binomial-inversion INPUTS, while
    the BDG coefficients (with signs) are the OUTPUTS.
- **Flag 2 — `Comment C_K values are self-contradictory.** Line 5:
  "c_0 = 1, c_1 = 1, c_2 = 9, c_3 = 16, c_4 = 8" (unsigned). Memory
  edit #6, RA framework: (1, −1, 9, −16, 8). The docstring labels
  these "BDG/Yeats Chord Multiplicities" but Yeats moments r_k are
  (1, 10, 35, 84, 165), and BDG coefficients c_k are (1,−1,9,−16,8).
  Neither matches the script's C_K. This looks like an error in
  transcription, or a different (outdated/alternative) labeling.
- **Flag 3 — Alexandrov interval sprinkling is genuine causal-set
  work.** `generate_alexandrov_points(n)` rejection-samples in
  [−1,1]⁴ for points inside the double-cone between (−1,0,0,0) and
  (+1,0,0,0), with Minkowski signature (+,−,−,−). This is standard
  sprinkling for Benincasa-Dowker / Yeats work. `get_causal_matrix`
  builds the causal adjacency matrix correctly.
- **Flag 4 — Interval counting via k-element chains is correct
  structurally.** For each ordered pair (i,j) with i ≺ j, counts points
  k with i ≺ k ≺ j — this is the Benincasa-Dowker N_k definition:
  number of causal intervals containing exactly k elements.
- **Flag 5 — Parallelization bug: `nk_totals` in `prange` loop.**
  `@njit(parallel=True)` with accumulation into a shared array
  `nk_totals` is a race condition in Numba. Results may be nondeterministic
  across runs. For correct parallel accumulation, each thread should
  have a local accumulator. The simulation may still give approximately
  correct means over 10⁸ iterations (race conditions wash out in mean),
  but this is not best practice and could produce wrong standard
  deviations.
- **Flag 6 — Script does not verify Yeats moments r_k nor BDG filter
  properties.** What it computes: ⟨N_k⟩ counts. Does not compute S_BDG
  filter, does not check P_acc, does not verify that its N_k means
  match Yeats-predicted r_k × (density/volume) scalings. The script
  appears incomplete relative to its stated purpose.
- **Verdict:** Genuine causal-set sprinkling infrastructure with a
  mis-specified coefficient array, unclear target relative to the
  canonical suite (no Paper references in docstring), and a Numba
  parallelization race condition. If the intent was to verify Yeats
  2025 moments numerically, the C_K array is wrong (should be r_k =
  1, 10, 35, 84, 165). If the intent was to apply the BDG filter, the
  signs are wrong. Probable status: **early scaffolding, superseded**
  by `D1_BDG_MCMC_simulation.py` (Entry 18) which uses correct signs
  and computes the filter directly. Should likely be tagged
  `historical` or `superseded` rather than canonical.

---

## Entry 20: `RA_CSG.py`

**Status:** `ARCHIVED — BROKEN` (Apr 20, 2026. Two `__main__` blocks,
NameError on execution (`count_bdg_intervals` undefined), and computes
path counts `sum(A^k)` mislabeled as BDG N_k — conceptually wrong.)
**Lines:** ~125 — **In scripts.txt:** unknown — **Target:** apparent
intent was BDG-action response to a volume-preserving stretch of a 4D
causal diamond. No Paper reference in docstring.

- Stated purpose: sprinkle N points uniformly into a 4D causal diamond,
  apply a volume-preserving stretch `t → λt, r → λ^(−1/3)r`, compute
  ⟨S_BDG⟩ on vacuum vs stretched, report the BDG action of the
  perturbation. (Reconstructed from function names and print statements
  — the file has no docstring.)
- **Structural problems visible at read-time:**
  1. **Two `run_eccentricity_experiment` function definitions** (lines
     66 and 94) with **different signatures and bodies**. Second
     definition shadows the first at module scope.
  2. **Two `if __name__ == "__main__":` blocks** (lines 91 and 122).
     Both execute when the file is run.
  3. **Second `run_eccentricity_experiment` calls `count_bdg_intervals`,
     which is not defined anywhere in the file.** The defined function
     is `count_bdg_chains`. Running the file fails with `NameError:
     name 'count_bdg_intervals' is not defined` after the first main
     block completes.
  4. **File has no module-level docstring.** Unusual for the canonical
     set; memory edit requires RA-related work to have docstrings.
- **Runtime behavior (verified, N=500):**
  - First `__main__` runs `run_eccentricity_experiment(N=2000,
    lambda_stretch=1.02)` (first definition). Produces output:
    `Vacuum Counts: {2: 14500, 3: 84984, 4: 156061, 5: 108899}`,
    `Delta N: {2: 746, ...}`, `BDG Action of Perturbation: -159641`.
  - Second `__main__` runs the shadowed-second-definition. Fails on
    `count_bdg_intervals` NameError.
  - With N=2000 as scripted, first main block exceeds 3 minutes
    (unverified completion time — timed out at 180s).
- **Flag 1 — CRITICAL: `count_bdg_chains` does NOT compute
  Benincasa-Dowker N_k.** The function computes `sum(A^k)` for k=1..4,
  interprets these as "number of k-element chains." But the
  Benincasa-Dowker N_k is **not path counts**. It is, for each ordered
  pair (x,y) with x ≺ y, the cardinality |{z : x ≺ z ≺ y}|; then total
  N_k is the number of such (x,y) pairs where this cardinality equals
  exactly k.
  - Worked example (4-element chain x₁≺x₂≺x₃≺x₄, A = upper-triangular
    all-ones):
    - sum(A) = 6 (= all causal relations). Script calls this "N_1".
    - Actual BDG N₀ (covering links, no elements between): 3.
    - sum(A²) = 4 (= length-2 paths). Script calls this "N_2".
    - Actual BDG N₁ (exactly 1 element between): 2 (pairs (1,3) and
      (2,4)).
  - The correct BDG computation requires, for each link (i,j) with
    A[i,j]=1, computing k_count = |{m : A[i,m]=1 ∧ A[m,j]=1}| and
    histogramming over pairs. `Yeats_BDG_MCMC.py` (Entry 19) actually
    does this correctly in its inner loop — the script you just
    dismissed as `unknown`/probably-historical uses the right BDG
    definition, while this one uses path sums mislabeled as N_k.
- **Flag 2 — BDG action printed is therefore meaningless relative to
  the framework.** The `-1·ΔN_1 + 9·ΔN_2 - 16·ΔN_3 + 8·ΔN_4 = -159641`
  output is a weighted sum of path-count deltas, not the BDG scalar
  curvature proxy. No conclusion about the physics of the stretched
  diamond can be drawn from this number.
- **Flag 3 — BDG coefficients used are (-1, 9, -16, 8).** Correct
  signs on k=1,3 (unlike Entry 19). But applied to the wrong N_k
  definition (Flag 1).
- **Flag 4 — Index labeling off by one.** Script's dict keys are 2, 3,
  4, 5 (labeled as "2-element chains," "3-element chains," etc.) while
  BDG convention uses k=0,1,2,3 for intervals with 0, 1, 2, 3 elements
  between endpoints. The comment `-1*delta_N[2] + 9*delta_N[3] - ...`
  suggests the author intended to identify their "N_k for k-element
  chains" with BDG N_{k-1}, but this mapping doesn't resolve Flag 1 —
  the underlying quantity being computed is still the wrong one (path
  count, not sub-diamond count).
- **Verdict:** This file has four overlapping problems:
  (a) **Duplicated functions and main blocks** — indicates incomplete
  edit / copy-paste that was never cleaned up;
  (b) **Runtime `NameError` in the second main block** — file fails
  to complete;
  (c) **Fundamental conceptual error in `count_bdg_chains`** — computes
  path counts, not Benincasa-Dowker interval cardinality counts;
  (d) **No docstring / unclear target paper.**
  Combined, this is not a working script. The eccentricity-response
  result "BDG Action of Perturbation: -159641" should not be cited as
  evidence for any claim in the suite. Recommend `historical` (if it
  predates working D1_BDG_MCMC_simulation) or `broken`/`superseded`.
  Under no circumstance should this be `canonical`.

---

## Entry 21: `mobius_uniqueness.py`

**Status:** `ARCHIVED — HISTORICAL` (Apr 20, 2026. Script's own output:
`Match: False`. Formula produces [1,-3,13,-71,465] not BDG coefficients.
Historical exploration, not currently referenced.)
**Lines:** ~482 — **In scripts.txt:** unknown — **Target:** O14
(Möbius inversion uniqueness claim for BDG integers)

- Stated purpose (docstring): "Do the BDG integers (1, -1, 9, -16, 8)
  follow uniquely from Möbius inversion on the chain poset of a causal
  set?" The script explores three approaches and ends by testing whether
  a Möbius + Γ-ratio formula reproduces the BDG d=4 coefficients.
- **Real computational content:** a formula is proposed,
  `c_k = (-1)^k · Σ_{j=0}^k (-1)^{k-j} C(k,j) · (d/2+j)!/(d/2)!`
  for d=4, evaluated at k=0..4.
- **Flag 1 — The formula produces [1, -3, 13, -71, 465], NOT [1, -1, 9,
  -16, 8].** Script's own final print:
  ```
  BDG actual: [1, -1, 9, -16, 8]
  Formula:    [1, -3, 13, -71, 465]
  Match: False
  ```
  Verified by running the file. The proposed Möbius + Γ-ratio formula
  **does not reproduce the BDG coefficients**. The script is honest
  about this — the final line explicitly prints `Match: False`.
- **Flag 2 — d=2 result in the same formula is also wrong.** Script
  output shows for d=2: `c_0=1, c_1=1, c_2=3, c_3=11`. The correct BDG
  d=2 coefficients are (1, -2). The formula mismatch is systematic,
  not just a d=4 artifact.
- **Flag 3 — The "critical insight" prose is a research plan, not a
  derivation.** The three-step strategy stated in the script (Möbius
  fixes signs, Γ-ratios fix magnitudes, self-sustaining selects d=4)
  is aspirational — none of the three steps is actually proved or
  computed in the file. The prose describes what a purely-discrete
  uniqueness proof would require, without supplying it.
- **Flag 4 — Confusion about what "second-order" means.** Script
  correctly notes that d=2 BDG has Σc_k(k≥1) = −2 ≠ 0 (so "second-
  order" Σ=0 is a d≥4 property, not a universal axiom). Good
  observation. Then this observation is not integrated with the rest
  of the file's reasoning; the Möbius formula is applied uniformly
  anyway.
- **Flag 5 — This is the RA-native uniqueness claim that O14 Lean
  rests on.** Memory edit / Stage A: `RA_O14_Uniqueness.lean` proves
  `r = (1, 10, 35, 84, 165)` Yeats moments and `c = (1, -9, 16, -8)`
  BDG coefficients are arithmetically consistent via binomial inversion.
  The Lean file does NOT prove the coefficients are UNIQUELY determined
  (Stage A Tier 2 presentation gap + content gap: no uniqueness
  statement). This Python script attempts to supply that uniqueness
  argument and **fails by its own verification** (Match: False). The
  current status: the uniqueness claim is supported by neither the Lean
  formalization nor this Python exploration. It is an open item.
- **Verdict:** Honest exploratory script that sets out the right
  question, proposes a candidate answer, verifies the candidate, and
  reports that the candidate fails. Zero deception; this is the right
  way to handle a negative result. But the content of the script does
  NOT support any claim like "O14 uniqueness is proved via Möbius
  inversion." If a Paper II / RASM / Foundation claim cites this or
  memory edit #6 cites "O14 uniqueness (Möbius)," the cite is currently
  not backed by a working derivation. Tag recommendation:
  `exploratory` or `historical` depending on whether a working
  uniqueness argument exists elsewhere.

---

## Entry 22: `uniqueness_compute.py`

**Status:** `ARCHIVED — HISTORICAL` (Apr 20, 2026. Proposed
self-consistency criterion E[N_k | S > 0] = E[N_k] is minimized by
trivial filters (all c_k = 0); BDG is not a local minimum. Criterion
does not select BDG. Historical exploration.)
**Lines:** ~250 — **In scripts.txt:** unknown — **Target:** apparent
intent is to numerically derive BDG coefficients from a self-consistency
principle ("filtered distribution of N_k remains Poisson-consistent")

- Stated purpose (docstring): find the growth-functional coefficients
  `c_k` by requiring `E[N_k | S > 0] ≈ E[N_k]` — that is, requiring
  the BDG filter not to bias the N_k distribution. Combined with the
  second-order condition, this is claimed to "uniquely determine the
  coefficients."
- **Real computational content:** Monte Carlo scan of K=4 coefficient
  space (c₁ = −1 fixed as normalization, c₂, c₃, c₄ varied over coarse
  grid), with residual `Σ_k (bias_k − 1)²` where
  `bias_k = E[N_k | S > 0] / E[N_k]` under Poisson(μ^(k+1)/(k+1)!)
  with μ=1.
- **Flag 1 — CRITICAL: the "self-consistency" criterion is maximized
  by the trivial (identity) filter.** Verified at 2M samples: for
  coefficients `[0, 0, 0, 0]`, S = 1 is constant, every vertex
  accepted, bias_k = 1 for all k, residual = 1e-6 ≈ 0. For the birth-
  only case `[-1, 0, 0, 0]` (S = 1 − N_1), residual = 1.0 (N_1 biased
  heavily because low-N_1 states dominate acceptance). For BDG
  `[-1, 9, -16, 8]`, residual = **1.66**. For the script's declared
  "refined best" `[-1, 15, 0, -0.5]`, residual = 0.52.
  - **The script's criterion penalizes filters that filter.** A filter
    designed to preferentially select high-BDG-score vertices *must*
    bias the N_k distribution conditional on acceptance — that is the
    mechanism of selective growth. Requiring `E[N_k | acc] = E[N_k]`
    is requiring the filter to have no effect.
  - The minimum of this residual is trivially achieved at all coeffs
    = 0 (no filter at all, birth term alone accepts everything).
  - So when the script reports "BDG is NOT the unique minimum-bias
    action" with BDG at residual 1.66 and a different point at 0.52,
    it is correct that BDG doesn't minimize this criterion — but
    this is because the criterion is not a physical uniqueness
    criterion in the first place.
- **Flag 2 — Script identifies BDG is not selected.** Final output:
  "BDG neighborhood scan" shows BDG `(9, -16, 8)` is nowhere in the
  "top 15 minimum residuals" around it. The minimum in the
  neighborhood scan is at `(10, -18, 7)` with residual 1.57, ALL
  within the same order as BDG (1.58 range) and all still much larger
  than the `[-1, 15, 0, -0.5]` point identified earlier. Script does
  not resolve this: it presents the anomaly but doesn't interpret it.
- **Flag 3 — The second-order condition Σc_k = 0 is abandoned mid-
  script.** Section "K=4: Full scan WITHOUT assuming second-order
  condition" explicitly drops Σc_k = 0. The declared "refined best"
  `[-1, 15, 0, -0.5]` has Σc_k = 13.5, not 0. If Σc_k = 0 were
  restored as a constraint (as memory edit #6 / Stage A's d'Alembertian
  motivation requires), the scan's result would be invalidated by
  construction. The script's self-consistency scan and the BDG
  second-order condition are not jointly enforced.
- **Flag 4 — Outcome: no uniqueness derivation.** The script does
  not produce a derivation of BDG coefficients from self-consistency
  + second-order + any additional principles. It produces:
  (a) evidence that self-consistency alone does not uniquely
  determine BDG (the trivial filter wins);
  (b) evidence that BDG is NOT a local minimum of the proposed
  criterion.
  Neither outcome supports the uniqueness claim the script was
  ostensibly testing.
- **Flag 5 — Potentially confuses what uniqueness should look
  like.** The BDG uniqueness (O14) argument in the literature and
  in Lean is via binomial inversion on Yeats moments, giving the
  coefficients arithmetically from the d=4 moment sequence
  (1, 10, 35, 84, 165) — NOT via a "filter doesn't bias Poisson"
  requirement. This script's self-consistency criterion is a
  different proposal entirely, and a failing one. It should not be
  cited as support for O14.
- **Verdict:** Exploratory script that proposes a self-consistency
  criterion for BDG uniqueness, scans parameter space numerically,
  and (without drawing the explicit conclusion) demonstrates the
  criterion is not a physical uniqueness criterion — trivial filters
  win. The positive claim of "self-consistency uniquely determines
  the coefficients" (docstring line 23) is not supported by the
  script's own output. Tag recommendation: `historical` or
  `broken-concept`. Should not be cited as evidence for O14 uniqueness
  or any Paper II claim about BDG coefficient determination.

---

## Entry 23: `o14_proof.py`

**Status:** `unknown` (pending tag — most mature O14 attempt; contains
correct arithmetic + one incorrect uniqueness claim flagged below)
**Lines:** 427 — **In scripts.txt:** unknown — **Target:** O14 / RASM /
Foundation (uniqueness of BDG coefficients)

- Stated purpose (docstring): "Claim: The BDG coefficients for any
  dimension d are UNIQUELY determined by (1) the Yeats moment sequence
  r_k(d), (2) binomial inversion, (3) D4U02 dimension selection."
  Aims to verify the full chain.
- **Real computational content:**
  - Yeats moments r_k(d) computed via exact factorial formula
    `r_k = (n(k+1)+1)! / ((n+1)! · (nk)!)` for d = 2n. Matches
    (1,10,35,84,165) for d=4 — **correct**.
  - Binomial inversion: `C_i = Σ_{k=0}^{i-1} C(i-1,k)(-1)^k r_k`.
    Applied to d=4 r_k gives (1, -9, 16, -8). Negation gives action
    coefficients (-1, 9, -16, 8) — **matches BDG**.
  - Hockey-stick rearrangement: `Σ C_i = Σ_{k=0}^{K-1} (-1)^k C(K,k+1) r_k`.
    Evaluated at d=4, K=4: 4·1 - 6·10 + 4·35 - 1·84 = 0 — **verified**.
  - Polynomial factorization `P(z) = 1 + z(z-1)(8z²-8z+1)` — **correct**.
- **Flag 1 — Core arithmetic chain is solid.** Steps "r_k → C_i →
  action" are verified exactly. This is the first script in the
  catalogue that computes the correct d=4 BDG coefficients from the
  Yeats moments via a well-specified inversion procedure. This is the
  load-bearing arithmetic for the Lean `RA_O14_Uniqueness.lean` claims.
- **Flag 2 — The Möbius-uniqueness argument (Step B) is framework-level
  correct but has an unstated identification.** Script invokes Rota
  1964 (Möbius function of any finite poset is unique) and identifies
  the r_k as cumulative counts on the Boolean lattice. The "Critical
  Audit" section at the end acknowledges this: "the claim that the
  r_k are 'cumulative' counts with the Boolean lattice as the
  containment structure needs verification." The audit's proposed
  resolution is correct (C(k,j) sub-intervals from choosing j of k
  elements) but this lemma is not stated formally anywhere in the
  Lean corpus (Stage A).
- **Flag 3 — CRITICAL: Step 3 claim "Σ C_i = 0 is a non-trivial
  identity specific to d=4 moments" is FALSE.** Verified
  independently: `Σ_{k=0}^{K-1} (-1)^k C(K, k+1) r_k(d) = 0` holds for
  ALL even d at K = d/2 + 2 (the "natural minimal depth"):
  - d=2, K=3: 3·1 − 3·3 + 1·6 = 0 ✓
  - d=4, K=4: 4·1 − 6·10 + 4·35 − 1·84 = 0 ✓
  - d=6, K=5: 0
  - d=8, K=6: 0
  - d=10, K=7: 0
  The vanishing is a hockey-stick-identity consequence holding for
  all even d, not a d=4-specific property. The script's own d=2
  check at K=3 gives Σ = 0 (which it partially acknowledges as a
  d=2 second-order-at-K=3 fact). The printed "For d=2: Σ C_i = -1"
  in the narrative uses a different K (the historical BDG d=2 depth
  K=1 with only one N_k term); the two statements are not compatible.
- **Flag 4 — Step D "selectivity → d=4" (Step E in the theorem, via
  D4U02) is orthogonal to the Σ=0 argument.** With Flag 3, the Σ=0
  identity does NOT select d=4 among even dimensions. What selects
  d=4 (if anything does) is the D4U02 selectivity argument, which is
  an INDEPENDENT condition not derivable from binomial inversion
  alone. The script's "complete chain" A→B→C→D→E is therefore not
  a single-track derivation; it's:
  - A,B,C: arithmetic machinery (work for all even d)
  - D,E: dimension-selection (distinct mechanism, D4U02 specific)
  The coefficients (-1,9,-16,8) follow from A-C **given d=4 as input**;
  they do not follow from A-E with d undetermined.
- **Flag 5 — Audit section correctly scores many steps.** Script's
  "CRITICAL AUDIT" at end is honest: Step A labeled SOLID (amplitude
  locality), Step B labeled SOLID with a flagged gap (Boolean-lattice
  containment lemma), Step C labeled SUPPORTED by literature, Step D
  CERTAIN (arithmetic), Step E SOLID. The audit's final line "O14
  IS PROVED" overstates — Flag 3 shows one of the substeps ("Σ=0 is
  d=4 specific") is arithmetically wrong, which means the "complete
  chain" argument in the theorem statement (Step D/E interplay) has
  a crack.
- **Verdict:** Best O14 script in the catalogue. The arithmetic pieces
  are all correct. The uniqueness-via-Möbius-inversion step is framework-
  level correct given the Boolean-lattice containment identification.
  The claim "Σ=0 selects d=4" is wrong and should be removed; the
  d=4 selection needs to come entirely from D4U02 (or an equivalent
  independent criterion). With that correction, the honest statement
  is:
  - "Given d as input, BDG coefficients are unique via Möbius inversion
    of Yeats moments" — **supported**
  - "d=4 is uniquely selected by D4U02" — **separate claim, CV-tier**
  - "BDG coefficients are unique derivations of RA from primitives" —
    requires the Boolean-lattice containment lemma + independent
    d-selection criterion (D4U02); chain is coherent but the single-
    bullet "Σ=0 → d=4" shortcut doesn't work.
  This script supports the "given-d" uniqueness claim; the "what
  selects d" part lives in D4U02 scripts.

---

## Entry 24: `o14_incidence_algebra.py`

**Status:** `unknown` (pending tag — companion / earlier-attempt
relative to Entry 23)
**Lines:** 550 — **In scripts.txt:** unknown — **Target:** O14
(incidence-algebra approach to BDG uniqueness)

- Stated purpose (docstring): attack O14 via the incidence algebra of
  a locally finite poset, treat BDG operator as `B = Σ c_k ζ^k` in
  this algebra, characterize "second-order" as `<B(const)> = O(λ^{2/d})`
  for large sprinkling density. Tries both continuum-scaling and
  purely-discrete formulations.
- **Real computational content:**
  - Standard formula `C_d(k) = Γ(d/2+1)^{k+1} / (Γ((k+1)d/2+1)·Γ(k+2))`
    tabulated for d=2..6, k=0..6. Uses scipy.special.gamma.
  - Polynomial analysis using sympy: `P_bdg = 1 - z + 9z² - 16z³ + 8z⁴`,
    computes `Q1 = P(z) - 1)/z`, shows Q1(1) = 0 (so (z-1) divides),
    factors `P(z) = 1 + z(z-1)(8z² - 8z + 1)` — **verified**.
  - Selectivity scan: parameterize R(z) = a·z² + b·z + (1-a-b)
    (with R(1)=1 enforced), scan (a,b) over a grid, compute
    `ΔS* = -log(P_acc)` at μ=1, rank configurations.
- **Flag 1 — BDG is NOT the selectivity maximum in the (a,b) scan.**
  Script output:
  ```
  BDG (a=8, b=-8, c=1): ΔS* = 0.5932
  Maximum ΔS* = 0.6414 at a=1, b=-4
  BDG rank by ΔS*: #120 out of 240
  ```
  Among the "top 15 by selectivity" configurations printed by the
  script, BDG is absent. Configurations like (a=1, b=-4, c=4) with
  coefficients [-4, 8, -5, 1] and (a=1, b=-10, c=10) with [-10, 20,
  -11, 1] ALL satisfy P(z) = 1 + z(z-1)R(z) with R(1)=1 AND have
  higher ΔS* than BDG.
- **Flag 2 — Consequence: "maximum selectivity at μ=1" does NOT
  select BDG uniquely.** The selectivity criterion (ΔS* maximized at
  μ=1) is a real algebraic constraint, and all configurations in the
  scan satisfy the factorization structure 1 + z(z-1)R(z) with R(1)=1.
  Within the resulting 2-parameter family, BDG is rank #120 of 240
  by selectivity — not extremal in any direction.
- **Flag 3 — Script is EXPLORATORY and doesn't overclaim.** Unlike
  `o14_proof.py` (Entry 23) which concludes "O14 IS PROVED," this
  script ends the selectivity scan and stops. There is no "therefore
  BDG is unique" claim. The file is honest about its partial status —
  it's setting up the algebraic framework (polynomial factorization,
  constraint space) and observing that additional constraints are
  needed beyond what it's computed.
- **Flag 4 — Polynomial factorization P(z) = 1 + z(z-1)R(z) is a
  genuine structural insight.** Verified by sympy: `P_bdg - (1 +
  z·(z-1)·(8z²-8z+1)) = 0` exactly. This factorization captures:
  (a) birth term = 1, (b) Σ c_k = 0 (from (z-1) factor), (c) vanishing
  at z=0 for the correction = trivial birth, (d) a residual R(z) that
  encodes "the physics." For d=2, the script correctly notes this
  factorization breaks down (no (z-1) factor) — confirming Σ=0 is
  a property of d≥4 at the appropriate K, orthogonal to Entry 23's
  Flag 3.
- **Flag 5 — The dimension of the constraint space is explicitly
  enumerated.** R_d has degree d/2, giving d/2+1 coefficients, with
  R(1)=1 reducing to d/2 free parameters. For d=4: 2 free parameters.
  Selectivity (μ=1 maximum) doesn't pin these uniquely. The script
  implicitly shows that **another constraint is needed** to pick out
  BDG within the 2-parameter family — but doesn't identify what that
  constraint is.
- **Verdict:** Exploratory companion to `o14_proof.py`. Establishes
  the polynomial-factorization structure cleanly (confirmed by sympy),
  enumerates the constraint space, and demonstrates that selectivity-
  at-μ=1 does NOT uniquely pick BDG within that space. Does not overclaim.
  Status suggestion: **keep as historical/scaffolding** alongside Entry
  23. Together they map what's known about O14 uniqueness: the
  arithmetic from moments works (23), the algebraic structure factors
  nicely (24), but neither alone closes "BDG is the unique choice."
  The missing constraint is likely non-redundancy (Möbius inversion
  uniqueness given the Boolean-lattice identification), which is the
  argument Entry 23 relies on — but that argument does not need the
  selectivity or polynomial-structure material in Entry 24. Entry 24
  is a partial exploration of an approach not ultimately used.

---

## Entry 25: `bdg_multicoupling.py`

**Status:** `unknown` (pending tag — narrative-output mismatch pattern)
**Lines:** 487 — **In scripts.txt:** unknown — **Target:** RASM /
Paper II (force hierarchy from BDG coefficients, depth-specific couplings,
lifetime predictions)

- Stated purpose (docstring): "Each BDG depth level has its OWN effective
  coupling. The depth levels ARE the forces." Proposes an identification
  c₁↔weak, c₂↔EM, c₃↔strong (confined), c₄↔strong (colour), with
  depth-specific Poisson rates λ_k computed from known couplings α_w,
  α_EM, α_s and particle-specific input masses.
- **Real computational content:**
  - Depth-specific rates `λ_k = α_k × (mass/Λ_k) × geometric/k!`
    for a curated list of 15 particles (hadrons, leptons, gauge bosons,
    Higgs).
  - "Stabilizing" rate `R_stab = λ₂·|c₂| + λ₄·|c₄|`; "destabilizing"
    rate `R_destab = λ₁·|c₁| + λ₃·|c₃|`.
  - Analytic lifetime estimate `τ_RA = S_init/(R_destab − R_stab) ×
    L_cycle × τ_Compton`.
- **Flag 1 — Every input α is PDG/empirical.** `alpha_s = 0.118`,
  `alpha_em = 1/137.036`, `alpha_w = 1/30`, `m_W = 80379` MeV,
  `Lambda_QCD = 200` MeV — all hardcoded PDG values at the top of the
  file. The depth-specific rates inherit empirical values for scales
  AND couplings. Per Apr 17 framing discipline, none of this is from
  DAG + BDG + LLC primitives.
- **Flag 2 — The depth↔force identification is STIPULATED, not
  derived.** Docstring prose: "depth 1 (c₁ = -1): electroweak / depth
  2 (c₂ = +9): electromagnetic / depth 3 (c₃ = -16): strong (confined)
  / depth 4 (c₄ = +8): strong (colour)". No derivation of why depth k
  corresponds to force X. Memory edit framing has c₂↔EM and c₃,c₄↔strong,
  but the "c₁↔weak" identification is specific to this script. This is
  the GS02 gauge-identification program, flagged in memory edit #6 as
  CV-tier and currently under-specified.
- **Flag 3 — Quantitative predictions fail systematically for all
  weakly-decaying particles.** Script output gives τ_pred for each
  particle; log₁₀(τ_pred / τ_obs) values:
  - Neutron: −25.6 (predicts 2×10⁻²³ s, observed 880 s)
  - Muon: −17.6
  - Charged pion: −15.3
  - Charged kaon: −14.4
  - Tau lepton: −11.9
  - Neutral pion: −5.1
  - Higgs: −1.7
  - W, Z bosons: −1.6 each
  The script's "ASSESSMENT" states "W/Z bosons: within ~1 order of
  magnitude" — this is **not true** for the printed output (both are
  1.6 OOM off, outside the claimed ~1 OOM).
- **Flag 4 — The "cross-force hierarchy" claim is also wrong for
  predictions.** Script output shows τ_pred ≈ 2×10⁻²³ s for neutron,
  pion, rho_770, etc. — ALL roughly the same number. The observed
  values span 25 orders of magnitude (880s to 4×10⁻²⁴s). Script prints
  "✓ Cross-force hierarchy: neutron >> pion >> resonances" as if this
  is a model success, but **the model does not predict the hierarchy**
  — it predicts all three particles to have similar ~10⁻²³ s lifetimes.
  The hierarchy appears only in the observed column, not the predicted
  column.
- **Flag 5 — Resonances are within 1 OOM, and this is real.** The 6
  short-lived strong-decaying particles (rho, omega, phi, Sigma_1385,
  Delta_1232, Roper_1440) all have `|log ratio| ≤ 0.9`. This is
  genuine agreement — the model does work for particles that decay
  via the "same-force" strong interaction (script's stated scenario).
  The wheels come off for cross-force (weak) decays, where the model
  treats neutron and rho as equivalent but they differ by ~26 OOM.
- **Flag 6 — The `topo_protect=True` proton bypass.** Proton gets
  `τ = ∞` by virtue of an input flag `topo_protect=True`, not by
  computation. Comment claims this is from "isospin flip allowed" for
  neutron (no flag) vs forbidden for proton (flag). This is a manual
  annotation encoding the observed stability, not a derived prediction.
- **Flag 7 — "Force unification at μ=1" narrative is arithmetic, not
  derivation.** Final section argues that at μ=1, λ_k · |c_k| are "all
  order-1" (1.0, 4.5, 2.7, 0.3) so forces "unify." The numbers are
  correct arithmetic from the factorial-suppressed Poisson rates times
  |c_k|. But "all order-1" is a loose characterization (the ratios
  span 4.5/0.3 ≈ 15), and the narrative "forces unify at Planck scale"
  is a standard SM/GUT observation re-decorated with BDG vocabulary.
  No independent prediction of the GUT scale from RA primitives.
- **Verdict:** Structural model that does one thing well (6 strong-
  resonance lifetimes to within 1 OOM using a simple S/R_net estimate)
  and several things badly (cross-force weak-decay lifetimes off by
  10–25 OOM; its own "ASSESSMENT" summary contains factually incorrect
  statements about the match quality). The "depth↔force" identification
  is stipulated rather than derived — this is the GS02 gauge program
  and is a genuinely open RA target. Under the Stage B cleanup rubric
  just discussed, this script falls in the `canonical, needs_work`
  category: the good parts (6 strong resonances) are real evidence
  for the same-force structural model, but:
  (a) empirical α and Λ inputs throughout,
  (b) the "ASSESSMENT" section overstates the agreement for W/Z and
      cross-force particles,
  (c) the cross-force hierarchy isn't predicted.
  The narrative text would need a serious rewrite if this is cited in
  Paper II. Archiving is probably premature — the strong-resonance
  result is useful — but the docstring/ASSESSMENT prose is drift-prone.

---

## Reference Note: `D4U02_analytic_proof.md`

**Not a Python script.** This is reference material — an analytic
proof document recording the April 4 result that the selectivity
ceiling of ΔS*(μ) lies at μ* > 1, combined with the certified
computation μ* = 1.019 ± 0.009. Catalogued here because it bears
directly on Stage B's O14 findings:

- **The document supplies what entries 23–24 need as the independent
  d=4-selection criterion.** Entry 23's "Σ C_i = 0 selects d=4" argument
  fails (the identity holds for all even d at K=d/2+2). Entry 24's
  "selectivity maximum at μ=1" fails to pick BDG within the R(z)
  parameter family. The D4U02 argument — that the first local maximum
  of ΔS*(μ) sits at μ* ≈ 1 due to a **number-theoretic barrier**
  (N₂ ≡ 7 mod 8 being required for K = −1, exponentially suppressed
  under Pois(1/2)) — is a **legitimate d=4-selection condition** that
  depends on the specific integers (9, −16, 8) in a way no generic
  even-d moment sequence exhibits.
- **Status claimed:** "DR" (derived). Proof structure reviewed:
  - Conditioning decomposition (Step 1): standard, correct.
  - Lower bound (Step 2): exact algebra, A ≥ 0.00342.
  - Upper bound (Step 3): modular arithmetic `9N₂ + 8N₄ − 16N₃ ≡ N₂
    (mod 8)`, correct; Poisson tail `P(N₂ ≥ 7 | Pois(1/2))` = 1.1×10⁻⁶,
    correct.
  - Conclusion ratio A/B ≈ 3410, numerical check `P(S=1) − P(S=0) =
    0.00157` matches.
- **Implication for the O14 chain (Stage B observation 19 update):**
  The honest uniqueness statement becomes:
  1. **Given d as input**: Yeats r_k(d) + Möbius inversion on Boolean
     lattice → unique BDG coefficients. Verified in Entry 23 (Steps
     A–D arithmetic). Depends on Boolean-lattice containment lemma
     (not in Lean).
  2. **d=4 selection**: via D4U02 number-theoretic barrier
     (μ* > 1 for d=4 coefficients). This document supplies the proof;
     corresponding Python script would compute μ* = 1.019 ± 0.009
     (memory edit: "D4U02 selectivity ceiling at μ ≈ 1.019").
  3. The "Σ=0 as d=4-selector" wrong-turn in Entry 23 can be dropped
     without weakening the overall argument. Σ=0 is a universal
     consequence of the moment structure at K=d/2+2; it doesn't need
     to be (nor should be claimed to be) a d=4-specific identity.
- **Action item**: when entries 23–24 are re-archived or consolidated,
  cite this document as the independent d=4-selection step so the
  chain reads:
  `(a) Boolean-lattice Möbius inversion → coefficients given d → (b)
  D4U02 modular barrier → d=4` rather than relying on a single-bullet
  hockey-stick argument.

Does not affect `Running Stage B totals` count (not a Python script).

---

## Entry 26: `rho_native.py`

**Status:** `needs_work`
**Lines:** 491 — **In scripts.txt:** unknown — **Target:** Paper II /
σ-filter programme (ρ(770) lifetime from BDG exit kernel, extended to
14 hadronic resonances + W/Z)

- Stated purpose (docstring): "No imported couplings. No estimated A_k
  values. Everything from BDG enumeration." Enumerates reachable states
  from ρ profile (2,1,0,0) under single-step depth insertions, builds
  transition kernel from counting alone, computes first-exit time from
  the identity class.
- **Real computational content:**
  - Full BFS enumeration of reachable states from (2,1,0,0) within
    confinement window L+2=5: 16 reachable states, split into in-class,
    exited, and disrupted. This enumeration part is genuinely RA-native.
  - Single-step transition analysis: depth-1 → (3,1,0,0) ΔS=-1 DRESSING,
    depth-2 → (2,2,0,0) ΔS=+9, etc. Each outcome classified from BDG
    arithmetic alone. Also RA-native.
  - μ_int fit for ρ: scan μ ∈ [0.01, 2.0], find value minimizing
    |log(τ_pred/τ_obs)|.
  - Extrapolation to 14 other particles via linear scaling `μ_int(m) =
    μ_ρ × (m/m_ρ)`.
- **Flag 1 — CRITICAL: "BEST FIT" hits the upper boundary of the scan
  range.** `mu_scan = np.linspace(0.01, 2.0, 2000)` — only scans up to
  μ=2.0. Script output: `BEST FIT: μ_int = 2.0000`. This is the
  endpoint value, not an interior optimum. At μ=2.0 the log ratio is
  still +0.42 (τ_pred 2.6× too high); a genuine best-fit search would
  find μ > 2.0 giving a smaller log ratio. The "best" is an artifact
  of truncation. This propagates to all downstream extrapolations.
- **Flag 2 — Comparison `fitted μ_int = 2.0000` vs `√(m_ρ/Λ_QCD) =
  1.9685` is not a discovery.** Script suggests the near-match is
  evidence for `μ ∝ √(m/Λ)`. But Flag 1 shows the 2.0 is the scan
  boundary, not a real fit value. The √ comparison therefore does not
  support anything; it's a near-coincidence with a boundary-hit
  artifact.
- **Flag 3 — The ω/ρ ratio is NOT reproduced.** ω(782) and ρ(770) have
  nearly identical profile (2,1,0,0) and mass (782 vs 775 MeV). Under
  linear μ scaling: μ_ω = 2.018, μ_ρ = 2.000, differing by 0.9%. Script
  predicts τ_ω/τ_ρ ≈ 1 (nearly identical lifetimes). Observed:
  τ_ω/τ_ρ = 7.7×10⁻²³ / 4.4×10⁻²⁴ = **17.5**. Off by factor of 17.
  The G-parity distinction between ω (G=−1, 3π only) and ρ (G=+1, 2π
  allowed) is not captured by this script — `pathwise_exit.py` (Entry
  28) is the attempt to fix this.
- **Flag 4 — Several particles predicted with "∞" lifetime.** φ(1020)
  and f₂(1270) show `p_exit = 0.000000, τ = ∞`. For these profiles
  (2,2,0,0), no single-step depth addition brings S ≤ 0 AND stays
  within the confinement window — so the single-step exit kernel
  gives zero exit probability. This is the "Type IV OZI" structural
  result (real feature, flagged in memory as an RA-native mechanism for
  OZI suppression), but the script produces `∞` without a fallback
  multi-step treatment. The infinity is a model limitation, not a
  prediction that these particles are stable.
- **Flag 5 — W/Z "matches" are artifacts of extrapolating μ-linear
  scaling to μ=200+.** μ_W = 4.71 × (80379/775) = 207, giving λ_k =
  207^k/k! huge. At such densities p_interact → 1 trivially, and the
  Poisson rates overwhelm any BDG arithmetic. The "match within 0.2
  OOM" for W/Z is not evidence the model captures weak decay — it
  reflects that at any sufficiently large μ, τ_steps becomes small
  and τ_pred × L × τ_Compton eventually crosses τ_obs. The scan has
  no structural meaning in this regime.
- **Flag 6 — Kendall τ = 0.545 across 12 same-force resonances.**
  15 discordant pairs out of 66 total pairs — 22.7% discordance.
  Moderate rank correlation. Script labels this as "the regime where
  the model is strongest," but τ = 0.5 is not a triumph; it means
  the model orders better than chance but with substantial error.
- **Flag 7 — Honest self-assessment at the end.** Section 7 explicitly
  asks: "Is μ_int DERIVED from BDG structure, or is it a fitted
  parameter? Currently: fitted (from τ_ρ)." This is good epistemic
  hygiene — the script acknowledges μ_int is a free parameter and
  frames the "derivation of μ from mass" as an open target, not a
  claimed result. This partially mitigates Flag 1's damage: the
  script is not claiming to have solved the resonance-lifetime problem,
  just to have sketched a kernel and identified one fitting parameter.
- **Verdict:** Genuine RA-native machinery (BFS enumeration, BDG
  arithmetic for outcome classification, exit-kernel structure) wrapped
  around a fitted parameter that hits the scan boundary. The honest
  framing in §7 redeems some of this, but the "BEST FIT = 2.0000"
  line is misleading on its face, and the ω/ρ failure is a substantive
  problem the script does not solve. Same-force resonance ordering
  (Kendall τ=0.55) is a real but modest structural result. Needs
  `needs_work` tag — specifically: extend scan range, add fallback
  for Type IV exits, document the ω/ρ failure prominently.

---

## Entry 27: `mu_int_derive.py`

**Status:** `ARCHIVED — HISTORICAL + BROKEN` (Apr 20 sub-pass v2.
SyntaxError U+2014 em-dash on line 132 prevents execution. Under patch,
all three candidate hypotheses fail on the script's own data: μ varies
25× within identical profile; universal-f hypothesis has CV=62%; S/L
candidate errors 22–920%. Narrative continues as if hypotheses held;
concludes with unsupported philosophical claim about mass. Matches the
Entry 21/22 archive pattern exactly.)
**Lines:** 467 — **In scripts.txt:** unknown — **Target:** Paper II /
σ-filter programme (test three candidate derivations of μ_int; goal:
replace fitted μ_int with a structural formula)

- Stated purpose (docstring): test three candidates for μ_int —
  (1) μ = (m/Λ_QCD)^p, (2) μ = L × (m/Λ_QCD)^q, (3) self-consistent
  renewal density (universal exit-fraction f*). Goal: eliminate the
  fitting parameter from Entry 26.
- **Flag 1 — CRITICAL: SyntaxError on line 132.** The error branch
  for particles that fail to fit uses Unicode em-dash `—` as a Python
  identifier inside an f-string:
  ```python
  print(f"{pname:<16} {Nstr:<14} {L:>3} {mass:>8} {tau_obs:>12.2e} "
        f"{—:>8} {—:>12} {lr:>8}")
  ```
  `—` is not a valid Python identifier. The script aborts at parse time
  before executing. I verified by running: `SyntaxError: invalid
  character '—' (U+2014)`. This script does not run. Entry 27 results
  below are from a patched version (replaced `{—:>8}` with `{"NOFIT":>8}`
  to get the script to execute).
- **Flag 2 — Under patch: individual μ fits differ by 25× within
  identical profile.** All three of ρ(770), ω(782), K*(892) have
  profile (2,1,0,0), L=3, similar masses. Fitted μ values:
  - ρ(770): μ_fit = 4.71
  - K*(892): μ_fit = 18.78
  - ω(782): μ_fit = **117.87**
  The ω fit is 25× higher than ρ despite nearly identical mass and
  identical profile. This directly refutes the script's proposed
  candidate 3 (μ depends only on (N, L)) on its own data. The script
  acknowledges this in §5 output ("μ range: 4.710 — 117.870 (spread:
  113.160)") but doesn't retract candidate 3; it continues to §6 as
  if the hypothesis were viable.
- **Flag 3 — Candidate 3 FAILS by script's own criterion.**
  Section 4 computes `f_exit` (universal exit fraction hypothesis):
  - mean: 0.1991 ± 0.1234
  - median: 0.2295
  - range: 0.0273 — 0.3242
  - CV: **62.0%**
  Script prints: "→ f_exit varies significantly across resonances
  (CV=62.0%)". So the universal-fraction hypothesis is NOT supported
  by the data — but the §8 summary still lists Candidate 3 as
  potentially viable ("Status: If f_exit is universal..."). The "if"
  is doing a lot of work when the data shows it isn't.
- **Flag 4 — Candidate 6 (μ = k · S/L) FAILS: errors 22% to 920%.**
  Under-patch output table:
  ```
  Particle     S/L    μ_pred   μ_fit   Error%
  ρ(770)       2.67   23.044   4.710   389.3%
  Roper(1440)  4.00   34.567   4.710   633.9%
  N(1680)      4.00   34.567   3.390   919.7%
  Λ(1520)      4.00   34.567  25.510   35.5%
  ...
  ```
  Mean error ~240%. The "universal k" is not universal. The script
  doesn't recalibrate its narrative after these errors print.
- **Flag 5 — High μ fits (100+) are degenerate, not meaningful.**
  At μ=117, Poisson rate λ_4 = μ⁵/120 = 1.9×10⁸. The BDG filter is
  so aggressive at these densities that essentially everything is
  destabilized. The "fit" at μ=117 isn't finding the RA-native density
  — it's finding the value where the scan loops hit τ_obs under
  degenerate conditions. The fitting procedure is insensitive to
  the BDG structure at these μ values.
- **Flag 6 — The §7 "mass is derived" narrative.** Script concludes
  with a philosophical argument that mass is derived from μ via
  `m = ℏ L τ_steps / (c² τ_obs)`, and that this "means E=mc² is not
  a law of nature, it is the DEFINITION of mass." This is:
  (a) not supported by the numerical results above (which show the
      μ-from-topology hypothesis fails)
  (b) a re-derivation of τ = ℏ/(Γ) = ℏ/(p_exit × rate) as if it were
      an ontological claim about mass
  (c) treats the tautology "fit μ to match τ_obs given m ⟹ m
      determined by μ given τ_obs" as if it were a discovery
  The script's actual data refutes the hypothesis its conclusion is
  built on. This is the clearest overreach pattern in the catalogue
  so far.
- **Flag 7 — Imports Λ_QCD = 200 MeV as a hardcoded constant.**
  Line 32: `Lambda_QCD = 200  # MeV`. Candidate 1 and 2 both use this
  as input. Per Apr 17 framing discipline, Λ_QCD should be derived
  from BDG + m_Planck (per memory edit, `μ_QCD = exp(√(4ΔS*)) = 4.7119`
  is derived, but Λ_QCD in MeV requires a separate dimensional anchor
  not computed in this script).
- **Verdict:** Script doesn't run as-is (SyntaxError). Under patch,
  the data refutes all three candidate hypotheses, but the script's
  narrative text presents Candidate 3 as viable and concludes with a
  philosophical claim about mass that isn't supported by its own
  numbers. Significant cleanup required: (a) fix the syntax error,
  (b) rewrite narrative sections to reflect that all three candidates
  failed, (c) retract the "mass is derived" argument until there's
  a candidate that actually fits the data. **Archive candidate** —
  this is an exploration whose conclusions the data did not support.
  Flag for the next archive sub-pass; keep catalogued so the negative
  result (all three μ-derivation hypotheses fail on same-force
  resonances) is recorded.

---

## Entry 28: `pathwise_exit.py`

**Status:** `needs_work` (v2 attempt at fixing ω/ρ ratio from Entry 26;
QFT σ-labels as mechanism — framing concern)
**Lines:** 486 — **In scripts.txt:** unknown — **Target:** Paper II /
σ-filter programme (v2 pathwise exit kernel with state-dependent σ +
daughter admissibility)

- Stated purpose (docstring): v1 gave τ_ω/τ_ρ = 1.3 (observed 17.5).
  v2 adds state-dependent Σ_k(M_j) at each step, daughter admissibility
  rules D(M → daughters), branching-volume structure.
- **Real computational content:**
  - Motif class with full σ-labels: isospin I, G-parity G, strangeness
    S, baryon B, flavor content.
  - Daughter admissibility function implementing G-parity conservation,
    baryon conservation, strangeness conservation, kinematic threshold.
  - Three exit-path types:
    - Type I direct: single-step disruption AND 2-body daughter admissible
    - Type III multi-step: single-step disruption but only 3-body
      admissible (e.g., ω → πππ); weight `p_interact × pk × f_frag²`
    - Type IV OZI: no single-step exit; BFS for multi-step exit paths
      up to length 4
  - μ_base = 4.71 (identified in comment as "calibrated from ρ"; this
    matches derived μ_QCD = exp(√(4ΔS*)) = 4.7119 per memory edit).
- **Flag 1 — v2 does NOT fix ω/ρ.** Script output:
  ```
  ρ(770)   I direct         τ_pred=7.86e-24  τ_obs=4.4e-24  log₁₀=+0.3
  ω(782)   III multi-step   τ_pred=1.23e-23  τ_obs=7.7e-23  log₁₀=-0.8
  ```
  τ_ω/τ_ρ predicted: 1.6×. Observed: 17.5×. Off by factor of 11.
  Docstring says v2 should fix this; output shows it doesn't. Script's
  "KEY IMPROVEMENTS" section says "The ω/ρ ratio **should improve**
  with proper σ at each step" — the conditional tense hedges, but the
  natural reading of "v2 adds σ to fix v1" is that the fix worked.
  It didn't.
- **Flag 2 — φ(1020) is catastrophically wrong.** Output:
  ```
  φ(1020)  IV OZI  τ_pred=1.65e-20  τ_obs=1.5e-22  log₁₀=+2.0
  ```
  Off by factor of 110. The summary line flags this: "φ off by 61.6×".
  The OZI BFS finds multi-step exits but predicts a lifetime 2 OOM
  too long. The script's "WHAT WORKS" list doesn't mention φ; it
  mentions only that "OZI suppression is structural (no single-step
  exit)" — which is a qualitative feature, not a quantitative match.
- **Flag 3 — Framing concern: QFT σ-labels used as mechanism.** The
  σ-label scheme {I, G, S, flavor, B} is directly imported from SM
  quantum numbers. The `daughter_admissible` function implements:
  G-parity conservation, baryon conservation, strangeness conservation.
  These are labeled "RA-native: LLC on σ-labels" in the docstring, but
  the content is QFT-native: G-parity is defined via isospin + charge
  conjugation (QFT operators), strangeness is a flavor label. Per Apr
  17 framing discipline: QFT terminology allowed as translation
  bridges but NEVER as mechanism. Here the SM conservation laws ARE
  the mechanism driving the exit-path structure, not a translation
  layer over something more primitive. This is exactly the pattern
  (pattern-identification table in RA_Framing_Discipline.md) that
  should trace to DAG + BDG primitives — but the paper-note table
  lists G-parity's RA-native counterpart as OPEN ("(open: structural
  reason for mass suppression in pseudoscalar meson motifs)").
  Entry 28 hasn't closed that gap; it's asserted.
- **Flag 4 — The `f_frag²` geometric-suppression factor is ad-hoc.**
  Comments in code:
  ```
  # Model: fraction of second-step disruptions that
  # produce valid 3-body exits ≈ p_frag_further
  # (those that DON'T recombine)
  # But we need ANOTHER filter: of those further
  # fragmented states, what fraction actually produces
  # admissible daughters?
  ```
  The `p_3body = f_frag * f_frag` formula is explicitly described as
  a "crude estimate" in a 40-line comment block. This is a fitting
  choice, not a derivation. The script's "WHAT'S STILL APPROXIMATE"
  list acknowledges: "f_frag is computed from Poisson rates, not from
  explicit daughter-state enumeration."
- **Flag 5 — Daughter threshold masses hardcoded in MeV.**
  ```python
  daughter_thresholds = {
      'ππ': 280, 'πππ': 420, 'KK̄': 987, 'Kπ': 634,
      'Nπ': 1078, 'Λπ': 1256,
  }
  ```
  These are sums of PDG pion/kaon/nucleon masses. Not from BDG
  structure. The kinematic threshold check is a physical requirement,
  but its numerical values are inherited, not derived.
- **Flag 6 — Same-force resonance "matches" are generous by
  definition.** Script's `0.2 < rp/ro < 5` threshold labels anything
  within factor 5 as "✓ MATCHES". Under this criterion, ρ/Δ/K*/Σ*
  "match" despite having `log₁₀` values spanning -0.4 to +0.3. The
  pattern "predicted lifetimes cluster at ~1 × τ_ρ while observed
  lifetimes span 1× to 17×" is masked by the factor-5 threshold.
- **Flag 7 — Honest "WHAT'S STILL APPROXIMATE" section.** Like Entry
  26's §7, the script concludes with explicit open-problem flagging:
  f_frag not derived, branching volume not computed, flavor
  rearrangement for φ→KK̄ not quantified. This is good epistemic
  hygiene and partially mitigates Flags 1-5: the script acknowledges
  its approximations rather than claiming victory.
- **Verdict:** More sophisticated than Entry 26 — incorporates σ-label
  admissibility and multi-step paths — but still fails on the central
  problem it was designed to solve (ω/ρ factor-17 ratio). The framing-
  discipline concern (Flag 3) is the most substantive: G-parity and
  strangeness enter as mechanism, not as derived labels. This is
  exactly the "σ-label conservation" identification flagged as OPEN
  in the RA framing discipline pattern table. The script is useful as
  machinery but should not be cited as evidence that RA derives
  same-force resonance lifetimes — it derives them *given* SM σ-labels
  as inputs. `needs_work` flag should include: (a) ω/ρ still broken,
  (b) φ off by factor 100, (c) framing-discipline gap on σ-labels.

---

## Archive Sub-Pass v2 — April 20, 2026 (continuation)

Executed after 28 scripts catalogued. Applied the same Entry 21-22
criterion ("hypothesis tested, data refuted, narrative continues as if
hypothesis holds") to the three candidates flagged after the first
sub-pass.

### Decisions:

| Entry | Script | Decision | Reason |
|---|---|---|---|
| 10 | `d2_two_phases.py` | KEEP | Self-labeled CONJECTURE with appropriate hedging; self-critiques its own magnitude claims; best epistemic self-awareness in catalogue so far. Stays `needs_work`. |
| 14 | `vwyler_proof.py` | RECLASSIFY | Arithmetic is correct and closes a real gap in Entry 12. Narrative issue (implied critical point at μ=1) is R2/R4 pattern — prose repair, not archive. Move from `needs_work pending` to `canonical, narrative_repair`. New repair item **R6** added below. |
| 27 | `mu_int_derive.py` | **ARCHIVE** as HISTORICAL + BROKEN | Exact match to Entry 21-22 pattern: SyntaxError U+2014 prevents execution; under patch, all three candidate hypotheses fail on the script's own data (μ varies 25× within identical profile; universal-f hypothesis has CV=62%; S/L candidate errors 22-920%); narrative concludes with unsupported philosophical claim about mass. |

### Archive action

Adding `mu_int_derive.py` to the archive list. The
`archive_obsolete_scripts.sh` script has been updated to include it —
use the updated version from `/mnt/user-data/outputs/`.

### R6 — new repair item for Entry 14

| # | Script | Repair needed |
|---|--------|---------------|
| R6 | `vwyler_proof.py` (Entry 14) | The "V_eff(1) = 1" result is correct and supported by MC (E[S\|μ=1] = 1.006). But the narrative implies μ=1 is a critical point; it is not. V_eff(μ) is not flat at μ=1 (V_eff(0.5)=1.25, V_eff(1)=1, V_eff(2)=35; derivative at μ=1 is +1, not 0). Reword to: "V_eff evaluates to 1 at μ=1 due to the d'Alembertian condition Σc_k = 0 (partial sum k=1..4), not because μ=1 is extremal." |

### R7 — new repair pattern flagged from Entry 26

| # | Script | Repair needed |
|---|--------|---------------|
| R7 | `rho_native.py` (Entry 26) | `mu_scan = np.linspace(0.01, 2.0, 2000)` finds "BEST FIT: μ = 2.0000" — the upper boundary. Extend scan range to confirm interior optimum; document if no interior optimum exists. Separately: Section 7 should flag ω/ρ factor-17 failure explicitly (currently only mentioned in passing that ω "comes out similar to ρ"). |

---

*Running Stage B totals: 28 scripts catalogued (5 archived in Apr 20
sub-pass + 1 archived in Apr 20 sub-pass v2 = 6 total archived).*
- *Joshua-confirmed status (cumulative through Apr 20, post-sub-pass v2):*
  - `ARCHIVED` (6 total): **Sub-pass 1 (5):** d3i_RA_RG (Entry 15,
    SUPERSEDED — duplicate of Entry 16); Yeats_BDG_MCMC (Entry 19,
    SUPERSEDED — sign error + race condition); RA_CSG (Entry 20,
    BROKEN — NameError, path-count vs BDG N_k); mobius_uniqueness
    (Entry 21, HISTORICAL — Match: False); uniqueness_compute
    (Entry 22, HISTORICAL — criterion minimized by trivial filters).
    **Sub-pass 2 (1, Apr 20):** mu_int_derive (Entry 27, HISTORICAL +
    BROKEN — SyntaxError U+2014; under patch all three candidate
    hypotheses fail; narrative continues as if they held)
  - `canonical, needs_work` (3): RASM_Verification, D1_Proof,
    BDG_Simulation
  - `canonical` (1): d3_alpha_s_proof (memory edit #6; "PROOF" framing
    flagged for repair — see R1)
  - `needs_work` (11, tagged Apr 20): assembly_mapper, born_rule_derivation,
    ra_flat_rotation_curve, bullet_cluster, casimir_benchmark,
    rindler_relative_entropy, d2_two_phases (sub-pass v2 confirmed KEEP —
    best epistemic self-awareness in catalogue), d3_alpha_s_BDG,
    qcd_running_proof, rho_native (Entry 26 — scan hits boundary + ω/ρ
    fails, see R7), pathwise_exit (Entry 28 — v2 still fails ω/ρ + φ off
    2 OOM + framing gap)
  - `canonical, narrative_repair` (3, Apr 20): d3i_complete (Entry 16,
    docstring vs output mismatch — R2); D1_BDG_MCMC_simulation (Entry 18,
    G_F label error — R5); vwyler_proof (Entry 14, sub-pass v2
    reclassification — correct arithmetic but misleading
    critical-point framing — R6)
  - `unknown` / pending tag (1): d1_BDG_string_tension (Entry 17, uses
    m_p as input)
  - `unknown` / pending tag (2): o14_proof (Entry 23, best O14
    script; arithmetic solid, "Σ=0 specific to d=4" claim false — see R3);
    o14_incidence_algebra (Entry 24, exploratory, selectivity does
    not pick BDG)
  - `unknown` / pending tag (1): bdg_multicoupling (Entry 25, strong
    resonances within 1 OOM but ASSESSMENT prose overstates — see R4)
  - *Active set after sub-pass v2: 22 canonical/needs_work/unknown
    scripts. Six archived. Seven narrative-repair items (R1–R7).
    Zero scripts in clean `canonical` status so far in the catalogue.*

*New cross-cutting observations from entries 26–28 (same-force resonance
programme):*

20. **The ω/ρ factor-17 ratio is the central unsolved problem of the
    same-force resonance programme.** Three scripts attack it: Entry 26
    fits μ to ρ and extrapolates linearly (predicts ω/ρ ≈ 1); Entry 27
    tries to derive μ from topology alone (same profile (2,1,0,0) for
    ρ/ω/K* requires μ values 4.7/117/18.8 — a 25× spread within an
    identical profile); Entry 28 adds σ-labels and multi-step paths
    (predicts ω/ρ = 1.6, still off by 11×). None of the three closes
    the ω/ρ puzzle. The observed factor of 17 comes from G-parity
    forbidding 2-pion decay for ω; RA needs an analogous structural
    mechanism, not an imported G-parity label.

21. **μ_int is functioning as a fitting parameter, not a derived
    quantity.** Entry 27 tests three derivation hypotheses (power law
    in m/Λ_QCD, L-modulated power law, self-consistent exit fraction)
    and all three fail on the same-force data. The data shows μ_fit
    varies 25× within identical BDG profiles (ρ/ω/K*), which refutes
    any derivation of μ from (N, L) alone. Paper II / RASM should
    not cite these scripts as "μ derived from topology" — the
    computations show the opposite.

22. **Framing-discipline gap: σ-labels (G-parity, strangeness) enter
    as mechanism in Entry 28.** Daughter admissibility uses full SM
    quantum number conservation (G, S, I, B). Labeled "RA-native: LLC
    on σ-labels" but the labels themselves are SM inheritance, not
    derived from DAG + BDG + LLC. This is the open item
    "Σ-label conservation blocks 2-body daughter, forces 3-body" in
    RA_Framing_Discipline.md — Entry 28 uses the QFT label as if it
    closed that gap. It doesn't.

23. **Boundary-truncated scans appear in Entry 26 (Flag 1).** This
    is a new pattern worth flagging for the repair list: a scan over
    [0.01, 2.0] finds the "best fit" at exactly 2.0, which is the
    upper endpoint. Any future script using `mu_scan = np.linspace(a,
    b, N)` must verify the returned optimum is interior; otherwise
    the "fit" is an artifact. R6 candidate for next archive/repair pass.

*New cross-cutting observations from entries 10–13:*

6. **The α_s = 1/√72 chain has three separate scripts.** d3_alpha_s_BDG.py
   prints it, d3_alpha_s_proof.py asserts BDG-coefficient identities that
   would justify it given stipulated physical identifications, and
   qcd_running_proof.py uses QCD running to match f_0. No single script
   closes the chain from BDG primitives to the f_0 match; each contributes
   a piece.

7. **"PROOF" labeling in docstrings does not match code content.**
   d3_alpha_s_proof.py asserts its docstring proof structure in comments
   and verifies only that the BDG coefficients satisfy three arithmetic
   identities. The physical identifications (photon↔c₂, quark↔c₄,
   amplitude↔√weight) that make the arithmetic predict α_s are not
   verified in code.

8. **QCD running appears alongside BDG results as quiet dependency.**
   qcd_running_proof.py uses 2-loop β-function + FLAG lattice anchor to
   obtain the numerical factor. Memory edit #6's f_0 = 0.07% match
   requires this QCD running step — it is not obtained from BDG
   combinatorics alone. The structural factor 17.32 is RA-native; the
   α_s(2m_p) multiplier is QCD-anchored.

9. **d2_two_phases.py has the best epistemic self-awareness so far.**
   Explicitly labels QCD identification as CONJECTURE, self-critiques
   the CMB ρ_A magnitude argument, and lists open hard walls. This is
   the style of epistemic hygiene the other canonical scripts should
   match.

10. **Entry 14 closes one gap from Entry 12.** `vwyler_proof.py` verifies
    V_eff(1) = 1 via the `c₁+c₂+c₃+c₄ = 0` partial-sum identity (the BDG
    d'Alembertian condition). MC cross-check: E[S|μ=1] = 1.006 over 500k
    Poisson(μ^k) samples. This verifies the "E[S_virtual]=1 at μ=1" claim
    that `d3_alpha_s_proof.py` only asserted in its docstring. The physical
    identifications (photon↔c₂, quark↔c₄, amplitude↔√weight) remain
    stipulated. The α_s = 1/√72 chain now has one arithmetic step verified
    cleanly and three physical identifications still external.

11. **V_eff(μ) is not flat.** Evaluating V_eff(μ) = c₀ + c₁μ + c₂μ² +
    c₃μ³ + c₄μ⁴ at other μ: V_eff(0.5) = 1.25, V_eff(1) = 1, V_eff(1.5)
    = 6.25, V_eff(2) = 35. μ=1 is not a critical point (dV/dμ at μ=1
    equals c₁+2c₂+3c₃+4c₄ = 1 ≠ 0). So "V_eff(1) = 1" is a point value
    arising from the partial-sum identity, not a generic property of the
    polynomial. The choice of μ=1 as "the m_Z scale" is itself a physical
    identification that would need separate motivation.

12. **Duplicate canonical scripts detected.** `d3i_RA_RG.py` and
    `d3i_complete.py` are byte-identical (same MD5). First instance of
    this pattern in the catalogue. Warrants a one-time sweep for other
    duplicates before Stage C.

13. **Docstring-vs-output drift in the α_s chain.** Three scripts
    (`d3_alpha_s_proof.py`, `d3i_RA_RG.py` / `d3i_complete.py`,
    `d1_BDG_string_tension.py`) contain docstring claims that do not
    match their own code output. `d3i_complete.py` docstring claims
    f_0 = 5.38 / 0.6% but output is 5.29 / 2.35%; the 0.6% number
    appears to be from the separately-uploaded `d1_BDG_string_tension.py`.
    The "PROOF" framing of `d3_alpha_s_proof.py` describes more than
    its three assertions establish. Pattern suggests docstrings get
    written or copy-pasted based on another script's output, then drift
    as the script evolves. Systematic issue worth flagging for Stage C.

14. **Direction-of-derivation issue is the deepest f_0 chain concern.**
    Memory edit #6 reports `f_0 = 5.416` to 0.07%. After this batch,
    the chain producing that match is:
    - Input m_p = 938.272 MeV from PDG (`d1_BDG_string_tension.py`)
    - Define Λ_RA := m_p/√c₄, by algebra matches PDG Λ_QCD to 0.08%
    - Q_eff := 2·m_p by construction
    - QCD 1-loop RGE from FLAG lattice anchor α_s(2 GeV)=0.3024 down
      to Q_eff gives α_s(Q_eff) = 0.311
    - f_0 = 17.3151 · 0.311 = 5.38 (0.58% from Planck 5.416)
    The "0.07%" may come from different inputs / different Q_eff than
    the script produces. Regardless of the exact number, the chain runs
    PDG-m_p → Λ → Q_eff → α_s → f_0, with QCD RGE integration as the
    engine. It is not a BDG-from-primitives prediction of f_0. The
    honest description: f_0 = (BDG-native 17.32 combinatorial factor)
    × (QCD-running α_s at a stipulated scale set by m_p). This should
    be reflected in any Paper III / RASM claim about f_0.

15. **c₄ = dim(SU(3)) identification needs its own derivation.**
    `d1_BDG_string_tension.py` identifies BDG coefficient c₄ = 8 with
    dim(SU(3)) = N²−1 = 8, i.e., the number of gluon transverse modes.
    This is the substantive physical identification behind m_p ∝ √c₄.
    Under Apr 17 framing discipline this requires derivation: why
    should the BDG coefficient at depth 4 equal the adjoint dimension
    of SU(3)? Numerical coincidence (both are 8) is suggestive but not
    sufficient. GS02 programme would need to supply this.

16. **m_p ↔ Λ_QCD is now three scripts running the same identity in
    three ways.** d1_BDG_string_tension.py takes m_p → Λ. Entry 18
    D1_BDG_MCMC_simulation.py takes Λ → m_p (via a tautological
    ⟨S|acc⟩→c₀=1 Monte Carlo). The d3i scripts (15/16) compute Q_IR
    from QCD running at α_s=1/3 and thus Λ_QCD ≈ Q_IR/4. The underlying
    BDG-native content is the √c₄ relation (c₄ = 8 hypothetically
    identified with dim(SU(3))); the empirical content requires one
    PDG anchor no matter which direction. Memory edit #6 treats the
    "0.08% m_p match" as a derived RA prediction; the scripts show it
    is a BDG-integer relation consistent with PDG data in either
    direction, not a prediction from primitives.

17. **Label/content errors in load-bearing scripts.**
    `D1_BDG_MCMC_simulation.py` prints "G_F/√2" when computing G_F
    (off by a factor of √2 in the label; numerical result matches PDG
    G_F to 0.3% but is not G_F/√2). `Yeats_BDG_MCMC.py` uses C_K =
    (1, 1, 9, 16, 8) without the BDG signs on k=1,3. Combined with
    earlier findings (d3i docstring mismatch, d3_alpha_s_proof "PROOF"
    framing), this is now a pattern: canonical scripts contain
    correctness-level labeling errors that survive because the
    numerical outputs happen to agree with targets. Recommend a Stage B
    sub-pass specifically checking that every printed quantity matches
    what the docstring claims is printed.

18. **Three distinct BDG N_k implementations across the catalogue,
    one of them wrong.** Entry 18 (`D1_BDG_MCMC_simulation.py`) uses
    Poisson-CSG sampling of N_k ~ Poisson(μ^k/k!) — a statistical
    shortcut that bypasses explicit causal-set construction, internally
    consistent. Entry 19 (`Yeats_BDG_MCMC.py`) sprinkles points in a
    Minkowski Alexandrov interval and correctly counts, for each
    causal pair, how many elements lie strictly between — this is the
    Benincasa-Dowker definition. Entry 20 (`RA_CSG.py`) computes
    `sum(A^k)` (path counts) and labels them N_k — this is the wrong
    quantity. Scripts 18 and 19 are consistent with the BDG framework
    modulo their other flagged issues (tautological σ claim in 18;
    coefficient sign error and race condition in 19). Script 20's
    "BDG action" output is disconnected from the framework and should
    not be cited. This creates an audit action: identify which sub-
    diamond computation underlies each claimed MCMC result in Papers
    II / III / RASM; Entry 20's output must not be among them.

19. **O14 uniqueness — four scripts, partial support, one arithmetic
    error to flag.** Four scripts in the catalogue target the
    uniqueness claim for BDG coefficients:
    - Entry 21 (`mobius_uniqueness.py`): Möbius + Γ-ratio formula,
      reports `Match: False`. **Historical.**
    - Entry 22 (`uniqueness_compute.py`): filter self-consistency
      criterion, minimized by trivial filters. **Historical.**
    - Entry 23 (`o14_proof.py`): binomial inversion of Yeats moments,
      correctly produces d=4 BDG coefficients. Includes incorrect
      claim "Σ=0 is specific to d=4" (Σ=0 holds for all even d at
      K=d/2+2 by hockey-stick). **Best O14 script; correction needed.**
    - Entry 24 (`o14_incidence_algebra.py`): polynomial factorization
      P(z) = 1 + z(z-1)R(z) with R(1)=1 for d=4 — verified. Demonstrates
      selectivity criterion does NOT uniquely select BDG within the
      R-family. **Exploratory; does not overclaim.**
    Synthesized status of O14:
    - "Given d as input, binomial inversion of Yeats r_k uniquely
      gives BDG coefficients" — **arithmetically verified in 23, 24
      (partial); depends on Boolean-lattice containment lemma which
      is not in Lean**
    - "Σ c_k = 0 uniquely selects d=4" — **false** (holds for all
      even d at the natural K)
    - "d=4 is uniquely selected by some condition" — **separate
      claim, traces to D4U02 (CV-tier computational)**
    - "BDG coefficients derive from primitives alone" — **requires
      (a) Boolean-lattice containment lemma, (b) d=4 selection via
      D4U02, (c) minimality K = d/2+2 from Yeats 2024**. Chain is
      plausible; no single script or Lean theorem closes it end-to-end.
    Stage A's finding that `RA_O14_Uniqueness.lean` lacks a uniqueness
    statement stands. Entry 23's arithmetic is the best Python-side
    support for the "given d, coefficients are unique" portion; the
    dimension-selection piece is elsewhere.
