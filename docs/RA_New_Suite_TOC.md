# Relational Actualism — New Canonical Suite
## Detailed Table of Contents for Three Papers
### April 2026 · Claude + ChatGPT collaborative architecture

---

## Architecture

| Paper | Title | Job | Target | Pages |
|-------|-------|-----|--------|-------|
| I | Relational Actualism: A Process Ontology for Physics | Define the theory | FoP / SHPMP | ~30 |
| II | From the Growing Ledger to Known Physics: Gravity, Matter, and Coupling Structure in Relational Actualism | Bridge to familiar physics | CQG / PRD | ~40 |
| III | Relational Actualism: Predictions, Departures, and Tests | Falsifiable consequences | Domain-split | ~30 |

**Parallel series:** Five Technical Audit Notes (Zenodo, cited by all three)
**Archive:** 12-paper original suite (Zenodo, derivation detail)

---

## Cross-Paper House Style

All three papers use consistent editorial devices:

### Status tags (in text and tables)
- **Lean-verified** (LV)
- **Computation-verified** (CV)
- **Derived** (DR)
- **Interpretive** (IN)
- **Open target** (OT)

### "This paper does / does not do" box
Every paper opens with an explicit scope statement.

### Audit note citations
Whenever a vulnerable or high-profile claim is made, cite the
corresponding audit note.

### End-of-section discipline
Each major section closes with a short paragraph:
- what is fixed here
- what is deferred
- what is still interpretive

---

# Paper I: Relational Actualism — A Process Ontology for Physics

**Job:** Define the theory. State the kernel, present the seven closures,
specify the implemented 4D theory. Then stop.

**What this paper does NOT do:** No predictions. No mass tables. No
cosmology. No biology. No "bosons to brains." Those belong in Papers
II and III.

**Target:** Foundations of Physics or Studies in History and Philosophy
of Modern Physics (~30 pages)

### Front-matter box

> **This paper does:** Define Kernel RA. Present the seven closures.
> Specify Implemented 4D RA. State the epistemic ladder.
>
> **This paper does not:** Derive Einstein's equations in detail.
> Derive or fully identify the Standard Model. Present coupling or
> mass numerics. Survey empirical predictions.

## Table of Contents

### 1. Introduction: What This Paper Is
- RA is a process ontology in which irreversible actualization events
  are the primitive physical reality
- This paper defines the theory; companion papers (II, III) apply it
- The five-level epistemic ladder is introduced: Kernel → Closure →
  Implementation → Interpretation → Speculation
- What this paper does NOT attempt (explicit scope statement)

### 2. The Kernel
- §2.1 Event primacy: actualization events, not objects, are primitive
- §2.2 Irreversible inscription: events write permanent causal records
- §2.3 The open future: weighted possibilities, not pre-realized fact
- §2.4 The actuality threshold: not every possibility becomes actual
- §2.5 Persistent entities: stable causal patterns, not substances
- §2.6 What the kernel rejects: block universe, observer-dependent
  collapse, state-first ontology, background spacetime

### 3. The Causal DAG
- §3.1 Formal definition: G = (V, ≺), directed acyclic graph
- §3.2 Time as the growing graph (not a background parameter)
- §3.3 Proper time as event count; relativistic time dilation
- §3.4 The arrow of time: encoded in irreversibility, not explained
  by initial conditions

### 4. The Seven Closures
- §4.1 Why closures matter: from philosophy to mathematics
  - Each kernel principle is pinned by a uniqueness or classification
    result, not by modeling choice
  - In 6/7 cases the closure is Lean-verified or computation-verified

- §4.2 Closure 1: Local causal action
  - Kernel: local neighborhoods carry combinatorial action
  - Closure: BDG is unique in 4D (O14, 47 Lean theorems)
  - The BDG integers (1, −1, 9, −16, 8) and their geometric origin
  - [Status: Lean-verified]

- §4.3 Closure 2: Local conservation
  - Kernel: conservation at every vertex
  - Closure: the Local Ledger Condition Σ_out(v) = Σ_in(v) (L01)
  - Graph Cut Theorem (L02): LLC survives severance
  - Markov Blanket (L03): subgraph shielding
  - [Status: Lean-verified]

