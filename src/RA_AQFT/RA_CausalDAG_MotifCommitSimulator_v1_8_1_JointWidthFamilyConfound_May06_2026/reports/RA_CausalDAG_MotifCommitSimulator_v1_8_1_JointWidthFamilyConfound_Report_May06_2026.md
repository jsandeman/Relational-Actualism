# RA v1.8.1 Joint Width × Family-Size Confound Audit Report

## Purpose

v1.7 canonical keying ablation invalidated the v1.5 positive orientation-specificity interpretation under matched-graph extraction, but v1.8 showed that a graph-derived low/high orientation-overlap gap can survive support-width-only matching while the shuffled-control gap does not. v1.8 also found strong association between orientation-overlap bins and family size.

v1.8.1 adds exact `support_width × family_size` matching to determine whether the residual v1.8 graph-derived gap survives the next confound control.

## Status

- Analysis-only packet.
- No Lean changes.
- No simulator semantic changes.
- No new orientation-link keying.
- Python tests pass.

## Packet-local result

The packet-local run used the small v1.7 subset bundled in this workspace:

```text
input_rows = 1152
keying_count = 6
width_classes = 1;2;3;4
family_size_classes = 1;3;4;7;11
selector_guardrail_passed = true
estimable_joint_group_fraction_graph = 0.0
v1_8_1_posture = joint_width_family_matching_not_estimable_redesign_sampler_needed
```

This is expected for the small subset and should not be promoted as a canonical result. It demonstrates that the analysis correctly distinguishes a non-estimable design from a positive or negative orientation-specific result.

## Canonical interpretation discipline

The canonical v1.7 outputs should be analyzed before any RAKB claim is promoted.

Possible outcomes:

1. **Residual graph-derived gap survives joint matching and differs from shuffled controls.**
   This supports a candidate residual graph-derived orientation association, still not a Nature-facing law.

2. **Residual graph-derived gap shrinks and matches shuffled controls.**
   This supports a support-width/family-size confound explanation.

3. **Joint matching is not estimable.**
   The sampler lacks sufficient overlap-bin support within joint strata; a redesigned matched sampler is needed.

## Guardrail

Do not promote a positive or negative orientation-specificity claim from raw or width-only gaps when family-size remains associated with orientation-overlap bins.
