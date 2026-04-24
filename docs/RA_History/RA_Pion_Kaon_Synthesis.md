# Pion and Kaon Instability as N₃/N₄ BDG Debt: A Synthesis

**Status:** Research synthesis combining existing RASM machinery with the topological-reproducibility insight.

**Date:** April 16, 2026

---

## 1. The Insight

Pions and kaons are unstable. In RA, this means their topologies are not stably reproducible under DAG growth. The question is: **why not?**

The answer appears to already exist in RASM §6, in the treatment of weak interactions — I just hadn't connected it properly to the pion/kaon case. Here is the synthesis.

## 2. What RASM already establishes

**(a) Stability criterion (RASM §5a):** A stable pattern has S_BDG(v) > 0 at every vertex. An unstable pattern has at least one vertex where S_BDG(v) ≤ 0 during its propagation; at that vertex the pattern dissipates into vacuum. This is decay.

**(b) Weak isospin = N_3/N_4 handedness charge (RASM §6):** The weak interaction acts on the N_3/N_4 degrees of freedom. W and Z bosons carry net Q_{N_3/N_4} ≠ 0 and therefore pay BDG actualization cost at every vertex of their propagation.

**(c) W/Z finite range from BDG debt (RASM §"Ranges"):** A pattern with rest-frame actualization frequency f_0 = mc²/h persists for proper time τ = ℏ/mc² before BDG debt becomes unsustainable. For the W boson: R_W = cτ_W ≈ 2 × 10⁻¹⁸ m.

**(d) BDG filter heavily penalizes N_3 (RASM §Selective Regime):** At all densities μ ∈ [1, 7], ΔN_3 < 0 and grows in magnitude with μ. The filter systematically suppresses N_3-rich configurations because c_3 = −16 is the most negative coefficient.

## 3. The connection

**The proton pattern (1, 2, 0, 0) has N_3 = N_4 = 0.** It is a pure N_1/N_2 structure carrying no weak-sector internal content. Under DAG growth, no vertex of the proton pattern needs to activate N_3 or N_4 degrees of freedom. It pays no weak BDG debt. Its score S = 18 is maintained at every vertex, and the pattern self-reproduces indefinitely. **τ_p = ∞.**

**The W/Z pattern carries Q_{N_3/N_4} ≠ 0.** Every vertex of its propagation must sustain N_3/N_4 content. Each such vertex pays BDG debt because the filter penalizes N_3 (and to a lesser extent creates tension with N_4 balance). The cumulative debt exhausts the pattern's coherence within τ = ℏ/mc². **Short range, effective mass.**

**The pion pattern (qq̄) inherits quark N_3/N_4 content through its decay channels.** The π± → μν channel involves a weak vertex: the quark-antiquark pair annihilates through a virtual W boson into a lepton pair. This means somewhere in the pattern's allowed time-evolution, a vertex with Q_{N_3/N_4} content must be activated. Unlike the proton, which NEVER needs such a vertex, the pion's propagation has *some probability per step* of encountering this weak-vertex requirement. That probability is the decay rate.

**The kaon is similar, with the additional strangeness content providing a specific N_3/N_4 signature that weak currents can access.** The K± → μν, K_L → πeν, K_S → ππ channels all involve N_3/N_4-carrying vertices.

## 4. Why this unifies mass and lifetime

Your original insight was that mass and lifetime should be outputs of the same structural calculation. This synthesis shows how.

**For a stable pattern (proton):**
- Mass = cascade energy through the N_1/N_2 structure. No N_3/N_4 content.
- Lifetime = ∞ because no weak vertex is ever required.
- The pattern lives entirely in the "shallow sector" (N_1, N_2).

**For an unstable pattern (pion, kaon):**
- Mass = effective energy of the qq̄ configuration, which lives predominantly in the N_1/N_2 shallow sector but has *access* to N_3/N_4 via decay channels.
- Lifetime = inverse of the probability per Planck time that the pattern accesses (and cannot reproduce) an N_3/N_4 vertex.
- The mass may be suppressed below the baryon scale because the pattern is "leaky" — its BDG score is maintained with some probability < 1 per step.

This predicts a qualitative correlation: **Goldstone-suppressed light mesons (π, K, η) should have short lifetimes** because their lightness and their instability share the same root — both reflect the pattern's marginal ability to maintain N_3/N_4 content.

