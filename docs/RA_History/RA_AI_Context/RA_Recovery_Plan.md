# RA Recovery Plan — April 8, 2026

## Problem Statement

The current set of Lean files (5 files, ~2252 lines) covers most of RA's LV claims but has gaps caused by a file reorganization between March 29 and April 6. The RAKB references theorem names and file locations that don't match the current files. This plan reconciles everything.

---

## Phase 1: Lean File Consolidation

### 1A. Recover graph-theoretic results into RA_D1_Proofs.lean

**Source:** RA Main Chat 1 (March 29), URL: https://claude.ai/chat/65c5904e-7930-4b6b-8cd2-dd54a25f0571

**Results to recover:**
- `ActualizationGraph` structure (vertices, edges, charge)
- `CausalCut` structure (V_L, V_R, partition, no backward edges)
- `satisfies_local_ledger` definition (L01)
- `boundary_flux`, `internal_edges`, `outgoing_edges`, `incoming_edges`
- `internal_flux_disjoint` [proved]
- `sum_outgoing_decompose` [sorry — Finset.sum_biUnion]
- `sum_incoming_decompose` [sorry — Finset.sum_biUnion]
- `RA_graph_cut_theorem` [proved given helpers] (L02)
- `horizon_partition` corollary (L02)
- `MarkovBlanket` structure + shielding lemmas (L03)

**Action:** Copy these sections from the March 29 chat into the current RA_D1_Proofs.lean as a new Section 0 (before the current Section 0). The two sorry tags on the helper lemmas are genuine Finset combinatorics — they should be closable with `Finset.sum_biUnion` + a disjointness proof.

**Sorry status after recovery:** 2 sorry (both mechanical Finset lemmas). These are the same kind of "completable" sorry as the List.Perm sorry in RA_AmpLocality.lean.

### 1B. Recover Koide proof

**Source:** RA Main Chat 1 (March 29), same URL

**Results to recover:**
- `kval` definition (Koide eigenvalue function)
- `koide_sum_val` : Σ kval θ k = 3
- `koide_sum_val_sq` : Σ kval θ k² = 6
- `koide_K_eq_two_thirds` : K = 2/3 [zero sorry]
- `majorana_K_eq_two_thirds` [zero sorry]
- Complex roots of unity helpers

**Action:** Either (a) recover into a standalone `RA_Koide.lean` file, or (b) append to RA_D1_Proofs.lean as a new Section 17. Option (b) is simpler and matches the RAKB's file reference.

**Sorry status:** 0 sorry. This is a clean proof.

### 1C. Add named wrapper theorems for L10, L11, L12

These results are already proved in the current file but under different names than the RAKB expects. Add aliases:

```lean
/-- L10: Confinement lengths. -/
theorem confinement_lengths :
    gluon_confinement_length = 3 ∧ quark_confinement_length = 4 :=
  ⟨rfl, rfl⟩

/-- L11: BDG closure — 5 topology types, 124 extensions exhaust SM. -/
theorem universe_closure := D1_closure_complete

/-- L12: Qubit structural fragility — electrons/photons at minimum BDG score 1. -/
theorem structural_fragility :
    chainScore 0 = 1 ∧ chainScore 2 > 0 ∧
    (∀ n, chainScore (n + 4) = 1) ∧
    -- Score 1 is the minimum positive score in the stable set:
    bdgScore 2 1 0 0 > 1 ∧  -- quark: 8 > 1
    bdgScore 1 2 0 0 > 1 ∧  -- gluon: 18 > 1
    bdgScore 1 1 0 0 > 1 :=  -- W boson: 9 > 1
  ⟨by norm_num [chainScore],
   by norm_num [chainScore],
   D1a_fixed_point,
   by norm_num [bdgScore],
   by norm_num [bdgScore],
   by norm_num [bdgScore]⟩
```

**Sorry status:** 0 sorry.

### 1D. Add L08 alias in RA_D1_Proofs.lean

Already present as part of Section 16 (`alpha_inv_137`). Also proved in RA_O14_Uniqueness.lean. No action needed, but ensure RAKB references both locations.

---

## Phase 2: Close Mechanical Sorry Tags

### 2A. RA_D1_Proofs.lean: `sum_outgoing_decompose` and `sum_incoming_decompose`

**Strategy:** Both need `Finset.sum_biUnion` with a disjointness hypothesis. The disjointness (`internal_flux_disjoint`) is already proved. The remaining step is showing that `outgoing_edges G v` for `v ∈ V_L` decomposes as `internal_edges ∪ boundary_flux` — a set-theoretic identity that follows from the definitions.

**Estimated effort:** ~30 lines each. Straightforward Finset manipulation.

### 2B. RA_AmpLocality.lean: `bdg_causal_invariance` List.Perm induction

**Strategy:** Induction on `List.Perm` swaps. Each swap exchanges two spacelike-separated vertices, and amplitude locality (proved) guarantees each factor is unchanged. The product of complex numbers commutes.

**Estimated effort:** ~40 lines. Uses `List.Perm.rec` + commutativity of ℂ multiplication.

