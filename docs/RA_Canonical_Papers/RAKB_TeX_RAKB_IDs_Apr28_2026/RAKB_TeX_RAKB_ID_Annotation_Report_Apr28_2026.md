# RAKB-ID TeX Annotation Report — Apr 28, 2026

Generated four canonical TeX sources with explicit, non-rendering RAKB ID comments.

## Summary

- Planned RAKB comment rows: 83
- Inserted RAKB comments: 83
- Unmatched plan rows: 0
- Annotation mode: TeX comments only (`% RAKB: ...`), so prose, equations, labels, citations, and rendered PDF output should be unchanged except for source comments.

## Files

- Paper I: `RA_Paper_I_Discrete_Spacetime_Actualization_BDG_Growth_Kernel_v9_2_final_Apr2026_rakb_ids.tex` — 26/26 comments inserted; unmatched=0
- Paper II: `RA_Paper_II_Emergent_Matter_Interaction_Discrete_Motif_Structure_v8_tiered_restored_Apr2026_rakb_ids.tex` — 21/21 comments inserted; unmatched=0
- Paper III: `RA_Paper_III_Discrete_Gravity_Cosmology_Causal_Severance_v9_tiered_restored_Apr2026_rakb_ids.tex` — 19/19 comments inserted; unmatched=0
- Paper IV: `RA_Paper_IV_Complexity_Life_Recursive_Closure_Discrete_Causal_Networks_v7_Apr23_2026_rakb_ids.tex` — 17/17 comments inserted; unmatched=0

## How to use

Copy the generated files from:

```text
docs/RA_Canonical_Papers_RAKB_IDs/
```

into your canonical paper directory when ready, or apply the unified diffs in:

```text
diffs/
```

The inserted comments are intentionally parser-friendly:

```tex
% RAKB: RA-ONT-001;RA-LLC-001
\subsection{From causal order to universe-state}
```

## Caveat

These comments encode the Stage D curated paper-to-RAKB crosswalk. They are not new proof claims and do not promote restoration candidates into `claims.yaml`.

## Drop-in replacement directory

For convenience, the packet also includes annotated TeX files with the original filenames:

```text
docs/RA_Canonical_Papers_RAKB_IDs_drop_in_replacements/
```

Use these only after reviewing the suffixed `_rakb_ids.tex` copies or the diffs.

## Compile check

All four `_rakb_ids.tex` files were checked with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error <file>
```

Result: all four passed. The packet does not include generated PDFs; it includes TeX sources, diffs, and reports only.
