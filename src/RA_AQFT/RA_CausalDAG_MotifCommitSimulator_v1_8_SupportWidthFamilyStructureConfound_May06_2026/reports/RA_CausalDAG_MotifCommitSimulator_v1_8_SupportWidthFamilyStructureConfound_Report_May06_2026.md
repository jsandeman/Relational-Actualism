# v1.8 Support-Width / Family-Structure Confound Audit Report

## Summary

v1.8 audits the likely confound identified by the v1.7 orientation-keying ablation: graph-derived orientation-overlap gaps match shuffled controls, so apparent low/high rescue gaps may be sorting artifacts induced by support width, family size, and orientation-bin construction.

## Scope

This packet is analysis-only:

- no new Lean module;
- no simulator semantic changes;
- no new actualization/rescue mechanism;
- no Nature-facing claim.

## Main diagnostics

The analysis computes:

1. support-width distribution by orientation bin;
2. family-size distribution by orientation bin;
3. rescue rate by support-width and orientation bin;
4. raw versus width-matched low/high gaps;
5. graph-derived versus shuffled control gaps within width-matched strata;
6. correlations between orientation bins and support-width/family-size.

## Packet-local finding

Against the packet-local v1.7 subset, low orientation bins are dominated by support-width 1 and high bins by support-width > 1. No support-width stratum contains both low and high bins, so width-matched low/high gap estimation is unavailable. This supports the hypothesis that the subset orientation gap is entangled with support-width/family structure.

## Canonical criterion

On the canonical v1.7 sweep, the important criterion is:

```text
If graph-derived and shuffled orientation gaps match within support-width and family-size strata, the orientation gap is a binning/family-structure artifact.
```

Conversely, a renewed orientation-specific hypothesis would require graph-derived keyings to differ from shuffled controls after width/family-size matching.