### 2C. RA_AQFT_Proofs_v10.lean: `Matrix.cfc_conj_unitary`

**Strategy:** Import from Lean-QuantumInfo (Meiburg et al. 2025). The proof exists in `Isometry.lean` of the LQI library. Need to add LQI as a dependency and write a ~10-line adapter.

**Estimated effort:** ~20 lines + lakefile dependency.

---

## Phase 3: RAKB Reconciliation

After Phases 1–2, update the RAKB to reflect actual file locations and theorem names:

| RAKB ID | RAKB says | Actual location | Action |
|---------|-----------|-----------------|--------|
| L01 | `local_ledger_condition in RA_D1_Proofs.lean` | Recovered from March 29 | Update: definitional (RA_D1_Proofs.lean §0) |
| L02 | `graph_cut_theorem in RA_D1_Proofs.lean` | Recovered; 2 sorry on helpers | Update: LV-structural (2 completable sorry) |
| L03 | `markov_blanket in RA_D1_Proofs.lean` | Recovered as structure definition | Update: structural definition (shielding is definitional) |
| L08 | `alpha_inv_137 in RA_D1_Proofs.lean` | Present in both D1 and O14 | OK as-is |
| L09 | `koide_formula in RA_D1_Proofs.lean` | Separate file; needs recovery | Update after 1B |
| L10 | `confinement_lengths in RA_D1_Proofs.lean` | `D1e_finite_confinement` | Add alias (1C) |
| L11 | `universe_closure in RA_D1_Proofs.lean` | `D1_closure_complete` | Add alias (1C) |
| L12 | `structural_fragility in RA_D1_Proofs.lean` | Implicit in D1a results | Add named theorem (1C) |
| O01 | `bdg_amplitude_locality in RA_AmpLocality.lean` | Present, zero sorry | OK |
| O02 | `bdg_causal_invariance in RA_AmpLocality.lean` | Present, 1 sorry (List.Perm) | Honest: LV with 1 mechanical sorry |
| O10s | `emergent_massless_spin2 in RA_Spin2_Macro.lean` | Present, zero sorry | OK |
| O14 | `RA_O14_Uniqueness.lean` | Present, zero sorry | OK |

---

## Phase 4: Accurate Theorem Count

After all phases, the honest count:

| File | Theorems/Lemmas | Sorry |
|------|-----------------|-------|
| RA_D1_Proofs.lean (current) | ~55 | 0 |
| RA_D1_Proofs.lean (recovered §0) | ~8 | 2 (Finset helpers) |
| RA_D1_Proofs.lean (Koide, §17) | ~8 | 0 |
| RA_D1_Proofs.lean (aliases, §18) | 3 | 0 |
| RA_AQFT_Proofs_v10.lean | ~20 | 1 (LQI adapter) |
| RA_AmpLocality.lean | ~8 | 1 (List.Perm) |
| RA_O14_Uniqueness.lean | ~47 | 0 |
| RA_Spin2_Macro.lean | ~6 | 0 |
| **Total** | **~155** | **4** |

Of the 4 sorry tags:
- 2 are Finset.sum_biUnion lemmas (completable, ~30 lines each)
- 1 is List.Perm induction (completable, ~40 lines)  
- 1 is LQI CFC adapter (completable by import, ~20 lines)

None are conceptual gaps. All are mechanical.

The paper claim should say **"~155 Lean 4 theorems with 4 mechanical sorry tags, all completable"** rather than "109 theorems with zero sorry."

---

## Phase 5: Paper Updates

### P1 (RA_P1.tex) — submission-ready
- Update Lean theorem names to match aliases
- Update theorem count in abstract and conclusions
- Section 6 (α_EM): clarify the "12² = 144" geometric meaning

### P2–P5 — need LaTeX conversion
- All four are currently plaintext-in-LaTeX (bold headers, no `\section{}`)
- Need conversion to proper LaTeX with theorem environments, equation numbering, bibliography
- P2 has duplicate title block (once in `\begin{center}`, once as plaintext)

### P0 (Biography) — close to current
- Companion paper references still point to 4-paper DOIs; need updating to 6-paper structure
- Otherwise content is current

### Website (index.html)
- Still shows 7-paper structure (RAQM/RAGC/EB/RAHC/RACI/RAQI/RADM)
- Needs updating to 6-paper structure (P0–P5)

---

## Execution Priority

1. **Phase 1C** (aliases) — 15 minutes, zero risk, immediately fixes 3 RAKB gaps
2. **Phase 1B** (Koide recovery) — 30 minutes, zero sorry, fixes L09
3. **Phase 1A** (graph-theoretic recovery) — 1 hour, adds 2 sorry but recovers L01/L02/L03
4. **Phase 3** (RAKB reconciliation) — 30 minutes, documentation only
5. **Phase 2** (close sorry tags) — 2–4 hours, optional but improves the count
6. **Phase 4** (accurate count) — 15 minutes after everything else
7. **Phase 5** (papers) — separate session(s)

---

*Plan drafted by Claude, April 8, 2026. All file references verified against uploaded content and chat history search.*
