# RAKB-tagged TeX sources — Apr 28, 2026

This packet contains new TeX source files for the four canonical Relational Actualism papers with explicit, non-rendering RAKB IDs inserted as comments.

Each insertion has the form:

```tex
% RAKB: RA-ONT-001;RA-LLC-001
\subsection{From causal order to universe-state}
```

The annotations are comments only, so the rendered paper content should not change.

## Contents

```text
docs/RA_Canonical_Papers_RAKB_IDs/                 review copies with _rakb_ids suffix
docs/RA_Canonical_Papers_RAKB_IDs_drop_in_replacements/  same annotated content with original filenames
diffs/                                             unified diffs against uploaded canonical TeX
reports/                                           insertion log, file summary, unmatched rows
scripts/insert_rakb_tex_ids.py                     reusable insertion script
```

## Recommended workflow

Review the `_rakb_ids.tex` files first. If they look good, either copy the drop-in replacements into `docs/RA_Canonical_Papers/`, or apply the diffs manually.

The generated comments encode the Stage D curated paper-to-RAKB crosswalk. They are not new proof claims and do not promote restoration candidates into `claims.yaml`.
