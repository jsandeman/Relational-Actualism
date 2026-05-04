# Workflow summary

Canonical flow:

```text
RAKB registry/source_text_references.csv
        ↓
rakb_generate_tex_ids.py
        ↓
generated TeX with % RAKB comments
        ↓
latexmk compile
        ↓
paper PDFs + auditable TeX source
```

The RA-* comments are generated artifacts. The registry is canonical.

Use `--mapping-source registry` for normal operation.
Use `--mapping-source plan` only for bootstrapping from an exported Stage-D comment plan.
