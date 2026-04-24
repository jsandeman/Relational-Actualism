# RA Papers — Microphysics RA-Native Audit

**Date:** April 21, 2026
**Scope:** Four-paper suite (I: Kernel/Engine, II: Matter/Forces/Motifs, III: Gravity/Cosmology, IV: Complexity/Life/Firewall), ~3,200 lines total TeX.
**Lens:** Apr 20 framing discipline — does each claim's *mechanism* trace to DAG+BDG+LLC+Nature-measurements, or does it import QM/SM/GR machinery?
**Methodology:** Read each paper's microphysics sections end-to-end; specifically searched for `exp(iS)`, Born rule, wavefunction, amplitude, Schrödinger, interference, superposition, Berry phase, Wilson loop, unitary, SM gauge groups, continuum metric.

---

## 0. Bottom-line finding (read first)

**The papers are more honest than I feared, but less honest than they need to be.**

The papers already contain explicit "programme-level / DR / conditional" flags on several claims that would otherwise look like straightforward derivations. That's the good news.

The bad news: the Born rule and the amplitude function enter RA **at the axiom level**, in Paper I Axiom 2 ("Stochastic actualization"). Every downstream claim that depends on squared-modulus probabilities, complex amplitudes, or Schrödinger evolution inherits this as an imported assumption. Under strict Apr 20 discipline, this is QM-as-mechanism, at the foundation.

Once that's recognized, the scope of the issue becomes clearer. There are roughly three strata in the papers' microphysics:

- **Stratum A — fully RA-native** (DAG/BDG/LLC + integer arithmetic + Nature measurements). Most dimensionless-number results, the severance formalism, the kinematic identifications.
- **Stratum B — depends on Axiom 2 (imported QM structure)**. Schrödinger emergence, Born-rule predictions, Berry-phase gauge group, BMV null, spin-bath collapse.
- **Stratum C — already flagged in the text as conditional/programme-level** (AQFT-layer theorems, SU(3)×SU(2)×U(1) identification, Lorentz-from-causal-invariance, D4U02 analytic closure).

The key observation is that **Stratum B is not currently labeled as such in the papers**. It reads as RA-native derivation because the Axiom 2 import is never re-invoked downstream — the amplitude is "just there," and readers won't notice the dependency without auditing to the axiom layer.

Everything below drills into specifics.

---

## 1. The foundational issue: Paper I Axiom 2

**Location:** Paper I, lines 179–182.

```
Axiom [Stochastic actualization]:
Among admissible candidates, one is selected stochastically according
to the quantum measure appropriate to the current potentia. The squared
modulus of the amplitude gives the probability, consistent with the Born rule.
```

**What this axiom does:**
1. Introduces an "amplitude" (unspecified domain, but downstream treated as complex-valued function).
2. Introduces the Born rule (probability = |amplitude|²).
3. Introduces "stochastic selection" of actualization events.

**What this axiom *doesn't* do:**
- Derive the amplitude form from DAG+BDG+LLC primitives.
- Specify why the amplitude is complex (as opposed to real, nonnegative, integer, or anything else).
- Derive the Born rule from anything more primitive.

**Apr 20 reading:** This is explicitly QM machinery imported as a foundational commitment. Every subsequent claim that uses amplitudes or probabilities inherits this import.

The honest way to describe RA under this reading is: RA is "DAG+BDG+LLC + [imported QM amplitude/Born-rule axiom]." The framework is not what it claims to be in Apr 20 language — there's a fifth pillar.

**What the papers do not currently say** but strict Apr 20 would require them to say: "The amplitude function and Born rule are imported from quantum mechanics as foundational axioms of RA, pending RA-native derivation. This is an open problem of the programme."

---

## 2. Stratum-A claims (fully RA-native, no issues)

These claims trace cleanly to DAG+BDG+LLC+Nature-measurements with no QM import:

