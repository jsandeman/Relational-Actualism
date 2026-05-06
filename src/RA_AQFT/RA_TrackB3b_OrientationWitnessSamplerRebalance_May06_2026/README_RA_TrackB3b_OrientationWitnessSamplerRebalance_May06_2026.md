# RA Track B.3b — Orientation-Witness Sampler / Topology Rebalance

This packet is a **coverage/sampler audit**. It does not compute or assert an orientation-rescue result.

Track B.3 showed that apparent v1.8.1-valid comparison domains came only from tainted/member-indexed or shuffled/null keyings. Track B.3b therefore searches available simulator settings using **legitimate native-witness keyings only**:

- `edge_pair_signed_no_member`
- `edge_direction_only`
- `incidence_role_signed`
- `catalog_augmented_edge_pair`
- `graph_cut_member_index_free`

The packet explicitly excludes the following from sufficiency counts:

- `member_indexed_edge_pair`
- `shuffled_overlap_control`

They can remain diagnostics in other packets, but they do not count as legitimate native-witness coverage.

## Demo result

The packet-local demo sweep produced:

```text
trial_rows = 8320
config_count = 16
legitimate_keying_count = 5
coverage_sufficient_cells_excluding_tainted_and_null = 0
max_high_bin_presence_rate = 0.45
posture = no_legitimate_keying_reaches_coverage_sufficiency_sampler_or_topology_redesign_needed
orientation_rescue_claim_made = false
```

This is a small demo, not a canonical run. Its value is to validate the search machinery and show the correct interpretation when no legitimate keying reaches coverage sufficiency.

## Canonical run

From the packet root:

```bash
python scripts/run_trackB3b_sampler_rebalance.py \
  --v0-9-simulator-dir ../RA_CausalDAG_MotifCommitSimulator_v0_9_NativeCertificateOverlap_May05_2026/simulator \
  --native-manifest-dir ../RA_CausalDAG_MotifCommitSimulator_v1_3_NativeOrientationLinkDerivation_May05_2026/outputs \
  --output-dir outputs \
  --seed-start 17 \
  --seed-stop 117 \
  --steps-values 32,48,64 \
  --max-targets-values 12,18,24,36 \
  --branch-probabilities 0.35,0.42,0.55 \
  --wide-join-probabilities 0.55,0.72,0.85 \
  --threshold-fractions 1.0,0.75,0.5,0.25 \
  --family-semantics augmented_exact_k,at_least_k \
  --min-rows-per-stratum 25
```

## Success criterion

A configuration is adequate only if all of the following hold:

1. At least one legitimate keying reaches coverage sufficiency.
2. Low and high bins coexist within support_width × family_size strata.
3. Rows per estimable stratum exceed the configured minimum.
4. Member-indexed keying is not counted.
5. Shuffled/null controls are not counted.
6. No orientation-rescue claim is made.

If no configuration works, the next step is not rescue analysis; it is an orientation-diverse graph/family generator redesign.
