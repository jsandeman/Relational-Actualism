# Stage A — Full Lean Audit Report

**Author:** Claude (with Joshua Sandeman)
**Dates:** April 17–19, 2026
**Scope:** Primary-materials catalog of all Lean 4 files in the RA project,
consolidating per-file transcripts from three working sessions.

**Discipline:** Inventory, not interpretation. Each entry records what the
file declares, what it proves versus what it axiomatizes versus what it
leaves open, and cross-references to other files. Value judgments (Tier
classifications, pushback on IC46) are separated from the catalog.

**Files catalogued:** 11 (8 canonical build roots + 3 auxiliary)

---

## Lakefile build roots

Package: `RelationalActualism` (Lean 4.29 + Mathlib git master).
Lean-QuantumInfo dependency commented out; enabling it would discharge the
CFC sorry in RA_AQFT_Proofs_v10.lean.

| Build root | KB labels claimed | In-file status |
|---|---|---|
| `RA_GraphCore` | L01, L02, L03 | 13 items, 0 sorry, 0 axiom |
| `RA_D1_Proofs` | L08, L10, L11, L12, D1a–D1h | ~50 real + ~12 tautology, 0 sorry, 0 axiom |
| `RA_Koide` | L09 | 18 items, 0 sorry, 0 axiom |
| `RA_AQFT_Proofs_v10` | L04–L07 | 20 items, **1 sorry, 2 axioms** |
| `RA_AmpLocality` | O01, O02 | 6 items, 0 sorry, 0 axiom |
| `RA_Spin2_Macro` | O10s | 15 items, 0 sorry, 0 axiom |
| `RA_O14_Uniqueness` | O14 | ~25 real items, 0 sorry, 0 axiom |
| `RA_BaryonChirality` | D3a, D3b | ~8 real items, 0 sorry, 0 axiom |

Auxiliary (not in lakefile):
- `RA_AQFT_CFC_Patch.lean` — 52 lines, documentation-only
- `RA_Alpha_EM_Proof.lean` — 228 lines, 24 declarations, high quality
- `RA_Complexity_Proofs.lean` — 324 lines, orphaned (full entry in
  companion file `Stage_A_RA_Complexity_Proofs_Entry.md`)

---

## File 1 — `RA_AmpLocality.lean` (207 lines)

**KB targets:** O01 (amplitude locality), O02 (causal invariance)
**Imports:** Mathlib only (no RA-internal imports)
**Sorry: 0 | Axioms: 0**

### Declaration map

| # | Item | Lines | Kind | Status |
|---|---|---|---|---|
| 1 | `CausalDAG` | 25–31 | structure | definitional |
| 2 | `causal_past` | 38–39 | def | definitional |
| 3 | `causal_interval` | 43–44 | def | definitional |
| 4 | `interval_subset_past` | 52–58 | lemma | **proved** |
| 5 | `interval_eq_interval_past` | 62–68 | lemma | **proved** |
| 6 | `bdg_increment` | 77–80 | def | definitional |
| 7 | `bdg_increment_depends_on_past_only` | 83–106 | lemma | **proved** |
| 8 | `bdg_amplitude` | 113–115 | noncomp def | definitional |
| 9 | `amplitude_local` | 118–121 | def | definitional |
| 10 | `bdg_amplitude_locality` (O01) | 127–136 | theorem | **proved** |
| 11 | `quantum_measure` | 144–146 | noncomp def | definitional |
| 12 | `foldl_mul_perm` | 151–167 | private lemma | **proved** |
| 13 | `bdg_causal_invariance` (O02) | 171–179 | theorem | **proved** |

**Total: 2 theorems + 3 public lemmas + 1 private helper = 6 proved items.**

### Flags

1. **`_hcausal` hypothesis unused in O02 proof.** `bdg_causal_invariance`
   uses only `foldl_mul_perm`, which follows from commutativity of ℂ alone.
   The causal-order hypothesis is underscored. The theorem holds for any
   permutation, not only causal-order-respecting ones.
2. **`quantum_measure` definition is trivial.** Each `bdg_amplitude` is
   `exp(i·ℤ)`, so each factor has modulus 1. The `normSq` of a
   unit-modulus product is always 1. O02 is true but the statement is
   provable independent of BDG content — the KB label "L07 conditional→
   unconditional via BDG-specific mechanism" is not what this Lean proof
   establishes.
