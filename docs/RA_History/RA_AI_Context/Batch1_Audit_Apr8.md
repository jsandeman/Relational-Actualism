# Batch 1 Audit: Submitted Papers vs Current RA State
## April 8, 2026

### Key checks:
1. Lovelock contamination (should use BDG uniqueness chain)
2. Sorry claims (O01/O02 now closed; AmpLocality zero sorry)
3. Statistics-as-mechanism errors
4. P5 references (eliminated)
5. Peer review status claims
6. Lean file/theorem count accuracy
7. O10/O11 framing (dissolved, not open)
8. GS02 gauge result
9. IC30 α_EM derivation
10. ΔS* value (0.60069 exact, not 0.601)

---

## RAQM (at FoP, 25 pages)

### CRITICAL ISSUES:

1. **Page 1 abstract**: "the Einstein field equations are the unique consistent macroscopic description of the RA causal graph by Lovelock's theorem"
   - CONTAMINATED. Should say "by BDG uniqueness (Benincasa-Dowker 2010)"
   - This is in the ABSTRACT of the paper under review at FoP.

2. **Page 1 abstract**: "amplitude_locality axiom" mentioned
   - NOW PROVED. O01 is LV. The abstract should note this.

3. **Page 17, Table 2**: "causal_invariance: Quantum measure independent of spacelike ordering (given amplitude_locality axiom)"
   - STALE. Should say "unconditional (amplitude locality proved as theorem)"

4. **Page 22**: "93 Lean-verified results" and "101 Lean-verified results"
   - STALE. Current count is 163 theorems across 7 files.

5. **Page 22, Table 2**: Lists "alpha_inv_137" with "norm_num" 
   - OK but should note IC30 full derivation (137.036019).

6. **Page 19, eq 19**: "ΔS* ≈ 0.601 nats"
   - Should be "ΔS* = 0.60069 nats" (exact irrational, 3/5 ruled out at 25σ)

7. **Page 22**: "RA_AQFT_Proofs_v10.lean compiles... with one intentional placeholder (Matrix.cfc_conj_unitary)"
   - STALE. Need to check current status.

8. **Page 9**: "unitary QM is what RA looks like at large causal density"
   - GOOD. RA-native framing.

9. **Page 19**: "the four-scale μ = 1 unification of RACF"
   - Should be FIVE-scale (QCD, galactic, fault-tolerance, ΔS*, Causal Firewall)

### MINOR ISSUES:

10. References to "eleven-paper suite" (p22) - now 12 papers + submitted papers
11. "Poisson-CSG generative measure" mentioned correctly as environment-dependent
12. Kinematic Snap mechanism well-stated, no contamination

### NO ISSUES WITH:
- Entropic criterion as primary (good)
- Reeh-Schlieder paragraph (good)  
- Born rule consistency framing (good)
- Three predictions (good)
- Spin-bath model (good)

---

## RACL (at CQG, 8 pages)

### CRITICAL ISSUES:

1. **Title and throughout**: Uses Lovelock's theorem as Step (E) of the main derivation
   - This paper IS the Lovelock derivation. The question is whether this is acceptable.
   - ASSESSMENT: RACL was written BEFORE the O10/O11 dissolution (Apr 5).
   - The RA-native chain is: L01+O01+L11 → BD uniqueness → EH action → variation → field eqs → Bianchi from LLC
   - RACL uses: LLC → Rideout-Sorkin → BDG locality → Benincasa-Dowker → Lovelock → Λ=0
   - The Lovelock step is ACCEPTABLE AS SCAFFOLDING in RACL because RACL's purpose is to prove GR emerges. Lovelock IS a valid step if you're working in the continuum limit.
   - BUT: The paper should acknowledge the RA-native chain exists and Lovelock is the continuum-limit expression.

2. **Page 6, §7**: "93 fully sorry-free results" and "RA_AQFT_Proofs_v10.lean compiles... with one intentional placeholder"
   - STALE counts. Now 163 theorems, and AmpLocality/GraphCore/Koide all zero sorry.

3. **Page 1 abstract**: "Lovelock's uniqueness theorem" prominent
   - Should add a sentence: "An RA-native derivation bypassing Lovelock via BDG uniqueness is noted in Section X"

4. **Page 4, Theorem 4.1 proof**: Uses distributional derivative δ(ΔS)
   - This is fine mathematically but the Lean status is honest ("awaits extension of Lean 4 spacetime manifold library")

### NO ISSUES WITH:
- LLC as starting point (correct, RA-native)
- P_act conservation theorem (correct)
- BDG locality lemma (correct)
- Vacuum suppression (correct)
- Departures from GR section (correct)

---

## RATM (at PRD, 9 pages)

### CRITICAL ISSUES:

1. **Page 8**: "RA_D1_Proofs.lean contains 75 results (64 theorems, 11 lemmas, 8 definitions)"
   - Need to verify against current file. The file has been modified (L10/L11/L12 aliases added).

2. **Page 8**: "101 Lean-verified results"
   - STALE. Now 163.

### MINOR ISSUES:

3. **Page 7, §7.5**: "SU(3)gen coherent state structure developed in companion paper RASM"
   - Fine, correctly defers to RASM.

4. **Page 1**: "eleven-paper Relational Actualism suite" implied
   - Minor; paper count has changed.

### NO ISSUES WITH:
- Five topology types (correct, LV)
- Confinement lengths L=3, L=4 (correct, LV)
- 124 extension cases (correct, LV)
- Sequential/topological distinction (correct)
- Gell-Mann-Nishijima verification (correct)
- Physical interpretation section (correct)
- No Lovelock contamination (correct - this paper is about particle topology, not GR)

---

## SUMMARY: Priority fixes by paper

### RAQM (HIGHEST PRIORITY - under review at FoP):
1. Abstract: Lovelock → BDG uniqueness
2. Abstract: amplitude_locality axiom → proved as theorem
3. Table 2: causal_invariance conditional → unconditional
4. Lean counts: 93/101 → 163
5. ΔS*: 0.601 → 0.60069
6. Four-scale → five-scale μ=1

### RACL (at CQG):
1. Add RA-native chain acknowledgment
2. Update Lean counts

### RATM (at PRD):
1. Update Lean counts
2. Minor file reference updates