- §4.4 Closure 3: Amplitude locality
  - Kernel: local amplitude depends only on causal past
  - Closure: BDG amplitude satisfies this (O01, zero sorry)
  - Key insight: transitivity of causal order + BDG structure
  - [Status: Lean-verified]

- §4.5 Closure 4: Causal invariance
  - Kernel: spacelike reordering does not change physics
  - Closure: unconditional causal invariance (O02)
  - Connection to Lorentz covariance at the discrete level
  - [Status: Lean-verified]

- §4.6 Closure 5: Continuum bridge
  - Kernel: dense coarse-graining yields continuum physics
  - Closure: ⟨S_BDG⟩ → (l_P²/4) R (Benincasa-Dowker 2010)
  - What this does and does not establish
  - [Status: Published theorem, CQG]

- §4.7 Closure 6: Actualization threshold
  - Kernel: nontrivial irreversibility threshold
  - Closure: S_BDG > 0 filter; P_acc = 0.548, ΔS* = 0.601 nats
  - Why naïve entropy positivity fails (elastic scattering
    counterexample)
  - The four-level hierarchy: discrete → increment → on-shell → informal
  - [Status: Computation-verified]
  - [Cites: Actualization Criterion audit note]

- §4.8 Closure 7: Persistent entities
  - Kernel: stable self-reproducing motifs
  - Closure: exactly 5 topology types in 4D (L11, 124 cases)
  - What the closure proves vs. what the SM mapping adds
  - [Status: Lean-verified]

### 5. Implemented 4D RA
- §5.1 What is now fixed (not optional):
  - BDG as local action
  - LLC as conservation law
  - Causal invariance of the possibility layer
  - Einstein-Hilbert as continuum limit
  - Concrete selectivity structure
  - Five-type topology universe
- §5.2 Why four dimensions
  - D4U02: selectivity maximum at μ* = 1.019
  - Force count: 3 non-gravitational DOFs
  - Cascade-confinement: stable matter requires d=4
  - Geometric identity: (4/3)d! = d×2^{d-1} only in d=4
- §5.3 The Engine of Becoming (five-step graph rewriting)
  - Enumerate candidates → assign amplitudes → filter by S_BDG > 0
    → select one → update graph + LLC


### 6. The Actualization Criterion in the Architecture
- §6.1 Summary of the four-level hierarchy (discrete → increment →
  on-shell → informal) — not full reproduction of audit note
- §6.2 Why naïve entropy positivity fails (elastic scattering example)
- §6.3 Why S_BDG > 0 is the fundamental criterion
- §6.4 What the continuum and perturbative formulations approximate
- [Cites: Actualization Criterion audit note]

### 7. What Paper I Fixes, What It Defers, and What It Leaves Open
- §7.1 What is fixed by Paper I (kernel, closures, implemented theory)
- §7.2 What is deferred to Paper II (bridges, interpretations)
- §7.3 What remains interpretive (explicit list)
- §7.4 What remains speculative (explicit list)
- Summary status table: claim | status (LV/CV/DR/IN/OT)

### 8. Formal Verification Summary
- 8 Lean files, ~204 theorems, 1 sorry (LQI adapter)
- Core theorem list (15-20 load-bearing results, curated)
- Where to find the proofs (GitHub, Zenodo)

### References

### Appendix A: Lean Proof Inventory
### Appendix B: The Actualization Criterion (audit note, or cite)

---

# Paper II: From the Growing Ledger to Known Physics

**Job:** Bridge from Implemented 4D RA to familiar physics. GR, particles,
gauge structure, coupling constants. Every section carries explicit
epistemic status labels.

