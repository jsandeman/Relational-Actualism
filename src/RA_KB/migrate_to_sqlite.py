#!/usr/bin/env python3
"""
migrate_to_sqlite.py
Convert rakb.yaml → rakb.db (SQLite)

Tables:
  claims      — one row per claim block
  deps        — claim_id → dep_id edges
  session_log — freeform narrative/IC notes (append-only)
"""

import re
import sqlite3
import sys
from pathlib import Path

YAML_PATH = '/home/claude/rakb.yaml'
DB_PATH   = '/home/claude/rakb.db'

# ── Schema ────────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS claims (
    id          TEXT PRIMARY KEY,
    type        TEXT,
    status      TEXT,
    updated     TEXT,
    claim       TEXT,
    derivation  TEXT,
    evidence    TEXT,
    gap         TEXT,
    papers      TEXT,
    notes       TEXT,
    supersedes  TEXT
);

CREATE TABLE IF NOT EXISTS deps (
    claim_id    TEXT NOT NULL REFERENCES claims(id),
    dep_id      TEXT NOT NULL,
    PRIMARY KEY (claim_id, dep_id)
);

CREATE TABLE IF NOT EXISTS session_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_date TEXT,
    source_id   TEXT,   -- which claim this note came from (NULL if global)
    entry       TEXT
);

