# Gauge Structure in RA
## What GS02 Establishes, What It Supports, and What Remains Interpretive
### Joshua F. Sandeman · April 2026

---

## 1. The claim under scrutiny

RA claims that the Standard Model gauge group SU(3) × SU(2) × U(1)
emerges from the BDG integer structure (1, −1, 9, −16, 8). This is
one of the framework's boldest claims, and it is exactly where the
distinction between theorem, computation, and interpretation matters
most.

This note separates the claim into four layers:

- **Layer A:** What is mathematically proved
- **Layer B:** What is computation-verified
- **Layer C:** What is a physically motivated structural reading
- **Layer D:** What remains to be derived

---

## 2. Layer A: What is mathematically proved

### 2.1 The BDG integers alternate in sign

The d=4 BDG coefficients are (c₀,c₁,c₂,c₃,c₄) = (+1,−1,+9,−16,+8).

The alternating sign pattern (+,−,+,−,+) is a mathematical consequence
of inclusion-exclusion counting on causal intervals in 4D Minkowski
space. It is not a choice or a fit. It follows from the combinatorics
of the Alexandrov interval volume formula Vol(J⁺∩J⁻) = (π/24)τ⁴.

**Status: Mathematical fact.** The signs are determined by d=4 geometry.

### 2.2 There are exactly three non-gravitational BDG degrees of freedom

The BDG action in d dimensions has d/2 + 1 terms. One linear
combination (the total score S_BDG) is used by gravity (it determines
the actualization filter and, in the continuum limit, the Ricci scalar).
The remaining d/2 independent combinations are non-gravitational.

In d=4: d/2 = 2, but the independent BDG variables are (N₁,N₂,N₃,N₄)
with one constraint (the score S), leaving 3 independent non-gravitational
degrees of freedom.

**Status: Counting fact.** Three non-gravitational DOFs in d=4 is
arithmetic, not interpretation.

### 2.3 The BDG closure theorem gives exactly five stable topology types

L11 (Lean-verified, 124 extension cases) establishes that the BDG action
in 4D admits exactly five topologically distinct stable pattern classes.

**Status: Lean-verified theorem.**

### 2.4 The confinement lengths are finite and fixed

L10 (Lean-verified): L_g = 3 (gluon), L_q = 4 (quark).

**Status: Lean-verified theorem.**

---

## 3. Layer B: What is computation-verified

### 3.1 The sign of c_k controls ancestor count bias

At μ=1, the conditional expectation E[N_k | S > 0] is:
- **strictly greater** than E[N_k] for positive c_k (k=0,2,4)
- **strictly less** than E[N_k] for negative c_k (k=1,3)

This is verified by exact enumeration over the full Poisson-weighted
BDG score distribution.

**Status: CV (exact enumeration).** The sign-bias pattern is a
computed fact, not an assumption.

### 3.2 Interpretation of the bias

Positive c_k encourages many ancestors at depth k (distributed,
isotropic causal neighborhoods). Negative c_k discourages many
ancestors at depth k (selecting anisotropic, directionally-structured
neighborhoods).

This is the physical reading of the computed bias: the BDG filter
preferentially selects isotropic structure at depths 0, 2, 4 and
anisotropic structure at depths 1, 3.

**Status: CV + structural reading.** The computation is exact;
the isotropic/anisotropic interpretation is physically motivated.

---

## 4. Layer C: The gauge-group interpretation

This is where the claim becomes interpretive rather than proved.

### 4.1 The depth-1 anisotropy → SU(2) × U(1) reading

At μ=1, λ₁ = μ¹/1! = 1, so each vertex has on average exactly one
nearest causal ancestor. One ancestor picks one spatial direction out
of three, breaking 3D isotropy into:

- 2 transverse directions → SU(2)_L
- 1 longitudinal direction → U(1)_Y

**What is established:** The depth-1 Poisson rate λ₁ = 1 is a
mathematical fact. The BDG filter selects configurations with exactly
one depth-1 ancestor (the c₁ = −1 penalty suppresses N₁ > 1).

**What is interpretive:** The identification of the "2+1 directional
split" with the specific group SU(2)_L × U(1)_Y is a physical
mapping. The combinatorics gives a 2+1 structure, but the step from
"2+1 anisotropy" to "SU(2) × U(1) gauge symmetry with specific
representations and quantum numbers" is not yet a theorem.

### 4.2 The depth-3/4 structure → SU(3) reading

c₃ = −16 heavily penalizes depth-3 ancestors (confined, non-propagating).
c₄ = +8 rewards depth-4 ancestors (isotropic, distributed).
The Lean-verified confinement length L_q = 4 and the three colour charges
from N₁ = 2 degeneracy both support a 3-colour structure.

**What is established:** The confinement structure, the finite confinement
lengths, and the 3-colour multiplicity from BDG topology (all LV or CV).

**What is interpretive:** The identification of this 3-colour confined
structure with specifically SU(3)_c — meaning the exact Lie algebra,
its representations, and the full QCD dynamics — is a physical mapping.

### 4.3 The depth-2 structure → Higgs/U(1) remnant reading

c₂ = +9 rewards depth-2 ancestors (isotropic, distributed).
The W/Z bosons are marginal vertices with S(1,0,0,0) = 0 exactly.
The photon escapes via depth-2 dressing: S(1,1,0,0) = 9.

**What is established:** The marginal score S = 0 for depth-1-only
vertices is a Lean-verified integer identity. The photon escape
mechanism via depth-2 dressing is a structural consequence.