The η' is the striking exception: it has **mass close to the baryon scale (≈ 958 MeV)** AND is not Goldstone-suppressed. RASM §6 already predicts this: η' is the flavor-singlet pseudoscalar that does not couple to the chiral current the same way as π, K, η. In the RA picture, η' does not inherit N_3/N_4 content the way the Goldstone pseudoscalars do. Hence its 1.8% match to the baryon cascade, and its relatively longer (though still finite) lifetime.

## 5. The specific derivation target

To convert this synthesis into a derivation, we need:

**(i) The BDG debt cost per weak-vertex activation.** This should be computable from the BDG coefficients: a W/Z-like vertex at a propagating pattern requires some specific N_3 or N_4 content, and the cost is ΔS_weak per step.

**(ii) The probability per step that a meson pattern accesses a weak vertex.** This depends on the pattern's internal structure (specifically, how "close" the qq̄ configuration sits to a weak-decay channel in the allowed extension space).

**(iii) The decay rate formula:** Γ ≈ P_weak-access × exp(−ΔS_weak) × f_0, where f_0 = mc²/h is the pattern's natural actualization frequency.

**(iv) The mass formula:** m_meson should come out as the pattern's rest-frame cascade energy, with an effective μ_meson reduced by the BDG-debt leakage relative to the baryon.

Step (iii) would give lifetime predictions for π, K, η. Step (iv) would give mass predictions. Both should emerge from the same computation.

## 6. Why spinor dynamics was a red herring

I earlier argued we'd need "RA-native spinor dynamics" to derive the pion mass. This was importing QCD. The correct program is to compute the **BDG debt structure of weak-sector content in the pion's allowed extension space**. Spinors don't appear. Goldstone theorems don't appear. Just:

- Vertices (actualization events)
- Chains (N_k)
- BDG score S
- Which vertices in the pattern's time-evolution require N_3/N_4 content
- How much BDG debt each such vertex costs

All RA-native. All tractable (in principle) via Monte Carlo on BDG-filtered Poisson-CSG with specified "transition channel" patterns.

## 7. What has already been established vs what is new

**Already in RASM:**
- Weak isospin as N_3/N_4 handedness charge
- W/Z range from BDG debt
- Maximal parity violation from DAG acyclicity
- Stability criterion as BDG-filtered self-similarity

**New from this synthesis:**
- The *pion/kaon instability mechanism* as specifically the weak-vertex-access probability
- The *unification* of mass and lifetime as outputs of the same structural calculation
- The *explanation* of why η' is special (no weak-vertex access at the pattern level)
- The *research target* framed cleanly in BDG-native terms

## 8. Proposed next steps

**Near-term (1-2 sessions):**
1. Locate the "five-type decay classification with Σ_eff values" mentioned in user memory — it may already contain the weak-vertex-access framework
2. Formalize the "weak-vertex-access probability" for π, K, η in terms of BDG-extensible configurations
3. Compute the per-step leakage probability from the BDG filter on weak-channel configurations

**Medium-term (a few sessions):**
1. Compute predicted lifetimes for π±, K±, K_S, K_L, η and compare to observation
2. Extract effective μ_meson from the leakage rate; check mass predictions
3. Write up as a short paper: "Unified mass-lifetime derivation for light mesons in Relational Actualism"

**Longer-term:**
1. Extend to baryon resonances (Δ, N*, Σ, Ξ, Ω)
2. Connect to the 5-type decay classification if it's the right framework
3. Check whether the η' prediction sharpens (currently 1.8% match, could become tighter if the weak-vertex-access mechanism predicts the exact splitting)

## 9. What this does and does not claim

**Claims:**
- Pion/kaon instability has a specific RA-native mechanism (weak-vertex BDG debt)
- Mass and lifetime are outputs of the same structural calculation
- η' matching the baryon scale at 1.8% reflects its lack of weak-vertex pattern access, consistent with QCD's anomaly story but derived differently

**Does not claim:**
- Specific mass predictions for π, K, η (mechanism identified; numerical computation not done)
- Specific lifetime predictions (same)
- Goldstone mechanism in any form (replaced by weak-vertex leakage)
- Connection to chiral symmetry breaking beyond the parity-violation account RASM already gives

---

## Epistemic status summary

| Claim | Tier | Evidence |
|-------|------|----------|
| Pions/kaons decay because weak-vertex access is required in their propagation | DR (pending formalization) | RASM §6 + §5a + user insight |
| η' matches baryon scale because it lacks weak-vertex access | PI | 1.8% numerical match + SM interpretation |
| Mass and lifetime unified by weak-vertex access probability | CN | Synthesis, no computation yet |
| Specific m_π, Γ_π values derivable from BDG | OP | Research target |
