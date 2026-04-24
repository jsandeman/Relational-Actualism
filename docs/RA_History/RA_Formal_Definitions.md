# RA Sequential Growth: Formal Definitions
## For External Review (ChatGPT)
### Joshua F. Sandeman · Claude (Opus 4.6) · April 12, 2026

---

## Purpose

This document provides precise formal definitions of the objects
in RA's sequential growth dynamics. It is intended to enable
rigorous external assessment of claims about severance, expansion,
and the bimodal phase transition.

---

## 1. The Causal Graph G

**Definition 1 (Causal Graph).** G = (V, ≺) is a locally finite
partially ordered set (poset) where:
  - V is a countable set of **vertices** (actualization events)
  - ≺ is a strict partial order on V satisfying:
    (a) **Irreflexivity:** v ⊀ v for all v ∈ V
    (b) **Transitivity:** u ≺ w and w ≺ v implies u ≺ v
    (c) **Local finiteness:** for all u ≺ v, the set
        {w : u ≺ w ≺ v} is finite

Properties (a) and (b) make (V, ≺) a DAG. Property (c) ensures
discreteness — no infinite chains between any two vertices.

**Definition 2 (Causal Past).** For v ∈ V:
  past(v) = {u ∈ V : u ≺ v}

**Definition 3 (Link/Edge).** A pair (u, v) with u ≺ v is a
**link** (or edge) if there is no w with u ≺ w ≺ v. Links are
the nearest-neighbor causal relations.

**Definition 4 (Chain).** A chain is a totally ordered subset
C ⊆ V: for all u, v ∈ C, either u ≺ v or v ≺ u.
The **chain length** (or depth) of G is the supremum of |C|
over all chains C.

**Definition 5 (Antichain).** An antichain is a subset A ⊆ V
where no two elements are comparable: for all u, v ∈ A with
u ≠ v, neither u ≺ v nor v ≺ u. Antichains represent
**spacelike-separated sets** — the discrete analogue of space.

**Definition 6 (Antichain cardinality).** The **width** of G
at depth d is the maximum antichain cardinality among vertices
at chain distance d from the "initial" vertex (if one exists).
In RA-native units, this IS the spatial extent.

---

## 2. The BDG Depth Profile

**Definition 7 (Depth-k ancestors).** For v ∈ V and k ∈ {1,2,3,4},
the depth-k ancestor count is:

  N_k(v) = |{u ∈ past(v) : the maximal chain from u to v
            has length exactly k}|

More precisely: N_k(v) counts elements u ∈ past(v) such that
the longest chain from u to v (within past(v)) has length k,
and there exists no w with u ≺ w where the longest chain from
w to v also has length k.

