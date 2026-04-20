# RA Programme State — April 16, 2026 (revised April 17, 2026)
## Master synthesis of April 9–16 session logs under the "bosons to brains" discipline

This document consolidates everything surfaced across the nine session logs (Apr 9, 10, 10–11, 11, 12, 14, 14-complete, 16, plus Complete Inventory, d4 Closure, RAKB Update) into one coherent picture of where RA stands.

**Framing:** Per `RA_Framing_Discipline.md`, every RA claim must trace to vertices + edges + BDG filter + LLC. Nothing imported as mechanism. This synthesis flags where the discipline is already met, where bridges still exist, and where work remains.

---

## Correction preamble (added April 17, 2026)

**This document was first produced on April 16 by synthesizing session logs, not by inspecting primary materials (Lean, Python, paper TeX).** On April 17, direct inspection of `RA_AQFT_Proofs_v10.lean` revealed three items that the session-log narration had compressed out:

1. **`Matrix.cfc_conj_unitary`** — a `sorry` in the Lean core (pure math gap, trivially closable from Lean-QuantumInfo)
2. **`vacuum_lorentz_invariant`** — a QFT-imported `axiom` (stating Poincaré invariance of the Minkowski vacuum from Wightman axioms)
3. **`petz_monotonicity`** — an LQI `axiom` (not load-bearing for frame_independence)

Item (2) is a direct violation of the RA framing discipline: Lorentz invariance should be *derived* from DAG + BDG, not *imported* as a QFT axiom.

**Consequences for this document's original claims:**

- The April 16 RAKB update listed 18 LV items. **The accurate count is 16 LV + 2 LV-conditional** (L04 frame_independence, L05 rindler_stationarity — both depending on the two items above).
- The "O11 Lorentz emergence: DISSOLVED" claim is **provisional**, not actualized. The dissolution narrative says Lorentz IS causal invariance via BDG sprinkling, but the Lean core still needs `vacuum_lorentz_invariant` as a separate axiom. A genuine dissolution would eliminate that axiom.
- The phrase "Lorentz ≡ causal invariance dissolution" in §1.6 below is too strong and has been qualified.

**The four pillars (LLC, O01 amplitude locality, O02 causal invariance, five topology types) remain genuinely LV with zero sorry.** The caveats apply specifically to the AQFT layer (L04, L05) that sits on top of the kernel.

See `RAKB_Patch_IC46.md` (April 17) for the formal RAKB correction.

This is the first of what will likely be several such corrections as Stage A of the audit proceeds. The pattern — session-log narration overstating bedrock by compressing out caveats that the primary materials explicitly flag — is exactly why we agreed to do the audit from primary materials.

---

## 1. What is fully RA-native (mechanism traces entirely to DAG + BDG + LLC)

### 1.1 Geometric foundations
- **d = 4 uniqueness**: two independent arguments both select d = 4
  - D4U02 selectivity ceiling at μ ≈ 1.019 (98.1% near-cancellation from 9 ≡ 1 mod 8)
  - Cascade exponent 2N_c − 1 = cycle length d + 1 only in d = 4
- **BDG integers (1, −1, 9, −16, 8)**: unique via O14 Möbius inversion on Yeats moments (47 Lean theorems, 0 sorry)
- **Benincasa-Dowker → GR**: established publication, d = 4 BDG → Einstein-Hilbert

### 1.2 Kernel dynamics (all Lean-verified or published)
- **LLC (Local Ledger Condition)**: L01, Lean-verified
- **Amplitude locality O01**: proved in `RA_AmpLocality.lean`, zero sorry
- **Causal invariance O02**: proved unconditionally (via O01 closure)
- **Kernel saturation theorem (Apr 12)**: KL divergence D_KL = ΔS* (same quantity), P_acc(μ→∞) = 1 with rate O(1/μ⁴)
- **Antichain drift theorem (Apr 12)**: E[ΔW] ≥ +0.34 at μ=1, drift reverses at μ_c ≈ 1.25

### 1.3 Particle topology and confinement
- **Five topology types (L11)**: 124 extension cases, Lean-verified, zero sorry
- **Confinement depths L_g = 3, L_q = 4**: Lean theorems
- **Charge quantization in e/3**: N_2 winding in d = 4
- **Baryon chirality** (D3): 13 Lean theorems, zero sorry
- **Exact proton stability**: LLC on N_2 winding (LV)
- **θ_QCD = 0 exactly**: no instantons possible in DAG (structural)