**Paper I:**
- The seven axioms themselves (with the exception of Axiom 2, noted above)
- BDG score S(v,G) and its integer coefficients (1,−1,9,−16,8)
- The BDG acceptance kernel K(N|μ) as derived from growth rule + filter
- The four-level actualization hierarchy (excluding the Level-2 probability-weighted version that relies on Axiom 2)
- Δ S* ≈ 0.601 nats at μ=1 (computation-verified from BDG integers)
- c = ℓ_P/t_P from graph bandwidth
- Proper time = N_act · t_P (integer count)
- E = γmc² from actualization frequency
- Singularity termination via bandwidth saturation
- d=4 uniqueness via cross-dimensional criteria
- α_EM⁻¹ = 137 (Lean-verified, integer arithmetic) + 137.036 via Wyler + discrete acceptance probability
- α_s(m_Z) = 1/√72 (pure BDG integer arithmetic)
- Koide K = 2/3 (now proven via pure trig identity in `kval_ratio_two_thirds`)
- Antichain drift bound (statistical theorem about BDG filter)

**Paper II:**
- BDG topology types and confinement depths
- Quark/lepton mass cascade via BDG integers (m_p = m_P·α_EM⁵/2²⁸, etc.)
- Higgs mass m_H = 133 m_p, W mass, π mass, neutron mass
- Baryon-to-dark-matter ratio
- Regge trajectory structure
- Renewal motifs, stability
- Charge quantization in units of e/3
- Strong CP: θ_QCD = 0 exactly (from discrete vacuum, no topological sectors in DAG)

**Paper III:**
- Severance formalism (kernel saturation, boundary flux)
- Black hole entropy as discrete boundary law (severed-link count)
- LLC + graph cut theorem
- Antichain drift and spatial expansion
- Heat death prohibition via fragmentation
- Hubble tension prediction (parameter-free from f₀ and Ω_b)
- Apparent dark energy from Λ=0
- WIMP prohibition (categorical)

**Paper IV:**
- The complexity hierarchy
- Markov blankets and decoherence
- Causal firewall
- Universal decoherence timescale (bath identification)
- Assembly depth and assembly theory
- Origin-of-life sandwich bound
- Landauer's principle from causal DAG
- Maxwell's demon dissolved

**Evaluation:** This is the majority of the programme by volume. It's rigorously RA-native. If the Axiom 2 problem could be solved, this entire stratum is unaffected.

---

## 3. Stratum-B claims (depend on Axiom 2, currently mislabeled as native)

These are the places where Axiom 2's QM machinery flows into downstream claims. The papers mostly present them as RA-derivations without re-disclosing the Axiom 2 dependency.

### 3.1 Paper I §10 — Measurement problem "dissolved"

**Line 434:** "In RA, a quantum state is any state with ΔS(ρ||σ₀) below the actualization threshold ΔS*."
- The relative entropy ΔS formulation uses *quantum* relative entropy S(ρ||σ) = Tr[ρ(log ρ − log σ)], which requires ρ and σ to be density matrices. That's QM machinery.

**Line 436:** "The Schrödinger equation is the macroscopic approximation that applies when the actualization density is low..."
- Asserted, not derived. Claim is an RA-native derivation of Schrödinger, but no derivation appears in the paper. Status table line 700 labels this "DR" — but for this to be DR, the derivation chain needs to be explicit in the paper. It isn't.

