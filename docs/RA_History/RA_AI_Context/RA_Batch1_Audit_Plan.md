# Relational Actualism — Batch 1 Audit Plan
## Submitted Papers: RAQM, RACL, RATM
### April 8, 2026 (Evening Session)

---

## Context

Three papers are currently under review at journals. All three contain stale Lean counts, outdated file references, and in some cases superseded physics claims. This document specifies every required change to bring each paper fully current with the RA state as of April 8, 2026.

### Current RA State (reference)

| Item | Value |
|---|---|
| Lean files | 7 (all compile clean in Lean 4.29) |
| Total theorems | 163 |
| Total sorry | 1 (LQI adapter in RA_AQFT_Proofs_v10.lean) |
| O01 (amplitude locality) | PROVED (RA_AmpLocality.lean, zero sorry) |
| O02 (causal invariance) | PROVED unconditionally (RA_AmpLocality.lean, zero sorry) |
| L01–L03 | PROVED (RA_GraphCore.lean, zero sorry) |
| L09 (Koide) | PROVED (RA_Koide.lean, zero sorry) |
| GR derivation | RA-native: L01+O01+L11 → BD uniqueness → EH → field eqs |
| Bianchi identity | IS the LLC at metric level (not a separate geometric fact) |
| O10 (discrete Bianchi) | DISSOLVED — Bianchi is LLC in continuum costume |
| O11 (Lorentz emergence) | DISSOLVED — Lorentz is causal invariance in continuum costume |
| GS02 (gauge groups) | CV — SU(3)×SU(2)×U(1) from BDG sign mechanism |
| IC30 (α_EM) | CLOSED — α⁻¹ = 137.036 via discrete Dyson equation (0.00001%) |
| IC31 (μ=1 ↔ m_Z) | OPEN — handled honestly via UV fixed-point framing |
| μ=1 unification | FIVE-scale (QCD, galactic, fault-tolerance, ΔS*, Causal Firewall) |
| Paper architecture | 5-paper suite: P0 (Foundation), P1–P4 |
| Paper architecture (12-paper) | Retained as the detailed derivation suite |

### Lean File Inventory (April 8, 2026)

| File | Content | Sorry |
|---|---|---|
| RA_D1_Proofs.lean | L08, L10, L11, L12 + 75 original results + aliases | 0 |
| RA_AmpLocality.lean | O01 (amplitude locality) + O02 (causal invariance) | 0 |
| RA_GraphCore.lean | L01 (LLC), L02 (graph cut), L03 (Markov blanket) | 0 |
| RA_Koide.lean | L09 (Koide formula K=2/3) | 0 |
| RA_AQFT_Proofs_v10.lean | L04, L05, L06, L07 + frame independence + Rindler | 1 (LQI adapter) |
| RA_Spin2_Macro.lean | O10s (spin-2 macroscopic limit) | 0 |
| RA_SteinChen.lean | Stein-Chen supporting lemmas | 0 |

---

## RAQM — Relational Actualism and Quantum Mechanics
**Journal:** Foundations of Physics (awaiting editor assignment)
**Current version:** RAQM_v4.pdf (25 pages)
**Priority:** HIGHEST — not yet reviewed; all fixes can go in before referee reports

### Fix 1 [HIGH] — Abstract: Lovelock → BDG uniqueness

**Location:** Page 1, abstract, line ~15
**Current:** "the Einstein field equations are the unique consistent macroscopic description of the RA causal graph by Lovelock's theorem"
**Replace with:** "the Einstein field equations are the unique consistent macroscopic description of the RA causal graph via BDG uniqueness (Benincasa & Dowker, 2010): the Lean-verified Local Ledger Condition, amplitude locality theorem, and d=4 closure theorem force the BDG action as the unique growth functional, whose continuum limit is the Einstein-Hilbert action"

### Fix 2 [HIGH] — Abstract: Lean counts

**Location:** Page 1, abstract
**Current:** References to "93 Lean-verified results," "RA_D1_Proofs.lean (73 results) and RA_Alpha_EM_Proof.lean (20 results)"
**Replace with:** "163 Lean-verified theorems across seven files with one intentional sorry (the LQI adapter in RA_AQFT_Proofs_v10.lean)"
**Also update:** File names throughout (RA_Alpha_EM_Proof.lean is superseded; add RA_AmpLocality.lean, RA_GraphCore.lean, RA_Koide.lean)

### Fix 3 [HIGH] — Abstract: O01 now proved

