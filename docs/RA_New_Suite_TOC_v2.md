# RA Three-Paper Canonical Suite — Table of Contents v2
## Revised April 11, 2026
## Incorporating Motif Renewal, Selection Rules, and σ-Filter Hierarchy

---

## Paper I: Relational Actualism — A Process Ontology for Physics
**Target:** Foundations of Physics / SHPMP / BJPS (~30pp)
**Scope:** Kernel axioms → closures → implemented 4D RA. Stops before bridges.

### Front matter
- "Does / Does not" box
- Abstract (~250 words)

### §1 Introduction
- The self-writing universe: opening vision
- What standard physics smuggles in (background time, external measurement)
- What RA does differently (happening is primitive)
- The epistemic ladder: Kernel → Closure → Implementation → Interpretation

### §2 The Kernel
- Five axioms stated as descriptions of what the universe does:
  A. Event primacy (things happen)
  B. Irreversible inscription (what happens stays happened)
  C. Open future (what hasn't happened is weighted possibility)
  D. Nontrivial threshold (not everything that could happen does)
  E. Stable motifs (what persists is what keeps happening the same way)
- What the kernel rejects (block universe, hidden variables, many worlds)

### §3 The Causal DAG
- Directed acyclic graph as the natural mathematical structure
- Acyclicity = irreversibility (Axiom B made formal)
- Time as the growing graph
- Proper time as actualization count along a worldline

### §4 The Seven Closures
- Each kernel axiom paired with a uniqueness closure:
  1. Local combinatorial action → BDG unique (O14, LV)
  2. Conservation at vertices → LLC (L01, LV)
  3. Amplitude depends on causal past → O01 (LV)
  4. Spacelike ordering irrelevant → O02 (LV)
  5. Dense coarse-graining → continuum → Benincasa-Dowker → EH (published)
  6. Nontrivial threshold → S_BDG > 0, P_acc = 0.548 (CV)
  7. Stable patterns define matter → 5 topology types (L11, LV)
- Status: 6/7 are LV or CV. One (BD→EH) is published peer-reviewed.

### §5 Implemented 4D RA
- The BDG integers (1, −1, 9, −16, 8) and why d=4
- The closed loop: growth → proposal → filter → inscription → growth
- The motif state M = (T, N, C, σ) [NEW: introduced here per ChatGPT]
  - T: topology class
  - N: BDG depth profile
  - C: confinement/reset memory
  - σ: internal discrete sector labels
- Why σ is not optional: it determines persistence and decay structure
- The intrinsic dimensionless character of the theory
- The Engine of Becoming (5-step algorithm)

### §6 Formal Verification
- Lean 4 / Mathlib: 204+ theorems, 1 sorry
- What is proved: LLC, graph cut, amplitude locality, causal invariance,
  Koide, confinement lengths, BDG closure, α_EM = 137
- What proofs establish vs what they don't

### §7 Relationship to Existing Frameworks
- Causal set theory (Sorkin, Dowker): shared ancestry, RA-specific action
- Process philosophy (Whitehead): shared ontology, RA adds mathematical structure
- Other QG approaches: LQG, string theory, causet — comparison table

### §8 What Paper I Does Not Claim
- No bridges to known physics (Paper II)
- No predictions (Paper III)
- No claim that the universe IS a BDG causal set — only that BDG is
  the unique implementation of the kernel in d=4

### §9 Conclusion
- "Here is a self-referential growth process whose internal structure,
  when approximated at different scales, looks like quantum mechanics,
  general relativity, the Standard Model, and the arrow of time —
  all without external inputs, external clocks, or external laws."

---

## Paper II: From the Growing Ledger to Known Physics
**Target:** CQG / PRD (~40pp)
**Scope:** All bridges from RA to known physics. Gravity, particles,
forces, couplings, masses, lifetimes, selection rules.

### Front matter
- "Does / Does not" box
- Abstract (~300 words)

### §1 Introduction
- Paper I established the kernel and its closures
- This paper bridges from the growing DAG to the physics we observe
- The bridge hierarchy: GR → particles → forces → couplings → masses → lifetimes

### §2 Gravity Bridge
- LLC → Bianchi (flat/weak-field: DR; curved: dissolved via O10)
- BDG uniqueness → Einstein-Hilbert (Benincasa-Dowker 2010)
- G_μν = 8πG P_act[T_μν], Λ = 0 structurally
- Vacuum suppression: off-shell → no metric sourcing
- Status tags throughout [LV/CV/DR/AR]

### §3 Stable Topology and the Finite Matter Universe
- L11: 5 topology types, 124 extensions exhaust SM (LV)
- The topology classes: quarks, gluons, gauge bosons, Higgs, leptons
- BDG closure as an exhaustiveness theorem
- What this proves vs what it maps (audit note: Particle-Topology)

### §4 From Topology Classes to Particle Classes
- SM identification as systematic interpretive mapping
- Charge quantization from N₂ winding numbers
- Baryon conservation from LLC on topological winding (D3, LV)
- Three generations from SU(3)_gen
- [NEW] Identity requires more than topology type alone:
  persistence and decay require the full (N, C, σ) structure
  → developed in §6

### §5 Force Differentiation and Coupling Structure
- Force hierarchy from factorial suppression: W_k = (μ^k/k!) × |c_k|
- All forces order-1 at μ=1 (unification)
- Differentiation at sub-Planckian density
- GS02: gauge groups from BDG sign mechanism (CV)
- α_EM = 1/137 (LV), α_s = 1/√72 (CV)
- IC30: integer 137 is derived; dressed 137.036 uses imported formula form
- [NEW] Forces are best understood not as primitive sectors but as
  emergent depth-channel statistics → developed in §6

### §6 Motif Renewal, Selection Rules, and Particle Lifetimes
[MAJOR NEW SECTION — center of gravity of Paper II]

#### §6.1 Particles as self-reproducing motifs
- M = (T, N, C, σ): full motif state definition
- Identity classes [M]_P: equivalence classes defining "same particle"
- Renewal, dressing, excitation, conversion, disruption taxonomy
- Confinement/reset memory: L_g = 3, L_q = 4 (LV)

#### §6.2 The factorization: Σ_k × A_k × G_k × B_k
- Σ_k(M): σ-filtered channel accessibility (selection rules)
- A_k(M): structural accessibility from topology and memory
- G_k(μ): geometric availability = μ^k/k! × |c_k|
- B_k(M→M'): branching rule (what the insertion does)
- This factorization replaces imported coupling constants

#### §6.3 Lifetime as first exit from identity class
- Step-count lifetime (dimensionless, primary)
- Laboratory lifetime = steps × L × τ_Compton (late translation)
- Energy = actualization rate (E = mc² as definition, not law)

#### §6.4 Same-force resonance results (CV)
- W boson: pred 2.5×10⁻²⁵, obs 3.0×10⁻²⁵ (log₁₀ = −0.1)
- Z boson: pred 1.9×10⁻²⁵, obs 2.6×10⁻²⁵ (log₁₀ = −0.1)
- Δ(1232): log₁₀ = +0.1
- N(1520), N(1680): log₁₀ ≈ 0.0
- ρ(770): calibration point
- Kendall τ = 0.545 for same-force family

#### §6.5 Selection rules as topology-space accessibility
- The four exit types:
  I   Direct: single-step disruption → direct fragmentation
  II  Rearrangement-limited: disruption + flavor rearrangement
  III Multi-step: σ blocks direct path, forces longer route
  IV  OZI/topology-protected: no single-step exit at all
- Hierarchy I < II < III ≤ IV matches observed lifetime ordering
- Daughter admissibility from σ-conservation
  (G-parity, baryon number, strangeness, kinematic threshold)

#### §6.6 The ρ/ω/φ hierarchy
- ρ(770): Type I, ππ allowed, τ ~ 10⁻²⁴ s
- ω(782): Type III, ππ forbidden by G, πππ via multi-step, τ ~ 10⁻²² s
- φ(1020): Type IV, no single-step exit (BDG arithmetic), τ ~ 10⁻²² s
- OZI suppression as a THEOREM of the (2,2,0,0) profile

#### §6.7 Pathwise exit kernel
- P_exit(M|μ) = Σ_γ Π_j Σ_kj × A_kj × G_kj × B_kj
- Exit probability as sum over constrained paths through topology space
- Branching volume as RA-native analogue of phase space
- The ω gap (~11×) as the branching volume ratio: number of valid
  3-body vs 2-body fragmentation configurations

#### §6.8 Three tiers of stability
- Topologically protected (τ = ∞): proton, electron, photon (D3, LV)
- Same-force decay (~10⁻²⁵ to 10⁻²³ s): W, Z, Δ, ρ (CV, factor ~2)
- Cross-force decay (~10⁻¹⁷ to 10³ s): ordering correct, magnitude open

#### §6.9 Open targets
- Derive Σ_k from BDG topology + LLC
- Compute branching volume from BDG fragmentation combinatorics
- Cross-force quantitative lifetimes (neutron, muon, pion)
- Phase space as topology-space fragmentation volume
- Mass as derived from internal graph density

### §7 Mass Predictions
- Proton mass: m_p = m_P α_EM⁵/2²⁸ = 941 MeV (0.3%)
- Higgs mass: m_H = (α⁻¹ − L_q) m_p = 125.2 GeV (0.06%)
- Neutrino mass sum: Σmν ≈ 59 meV
- Roper gap: 290 MeV from two-pion loop
- f₀ = 5.42 baryon-to-dark ratio (Planck: 5.416)

### §8 What Paper II Establishes
- GR from LLC + BDG uniqueness (no Lovelock import)
- SM from 5 topology types (exhaustive, LV)
- Forces from depth-channel statistics (not primitive sectors)
- Selection rules from topology-space accessibility (new physics)
- Particle lifetimes from motif renewal (CV for same-force)
- Mass predictions with 0.06%–0.3% accuracy
- All from BDG integers + causal graph + discrete dynamics

---

## Paper III: Predictions, Departures, and Tests
**Target:** PRD / JCAP (~30pp)
**Scope:** All falsifiable consequences, with dependency chains
and falsification conditions.

### §1 Introduction
- Papers I and II established the framework and its bridges
- This paper presents the testable consequences
- Each prediction with: statement, dependency chain, falsification criterion

### §2 Near-Term Predictions (< 5 years)
- BMV null result (gravity-mediated entanglement)
- WIMP prohibition (no signal below neutrino floor)
- Hubble gradient: H₀ correlates with ρ_b along line of sight
- CMB axis of evil from Kerr nucleation
- Neutrino mass sum Σmν ≈ 59 meV (CMB-S4)

### §3 Medium-Term Predictions (5–20 years)
- Kinematic Coherence Bound: N_max = η × p_th
- Spin-bath collapse timescale: t* = 0.274/g
- Gravitational wave Planck-scale corrections

### §4 Long-Term Predictions
- SETI biosignature criteria (Causal Firewall F1, F2)
- Cabibbo angle |V_us| = sin(2/9)

### §5 Where RA Departs from Standard Physics
- No dark matter particles (actualization-density topology instead)
- No cosmological constant (Λ = 0 structurally)
- No Boltzmann Brains (structurally impossible + heat death prohibited)
- No proton decay (exact baryon conservation from LLC winding)
- No heat death (causal severance fragments graph before equilibrium)
- Selection rules from topology, not group theory

### §6 Falsification Conditions
- If BMV positive: RA's gravity treatment is wrong
- If WIMP detected: actualization-density dark matter is wrong
- If H₀ uncorrelated with ρ_b: Hubble mechanism is wrong
- If Σmν < 40 meV: SU(3)_gen generation structure needs revision
- If proton decays: LLC winding conservation is wrong
- Each condition with specific experimental reference

### §7 What Paper III Does Not Claim
- No claim of certainty — these are falsifiable predictions
- No claim of completeness — the research programme continues
- RA asks for serious investigation, not acceptance

---

## Cross-Paper House Style

### Status tags (mandatory on every claim)
- [LV] Lean-verified
- [CV] Computation-verified
- [DR] Derived (all steps explicit)
- [AR] Argued (physically motivated)
- [Structural] Framework-level (ordering/mechanism, not magnitude)

### Front-matter "Does / Does Not" box (every paper)
### Audit notes cited in bibliography
### Companion scripts referenced for reproducibility

---

## Old Suite → New Suite Mapping

| Old paper(s) | New location |
|---|---|
| RAQM | Paper I §2-5 + Paper III §2 |
| RAGC | Paper II §2 + Paper III §2-3 |
| RAEB | Paper I §5 + Paper II §2 |
| RASM | Paper II §3-5 |
| RATM | Paper II §3-4 |
| RACL | Paper II §2 |
| RAQI | Paper III §3 |
| RADM | Paper II §2 + Paper III §2 |
| RAHC | Paper III §5 (reframed around σ-filter hierarchy) |
| RACI | Paper III §4-5 |
| RACF | Paper III §4-5 |
| Foundation | Distributed across all three papers |
| Motif Renewal | Paper II §6 (NEW, major section) |
| Force Differentiation | Paper II §5-6 (NEW) |
| Self-Writing Universe | Paper I §1, §9 (philosophical frame) |
| Selection Rules | Paper II §6.5-6.7 (NEW, core result) |

---

*TOC v2 revised April 11, 2026.*
*Incorporates ChatGPT's architectural recommendations and the
motif renewal / selection rules discoveries of April 10-11.*