CREATE INDEX IF NOT EXISTS idx_deps_claim  ON deps(claim_id);
CREATE INDEX IF NOT EXISTS idx_deps_dep    ON deps(dep_id);
CREATE INDEX IF NOT EXISTS idx_claims_status ON claims(status);
"""

# ── Parser ─────────────────────────────────────────────────────────────────
def parse_yaml(path):
    with open(path) as f:
        text = f.read()

    # Split on block boundaries
    block_pat = re.compile(r'^=== CLAIM: (\S+) ===\s*\n', re.MULTILINE)
    starts = [(m.group(1), m.end()) for m in block_pat.finditer(text)]

    claims = []
    global_session_notes = []

    # Collect text before first block as global session notes
    if starts:
        preamble = text[:starts[0][1] - len(starts[0][0]) - len('=== CLAIM:  ===\n')]
        global_session_notes.append(('GLOBAL_PREAMBLE', preamble))

    for i, (cid, body_start) in enumerate(starts):
        body_end = starts[i+1][1] - len(starts[i+1][0]) - len('=== CLAIM:  ===\n') \
                   if i+1 < len(starts) else len(text)
        # Find actual end (next block header)
        next_match = block_pat.search(text, body_start)
        body = text[body_start: next_match.start() if next_match else len(text)]

        claim = extract_block(cid, body)
        claims.append(claim)

        # Extract session notes (// lines and IC## entries) from body
        notes_lines = []
        for line in body.split('\n'):
            s = line.strip()
            if s.startswith('//') or re.match(r'IC\d+\s*\|', s) or s.startswith('# '):
                notes_lines.append(line)
        if notes_lines:
            global_session_notes.append((cid, '\n'.join(notes_lines)))

    return claims, global_session_notes


def extract_field(body, field):
    """Extract scalar field value."""
    m = re.search(rf'^{field}:\s*(.*)', body, re.MULTILINE)
    return m.group(1).strip() if m else ''


def extract_multiline_field(body, field):
    """Extract multi-line YAML block (pipe-style)."""
    # Match field: |\n  ...
    m = re.search(rf'^{field}:\s*\|\s*\n((?:[ \t]+.*\n?)*)', body, re.MULTILINE)
    if m:
        raw = m.group(1)
        # Dedent: remove common leading whitespace
        lines = raw.split('\n')
        dedented = [re.sub(r'^  ', '', l) for l in lines]
        return '\n'.join(dedented).strip()
    # Fallback: single-line value
    return extract_field(body, field)


def extract_deps(body):
    m = re.search(r'^deps:\s*\[([^\]]*)\]', body, re.MULTILINE)
    if not m:
        return []
    raw = m.group(1)
    return [x.strip() for x in re.split(r'[\s,]+', raw) if x.strip()]


def extract_block(cid, body):
    # Strip // comment lines and IC## lines from the body before field extraction
    clean_lines = []
    for line in body.split('\n'):
        s = line.strip()
        if s.startswith('//') or re.match(r'IC\d+\s*\|', s):
            continue
        clean_lines.append(line)
    clean_body = '\n'.join(clean_lines)

    return {
        'id':         cid,
        'type':       extract_field(clean_body, 'type'),
        'status':     extract_field(clean_body, 'status'),
        'updated':    extract_field(clean_body, 'updated'),
        'claim':      extract_field(clean_body, 'claim'),
        'derivation': extract_multiline_field(clean_body, 'derivation'),
        'evidence':   extract_field(clean_body, 'evidence'),
        'gap':        extract_field(clean_body, 'gap'),
        'papers':     extract_field(clean_body, 'papers'),
        'notes':      extract_multiline_field(clean_body, 'notes'),
        'supersedes': extract_field(clean_body, 'supersedes'),
        'deps':       extract_deps(clean_body),
    }


# ── Migration ──────────────────────────────────────────────────────────────
def migrate(yaml_path, db_path):
    print(f"Parsing {yaml_path}...")
    claims, session_notes = parse_yaml(yaml_path)
    print(f"  Found {len(claims)} claims")

    print(f"Creating {db_path}...")
    Path(db_path).unlink(missing_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)

    # Insert claims
    ok = 0
    for c in claims:
        try:
            conn.execute("""
                INSERT INTO claims
                  (id, type, status, updated, claim, derivation, evidence, gap, papers, notes, supersedes)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, (c['id'], c['type'], c['status'], c['updated'],
                  c['claim'], c['derivation'], c['evidence'], c['gap'],
                  c['papers'], c['notes'], c['supersedes']))
            ok += 1
        except sqlite3.Error as e:
            print(f"  ERROR inserting {c['id']}: {e}")
    print(f"  Inserted {ok}/{len(claims)} claims")

    # Insert deps (skip dangling refs gracefully)
    dep_ok = dep_skip = 0
    all_ids = {c['id'] for c in claims}
    for c in claims:
        for dep in c['deps']:
            if dep not in all_ids:
                dep_skip += 1
                continue
            try:
                conn.execute("INSERT OR IGNORE INTO deps VALUES (?,?)", (c['id'], dep))
                dep_ok += 1
            except sqlite3.Error as e:
                print(f"  ERROR inserting dep {c['id']}→{dep}: {e}")
    print(f"  Inserted {dep_ok} deps ({dep_skip} dangling refs skipped)")

    # Insert session notes
    note_ok = 0
    for source_id, entry in session_notes:
        if entry.strip():
            conn.execute(
                "INSERT INTO session_log (session_date, source_id, entry) VALUES (?,?,?)",
                ('2026-04-07', source_id if source_id != 'GLOBAL_PREAMBLE' else None, entry)
            )
            note_ok += 1
    print(f"  Inserted {note_ok} session log entries")

    conn.commit()

    # Verification
    print("\nVerification:")
    for row in conn.execute("SELECT status, COUNT(*) FROM claims GROUP BY status ORDER BY COUNT(*) DESC"):
        print(f"  {row[0]:12} {row[1]}")
    n_deps = conn.execute("SELECT COUNT(*) FROM session_log").fetchone()[0]
    print(f"  session_log entries: {n_deps}")

    conn.close()
    size_kb = Path(db_path).stat().st_size // 1024
    print(f"\nDone. {db_path} ({size_kb} KB)")
    return ok


if __name__ == '__main__':
    yaml_path = sys.argv[1] if len(sys.argv) > 1 else YAML_PATH
    db_path   = sys.argv[2] if len(sys.argv) > 2 else DB_PATH
    migrate(yaml_path, db_path)
