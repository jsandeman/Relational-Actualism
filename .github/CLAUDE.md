# .github/CLAUDE.md

Project-specific guidance for Claude when responding to GitHub events on this
repository (PRs, issues, review comments via the Claude GitHub app, or the
Claude Code Action). The root `CLAUDE.md` covers full repository conventions;
this file holds the rules that matter most for *asynchronous* responses where
no human is in the loop turn-by-turn.

## Identity of this repository

This is a research repository for **Relational Actualism (RA)** — a discrete-
causal-graph framework for fundamental physics. It is not a typical software
project. Most non-trivial PRs touch a knowledge-base layer (RAKB) that ties
Lean proofs, Python computations, Julia simulators, and LaTeX papers to
typed claim nodes. Read the root `CLAUDE.md` for the big picture before
responding to anything substantive.

## Hard rules for GitHub-side responses

- **Never push to `main` and never merge PRs autonomously.** Comment, request
  changes, suggest patches — but the human owner ships releases.
- **Never modify the `docs/RA_KB/registry/` files in a comment-only review.**
  Registry edits happen via explicit upsert scripts or hand edits in a PR;
  drive-by suggestions to "just bump this YAML field" are a known footgun
  because the registry has cross-file invariants checked by
  `validate_rakb_v0_5.py`. If a registry change is needed, ask the author to
  run the validator and post the diff in counts (`claims=N issues=M ...`).
- **Never propose promoting a result into `registry/claims.yaml`** unless the
  PR includes one of: a Lean build-confirmed file (`lean_build_confirmed_no_sorry`
  or stronger), a derivation in RA-native vocabulary (DR), or a reproducible
  computation (CV). Otherwise route to `issues.yaml`,
  `targets.yaml`, or `restoration_candidates.csv`.
- **Don't touch `% RAKB:` comments in TeX by hand.** They are regenerated from
  `docs/RA_KB/registry/source_text_references.csv` by
  `docs/RA_Canonical_Papers/Makefile.rakb`. If a PR hand-edits them, request
  that the author regenerate via `make -f Makefile.rakb ids` and commit the
  generator output.

## RA framing discipline (essential context)

The target is **Nature**, not one-to-one recovery of Standard-Model / QFT / GR
categories. Continuum or legacy vocabulary (quark, gluon, gauge group, metric,
Hilbert space, etc.) is allowed only as **translation/cartography**, not as
mechanism. Any PR or issue that introduces SM-flavored identifiers in the
Lean tree is suspect — the Apr 21 2026 rename pass deliberately moved away
from those (gluon→sym_branch, quark→asym_branch, confinement→filter_horizon,
etc.; see `src/RA_AQFT/lakefile.lean` docstring). Flag SM-flavored regressions
in review.

Mechanisms must trace to: DAG + BDG + LLC + actualization + Nature-measurements.
That's the chain. If a PR claims a mechanism that doesn't bottom out there,
ask for the trace.

## Reviewing common PR types

### Lean PRs (`src/RA_AQFT/*.lean`)
- Confirm the file is in the active roots in `lakefile.lean` if the author
  claims it's load-bearing. Retired roots are listed in the docstring at the
  top of `lakefile.lean` with rationale — don't reactivate without restating
  the reason for retirement.
- Check for `sorry`, `admit`, and unjustified `axiom` declarations. The active
  closure target is "no sorry / no admit / no axiom" except for documented
  interface axioms (e.g. amplitude locality in `RA_AmpLocality.lean`).
- For PRs that add a new root, expect a build log in
  `docs/RA_KB/reports/lake_build_*.log` and a corresponding artifact row in
  `registry/artifacts.csv` with status `lean_env_compile_confirmed_no_sorry_no_admit_no_axiom`
  or stronger.

### Python computational PRs (`src/RA_AQFT/*.py`, `src/RA_Complexity/`, `data/DFT_Survey/`)
- A computational PR earns a `CV` (computes-verified) status only if it has
  a smoke test or reproducible script alongside the computation. PRs that add
  a single number without reproduction route to `targets.yaml` or
  `issues.yaml`, not `claims.yaml`.
- The `bmv_comparator.py` artifact pattern is a good model: simulator + test
  file + sweep CSV + RAKB upsert (target + artifact rows + edges).

### Paper PRs (`docs/RA_Canonical_Papers/*.tex`)
- New TeX content needs RAKB IDs regenerated via
  `make -f Makefile.rakb ids` (or `check-ids` for verification only).
- New citations should be in `common/ra_references.bib` or extracted by
  `make -f Makefile.rakb bib-audit`.
- Don't approve a paper PR with stale `% RAKB:` comments — fail the review
  and ask for regeneration.

### RAKB PRs (`docs/RA_KB/registry/*`)
- Always require that the author has run `validate_rakb_v0_5.py` and pasted
  the new counts in the PR description.
- Don't accept registry edits that delete `*.bak_*` files — those are
  upsert-script backups.
- New `RA-*-NNN` IDs must be unique across the whole registry (claims, issues,
  targets, framing, archived). The validator catches this; cite it.

## Triaging issues

The repository uses `.github/ISSUE_TEMPLATE/` for structured submissions.
For new issues:

- **Mathematical proposal templates** (Lean / proof-related): map the proposal
  to one of the load-bearing open problems (amplitude locality, Bianchi
  compatibility on curved backgrounds, Type-III₁ continuum limit, Causal
  Firewall limit theorem) if it fits. If it doesn't fit any of those, ask
  whether it's a new RAKB issue (`RA-OPEN-*`) or a derivation that should
  route through `restoration_candidates.csv`.
- **Bug reports / build failures**: check the toolchain in `lean-toolchain`
  matches what the issue uses, and whether the build log in
  `docs/RA_KB/reports/lake_build*.log` covered the same root.
- **External-collaborator inquiries**: be welcoming; the `CONTRIBUTING.md`
  lists three "hard walls" where help is wanted (modular theory, Causal
  Firewall limit, Bianchi). Route inquiries there.

## What to never invent in async responses

- A registry node ID. If you cite `RA-FOO-NNN`, it must exist in
  `claims.yaml` / `issues.yaml` / `targets.yaml` / `framing.yaml`. The
  validator will catch fabricated IDs but the human reading the comment
  won't, and they'll waste time looking it up.
- A Lean lemma name. Check the file before referencing.
- A status like `LV` or `CV` for a PR that doesn't yet meet that bar — these
  are the epistemic discipline tags and inflating them is the worst class
  of async-Claude error.
