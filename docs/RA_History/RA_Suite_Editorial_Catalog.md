# Suite-Wide Editorial Catalog — April 17, 2026

**Purpose.** Apply ChatGPT's two suite-wide rewrite rules:
1. **Legacy-series citations demoted to historical/archival only.** The 4-paper suite is primary; RAQM/RAQI/RACI/RAHC/RACF/RAGC/RASM/RACL/RATM/RADM/RAEB are archival.
2. **QFT/GR vocabulary is translation, not mechanism or success criterion.** RA generates physics from primitives; QFT/GR concepts are used as translation dictionaries.

**Format.** Each fix has: location, current text, proposed text, rationale. Two severity tiers:
- **[CRITICAL]** violates rule 1 or 2 directly; must be fixed
- **[SOFTEN]** acceptable but could be sharpened
- **[KEEP]** looks like a violation but is actually a correct use (called out so you can confirm)

Paper I has been audited separately; preliminary scan shows it does not have legacy-series citations or major QFT identification-vs-translation issues. The catalog starts at Paper II.

---

## PART A: LEGACY-SERIES CITATIONS

### PAPER I — LEGACY CITATIONS

**None found.** Paper I uses "Paper II", "Paper III", "Paper IV" as cross-references. Clean.

### PAPER II — LEGACY CITATIONS

**None found.** Paper II does not cite RAQM/RAQI/RACI/RAHC/etc. directly. Clean.

### PAPER III — LEGACY CITATIONS

**A3.1 [KEEP with audit note] — "RACL chain" naming in abstract and §2**

Location: line 111 (abstract), line 163 (§2 "derivation chain")
Current: "General relativity with Λ=0 follows from the **RACL chain**..." / "The **RACL chain** proceeds in seven steps..."

Analysis: "RACL" was the name of the predecessor paper on causal-Lorentzian work, but in this context it's being used as the name of the derivation chain itself, not as a citation. It's a naming vestige of the legacy series that now reads as an acronym the paper doesn't define.

**Proposed fix:** Rename "RACL chain" → "GR derivation chain" throughout. Two occurrences.

Rationale: The paper defines the chain in §2 anyway. The RACL name adds no information and carries the legacy inheritance ChatGPT's rule 1 forbids.

### PAPER IV — LEGACY CITATIONS

**A4.1 [CRITICAL] — RACI cited as primary source for DFT/F1 computation (§5.2)**

Location: lines 313–319 (§5.2 Computational evidence from DFT calculations)

Current text (prose):
> "These DFT results, combined with the non-Markovian decoherence analysis (§5.1.3), give quantitative support for the Causal Firewall conditions in the RNA-world parameter range. **The computational protocol is described in the accompanying supplementary material to RACI [Sandeman2026RACI].**"

Current text (audit paragraph I added earlier today):
> "The B3LYP/6-311+G\* protocol and the specific R_QD values for the representative molecule set are claimed at the CV tier **on the basis of the RACI supplementary computation**. ... Readers who require audit-level independence should regard this row as plausible and reproducible in principle but not audited within the present suite pass, and **should consult the RACI supplementary material** for the underlying computation."

**Problem:** This cites RACI as the primary source for the DFT material, which violates rule 1. The suite either contains the DFT computation or it doesn't — pointing at a superseded preprint is not acceptable.

**Three options for the fix (you pick):**

**Option (a) — migrate:** Move the DFT protocol + R_QD results into Paper IV §5.2 directly, as a short subsection with the B3LYP/6-311+G\* protocol, the molecule list, the R_QD values, and the interpretation. This would add ~0.5–1 page to Paper IV and establish Paper IV as primary.

**Option (b) — soften to PI:** Drop the CV claim. Say: "DFT calculations at the B3LYP/6-311+G\* level are expected to support F1 for small prebiotic molecules; the specific verification is an open computational target for the present suite." Remove the RACI citation.