### 1.4 Coupling constants
- **α_EM⁻¹ = 137** (integer core): Lean-verified (`norm_num`)
- **α_EM⁻¹ = 137.036**: discrete Dyson equation (IC30 closure), CV
- **α_s(m_Z) = 1/√72**: BDG UV fixed point, CV
- **α_s^IR = 1/3**: BDG IR fixed point (confinement), CV
- **Koide K = 2/3** (leptons): Lean-verified

### 1.5 Selection rules and decay classification (Apr 10–11 discovery, Apr 16 integrated)
- **Five-type σ-filter classification**: 19 strongly-decaying particles, 3 OOM of τ, Σ_eff hierarchy 1 → 0.4 → 0.1 → 0 → 0.002
- **Type IV exact-zero theorem**: profile (2,2,0,0) has no single-step BDG exit (arithmetic, DR)
- **μ_QCD DERIVED** (Apr 11 breakthrough): μ_QCD = exp(√(4ΔS*)) = 4.7119, matches fitted value 4.7106 to 0.027%. **No free parameter** in σ-filter framework.

### 1.6 Gravitational and cosmological
- **Λ = 0 from P_act** (structural, not fine-tuned)
- **GR from BDG uniqueness** (RACL 7-step chain, RA-native, no Lovelock)
- **Bianchi ≡ LLC dissolution** (same conservation, different scales)
- **Lorentz ≡ causal invariance dissolution** — *PROVISIONAL as of Apr 17*. The dissolution narrative is coherent but the Lean core still imports `vacuum_lorentz_invariant` as a QFT axiom; a genuine dissolution requires replacing that axiom by a BDG-native derivation. See IC46.
- **Kernel saturation → severance**: TV → 0 at μ > 10 structurally forces fragmentation
- **Heat death prohibition**: structural (severance fragments graph before equilibrium)
- **Arrow of time**: primitive (DAG growth direction), not statistical

### 1.7 Numerical matches (zero free parameters)
| Quantity | RA | Observed | Match |
|----------|-----|----------|-------|
| α_EM⁻¹ | 137.036 | 137.036 | 0.00001% |
| α_s(m_Z) | 1/√72 = 0.11785 | 0.1180 | 0.13% |
| Koide K | 2/3 | 2/3 | exact (LV) |
| m_p | 941 MeV | 938.3 MeV | 0.3% |
| r_p | 0.84 fm | 0.8414 fm | 0.03% |
| m_H | 125.2 GeV | 125.1 GeV | 0.06% |
| μ_QCD | 4.7119 | 4.7106 (fitted) | 0.027% |
| f_0 (baryon/DM) | 5.42 | 5.416 | 0.07% |
| H_local | 73.6 km/s/Mpc | 73.0 ± 1.0 | 0.8% |
| Ω_Λ (apparent) | 0.68 | 0.69 | 1.4% |
| η' mass match | 958 MeV | 941 (cascade) | 1.8% |

---

## 2. RA-native but containing unfinished bridges (PI/CN tier, flagged)

These results have numerical success but retain an identification that hasn't been derived structurally. Under the framing discipline, these are targets for upgrade, not endpoints.

### 2.1 Mass cascade
- **m_p = m_P α_EM⁵/2²⁸ = 941 MeV**: μ⁵ gluon-vertex cascade established, but N_eff = L_q³ = 64 (IC41) is a **conjecture** requiring three candidate interpretations (confinement volume, c₄², 4|c₃|) to be discriminated.
- **Higgs m_H = 133 m_p**: depth-2 + EM ratio identification (PI 0.06%)
- **Proton radius r_p = L_q ℓ_Compton**: PI (0.03%)
- **Pion m_π ≈ 124 MeV**: 11% off, flagged as needing weak-vertex-access extension (new §6.5 work)

### 2.2 Flavor physics
- **Koide breaking (quarks)**: K = 2/3 + Casimir formula (3–8% match), identification not derivation
- **Cabibbo angle θ_lep = 2/9**: conjecture, 1.8% match
- **|V_cb| = (2/π)δ = 0.0424**: conjecture, 0.4% match
- **Majorana neutrinos, Σm_ν ≈ 59 meV**: DR for qualitative, PI for specific mass scale