**What this paper does NOT do:** No kernel definition (that's Paper I).
No predictions (that's Paper III). No biology/complexity.

**Target:** Classical and Quantum Gravity or Physical Review D (~40 pages)

### Front-matter box

> **This paper does:** Present the strongest bridge results from
> implemented RA to known physics. Separate formal closure, derived
> bridges, and interpretive mapping. Collect the gravity, matter,
> gauge, and coupling stories in one place.
>
> **This paper does not:** Define the kernel from scratch. Catalog the
> full prediction suite. Present cosmology/biology extrapolations.
> Claim theorem-level closure where audit notes show interpretation.

## Table of Contents

### 1. Introduction
- Paper I defined the theory; this paper applies it
- Each section explicitly labels: theorem / CV / derived / interpretive / open
- The five-level ladder is assumed from Paper I

### 2. Gravity: The GR Bridge
- **Main status: LV + Published + Derived**
- §2.1 Route 1: The Lovelock chain
  - LLC → P_act conservation → BDG locality → BD → Lovelock → EFE
  - Ingredient status table (LV/Published/Derived for each step)
  - Result: G_μν = 8πG P_act[T_μν], Λ = 0, no free parameters
- §2.2 Route 2: The RA-native BDG uniqueness chain
  - L01 + O01 + L11 → BD → EH → variation → EFE
  - Bianchi = LLC (interpretive synthesis)
- §2.3 Vacuum suppression and Λ = 0
  - Virtual processes have S_BDG ≤ 0 → P_act projects them out
  - The cosmological constant problem does not arise
- §2.4 What is Lean-backed vs. derived vs. interpretive
  - Explicit status table for every ingredient
  - [Cites: GR Bridge audit note]

### 3. Matter: Particle Topology
- **Main status: LV + CV + Interpretive**
- §3.1 The BDG Closure Theorem (L11)
  - What is proved: 5 types, 124 cases, exhaustive, Lean-verified
  - What "stable" means formally
  - The five types described by depth profile
- §3.2 Supporting results
  - Confinement lengths L_g = 3, L_q = 4 (L10, LV)
  - Chirality from acyclicity (D3, LV)
  - Baryon conservation (D3, LV)
  - W/Z marginal S = 0, photon S = 9 (LV integer identities)
  - 3 colours from N₁ = 2 (CV)
- §3.3 The Standard Model interpretation
  - Five types → quark, gluon, gauge boson, Higgs, lepton
  - Why the mapping is systematic (depth profile → interaction)
  - Why the mapping is interpretive (not yet theorem-level)
  - The exhaustiveness question (L11 vs. full BSM exclusion)
- §3.4 Where the line falls
  - Status table: LV / CV / interpretive / open
  - [Cites: Particle-Topology audit note]

### 4. Gauge Structure
- **Main status: CV + Interpretive**
- §4.1 Layer A: What is proved
  - Sign alternation (+,−,+,−,+) forced by inclusion-exclusion
  - Three non-gravitational DOFs in d=4
  - Confinement lengths and topology closure (LV)
- §4.2 Layer B: What is computation-verified
  - Sign controls ancestor count bias (exact enumeration)
  - Isotropic/anisotropic interpretation
- §4.3 Layer C: The gauge-group interpretation
  - Depth-1 → SU(2)×U(1) reading
  - Depth-3/4 → SU(3) reading
  - Depth-2 → Higgs/U(1) reading
  - "Strongly constrained interpretive mapping"
- §4.4 Layer D: What remains to be derived
  - Representation theory, β-functions, anomaly cancellation
  - Three specific paths to upgrade
  - [Cites: GS02 audit note]

### 5. Coupling Constants
- **Main status: LV + CV (inputs locked, formula form imported)**
- §5.1 The fine structure constant
  - Step 1: 137 = 144 − 7 (LV)
  - Step 2: Dyson correction → 137.036 (CV, imported formula form)
  - Step 3: P_acc × c₂ ≈ π²/2 (consequence, not input)
  - Anti-numerology argument (5 criteria)
  - [Cites: IC30 audit note]
- §5.2 The strong coupling constant
  - α_s = 1/√72 = 0.11785 (CV, 0.13% match)
  - UV fixed point from BDG RG flow
  - IR fixed point α_s = 1/3 (confinement)
- §5.3 The Koide formula
  - K = 2/3 from BDG integers (L09, LV)
  - What the identity establishes vs. what the mass interpretation adds

### 6. Mass Numerics: Derived, Constrained, and Conjectural
- **Main status: mixed (CV + conjectural)**
- §6.1 The cascade formula: m_p = m_P α⁵/2²⁸ = 941 MeV (0.3%)
- §6.2 The Higgs mass: m_H = (α⁻¹ − L_q) m_p = 125.2 GeV (0.06%)
- §6.3 The proton radius: r_p = L_q × l_C = 0.841 fm (0.03%)
- §6.4 The pion mass: m_π = (2/3)⁵ m_p = 124 MeV (11%)
- §6.5 The W boson mass: m_W = 6^{5/2} m_p = 83 GeV (3.3%, conjectured)
- §6.6 Status table: which are derived vs. conjectured
- §6.7 d=4 uniqueness: cascade exponent 2N_c−1 = cycle length d+1

### 7. What Paper II Establishes
- Summary status table for all claims
- What is theorem, what is bridge, what is interpretive, what is frontier
- What remains for Paper III

### References

### Appendix A: Ingredient Status Tables (complete)
### Appendix B: The BDG Calculator (computational details)

---

# Paper III: Relational Actualism — Predictions, Departures, and Tests

**Job:** Every falsifiable consequence, traced to its kernel axiom and
closure. What distinguishes RA from other frameworks. What would
falsify it.

**What this paper does NOT do:** No theory definition (Paper I). No
bridge derivations (Paper II). Each prediction is stated with its
dependency chain but the derivation lives in Paper II or the archive.

**Target:** Domain-splittable; some sections could become standalone
letters (~30 pages total)

### Front-matter box

> **This paper does:** Collect the framework's testable predictions.
> Separate strong bridge claims from speculative departures. Trace
> each prediction to its structural source.
>
> **This paper does not:** Define Kernel RA from scratch. Derive the
> main bridges in full detail. Present interpretive mappings as
> theorem-level results.

## Table of Contents

### 1. Introduction
- A theory that cannot be falsified is not physics
- RA makes specific, quantitative predictions across an unusually
  wide range of experimental domains
- Each prediction is traced to its kernel axiom and closure result
- What a positive or negative result would mean for the framework

### 2. Near-Term Predictions (within 5 years)

- §2.1 BMV null result
  - Depends on: Kernel D (threshold) + Closure 6 (BDG filter) +
    vacuum suppression (Paper II §2.3)
  - Prediction: strict null for gravity-mediated entanglement
  - What falsification would mean: P_act does not project vacuum
  - Experimental status: multiple groups pursuing

- §2.2 No WIMP dark matter
  - Depends on: Closure 7 (5 types) + vacuum suppression
  - Prediction: categorical, not probabilistic — no signal to neutrino floor
  - What falsification would mean: actualization without EM/strong
    interaction is possible
  - Experimental status: LZ/XENONnT ongoing, consistent so far

- §2.3 Hubble tension as baryon-density gradient
  - Depends on: Closure 5 (continuum bridge) + bandwidth partition
  - Prediction: H₀ correlates linearly with ρ_b along line of sight
  - H_local = 73.6, H_Eridanus = 76.8 km/s/Mpc (parameter-free)
  - What falsification would mean: actualization density does not
    couple to expansion rate
  - Experimental status: testable now with DESI

- §2.4 Loschmidt echo threshold
  - Depends on: Closure 6 (ΔS* = 0.601)
  - Prediction: sharp reversibility transition at t* = 0.548/g
  - What falsification would mean: actualization threshold is wrong
  - Experimental status: testable in superconducting circuits

### 3. Medium-Term Predictions (5–20 years)

- §3.1 CMB axis of evil from Kerr nucleation
  - Depends on: Closure 5 + causal severance (Paper II §2)
  - Five anomalies from one mechanism (parent SMBH spin axis)
  - Three parameters, zero remaining freedom
  - Four new predictions: alignment persistence, cosmic web correlation,
    parent mass, quadrupole-octupole phase
  - What falsification would mean: Big Bang is not a causal severance

- §3.2 Kinematic Coherence Bound
  - Depends on: Closure 7 (L12, qubit fragility)
  - Prediction: hard ceiling N_max = η × p_th for fault-tolerant arrays
  - Distinguishes RA from standard decoherence (wall vs. exponential)
  - What falsification would mean: BDG fragility score is wrong

- §3.3 Neutrino mass sum
  - Depends on: L09 (Koide) + SU(3)_gen + Majorana condition
  - Prediction: Σm_ν ≈ 59 meV (testable by CMB-S4/Euclid at ~20 meV)
  - What falsification would mean: SU(3)_gen generation structure
    needs revision

- §3.4 No proton decay / exact baryon conservation
  - Depends on: Closure 2 (LLC) + D3 (baryon conservation, LV)
  - Prediction: proton lifetime is infinite (categorical)
  - θ_QCD = 0 exactly (no axion needed)
  - What falsification would mean: LLC is wrong

### 4. Structural Predictions (long-term)

- §4.1 Causal Firewall and biosignature criteria
  - Depends on: Closure 6 (μ = 1 threshold) + five-scale unification
  - Substrate-independent criteria F1/F2 for complex life
  - SETI beyond the habitable zone
  - What falsification would mean: actualization density is not
    relevant to biological complexity

- §4.2 Gravitational wave Planck-scale corrections
  - Depends on: discrete graph structure at Planck scale
  - Prediction: dispersive corrections of order (f × l_P)²
  - Testable with third-generation detectors in extreme events

### 5. Where RA Departs from Standard Physics
- §5.1 vs. ΛCDM: Λ = 0, dark matter as topology, Hubble gradient
- §5.2 vs. Many-Worlds: actualization is real, not branching
- §5.3 vs. Copenhagen: no Heisenberg cut, no observer dependence
- §5.4 vs. GRW/CSL: threshold is ΔS* not λ_GRW; scales with
  coupling g not phenomenological rate
- §5.5 vs. String theory: no extra dimensions, no landscape,
  no supersymmetric partners

### 6. What Would Falsify RA
- §6.1 A positive BMV result (gravity from superposition)
- §6.2 A WIMP detection (actualization without standard interactions)
- §6.3 Proton decay (LLC violation)
- §6.4 No Hubble gradient with better data
- §6.5 Neutrino mass below 20 meV (SU(3)_gen failure)
- §6.6 Quantum computers scaling past the KCB without hitting a wall

### 7. Summary: The Experimental Programme
- Table: prediction | kernel dependency | closure dependency |
  timescale | current status | what falsification means

### References

---

# Relationship to Existing Corpus

## Old suite → New suite mapping

| Old Paper | Content mined for | New location |
|-----------|-------------------|--------------|
| RAQM | Kernel, actualization criterion, Unruh | Paper I §2,4.7; Paper II §2 |
| RAGC | GR bridge, vacuum suppression, cosmology | Paper II §2; Paper III §2.3,3.1 |
| RAEB | Engine of Becoming, causal invariance | Paper I §4.4,4.5,5.3 |
| RASM | BDG integers, couplings, masses, SM | Paper I §4.2; Paper II §5,6 |
| RATM | Topology, gauge groups, generations | Paper II §3,4 |
| RACL | GR uniqueness, field equations | Paper II §2.1,2.2 |
| RAQI | Kinematic Coherence Bound | Paper III §3.2 |
| RADM | Dark matter, WIMP prohibition | Paper III §2.2,5.1 |
| RAHC | Complexity hierarchy | Paper III §4.1 |
| RACI | Causal Firewall, origin of life | Paper III §4.1 |
| RACF | Biosignature criteria | Paper III §4.1 |
| Foundation | Overview (superseded by Paper I) | — |

## Audit note citations

| Audit Note | Cited in |
|------------|----------|
| Actualization Criterion | Paper I §4.7, Paper II §2.3 |
| GR Bridge | Paper II §2.4 |
| Particle-Topology | Paper II §3.4 |
| GS02 Gauge | Paper II §4.4 |
| IC30 Fine Structure | Paper II §5.1 |

---

# Writing Order

**Do not draft in numerical order only. Draft in order of maximum stability.**

1. **Audit notes first.** Finalize and post to Zenodo so they can be cited.

2. **Paper I front matter + section briefs.** Lock the architecture before
   content starts sprawling. Write the "This paper does / does not do" box,
   section headings, and one-paragraph briefs for each section.

3. **Paper I full draft.** This is the foundation. Nothing else makes sense
   without it. Can be submitted independently.

4. **Paper II §2 (GR bridge).** This is the strongest bridge result and
   stabilizes the rest of Paper II.

5. **Paper II §§3–6 (matter/gauge/couplings).** Build outward from the
   gravity bridge.

6. **Paper III.** The most journal-flexible. Sections can be extracted as
   standalone letters if needed.

7. **Polish the suite as a set.** Cross-references, consistent notation,
   house style enforcement.

---

*Table of contents designed April 10, 2026.*
*Claude (Opus 4.6) + ChatGPT (GPT-4o) collaborative architecture.*
