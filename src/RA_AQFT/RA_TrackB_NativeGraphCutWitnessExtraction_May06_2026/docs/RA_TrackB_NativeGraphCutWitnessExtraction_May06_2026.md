# RA Track B.1: Native Graph/Cut Orientation Witness Extraction

Track A formalized the robust support-family and certification-family spine.
Track B begins the harder task: extracting native witness data from graph/cut
structure rather than from simulator row metadata or arbitrary keying.

The motivating failures were:

- v1.5's positive orientation-specificity signal was retracted.
- v1.6/v1.7 showed matched-graph orientation keying did not recover the signal.
- v1.8/v1.8.1 showed width/family-size/binning structure controls the apparent
  orientation gaps.

This packet therefore does not seek another orientation-rescue result.  It
instead introduces a graph/cut-local witness extraction interface that future
analyses must use before making any orientation-specific claim.

## New distinction

Bad/provenance-control witness:

```text
edge token + member_idx
```

Track B witness:

```text
graph incidence + cut vertices + depth/local orientation relation
```

The latter is member-index-free and can be mapped to the Lean orientation-closure
surface.

## Remaining gap

This packet still uses an operational DAG incidence extractor.  The next step is
to connect extracted witness records more directly to native RA declarations in
`RA_CausalOrientation_Core`, `RA_D1_NativeLedgerOrientation`,
`RA_D1_NativeClosure`, and `RA_D1_GraphCutCombinatorics` once the import hygiene
around the D1 chain is stable.
