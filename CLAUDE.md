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

## RAKB packet-application workflow

Packets that arrive under `src/RA_AQFT/<Name>_FormalBridge_<Date>/` or `docs/RA_KB/<Name>_<Date>/` typically ship `lean/`, `patches/`, `scripts/apply_*.py`, `registry_proposals/`, and `reports/`. The apply scripts assume a flatter or older registry shape than the active RAKB v0.5; do not run them blindly. Workflow:

1. **Inspect first.** Read the apply script and every file under `registry_proposals/`. Verify which target files the script writes (`claims.csv` vs `claims.yaml`, etc.) and what its key fields are.
2. **Dry-run.** Every apply script has `--dry-run`. Use it.
3. **Lean install:** copy the module + patch the lakefile via the script. Then *manually inspect* the lakefile around the insertion point — apply scripts consistently insert mid-comment-block (between `` `Foo, `` and its dangling `--` continuation lines) and need rejoining.
4. **Lake build before promoting status.** Lean toolchain is at `/Users/jsandeman/.elan/bin/lake`; you can compile. Run `lake build <ModuleName>` from `src/RA_AQFT/` to get full Tier-B closure. Do **not** rely on the prior session's "user_local_compile_confirmed" — refresh stale `.olean`s by rebuilding the upstream first if needed.
5. **Consult `framing.yaml` before designing claims or metrics.** When designing new claims or metrics in a packet series, scan `framing.yaml` for relevant `*-METHOD-*` entries first — they encode vocabulary discipline, layer-separation invariants, and metric-design rules established by prior audits. Don't reintroduce terms or comparison patterns those entries explicitly proscribe.
6. **Translate proposals into the active schema** rather than running the proposals-apply script. Specifically:
   - claim entries → `claims.yaml` (NOT `claims.csv`); fill in **all** v0.5 fields (see schema reference below).
   - methodological/modeling guardrails → `framing.yaml` with `framing_kind: methodological_guardrail | modeling_guardrail`, NOT `claims.yaml`.
   - artifacts → `artifacts.csv` with the active 14-column header.
   - edges → `claim_artifact_edges.csv` (12 columns, watch for unquoted commas in `claim_name`).
   - dependencies → both `claim_edges.csv` and `all_dependency_edges.csv`. Strip file-name "deps" (only claim IDs go in edge files).
7. **Status promotion rule.** If `lake build` closes with no `sorry`/`admit`/`axiom`, promote the packet's `source_level_*_pending_compile` to `proof_status: lean_verified_or_compiled_native` and `source_status: {<file>: lean_build_confirmed_no_sorry_no_admit_no_axiom}`. If only `lake env lean <file>.lean` succeeds (without `lake build`), use `user_local_lean_env_compile_confirmed_no_sorry_no_admit_no_axiom` for the file source_status.
8. **Backups.** Make `*.bak_YYYYMMDD_HHMMSS` for every registry file you modify. Never edit the existing `*.bak_*` files.
9. **Validate.** `python scripts/validate_rakb_v0_5.py` from `docs/RA_KB/`. The validator FAILS on missing `artifact_id` in `claim_artifact_edges`; it WARNS on missing claim_id, so warnings are real bugs. Common cause of false fails: an unquoted comma in `claim_name` shifts CSV columns — quote names containing commas.
10. **Regen paper IDs.** `cd docs/RA_Canonical_Papers && make -f Makefile.rakb ids`. Expect 0 `id_warnings`. `unmapped_sections: 95` is pre-existing, ignore.
11. **Don't track `.DS_Store`.** Packet zips often carry one at the root. The repo has zero tracked `.DS_Store`. Stage subdirectories explicitly when adding a packet.
12. **Don't push to `main`.** Direct push is policy-denied. Either open a PR (`gh pr create`) or hand the push back to the user; do not chase workarounds.

## RAKB v0.5 active-schema reference

Use these exact field names — apply scripts often use leaner schemas; reject those.

**`claims.yaml` entry** (top-level shape: `{registry_version: ..., claims: [...]}`):
```yaml
- id: <RA-…>                               # unique across all node sets
  name: <one-line>
  domain: <kernel|matter|gravity|complexity|framing>
  papers: [I|II|III|IV, ...]
  statement: <prose>
  nature_targets: [<...>]
  ra_observable: <name|null>
  sources: [<file or doc names>]
  proof_dependencies: [<RA-… ids only>]
  framing_links: [<RA-METHOD-/RA-NONTARGET-/RA-…-METHOD-…>]
  restoration_preconditions: []
  caveats: <prose>
  next_tasks: []
  source_status:
    <filename>: <lean_build_confirmed_no_sorry_no_admit_no_axiom |
                 user_local_lean_env_compile_confirmed_no_sorry_no_admit_no_axiom |
                 lean_env_compile_confirmed_no_sorry_no_admit_no_axiom>
  legacy_proof_status: <ANC|DR|STATED|...>
  proof_status: <axiom_or_stated_foundation |
                 lean_verified_or_compiled_native |
                 interpretive_formal_bridge | ...>
  legacy_support_status: <none|...>
  auxiliary_support_status: <none_recorded|...>
  claim_kind: <foundation | formalized_result | derived_result | interpretive_bridge>
  formal_anchor: <Lean-decl-list joined by ' ; '>
  packet_origin: <packet directory name>      # for claims added via packet
```

**`framing.yaml` entry** (top-level shape: `{registry_version: ..., framing_policies: [...]}`). Differences from claims:
- No `proof_status`; use `legacy_proof_status` only.
- Use `framing_kind: <negative_scope_or_translation_policy | methodological_guardrail | modeling_guardrail>` instead of `claim_kind`.
- `auxiliary_support_status: methodological_guardrail_recorded | modeling_discipline_recorded | comparative_cartography`.

**`artifacts.csv` header** (14 columns):
```
artifact_id,filename,type,status,artifact_role,supports_results,repo_relative_path,sha256,git_sha,path_observed,notes,migration_note,path,role
```
- `supports_results` is `;`-joined claim IDs.
- `type` examples: `lean`, `md`, `diff`, `dir`, `log`, `zip`.
- Common `artifact_role`: `formal_source`, `formalization_module`, `formal_bridge_report`, `bridge_mapping`, `methodology_report`, `packet_provenance`, `lakefile_patch`, `source_audit`.

**`claim_artifact_edges.csv` header** (12 columns):
```
claim_id,claim_name,claim_node_type,artifact_id,filename,artifact_type,relation,source_span,verification_status,notes,node_type,type
```
- `claim_node_type`: `claim` for claims.yaml entries, `framing` for framing.yaml entries (the validator union of node sets accepts both).
- `relation` examples: `formal_anchor`, `proves`, `formal_source`, `formal_bridge_report`, `bridge_mapping`, `compile_confirmation_report`, `lakefile_patch`, `methodological_anchor`, `packet_provenance`, `source_audit`.
- **Quote `claim_name` if it contains a comma** — otherwise CSV column-shift bugs the validator.

**`claim_edges.csv` / `all_dependency_edges.csv` header** (7 columns):
```
src,dst,kind,src_node_type,dst_node_type,src_name,dst_name
```
- `kind` used so far: `proof_dependency`, `interpretive_dependency`.
- `claim_edges.csv` strictly enforces `src/dst ∈ claims.yaml` (validator FAILS on misses).
- `all_dependency_edges.csv` is broader — claims/issues/targets/framing all valid.

## Recurring Lean-module fixes for packet sources

1. **`Σ` is reserved.** Lean 4 reserves `Σ` for the dependent-pair (`Sigma`) binder; packet authors keep using it as an identifier for "selector closure". Run a `Σ → S` rename across the whole installed module before `lake build`. Recompute SHA after.
2. **`Type`-valued witnesses can't sit under `And` in `Prop`.** When a packet writes `∃ …, P ∧ MyWitnessStruct M₁ M₂ ∧ Q` and `MyWitnessStruct` is a `structure` (so `Type`, not `Prop`), wrap with `Nonempty (…)` and on the proof side wrap the call with an anonymous constructor `⟨…⟩`. Don't try to make the structure a `Prop` — it's intentionally `Type` so downstream code can pattern-match the witness data.
3. **Stale `.olean`s.** If you edit an upstream module, downstream `lake env lean <new>.lean` may report nonsense errors (e.g. "field `supports` does not exist") because the cached olean is from before the edit. Run `lake build <upstream-module>` first to refresh, then check the new module.
4. **Lakefile insertion is mid-comment-block.** The apply scripts insert `` `NewModule, `` immediately after `` `OldModule, `` whose comment continues on the next 2–3 lines (`-- …`). Result: the new entry appears between `OldModule` and its own comment continuation, which then visually attaches to the new entry. Manual fix: move the new entry below the dangling `--` lines and give it its own short comment.
5. **`lexical check: no sorry/admit/axiom`** is necessary but not sufficient. Always also run `lake build`.
6. **`chainScore` collision in D1 native modules (resolved 2026-05-05 — RA-ISSUE-LEAN-CHAINSCORE-001).** `RA_D1_Core` and `RA_D1_NativeKernel` historically both defined `chainScore`/`bdgScore`/`chain_score_via_bdg_*` in the root namespace, so any module importing both transitive chains failed with `environment already contains 'chainScore.match_1'`. The fix wrapped the entire content of `RA_D1_NativeKernel.lean` in `namespace D1Native ... end D1Native`, and added `open D1Native` to the four files that use those identifiers unqualifiedly (`RA_D1_NativeConfinement`, `RA_D1_NativeClosure`, `RA_D1_NativeLedgerOrientation`, `RA_D1_NativeDimensionality`). New downstream packets that consume the D1Native arithmetic should add `open D1Native` after their imports; uses qualified by `_root_.` (e.g. `_root_.bdgScore` in `RA_GraphOrientationClosure`) keep referring to `RA_D1_Core`'s root-namespace definition. If you see `chainScore.match_1` errors, check whether a downstream module is using both branches without an `open`.
7. **Field-name and parameter-passing fixes for v1.x orientation-link bridges.** Two pattern bugs recurred across v1.2 and v1.3 packet-original Lean files, both relating to the v1.0 `RA_MotifNativeCertificateComponents` module: (a) packet authors wrote `C.orientationEvidence` but the v1.0 field is named `orientationComponent`; (b) packet authors wrote `DAGNativeCertificateComponentContext G Γ M F Ξ Ω` (six explicit args) but v1.0's structure only takes `Ω` explicit (the rest are inferred from `Ω`'s type). Same fixes apply to the Graph variant. Apply both renames mechanically when a packet's Lean fails to compile against the v1.0 component context.

## RAKB-update rejection list (things that have wasted time)

- Don't run `apply_ra_method_guardrails_upsert.py` (or analogues) without redirecting claims output away from `claims.csv`. The repo has no `claims.csv`; running it creates an orphan.
- Don't promote a "modeling discipline" or "methodological guardrail" into `claims.yaml`. Always `framing.yaml` with the right `framing_kind`.
- Don't trust the SHA recorded in a packet's proposed `artifacts.csv` for the *installed* module — you almost always edit the module before build closes (Σ rename, `Nonempty` wrap, etc.), so the installed SHA differs from the packet original. Record both: `Packet original SHA <a>; installed SHA <b> after <change>` in the artifact `notes`.
- Don't `git add <packet-root>/` when the packet root has a `.DS_Store`. Add subdirectories explicitly.
- Don't try `git push origin main`. Hand it to the user.
