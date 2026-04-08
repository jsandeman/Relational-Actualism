#!/usr/bin/env python3
"""
rakb_tools.py — session tools for rakb.db

Usage:
  python3 rakb_tools.py status            # current status distribution
  python3 rakb_tools.py open              # OP and AR claims
  python3 rakb_tools.py claim O03_REFRAMED  # full claim detail
  python3 rakb_tools.py unlocks O14       # what O14 enables downstream
  python3 rakb_tools.py validate          # run all integrity checks
  python3 rakb_tools.py snapshot          # generate rakb_snapshot.md
  python3 rakb_tools.py update O03_REFRAMED status DR  # update a field
  python3 rakb_tools.py log "Session note text"         # append to session log
"""

import sqlite3
import sys
import re
from pathlib import Path
from datetime import date

DB_PATH = '/home/claude/rakb.db'
SNAPSHOT_PATH = '/mnt/user-data/outputs/rakb_snapshot.md'

STATUS_RANK   = {'LV':5,'CV':4,'DR':3,'AR':2,'OP':1,'DEPRECATED':0}
STATUS_EMOJI  = {'LV':'🔵','CV':'🟢','DR':'✅','AR':'🟡','OP':'🔴','DEPRECATED':'⚫'}

def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def cmd_status(conn):
    print("\nRAKB STATUS DISTRIBUTION")
    print("─" * 40)
    for row in conn.execute(
        "SELECT status, COUNT(*) as n FROM claims GROUP BY status ORDER BY n DESC"
    ):
        bar = '█' * row['n']
        emoji = STATUS_EMOJI.get(row['status'], ' ')
        print(f"  {emoji} {row['status']:12} {row['n']:3}  {bar}")
    total = conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
    print(f"  {'TOTAL':14} {total}")

    lean = conn.execute(
        "SELECT claim FROM claims WHERE id='META_LEAN_COUNT'"
    ).fetchone()
    if lean:
        print(f"\nLean: {lean['claim'][:80]}")


def cmd_open(conn):
    print("\nOPEN PROBLEMS")
    print("─" * 60)
    rows = conn.execute(
        "SELECT id, claim FROM claims WHERE status='OP' ORDER BY id"
    ).fetchall()
    if rows:
        for r in rows:
            print(f"  🔴 [{r['id']}] {r['claim'][:70]}")
    else:
        print("  ✓ None — zero foundational open problems.")

    print("\nARGUED (may need attention)")
    print("─" * 60)
    for r in conn.execute(
        "SELECT id, claim FROM claims WHERE status='AR' ORDER BY id"
    ):
        print(f"  🟡 [{r['id']}] {r['claim'][:70]}")


def cmd_claim(conn, cid):
    r = conn.execute("SELECT * FROM claims WHERE id=?", (cid,)).fetchone()
    if not r:
        print(f"Claim '{cid}' not found.")
        return
    print(f"\n{'='*60}")
    print(f"  {cid}  [{r['status']}]  type:{r['type']}  updated:{r['updated']}")
    print(f"{'='*60}")
    print(f"CLAIM:  {r['claim']}")
    if r['evidence']:
        print(f"EVIDENCE: {r['evidence'][:120]}")
    if r['gap'] and r['gap'] not in ('—','-',''):
        print(f"GAP: {r['gap'][:120]}")
    if r['papers']:
        print(f"PAPERS: {r['papers']}")

    deps = conn.execute(
        "SELECT d.dep_id, c.status FROM deps d "
        "JOIN claims c ON d.dep_id=c.id WHERE d.claim_id=?", (cid,)
    ).fetchall()
    if deps:
        print(f"DEPS: {', '.join(f'{d[0]}({d[1]})' for d in deps)}")

    downstream = conn.execute(
        "SELECT d.claim_id, c.status FROM deps d "
        "JOIN claims c ON d.claim_id=c.id WHERE d.dep_id=?", (cid,)
    ).fetchall()
    if downstream:
        print(f"ENABLES: {', '.join(f'{d[0]}({d[1]})' for d in downstream)}")

    if r['derivation']:
        print(f"\nDERIVATION:\n{r['derivation'][:500]}{'...' if len(r['derivation'] or '')>500 else ''}")


def cmd_unlocks(conn, cid):
    """Transitive closure: what does cid enable downstream?"""
    print(f"\nTransitive downstream of [{cid}]:")
    visited = set()
    queue = [cid]
    while queue:
        current = queue.pop(0)
        for row in conn.execute(
            "SELECT d.claim_id, c.status, c.claim FROM deps d "
            "JOIN claims c ON d.claim_id=c.id WHERE d.dep_id=?", (current,)
        ):
            if row['claim_id'] not in visited:
                visited.add(row['claim_id'])
                e = STATUS_EMOJI.get(row['status'],' ')
                print(f"  {e} [{row['claim_id']}|{row['status']}] {row['claim'][:60]}")
                queue.append(row['claim_id'])
    if not visited:
        print("  (nothing downstream)")