**Option (c) — supplement-to-this-suite:** State that a Paper IV supplement (to be published alongside this suite) contains the DFT protocol; cite the supplement rather than RACI. This requires producing the supplement.

My recommendation: **Option (b) is safest for the immediate suite pass** — it removes the legacy dependency without requiring migration work. Option (a) is the correct long-term fix but adds significant content.

**A4.2 [CRITICAL] — RACI cited again in §5.3 sandwich bound**

Location: line 342

Current:
> "**Computational evidence.** B3LYP/6-311+G\* density functional theory calculations supporting Condition F1 have been performed for small prebiotic molecules, verifying that the quantum Darwinism redundancy parameter exceeds unity for molecular environments at biological temperatures [Sandeman2026RACI]."

**Fix:** Same as A4.1. If Option (b), change to: "B3LYP/6-311+G\* density functional theory calculations are expected to support Condition F1 for small prebiotic molecules at biological temperatures; the explicit verification is an open computational target for this suite." Remove RACI citation.

**A4.3 [CRITICAL] — RAQI/RAQM cited as primary sources for KCB, t\*, Landauer, Maxwell's demon (§7)**

Location: line 351 (the §7 scope note I wrote earlier today — which you now correctly identify as worse than what was there before)

Current:
> "**Scope note.** The results in this section—the Kinematic Coherence Bound, the spin-bath collapse timescale t\*=0.274/g, the Landauer bound, and the Maxwell's demon analysis—**are inherited from the RAQI and RAQM companion papers rather than newly derived in Paper IV**. They are presented here for suite coherence, because the complexity-and-life architecture developed in §§2–6 uses the KCB-style quantum-information machinery as its decoherence backbone. Readers should not read the presentation in this section as fresh first-principles closure within Paper IV; **the load-bearing derivations live in RAQI/RAQM**."

**Problem:** This is the exact framing inversion you identified. The scope note I wrote makes RAQI/RAQM primary and Paper IV dependent, which is backwards.

**Proposed fix:** Replace with:
> "**Scope note.** The results in this section—the Kinematic Coherence Bound (KCB), the spin-bath collapse timescale t\*=0.274/g, the Landauer bound, and the Maxwell's demon analysis—are presented as consequences of the actualization-event ontology established in Paper I and elaborated through the renewal-motif architecture of Paper II. Earlier versions of some of this material appeared in predecessor preprints (RAQI, RAQM) that this suite supersedes; the canonical presentations are now the cross-suite locations indicated in the text (principally Paper I §[TBD] and the derivations given in this section)."

Rationale: Inverts the primacy. Paper I is primary; legacy preprints are archival. Cross-references to Paper I should be added where specific derivations live there; where derivations are in this section, they stand on their own.

**Question for you to answer before I can finalize this fix:** Where in Paper I does the KCB / t\* / Landauer / spin-bath material actually live? If it's not in Paper I of this suite, then the material needs to be either (i) added to Paper I, (ii) derived in Paper IV §7 on its own merits, or (iii) acknowledged as inherited from superseded work without the CV/DR claim. I can do (ii) if you confirm that the §7 text already contains the derivations; otherwise (i) or (iii) is needed.

**A4.4 [CRITICAL] — §12 table row cites RACI**

Location: line 524

Current:
> "B3LYP support for F1 & DFT computation (RACI supplement) & CV (not re-audited in suite pass) \\\\"

**Fix:** Depends on Option (a)/(b)/(c) in A4.1. If Option (b): replace row with
> "B3LYP support for F1 (DFT) & Expected to hold; not verified in suite & Open computational target \\\\"

**A4.5 [CRITICAL] — Bibliography entries for legacy preprints**

Location: lines 588, 589, 590, 594

Current:
> `\bibitem{Sandeman2026RACI}` — RACI preprint
> `\bibitem{Sandeman2026RAHC}` — RAHC preprint
> `\bibitem{Sandeman2026RACF}` — RACF submission
> `\bibitem{Sandeman2026RAQI}` — RAQI preprint

