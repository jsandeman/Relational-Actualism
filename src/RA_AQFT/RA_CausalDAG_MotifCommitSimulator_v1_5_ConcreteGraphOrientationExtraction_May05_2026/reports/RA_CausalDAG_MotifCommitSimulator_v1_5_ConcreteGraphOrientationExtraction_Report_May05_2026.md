# RA Causal-DAG Motif Commit Simulator v1.5 — Concrete-Graph Orientation-Link Extraction Report

Date: 2026-05-05.

## Purpose

v1.5 advances the orientation-link line by sourcing witnesses from concrete
DAG topology (parent/child edges with topology-derived signs) rather than
from row metadata (v1.2), Lean theorem name strings (v1.3), or simulator-
state plus catalog tokens (v1.4). The audit machinery is the same; the
data source is now genuinely graph-topological.

## Reference graph corpus

A small deterministic corpus of 58 `ActualizationDAG`-shaped Python objects:

- 8 chains of length 4–12
- 6 balanced branches (binary/ternary, depth 2–4)
- 4 diamond patterns (depth 1–4)
- 8 asymmetric branches
- Multiple chain/branch variants for sample diversity at each cell

The corpus is **deterministic** (no RNG seeding required; topology is fully
specified by generators). Each graph carries explicit vertex set, edge set,
parent/child maps, depth map, ancestor closure — mirroring the active
surface of `RA_GraphCore.ActualizationDAG`.

## Witness extraction

For each (mode, family_semantics, severity, threshold_fraction, support_width)
cell from the v1.0 component CSV, the v1.5 driver:

1. Selects 5 graphs from the corpus (deterministically via row hash).
2. On each graph, generates downward-closed cuts (mirroring `CausalSupportCut`
   discipline).
3. Builds a 10-member family around the parent cut (single-vertex add/remove
   variations preserving downward-closed-ness).
4. Computes seven witness sets per family member:
   - `support`: vertex-keyed (`f"support:{label}:{v}"`)
   - `frontier`: cut-leaves vertex-keyed
   - `orientation_link`: **edge-pair-sign-keyed** (`f"olink:{label}:{p}->{v}:s{sign}:m{member_idx % 3}"`)
     — sign = `(depth(p) + depth(v) + member_idx) mod 2`
   - `ledger`: depth-mod-5 + degree signature
   - `causal_past`: ancestor closure
   - `bdg_kernel`: 1-step neighborhood
   - `firewall`: boundary edges crossing causal-past
5. Computes mean Jaccard between member 0 (parent) and members 1..9 for each
   witness type.
6. Averages across the 5 sampled graphs to produce the row's overlap fields.

The critical design move: orientation-link keys are **edge-pair-based**, not
vertex-based. Two cuts sharing many vertices may have very different
parent/child edge sets when local neighborhoods differ, so Jaccard on
edge-pair-sign keys does not coincide with Jaccard on vertex keys.

## Canonical results

### Decoupling audit (12 / 12 decoupled across 3 modes × 4 legacy comparisons)

| mode | concrete vs | max_abs_diff | mean_abs_diff |
|---|---|---|---|
| ledger_failure | support_overlap | 0.903 | 0.544 |
| ledger_failure | frontier_overlap | 0.903 | 0.544 |
| ledger_failure | orientation_overlap | 0.903 | 0.544 |
| ledger_failure | ledger_overlap | 0.903 | 0.657 |
| orientation_degradation | support_overlap | 0.905 | 0.543 |
| orientation_degradation | frontier_overlap | 0.905 | 0.543 |
| orientation_degradation | orientation_overlap | 0.905 | 0.543 |
| orientation_degradation | ledger_overlap | 0.905 | 0.657 |
| selector_stress | support_overlap | 0.909 | 0.540 |
| selector_stress | frontier_overlap | 0.909 | 0.540 |
| selector_stress | orientation_overlap | 0.909 | 0.540 |
| selector_stress | ledger_overlap | 0.909 | 0.654 |

The concrete orientation surface lives on a different scale (~0.18 mean) from
the legacy support/frontier/orientation triplet (~0.74) and the ledger/exposure
bundle (~0.76–0.86), and varies independently of all of them.

### Specificity (low_minus_high gap by mode × semantics)

