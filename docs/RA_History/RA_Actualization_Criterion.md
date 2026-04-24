# The Actualization Criterion
## Necessary Structure, Nontriviality, and Discrete Realization
### Joshua F. Sandeman · April 2026

---

## 1. The problem this note solves

Relational Actualism claims that not every physical interaction becomes a
permanent event — that there is a genuine, nontrivial threshold separating
reversible quantum possibility from irreversible causal fact. This is
Kernel Axiom D: *only candidates crossing a nontrivial irreversibility
threshold become actual.*

The framework has stated this criterion in multiple ways across the paper
suite, and those statements are not all equivalent:

**Statement A (too weak):** "An interaction actualizes when it produces
ΔS(ρ‖σ₀) > 0 with respect to the vacuum reference state."

**Statement B (perturbative implementation):** "On-shell boson emission
satisfying p^μ p_μ = m²c² is sufficient for actualization."

**Statement C (the discrete criterion):** "A candidate vertex actualizes
when its BDG score S_BDG = 1 − N₁ + 9N₂ − 16N₃ + 8N₄ > 0."

Statement A is **trivially satisfied** for almost any non-vacuum state.
Any state locally distinguishable from the vacuum has S(ρ‖σ₀) > 0 by
definition. This was correctly identified as a fatal flaw by external
review.

Statement B is a valid perturbative implementation but is neither
fundamental nor general — it breaks down in strongly coupled regimes.

Statement C is the actual criterion. It is non-trivial (P_acc ≈ 0.548,
meaning ~45% of candidates are rejected), discrete, computable, and
well-defined. But it has not been presented as the primary criterion
in the foundational paper (RAQM), which instead emphasizes Statement A.

This note establishes the correct hierarchy and makes the criterion
rigorous.

---

## 2. What the criterion must satisfy

Any viable actualization criterion for RA must satisfy five conditions:

### 2.1 Nontriviality
The criterion must reject a significant fraction of candidate events.
If everything actualizes, the framework collapses to standard unitary
evolution with no measurement problem dissolution.

### 2.2 Discreteness
The criterion must be well-defined on the discrete causal graph — the
primitive ontological structure. Continuum formulations are approximations
to the discrete criterion, not the other way around.

### 2.3 Locality
The criterion must depend only on the local causal neighborhood of the
candidate vertex. Global information about the graph must not be required.
(This is amplitude locality, O01, Lean-verified.)

### 2.4 Covariance
The criterion must be independent of the linear extension (temporal
ordering) of the causal partial order. Different observers must agree on
which events actualize. (This is causal invariance, O02, Lean-verified.)

### 2.5 Record formation
The criterion must ensure that actualized events leave a permanent,
redundant causal record — one that cannot be erased by subsequent
dynamics.

---

## 3. The discrete criterion (fundamental)

### 3.1 Definition

Let G = (V, ≺) be the current causal DAG. A candidate vertex v proposes
to extend G by adding new causal relations to existing vertices.

The BDG action scores the candidate's local causal neighborhood:

    S_BDG(v) = c₀ + c₁N₁ + c₂N₂ + c₃N₃ + c₄N₄

where N_k counts the number of elements in the causal past of v with
exactly k−1 intervening elements, and (c₀,c₁,c₂,c₃,c₄) = (1,−1,9,−16,8)
are the BDG integers for d=4 (uniquely fixed by O14, Lean-verified).

**The actualization criterion:** Vertex v actualizes if and only if

    S_BDG(v) > 0.

If S_BDG(v) ≤ 0, the candidate is rejected. No vertex is written.
The interaction remains virtual — part of the quantum possibility
layer (Level 2 of the Engine of Becoming) but not part of the
actualized causal record (Level 1).

### 3.2 Nontriviality

At the Planck density μ = 1, the BDG score is a random variable:

    S = 1 − N₁ + 9N₂ − 16N₃ + 8N₄

where N_k ~ Pois(μ^k/k!) independently. The acceptance probability is:

    P_acc(μ=1) = P(S > 0) = 0.54844    [CV: exact enumeration]

This means **45.2% of candidate vertices are rejected**. The filter
is genuinely selective. This is not a rubber stamp — it is a filter
that rejects nearly half of all proposed events at the operating
density of the universe.

The per-vertex entropy cost of actualization is:

    ΔS* = −log P_acc(1) = 0.60069 nats   [CV: certified bounds]

This is the "price of becoming real" — the information-theoretic cost
of crossing from possibility into actuality.

### 3.3 Why S_BDG > 0 is not trivially satisfied

Unlike S(ρ‖σ₀) > 0 (which holds for any non-vacuum state), the BDG
criterion S_BDG > 0 has genuine structure:

**Negative BDG coefficients matter.** The coefficients c₁ = −1 and
c₃ = −16 are large and negative. A candidate with many depth-1 or
depth-3 ancestors is actively penalized. Virtual processes — those
producing off-shell mediators that connect to many nearby vertices
without propagating to the asymptotic environment — tend to have
high N₁ and N₃ counts, driving S_BDG negative. This is not an
accident; it is a structural consequence of inclusion-exclusion
counting in 4D causal geometry.