**Proposed fix — two options:**

**Option (x) — remove entirely** if no Paper IV prose references them after the A4.1–A4.3 fixes are applied. Check after fixes.

**Option (y) — retain as archival-only** with a note: Add a "Historical note" paragraph at the end of the paper before the bibliography stating:
> "Predecessor preprints (RAQM, RAQI, RACI, RAHC, RACF) developed earlier versions of parts of this material. The present 4-paper suite supersedes them; they are retained here only as archival provenance. Where specific superseded computations are referenced (e.g., the DFT/F1 protocol), this is explicit and does not imply current validity of the full preprint."

Then keep the `\bibitem` entries but they are cited only from the historical note, not from load-bearing claim locations.

My recommendation: **Option (y)**. Provenance matters for academic honesty; you authored those preprints. Removing them entirely would look like hiding the evolution of the work.

---

## PART B: QFT/GR VOCABULARY — IDENTIFICATION vs TRANSLATION

### PAPER II — LARGEST EXPOSURE

**B2.1 [CRITICAL] — §2 Topology types table uses SM labels as primary, BDG as derivative**

Location: lines 106–115 (§2 "The Five Topology Types" table)

Current:
```
Type | Particle class            | BDG depth L | Color      | Gauge structure
1    | Quarks                    | 4           | 3-colour   | SU(3) confined
2    | Gluons                    | 3           | 3-colour   | SU(3) confined
3    | Gauge bosons (W,Z,γ)     | 1           | singlet    | SU(2)×U(1)
4    | Higgs boson               | 2           | singlet    | scalar
5    | Leptons and neutrinos     | 1           | singlet    | chiral
```

**Problem:** The column ordering — "Particle class" first, "BDG depth L" second — treats the SM label as primary and the BDG structure as derivative. This is the exact identification-as-mechanism pattern. Also, "Color" (SM concept) and "Gauge structure" (SM concept) are presented as properties of the BDG types rather than as translation targets.

**Proposed fix:**

```
Type | BDG depth L | Branching structure  | SM translation
1    | 4           | 3-spatial N_2 branches | Quarks (color-triplet, confined)
2    | 3           | 3-spatial N_2 branches | Gluons (color-octet, confined)
3    | 1           | singlet                | Gauge bosons W, Z, γ
4    | 2           | N_2-dominant scalar    | Higgs boson
5    | 1           | singlet, chiral        | Leptons / neutrinos
```

Rationale: BDG depth and branching structure are RA-native; the SM column is explicitly labeled "SM translation" per rule 2. The color/gauge group columns are dropped because they were doing identification work that the "SM translation" column now does in honest form.

Follow-through: Table caption should say "BDG topology classes and their Standard-Model translations" and the surrounding prose should be checked for "color" / "SU(3)" language. Specifically line 124 ("Confinement from BDG topology") is fine, but §2.2 "Three generations" references SU(3)_gen which may need the same softening.

**B2.2 [SOFTEN] — §2.2 SU(3)_gen identification**

Location: line 128

Current:
> "Three generations of quarks and leptons follow from the SU(3)_gen symmetry of the BDG excitation levels {N_2, N_3, N_4}—the three non-gravitational degrees of freedom of the four-dimensional causal diamond."

**Proposed fix:**
> "Three generations of the fermion spectrum follow from the three-fold structure of the BDG excitation levels {N_2, N_3, N_4} — the three non-gravitational degrees of freedom of the four-dimensional causal diamond. The continuous-symmetry translation of this three-fold structure, useful for connecting to Standard-Model language, is an approximate SU(3)_gen; in RA, the primary structure is the discrete three-level BDG architecture, of which SU(3)_gen is a derived continuum image."

**B2.3 [SOFTEN] — §3.3.1 "The structural parallel between generations and colours"**

Location: lines 196–201