**What is interpretive:** The identification of the depth-2 background
with the Higgs mechanism and the residual U(1)_EM is physically
motivated but not yet derived from BDG dynamics alone.

---

## 5. Layer D: What remains to be derived

### 5.1 The representation theory

A full derivation of SU(3) × SU(2) × U(1) from BDG requires showing
that the BDG-filtered dynamics on the DAG produces:

- The specific Lie algebras su(3), su(2), u(1)
- The correct representations (fundamental, adjoint, singlet, etc.)
- The correct quantum number assignments (hypercharge, isospin, colour)
- The correct coupling structure between particle types

None of these are currently proved. They are all structural readings
of the BDG topology, supported by computation but not derived as
theorems.

### 5.2 The running of gauge couplings

The BDG RG analysis gives UV and IR fixed points for α_s (C01, CV)
but does not yet derive the full β-function or show that the three
couplings run independently with the correct Standard Model β-coefficients.

### 5.3 Anomaly cancellation

The Standard Model gauge structure requires specific anomaly
cancellation conditions (e.g., the sum of hypercharges vanishes within
each generation). Whether these follow from BDG topology is not yet
established.

---

## 6. The honest summary

| Aspect | Status | Evidence |
|--------|--------|----------|
| Sign alternation (+,−,+,−,+) | **Mathematical fact** | d=4 inclusion-exclusion |
| Three non-gravitational DOFs | **Counting fact** | d/2 arithmetic |
| Five stable topology types | **Lean-verified** | L11, 124 cases |
| Confinement lengths L=3, L=4 | **Lean-verified** | L10 |
| Sign controls ancestor bias | **Computation-verified** | Exact enumeration |
| Depth-1 gives 2+1 split | **CV + structural reading** | λ₁ = 1 + c₁ penalty |
| Three colour charges from N₁=2 | **CV + structural reading** | BDG topology |
| W/Z marginal at S=0 | **Lean-verified** | Integer identity |
| Photon escapes via depth-2 | **Structural consequence** | S(1,1,0,0) = 9 |
| Full SU(3)×SU(2)×U(1) | **Interpretive mapping** | Systematic but not theorem |
| Representation theory | **Open** | Not yet derived |
| β-functions | **Open** | Not yet derived |
| Anomaly cancellation | **Open** | Not yet derived |

---

## 7. What this means for how RA should talk about gauge groups

### What RA should say:

"The BDG sign structure and depth-anisotropy pattern in d=4 strongly
constrain a three-factor non-gravitational interaction structure. The
sign alternation is forced by inclusion-exclusion geometry. The
conditional ancestor counts confirm the isotropic/anisotropic pattern
by exact enumeration. This structure admits a natural and systematic
interpretation as SU(3) × SU(2) × U(1). The full representation-theoretic
derivation — proving the exact Lie algebra structure, quantum number
assignments, and anomaly cancellation from BDG dynamics — remains an
active research target."

### What RA should not say:

"The Standard Model gauge group is derived from the BDG integers."

The word "derived" is too strong for the current state. What IS derived
is the constraint structure (three DOFs, sign pattern, confinement,
topology closure). What is NOT yet derived is the exact group-theoretic
identification.

### The right framing:

The gauge-group story is a **strongly constrained interpretive mapping**
built on a genuine mathematical substrate. It is not numerology (the
substrate is real and Lean-verified). It is not yet a theorem (the
interpretation layer is not machine-checked). It is somewhere in between,
and honest labeling of that position is a strength, not a weakness.

---

## 8. What would upgrade GS02 from interpretation to theorem

A complete derivation would require one of:

1. **Discrete representation theory:** Show that the BDG-filtered growth
   dynamics on the DAG produces states that transform under irreducible
   representations of su(3) ⊕ su(2) ⊕ u(1), with the correct branching
   rules and quantum numbers. This is a hard but well-posed target.

2. **Emergent gauge symmetry:** Show that the effective continuum field
   theory of the BDG-filtered Poisson-CSG has SU(3) × SU(2) × U(1) as
   its local gauge symmetry, via a causal-set analogue of the spin-foam
   or lattice gauge construction. This connects to existing programs in
   LQG and causal set theory.

3. **Anomaly bootstrap:** Show that the BDG topology classification +
   LLC conservation + confinement structure uniquely determines the gauge
   group via anomaly cancellation conditions. This would be the most
   elegant route: the gauge group is forced by consistency, not derived
   from dynamics.

Any of these would be a major result in mathematical physics. The fact
that they are not yet achieved does not diminish the substrate — it
defines the frontier.

---

## 9. Connection to the epistemic ladder

In the Kernel vs Implemented RA framework:

- The **kernel** says: three non-gravitational DOFs exist in d=4.
- The **closure** (L11, LV) says: five topology types, finite and exhaustive.
- The **implementation** says: sign alternation produces directional bias,
  confinement is finite, marginal vertices exist at S=0.
- The **interpretation** says: this IS SU(3) × SU(2) × U(1).
- The **speculation** says: the full representation theory follows.

Everything below the interpretation layer is solid. The interpretation
itself is strongly motivated. The speculation defines the research target.

---

*Technical note produced April 9, 2026.*
*This document addresses Pressure Point 3 (gauge-group language) of the
ChatGPT priority assessment and directly responds to the Kernel vs
Implemented RA analysis §7.2.*