**Concrete examples:**
- Baseline: N = (0,0,0,0), S = 1. This fixes the score normalization;
  it does not imply spontaneous ledger inscription in the absence of a
  candidate interaction. A vertex is only proposed when an interaction
  occurs — the baseline score merely confirms that the BDG action is
  calibrated so that isolated events are admissible.
- W/Z boson: N = (1,0,0,0), S = 0. Marginal — exactly at threshold.
- Photon: N = (1,1,0,0), S = 9 > 0. Actualizes freely.
- Gluon vertex: N = (1,2,0,0), S = 18 > 0. Actualizes strongly.
- Dense virtual: N = (3,1,1,0), S = 1−3+9−16 = −9 < 0. Rejected.
- Deeply connected: N = (2,0,2,0), S = 1−2−32 = −33 < 0. Rejected.

The BDG filter is a genuine discriminator between interactions that
produce permanent causal records and those that remain virtual.
The filter is evaluated only on physically proposed candidate
vertices — interactions that actually occur — not on arbitrary
formal local patterns of the graph.

### 3.4 What "virtual" means in RA

A virtual process is one for which S_BDG ≤ 0. It contributes to
quantum amplitudes (Level 2) but does not write a vertex to the
causal graph (Level 1). Virtual processes are real in the quantum
sense — they affect scattering amplitudes, the Lamb shift, the
Casimir effect. But they are not actual in the causal sense — they
leave no permanent record and they do not source the gravitational
field.

This is the RA-native dissolution of the vacuum energy problem:
virtual processes have S_BDG ≤ 0, therefore P_act projects them out
of the metric source, therefore the vacuum does not gravitate,
therefore Λ = 0 structurally.

### 3.5 Why positive BDG score is the discrete signature of record-forming irreversibility

The connection between S_BDG > 0 and irreversible record formation
is not merely definitional. It has structural content:

**Negative BDG coefficients penalize locally reabsorbable structure.**
The coefficients c₁ = −1 and c₃ = −16 penalize vertices with many
depth-1 and depth-3 ancestors. These are precisely the configurations
where the candidate vertex is deeply embedded in a dense local
neighborhood — connected to many nearby vertices, with many
intervening elements. Such configurations are characteristic of
short-range virtual exchanges that can be reabsorbed by the local
environment without propagating outward.

**Positive BDG coefficients reward causally exportable structure.**
The coefficients c₂ = +9 and c₄ = +8 reward vertices with depth-2
and depth-4 ancestors. These correspond to configurations where the
candidate vertex connects to the graph through extended causal chains
that reach beyond the immediate neighborhood. Such configurations are
characteristic of on-shell processes that propagate information to
the asymptotic environment — precisely the processes that form
permanent records.

**The sign alternation is forced by inclusion-exclusion.** The
alternating sign pattern (+,−,+,−,+) is not a design choice. It is
a mathematical consequence of inclusion-exclusion counting on causal
intervals in 4D. The BDG integers encode the geometry of the causal
diamond, and that geometry naturally distinguishes locally confined
processes (penalized) from causally propagating processes (rewarded).

**Therefore:** S_BDG > 0 selects for precisely those interactions
whose causal structure extends beyond the local neighborhood — i.e.,
those that form permanent, non-reabsorbable records. S_BDG ≤ 0
selects for locally confined, reabsorbable processes — i.e., virtual
exchanges. The BDG filter is not an arbitrary accept/reject rule
grafted onto the ontology. It is the discrete geometric criterion
for whether an interaction's causal footprint is exportable (actual)
or confinable (virtual).

---

## 4. The continuum translation (approximate)

In the dense-graph regime (μ >> 1), the discrete BDG criterion admits
an effective continuum translation. This is an approximation to the
fundamental discrete filter, not a replacement for it.

### 4.1 From S_BDG > 0 to ΔS > ΔS*

In the continuum approximation, the BDG score S_BDG maps onto a
relative entropy increment. The acceptance probability P_acc defines
a threshold ΔS* = −log P_acc ≈ 0.601 nats. An interaction actualizes
when the relative entropy increment exceeds this threshold:

    ΔS ≡ S(ρ_post‖σ₀) − S(ρ_pre‖σ₀) > ΔS*

This increment threshold is an effective dense-regime representation
of the discrete BDG filter, not a replacement for it.

Note: this is an **increment** condition (ΔS = S_post − S_pre), not
a static positivity condition (S > 0). The increment formulation
avoids the triviality problem because ΔS = 0 for any process that
does not change the system's distinguishability from vacuum.

### 4.2 Why ΔS (increment) is non-trivial when S (absolute) is trivial

The absolute relative entropy S(ρ‖σ₀) is positive for any non-vacuum
state. But the **increment** ΔS = S_post − S_pre is zero for:

