# The GR Bridge
## What Is Lean-Backed, What Is Published, What Is Derived, and What Is Interpretive
### Joshua F. Sandeman · April 2026

---

## 1. The claim

RA derives Einstein's field equations G_μν = 8πG P_act[T_μν] with
Λ = 0 and no free parameters, via two independent routes:

- **Route 1 (Lovelock chain):** LLC → P_act conservation → BDG
  locality → Benincasa-Dowker → Lovelock → EFE
- **Route 2 (RA-native BDG uniqueness):** L01 + O01 + L11 →
  Benincasa-Dowker → EFE → Bianchi = LLC

Both arrive at the same unique field equation. This is the strongest
physics-bridge result in the framework.

---

## 2. Route 1: The Lovelock chain (RACL Theorem 5.1)

### Step A: Local Ledger Condition
At every vertex of the growing DAG, incoming and outgoing conserved
quantities balance: Σ_out(v) = Σ_in(v).

**Status: Lean-verified (L01).** Zero sorry. This is the discrete
conservation primitive.

### Step B: P_act conservation theorem
In the continuum limit, the actualization projector P_act preserves
the covariant divergence: ∇_μ P_act[T^μν] = 0.

**Status: Derived (proved in RACL).** This is an RA-original result.
It bridges discrete LLC to continuum conservation.

### Step C: Benincasa-Dowker continuum limit
In the dense-sprinkling limit, the expectation value of the BDG
action converges to the Einstein-Hilbert action:
⟨S_BDG⟩ → (l_P²/4) R.

**Status: Published theorem (CQG 2010, peer-reviewed).** This is
the key external result in the chain. It is not RA-specific — it
belongs to the causal set theory community.

### Step D: Lovelock uniqueness
In 4D, the unique divergence-free, symmetric, second-order tensor
built from the metric and its first and second derivatives is
H_μν = αG_μν + Λg_μν.

**Status: Published theorem (1971, textbook result).**

### Step E: Vacuum suppression
The actualization projector P_act projects out vacuum contributions
from the stress-energy source. Virtual particles have S_BDG ≤ 0 and
therefore do not contribute to P_act[T_μν]. Consequently Λ = 0 —
the cosmological constant vanishes structurally, not by cancellation.

**Status: Derived (proved in RAGC).** RA-original result. Depends
on the actualization criterion (Pressure Point 1, now resolved by
the Actualization Criterion audit note).

### Step F: BDG locality lemma
The BDG action gives a second-order curvature surrogate, consistent
with the Lovelock second-derivative requirement.

**Status: Derived (proved in RACL).** RA-original result.

### Step G: Assembly
Combining A–F: the unique consistent macroscopic field equation is

    G_μν = 8πG P_act[T_μν]

with Λ = 0 and no free parameters.

**Status: Derived.** The assembly is RA-original. It uses three
external published results (Rideout-Sorkin, Benincasa-Dowker,
Lovelock) and four RA-original contributions (LLC, P_act
conservation, BDG locality, vacuum suppression).

### Remark (what is proved vs imported)
RACL Remark 5.2 explicitly documents: "Three imported published
results: Rideout-Sorkin, Benincasa-Dowker, Lovelock. RA-original
contributions: LLC (Lean), P_act conservation (proved here), BDG
locality (proved here), vacuum suppression (proved in RAGC)."

---

## 3. Route 2: The RA-native BDG uniqueness chain

### Step 1: L01 (LLC) — Lean-verified
### Step 2: O01 (amplitude locality) — Lean-verified, zero sorry
### Step 3: L11 (d=4 BDG closure) — Lean-verified, 124 cases

### Step 4: Benincasa-Dowker uniqueness
The BDG action is the unique local causal-set action in d=4, under
the Benincasa-Dowker closure conditions, whose continuum limit is
the Einstein-Hilbert action ⟨S_BDG⟩ → (l_P²/4) R.

**Status: Published theorem.**

### Step 5: Variation of EH → field equations
Standard variational calculus: δ(EH action) = 0 → G_μν = 8πG T_μν.

### Step 6: LLC on source → ∇_μ T^μν = 0

### Step 7: ∇_μ G^μν = 0 (Bianchi identity)

**The chain:**
L01 + O01 + L11 → BDG uniqueness (BD 2010) → ⟨S_BDG⟩ = (l_P²/4)R
→ variation → G_μν = 8πG P_act[T_μν] → LLC on source → ∇_μT = 0
→ ∇_μG = 0.

---

## 4. The Bianchi = LLC insight

In standard GR, the geometric Bianchi identity ∇_μG^μν ≡ 0 and
matter conservation ∇_μT^μν = 0 are mysteriously compatible —
they must hold simultaneously but seem to come from different sources
(geometry vs. physics).

