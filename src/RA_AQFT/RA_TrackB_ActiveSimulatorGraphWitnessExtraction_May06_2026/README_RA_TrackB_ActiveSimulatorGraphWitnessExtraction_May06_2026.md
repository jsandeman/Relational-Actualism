# RA Track B.2 — Active Simulator Graph Witness Extraction (May 06, 2026)

This packet applies the Track B graph/cut orientation-witness extractor to **active v0.9 simulator graph states**.

It is infrastructure only. It makes no orientation-specific rescue claim.

## Purpose

Track B.1 built a graph/cut-local orientation witness surface on a packet-local tiny DAG. Track B.2 checks whether the same witness extraction discipline can be applied to the actual simulator graph states used in the v0.9 native-certificate-overlap workbench.

## Key guardrails

- Witness tokens are keyed by graph incidence, cut vertices, and local depth/parity structure.
- Witness tokens must not include support-family member indices.
- Fixed-bin discipline is preserved for later confound audits.
- The packet reports coverage / estimability only; it does not compute rescue outcomes.

## Included demo

The packet-local demo used v0.9 simulator code available in this workspace:

```text
seeds = 17..20
steps = 16
max_targets = 6
threshold_fractions = 1.0,0.75,0.5,0.25
family_semantics = at_least_k,augmented_exact_k
```

Summary:

```text
witness_rows = 456
overlap_rows = 192
active_orientation_overlap_bins = low;medium
support_width_classes = 1;2;3;4
family_size_classes = 1;3;4;5;7;11;15
graph_surface_member_index_free = true
bad_control_detects_member_index_instability = true
estimable_width_family_strata = 0
orientation_rescue_claim_made = false
```

The lack of high-bin coverage in this demo is not a scientific result. It is a coverage/estimability diagnostic showing what later active-state runs must populate before any orientation-rescue analysis can be attempted.

## Canonical usage

```bash
python scripts/run_trackB_active_graph_witness_extraction.py \
  --v0-9-simulator-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/simulator \
  --output-dir outputs \
  --seed-start 17 \
  --seed-stop 117 \
  --steps 32 \
  --max-targets 12 \
  --threshold-fractions 1.0,0.75,0.5,0.25 \
  --family-semantics at_least_k,augmented_exact_k
```

## Outputs

- `ra_trackB2_active_graph_witness_members.csv`
- `ra_trackB2_active_graph_orientation_overlap.csv`
- `ra_trackB2_member_index_audit.csv`
- `ra_trackB2_fixed_bin_coverage.csv`
- `ra_trackB2_width_family_estimability.csv`
- `ra_trackB2_active_graph_witness_summary.csv`
- `ra_trackB2_active_graph_witness_summary.md`
- `ra_trackB2_active_graph_witness_state.json`

## RAKB posture

The proposed claims are infrastructure claims. They should not be read as evidence for orientation-specific rescue. Future rescue claims still require the v1.9 native-witness requirements: active-state witness extraction, fixed-bin confound discipline, shuffled controls, partial-correlation controls, canonical scale, and no member-index artifact.