- Elastic scattering (state changes but distinguishability doesn't)
- Virtual exchange (no environmental record formed)
- Stationary thermal baths (the Rindler/Unruh case: L05, Lean-verified)
- Reversible unitary evolution (no entropy production)

The increment ΔS is positive only when the interaction produces
genuinely new environmental distinguishability — i.e., when it forms
an irreversible causal record. This is the continuum translation of
the discrete S_BDG > 0 condition.

### 4.3 The perturbative regime

In weakly coupled QFT, ΔS > ΔS* coincides with the on-shell condition
p^μ p_μ = m²c². An on-shell boson propagates to the asymptotic
environment, creates orthogonal environmental states, and generates
ΔS > 0. An off-shell (virtual) boson does not propagate, does not
create environmental orthogonality, and generates ΔS = 0.

The on-shell condition is therefore a **sufficient** perturbative
implementation of the general criterion, not the criterion itself.

### 4.4 The strongly coupled regime

In strongly coupled regimes (QCD, condensed matter), the quasi-particle
picture breaks down. There are no cleanly identifiable on-shell bosons.
The criterion reverts to its fundamental discrete form: S_BDG > 0 for
each candidate vertex. The continuum translation ΔS > ΔS* provides
the effective description, with ΔS computed from the environmental
entanglement structure rather than from individual boson emission.

---

## 5. The hierarchy of formulations

The correct hierarchy, from fundamental to approximate, is:

### Level 0 (fundamental, discrete):
    S_BDG(v) > 0
    on the growing causal DAG
    [Status: well-defined, non-trivial (P_acc = 0.548)]

### Level 1 (continuum translation):
    ΔS(ρ_post‖σ₀) − S(ρ_pre‖σ₀) > ΔS* = 0.601 nats
    [Status: approximation to Level 0 in dense regime]

### Level 2 (perturbative implementation):
    p^μ p_μ = m²c² (on-shell condition)
    [Status: sufficient condition in weakly coupled QFT]

### Level 3 (informal):
    "irreversible environmental entanglement"
    [Status: physically correct but not mathematically precise]

The papers should present this hierarchy explicitly. RAQM should state
Level 0 as the fundamental criterion and Levels 1–3 as successive
approximations, not the other way around.

---

## 6. Why naïve entropy positivity (Statement A) fails

For the record, here is the explicit failure mode:

Statement A says: "Actualize when S(ρ‖σ₀) > 0."

Consider an electron elastically scattered by a proton. After scattering,
the electron has a different momentum. Its state ρ_post ≠ σ₀, so
S(ρ_post‖σ₀) > 0. But if no real photon was emitted — if the exchange
was entirely virtual — no environmental record was formed, no vertex
should be written, and no actualization should occur.

Statement A would incorrectly actualize this virtual process.

The BDG criterion handles this correctly: a virtual exchange at short
range typically has high N₁ (many depth-1 ancestors), driving S_BDG
negative. The candidate is rejected. The virtual process remains in
the possibility layer.

The increment formulation (Level 1) also handles it: ΔS = S_post − S_pre
= 0 for elastic scattering with no photon emission, because the
system-environment distinguishability has not changed.

---

## 7. Connection to the kernel axioms

The actualization criterion connects to the kernel as follows:

**Kernel D** (nontrivial threshold): Realized by S_BDG > 0, with
P_acc = 0.548 quantifying the rejection rate.

**Kernel B** (irreversible inscription): Realized by the irreversibility
of DAG vertex addition. Once written, a vertex cannot be removed.
The LLC (L01) ensures conservation at the new vertex.

**Kernel C** (weighted possibilities): Realized by the quantum measure
on candidate extensions (Level 2 of the Engine of Becoming). Candidates
with S_BDG ≤ 0 contribute to amplitudes but not to the actualized graph.

**Closure Row 6** (from the spine): The abstract kernel principle
"nontrivial threshold exists" is closed by the concrete BDG filter
with P_acc = 0.548 and ΔS* = 0.601 nats.

---

## 8. What this note establishes

1. The fundamental actualization criterion is **S_BDG > 0** on the
   discrete causal graph — not S(ρ‖σ₀) > 0 in the continuum.

2. This criterion is **non-trivial**: it rejects ~45% of candidates.

3. The continuum translation is an **increment** condition
   (ΔS = S_post − S_pre > ΔS*), not a static positivity condition.

4. The on-shell condition is a **perturbative sufficient condition**,
   not the fundamental criterion.

5. The hierarchy is: discrete BDG → continuum increment → perturbative
   on-shell → informal "irreversible entanglement."

6. The naïve formulation (Statement A) is trivially satisfied and must
   not be used as the primary statement of the criterion.

---

## 9. Implications for RAQM revision

The revised RAQM should:

- State the BDG filter as the fundamental criterion in the abstract
- Present the hierarchy explicitly (§5 of this note)
- Use the increment formulation (ΔS > ΔS*) for continuum discussion
- Present on-shell emission as a perturbative sufficient condition
- Include the "elastic scattering" counterexample (§6) to demonstrate
  why naïve positivity fails
- Cross-reference this note and the BDG calculator on the Graph page

This substantially resolves the highest-priority conceptual vulnerability
in the framework.

---

*Technical note produced April 9, 2026.*
*This document addresses Pressure Point 1 of the Kernel vs Implemented RA
analysis and directly responds to the external review critique of §2.1.*