Current:
> "The three generation levels {N_2, N_3, N_4} and the three colour charges {r, g, b} arise from precisely the same source..."
> "For the colour sector, the continuous extension of S_3 is SU(3)_colour, whose invariants give the Gell-Mann–Okubo baryon mass relations. The analogous structure for the generation sector is SU(3)_gen."

**Proposed fix:** Keep the structural parallel claim (it's real RA content) but invert the primacy:
> "Two three-fold structures in the BDG architecture have precisely the same source: the three spatial components of N_2 branching, and the three non-gravitational excitation levels {N_2, N_3, N_4}. Both are properties of d=4 causal geometry. In the continuum translation to the Standard Model, the first three-fold structure is what SU(3)_colour organizes, and the second is what an approximate SU(3)_gen would organize."

**B2.4 [SOFTEN] — §3.4 "Koide breaking in quarks"**

Location: lines 227–246

Current (lead sentence): "The exact Koide relation K=2/3 holds for charged leptons because they carry no colour charge—SU(3)_gen acts undisturbed in the lepton sector."

Current (§3.4 table heading): "Sector | Q_N1 | C_{2,colour} | K_pred | K_obs"
Sector labels: "Leptons", "Down quarks", "Up quarks", "Neutrinos"

**Proposed fix (lead sentence):**
> "The exact Koide relation K=2/3 holds for BDG Type-5 motifs (which the Standard Model names charged leptons) because they carry no N_2 spatial-branching charge — the generation-level structure acts undisturbed in this sector."

**Proposed fix (table):** Keep the table structure but rename "Sector" column header to "BDG motif (SM translation)" and rows to:
- "Type 5 (charged leptons: e, μ, τ)"
- "Type 1, Q_N1 = 1 (down quarks: d, s, b)"
- "Type 1, Q_N1 = 2 (up quarks: u, c, t)"
- "Type 5, Q_N1 = 0 (neutrinos)"

**B2.5 [CRITICAL] — §4 "The Mass Cascade" treats SM particles as the targets of derivation**

Location: lines 354–480 (entire §4)

Current framing: The section opens "The proton mass is not input into RA. It is identified via a multiplicative cascade..." The language throughout treats m_p, m_H, m_W, m_π, r_p as the things being derived.

**Problem:** This is the exact violation. The cascade derives a specific BDG quantity (m_P · α_EM^5 / 2^28 = 941 MeV). That number gets *identified with* the observed proton mass. The proton mass is an external empirical target; RA derives the BDG number.

**Proposed fix (opening paragraph of §4):**
> "This section derives a specific BDG quantity: the mass scale produced by a five-power Poisson-CSG cascade through the depth-4 coefficient c_4 = 8. The derived value, m_P · α_EM^5 / 2^28 ≈ 941 MeV, is then identified with the observed proton mass (938.3 MeV, 0.3% match). The identification is a phenomenological interpolation in the sense of §1; what is derived from RA primitives is the cascade structure and the numerical value, not the SM-level 'proton mass' concept. Extensions of the cascade to BDG quantities identified with m_n, m_π, m_H, r_p, and m_W are given below, with epistemic tiers flagged throughout."

Follow-through: individual subsection framings (§4.5 Neutron, pion, §4.7 Higgs, §4.8 W) should be checked for the same translation discipline.

**B2.6 [SOFTEN] — §5 "Force Ranges: One Principle, Three Outcomes"**

Location: lines 500–530

Current: The section opens "The range of a force in RA follows from a single unified principle: how far an exchange pattern can propagate..." and uses "EM", "Weak", "Strong" as primary labels.

**Proposed fix:** Retain SM labels but clarify their status. Change section subtitle from "One Principle, Three Outcomes" to "One Principle, Three BDG-Native Outcomes," and add a framing sentence:
> "RA produces three qualitatively distinct BDG-native propagation behaviors from a single bandwidth-limited graph-propagation principle. The Standard Model classifies these behaviors as electromagnetism (Coulombic), weak force (Yukawa-like), and strong force (confining). The RA statements below are about the BDG propagation behavior; the SM labels are used for translation."

**B2.7 [SOFTEN] — §6 "The Gauge Group from BDG Geometry" opening**

Location: lines 571–573

Current: "The Standard Model gauge group SU(3)×SU(2)×U(1) is identified in this paper, at the DR/PI level, with the product of two independent geometric structures on the BDG-filtered growth process. The identification is a programme-level proposal, not a closed theorem chain from BDG primitives to a fully derived gauge group."

Analysis: This is already softened from the earlier "IS" language. The word "identified" and the "not a closed theorem chain" caveat are correct. Minor polish only — keep as-is or very lightly tweak to reinforce that the BDG algebra is primary:

**Light touch fix (optional):**
> "This section describes two independent geometric structures on the BDG-filtered growth process: an inter-depth transfer structure and an intra-depth direction structure. At the DR/PI level, the product of these structures admits an identification with the Standard Model gauge group SU(3)×SU(2)×U(1). The identification is a programme-level proposal, not a closed theorem chain: what RA derives is the BDG transfer-matrix algebra and its holonomy, and its translation to continuum gauge theory is an open question discussed below."

**B2.8 [KEEP] — §5.3 "Strong force asymptotic freedom and confinement"**

Location: lines 536+

Analysis: This section uses "colour charge," "quark separation," "QCD flux tube" language heavily. On first reading I flagged it as a potential problem, but looking more carefully: it's carefully labeled as what happens to "N_2 branching charge" in RA language, with the SM translations used throughout as reading aids. The paragraph structure is RA-primary, SM-translation-secondary. I think it's acceptable as written, and rewriting it to strip "colour charge" entirely would make it much harder to read.

**Recommendation:** Keep as-is. If you disagree, let me know and I'll propose the stripped version.

**B2.9 [CRITICAL] — §9.2 "Charge quantization"**

Location: line 783

Current: "Charge quantization in units of e/3 is a theorem about N_2 winding numbers in the BDG closure pattern. In a 3+1D causal graph, a vertex can receive signed edges from at most three independent spatial directions. The net signed N_1 charge is therefore constrained to integer values in {-3,-2,-1,0,+1,+2,+3}. Identifying the unit charge with e/3 (one spatial edge per dimension)..."

Analysis: The first sentence is fine (RA-native statement about N_2 winding). The "Identifying the unit charge with e/3" step is the translation — and then the follow-through paragraph labels the result with SM names (up quark, down quark, electron, neutrino, W±). This is okay because RA really does produce the {-3,-2,-1,0,+1,+2,+3} signature.

**Minor fix:** Replace the follow-through paragraph's opening
> "This matches the complete set of electric charges in the Standard Model..."
with:
> "Under the e/3 translation, the integer values {-3,-2,-1,0,+1,+2,+3} correspond to the electric-charge assignments the Standard Model gives to its full particle content: up quark +2e/3 (Q_{N_1}=+2), down quark -e/3 (Q_{N_1}=-1), electron -e (Q_{N_1}=-3), neutrino 0 (Q_{N_1}=0), W± (Q_{N_1}=±3), and neutral particles (Q_{N_1}=0). The RA content is the discrete seven-value signature in 3+1D; the SM content is the particular mapping of those values to the observed particle catalog."

### PAPER III — MODERATE EXPOSURE

**B3.1 [SOFTEN] — §1 Introduction "must reproduce general relativity"**

Location: line 139

Current: "Paper III is the paper where RA meets the macroscopic universe. The causal graph of Paper I, filtered by the BDG action and populated by the renewal motifs of Paper II, **must reproduce general relativity** at large scales, address the outstanding puzzles of cosmology, and provide a coherent account of horizons and entropy."

**Problem:** "Must reproduce general relativity" is exactly the success-criterion language ChatGPT's rule 2 forbids. RA doesn't need to reproduce GR; it needs to account for the observational regularities GR describes.

**Proposed fix:**
> "Paper III is the paper where RA meets the macroscopic universe. The causal graph of Paper I, filtered by the BDG action and populated by the renewal motifs of Paper II, **must account for the gravitational and cosmological phenomena** that general relativity describes, address the outstanding puzzles of cosmology, and provide a coherent account of horizons and entropy. Where RA-native structure admits a continuum translation that matches the GR description, that is shown explicitly; where it does not, the difference is identified rather than papered over."

**B3.2 [SOFTEN] — §4.3 "MOND-like phenomenology reproduced"**

Location: line 292

Current: "This **reproduces the MOND-like phenomenology** (Milgrom's a_0) as an emergent scale in the RA framework, rather than a fundamental acceleration constant."

**Proposed fix:**
> "This produces a MOND-like phenomenology: the RA-native modification to Poisson's equation at low actualization density generates an effective acceleration scale (analogous to Milgrom's a_0) that emerges from BDG dynamics rather than being posited as a fundamental constant."

Minor fix. "Reproduces" is the flagged word.

**B3.3 [KEEP] — §9.2 DESI and §9.2.1 (w_0, w_a)**

Location: lines 614–626

Analysis: This section uses "reproduces the DESI measurements" once. In context, it's fine — the RA claim is "a narrow parameter band in the EdS→Milne family matches DESI's fitted values." The word "reproduces" is doing descriptive work, not setting a success criterion.

**Recommendation:** Keep.

**B3.4 [SOFTEN] — §10 Conclusion "recover a large fraction"**

Location: line 806

Current: "...a finite discrete theory with causal severance, a severed-link entropy observable, and structurally vanishing Λ **can already recover a large fraction of the conceptual architecture** usually distributed across black-hole thermodynamics, gravitational theory, and cosmological phenomenology."

**Proposed fix:**
> "...a finite discrete theory with causal severance, a severed-link entropy observable, and structurally vanishing Λ already produces an RA-native architecture that accounts for a large fraction of the phenomena traditionally organized across black-hole thermodynamics, gravitational theory, and cosmological phenomenology — without requiring a one-to-one translation of every legacy concept."

Reinforces rule 2 explicitly.

### PAPER IV — MODERATE EXPOSURE

**B4.1 [SOFTEN] — §1 Intro: "does the same machinery generate biological complexity?"**

Location: line 141

Current (already softened today): "Papers I–III develop the consequences of this commitment, filtered through the BDG integers (1,-1,9,-16,8), in the domains of quantum mechanics, the Standard Model, general relativity, and cosmology. The discrete/topological core of those papers is well-supported; several continuum-bridge steps are explicitly labeled DR (derived) conditional, PI, or CN, as their epistemic-status tables document. The present paper asks: **does the same machinery extend to biological complexity?**"

Analysis: The phrase "in the domains of quantum mechanics, the Standard Model, general relativity, and cosmology" still frames Papers I–III's success by matching legacy theory names. The question "does the same machinery extend to biological complexity" is fine.

**Proposed fix:**
> "Papers I–III develop the consequences of this commitment, filtered through the BDG integers (1,-1,9,-16,8), across phenomena usually organized by quantum mechanics, the Standard Model, general relativity, and cosmology. The discrete/topological core of those papers is well-supported; several continuum-bridge steps that translate RA-native structure into those legacy vocabularies are explicitly labeled DR conditional, PI, or CN, as the epistemic-status tables document. The present paper asks whether RA-native primitives extend to the phenomena usually organized as biological complexity."

**B4.2 — All legacy-citation fixes covered in A4.1–A4.5.**

---

## PART C: OPERATING PRINCIPLE TO STATE EXPLICITLY IN THE SUITE

ChatGPT's suggestion — and I endorse it — is that the suite should state its framing discipline explicitly in one place. **Proposed new paragraph for Paper I §1 (Introduction), just after the ontology is stated:**

> **Framing discipline.** The aim of Relational Actualism is not to append a discrete substructure to legacy continuum physics, nor to recover every legacy concept one-for-one. The aim is to derive empirical physics from RA primitives: the growing causal graph, the BDG filter, and the actualization rule. Where the RA-native structure admits a translation into the vocabulary of quantum field theory, general relativity, or the Standard Model, that translation is useful as a reading aid and as a point of contact with existing theory. But the translation is never the mechanism, and matching legacy concepts one-for-one is never the success criterion. The success criterion is empirical: RA should produce the observational phenomena, whether or not those phenomena organize themselves into the categories legacy frameworks have historically used.

This paragraph, plus a short echo in each of Papers II/III/IV referencing back to it, would anchor the suite's framing discipline explicitly and let reviewers calibrate.

---

## SUMMARY OF FIXES BY PAPER

### Paper I
- Add framing-discipline paragraph (Part C)

### Paper II
- **B2.1** [CRITICAL] Restructure topology table: BDG primary, SM translation secondary
- **B2.2** [SOFTEN] SU(3)_gen language in §2.2
- **B2.3** [SOFTEN] Primacy inversion in §3.3.1 structural parallel
- **B2.4** [SOFTEN] Koide breaking sector labels
- **B2.5** [CRITICAL] §4 opening: cascade derives BDG quantity, identifies with m_p
- **B2.6** [SOFTEN] §5 force ranges framing
- **B2.7** [LIGHT] §6 gauge group opening (optional)
- **B2.9** [CRITICAL] §9.2 charge quantization translation
- Short echo of framing-discipline paragraph at the start

### Paper III
- **A3.1** [fix] Rename "RACL chain" → "GR derivation chain" (2 occurrences)
- **B3.1** [SOFTEN] §1 "must reproduce general relativity" → "must account for the phenomena GR describes"
- **B3.2** [SOFTEN] §4.3 "reproduces MOND-like phenomenology" → "produces a MOND-like phenomenology"
- **B3.4** [SOFTEN] §10 "recover a large fraction" → "accounts for a large fraction ... without requiring one-to-one translation"
- Short echo of framing-discipline paragraph at the start

### Paper IV
- **A4.1** [CRITICAL] §5.2 DFT/F1 — pick Option (a)/(b)/(c); my recommendation is **(b)**: soften to open target, drop RACI citation
- **A4.2** [CRITICAL] §5.3 DFT evidence reference — same treatment
- **A4.3** [CRITICAL] §7 scope note — invert primacy; but requires knowing where KCB/t\*/Landauer actually live in this suite
- **A4.4** [CRITICAL] §12 table row — update per A4.1 fix
- **A4.5** [decision] Bibliography: my recommendation is **Option (y)** — retain legacy preprints as archival-only with a "Historical note" paragraph
- **B4.1** [SOFTEN] §1 intro phrasing
- Short echo of framing-discipline paragraph at the start

---

## DECISIONS NEEDED FROM YOU BEFORE I CAN APPLY

1. **A4.1 / A4.2:** For the DFT/F1 material, which option? (a) migrate into Paper IV, (b) soften to open target and drop RACI citation, or (c) produce a standalone supplement?

2. **A4.3:** Where in the current 4-paper suite do the KCB / t\*=0.274/g / Landauer / Maxwell's demon derivations live? If they're already in Paper I, tell me the section. If they're not yet in the suite at all, we either need to add them to Paper I or downgrade the §7 claims in Paper IV.

3. **A4.5:** Retain legacy bibliography entries with a "Historical note" (Option y)? Or remove entirely (Option x)?

4. **Part C framing-discipline paragraph:** Insert into Paper I §1 and echo in II/III/IV? I strongly recommend yes.

5. **B2.1 topology table rewrite:** Approve the proposed column restructuring, or do you want a different ordering?

6. **B2.5 §4 cascade framing:** Approve the proposed "derives BDG quantity, identifies with proton mass" framing?

7. **Any [KEEP] items** I've called correct that you think are actually violations?

Once I have answers, I can apply the fixes in one pass per paper and re-compile.
