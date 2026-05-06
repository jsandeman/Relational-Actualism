# RA CausalDAG MotifCommitSimulator v1.7 — Orientation-Keying Ablation

## Purpose

v1.6 closed the rescue/topology disconnection from v1.5, but its orientation-link extractor used member-indexed tokens. v1.7 is a forensic keying-ablation packet: it replays matched v0.9 trials and computes orientation-link overlap under multiple graph-coupled keying schemes.

This packet does **not** introduce new Lean semantics and does **not** make a Nature-facing claim. It asks whether v1.6's negative/reversed orientation-specificity result is stable across reasonable graph-derived keyings or partly induced by member-indexed tokenization.

## Keying variants

- `member_indexed_edge_pair`: v1.6 behavior / provenance control.
- `edge_pair_signed_no_member`: graph/depth signed edge-pair tokens without member index.
- `edge_direction_only`: directed incidence only.
- `incidence_role_signed`: parent/child role plus graph/depth sign, no member index.
- `catalog_augmented_edge_pair`: no-member edge-pair tokens plus native theorem-catalog tokens.
- `shuffled_overlap_control`: deterministic null/control tokens.

## Run command

```bash
python scripts/run_orientation_keying_ablation_v1_7.py \
  --v0-9-simulator-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/simulator \
  --native-manifest-dir ../RA_CausalDAG_MotifCommitSimulator_v1_3_NativeOrientationLinkDerivation_May05_2026/outputs \
  --output-dir outputs \
  --seed-start 17 \
  --seed-stop 21 \
  --max-targets 8 \
  --severance-seeds 101 \
  --modes ledger_failure,orientation_degradation,selector_stress \
  --severities 0.5 \
  --threshold-fractions 0.5 \
  --family-semantics at_least_k,augmented_exact_k
```

A larger canonical sweep should increase seeds, severance seeds, severities, and thresholds.

## Interpretation guardrail

No orientation-specific rescue claim should be promoted unless it survives matched-graph extraction under non-member graph/native keyings at canonical scale.

Possible outcomes:

1. **All keyings fail or reverse**: v1.5 orientation-specificity likely does not survive matched-graph extraction.
2. **Only member-indexed keying fails/reverses**: v1.6 reversal may be keying artifact.
3. **Catalog/native-like keying recovers signal**: orientation specificity may require native sign-source enrichment rather than edge-pair topology alone.
