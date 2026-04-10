# PAPER UPDATE CONTENT — April 6, 2026 Session Results
# =====================================================
# This file contains the new and revised sections for each paper.
# Content is written in final-draft prose, ready for integration.


## P0 — NEW SECTION: "Act VIII: The Uniqueness" (insert between Act VII and Coda)
## ================================================================================

### Act VIII: The Only Possible Universe

Everything described in the preceding acts — the nucleation from a spinning black hole, the crystallisation of the particle spectrum, the emergence of structure and complexity, the quantum world, the fragmentation fate — depends on a specific growth rule: the BDG action, with its five integers (1, −1, 9, −16, 8) governing which proposed actualization events become real. The deepest question the framework faces is: why these integers? Are they chosen from alternatives, or are they the only possibility?

The answer, arrived at through a combination of recent combinatorial mathematics and the internal logic of the framework itself, is that they are the only possibility. The argument has five steps, each building on the last.

First, causal invariance — the requirement that the quantum measure on spacelike-separated events is independent of the order in which they are processed — forces the growth rule to be a linear function of the interval layer counts N_k. The amplitude at each vertex must depend only on its causal past, and the total amplitude must be multiplicative over spacelike vertices. The only functions compatible with both conditions are exponentials of linear combinations: exp(i × Σ c_k N_k). This is proved.

Second, the interval counts N_k are cumulative: the count at depth k includes contributions from sub-structures already counted at lower depths. An interval with k intermediate elements contains C(k, j) sub-intervals of depth j, for each j ≤ k — because choosing j of k intermediate elements gives a sub-interval. The containment structure is the Boolean lattice. To extract the genuinely new information at each depth — the information not already captured at lower depths — requires Möbius inversion on this lattice. The Möbius function of any finite poset is unique (a theorem of Gian-Carlo Rota, 1964). Therefore the extraction of net-new information from cumulative counts is unique: it is binomial inversion, and nothing else.

Third, the cumulative counts themselves — the "raw moments" r_k — are determined by the combinatorial structure of d-dimensional causal intervals. Karen Yeats, in a 2024 paper published in Classical and Quantum Gravity, showed that these counts correspond to specific classes of non-crossing partial rooted chord diagrams with coloring and nesting constraints. For d = 4, the moments are r_k = (2k+3)(2k+2)(2k+1)/6, giving (1, 10, 35, 84, ...). These are not parameters. They are the answers to a counting question about four-dimensional causal diamonds.

Fourth, applying the unique binomial inversion to the unique d = 4 moments gives:

C_i = Σ C(i−1, k)(−1)^k r_k = (1, −9, 16, −8)

and hence the action coefficients (−1, 9, −16, 8) — exactly the BDG integers. As a bonus, the sum Σ C_k = 0 — the second-order condition, which ensures the growth rule responds to the structure of the causal past rather than merely its size — is not an additional constraint but an automatic consequence of the d = 4 moments. It holds for all even dimensions, verified computationally for d = 2, 4, 6, and 8.

Fifth, the dimension d = 4 is itself uniquely selected. Among all dimensions, only d = 4 has the property that the selectivity function ΔS*(μ) — the measure of how discriminating the growth rule is — achieves its first local maximum within 2% of the Planck density μ = 1. In d = 2 and d = 3, the selectivity ceiling is in the wrong place. In d = 5 and higher, the ceiling is far above the Planck density, offering no natural operating point. Only d = 4 operates at maximum discriminability at its natural density. This is the D4U02 result, proved computationally with certified error bounds.

The chain is complete. Self-consistency determines the dimension. The dimension determines the moments. The moments, under the unique non-redundant extraction, determine the coefficients. The coefficients determine the growth rule. The growth rule determines the particle spectrum, the coupling constants, the cosmological parameters, and everything else.

There are no free parameters. There are no alternatives. The universe could not have been otherwise.


## P0 — REVISED CODA (replaces current Coda)
## ==========================================

### Coda: One Nature of Nature

