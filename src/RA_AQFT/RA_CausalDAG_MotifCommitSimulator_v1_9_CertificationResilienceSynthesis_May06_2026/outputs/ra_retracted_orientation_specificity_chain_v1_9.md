# Retracted orientation-specificity chain (v1.5 — v1.8.1)

This document collects the **negative result** that closes the v1.x orientation-overlap rescue audit. Cite this synthesis when discussing the orientation-overlap result; do NOT pull v1.5 +0.028 or any pre-v1.8.1 reading directly.

## Net result

> Under matched-graph extraction at canonical scale, no orientation-specific certification-rescue signal is supported. The apparent gaps observed in v1.5 (+0.028) and v1.6 (-0.146 / -0.229) are artifacts of (a) a deterministic-hash mapping between cells and an independent graph corpus (v1.5), (b) a member-indexed witness keying flaw shared between v1.5 and v1.6, and (c) the structural co-determination of orientation_overlap with `(support_width, family_size)` at the cell level (v1.7 onward).

## Timeline

### v1.5 (2026-05-05) — original positive claim
- **Original claim**: `RA-SIM-CONCRETE-GRAPH-ORIENT-002` reported a +0.028 augmented_exact_k specificity gap and -0.147 / -0.070 partial correlations on a parallel synthetic-deterministic graph corpus (58 graphs).
- **Honesty caveat at release**: rescue values came from v0.9 simulator runs but orientation overlap came from a hash-keyed sampling of independent topology, so the +0.028 could be a sampling artifact.
- Audit machinery passed end-to-end (decoupling 12/12; selector_stress correctly classified).
- See audit_events `EV-2026-05-05-001`.

### v1.6 (2026-05-05) — first matched-graph diagnostic
- **Original claim**: `RA-SIM-GRAPH-COUPLED-ORIENT-002` reported reversed-sign rescue gaps -0.146 / -0.229 on a 192-trial subset; framed as v1.5 retraction at the time.
- Closed the v1.5 rescue/topology disconnection methodologically (rescue + orientation_overlap from the same `CausalDAG` per trial). That part stands as `RA-SIM-GRAPH-COUPLED-ORIENT-001`.
- See audit_events `EV-2026-05-05-002` ... `EV-2026-05-05-005`.

### v1.6 audit (2026-05-05) — witness-keying bug identified
- The v1.5 / v1.6 `graph_coupled_orientation_link_witness` keyed sign on `(depth(v) + depth(p) + member_idx) % 2` plus a `:m{member_idx % 3}` token tag. On regular topologies (chains etc.) with constant depth-parity, this forced sibling family members to produce disjoint witness sets and intra-family Jaccard ≈ 0; per-cell output had 18/24 cells with `overlap = 0` exactly.
- Patched in commit `b742034` to `(depth(v) + depth(p)) % 2` with no member tag.
- See audit_events `EV-2026-05-05-003`.

### 2026-05-05 commit 3b40be2 — silent regression
- Commit `3b40be2` ("v1.6 audit corrections") silently overwrote the `b742034` fix when it re-installed a packet copy that carried the pre-bug-fix witness. The audit-corrections commit message did not flag the regression; the keying bug returned to the repo unnoticed.
- See audit_events `EV-2026-05-06-001`.

### v1.6 keying-tainted reframing (2026-05-06)
- After the regression was identified, the v1.5 retraction by v1.6 was softened: both packets share the same member_idx-keyed witness, so v1.6 did not cleanly retract v1.5; both became "keying-tainted, pending v1.7 ablation".
- See audit_events `EV-2026-05-06-002`.

### v1.7 (2026-05-06) — canonical keying ablation
- **Run**: 194,400 base trials × 6 keyings = 1,166,400 keyed rows; 36 cells per (keying, mode, family_semantics).
- Six keying variants: `member_indexed_edge_pair`, `edge_pair_signed_no_member`, `edge_direction_only`, `incidence_role_signed`, `catalog_augmented_edge_pair` (with v1.3 native catalog tokens), `shuffled_overlap_control`.
- For orientation_degradation, all six keyings produced negative_or_reversed_specificity verdicts. Critically, the **shuffled_overlap_control matched the graph-derived keyings** in the raw aggregation (-0.213 / -0.188 vs -0.211 / -0.191): if random tokens reproduce the same gap as graph-derived ones, the gap is not measuring orientation specificity.
- v1.5 +0.028 was canonically retracted under this ablation (`RA-SIM-ORIENT-KEYING-001`); the reversed-sign verdict was reframed as a binning artifact (`RA-SIM-ORIENT-KEYING-002`).
- See audit_events `EV-2026-05-06-003`, `EV-2026-05-06-004`.

### v1.8 (2026-05-06) — width-only matching, transient Case B
- **Run**: same 1.17M-row trial rows, this time tertile-binning orientation_overlap per (keying, mode, family_semantics) and computing low_minus_high gap within fixed `support_width` strata.
- Headlines: graph keyings raw -0.198/-0.209 → width-matched -0.177/-0.180 (only ~10% reduction). Shuffled control raw -0.193 → width-matched **+0.171** for orientation_degradation/at_least_k (sign flips).
- This transient reading suggested **Case B residual orientation signal** -- the graph-derived gap appeared to survive width matching while the shuffled control collapsed. Family-size remained uncontrolled.
- See audit_events `EV-2026-05-06-005`.