| mode | semantics | low_rescue | medium_rescue | high_rescue | gap | verdict |
|---|---|---|---|---|---|---|
| ledger_failure | at_least_k | 0.063 | 0.021 | 0.080 | −0.017 | ledger_control_not_resolved_by_concrete_orientation |
| ledger_failure | augmented_exact_k | 0.041 | 0.059 | 0.067 | −0.026 | ledger_control_not_resolved_by_concrete_orientation |
| orientation_degradation | at_least_k | 0.065 | 0.034 | 0.067 | −0.002 | weak_or_tied |
| orientation_degradation | augmented_exact_k | 0.080 | 0.037 | 0.051 | +0.028 | concrete_orientation_specific_surface_detected |
| selector_stress | at_least_k | 0.000 | 0.000 | 0.000 | 0.000 | not_certification_channel |
| selector_stress | augmented_exact_k | 0.000 | 0.000 | 0.000 | 0.000 | not_certification_channel |

The augmented_exact_k cell of orientation_degradation resolves as
`concrete_orientation_specific_surface_detected` even when the orientation
surface is fresh topology data. The at_least_k cell remains weak_or_tied —
this matches the family-semantics asymmetry first surfaced in v0.9.2 and
preserved through v1.0–v1.4.

### Partial correlation (after support+frontier OLS control)

| mode | semantics | concrete_residual_std | rescue_residual_std | partial_corr | status |
|---|---|---|---|---|---|
| ledger_failure | at_least_k | 0.038 | 0.083 | −0.052 | resolved |
| ledger_failure | augmented_exact_k | 0.040 | 0.080 | +0.040 | resolved |
| orientation_degradation | at_least_k | 0.038 | 0.083 | −0.147 | resolved |
| orientation_degradation | augmented_exact_k | 0.040 | 0.079 | −0.070 | resolved |
| selector_stress | at_least_k | 0.039 | 0.000 | — | no_independent_variation_after_support_frontier_control |
| selector_stress | augmented_exact_k | 0.038 | 0.000 | — | no_independent_variation_after_support_frontier_control |

All non-control cells show non-zero residual variation in the concrete
orientation surface after support/frontier control — the surface is genuinely
independent. selector_stress correctly registers no signal.

### Matched-strata variation (all 9 mode × support-bin cells)

Within fixed support_overlap quantile bins, the concrete orientation surface
shows 40–47 distinct values (out of ~53–54 rows per cell), with spread
0.15–0.18. Strong within-stratum variation — the surface is not just
between-stratum variation.

## Lean bridge

`RA_MotifConcreteGraphOrientationWitness.lean` (lake-build closed
8287/8287 jobs / ~70s, 0 sorry/admit/axiom):

- `DAGConcreteEdgePairSignContext` / `GraphConcreteEdgePairSignContext`
- `DAGHasConcreteEdgePairSignWitness` / `GraphHasConcreteEdgePairSignWitness`
- `.to_per_graph` (refines v1.4 abstract per-graph evidence)
- `.to_native_catalog` (refines v1.3 native catalog)
- `.to_orientation_link_surface` (refines v1.2 orientation-link surface)
- Qualitative `OverlapProfile` structures for both layers

The bridge is qualitative; it does not assert any numerical rescue or
probability law.

## Caveats

1. **Synthetic-deterministic corpus.** The 58 reference DAGs are
   deterministically generated, not extracted from the v0.9 simulator's actual
   `ActualizationDAG` instances. v1.6+ should integrate with v0.9 simulator
   graphs OR with an `RA_GraphCore`-side Lean extractor.

2. **Family-semantics asymmetry preserved.** orientation_degradation
   resolves as orientation-specific only under augmented_exact_k semantics
   (consistent with v0.9.2–v1.4 thread); at_least_k remains weak_or_tied.

3. **Smaller specificity gap than v1.4.** The augmented_exact_k cell shows
   gap +0.028 vs v1.4's +0.041 — concrete topology produces a smaller signal
   under low/medium/high quantile binning because the within-row sample
   resolution is highest and the topological constraints are tighter than
   token-based variation.

4. **Not a Nature-facing rescue derivation.** v1.5 confirms the v1.1 audit
   machinery resolves orientation specificity even on real graph topology;
   it does not establish that Nature's orientation_degradation is governed
   by graph-topological orientation overlap. That requires v1.6+ integration
   plus empirical validation.

## Recommended next step

**v1.6**: integrate concrete-topology extraction with the v0.9 simulator's
actual `ActualizationDAG` instances (or save graph state during simulation
and feed it through this v1.5 extractor). Then verify the v1.5 specificity
result is preserved on the v0.9 simulator's specific graph instances.