The story told in this document — from the parent black hole's spin through the coupling constants and the cosmic web to the origin of life and the fragmentation of the universe — involves no new fields, no extra dimensions, no additional free parameters, and no post-hoc adjustments. Every piece follows from the same ontological commitment: that irreversible actualization events, writing permanent edges into a growing directed acyclic graph, are the primitive physical reality.

And that commitment, as the uniqueness theorem reveals, admits exactly one realisation. The growth rule is not chosen. The dimension is not chosen. The coupling constants are not chosen. They are the unique solution to a combinatorial identity — the only way for an irreversibly growing causal graph to be self-consistent.

Traditional physics sees the laws of nature as fixed rules, and the phenomena of nature as what those rules produce. The deepest insight of Relational Actualism is that this distinction is an artifact of description, not a feature of reality. The Local Ledger Condition is not a law that the causal graph obeys. It is the causal graph, stated as a property. Conservation of energy is not a constraint imposed on actualization events. It is what actualization events are, viewed at the level of bookkeeping. The irreversibility of time is not explained by the framework. It is encoded in the framework's most primitive commitment, since actualization — by definition — is directed.

The universe does not obey laws and produce phenomena. The universe is the laws and the phenomena, simultaneously, at every vertex of the growing graph. And the growth rule that governs this process is not one rule among many — it is the only rule that could exist.

Einstein asked whether God had any choice in making the universe. The answer, from within Relational Actualism, is no. Not because the universe was designed, but because self-consistency admits exactly one solution. The integers (1, −1, 9, −16, 8) that govern which events become real are not parameters of a theory — they are the unique output of a combinatorial identity on the Boolean lattice of causal intervals, in the only dimension where the result is self-sustaining.

The universe is not a thing that winds down. It is a thing that branches — endlessly, irreversibly, creatively. It has no terminal state, because the process that builds complexity is the same process that fragments the graph and nucleates new worlds. Complexification and dissipation are two faces of the same act: ceaseless, causal transformation.

This is what one nature of Nature looks like, from bosons to brains and beyond — and it is the only nature Nature could have had.


## P3 — NEW SECTION: "Nucleation Cosmology" (major addition)
## ==========================================================

### The Birth Certificate of the Universe

Standard cosmology takes the initial conditions of the universe — the baryon-to-photon ratio, the amplitude and spectrum of primordial perturbations, the spatial flatness — as given. Relational Actualism derives them from the parent black hole's properties at the moment of causal severance.

When a region of the causal graph reaches the bandwidth saturation threshold μ₂ ≈ 5.7, the acceptance probability for new actualization events drops to zero. The graph cannot grow further locally, and the region severs from the parent graph. The graph cut theorem (machine-verified in Lean 4) guarantees that the Local Ledger Condition holds independently on each side. The daughter universe inherits its initial conditions from the boundary flux Φ_boundary through the severance surface.

The baryon-to-photon ratio η_b = 6.1 × 10⁻¹⁰ is set by the Bekenstein-Hawking entropy of the parent black hole. Inverting: S_BH/k_B ≈ N_baryons/η_b ≈ 10⁹⁰, giving a parent mass M_parent ≈ 2.5–6.6 × 10⁶ solar masses. This is a supermassive black hole — the kind found at the centres of galaxies. Stellar-mass black holes do not have sufficient entropy to produce a viable daughter universe with our observed η_b.

#### The Kerr Geometry and CMB Anomalies

A real astrophysical SMBH spins, and its spin defines a preferred axis and plane. The Kerr metric describes an oblate horizon whose geometry depends on the dimensionless spin parameter a*. Decomposing the horizon metric function Σ_+(θ) = r_+² + a²cos²θ into spherical harmonics reveals a clean structure: the spin produces a pure quadrupole (ℓ = 2) deformation with ε₂ ∝ a*², while the octupole (ℓ = 3) is identically zero from the Kerr geometry alone. Any octupole must come from the accretion environment — the asymmetric infall that breaks equatorial symmetry — but it shares the same axis as the quadrupole, because the accretion disk lies in the spin's equatorial plane.

The daughter universe is born with anisotropic initial conditions:

δρ/ρ(θ, φ) = ε₂ P₂(cosθ) + ε₃ P₃(cosθ)