### v1.8.1 (2026-05-06) — joint width × family-size matching, Case A confirmed
- Two complementary readings, both on the same 1.17M-row data:
  1. **Within-stratum re-binning** (`RA-SIM-CONFOUND-V18-1-001`): for each `(mode, family_semantics, threshold_fraction, severity, support_width, family_size)` stratum, tertile orientation_overlap within the stratum and compute the gap. Result: `mean_abs_joint_matched_gap_graph = 0.003`; `mean_abs_graph_minus_shuffled_joint = 0.005`. Case A confirmed: gap collapses to zero within strata.
  2. **Cell-level binning + estimability check** (`RA-SIM-CONFOUND-V18-1-PACKET-001`): tertile orientation_overlap at the (keying, mode, family_semantics, severity, threshold_fraction) cell level, then check whether each `(support_width, family_size)` stratum within the cell contains both low and high bins. Result: `estimable_joint_group_fraction_graph = 0.0` -- no graph keying cell × stratum spans low and high bins. Case C confirmed: orientation_overlap is nearly a deterministic function of `(support_width, family_size)` at cell level.
- Both readings converge on **no orientation-specific signal**. The cell-level reading is the methodologically conservative formulation: the question itself is non-estimable from the v1.7 sampler at fixed `(width, family_size)` strata.
- See audit_events `EV-2026-05-06-006`, `EV-2026-05-06-007`.

## Net registry consequences

The chain is recorded with these proof statuses:

| Claim | Status |
|---|---|
| `RA-SIM-CONCRETE-GRAPH-ORIENT-001` (v1.5 framework) | `simulation_validated_canonical_run_confirmed` (positive specificity reading is superseded) |
| `RA-SIM-CONCRETE-GRAPH-ORIENT-002` (v1.5 +0.028) | `simulation_retracted_by_v1_7_canonical_ablation` |
| `RA-SIM-GRAPH-COUPLED-ORIENT-001` (v1.6 methodology) | `simulation_methodology_confirmed_canonical_via_v1_7` |
| `RA-SIM-GRAPH-COUPLED-ORIENT-002` (v1.6 reversed) | `simulation_canonical_artifact_corrigendum_resolved` |
| `RA-SIM-ORIENT-KEYING-001` (v1.7 retraction) | `simulation_validated_canonical_run_confirmed` |
| `RA-SIM-ORIENT-KEYING-002` (v1.7 binning artifact) | `simulation_validated_canonical_run_confirmed` |
| `RA-SIM-CONFOUND-V18-001` (v1.8 width-only) | `simulation_validated_preliminary_width_matched_diagnostic_superseded_by_v1_8_1` |
| `RA-SIM-CONFOUND-V18-1-001` (Case A, within-stratum) | `simulation_validated_canonical_run_confirmed` |
| `RA-SIM-CONFOUND-V18-1-002` (pure-graph keyings non-estimable) | `simulation_validated_canonical_run_confirmed` |
| `RA-SIM-CONFOUND-V18-1-PACKET-001` (Case C, cell-level) | `simulation_validated_canonical_run_confirmed` |

## Methodological discipline that emerged

These rules now live in `RA-SIM-CONFOUND-METHOD-001` framing entry:

(a) Joint stratification on at least `(support_width, family_size)` before any matched-graph orientation-rescue claim.
(b) Shuffled-overlap control evaluated within the SAME joint strata.
(c) Per-keying estimability report (fraction of strata producing non-tied orientation values).
(d) Treat keyings with low estimability as structurally entangled.
(e) Prefer cell-level tertile binning over within-stratum re-binning.
(f) **Fixed-bin discipline**: bins used to define the tested signal must remain fixed across confound controls. If joint strata lack both low and high bins under that fixed definition, the signal is non-estimable rather than rescued by local re-binning.

Plus the v1.7 framing rule (`RA-SIM-ORIENT-KEYING-METHOD-001`): no orientation-overlap rescue claim should be cited unless it survives matched-graph extraction AND a shuffled overlap control.

## What is NOT retracted

The following remain valid (see `ra_confirmed_resilience_signatures_v1_9.md`):

- The matched-graph extraction methodology itself (v1.6 closed the v1.5 rescue/topology disconnection).
- The v1.1 audit machinery (decoupling, partial correlation, specificity, matched strata) -- this works correctly on real topology data; v1.5 demonstrated that.
- The v1.0/v1.2/v1.3/v1.4/concrete-graph qualitative Lean bridges (Type-valued refinement structure; no numerical orientation-rescue claim was ever asserted by the Lean side).
- The certification-rescue / certificate-correlation positive line (v0.7..v0.9.x) is independent of the orientation-overlap chain and remains intact.
- The v0.9.2 family-semantics asymmetry (`augmented_exact_k` carries the strong rescue signal vs `at_least_k`) is a v0.9-internal finding; it has NOT been independently confirmed by v1.x but it has also NOT been refuted -- the orientation-overlap mechanism failed to cross-validate it, but other mechanisms (e.g. direct certification correlation in v0.8.1) still support it as a v0.9-internal finding.

## What it would take to revisit

See `ra_open_native_witness_requirements_v1_9.md`.