3. **Structure-level note.** `CausalDAG` defines `precedes : V→V→Prop`
   as a strict partial order (irrefl + trans). Antisymmetry is derivable.
4. **`bdg_increment` is parameterized in `cs : Fin 5 → ℤ`.** The proof
   of O01 holds for any Fin-5 integer coefficient family; the specific
   BDG values (1,−1,9,−16,8) are not load-bearing in this file.

---

## File 2 — `RA_GraphCore.lean` (253 lines)

**KB targets:** L01 (Local Ledger Condition), L02 (Graph Cut), L03 (Markov Blanket)
**Imports:** Mathlib only
**Sorry: 0 | Axioms: 0**

### Declaration map

| # | Item | Lines | Kind | Status |
|---|---|---|---|---|
| 1 | `Vertex` | 22–24 | structure | definitional |
| 2 | `Edge` | 26–30 | structure | definitional |
| 3 | `ActualizationGraph` | 32–38 | structure | definitional |
| 4 | `outgoing_edges`, `incoming_edges` | 44–48 | defs | definitional |
| 5 | `satisfies_local_ledger` (L01) | 54–55 | def (Prop) | definitional |
| 6 | `CausalCut` | 61–65 | structure | definitional |
| 7 | `internal_edges`, `boundary_flux`, `src_in_VL`, `dst_in_VL` | 67–79 | defs | definitional |
| 8 | `outgoing_pairwise_disjoint` | 86–91 | lemma | **proved** |
| 9 | `incoming_pairwise_disjoint` | 94–99 | lemma | **proved** |
| 10 | `outgoing_pairwise_disjoint_VL` | 102–105 | lemma | **proved** |
| 11 | `incoming_pairwise_disjoint_VL` | 107–110 | lemma | **proved** |
| 12 | `biUnion_outgoing_eq_src_in_VL` | 113–119 | lemma | **proved** |
| 13 | `biUnion_incoming_eq_dst_in_VL` | 122–128 | lemma | **proved** |
| 14 | `internal_flux_disjoint` | 131–135 | lemma | **proved** |
| 15 | `src_in_VL_eq_internal_union_boundary` | 138–152 | lemma | **proved** |
| 16 | `dst_in_VL_eq_internal` | 155–163 | lemma | **proved** (uses `no_backward`) |
| 17 | `sum_outgoing_decompose` | 170–181 | lemma | **proved** |
| 18 | `sum_incoming_decompose` | 184–192 | lemma | **proved** |
| 19 | `RA_graph_cut_theorem` (L02) | 200–212 | theorem | **proved** (linarith chain) |
| 20 | `horizon_partition` | 214–218 | theorem | alias of #19 |
| 21 | `MarkovBlanket` (L03) | 224–233 | structure | **definitional only; no theorems proved** |
| 22 | `MarkovBlanket.boundary` | 235–237 | def | definitional |

**Total: 2 theorems (1 alias) + 11 lemmas = 13 proved items.**

### Flags

1. **Primitive type clash with AmpLocality.** GraphCore uses
   `topo_order : Vertex → ℕ` + `arrow_of_time : topo_order src < dst`.
   AmpLocality uses binary `precedes`. Any claim that AmpLocality's O01
   applies to GraphCore's graphs needs a bridge lemma.
2. **`arrow_of_time` field unused in L02.** The graph cut theorem proof
   uses `no_backward` directly. `arrow_of_time` is a structural
   requirement not load-bearing for any proved theorem here.
3. **L03 MarkovBlanket is structure-only.** No theorems proved about
   blankets. The structure lacks pairwise-disjointness of
   Internal/External/Sensory/Active — only requires union covers G.V.
4. **API-brittleness note in file.** Lines 249–252 flag reliance on
   `Finset.sum_biUnion` signature not changing in Mathlib.

---

## File 3 — `RA_AQFT_Proofs_v10.lean` (487 lines)

**KB targets:** L04 (frame independence), L05 (Rindler stationarity), L06, L07
**Imports:** Mathlib only
**Sorry: 1 | Axioms: 2 — including the IC46 finding**

### Declaration map