def cmd_validate(conn):
    errors = []
    warnings = []

    # 1. Deps pointing to non-existent claims
    for row in conn.execute(
        "SELECT d.claim_id, d.dep_id FROM deps d "
        "LEFT JOIN claims c ON d.dep_id=c.id WHERE c.id IS NULL"
    ):
        errors.append(f"[{row['claim_id']}] dep '{row['dep_id']}' not found")

    # 2. Live claims depending on DEPRECATED
    for row in conn.execute(
        "SELECT c.id, d.dep_id FROM claims c "
        "JOIN deps d ON c.id=d.claim_id "
        "JOIN claims dep ON d.dep_id=dep.id "
        "WHERE dep.status='DEPRECATED' AND c.status!='DEPRECATED'"
    ):
        errors.append(f"[{row['id']}] depends on DEPRECATED '{row['dep_id']}'")

    # 3. L07 gap inconsistent with O01 status
    l07 = conn.execute("SELECT gap FROM claims WHERE id='L07'").fetchone()
    o01 = conn.execute("SELECT status FROM claims WHERE id='O01'").fetchone()
    if l07 and o01 and 'conditional on O01' in (l07['gap'] or '') and o01['status'] == 'LV':
        warnings.append("L07 gap says 'conditional on O01' but O01 is LV — clear the gap")

    # 4. LV/CV claims with non-trivial gap (excluding known legitimate ones)
    LEGIT_GAPS = {'L04','D4U02','O01','GS02','P02','P04','SM10','CS09'}
    for row in conn.execute(
        "SELECT id, gap FROM claims WHERE status IN ('LV','CV') "
        "AND gap IS NOT NULL AND gap NOT IN ('','—','-')"
    ):
        if row['id'] not in LEGIT_GAPS:
            warnings.append(f"[{row['id']}] non-trivial gap in LV/CV claim: {row['gap'][:60]}")

    # 5. OP claims depending on something with higher status (epistemic consistency)
    # (no check needed — OP depending on LV is fine)

    print("\nVALIDATION REPORT")
    print("─" * 50)
    if errors:
        print(f"ERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print("  ✓ No errors")
    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print("  ✓ No warnings")
    return len(errors)


def cmd_update(conn, cid, field, value):
    allowed = {'status','gap','updated','evidence','notes','claim','derivation','papers'}
    if field not in allowed:
        print(f"Field '{field}' not updatable via this command. Use SQL directly.")
        return
    old = conn.execute(f"SELECT {field} FROM claims WHERE id=?", (cid,)).fetchone()
    if not old:
        print(f"Claim '{cid}' not found.")
        return
    conn.execute(f"UPDATE claims SET {field}=?, updated=? WHERE id=?",
                 (value, date.today().isoformat(), cid))
    conn.commit()
    print(f"Updated [{cid}].{field}: '{(old[0] or '')[:50]}' → '{value[:50]}'")


def cmd_log(conn, entry, source_id=None):
    conn.execute(
        "INSERT INTO session_log (session_date, source_id, entry) VALUES (?,?,?)",
        (date.today().isoformat(), source_id, entry)
    )
    conn.commit()
    print(f"Session log entry added ({len(entry)} chars)")


def cmd_snapshot(conn):
    today = date.today().isoformat()
    lines = [
        f"# RAKB Snapshot — {today}",
        f"Generated from rakb.db\n",
    ]

    # Status summary
    lines.append("## Status Distribution\n")
    lines.append("| Status | Count |")
    lines.append("|--------|-------|")
    for row in conn.execute(
        "SELECT status, COUNT(*) as n FROM claims GROUP BY status ORDER BY "
        "CASE status WHEN 'LV' THEN 1 WHEN 'CV' THEN 2 WHEN 'DR' THEN 3 "
        "WHEN 'AR' THEN 4 WHEN 'OP' THEN 5 ELSE 6 END"
    ):
        lines.append(f"| {STATUS_EMOJI.get(row['status'],'')} {row['status']} | {row['n']} |")
    total = conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
    lines.append(f"| **TOTAL** | **{total}** |")

    # Lean count
    lean = conn.execute("SELECT claim FROM claims WHERE id='META_LEAN_COUNT'").fetchone()
    if lean:
        lines.append(f"\n**Lean:** {lean['claim']}\n")

    # Open problems
    lines.append("\n## Open Problems\n")
    op = conn.execute(
        "SELECT id, claim FROM claims WHERE status='OP' ORDER BY id"
    ).fetchall()
    if op:
        for r in op:
            lines.append(f"- **[{r['id']}]** {r['claim']}")
    else:
        lines.append("*None — zero foundational open problems.*")

    # Claims by section
    sections = [
        ('LV', '🔵 Lean-Verified'),
        ('CV', '🟢 Computation-Verified'),
        ('DR', '✅ Derived'),
        ('AR', '🟡 Argued'),
        ('OP', '🔴 Open'),
        ('DEPRECATED', '⚫ Deprecated'),
    ]
    for status, heading in sections:
        rows = conn.execute(
            "SELECT id, type, claim, evidence, gap, updated FROM claims "
            "WHERE status=? ORDER BY id", (status,)
        ).fetchall()
        if not rows:
            continue
        lines.append(f"\n## {heading} ({len(rows)})\n")
        lines.append("| ID | Type | Claim | Gap | Updated |")
        lines.append("|----|------|-------|-----|---------|")
        for r in rows:
            claim_short = (r['claim'] or '')[:60].replace('|','\\|')
            gap_short   = (r['gap']   or '—')[:40].replace('|','\\|')
            lines.append(
                f"| {r['id']} | {r['type']} | {claim_short} | {gap_short} | {r['updated']} |"
            )

    # Recent session log
    lines.append("\n## Recent Session Log (last 10 entries)\n")
    for row in conn.execute(
        "SELECT session_date, source_id, entry FROM session_log "
        "ORDER BY id DESC LIMIT 10"
    ):
        src = f"[{row['source_id']}] " if row['source_id'] else ""
        lines.append(f"**{row['session_date']}** {src}{(row['entry'] or '')[:200]}\n")

    snapshot = '\n'.join(lines)
    with open(SNAPSHOT_PATH, 'w') as f:
        f.write(snapshot)
    print(f"Snapshot written: {SNAPSHOT_PATH} ({len(snapshot)//1024} KB)")


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    if not Path(DB_PATH).exists():
        print(f"Database not found: {DB_PATH}")
        sys.exit(1)

    conn = connect()
    args = sys.argv[1:]

    if not args or args[0] == 'status':
        cmd_status(conn)
    elif args[0] == 'open':
        cmd_open(conn)
    elif args[0] == 'claim' and len(args) >= 2:
        cmd_claim(conn, args[1])
    elif args[0] == 'unlocks' and len(args) >= 2:
        cmd_unlocks(conn, args[1])
    elif args[0] == 'validate':
        sys.exit(cmd_validate(conn))
    elif args[0] == 'update' and len(args) >= 4:
        cmd_update(conn, args[1], args[2], ' '.join(args[3:]))
    elif args[0] == 'log' and len(args) >= 2:
        cmd_log(conn, ' '.join(args[1:]))
    elif args[0] == 'snapshot':
        cmd_snapshot(conn)
    elif args[0] == 'papers':
        cmd_papers(conn, args[1] if len(args) > 1 else None)
    elif args[0] == 'paper' and len(args) >= 2:
        cmd_paper_claims(conn, args[1])
    elif args[0] == 'claim-papers' and len(args) >= 2:
        cmd_claim_papers(conn, args[1])
    else:
        print(__doc__)

    conn.close()


def cmd_papers(conn, suite=None):
    """Show all papers, optionally filtered by suite."""
    STATUS_ICON = {
        'drafting': '✏️ ',
        'submitted': '📤',
        'awaiting-editor-assignment': '⏳',
        'with-editors': '👁️ ',
        'under-review': '🔍',
        'accept-minor': '✅',
        'reject-resubmit': '🔄',
        'published': '📗',
    }
    where = "WHERE suite=?" if suite else ""
    args  = (suite,) if suite else ()
    print(f"\n{'PAPERS':60}")
    print("─" * 70)
    for r in conn.execute(
        f"SELECT id, suite, status, title, target_journal, deadline FROM papers {where} ORDER BY suite, id",
        args
    ):
        icon = STATUS_ICON.get(r['status'], '  ')
        jrnl = f" → {r['target_journal']}" if r['target_journal'] else ""
        dl   = f" [deadline: {r['deadline']}]" if r['deadline'] else ""
        print(f"  {icon} [{r['id']}|{r['suite']}] {r['title'][:50]}{jrnl}{dl}")
        if r['status'] not in ('drafting',):
            print(f"       status: {r['status']}")


def cmd_paper_claims(conn, paper_id):
    """Show all claims mapped to a paper."""
    rows = conn.execute("""
        SELECT c.id, c.status, c.claim FROM claims c
        JOIN paper_claims pc ON c.id=pc.claim_id
        WHERE pc.paper_id=? ORDER BY c.id
    """, (paper_id,)).fetchall()
    if not rows:
        print(f"No claims mapped to '{paper_id}' (or paper not found).")
        return
    print(f"\nClaims for [{paper_id}] ({len(rows)} total):")
    for r in rows:
        print(f"  {STATUS_EMOJI.get(r['status'],' ')} [{r['id']}|{r['status']}] {r['claim'][:65]}")


def cmd_claim_papers(conn, claim_id):
    """Which papers reference a given claim?"""
    rows = conn.execute("""
        SELECT p.id, p.suite, p.status, p.title FROM papers p
        JOIN paper_claims pc ON p.id=pc.paper_id
        WHERE pc.claim_id=? ORDER BY p.suite, p.id
    """, (claim_id,)).fetchall()
    if not rows:
        print(f"Claim '{claim_id}' not mapped to any papers.")
        return
    print(f"\nPapers referencing [{claim_id}]:")
    for r in rows:
        print(f"  [{r['id']}|{r['suite']}|{r['status']}] {r['title'][:60]}")

def _extend_main():
    pass  # marker — main already extended above via APPEND block

if __name__ == '__main__':
    main()


# ── Paper commands ─────────────────────────────────────────────────────────