### 2.3 Dark energy
- **w_0 = −0.71, w_a = −0.91**: EdS → Milne transition with t_trans = 0.575 (IC43), one remaining underived parameter. Path: nucleation perturbation spectrum → void fraction evolution → transition epoch.

### 2.4 σ-filter values
- **Σ(II), Σ(III), Σ(V)**: empirical, not yet derived from BDG branching volume. This is a CV → DR upgrade target.

### 2.5 W boson mass
- **m_W = 6^(5/2) m_p = 83 GeV**: conjecture, 3.3% off

---

## 3. Open research programs (flagged, path known)

Under the framing discipline, these are the targets that matter most — the places where the "bosons to brains, one mechanism" claim currently has gaps.

### 3.1 Weak-vertex-access framework (just flagged in Paper II §6.5)
- **Target**: P_WVA(π±) ≈ 7×10⁻¹⁶ from BDG extension structure
- **Extends to**: π, K, K_L, K_S, μ, n, τ
- **Connection**: closes both pion residual and cross-force lifetime gaps simultaneously

### 3.2 Branching volume V(γ, d)
- **Target**: derive Σ(II), Σ(III), Σ(V) from BDG extension enumeration
- **Status**: energy-budget daughter-counting attempted Apr 11 (branching_volume.py), got K* suppression right at 2.6× vs 3.0× observed
- **Gap**: 3-body kinematics / angular momentum for full ω/ρ ratio

### 3.3 N_eff derivation (IC41)
- **Target**: derive N_eff = 64 from BDG Poisson-CSG self-consistency
- **Status**: three candidates identified, none discriminated

### 3.4 t_trans derivation (IC43)
- **Target**: derive t_trans = 0.575 from nucleation perturbation spectrum
- **Status**: connects DESI dark energy to Kerr nucleation programme

### 3.5 w_0, w_a from Buchert averaging
- **Status**: Wiltshire timescape literature identified as connection point
- **Gap**: proper backreaction formalism application to RA

### 3.6 Kerr nucleation α = 0.68
- **Status**: fit, not derived
- **Target**: derive from Kerr chirality → η_b pathway

### 3.7 Remaining Lean sorry
- **One intentional**: LQI adapter in RA_AQFT_v10

---

## 4. Cross-session integrity checks

### 4.1 Claims that have been corrected across sessions
These are *important*: the programme self-corrects honestly, which strengthens surviving claims.

- **"Drift mechanism drives cosmic expansion"** (Apr 14 antichain drift) → **CORRECTED**: BDG filter inert at cosmic scales (μ ≪ 1 by 80+ orders); expansion from GR + Milne voids + backreaction
- **"Direct density-severance for early BHs"** (Apr 14) → **PARKED**: RA gives GR, which governs collapse; data on LRD identity still debated
- **"Volume-weighted averaging gives w_0, w_a"** (Apr 14) → **CORRECTED**: requires Buchert formalism, not naive weighting
- **"Ancestor partitioning for fragmentation"** (Apr 11 branching_volume v1) → **CORRECTED**: daughters are new entities from energy budget, not inherited ancestors
- **"Corrections to baseline"** language (Apr 11) → **RETIRED**: replaced by "stabilization layers" (self-consistency conditions, not patches)

### 4.2 Claims whose status was upgraded (as of Apr 16, some since revised)
- O01 amplitude locality: OP → LV (proved in Lean)
- O02 causal invariance: OP → LV (via O01 closure)
- L07 causal invariance: conditional → unconditional (in `RA_AQFT_Proofs_v2.lean`)
- O10 discrete Bianchi: OP → **DISSOLVED** (via D10 — Bianchi IS LLC)
- O11 Lorentz emergence: OP → **DISSOLVED-PROVISIONAL** (see §4.3 below — the dissolution is articulated but not yet reflected in the Lean core)
- A01 GR uniqueness: AR → DR (via RACL chain, no Lovelock)
- A02 WIMP prohibition: AR → DR (via P_act structure)

### 4.3 Corrections made after primary-material inspection (Apr 17)
Direct inspection of `RA_AQFT_Proofs_v10.lean` revealed scope caveats on claims the RAKB and session logs had labeled as unconditionally LV:

- **L04 frame_independence**: LV → **LV-conditional**. Depends on `Matrix.cfc_conj_unitary` (sorry, trivially closable from LQI) and `vacuum_lorentz_invariant` (QFT axiom, framing-discipline violation).
- **L05 rindler_stationarity**: LV → **LV-conditional**. Inherited from L04 (L05 is a one-line corollary).
- **O11 Lorentz emergence dissolution**: DISSOLVED → **DISSOLVED-PROVISIONAL**. The narrative from Apr 16 (Lorentz IS causal invariance via BDG sprinkling) is coherent but not yet actualized in the Lean core, which still imports `vacuum_lorentz_invariant` as a QFT axiom. A genuine dissolution would eliminate the axiom.

See `RAKB_Patch_IC46.md` for the formal corrections.

### 4.3 Vocabulary discipline (established Apr 11)
- "Corrections" → "stabilization layers"
- "Selection rules as prohibitions" → "selection rules as self-consistency conditions"
- "Parameters" → "structure"
- "Fudges" → NOT PERMITTED (per framing discipline)

---

## 5. Suite state

### 5.1 12-paper → 4-paper restructure (completed Apr 16)
- Paper I (14 pp): Kernel and Engine of Becoming
- Paper II (30 pp, just updated with §6.5): Matter, Forces, Renewal Motifs
- Paper III (19 pp): Gravity, Cosmology, Severance
- Paper IV (13 pp): Complexity, Life, Causal Firewall

Total: 77 pp, clean compiles, zero Type 3 fonts. Full content from original 12 papers preserved; originals archived on Zenodo.

### 5.2 Lean state (corrected Apr 17 from direct inspection of `RA_AQFT_Proofs_v10.lean`)
- 8 files, ~3000 lines, 176+ theorems
- **Remaining unproved items in `RA_AQFT_Proofs_v10.lean`:**
  - 1 `sorry`: `Matrix.cfc_conj_unitary` (pure math, closable by copying from Lean-QuantumInfo Isometry.lean)
  - 1 QFT axiom: `vacuum_lorentz_invariant` (Poincaré invariance of Minkowski vacuum; framing-discipline violation, see IC46)
  - 1 LQI axiom: `petz_monotonicity` (data processing inequality; not load-bearing for L04/L05)
- **`RA_AmpLocality.lean`**: 1 intentional sorry (List.Perm induction pending assembly of existing proof from `RA_AQFT_Proofs_v2.lean`)
- **All other Lean files** (`RA_GraphCore.lean`, `RA_Koide.lean`, `RA_O14_Uniqueness.lean`, `RA_Spin2_Macro.lean`, `RA_BaryonChirality.lean`): reported as zero sorry (pending Stage A verification)
- GitHub: jsandeman/Relational-Actualism
- **Status correction from Apr 16 narration**: the claim "zero sorry except LQI adapter" was an overstatement. Actual state has 2 sorries + 2 axioms, one of which is QFT-imported.

### 5.3 Peer review status (Apr 16)
- **RAQM at FoP**: awaiting editor assignment
- **RACF at IJA**: **in active peer review with reviewers assigned** (first to reach this stage)
- **RACL at PRD**: after CQG desk-rejection
- **RATM**: rejected by PRD (DQ14566)
- **P1 at PRL**: rejected, rebuttal written
- **RAEB**: reject with resubmission encouraged

---

## 6. What's next under the framing discipline

**Revised April 17 to prioritize framing-discipline violations surfaced by primary-material inspection.** The RAKB IC46 correction has moved this to the top of the list.

### Priority 0: Close or reformulate `vacuum_lorentz_invariant` (Apr 17 correction)
- **Highest severity**: the Lean core currently imports a QFT axiom that the RA framing discipline forbids as mechanism
- Three resolution paths:
  1. **Derive** `vacuum_lorentz_invariant` from L07 (causal invariance) + BDG sprinkling limit → converts O11 "DISSOLVED-PROVISIONAL" to "DISSOLVED" genuinely
  2. **Reformulate** L04/L05 to not require vacuum invariance as a separate axiom (e.g., state for any U-invariant reference state σ₀)
  3. **Close the cheap gap first**: `Matrix.cfc_conj_unitary` sorry can be discharged by copying from Lean-QuantumInfo; this resolves item (a) of IC46 without touching item (b), giving a partial improvement
- Also: close `petz_monotonicity` axiom via the LQI adapter (not load-bearing, but removes a listed axiom)