| # | Item | Lines | Kind | Status |
|---|---|---|---|---|
| 1 | `inner_adjoint_rectangular` | 52–63 | lemma | **proved** |
| 2 | `Matrix.log'` (cfc Real.log wrapper) | 84–86 | noncomp def | definitional |
| 3 | `MatPosSemidef` | 94–96 | Prop def | definitional |
| 4 | `DensityMatrix` | 102–107 | structure | 4 fields |
| 5 | `DensityMatrix.ext` | 110–112 | theorem | **proved** |
| 6 | `vacuumState` | 118–146 | def | **3 field proofs** (herm, pos, tr1) |
| 7 | `rindlerThermal` | 152–192 | noncomp def | **3 field proofs** |
| 8 | `UnitaryMatrix` | 198–202 | structure | 3 fields |
| 9 | `MatPosSemidef.conj_unitary` | 210–231 | lemma | **proved** |
| 10 | `unitaryConj` | 233–247 | def | **3 field proofs** |
| 11 | `trace_unitary_conj` | 253–257 | lemma | **proved** |
| 12 | `Matrix.cfc_conj_unitary` | 278–287 | lemma | **sorry** (LQI-closable) |
| 13 | `log_unitary_conj` | 291–295 | lemma | **proved** (corollary of #12) |
| 14 | `quantumRelEnt` | 303–305 | noncomp def | definitional |
| 15 | `relEnt_unitary_invariant` | 312–335 | theorem | **proved** (independent of #16) |
| 16 | **`vacuum_lorentz_invariant`** | 344–345 | **axiom** | **PROBLEMATIC — see pushback** |
| 17 | `frame_independence` (L04) | 349–353 | theorem | proved *modulo #16* |
| 18 | `rindler_stationarity` (L05) | 357–363 | theorem | proved *via #17 modulo #16* |
| 19 | `CPTPMap` | 370–375 | structure | 2 fields |
| 20 | `CPTPMap.apply` | 378–430 | noncomp def | **3 field proofs** |
| 21 | `petz_monotonicity` | 436–441 | **axiom** | LQI-closable; not load-bearing |

**Counts:** 4 proved theorems + 4 proved lemmas + 1 sorry lemma + 12 proved
field-obligations across structured defs = 20 genuinely proved items.

### Flags

1. **IC46 — `vacuum_lorentz_invariant` axiom is logically inconsistent with
   `vacuumState` definition.** See pushback section below.
2. **`Matrix.cfc_conj_unitary` sorry (line 287).** Closable by uncommenting
   the lean-quantuminfo dependency in lakefile. Proof is one line:
   `exact Matrix.cfc_conj_unitary_of_lqi U M f`.
3. **`petz_monotonicity` axiom.** Not load-bearing for L04 or L05.
   Discharge requires LQI import + ~50-line DensityMatrix↔MState adapter.
4. **`relEnt_unitary_invariant` is independent of #16.** Its proof uses
   only `log_unitary_conj` and `trace_unitary_conj`. This theorem is
   sound even if #16 is deleted.

---

## File 4 — `RA_D1_Proofs.lean`

**KB targets:** L08 (α_EM = 144−7 = 137), L10 (confinement), L11 (5-topology
BDG closure, 124 extension cases), L12 (qubit fragility), D1a–D1h (particle
classification)
**Sorry: 0 | Axioms: 0**

### Summary

~50 real proved items + ~12 items flagged as tautologies-labeled-as-physics.

### Flagged tautologies (Tier 3 structural gap)

`P_act_conservation`, `RA_field_equation_unique`, and similar §16 items
have theorem statements like `(0:ℤ) = 0 := rfl` but docstrings label them
as covariant-derivative conservation equations (∇_μ(P_act T^μν) = 0).
There is no Lean representation of P_act, T^μν, or covariant derivative
anywhere in the corpus. The gap is the entire relativistic field-theoretic
formalism — cannot be closed without building new infrastructure.

### Flagged presentation gaps (Tier 2)

- `t1`/`t2` extension tables: transcribed from Python enumerations, not
  formally linked to `bdgScore`. Later theorems
  `gluon_ext_scores_correct` / `quark_ext_scores_correct` close this for
  the Fin 15 base cases.
- `confinement_lengths` (L10): claimed L_g=3, L_q=4 not derived from
  worldline analysis — stated as arithmetic.

### Substantively proved content

- Nat.choose / Fin arithmetic base tables
- α_EM arithmetic label: 144 − 7 = 137
- 5-topology BDG closure: 124 extension cases enumerated
- Koide base-case arithmetic used by RA_Koide.lean
- Various score-comparison lemmas for extension patterns

---

## File 5 — `RA_Koide.lean`

**KB target:** L09 (K = 2/3 from BDG integers)
**Sorry: 0 | Axioms: 0**

### Summary

18 items, all real. Clean formalization of the K=2/3 algebraic identity
with no physics-bridge issues internal to the file. Physics bridge to
lepton masses lives outside Lean, as intended.

---

## File 6 — `RA_Spin2_Macro.lean` (137 lines)

**KB target:** O10s (emergent massless spin-2)
**Sorry: 0 | Axioms: 0**

### Declaration map

| # | Item | Lines | Kind |
|---|---|---|---|
| 1 | `MacroSpace := Fin 5 → ℝ` | 21 | abbrev |
| 2 | `traceMap` | 23–26 | linear map |
| 3 | `c_R : Fin 5 → ℝ` = (1,−1,9,−16,8) | 28–29 | def |
| 4 | `bdgMap` | 31–38 | linear map |
| 5 | `l_R : Fin 5 → ℝ` = (0,1,−1,1,−1) | 40–41 | def |
| 6 | `llcMap` | 43–50 | linear map |
| 7 | `physicalSubspace` | 52–53 | Submodule (triple kernel intersection) |
| 8 | `mem_physicalSubspace` | 56–61 | lemma |
| 9 | `fin5_sum` | 64–67 | private lemma |
| 10 | `projMap` | 73–80 | linear map |
| 11 | `liftMap` | 82–98 | linear map |
| 12 | `proj_lift_id` | 100–104 | private lemma |
| 13 | `lift_proj_id` | 106–116 | private lemma |
| 14 | `physIso` | 118–122 | LinearEquiv |
| 15 | `emergent_massless_spin2` | 128–132 | **theorem O10-spin2** |

**All 15 items proved. Explicit LinearEquiv construction. Real linear algebra.**

### Hand-verified constraint algebra

- **BDG constraint with liftMap image:** c₀·0 + c₁·(7a+b)/8 + c₂·(15a−7b)/8
  + c₃·a + c₄·b = (−7a−b+135a−63b)/8 − 16a + 8b = 16a − 8b − 16a + 8b = 0 ✓
- **LLC constraint with liftMap image:** (7a+b)/8 − (15a−7b)/8 + a − b
  = (−8a+8b)/8 + a − b = 0 ✓
- **`emergent_massless_spin2`:** `LinearEquiv.finrank_eq physIso` gives
  finrank = finrank ℝ² = 2.

### Flags

1. **`l_R = (0,1,−1,1,−1)` stipulated, not derived from GraphCore LLC.**
2. **Physics bridge external.** The 2-dimensional kernel is rigorously
   proved. The identification with "massless spin-2 graviton polarizations"
   is an external physical-content bridge.

---

## File 7 — `RA_O14_Uniqueness.lean` (239 lines)

**KB target:** O14 (BDG coefficient uniqueness via binomial inversion)
**Sorry: 0 | Axioms: 0**

### Summary

~25 real items across five categories:

1. **Yeats moment values at k=0..4** via `native_decide` (1, 10, 35, 84, 165)
2. **Nat.choose values** (15 theorems via `native_decide`)
3. **yeats_moment ↔ Nat.choose bridges at k=0..3** (4 theorems — real
   combinatorial identity: `(2k+3)(2k+2)(2k+1)/6 = Nat.choose (2k+3) 3`)
4. **Hockey-stick identities across d=2, 4, 6, 8** (4 theorems — non-trivial
   combinatorial verifications of `Σⱼ (−1)ʲ C(d,j+1) r_j = 0`)
5. **C1_eq through C4_eq**: arithmetic sums matching binomial-inversion outputs

### Flags

1. **Presentation gap (Tier 2, closable).** C1_eq..C4_eq state literal
   integer arithmetic, not symbolic applications of `Nat.choose` and `r`.
   Four additional one-line bridge lemmas (example below) would wire them:
   ```lean
   theorem C2_via_inversion :
       (Nat.choose 1 0 : ℤ) * r 0 - (Nat.choose 1 1 : ℤ) * r 1 = -9 := by
     rw [choose_1_0, choose_1_1, r_eq_0, r_eq_1]; norm_num
   ```
2. **Content gap: no uniqueness statement.** No theorem of the form
   `∃! C, ∀ k, r k = ...`. This is a real gap — not presentational —
   and requires a new theorem stating the inversion uniqueness explicitly.

---

## File 8 — `RA_BaryonChirality.lean`

**KB targets:** D3a (chirality), D3b (baryon conservation)
**Sorry: 0 | Axioms: 0**

### Summary

~8 real items. D3 RESOLVED claim from memory edit.

### Flags

1. **N₂-preservation claim has counter-example.** Score equality (two
   configurations have the same BDG score) does not imply N-vector
   equality. Empirical check: 10 distinct N-vectors give score 18 with
   N₂ ∈ {1, 2, 3, 4}. Preserving score ≠ preserving baryon number.
2. **`D3_chirality_and_baryon` master theorem** omits the structural
   content its name implies — it aggregates sub-results but doesn't
   bridge them to SM chirality definitions.
3. **(Tier 2 closure path):** Proper N-vector type + bridge lemma
   `score_determines_N` would formalize what the file implies.

---

## File 9 — `RA_AQFT_CFC_Patch.lean` (52 lines)

**Status:** documentation-only. Not in lakefile.
**Sorry: 0 | Axioms: 0**

### Content

All declarations inside `/- ... -/` block comments. Zero live Lean
content. Serves as a note documenting the path to closing the CFC sorry
in RA_AQFT_Proofs_v10.lean via Lean-QuantumInfo import.

Not superseded; not a gap. Orthogonal to the build.

---

## File 10 — `RA_Alpha_EM_Proof.lean` (228 lines)

**Status:** Not in lakefile. High-quality auxiliary file.
**Sorry: 0 | Axioms: 0**

### Declaration map

| # | Item | Lines | Kind | Status |
|---|---|---|---|---|
| 1 | `c : Fin 5 → ℤ` | 27–31 | def | BDG coefficients |
| 2 | `bdg_144_factorisation` | 32–33 | theorem | **real** (3!·4! = 144) |
| 3 | `bdg_7_depths` | 35 | theorem | trivial (3+4=7) |
| 4 | `alpha_inv_137` | 37 | theorem | trivial (144−7=137) |
| 5 | `bdg_alpha_s_weight` | 39 | theorem | **real** (c₂·c₄ = 72) |
| 6 | `two_couplings_from_bdg` | 41–47 | theorem | composite |
| 7 | `E_mu` | 48–50 | noncomp def | polynomial |
| 8 | `P_type1`, `P_type2` | 51–58 | noncomp defs | stipulated |
| 9 | `bdg_depth_ratio_exact` | 59–68 | theorem | **real** (ratio = μ⁷/144) |
| 10 | `f_em` | 69–70 | noncomp def | 144α − (1+α)⁷ |
| 11 | `f_em_continuous` | 71–72 | lemma | **real** (fun_prop) |
| 12 | `f_em_at_zero` / `_at_one` | 73–76 | lemmas | **real** |
| 13 | `f_em_expand` | 77–83 | theorem | **real** (binomial) |
| 14 | `alpha_EM_exists` | 84–103 | theorem | **real** (IVT on [0,1]) |
| 15 | `f_em_at_inv138_neg` / `_inv136_pos` | 104–115 | lemmas | **real** |
| 16 | `f_em_hasDerivAt` | 116–129 | theorem | **real** (derivative) |
| 17 | `f_em_deriv_pos` | 130–136 | lemma | **real** (on bounded interval) |
| 18 | `f_em_strictMono_on` | 137–149 | theorem | **real** |
| 19 | `alpha_EM_bounds` | 150–168 | theorem | **real** (root in (1/138, 1/136)) |
| 20 | `alpha_EM_unique_in_interval` | 169–185 | theorem | **real** (uniqueness) |
| 21 | `bdg_alpha_EM_prediction` | 186–187 | theorem | trivial |
| 22 | `bdg_leading_order_residual` | 188–228 | theorem | **real** (numerical bound) |

**Total: 24 declarations (5 defs + 20 theorems/lemmas). Real-analysis content.**

### Assessment

Substantive file. Items 11–23 are genuine real-analysis Lean: continuous
function, IVT (applied twice), derivative computation, strict monotonicity
on a bounded interval, uniqueness by monotonicity. Items 3, 4, 21 are
trivial arithmetic but connected to the actual fixed-point equation
144α = (1+α)⁷ whose root is proved to lie in (1/138, 1/136).

### Flags

1. **Not in lakefile.** Adding it would upgrade L08 from
   "arithmetic labels" to "analytic proof of existence, uniqueness, and
   leading-order accuracy of the α_EM fixed-point root." Real KB status
   improvement.
2. **`f_em α = 144α − (1+α)⁷` is stipulated.** Derivation of this equation
   from BDG structure is external.
3. **`P_type1`, `P_type2` densities stipulated.** Identification with
   photon/electron vertices is external.
4. **Does not formalize α_EM = 1/137.036 (empirical value).** Proves
   root ∈ (1/138, 1/136), leaves the identification-with-physics as an
   external claim.

---

## File 11 — `RA_Complexity_Proofs.lean` (324 lines)

**Status:** Joshua-flagged `canonical, needs_work` (Apr 19, 2026).
Orphaned — not in current lakefile.

**Full entry:** see `Stage_A_RA_Complexity_Proofs_Entry.md` (145 lines,
companion file in outputs).

### Summary

- 4 genuine proofs (RA_graph_cut_theorem chain + markov_blanket_shielding)
- 3 tautologies dressed as theorems:
  - `assembly_index_correspondence` (returns hypothesis)
  - `actualization_frame_invariance` (P↔P via Iff.rfl)
  - `biological_persistence` (unused _h_stable)
- 1 sorry: `biological_persistence_strong` (line 309)
- 1 content-free axiom: `causal_firewall_threshold : Prop` (no body)
- 1 Bool axiom: `vacuum_energy_suppression`
- `is_acyclic : True` stubbed (not actually DAG)

Paper IV's formal backing is substantially weaker than Papers II/III.
RACF peer-review implication noted but not a review-blocker.

---

## Aggregated tally (all 11 files)

| File | In lakefile | Proved | Sorry | Axioms | Key Stage A issue |
|---|---|---|---|---|---|
| RA_AmpLocality.lean | Yes | 6 | 0 | 0 | `_hcausal` unused; quantum_measure trivially perm-invariant |
| RA_GraphCore.lean | Yes | 13 | 0 | 0 | MarkovBlanket no theorems; arrow_of_time unused |
| RA_AQFT_Proofs_v10.lean | Yes | 20 | **1** | **2** | **IC46 inconsistency** + 1 LQI-closable sorry |
| RA_D1_Proofs.lean | Yes | ~50 | 0 | 0 | ~12 tautologies labeled as physics (Tier 3) |
| RA_Koide.lean | Yes | 18 | 0 | 0 | clean |
| RA_Spin2_Macro.lean | Yes | 15 | 0 | 0 | l_R stipulated |
| RA_O14_Uniqueness.lean | Yes | ~25 | 0 | 0 | no uniqueness statement; C_eq presentation gap |
| RA_BaryonChirality.lean | Yes | ~8 | 0 | 0 | score ≠ N-vector counter-example |
| RA_AQFT_CFC_Patch.lean | No | 0 | 0 | 0 | documentation-only |
| RA_Alpha_EM_Proof.lean | No | 24 | 0 | 0 | high-quality, not in build |
| RA_Complexity_Proofs.lean | No | 4 | 1 | 2 | tautologies + stubbed DAG |

### Global counts

- **~183 genuinely proved items** across 11 files (was reported as ~116
  across 10 files before RA_Complexity_Proofs audit; adjusts with file 11
  and more precise re-count)
- **~15 tautologies with physics-themed docstrings** (D1_Proofs §16
  cluster + 3 in Complexity_Proofs)
- **2 active sorries:** Matrix.cfc_conj_unitary (LQI-closable);
  biological_persistence_strong (Complexity_Proofs)
- **4 axioms:** petz_monotonicity (not load-bearing); vacuum_lorentz_invariant
  (IC46 — inconsistent as stated); causal_firewall_threshold (content-free);
  vacuum_energy_suppression (Bool)
- **~94 transcription-trusted items** (D1_Proofs t1/t2 extension tables,
  BaryonChirality score→N-vector comments)

---

## Three-tier gap calibration

**Tier 1 — Formally clean, ready as-is:**
- RA_GraphCore.lean
- RA_Koide.lean
- RA_Spin2_Macro.lean
- RA_AmpLocality.lean (with flag on `_hcausal`)
- RA_Alpha_EM_Proof.lean (if added to lakefile)

**Tier 2 — Real content with closable presentation gaps:**
- RA_O14_Uniqueness.lean: add 4 bridge lemmas invoking Nat.choose + r
  symbolically; optionally add binomInverse def + uniqueness theorem
- RA_D1_Proofs.lean Fin 15 base tables: already closed via
  `gluon_ext_scores_correct` / `quark_ext_scores_correct`
- RA_BaryonChirality.lean N₂-preservation: needs N-vector type + bridge
  lemma mapping score → N-vector invariants

**Tier 3 — Structural gaps requiring new infrastructure:**
- RA_D1_Proofs.lean §16 (P_act_conservation cluster): no Lean
  representation of P_act, T^μν, covariant derivative
- RA_D1_Proofs.lean t1/t2 tables: would need N-vector type + extension
  operation formalized
- RA_D1_Proofs.lean L10 confinement: would need worldline derivation of
  L_g=3, L_q=4
- RA_AQFT_Proofs_v10.lean IC46: needs either IsLorentzBoost predicate
  (Tier 3, modest) or BDG-sprinkling derivation replacing axiom (Tier 3+)
- RA_Complexity_Proofs.lean: needs P_act representation, proper DAG
  acyclicity (not `True`), persistence theorem proof

---

## IC46 — Critical pushback on `vacuum_lorentz_invariant`

**Finding:** the axiom at lines 344–345 of `RA_AQFT_Proofs_v10.lean` is
not merely a framing-discipline violation (importing QFT axiom into
RA-native formalization). **As written, it is logically inconsistent with
the `vacuumState` definition in the same file.**

### Axiom statement

```lean
axiom vacuum_lorentz_invariant (U : UnitaryMatrix n) :
    unitaryConj U vacuumState = (vacuumState : DensityMatrix n)
```

Universally quantifies over all unitaries U on ℂⁿ.

### vacuumState definition (line 118)

`Matrix.diagonal (fun i => if i = 0 then 1 else 0)` — rank-1 projector
onto basis vector 0.

### Explicit counter-example (n=2)

Let U = Pauli X = `[[0,1],[1,0]]`. Verifies UnitaryMatrix requirements
(U·U⁺ = U⁺·U = I).

- `U · diag(1,0) · U⁺ = diag(0,1)`
- `vacuumState.mat = diag(1,0)`
- `(unitaryConj U vacuumState).mat = diag(0,1)`
- By `DensityMatrix.ext` (line 110), these are unequal density matrices.

So the axiom, instantiated at n=2 with U = Pauli X, asserts a false
equality. From a false axiom, any proposition is derivable (ex falso).

### Consequences

- `frame_independence` (L04, lines 349–353) derives inside this
  inconsistent axiom system. Lean's kernel accepts compilation (axioms
  are not consistency-checked), but the conclusion — invariance under
  *all* unitaries — is not what should be provable. A sound proof would
  need to restrict U to Lorentz boosts.
- `rindler_stationarity` (L05) inherits the issue via frame_independence.
- `relEnt_unitary_invariant` (theorem 15) is independent of this axiom
  and is genuinely proved.

### Minimum-cost fix

Introduce an explicit predicate and restrict the axiom:

```lean
axiom IsLorentzBoost {n : ℕ} [NeZero n] [Fintype (Fin n)]
    [DecidableEq (Fin n)] : UnitaryMatrix n → Prop

axiom vacuum_lorentz_invariant (U : UnitaryMatrix n)
    (hU : IsLorentzBoost U) :
    unitaryConj U vacuumState = (vacuumState : DensityMatrix n)
```

Then `frame_independence` and `rindler_stationarity` must carry the
`IsLorentzBoost U` hypothesis. Still a QFT axiom import (IC46-class
framing-discipline issue), but consistent.

### RA-native fix (Tier 3+)

Derive the fixed-point structure from BDG sprinkling + vertex symmetry.
Scope: substantial new primitive infrastructure.

### KB implication

Memory edit #10 currently calls out L04/L05 as "LV-conditional." Accurate
characterization should sharpen to: "LV-conditional-on-inconsistent-axiom,
pending IC46 resolution." Recommend not using L04/L05 as foundations for
downstream KB claims until either the minimum fix or the RA-native fix is
landed.

---

**Stage A complete.** 11 files catalogued with full declaration maps,
status counts, and cross-file dependencies. Open items enumerated by
tier. IC46 inconsistency surfaced with explicit counter-example.

Stage B (Python scripts) is in progress — see `Stage_B_Inventory.md`.
Stages C and D have not begun.
