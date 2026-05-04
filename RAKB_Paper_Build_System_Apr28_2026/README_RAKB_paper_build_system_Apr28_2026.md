# RAKB paper build system — Apr28 2026

This packet turns RAKB-tagged TeX generation into a repeatable workflow.

It assumes the generated-paper workspace lives under:

```text
docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/
```

That matches the path system where the RAKB TeX folder is inside `docs/RA_Canonical_Papers`.

## What this does

The generator reads the RAKB paper-to-node mapping and regenerates non-rendering TeX comments:

```tex
% RAKB: RA-ONT-001;RA-LLC-001
\subsection{From causal order to universe-state}
```

The canonical source of the mapping should be:

```text
docs/RA_KB/registry/source_text_references.csv
```

using rows whose `relation` is:

```text
canonical_tex_projection
```

with source labels like:

```text
Paper I — subsection: From causal order to universe-state
```

If the registry mapping is absent or not yet updated, the script can fall back to the Stage-D comment plan:

```text
docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/reports/RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv
```

## Install

From the repo root, copy the overlay:

```bash
cp -R <packet>/repo_overlay/* .
chmod +x docs/RA_KB/scripts/rakb_generate_tex_ids.py
chmod +x docs/RA_KB/scripts/rakb_extract_bibitems.py
```

## Regenerate RAKB IDs from the registry

From the repo root:

```bash
python docs/RA_KB/scripts/rakb_generate_tex_ids.py \
  --repo . \
  --output-root docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026 \
  --mapping-source registry \
  --drop-in \
  --fail-on-unmatched
```

Outputs:

```text
docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/generated_tex/
docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/drop_in_replacements/
docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/reports/
docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/diffs/
```

## Regenerate from the Stage-D plan instead

Use this only as a fallback/bootstrap path:

```bash
python docs/RA_KB/scripts/rakb_generate_tex_ids.py \
  --repo . \
  --output-root docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026 \
  --plan-csv docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/reports/RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv \
  --mapping-source plan \
  --drop-in \
  --fail-on-unmatched
```

## Review and drop in

Review the generated diffs first:

```bash
ls docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/diffs
```

Then replace the canonical TeX files:

```bash
cp docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/drop_in_replacements/*.tex \
   docs/RA_Canonical_Papers/
```

The script removes old `% RAKB:` comments and regenerates them from the current mapping. Do not hand-edit the comments in TeX; update the registry mapping instead.

## Compile

From `docs/RA_Canonical_Papers`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error *.tex
```

or compile generated copies:

```bash
cd docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/generated_tex
latexmk -pdf -interaction=nonstopmode -halt-on-error *.tex
```

## Makefile shortcuts

From `docs/RA_Canonical_Papers`:

```bash
make -f Makefile.rakb ids
make -f Makefile.rakb check-ids
make -f Makefile.rakb compile-generated
make -f Makefile.rakb bib-audit
```

## Updating RA-* IDs properly

1. Update `docs/RA_KB/registry/source_text_references.csv`.
2. Validate RAKB:
   ```bash
   cd docs/RA_KB
   python scripts/validate_rakb_v0_5.py
   ```
3. Regenerate TeX IDs using `rakb_generate_tex_ids.py`.
4. Inspect:
   ```text
   reports/rakb_tex_id_unmatched_mapping_rows.csv
   reports/rakb_tex_id_unmapped_sections.csv
   reports/rakb_tex_id_registry_id_warnings.csv
   ```
5. Compile.
6. Commit registry + generated TeX together.

## Style and bibliography layer

This packet also adds:

```text
docs/RA_Canonical_Papers/common/ra_suite.sty
docs/RA_Canonical_Papers/common/ra_references.bib
docs/RA_Canonical_Papers/latexmkrc
```

The style file is conservative and can be adopted later by replacing repeated preambles with:

```tex
\usepackage{common/ra_suite}
```

The bibliography file is a starter canonical `.bib`. The current papers still use inline `thebibliography`; do not automatically replace those until the bib audit is reviewed.

Generate a bibliography audit/seed file from current inline bibliographies:

```bash
python docs/RA_KB/scripts/rakb_extract_bibitems.py \
  --repo . \
  --out docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/reports \
  --bib-out docs/RA_Canonical_Papers/common/ra_references_seed_from_bibitems.bib
```

This produces an inventory of current `\bibitem` entries and a conservative BibTeX seed preserving their rendered text.

## Scope note

This system regenerates TeX annotations from RAKB and compiles the existing paper prose. It does not synthesize new prose from RAKB claims. That should remain a separate, reviewed editorial operation.
