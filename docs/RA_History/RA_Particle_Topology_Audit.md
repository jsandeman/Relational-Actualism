# From Topology Classes to Particle Classes
## What L11 Proves, What the Mapping Adds, and Where the Line Falls
### Joshua F. Sandeman · April 2026

---

## 1. The claim under scrutiny

RA claims that the five stable BDG topology types in 4D correspond
exactly to the five particle classes of the Standard Model. This is
the particle-topology bridge — one of the framework's most distinctive
claims and one of the most important to get right.

---

## 2. What L11 actually proves (Lean-verified)

The BDG Closure Theorem (L11) is proved in RA_D1_Proofs.lean across
124 single-step extension cases with zero sorry tags.

### 2.1 The formal statement

In 4D BDG dynamics, every single-step extension of the causal graph
falls into one of exactly five topologically distinct stability classes.
No sixth class exists. The classification is exhaustive.

### 2.2 What "stable" means

A BDG pattern is stable if it has S_BDG > 0 (passes the actualization
filter) and its topology is preserved under further graph extensions.
Stability is a property of the local causal neighborhood structure,
not of any externally imposed particle label.

### 2.3 What the five types are (formally)

The five classes are distinguished by their BDG depth profile
(N₁, N₂, N₃, N₄) and the topology of their causal past:

| Type | Depth profile | BDG score | Causal past topology |
|------|--------------|-----------|---------------------|
| 1 | High N₁, N₂ | Positive (confined) | Sequential + branching |
| 2 | High N₁, moderate N₂ | Positive (confined) | Sequential chain |
| 3 | Low N₁, moderate N₂ | Positive (free) | Simple past |
| 4 | Moderate depth-2 | Positive (scalar) | Symmetric past |
| 5 | Minimal depth | Positive (chiral) | Minimal past |

### 2.4 Supporting Lean results

- **D1a (sequential fixed points):** The chain score stabilizes at
  depth k ≥ 4. No new stability classes appear beyond depth 4.
- **D1b (minimal patterns):** Symmetric and asymmetric Y-join scores
  are computed exactly.
- **D1c (confinement):** L_g = 3, L_q = 4 (L10, Lean-verified).
- **D1_closure_complete:** All 124 single-step extensions classified.

**Status: All Lean-verified, zero sorry.**

---

## 3. The physical identification (interpretive)

This is where the mapping from topology to physics occurs.

### 3.1 The proposed correspondence

The following table presents the current best mapping from BDG
topology types to Standard Model particle classes. These are
**mapping proposals** — systematic and internally consistent, but
not yet theorem-level identifications.

| BDG Type | Proposed SM identity | Key supporting property |
|----------|---------------------|-------------|
| Type 1 | Quarks | 3-colour (N₁=2 gives 3 configs), confined (L_q=4) |
| Type 2 | Gluons | 3-colour (N₁=2), confined (L_g=3), self-interacting |
| Type 3 | Gauge bosons (γ,W,Z) | Free propagation, depth-1 structure |
| Type 4 | Higgs | Scalar, depth-2 dominant, S=0 marginal for W/Z |
| Type 5 | Leptons + neutrinos | Minimal BDG depth, chiral |

### 3.2 What supports the identification

Each identification is supported by multiple structural correspondences:

**Quarks (Type 1):**
- N₁ = 2 degeneracy → exactly 3 distinct causal configurations → 3 colour charges [CV]
- Confinement length L_q = 4 → finite range [LV]
- Sequential causal past → fermion-like propagation [structural]

**Gluons (Type 2):**
- Same N₁ = 2 structure as quarks → carry colour [CV]
- Shorter confinement L_g = 3 → self-interacting, shorter range [LV]
- No asymptotic states → confined [LV]

**Gauge bosons (Type 3):**
- Free propagation (S > 0 without confinement) → infinite range [structural]
- W/Z: S(1,0,0,0) = 0 exactly → marginal, massive [LV: integer identity]
- Photon: S(1,1,0,0) = 9 → freely actualizing, massless [LV: integer identity]

**Higgs (Type 4):**
- Scalar topology → spin-0 [structural]
- Depth-2 dominant → couples to the background actualization density [structural]
- RA-native Higgs mechanism: depth-2 dressing of marginal vertices [interpretation]

**Leptons (Type 5):**
- Minimal BDG depth → simplest stable pattern [structural]
- Chiral structure from DAG acyclicity → maximal parity violation [LV: D3]
- No colour charge → no confinement [structural]

### 3.3 What makes the identification systematic

The mapping is not ad hoc. It follows a consistent rule: the BDG
depth profile determines the interaction structure, and the
interaction structure determines the particle identity. Specifically:

