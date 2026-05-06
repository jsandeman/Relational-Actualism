# Track B.3b Orientation-Witness Sampler / Topology Rebalance

## Purpose

Track B.3 showed that the active witness extractor works, but legitimate native-witness keyings did not reach v1.8.1 coverage sufficiency. Track B.3b searches simulator configurations for legitimate v1.8.1-valid comparison domains.

This packet is deliberately infrastructure-only. It does not test or assert orientation-specific rescue.

## Method

For each simulator configuration, the packet:

1. Builds active v0.9 simulator graph states.
2. Extracts graph/cut orientation witnesses using legitimate keyings only.
3. Computes all-pairs and parent-anchored orientation-overlap diagnostics.
4. Assigns fixed absolute low/medium/high bins.
5. Tests support_width × family_size strata for low/high co-presence.
6. Counts coverage sufficiency only for legitimate keyings.

## Key exclusion rule

Tainted and null keyings do not count toward sufficiency:

- `member_indexed_edge_pair` is retracted/tainted.
- `shuffled_overlap_control` is a null control.

## Packet-local demo

The included demo found no coverage-sufficient legitimate cells across 16 small configurations. The strongest high-bin presence rate was 0.45, but no joint support_width × family_size stratum contained adequate low/high support under the configured minimum.

## Interpretation

A failure to find adequate coverage is not an orientation-rescue result. It means the current simulator configuration space does not support the comparison domain required by v1.8.1.

## Next step on failure

If the canonical run also fails, proceed to an orientation-diverse topology/family generator rather than a rescue analysis.