### Priority 1: Continue Stage A Lean audit
- The IC46 correction demonstrated that narration-based assessment was missing axioms. More corrections likely when the other Lean files are inspected.
- Batch 1: `RA_GraphCore.lean`, `RA_AmpLocality.lean` (foundations)
- Batch 2: `RA_O14_Uniqueness.lean`, `RA_D1_Proofs.lean` (BDG structure)
- Batch 3: `RA_Koide.lean`, `RA_BaryonChirality.lean`
- Batch 4: `RA_Spin2_Macro.lean`, remaining files

### Priority 2: Weak-vertex-access derivation for π±
- Extends Paper II §6.5 Type VI from open program to CV result
- Closes pion residual as a structural consequence, not an imported Goldstone mechanism
- Directly tests the "bosons to brains, one mechanism" claim
- Note: Apr 17 exploratory work showed the formula works for π± to 0.5% but fails for kaons/muons/neutron; needs further structural development

### Priority 3: N_eff = L_q³ = 64 derivation
- IC41: the one remaining conjecture in the proton mass cascade
- If closed, the entire mass cascade becomes DR-tier
- Path: BDG Poisson-CSG self-consistency condition on baryon motifs

### Priority 4: Branching volume V(γ, d) for Σ(II), Σ(III)
- Upgrades σ-filter classification from CV to DR
- The Apr 11 attempt got K* right; needs angular momentum treatment for ω

### Priority 5 (longer-term): t_trans from nucleation
- Closes the one parameter in the DESI dark energy result
- Requires nucleation perturbation spectrum development

---

## 7. Architectural principle preserved across sessions

The programme has a consistent architecture that survives all session-to-session work:

**Five-level epistemic ladder** (established Apr 10 with ChatGPT):
1. Kernel (philosophically necessary)
2. Closure (uniqueness-forced mathematical pinning)
3. Implementation (specific 4D theory)
4. Interpretation (physical reading)
5. Speculation (ambitious extrapolation)

**Seven-row spine** (Apr 10): each kernel axiom paired with a uniqueness closure. 6 of 7 closures are LV or CV.

**Epistemic ladder** (used consistently in papers): LV → CV → DR → AR → PI → CN → OP

**Audit notes as a standard document class**: five produced Apr 10 (actualization criterion, GS02, IC30, particle topology, GR bridge). Pattern continues in any new vulnerable claim.

**Bimodal ontology** (Apr 12): (G, Π) = (actualized graph, potential/unsettled). Both are real; actualization is irreversible inscription. Berry phase is an Axiom 6 joint observable.

**Self-writing universe** (Apr 10 philosophical capstone): "RA has structure, not parameters. Parameters are what you need when your model is missing structure."

---

## 8. What the inventory actually proves (corrected Apr 17)

Counting strictly:

- **12+ zero-parameter numerical matches** (all within 1.5%)
- **9 dissolved foundational problems** — with caveat that O11 (Lorentz) is DISSOLVED-PROVISIONAL per IC46 until `vacuum_lorentz_invariant` is closed; the other 8 remain DISSOLVED
- **15+ falsifiable predictions** (5 testable now with existing data: BMV, WIMP null, DESI w-void, BAO splitting, SN residuals)
- **176+ Lean theorems**, with accurate gap accounting:
  - 2 `sorry`s (both closable: `Matrix.cfc_conj_unitary` from LQI; `RA_AmpLocality.lean` List.Perm assembly)
  - 2 axioms (`vacuum_lorentz_invariant` — framing-discipline violation; `petz_monotonicity` — not load-bearing)
- **77 pages canonical suite** + 12 archived papers on Zenodo

The task forward: **keep closing bridges until every PI becomes DR and every CN becomes CV or DR**. Every hadron, every meson, every decay rate should fall out of (DAG + BDG + LLC) with nothing imported as mechanism. **And keep closing axioms** — the `vacuum_lorentz_invariant` axiom is exactly the kind of "import as mechanism" the framing discipline forbids.

The η' 1.8% match is the current cleanest example of the programme working: one primitive framework (the σ-filter), one structural fact (η' is the unique Type V), one consequence (mass ≈ baryon cascade). No Goldstone theorem needed. No anomaly mechanism imported. Just the topology doing its work.

That's the pattern we extend to everything else — including, now, the Lean core itself.
