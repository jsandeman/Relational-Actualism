# Stage A — RA_Complexity_Proofs.lean Audit Entry

**Date:** April 19, 2026
**File:** `/mnt/user-data/uploads/RA_Complexity_Proofs.lean` (324 lines)
**Status tag:** `canonical, needs_work` (per Joshua, Apr 19 2026)
**Not in current lakefile roots.** Orphaned from the 8-file canonical
build. Whether it compiles on current Mathlib has not been tested.
**Target paper:** Paper IV (Complexity, Life, Causal Firewall).
Section comments reference old paper identifiers (RAHC, RACI, RACF,
RAGC), confirming this predates the April 16 12→4 paper restructure.

---

## Structural inventory

| Section | Lines | Content | Status |
|---|---|---|---|
| 1. Ontology | 16–29 | Vertex, Edge, ActualizationGraph | definitions only; `is_acyclic : True` is stubbed |
| 2. LLC | 36–43 | `satisfies_local_ledger` | definition |
| 3. Causal Cut | 50–60 | `CausalCut`, `boundary_flux`, `internal_edges` | definitions |
| 4. Helper lemmas | 66–167 | disjointness + sum-decomposition | **3 genuine proofs (~100 lines)** |
| 5. Graph Cut Theorem | 174–192 | `RA_graph_cut_theorem` + alias | **1 genuine proof + 1 trivial alias** |
| 6. Markov Blanket | 199–232 | Structure + shielding lemma | **1 genuine proof (~14 lines)** |
| 7. Assembly Index | 239–262 | `assembly_index_correspondence` | ⚠️ **tautology** (returns hypothesis) |
| 8. Observer Frame | 269–283 | `actualization_frame_invariance` | ⚠️ **tautology** (P ↔ P) |
| 9. Causal Firewall | 290–309 | persistence + threshold | ⚠️ 1 tautology + 1 content-free axiom + **1 sorry** |
| 10. Vacuum energy | 316–323 | `vacuum_energy_suppression` | 1 Bool axiom |

## Gap accounting

| Item | Count | Notes |
|---|---|---|
| Genuine proved theorems | 4 | §4 helpers (×3), `RA_graph_cut_theorem`, `markov_blanket_shielding` |
| Trivial aliases | 1 | `horizon_partition` := `RA_graph_cut_theorem` |
| Tautologies presented as theorems | 3 | §7, §8, `biological_persistence` |
| Active sorries | 1 | `biological_persistence_strong` (line 309) |
| Content-free axioms | 1 | `causal_firewall_threshold : Prop` (type-only, no body) |
| Bool/external axioms | 1 | `vacuum_energy_suppression` |
| Stubbed constraints | 1 | `is_acyclic : True` |

## What's actually proved vs. what's claimed in Paper IV

### Real content (carries weight)
- **`RA_graph_cut_theorem`**: If LLC holds on all vertices in V_L of a
  causal cut, then boundary flux sums to zero. Proof chains through 3
  substantive lemmas (~100 lines total) using biUnion decomposition
  and `arrow_of_time`. This is non-trivial.
- **`markov_blanket_shielding`**: If an edge ends in Internal, its
  source is not in External. Uses `shield_internal` + disjointness.

### Tautologies (do NOT carry weight)
- `assembly_index_correspondence`: theorem = `SAI.value ≤ AI.index`;
  hypothesis `hC1 : condition_C1 G MB AI SAI` unfolds to the same
  inequality; proof is `hC1`. The correspondence between RA's assembly
  index and the Cronin-Walker standard index is **assumed as a
  hypothesis**, not derived.
- `actualization_frame_invariance`: statement `LLC ↔ LLC`; proof
  `Iff.rfl`. Frame arguments unused. The theorem that different
  observer frames yield the same LLC-satisfaction is **not proved**.