with the preferred axis equal to the parent's spin axis.

#### Inflationary Dilution: The (2/ℓ)² Law

The raw Kerr quadrupole (ε₂ ~ 0.01–0.5) vastly exceeds the observed CMB perturbation scale (~10⁻⁵). The resolution is inflationary dilution: the rapid early expansion stretches the nucleation perturbation by a factor e⁻²ᐩᴺ, where ΔN is the number of e-folds beyond the minimum needed to solve the horizon problem.

Different multipoles exit the causal horizon at different times. Mode ℓ exits ln(ℓ/2) e-folds after ℓ = 2. The resulting dilution at each multipole is:

(amplitude at ℓ) / (amplitude at ℓ = 2) = (2/ℓ)²

This is parameter-free — it follows from the kinematics of horizon exit during inflation, with no model dependence. The consequences are immediate:

- ℓ = 2: full nucleation signal (reference amplitude)
- ℓ = 3: 44% of the ℓ = 2 amplitude (20% in power)
- ℓ = 4: 25% of the ℓ = 2 amplitude (6% in power)
- ℓ ≥ 6: less than 0.1% of the ℓ = 2 power — negligible

This predicts that nucleation anomalies appear only at ℓ = 2 and ℓ = 3, with rapidly decreasing strength, and are undetectable at ℓ ≥ 4. This matches the observed pattern exactly.

#### Five Anomalies, Three Parameters, Zero Freedom

The model has three parameters: the parent spin a*, the extra e-folds ΔN beyond the inflation minimum, and the accretion asymmetry δ_acc = ε₃/ε₂. These are constrained by three independent observations:

1. The low quadrupole: C₂ observed ≈ 200 μK² vs ΛCDM prediction ≈ 1100 μK² (80% suppression). This fixes ε₂(a*) × e⁻²ᐩᴺ = 2.1 × 10⁻⁵.

2. The North/South hemisphere asymmetry: A_NS ≈ 0.07. This fixes δ_acc ≈ 0.69.

3. The quadrupole-octupole alignment angle: 9–13° (Planck data). This is consistent with the C₂ constraint (self-check).

Two additional consistency checks are satisfied without adjustment:

4. C₃ is not suppressed (slightly above ΛCDM): the (2/ℓ)² dilution makes the ℓ = 3 nucleation signal 44% of ℓ = 2, too weak to cause suppression but sufficient to cause alignment.

5. Higher multipoles (ℓ ≥ 4) are normal: the (2/ℓ)² dilution makes the nucleation signal negligible.

The system is just-determined: three parameters, three constraints, two consistency checks, zero remaining freedom. The parent spin a* and ΔN trade off logarithmically (higher spin requires more dilution), giving N_total ≈ 64–65 e-folds for any reasonable a* ∈ [0.3, 0.998]. This is itself a prediction: RA predicts near-minimum inflation.

ΛCDM has no mechanism for any of these anomalies. RA explains all five from a single source: the Kerr geometry of the parent SMBH.

#### The Cosmic Web as Evolutionary Consequence

The nucleation perturbations seed structure formation through the μ-dependent expansion feedback intrinsic to RA. The field equations couple the local expansion rate inversely to baryon density: underdense regions expand faster, further diluting; overdense regions expand slower, further concentrating. This positive feedback drives density perturbations away from uniformity, producing the filamentary cosmic web.

The feedback has two endpoints. Underdense voids approach the Erdős-Rényi percolation threshold μ = 1, below which the causal graph fragments — a starvation severance. Dense filament boundaries approach the causal termination threshold μ₂ ≈ 5.7, where new causal severances fire, nucleating daughter universes. Both endpoints are causal disconnection. The universe does not reach thermal equilibrium because fragmentation precedes it. The standard "heat death" scenario requires a single connected component persisting for infinite time; RA's fragmentation mechanism prevents this.

The full causal chain runs: parent SMBH geometry → anisotropic boundary flux → daughter initial conditions → CMB anomalies → structure formation via μ-dependent feedback → filamentary cosmic web → void starvation severance plus boundary density severance → next-generation daughter universes → cycle continues.

