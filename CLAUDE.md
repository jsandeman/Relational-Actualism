# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A research repository for **Relational Actualism (RA)** — a discrete-causal-graph framework for fundamental physics. Unlike a typical software project, this repo is a four-format scientific artifact:

- **Lean 4 / Mathlib proofs** (`src/RA_AQFT/`) — formally verified theorems
- **Python computational artifacts** (`src/RA_AQFT/*.py`, `src/RA_Complexity/`, `data/DFT_Survey/`) — derivations, enumerations, numerical checks
- **Julia simulator** (`src/RAGrowSim/`) — RA growth dynamics on DAGs
- **Canonical LaTeX papers** (`docs/RA_Canonical_Papers/`) — Papers I–IV plus archived versions
- **RAKB (RA Knowledge Base)** (`docs/RA_KB/`) — a typed registry that wires the above together and tracks epistemic status

Most non-trivial work touches *two or more* of these formats and must keep them consistent via the RAKB registry. Read the RAKB section before editing claims, papers, or proofs.

## Build / test commands

### Lean proofs (`src/RA_AQFT/`)
```bash
cd src/RA_AQFT && lake build
```
Toolchain pinned in `lean-toolchain` (currently `leanprover/lean4:v4.29.0`). Active proof roots are listed in `lakefile.lean` under three tiers (A bedrock / B native content / C flagged); the docstring at the top of `lakefile.lean` explains why specific files have been retired or renamed and is the authoritative map of what is currently in scope. `lakefile_v1.lean` is a kept-around prior config — don't edit it.

### Julia simulator (`src/RAGrowSim/`)
```bash
cd src/RAGrowSim
julia --project=. test/runtests.jl                            # full test suite
julia --project=. scripts/run_seeded.jl chain4 12 30          # single seeded run
julia --project=. scripts/run_measure_comparison.jl           # run-comparison driver
```

### RAKB validation (`docs/RA_KB/`)
```bash
python docs/RA_KB/scripts/validate_rakb_v0_5.py               # structural validator
```
The `scripts/` directory also holds many one-shot `apply_*_upserts.py` migration scripts — these are historical, not part of a CI loop.

### Paper RAKB-ID regeneration (`docs/RA_Canonical_Papers/`)
```bash
cd docs/RA_Canonical_Papers
make -f Makefile.rakb ids                # regenerate "% RAKB:" comments from registry
make -f Makefile.rakb check-ids          # verify all references resolve
make -f Makefile.rakb compile-generated  # latexmk on generated_tex/
make -f Makefile.rakb bib-audit          # extract bibitems → common/*.bib
```
Never hand-edit `% RAKB:` comments in TeX — regenerate them from `docs/RA_KB/registry/source_text_references.csv` (rows with `relation = canonical_tex_projection`).

## RAKB conventions (read before editing claims, proofs, or papers)

The RAKB is the source of truth that ties Lean files, Python scripts, and TeX sections to typed claim nodes. The active version is **v0.5.1**.

### Registry layout (`docs/RA_KB/registry/`)
- `claims.yaml` — active foundations and proven results
- `issues.yaml` — open formalization targets
- `targets.yaml` — empirical predictions and benchmarks
- `framing.yaml` — translation/non-target policies (e.g. "Born rule is non-target")
- `artifacts.csv` — file-level inventory with sha256 / git_sha
- `claim_artifact_edges.csv` — claim → supporting artifact
- `claim_edges.csv` — proof dependencies between claims (active only)
- `all_dependency_edges.csv` — full edge set incl. issue/target edges
- `source_text_references.csv` — TeX section ↔ claim mapping (drives `% RAKB:` regeneration)
- `restoration_candidates.csv` — content not yet promoted to active claims

The `*.bak_YYYYMMDD_HHMMSS` files in `registry/` are upsert-script backups, not active state. `archive/` holds prior monolithic registries (legacy `RA_results_master_v0_*.yaml`).

### Epistemic status taxonomy (from `RAKB_New_Session_Prompt`)
When classifying a result, use these tags — they encode how strongly Nature backs the claim:
- **LV / lean_build_confirmed** — machine-checked in Lean
- **DR** — derived in RA-native terms, not machine-checked
- **CV / computes** — computation-verified or numerically reproduced
- **PI** — phenomenological interpolation or bridge
- **CN** — conjecture with stated path to closure
- **bridge / cartography** — translation only, not mechanism
- **restoration_candidate** — potentially important but not promoted
- **archived / historical** — provenance only

### RA framing discipline
The target is Nature, not one-to-one recovery of SM/QFT/GR categories. Continuum or legacy vocabulary is allowed as **translation**, not mechanism. Mechanisms must trace to DAG + BDG + LLC + actualization, plus Nature-measurements. If a new result is not fully source-backed, put it in `restoration_candidates.csv`, `issues.yaml`, or `targets.yaml` rather than promoting it directly into `claims.yaml`.

### When making a registry change
1. State which files you inspected.
2. State whether the change touches claims, targets, issues, source_text_references, artifacts, claim_artifact_edges, or restoration_candidates.
3. Express upserts as CSV rows, not prose.
4. Re-run `validate_rakb_v0_5.py` after the change.
5. Regenerate paper RAKB IDs (`make -f Makefile.rakb ids`) so TeX stays synchronized.

## Other directories

- `relational-actualism-web/` — single-file static site for relationalactualism.org. No build step; deploy `index.html` directly.
- `RAKB_Build_Instructions_Apr28_2026_Packet/` and `RAKB_Paper_Build_System_Apr28_2026/` — operational packets containing the canonical "new session" prompt and the paper-build overlay. The `repo_overlay/` of the latter is the upstream of `docs/RA_KB/scripts/rakb_generate_tex_ids.py` and the `Makefile.rakb`.
- `docs/RA_History/`, `docs/RA_Logs/`, `docs/RA_Submitted_Paper_Versions/` — provenance only. Do not treat as authoritative for current claims.
- `data/DFT_Survey/` — B3LYP/6-311+G* thermochemistry inputs/outputs and the assembly-index mapper, supporting the complexity papers.

## Key open problems (from README / CONTRIBUTING)

These are the load-bearing gaps; flag any work that bears on them:
- Intrinsic discrete proof of **amplitude locality** (currently an axiom in `RA_AmpLocality.lean`)
- Covariant RA field equations / Bianchi compatibility on curved backgrounds
- Continuum limit: type III₁ AQFT extension
- Causal Firewall limit theorem ($\lambda \cdot \tau_d \cdot l^3 = 1$)

## GitHub-side responses (Claude GitHub app, Claude Code Action)

If you are responding to a GitHub event (PR comment, issue, review request)
rather than to a local user in Claude Code, also read `.github/CLAUDE.md`.
It holds rules tightened for asynchronous, no-human-in-the-loop responses
— in particular: never push to `main`, never modify the registry in a
review-only comment, never invent registry node IDs, and never inflate
epistemic-status tags (LV/DR/CV) for PRs that don't meet the bar.

## Things to avoid

- Don't edit the many `*.bak_*` files in `docs/RA_KB/registry/` — they are upsert-script backups.
- Don't promote a result into `claims.yaml` without LV/DR/CV evidence; route it through `issues.yaml`, `targets.yaml`, or `restoration_candidates.csv`.
- Don't hand-edit `% RAKB:` comments in TeX — regenerate from the registry.
- Don't reactivate retired Lean roots (see `lakefile.lean` docstring) without restating the reason for retirement.