- `biological_persistence`: assumes LLC pointwise on Internal, concludes
  LLC at one internal vertex. The `_h_stable : stability_threshold`
  hypothesis is unused. "Persistence follows from stability" is **not
  proved**; persistence is assumed and restated.

### Not formalized
- **`biological_persistence_strong`** (the version that derives LLC from
  stability_threshold alone): sorry.
- **`causal_firewall_threshold`**: declared as `axiom ... : Prop` with no
  content body. Name-binding only; satisfied by `True`.
- **DAG acyclicity**: `is_acyclic : True` stub means every "graph" in
  this file is allowed to have cycles. None of the causal reasoning
  actually enforces acyclicity.

## Paper IV implication

The canonical Lean support for Paper IV-grade claims is substantially
weaker than for Papers II–III. Specifically, these Paper IV claims have
narrative backing in the prose but do not have formal backing here:

1. Assembly index correspondence (Paper IV §4)
2. Observer-frame invariance of actualization (Paper IV §7)
3. Biological persistence from stability threshold alone (Paper IV §7)
4. Causal firewall threshold as a structural claim (Paper IV §7)

Upgrading from `canonical, needs_work` to `canonical, closed` requires
at minimum:

- Replace `is_acyclic : True` with a real acyclicity predicate (likely
  adapting the DAG structure from `RA_GraphCore.lean`).
- Rewrite `assembly_index_correspondence` to state and prove an actual
  correspondence (not a hypothesis-restatement). The real theorem
  content is not identified here.
- Rewrite `actualization_frame_invariance` to state frame-independence
  across two frames, not `P ↔ P`. The real theorem content should
  quantify over `f1 f2`.
- Close `biological_persistence_strong` or replace it with a theorem
  whose conclusion is actually stronger than its hypothesis.
- Give `causal_firewall_threshold` a definite propositional body (or
  convert to a def with content).

## Relation to RACF peer review status

RACF is at IJA with reviewers assigned (first paper in the suite to
reach active review). Astrobiology referees are unlikely to probe the
Lean formalization depth, so this gap is not a review-blocker. But if
anyone does ask for formal backing of the F1/F2/B1–B3 claims, this file
is what they'd see, and it does not support what the paper narrates at
the level the other canonical files do.

---

## Stage A close

With this entry, Stage A covers:
- 8 canonical lakefile-tracked files (audited in prior sessions;
  entries live in session transcripts)
- 2 auxiliary files (RA_AQFT_CFC_Patch.lean — doc-only; RA_Alpha_EM_Proof.lean
  — not in lakefile, high quality, 228 lines, candidate for promotion)
- 1 canonical-but-orphaned file (this one — `RA_Complexity_Proofs.lean`)

**Total: 11 Lean files inventoried.**

Stage A corrected totals (reflecting today's additions):
- Genuinely proved items: ~120
- Tautologies with physics framing: 15 (12 prior + 3 here)
- Active sorries: 2 (`vacuum_lorentz_invariant` axiom remains separate; CFC
  sorry in AQFT_v10 reverted post-port-failure; `biological_persistence_strong` here)
- Content-free axioms: 1 (new; `causal_firewall_threshold`)
- QFT-imported / Bool / external axioms: 3 (`vacuum_lorentz_invariant`,
  `petz_monotonicity`, `vacuum_energy_suppression`)
- Stubbed constraints: 1 (new; `is_acyclic : True`)

Stage A is closable. Open items remaining (for non-Stage-A attention):

- IC46 `vacuum_lorentz_invariant` reformulation (Priority 0; from prior sessions)
- CFC sorry in `RA_AQFT_Proofs_v10.lean` (requires Mathlib API exploration
  per `RA_CFC_Port_Retrospective.md`)
- `RA_Complexity_Proofs.lean` upgrade (this file; canonical, needs work)
- `RA_Alpha_EM_Proof.lean` promotion to lakefile (upgrades L08 status)

Ready to begin Stage B (Python scripts) when Joshua uploads the first batch.

---

*Entry produced April 19, 2026.*
