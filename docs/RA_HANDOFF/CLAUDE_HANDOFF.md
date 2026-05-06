# Claude Code Handoff — RA Track B Assistant

> Paste this at the top of a fresh Claude Code session if you're picking up
> the RA Track B workflow on a new machine, or if memory at the canonical
> path is unavailable. On the original machine, the assistant's persistent
> memory is auto-loaded and you can skip most of this.

---

You are continuing a long-running RA repo session. The previous session left
you in a fully populated state — DO NOT start from scratch.

## What's already in place (auto-loaded by Claude Code; you do not need to re-read these unless something specific seems wrong)

1. **`CLAUDE.md`** (project root) — operational rules. Recent additions
   (commit `39beb44`):
   - workflow step 12: pre-commit large-file scan (>100 MB)
   - "Recurring Lean-module fixes" extended to item 8 (Track B.1
     methodological Prop-field accessor circularity)
   - new section **"Recurring Python packet fixes"** (3 multi-source-CSV-
     merge bugs)
   - rejection-list entries on blind staging of packet `outputs/` and on
     trusting byte-identical graph-vs-control without column-priority check.

2. **Persistent memory** at
   `/Users/jsandeman/.claude/projects/-Users-jsandeman-projects-Relational-Actualism/memory/`.
   `MEMORY.md` indexes all entries. Notable:
   - `feedback_v1_8_1_controls_orientation_rescue.md`
   - `feedback_coverage_sufficiency_excludes_tainted_null.md`
   - `feedback_pandas_normalizer_packet_bug.md`
   - `feedback_packet_normalizer_keying_collision.md`
   - `feedback_packet_overlap_column_priority.md`
   - `project_track_b_work_order.md`  (B.1 → B.2 → B.3 → B.3b → B.4
     (negative, corrigendum) → next is **B.3c or B.4a**)

3. **RAKB** at `docs/RA_KB/registry/`. Active state (post-corrigendum):
   158 claims, 44 framing, 30 audit_events. The `audit_events.csv` is the
   per-event timeline; reading the last ~10 events reproduces current state.
   Validator:
   ```bash
   cd docs/RA_KB && python scripts/validate_rakb_v0_5.py
   ```

## Where Track B stands (one-line)

B.4 locked-envelope rescue analysis is non-estimable + the byte-identical
graph-vs-control finding was **RETRACTED** (column-priority bug).
Authorized next packet is **Track B.3c** (envelope-deepening sampler sweep
targeting `incidence_role_signed`'s 4-unique-overlap-value sparsity) or
**Track B.4a** (generator redesign). Track B.5 rescue analysis is **NOT**
authorized.

## The user's operational protocol

- **Auto mode is on by default** for this user.
- **Push to main is denied for the assistant**; the user runs
  `git push origin main` themselves between cycles.
- The user pastes a `<packet> has dropped` message followed by the canonical
  run command. Your job:
  1. Review the packet (Lean + Python + tests + registry proposals).
  2. Install Lean to `src/RA_AQFT/`, patch lakefile, build, lex check.
  3. Run unit tests, then the canonical command.
  4. Install in registry (translating proposals into v0.5 active schema).
  5. Validate, regen paper IDs, commit.
- For **destructive git ops** (force-push, `filter-repo`, branch deletion):
  wait for explicit user authorization. Auto mode does not override this.

## Quick start for the next cycle

1. `git log --oneline -10` (verify clean state).
2. `tail -20 docs/RA_KB/registry/audit_events.csv` (last events).
3. `ls src/RA_AQFT/ | grep -iE "trackB3c|TrackB3c|trackB4a|TrackB4a"`
   (find the next packet directory).
4. Review the packet README + canonical run command, then proceed per the
   `CLAUDE.md` packet-application workflow.

## Companion handoff

A separate handoff prompt for the ChatGPT packet-author session lives at
`docs/RA_HANDOFF/CHATGPT_HANDOFF.md`. Hand the user the same instruction
when they open a new ChatGPT chat for packet authoring — the two prompts
are designed to keep both sides aligned on the same Track B work order
and the same recurring packet-bug rules.
