# RA_BaryonChirality Native Audit v1

## Bottom line

`RA_BaryonChirality.lean` does contain real native content, but the file should not remain in the active root under its current name or vocabulary.

The genuine native content is:

1. DAG acyclicity forbids reverse causal precedence.
2. The reverse winding profile `(1,1,1,0)` is filtered while the forward profile `(1,1,0,1)` is stable.
3. The depth-2 ledger count is preserved across the classified long-lived motif extensions.

What must be removed from the active root is the imported framing:

- `baryon`
- `parity violation`
- `gluon`
- `quark`
- comparison language about the Standard Model

## Recommended replacement

Replace the file by `RA_CausalOrientation_Core` with two top-level outputs:

- `orientation_one_way`
- `orientation_and_depth2_ledger_core`

These preserve the underlying arithmetic and DAG content while removing imported categories.

## Status by declaration

- `no_backward_edge`: keep (optionally rename to `no_reverse_precedence`)
- `maximal_parity_violation`, `chirality_maximal`: rewrite into orientation language
- `particle_n2_values`, `gluon_n2_preserved_all`, `quark_*`: rewrite into motif / depth-2-ledger language
- `D3_chirality_and_baryon`: replace by a split theorem pair rather than keeping the imported composite statement