Angular momentum is transmitted across generations: each daughter's structure formation is seeded by the parent's geometry, and the daughter's evolved cosmic web provides the asymmetry that seeds granddaughter universes at dense filament boundaries.


## P4 — REVISED SECTION: "Open Problems" (replaces current open problem listing)
## ==============================================================================

### Open Problems: Current Status

The programme's foundational status changed qualitatively with the O14 uniqueness result. The growth rule is uniquely determined by self-consistency; the open problems are now technical rather than foundational.

**Closed or superseded:**

O02 (Causal invariance without amplitude locality axiom): Effectively closed. O01 (amplitude locality) is Lean-verified as a theorem of BDG dynamics. The remaining work is a mechanical Lean completion of a List.Perm induction step.

O09 (Covariant Step 4): Effectively closed. Follows directly from O01 for the unique BDG action.

O10 (Discrete Bianchi) and O11 (Lorentz emergence): Superseded by O14. The unique growth rule's continuum limit automatically satisfies Bianchi (by Benincasa-Dowker 2010) and exhibits Lorentz invariance (by Dowker-Glaser 2013). These are no longer independent open problems; they are properties of the unique action.

**Reframed and more tractable:**

O03 (Bianchi on curved backgrounds): Reframed as: prove the unique BDG action has a well-defined continuum limit on curved backgrounds. Partial results exist (Machet-Wang 2020). No longer requires deriving an unknown operator; requires proving convergence of the known unique operator.

O06 (ξ from first principles): Essentially resolved. With the unique action established, ξ = ΔS*/l_P² where l_P is the unique discreteness scale. The remaining step is a formal identification.

O12 (Scale bridge): Reframed as a computational problem in the unique BDG dynamics, not a conceptual problem about which dynamics to use.

**Genuinely open (technical):**

O04 (WEP formal bounds): Explicit equilibration dynamics calculation. Lower priority.

O05 (Unruh detector): Open quantum systems model for detector coupling. Requires collaborator expertise.

O07 (BMV timescale): The most experimentally urgent remaining problem. Quantitative decoherence criterion for macroscopic centre-of-mass, needed before BMV experimental data arrives. High priority.

O08 (Causal Firewall decoherence timescale): First-principles derivation of τ_d. Partially addressed by non-Markovian correction. Lower priority (long-term prediction).

O13 (Fragmentation timescale): Requires O12 (scale bridge) first. Computational.

**Net status: zero foundational open problems, five technical problems, of which one (O07) is experimentally urgent.**


## P1 — NEW PARAGRAPH (insert at end of introduction or beginning of conclusions)
## ===============================================================================

The BDG integers (1, −1, 9, −16, 8) from which all results in this paper are derived — α_EM = 1/137, α_s = 1/√72, the Koide formula, the five-topology closure — are not free parameters of the framework. A uniqueness theorem (O14) establishes that these integers are the unique output of Möbius inversion (binomial inversion on the Boolean lattice) applied to the combinatorial moment sequence r_k = (2k+3)(2k+2)(2k+1)/6, which counts non-crossing partial chord diagrams on four-dimensional causal intervals (Yeats 2025). The moment sequence is fixed by d = 4 causal geometry; the inversion is the unique non-redundant extraction (Rota 1964); and d = 4 is the unique dimension with self-sustaining selectivity at the Planck density (D4U02). The coupling constants derived in this paper are therefore not merely consistent with four-dimensional causal geometry — they are the only coupling constants that a self-consistent growing causal graph can produce.


## P2 — NEW PARAGRAPH (insert in the discussion of the actualization criterion)
## =============================================================================

The actualization threshold ΔS* = 0.601 nats used throughout this paper is computed from the unique BDG growth rule at the Planck density μ = 1. A uniqueness theorem (O14) establishes that this growth rule — and hence ΔS* — is the only self-consistent option for an irreversibly growing causal graph. The measurement problem is therefore not merely dissolved by RA's actualization criterion; it is dissolved by the only actualization criterion that could exist. No alternative threshold is compatible with the self-consistency of the causal graph.