**Location:** Page 1, abstract
**Current:** "causal invariance... given amplitude_locality axiom"
**Replace with:** "causal invariance is unconditional — amplitude locality is proved as a theorem of discrete DAG dynamics (RA_AmpLocality.lean) with zero sorry tags"

### Fix 4 [HIGH] — Section 5.3.2 (p. 17): amplitude_locality status

**Location:** Page 17, paragraph on amplitude_locality
**Current:** "The amplitude_locality axiom (used in causal_invariance) is physically justified by QFT microcausality... but its intrinsic discrete proof is an open target"
**Replace with:** "Amplitude locality has been proved as a theorem of discrete DAG dynamics (bdg_amplitude_locality in RA_AmpLocality.lean) — the proof exploits the transitivity of the causal order to show the BDG action increment depends only on the causal past, with no appeal to QFT microcausality. With O01 proved, the causal invariance theorem (bdg_causal_invariance in the same file) is unconditional, with zero sorry tags."
**Remove:** "Hard Wall HW2" for amplitude locality. HW2 should be narrowed to only the type III₁ AQFT extension.

### Fix 5 [HIGH] — Table 2 (p. 22): Lean theorem → physics claim

**Location:** Page 22, Table 2

**Update causal_invariance row:**
- Current: "Quantum measure independent of spacelike ordering (given amplitude_locality axiom)"
- Replace: "Quantum measure independent of spacelike ordering. Unconditional — amplitude locality proved as theorem. Zero sorry tags."

**Add new rows:**

| Lean theorem | Physics claim |
|---|---|
| bdg_amplitude_locality (RA_AmpLocality.lean) | BDG amplitude depends only on causal past. O01 closed. |
| bdg_causal_invariance (RA_AmpLocality.lean) | Quantum measure permutation-invariant. O02 closed unconditionally. |
| koide_formula (RA_Koide.lean) | Koide K=2/3 from BDG integers. L09. |
| local_ledger_condition (RA_GraphCore.lean) | LLC at every DAG vertex. L01. |
| graph_cut_theorem (RA_GraphCore.lean) | LLC holds independently at causal severance. L02. |
| markov_blanket (RA_GraphCore.lean) | Subgraph shielding from exterior. L03. |

**Update paragraph below table:**
- Remove: "The amplitude_locality axiom... its intrinsic discrete proof is an open target (Hard Wall HW2)"
- Replace: "All causal graph theorems are now fully proved. The remaining Lean target is the type III₁ AQFT extension of frame_independence and rindler_stationarity to infinite-dimensional von Neumann algebras via Tomita-Takesaki modular theory."

### Fix 6 [MEDIUM] — Section 3.2.1 (p. 6): Forward reference to α_EM = 137.036

**Location:** Page 6, after the paragraph on α⁻¹_EM = 137
**Add:** "The integer 137 is the bare BDG depth-ratio fixed point (Lean-verified). The dressed coupling receives a fractional correction from angular screening by virtual processes, computed via the discrete Dyson equation: α⁻¹_EM = (137 + √(137² + 4·P_acc·c₂))/2 = 137.036, matching the PDG value to 0.00001% with no free parameters. The full derivation is given in the companion paper RASM [ref]. The near-identity P_acc × c₂ ≈ π²/2 is a consequence of the BDG structure, not an input."

### Fix 7 [MEDIUM] — Page 19: μ=1 scale count

**Location:** Page 19, eq. (19) vicinity
**Current:** "four-scale μ=1 unification of RACF"
**Replace with:** "five-scale μ=1 unification" (QCD confinement, galactic rotation, fault-tolerance, ΔS*, Causal Firewall)

### Fix 8 [MEDIUM] — Page 22: Lean corpus summary

**Location:** Page 22, paragraph starting "The combined RA Lean 4 corpus"
**Current:** "93 fully sorry-free results across RA_D1_Proofs.lean (73 results) and RA_Alpha_EM_Proof.lean (20 results)"
**Replace with:** "163 Lean-verified theorems across seven files (RA_D1_Proofs.lean, RA_AmpLocality.lean, RA_GraphCore.lean, RA_Koide.lean, RA_AQFT_Proofs_v10.lean, RA_Spin2_Macro.lean, RA_SteinChen.lean), with one intentional sorry (the LQI adapter in RA_AQFT_Proofs_v10.lean)"

### Fix 9 [LOW] — Page 23: Code availability

