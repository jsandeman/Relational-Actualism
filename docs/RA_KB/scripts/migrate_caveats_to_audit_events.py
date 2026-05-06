#!/usr/bin/env python3
"""Comprehensive caveat migration helper.

Reads a JSON mapping {entity_id: new_caveat} and rewrites the corresponding
`caveats: ...` block inside claims.yaml, framing.yaml, or issues.yaml.

The substitution is line-anchored on the YAML entry: it locates `- id: <ID>`
and the next sibling-level `- id:` (or end-of-file), then within that range
finds the `caveats:` line and rewrites the block until the next sibling
field at the same indentation. Output uses the `>` block-scalar form so
multi-line trimmed caveats stay readable.

Run example:
    python scripts/migrate_caveats_to_audit_events.py \
        --target registry/claims.yaml \
        --map /path/to/migration_payload.json \
        --report /path/to/report.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def find_entry_range(lines: List[str], entry_id: str) -> Tuple[int, int]:
    """Return [start, end) line indices for the YAML entry whose `- id: <entry_id>` matches."""
    pattern = re.compile(rf"^- id:\s*{re.escape(entry_id)}\s*$")
    start = None
    for i, line in enumerate(lines):
        if pattern.match(line):
            start = i
            break
    if start is None:
        return -1, -1
    # Find next top-level `- id:` line
    for j in range(start + 1, len(lines)):
        if re.match(r"^- id:\s*\S", lines[j]):
            return start, j
    return start, len(lines)


def find_caveats_block(lines: List[str], start: int, end: int) -> Tuple[int, int, int]:
    """Return (caveat_line, body_end, indent_count) for the caveats block within [start, end)."""
    # caveats appears at 2-space indent within the entry
    pattern = re.compile(r"^(\s+)caveats:")
    cav_line = None
    indent_count = None
    for i in range(start, end):
        m = pattern.match(lines[i])
        if m:
            cav_line = i
            indent_count = len(m.group(1))
            break
    if cav_line is None:
        return -1, -1, 0
    # Find next sibling field at same indent
    sibling_pat = re.compile(rf"^\s{{{indent_count}}}\S")
    body_end = end
    for j in range(cav_line + 1, end):
        if sibling_pat.match(lines[j]):
            body_end = j
            break
    return cav_line, body_end, indent_count


def render_caveat_block(text: str, indent: int) -> List[str]:
    """Format a multi-line caveat string as YAML `>` block scalar."""
    pad = " " * indent
    body_pad = " " * (indent + 2)
    out = [f"{pad}caveats: >\n"]
    # Wrap on whitespace at ~74 chars + body padding
    max_width = 74 - (indent + 2)
    paragraphs = text.split("\n\n")
    for pi, para in enumerate(paragraphs):
        words = re.split(r"\s+", para.strip())
        line = ""
        for w in words:
            if not w:
                continue
            if not line:
                line = w
            elif len(line) + 1 + len(w) > max_width:
                out.append(f"{body_pad}{line}\n")
                line = w
            else:
                line += " " + w
        if line:
            out.append(f"{body_pad}{line}\n")
        if pi != len(paragraphs) - 1:
            out.append("\n")
    return out


def apply_migration(target: Path, mapping: Dict[str, str]) -> Dict[str, object]:
    text = target.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    report = {"target": str(target), "migrated": [], "missing": [], "before_chars": {}, "after_chars": {}}

    # Process longest-first so substitutions don't shift earlier ranges.
    # Actually we insert/delete lines, so process in reverse order of entry start lines.
    starts: List[Tuple[int, str, str]] = []
    for entry_id in mapping.keys():
        s, e = find_entry_range(lines, entry_id)
        if s == -1:
            report["missing"].append(entry_id)
            continue
        cav_line, body_end, indent = find_caveats_block(lines, s, e)
        if cav_line == -1:
            report["missing"].append(f"{entry_id} (no caveats)")
            continue
        before = "".join(lines[cav_line:body_end])
        report["before_chars"][entry_id] = len(before)
        starts.append((cav_line, body_end, entry_id))

    starts.sort(key=lambda x: x[0], reverse=True)

    for cav_line, body_end, entry_id in starts:
        # We re-find indent from current lines (defensive)
        m = re.match(r"^(\s+)caveats:", lines[cav_line])
        indent = len(m.group(1)) if m else 2
        new_block = render_caveat_block(mapping[entry_id], indent)
        report["after_chars"][entry_id] = sum(len(s) for s in new_block) - len(new_block[0]) + len(f"{' '*indent}caveats: ")
        lines[cav_line:body_end] = new_block
        report["migrated"].append(entry_id)

    target.write_text("".join(lines), encoding="utf-8")
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, type=Path)
    ap.add_argument("--map", required=True, type=Path, help="JSON file with {entry_id: new_caveat}")
    ap.add_argument("--report", type=Path, default=None)
    args = ap.parse_args()

    mapping = json.loads(args.map.read_text(encoding="utf-8"))
    report = apply_migration(args.target, mapping)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("target", "migrated", "missing")}, indent=2))
    print(f"Migrated {len(report['migrated'])} entries; {len(report['missing'])} missing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
