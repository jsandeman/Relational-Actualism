# RAKB Python Computation Audit Packet — Apr 28, 2026

This packet starts Stage B of the RA audit: the Python computation layer.

It is designed to run locally inside the RA repository and produce RAKB-ready evidence tables without executing scientific scripts. The first pass is static by design: it inventories source files, imports, definitions, constants, numeric literals, IO calls, randomness, plotting, claim references, bridge-theory terms, and RA-native terms.

## Current status before Stage B

Lean Stage A is now structurally closed: the v5 upserts were applied, RAKB validation passed, and the D2-root Lake build completed successfully. The remaining Lean warning is the known unused `hN2` variable in `RA_D3_CosmologicalExpansion.lean`.

## Why Python gets a separate audit

Python files are not proof artifacts. They can support claims as:

- computational enumeration
- numerical benchmark
- visualization or report generation
- empirical target test
- candidate support only
- legacy/provenance script

The audit separates these roles so that `computes` and `reproduces` edges are not confused with Lean-verified proof edges.

## Install/use

Copy the script into your repository:

```bash
mkdir -p docs/RA_KB/scripts
cp scripts/ra_python_static_audit.py docs/RA_KB/scripts/
```

Run from the RA repo root:

```bash
python docs/RA_KB/scripts/ra_python_static_audit.py \
  --repo . \
  --out docs/RA_KB/reports/python_audit_Apr28_2026 \
  --roots src/RA_AQFT src/RA_Complexity data/DFT_Survey src/ra_audit.py
```

Then archive the resulting folder:

```bash
zip -r RA_python_audit_outputs_Apr28_2026.zip docs/RA_KB/reports/python_audit_Apr28_2026
```

## Generated outputs

The script writes:

```text
python_file_inventory.csv
python_import_edges.csv
python_declarations.csv
python_constants.csv
python_numeric_literals.csv
python_io_calls.csv
python_randomness.csv
python_plot_calls.csv
python_claim_refs.csv
python_bridge_terms.csv
python_call_edges.csv
python_audit_graph.jsonl
python_audit_report.md
```

## How to interpret evidence status

Use these status labels for RAKB Stage B:

```text
uploaded_static_audited
static_review_bridge_flags
static_review_ra_native
needs_execution_reproduction
execution_reproduced
candidate_support_only
legacy_or_provenance
```

Promote a Python script to `computes` or `reproduces` only after recording:

```text
command
working directory
Python version
package environment
inputs
outputs
random seed / determinism status
expected output hash or summary
claim IDs supported
```

## Recommended next source upload

Upload either:

```text
RA_python_computation_sources_Apr28_2026.zip
```

or, after running this audit locally:

```text
RA_python_audit_outputs_Apr28_2026.zip
```

The best next upload is both: source zip + audit-output zip.