(Note: in the Poisson-CSG model, N_k(v) is the number of
elements in the "order interval of size k" — the k-th layer
of v's causal diamond.)

**Definition 8 (BDG Score).** For d=4, the BDG score of vertex v
in context G is:

  S(v, G) = c₀ + c₁N₁(v) + c₂N₂(v) + c₃N₃(v) + c₄N₄(v)

where the BDG coefficients are:

  (c₀, c₁, c₂, c₃, c₄) = (1, -1, 9, -16, 8)

These integers are determined uniquely by d=4 causal diamond
geometry (Benincasa-Dowker 2010; RA_O14_Uniqueness.lean,
Lean-verified, 47 theorems, 0 sorry).

---

## 3. The Sequential Growth Rule (Engine of Becoming)

**Definition 9 (Sequential Growth).** Starting from a finite
causal graph G_n = (V_n, ≺_n) with |V_n| = n, a new vertex
v_{n+1} is added as follows:

  **Step 1 (Proposal):** A candidate past set P ⊆ V_n is
  selected. The new vertex v_{n+1} will satisfy
  past(v_{n+1}) = P (plus all transitive ancestors of P).

  **Step 2 (Score computation):** Compute the depth profile
  N_k(v_{n+1}) from the proposed past set P and the existing
  graph G_n. Compute S(v_{n+1}, G_n ∪ {v_{n+1}}).

  **Step 3 (BDG Filter):** If S > 0, the candidate is
  **admissible**. If S ≤ 0, the candidate is **filtered**.

  **Step 4 (Actualization):** Among admissible candidates,
  one is selected (the quantum measure assigns amplitudes;
  the selection is stochastic). The selected candidate becomes
  permanent: G_{n+1} = G_n ∪ {v_{n+1}} with the specified
  causal relations.

  **Step 5 (Irreversibility):** Once added, v_{n+1} cannot
  be removed. G only grows. This is Axiom 2 of the bimodal
  ontology.

**Definition 10 (Acceptance Probability).** In the Poisson-CSG
model (the statistical limit of the sequential growth rule),
the acceptance probability at density μ is:

  P_acc(μ) = P(S > 0)

where S = 1 + c₁N₁ + c₂N₂ + c₃N₃ + c₄N₄ and each N_k is
an independent Poisson random variable with parameter
λ_k = μ^k / k!.

**IMPORTANT NOTE ON P_acc VALUES:**

Two methods for computing P_acc give DIFFERENT values at the
same μ because they compute DIFFERENT quantities:

  (a) **Monte Carlo P_acc:** Sample (N₁,N₂,N₃,N₄) from
      independent Poisson(λ_k) distributions. Compute
      P(S > 0) by sampling. This is the MARGINAL acceptance
      probability — the probability that a randomly placed
      vertex in a Poisson process at density μ passes the filter.

  (b) **Exact enumeration P_acc:** Enumerate all integer profiles
      (N₁,N₂,N₃,N₄) up to a cutoff. Weight each by its
      Poisson probability. Sum the weights of admissible profiles.
      This should give the SAME answer as (a) if done correctly.

  (c) **Profile FRACTION:** Count the fraction of integer profiles
      (without Poisson weights) that are admissible. This is a
      DIFFERENT quantity — it counts profiles uniformly, not by
      their Poisson probability.

The discrepancy flagged by ChatGPT (P_acc ≈ 0.50 vs 0.24 at
μ = 5.7) arises from confusing (a)/(b) with (c). The Poisson-
weighted P_acc and the uniform-fraction P_acc are different
observables. The physically correct one for RA is (a)/(b):
the Poisson-weighted marginal acceptance probability.

**Canonical values (Monte Carlo, 100k samples, seed=42):**

```
μ       P_acc(MC)    ΔS*
0.500   0.639        0.447
1.000   0.548        0.601
2.000   0.537        0.622
3.000   0.447        0.805
4.000   0.405        0.904
4.712   0.414        0.882
5.000   0.429        0.847
5.700   0.502        0.690
7.000   0.747        0.291
10.000  1.000        0.000
```

---

## 4. The Potentia Π

**Definition 11 (Potentia).** Given a causal graph G_n, the
potentia Π(G_n) is the set of all admissible single-vertex
extensions:

  Π(G_n) = {(v, P) : P ⊆ V_n and S(v, G_n ∪ {v}) > 0
             where past(v) = ↓P}

where ↓P denotes the downward closure of P under ≺.

Each element of Π is a possible next actualization event.
The quantum measure assigns a complex amplitude to each
element. The squared modulus gives the probability.

**Properties of Π:**
  - Π depends on G (Axiom 3 of bimodal ontology)
  - Π is finite for finite G (local finiteness)
  - Π is non-empty unless G is "maximally packed" (no
    admissible extensions exist)
  - The cardinality |Π(G)| measures the "richness" of
    available possibilities

**Definition 12 (Bimodal State).** The universe-state at step n
is the pair:

  U_n = (G_n, Π(G_n))

where G_n is the actualized graph (settled, irreversible) and
Π(G_n) is the structured potentia (unsettled, determined by G_n).

---

## 5. Causal Severance

**Definition 13 (Causal Severance).** A causal severance of G
is a partition V = V_A ∪ V_B (disjoint) such that:
  - No vertex in V_A has a link to any vertex in V_B
  - No vertex in V_B has a link to any vertex in V_A

After severance, G splits into two independent graphs
G_A = (V_A, ≺|_{V_A}) and G_B = (V_B, ≺|_{V_B}).

The LLC holds independently on each side (L02, Lean-verified).

**Definition 14 (Severance Boundary).** The boundary of a
severance is:

  ∂V_A = {v ∈ V_A : v had at least one link to V_B before
          severance, or would have had an admissible extension
          into V_B}

These are the "last vertices" — the ones whose outgoing
causal connections are severed.

**Definition 15 (Severed Edge Count).** The number of edges
(links) that were severed:

  N_sev = |{(u,v) : u ∈ V_A, v ∈ V_B, (u,v) was a link in G}|

For an EVENT HORIZON (a null severance surface), the severed
edges are those that WOULD have connected interior vertices to
exterior vertices but cannot, because no future-directed causal
path crosses the horizon.

**CRITICAL DISTINCTION (flagged by ChatGPT):**

  N_boundary = |∂V_A|  (number of boundary VERTICES)
  N_sev = number of severed EDGES

These are NOT the same. They are related by:

  N_sev = Σ_{v ∈ ∂V_A} d_out(v)

where d_out(v) is the number of outgoing links from v that
cross the severance. In general:

  N_sev = ⟨d_out⟩ × N_boundary

where ⟨d_out⟩ is the mean outgoing degree of boundary vertices.

**The entropy observable must be precisely specified:**

  Option A: S = N_boundary (vertex count)
  Option B: S = N_sev (edge count)
  Option C: S = N_boundary × log(d_out) (vertex count × info per vertex)

These are different quantities. The BH entropy literature (Dou-Sorkin)
uses a variant of Option B (link counting). The nucleation report
sometimes uses Option A (vertex counting). This ambiguity must be
resolved.

**Current status: UNRESOLVED.** The correct RA-native entropy
observable needs to be precisely defined and defended. The
dissolution claim ("S = severed edges, 1/4 is translation") is
directionally correct but the observable itself is not yet pinned
down to one of the above options.

---

## 6. The Acceptance Kernel and the Selective Regime

**Definition 16 (Acceptance Kernel).** At density μ, the
acceptance kernel K(N | μ) is the conditional distribution
of the depth profile N = (N₁,N₂,N₃,N₄) given S(N) > 0:

  K(N | μ) = Poisson(N; λ(μ)) × 𝟙[S(N) > 0] / P_acc(μ)

where Poisson(N; λ) = Π_k exp(-λ_k) λ_k^{N_k} / N_k!
and λ_k = μ^k / k!.

**Definition 17 (Selective Regime).** The density interval
where the acceptance kernel is most discriminating — i.e.,
where the conditional distribution K(N|μ) differs most from
the unconditional Poisson(N; λ(μ)).

From the P_acc table: the selective regime is approximately
μ ∈ [3, 6], where P_acc drops to its minimum (~0.40-0.50).
Below μ ≈ 3, most profiles pass (gentle filter).
Above μ ≈ 10, essentially all profiles pass (saturated filter).

**What the selective regime selects for:**

In the selective regime, accepted profiles have:
  - Fewer N₁ than Poisson average (penalized by c₁ = -1)
  - Fewer N₃ than Poisson average (penalized by c₃ = -16)
  - More N₂, N₄ relative to baseline (rewarded by c₂, c₄ > 0)

This is the "depth composition bias" documented in the
spatial expansion section of the nucleation report.

---

## 7. Epistemic Labels (per ChatGPT recommendation)

Following ChatGPT's hierarchy, the claims in the nucleation
programme are labeled:

**ESTABLISHED DISCRETE CLAIM:**
  - Causal severance defines a graph-theoretic hidden-DOF count
  - The LLC holds independently on each side (L02, LV)
  - The BDG score is linear in depth profile (universal phase kicks)
  - The BDG filter penalizes depth-1 connections (c₁ = -1, arithmetic)

**STRONG NUMERICAL EVIDENCE:**
  - P_acc profile through the severance regime (MC, 100k samples)
  - Selective regime biases accepted profiles toward sparse structure
  - N_mol ∝ A in d=4 (Homšak-Veroni 2024, PRD, >10⁶ points)

**CONJECTURE (well-posed theorem target):**
  - Bimodal phase transition: filter saturation → Π collapses
  - Global antichain-driven expansion from the depth composition bias
  - S_BH = severed edge count gives correct area scaling with
    coefficient determined by BDG-to-metric normalization

**SPECULATIVE BRIDGE:**
  - Kerr chirality sources η_b (no computation, no coupling mechanism)

**PHENOMENOLOGICAL FIT:**
  - α = 0.68 (energy release fraction; constrained by η_b, not derived)

---

## 8. The Theorem Targets

**Target 1 (BH Entropy Observable).** Define the RA-native entropy
observable precisely (vertex count, edge count, or information-
theoretic quantity). Prove it is finite, severance-invariant, and
proportional to the continuum area in the thermodynamic limit.

**Target 2 (Phase Transition).** For the BDG-filtered Poisson-CSG,
prove there exists a critical density interval [μ₋, μ₊] where
the acceptance kernel becomes asymptotically profile-independent
(entropy of the kernel → 0, or P_acc → 1 uniformly).

**Target 3 (Antichain Drift).** Under the BDG sequential growth
measure, prove that the expected antichain cardinality growth rate
exceeds the expected chain depth growth rate in the selective
regime μ ∈ [3, 6].

**Target 4 (η_b Coupling).** Derive a quantitative relationship
η_b = F(a*, ε₃, BDG) from a discrete symmetry analysis of
motif-selection under chiral boundary conditions at severance.

**Target 5 (α Derivation).** Derive the energy release fraction
α from the BDG filter's behavior during the saturation transition
μ ∈ [5.7, 10], without fitting to observed η_b.

---

*This document defines the objects. The theorems remain to be proved.*
*The dissolution claim is directionally correct but the observable*
*is not yet pinned down. ChatGPT's critique is accepted in full.*

---

## Addendum: Entropy Observable — RESOLVED

### Definition 18 (Cross-Severance Link Set)

For a severance V = V_A ⊔ V_B of causal graph G = (V, ≺):

  L_Σ = {(u,v) ∈ L(G) : u ∈ V_A, v ∈ V_B}

where L(G) is the set of links (irreducible causal relations).

### Definition 19 (RA-Native Severance Entropy)

  **S_RA(Σ) = |L_Σ|**

The entropy counts irreducible future-directed causal links
blocked by the severance.

### Definition 20 (Severance Out-Degree)

For boundary vertex u ∈ ∂V_A:
  d^Σ_out(u) = |{v ∈ V_B : (u,v) ∈ L_Σ}|

Then: S_RA(Σ) = Σ_{u ∈ ∂V_A} d^Σ_out(u)

### Relationship to Boundary Vertex Count

  S_RA = ⟨d^Σ_out⟩ × N_∂

Boundary vertex count is a PROXY, not the entropy itself.

### The Entropy Observable Ambiguity (Section 5) is now RESOLVED.

Option B (severed edge count) is the correct RA-native observable,
justified by Propositions 1-3 (ChatGPT, April 12 2026).

*Contributed by ChatGPT (GPT-4o).*