- Depth-1 structure → electroweak coupling
- Depth-2 structure → electromagnetic/Higgs coupling
- Depth-3/4 structure → strong coupling
- Confinement length → free vs. confined
- N₁ degeneracy → colour multiplicity

This is a **systematic structural correspondence**, not a free
assignment of labels. Changing any identification would break the
internal consistency of the mapping.

---

## 4. Where the line falls

### 4.1 What is theorem-level

- Five and only five stable topology types exist in 4D [LV]
- Confinement lengths are L_g=3, L_q=4 [LV]
- The closure is exhaustive over 124 extensions [LV]
- The chain score stabilizes at depth ≥ 4 [LV]
- W/Z marginal score S=0, photon score S=9 [LV: integer identity]
- Chirality from DAG acyclicity [LV: D3, 13 theorems]
- Baryon number exactly conserved [LV: D3]

### 4.2 What is computation-verified

- N₁=2 gives exactly 3 causal configurations (colour) [CV]
- Conditional ancestor counts biased by BDG sign [CV]
- All BDG scores for named particle configurations [CV]

### 4.3 What is interpretive

- "Type 1 = quarks" (vs. some other confined coloured fermion)
- "Type 3 = gauge bosons" (vs. some other free boson)
- "Type 5 = leptons" (vs. some other chiral minimal-depth fermion)
- The Higgs identification as depth-2 background dressing
- The claim that five types EXHAUST the SM (i.e., that no SM particle
  falls outside these five types and no BSM particle fits inside them)

### 4.4 What is open

- Why exactly the SM quantum numbers (hypercharge, isospin assignments)
  emerge from the BDG depth profiles
- Whether the three-generation structure is forced or merely compatible
- Whether the full interaction vertex structure (QED/QCD/weak vertices)
  follows from the BDG topology or requires additional input
- The spin-statistics connection in the discrete framework

---

## 5. The exhaustiveness question

The strongest form of the claim is: "No BSM particles of new types
are possible — their topology does not exist."

### 5.1 What this means precisely

L11 proves that no sixth stable topology class exists in 4D under
single-step BDG extensions. Any proposed BSM particle must belong
to one of the five existing types.

### 5.2 What this does and does not exclude

**Excluded:** New particles with novel BDG topology (e.g., a
particle that is neither quark-like, gluon-like, gauge-boson-like,
Higgs-like, nor lepton-like in its causal structure).

**Not excluded by L11 alone:** Additional particles WITHIN existing
topology types (e.g., a fourth generation of quarks, additional
Higgs bosons, heavy leptons). These would share the topology of
existing particles but differ in mass or quantum numbers.

**Excluded by other RA results:** A fourth generation is excluded
by the SU(3)_gen generation structure (three BDG excitation levels
in d=4). Additional Higgs bosons are excluded by the RA-native Higgs
mechanism (the depth-2 background has one collective mode).

### 5.3 Honest summary

L11 proves: the topology universe is closed (five types, no more).
The full BSM exclusion requires L11 + generation closure + Higgs
uniqueness — a combination of Lean-verified and interpretive results.

---

## 6. The honest summary table

| Aspect | Status |
|--------|--------|
| Five stable topology types in 4D | **Lean-verified** (L11) |
| Exhaustive over 124 extensions | **Lean-verified** |
| Confinement lengths L_g=3, L_q=4 | **Lean-verified** (L10) |
| Chirality from acyclicity | **Lean-verified** (D3) |
| Baryon conservation exact | **Lean-verified** (D3) |
| W/Z marginal, photon free | **Lean-verified** (integer identities) |
| 3 colours from N₁=2 | **Computation-verified** |
| Type 1 = quarks, etc. | **Interpretive mapping** |
| Five types = full SM | **Interpretive** (systematic, not arbitrary) |
| No BSM topologies | **Lean-verified** (L11) |
| No fourth generation | **Interpretive** (SU(3)_gen) |
| Full interaction vertices | **Open** |
| Spin-statistics | **Open** |

---

## 7. Recommended language

### What RA should say:

"The BDG closure theorem (Lean-verified) establishes that exactly five
topologically distinct stable pattern classes exist in 4D. These
classes exhibit structural properties — confinement, colour multiplicity,
chirality, mass hierarchy — that correspond systematically to the five
particle classes of the Standard Model. The identification is not
arbitrary: it follows a consistent rule linking BDG depth profile to
interaction structure. The full derivation of SM quantum numbers and
interaction vertices from BDG topology remains an active target."

### What RA should not say:

"The Standard Model particle spectrum is derived from BDG topology."

The topology classification IS derived. The SM identification is a
systematic interpretive mapping built on that classification.

---

*Technical audit note produced April 9, 2026.*
*Addresses Priority 4 of the ChatGPT assessment (particle-topology
mapping language).*