In RA, they are **the same conservation law** — the LLC — at
different levels of description. The discrete LLC (L01) manifests as
∇_μT = 0 in the matter sector and as ∇_μG = 0 in the geometry
sector. There is no mystery of compatibility because there is only
one conservation law.

**Status: Interpretive synthesis.** The formal ingredients are proved
(LLC, field equations, Bianchi). The identification of Bianchi with
LLC at a different scale is an interpretive reading of the formal
structure — deeply motivated but not itself a theorem.

---

## 5. The ingredient status table

| Ingredient | Source | Status |
|-----------|--------|--------|
| LLC (Σ_out = Σ_in) | L01 | **Lean-verified** |
| Amplitude locality | O01 | **Lean-verified** |
| Causal invariance | O02 | **Lean-verified** |
| d=4 BDG closure | L11 | **Lean-verified** |
| P_act conservation | RACL | **Derived** (RA-original) |
| BDG locality lemma | RACL | **Derived** (RA-original) |
| Vacuum suppression | RAGC | **Derived** (RA-original) |
| Benincasa-Dowker | CQG 2010 | **Published theorem** |
| Lovelock uniqueness | 1971 | **Published theorem** |
| Rideout-Sorkin covariance | 2000 | **Published theorem** |
| Assembly → G_μν = 8πG P_act[T] | RACL | **Derived** |
| Bianchi = LLC | RACL | **Interpretive synthesis** |

---

## 6. What would make this airtight

### 6.1 Lean-formalize the Benincasa-Dowker theorem

The single non-LV link in the otherwise Lean-verified Route 2 chain
is the Benincasa-Dowker continuum limit theorem. A Lean formalization
would make the entire GR derivation machine-checked from discrete
axioms to Einstein's equations. This is a long-term target — it
requires formalizing Poisson point process theory in Lean, which is
not currently available in Mathlib.

### 6.2 Derive the P_act conservation theorem in Lean

P_act conservation is proved on paper in RACL but not yet formalized
in Lean. A Lean proof would upgrade Route 1 Step B from "Derived"
to "Lean-verified."

### 6.3 Close the curved-background Bianchi identity

D04 (Bianchi identity from LLC) is currently proved in flat/weak-field
limit. The extension to curved backgrounds requires type III₁ AQFT
(Tomita-Takesaki theory). This has been dissolved as a problem (the
discrete LLC IS the Bianchi identity in continuum costume, so no
separate curved-background proof is needed), but the dissolution
itself is interpretive rather than theorem-level.

---

## 7. Separating the GR bridge from cosmological departures

### 7.1 The bridge (strong)

The claim "GR emerges as the unique macroscopic limit" is the
strongest physics result in the framework. It uses:
- 4 Lean-verified discrete inputs
- 3 published external theorems
- 3 RA-original derived results
- Zero free parameters

### 7.2 The departures (mixed)

Where RA departs from standard GR:

| Departure | Status | Notes |
|-----------|--------|-------|
| Λ = 0 structurally | **Derived** | From vacuum suppression |
| Dark matter as topology | **Derived** (RADM) | BDG bandwidth partition |
| Hubble tension from baryon density | **CV** | Parameter-free, testable |
| Kerr nucleation / axis of evil | **Derived** (RAGC) | New, 4 predictions |
| Event horizons as graph cuts | **Derived** | From L02 |
| Sparse-regime departures | **Argued** | Where P_act ≠ 1 |

The departures range from strong (Λ = 0) to argued (sparse-regime
details). They should be presented as a separate downstream layer,
not conflated with the GR bridge itself.

### 7.3 Why this separation matters

The GR bridge is one of RA's most credible achievements. If weaker
cosmological claims (e.g., specific Hubble values, dark matter
fractions) are presented in the same breath, skeptics may use
uncertainty about the departures to dismiss the bridge. The bridge
should stand on its own.

---

## 8. Recommended language

### What RA should say:

"The Einstein field equations with Λ = 0 are derived as the unique
macroscopic limit of the BDG-filtered actualization graph, via two
independent routes — one using Lovelock's uniqueness theorem, one
using BDG uniqueness directly. Both routes combine Lean-verified
discrete inputs with published causal-set theorems and RA-original
derivational steps. No free parameters appear. The Bianchi identity
and matter conservation are identified as the same conservation law
(the LLC) at different scales."

### What RA should not say:

"GR is fully derived in Lean."

The discrete inputs are Lean-verified. The continuum bridge
(Benincasa-Dowker) is a published external theorem. The assembly is
derived on paper. The full chain is not machine-checked end-to-end.

---

*Technical audit note produced April 9, 2026.*
*Addresses Priority 6 of the ChatGPT assessment (GR bridge audit)
and the Four Artifacts request for the cleanest GR bridge derivation.*