**Location:** Page 23, Code availability section
**Update:** File list to reflect current 7-file Lean suite plus lakefile.lean

### Fix 10 [LOW] — Conclusion (p. 23)

**Location:** Page 23, Conclusion
**Add sentence:** "Since submission, amplitude locality has been proved as a theorem of discrete DAG dynamics, making the causal invariance result unconditional. The Lean-verified corpus has grown to 163 theorems across seven files."

---

## RACL — Conserved Quantities / Einstein Field Equations
**Journal:** Classical and Quantum Gravity (under review)
**Current version:** RACL_CQG_v1.pdf (8 pages)
**Priority:** HIGH — under active review

### Fix 1 [HIGH] — Abstract: Add RA-native derivation

**Location:** Page 1, abstract
**Current:** Abstract describes only the Lovelock derivation chain
**Add to abstract:** "We additionally present a second, fully RA-native derivation that does not require Lovelock's theorem: three Lean-verified results — the Local Ledger Condition (L01), the amplitude locality theorem (O01), and the d=4 BDG closure (L11) — combined with the published Benincasa-Dowker continuum limit theorem, yield the Einstein-Hilbert action directly. The Bianchi identity in this chain is the LLC viewed at the metric level, not a separate geometric constraint."

### Fix 2 [HIGH] — New Section: RA-native derivation

**Location:** After Section 5 (Main Derivation), add Section 5.1

**Title:** "Alternative: The RA-Native Derivation via BDG Uniqueness"

**Content:** Present the chain:
1. L01 (LLC, LV) + O01 (amplitude locality, LV) + L11 (d=4, LV)
2. → BDG uniqueness (Benincasa-Dowker 2010, published theorem): the BDG action is the unique local causal-set action in d=4
3. → Continuum limit of BDG action = Einstein-Hilbert action (BD Theorem 1)
4. → Variation of EH action → G_μν = 8πG P_act[T_μν]
5. → LLC on source → ∇_μT^μν = 0 → ∇_μG^μν = 0

**Key framing:** "In standard GR, the geometric Bianchi identity and matter conservation are mysteriously compatible. In RA, they are the same conservation law (the LLC) at different levels of description. The Lovelock derivation of Section 5 confirms this from the differential geometry side; the BDG uniqueness derivation confirms it from the discrete side. Both arrive at the same field equation."

**Note:** This does NOT replace the Lovelock derivation — it supplements it. The Lovelock derivation remains valid scaffolding and CQG referees will appreciate it. The RA-native derivation is the stronger result.

### Fix 3 [HIGH] — Section 2.1 (p. 2): O01 now proved

**Location:** Page 2, after LLC description
**Add:** "The amplitude locality theorem — that the BDG amplitude depends only on the causal past of the proposed vertex — has been proved as a theorem of discrete DAG dynamics (RA_AmpLocality.lean, zero sorry tags), closing O01. Combined with L01 (LLC) and L11 (d=4 closure), these three Lean-verified results constitute the complete discrete input to the BDG uniqueness derivation."

### Fix 4 [MEDIUM] — Lean counts

**Location:** Page 2 ("93 sorry-free results") and Page 6 (Lean table)
**Update:** 93 → 163 theorems across 7 files

### Fix 5 [MEDIUM] — Lean verification table (p. 6)

**Location:** Page 6, Lean verification status table

**Add rows:**

| Ingredient | File | Status |
|---|---|---|
| Amplitude locality (O01) | RA_AmpLocality.lean | Lean-proved, 0 sorry |
| Causal invariance (O02) | RA_AmpLocality.lean | Lean-proved, 0 sorry (unconditional) |
| Koide K=2/3 (L09) | RA_Koide.lean | Lean-proved, 0 sorry |
| LLC (L01) | RA_GraphCore.lean | Lean-proved, 0 sorry |
| Graph Cut (L02) | RA_GraphCore.lean | Lean-proved, 0 sorry |
| Markov Blanket (L03) | RA_GraphCore.lean | Lean-proved, 0 sorry |

**Update existing rows:** File names where changed

### Fix 6 [MEDIUM] — Section 8 (Relation to Prior Work)

**Location:** Page 6–7
**Add paragraph:** "The RA-native derivation (Section 5.1) supersedes the need for Lovelock's theorem while not contradicting it. The Lovelock derivation remains valid as an independent confirmation from differential geometry, but the fundamental result is that the LLC alone — a vertex-level balance condition machine-checked in Lean 4 — forces the macroscopic dynamics to be GR. The BDG uniqueness chain (L01+O01+L11 → BD → EH) makes this explicit: GR is an output of the discrete dynamics, derived entirely within RA's own mathematical framework."