**Line 440 — honest disclosure:** "The Born rule... is consistent with RA's quantum measure but is **not derived from it**. In RA, the Born rule is a constraint on the amplitude function (a(x) ∝ ψ(x)), not an additional postulate."
- This is candid but muddled. "Not derived from [RA's quantum measure]" is true. "Constraint on the amplitude function" is how Axiom 2 reads; "not an additional postulate" is technically true (it's part of Axiom 2) but rhetorically understates that Axiom 2 imports it.

**Line 445–451 — the Schrödinger derivation claim:**
```
The amplitude function a(x) at each vertex evolves by superposition of
contributions from all ancestors in the causal past.

In the low-density limit (μ ≪ 1), ... The amplitude at a candidate vertex
is linear in the ancestor amplitudes:
a(x) = Σ_{y ∈ past(x)} K(x, y) a(y)
where K(x, y) is the BDG vertex kernel. In the continuum limit, this
becomes a second-order partial differential equation of the Schrödinger
type. The Schrödinger equation is not primitive; it is the Level-2
statistical limit of the Level-1 discrete BDG dynamics.
```
- Linear superposition over ancestors is **assumed**, not derived. Why linear? Why not exponential, polynomial, or any other functional form? The answer is Axiom 2 — the amplitude-structure is axiomatic.
- "In the continuum limit, this becomes a Schrödinger-type PDE" — asserted. No derivation of the kernel K(x,y) from BDG primitives is shown. Whether K gives Schrödinger specifically (as opposed to some other PDE) depends on details that are not in the paper.

**Status table line 700:** `"Schrödinger eq. as low-μ limit & Continuum limit argument & DR"` — this labeling is too strong. "DR" means all steps explicit within RA. The steps here are not all explicit; the linearity and complex-valuedness of the amplitude are Axiom-2 imports.

**Honest relabeling would be:** `"Schrödinger eq. as low-μ limit | Sketch + Axiom 2 (Born rule import) | AR/conditional on Axiom 2 discharge"`.

### 3.2 Paper I §9.3 — Unruh via Rindler stationarity

**Lines 407–429 + Line 647:** The Rindler stationarity theorem depends on the `vacuum_lorentz_invariant` axiom (Poincaré invariance of the Minkowski vacuum).

**Good news:** This is *already* flagged as LV-conditional in both the Lean table and the status table, with explicit language: "Replacing `vacuum_lorentz_invariant` with an RA-native derivation from the BDG sprinkling limit is a known open target."

**Bad news (stale after Apr 21):** The papers reference `RA_AQFT_Proofs_v10.lean` as containing conditional Lean results. Per Apr 21 memory, the AQFT stage has been **retired** from the active Lean corpus (IC46 dissolved by retirement). The paper's Lean table is now inaccurate; the AQFT theorems are archival, not conditional-LV. The Unruh resolution claim, as currently written, appeals to Lean theorems that are no longer in the active build.

**Honest update needed:** Either re-derive Rindler stationarity without the AQFT stage (now that it's retired), or explicitly label the Unruh resolution as using archival Lean theorems that depend on imported QFT axioms.

### 3.3 Paper I §13 — Predictions ("BMV null," "spin-bath collapse")

**Line 660:** "Because the spacetime metric is updated only from actualized vertices, quantum superpositions cannot source a superposed gravitational field... RA predicts a strict null result."
- The prediction is RA-native *given* quantum superposition exists. But "superposition" is a QM concept inherited from Axiom 2. The null result is correctly derived from "unactualized → no gravitational source" (RA-native), but the existence of the premise (superposed mass before actualization) uses QM language.
- This is actually defensible: RA says "there are candidate states before they actualize." Call that superposition or candidacy, same thing. The null result follows from "candidates don't actualize gravity."
- The presentation could be cleaner: replace "superposition" with RA-native "unactualized candidate state" throughout.

**Line 670:** "Spin-bath collapse timescale t* ≈ 0.274/g."
- Uses QM spin-bath formalism as the environmental model. The prediction specifies a number (0.274) but the setup assumes quantum spins coupled via measured coupling g. This is in Stratum B — depends on importing QM to set the problem.

### 3.4 Paper II §7 — Gauge group identification

**Line 601 — honest disclosure:** "The Standard Model gauge group SU(3)×SU(2)×U(1) is identified in this paper, at the DR/PI level, with the product of two independent geometric structures... The identification is a **programme-level proposal, not a closed theorem chain** from BDG primitives to a fully derived gauge group."

**Line 653 — also honest:** "The identification of the Berry-phase structure with the continuum SU(3) gauge group is a **programme-level step (DR/PI), not a derivation at theorem level.**"

**Line 667 — also honest:** "the identification of that structure with the continuum Standard-Model gauge group is an **interpretive step (DR/PI), not a derivation from BDG primitives**..."

**Evaluation:** Paper II gets the honesty right here. The gauge group identification is repeatedly and correctly flagged as interpretive.

**Hidden Axiom 2 dependency:** The Berry-phase theorems themselves (lines 628–651) compute "Wilson loop eigenphases" for "rotations about axes in SU(2) Lie algebras." The mathematical structure of Wilson loops — `W = exp(i ∮ A·dx)` for connections A — is QM machinery. The "phase kicks" `ΔS_ij = c_j − c_i` are RA-native integers, but the assumption that they get **exponentiated as complex phases** (`exp(i·ΔS)`) to compute eigenphase observables like 0.806 rad is the exp(iS) issue in a different guise.

**Honest relabeling would add:** "The Berry-phase calculation assumes the standard QM machinery of unitary-matrix exponentiation of phase kicks. Under Axiom 2, this is imported; deriving it from DAG+BDG+LLC is an open target shared with the broader amplitude-form question."

### 3.5 Paper III abstract + §2 — Lorentz invariance

**Abstract (line 111):** "General relativity with Λ=0 follows from the RACL chain: the Local Ledger Condition (Lean-verified), amplitude locality (Lean-verified), the d=4 BDG closure theorem, and the Benincasa-Dowker continuum-limit result."
- "Amplitude locality (Lean-verified)" appeals to O01, which is the Lean theorem `bdg_amplitude_locality`. This theorem is about `bdg_amplitude := exp(I · bdg_increment)` — the Complex.exp amplitude. The Lean-verified locality is conditional on the amplitude form; it doesn't derive the amplitude.

**§2.3 (Line 205):** "Lorentz invariance as the continuum image of causal invariance (DR, conditional)"
- Labeled as "(DR, conditional)" — good.

**§2.3 scope limit (Line 214):** "the Lean chain currently inherits the `vacuum_lorentz_invariant` axiom and one live sorry in `RA_AQFT_Proofs_v10.lean` (the LQI adapter) from Paper I. The 'continuum Lorentz invariance is the causal invariance in continuum dress' reading is therefore a DR claim **conditional on those AQFT audit items**, not an unconditional dissolution."
- Honest disclosure. Good.

**§2.3 (Line 219):** "**Readers should not take this as an independent Lean-verified derivation of continuum Lorentz invariance from RA primitives.**"
- Excellent honest labeling.

**Stale-after-Apr-21 issue:** Same as Paper I §9.3. The AQFT stage is now retired, so the "conditional on AQFT audit items" framing needs updating. The items aren't "conditional" — they're archived.

### 3.6 Paper IV §10.3 — Spin-bath collapse timescale

**Line 387:** "For a quantum system coupled to a spin bath with externally measured coupling strength g, RA predicts a specific timescale for wave function collapse."
- Uses "quantum system," "wave function collapse" as given — inherits Axiom 2.
- Prediction itself uses RA-native ΔS* (Level-2 threshold crossing time). The bath is modeled with quantum spin machinery.

---

## 4. Stratum-C (already honestly flagged as conditional/programme-level)

These are the places the papers already disclose the gap honestly:

| Location | Claim | Status given in paper |
|---|---|---|
| Paper I §9.3, §13 table | Rindler stationarity → Unruh resolution | "LV (conditional†)" with explicit ⁺ footnote on CFC sorry + `vacuum_lorentz_invariant` axiom |
| Paper II §7 | SU(3)×SU(2)×U(1) identification | "DR/PI level, programme-level proposal" (repeated 3×) |
| Paper III §2.3 | Lorentz ← causal invariance | "(DR, conditional)" + explicit scope limits |
| Paper I §10.3 | D4U02 analytic closure | "Open" with stated path |
| Paper II §11 | Gauge coupling unification | Flagged as consequence of BDG topology, not SUSY-style unification |

**Evaluation:** These flags are well-done. They're what Stratum B claims *should* look like, too.

---

## 5. Stale references (Lean file naming, post-Apr-21)

**All four papers reference Lean files by their pre-rename names:**
- `RA_Koide.lean` (renamed to `RA_KvalRatio.lean` on Apr 21)
- `RA_Spin2_Macro.lean` (renamed to `RA_BDG_LLC_Kernel.lean` on Apr 21)
- `RA_BaryonChirality.lean` (content now in `RA_CausalOrientation_Core.lean`; original is archival)
- `RA_AQFT_Proofs_v10.lean` (retired to archival)

**All four papers reference SM-flavored identifiers in their Lean citations:**
- `koide_formula` (dropped in rename pass; now `kval_ratio_two_thirds`)
- `gluon` / `quark` confinement (now `sym_branch` / `asym_branch` filter horizons)

**Paper I §13 Lean table needs substantial rewrite** to match the current state. The "176+ theorems across 8 files" figure is also outdated (now 11 roots, ~190 theorems).

---

## 6. Consolidated findings

### Framing-discipline scorecard per paper

| Paper | Stratum-A content | Stratum-B content (unflagged) | Stratum-C content (flagged) | Axiom 2 dependency mentioned? |
|---|---|---|---|---|
| I (Kernel) | Most of §§1–8, 11–13 | §§9, 10, 13 (Unruh, measurement, BMV, spin-bath) | §§9.3, 10.3 explicitly | **No — Axiom 2 is stated but its downstream dependency isn't traced** |
| II (Matter) | Most of §§2–6, 9–11 | §7 Berry phase mathematical structure | §7 gauge group identification | No |
| III (Gravity) | Most of §§3–8, §§10–11 | §2 relies on O01 which relies on Axiom 2 | §2.3 Lorentz, §9 BMV | Partially — AQFT dependency flagged, Axiom 2 not |
| IV (Complexity) | Most of §§2–9, §§11–12 | §10.3 spin-bath prediction | Minor | No |

### The single most impactful honest relabeling

If you were to add *one* paragraph to Paper I, it would be (at Axiom 2 or in §10):

> **Scope of Axiom 2.** The stochastic actualization axiom imports the complex-amplitude function and the Born rule from quantum mechanics. These are not derived from the other six axioms. Any RA prediction that depends on the Born rule, wavefunction superposition, Schrödinger evolution, or complex-amplitude structure (including the BMV null, spin-bath collapse, Schrödinger as a low-density limit, and the Berry-phase gauge group identification in Paper II) inherits this import. Deriving Axiom 2 from DAG+BDG+LLC primitives is an open problem of the programme. RA with Axiom 2 is a well-defined framework; RA without Axiom 2 (i.e., from the other six axioms alone) does not currently close the QM-prediction side of the programme.

This single paragraph would relabel roughly half of Stratum B as appropriately-conditional, without requiring any mathematical changes to any paper.

### Secondary recommendations

1. Update all four papers' Lean references to the post-rename file names and identifier names.
2. Retire the AQFT-conditional framing in Paper I §9 and Paper III §2.3. Those aren't conditional — AQFT is archived. Either (a) re-derive the relevant results in the active native corpus, or (b) label the Unruh resolution and Lorentz-from-causal-invariance as "archival / pending RA-native reconstruction."
3. Relabel Schrödinger-as-low-μ-limit (Paper I §10) from "DR" to "AR conditional on Axiom 2" in the status table.
4. Add an explicit note to the Berry-phase programme (Paper II §7) that the Wilson-loop eigenphase computation uses standard QM unitary exponentiation.
5. Consider a short new paper or appendix dedicated to the Axiom 2 question: what would an RA-native derivation look like? Candidate approaches: (a) complex amplitudes as observer-accessible coarse-graining of classical DAG-transition probabilities (CSG-like), (b) derivation of Born rule from envariance-style arguments applied to DAG structure, (c) genuine open problem with no current approach. Honest programmatic labeling is a win regardless of which is true.

### What this audit does not question

- The *RA-nativity* of any Stratum-A claim.
- The *correctness* of any Stratum-B claim as a mathematical consequence of Axiom 2 + the other axioms.
- The *empirical adequacy* of any prediction — BMV null, interference patterns, etc. are consistent with observations, and this audit doesn't touch that.

This audit is strictly about the *framing* of the programme under Apr 20 discipline: what's derived from native primitives vs. what's imported and threaded through as an axiom.

---

## 7. Final assessment

Under a strict Apr 20 reading, the programme's framing-discipline status is:

- **Stratum A** (most of the programme by content): compliant.
- **Stratum B** (QM-prediction side): non-compliant *as currently labeled*. Would become compliant with honest labeling of the Axiom 2 dependency.
- **Stratum C** (already flagged): compliant — the existing flags are the right pattern.

**The programme is closer to Apr 20 compliance than I expected when we started the session.** The non-QM microphysics (most of Paper II's mass/coupling results, Paper III's severance/entropy/cosmology, Paper IV's complexity) is genuinely RA-native. The QM-side is where the remaining work is, and it's concentrated in identifiable places.

**The practical path to "honest Apr 20 compliance" is not a content rewrite.** It's:
1. The Axiom 2 disclosure paragraph above.
2. Relabeling of ~6–8 specific Stratum-B claims in the status tables.
3. An update to Lean references after Apr 21's renames.
4. A decision on how to handle the (now archival) AQFT-conditional claims.

None of this requires new math or new derivations. It's labels and Lean citations.

**The substantive research question** — deriving Axiom 2 from the other six — remains open, as you said. This audit doesn't advance that; it makes explicit what the open problem implies for everything currently in print.

---

*End of audit. Total read time: ~45 minutes. All line references are to the April 2026 4-paper TeX files at /mnt/user-data/uploads/.*
