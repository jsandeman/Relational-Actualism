# RA Native Active Root v3

## Strict active root

The active native root is now:

1. `RA_GraphCore_Native`
2. `RA_AmpLocality_Native`
3. `RA_BDG_Coefficient_Arithmetic`
4. `RA_MotifDynamics_Core`
5. `RA_CausalOrientation_Core`

## Why this is the right root

This root stays entirely inside:

- DAG structure and causal precedence
- BDG coefficient arithmetic
- local ledger conservation
- finite motif dynamics
- orientation / depth-ledger consequences

It excludes:

- AQFT / CFC / Unruh / on-shell adapters
- coupling overlays (`alpha_*`, `Koide`, etc.)
- field-equation and source-law bridge files
- quantum-information / thermodynamic overlays
- imported theory-label vocabulary as theorem targets

## Immediate in-repo landing order

1. land `RA_GraphCore_Native`
2. land `RA_AmpLocality_Native`
3. land `RA_BDG_Coefficient_Arithmetic`
4. swap `lakefile_native_strict_v3.lean`
5. only then continue theorem work in the active root

## Canonical naming rule

The active root should now speak in:

- ledger
- cut
- flux
- shield
- past
- interval
- extension order
- coefficient arithmetic
- motif
- orientation
- depth

and not in:

- horizon partition
- Markov blanket
- quantum measure
- gauge/coupling labels
- GR/QFT/SM bridge categories