### Fix 7 [LOW] — Acknowledgements / Data availability

**Location:** Page 7–8
**Update:** Repository file list to current 7-file suite

---

## RATM — The Topology of Matter
**Journal:** Physical Review D (manuscript DQ14566, awaiting referee assignment)
**Current version:** RATM_PRD_v1.pdf (9 pages)
**Priority:** HIGH — passed editorial screen, referee assignment imminent

### Fix 1 [MEDIUM] — Abstract: Lean counts

**Location:** Page 1, abstract
**Current:** "75 results (64 theorems, 11 lemmas, 8 definitions) with zero sorry tags"
**Replace with:** Current count for RA_D1_Proofs.lean including L10/L11/L12 aliases added April 8

**Current:** "101 Lean-verified results"
**Replace with:** "163 Lean-verified theorems across seven files"

### Fix 2 [MEDIUM] — Abstract: File reference

**Location:** Page 1, abstract
**Current:** "RA_AQFT_Proofs_v2.lean"
**Replace with:** "RA_AQFT_Proofs_v10.lean" (note: v2 is the old file; v10 is current)

### Fix 3 [MEDIUM] — Section 8 (Coherent State): File reference

**Location:** Page 7
**Current:** "koide_coherent_state (in RA_AQFT_Proofs_v2.lean)"
**Replace with:** "koide_formula (in RA_Koide.lean)" — the Koide proof was moved to its own file this session

### Fix 4 [MEDIUM] — Section 10 (Conclusion): Lean update

**Location:** Page 8
**Current:** "75 results" and "zero sorry tags"
**Update counts.** Add: "Since submission, amplitude locality (O01) has been proved as a theorem of discrete DAG dynamics (RA_AmpLocality.lean, zero sorry tags), closing the causal invariance theorem unconditionally. The RA Lean corpus now contains 163 theorems across seven files."

### Fix 5 [RECOMMENDED] — New subsection: GS02 gauge group result

**Location:** Section 7 (Physical Interpretation), add §7.6 "Gauge Group Structure"

**Content:** The SU(3)×SU(2)×U(1) gauge group emerges from the alternating sign structure of the BDG coefficients (+,−,+,−,+). Include the depth-by-depth table:

| Depth k | c_k | Sign | Angular effect | Gauge structure |
|---|---|---|---|---|
| 0 | +1 | + | baseline | — |
| 1 | −1 | − | E[N₁]=1 → 2+1 split | SU(2)_L × U(1)_Y |
| 2 | +9 | + | distributed → scalar | U(1) remnant (Higgs) |
| 3 | −16 | − | heavily penalised → confined | inherits SU(3) |
| 4 | +8 | + | distributed → isotropic | native SU(3)_c |

**Framing:** "The 2+1 split at depth 1 has a concrete origin: at μ=1, λ₁=1, so each vertex has on average exactly one nearest causal ancestor. One ancestor picks one spatial direction, breaking three-dimensional isotropy into two transverse (SU(2)_L) and one longitudinal (U(1)_Y). Confirmed by exact enumeration [CV]."

**Rationale:** RATM is the particle topology paper. The gauge group result belongs here more naturally than anywhere else in the suite. It would significantly strengthen the paper's contribution.

### Fix 6 [LOW] — Acknowledgements / Data availability

**Location:** Page 8
**Update:** Repository file list to current 7-file suite

---

## Execution Plan

| Step | Paper | Action | Requires |
|---|---|---|---|
| 1 | RATM | Apply Fixes 1–4, 6 (mechanical updates) | .tex source |
| 2 | RATM | Draft §7.6 GS02 gauge section (Fix 5) | .tex source |
| 3 | RACL | Apply Fixes 3–5, 7 (mechanical updates) | .tex source |
| 4 | RACL | Draft §5.1 RA-native derivation (Fix 2) | .tex source |
| 5 | RACL | Update abstract (Fix 1) | After §5.1 is written |
| 6 | RAQM | Apply all 10 fixes | .tex source |
| 7 | All | Compile, verify zero LaTeX errors, present PDFs | — |

### Source files needed

All three papers require .tex source files. Do you have them, or should I reconstruct from the PDFs?

---

*Audit plan produced by Claude (Opus 4.6), April 8, 2026.*
