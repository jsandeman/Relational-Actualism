# RA Handoff Prompts

Two self-contained prompts for transitioning the RA Track B workflow into
new chat / session contexts.

## Files

- **`CHATGPT_HANDOFF.md`** — paste at the top of a fresh ChatGPT chat. ChatGPT
  authors installable packets in this workflow.
- **`CLAUDE_HANDOFF.md`** — paste at the top of a fresh Claude Code session
  if you're working on a different machine, or if persistent memory at the
  canonical path is unavailable. On the original machine, Claude's memory
  is auto-loaded and you only need this if state seems missing.

## When to use

- Starting a new ChatGPT chat for the next Track B packet → use
  `CHATGPT_HANDOFF.md`.
- Starting a new Claude Code session on a different machine, or after
  manual memory reset → use `CLAUDE_HANDOFF.md`.
- Same machine, same memory directory: Claude auto-loads `MEMORY.md` and
  `CLAUDE.md`. The handoff file is documentation more than load-required.

## Maintenance

Update both files when:

- A new track / phase lands (B.3c, B.4a, B.5, …) — bump the "Current Track
  B status" / "Where Track B stands" sections.
- A new recurring packet bug pattern is added to `CLAUDE.md` → mirror the
  one-line summary in `CHATGPT_HANDOFF.md`.
- The keying ontology, controlling standard, or sufficiency rule changes
  (these have audit-event IDs locked) — update the corresponding section
  in both files and add the new audit-event citation.

The two files are intentionally redundant on key facts so each can be
pasted independently and remain self-sufficient.
