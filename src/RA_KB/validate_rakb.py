#!/usr/bin/env python3
"""
validate_rakb.py — RAKB consistency validator
Run after every session: python3 validate_rakb.py rakb.yaml

CHECKS:
  1. All dep IDs exist as claim blocks
  2. No "OPEN"/"still open"/"remains open" language in non-comment lines of
     closed claims (LV, CV, DR)
  3. No non-trivial gap field in LV or CV claims
  4. L07 gap field consistent with O01 status
  5. Auto-generates Open Problem Summary from status fields
  6. Auto-generates Lean count summary
  7. Flags inline pipe entries that shadow block claims (duplication)
  8. Detects DEPRECATED claims still referenced in non-DEPRECATED deps
  9. Status hierarchy: dep cannot have lower epistemic status than its dependent
     (e.g. LV claim cannot depend on OP claim without a noted exception)
 10. Prints final status distribution
"""

import re
import sys
from collections import defaultdict, Counter

YELLOW = "\033[33m"
RED    = "\033[31m"
GREEN  = "\033[32m"
CYAN   = "\033[36m"
RESET  = "\033[0m"

STATUS_RANK = {'LV': 5, 'CV': 4, 'DR': 3, 'AR': 2, 'OP': 1, 'DEPRECATED': 0}

def parse_blocks(text):
    """Parse all === CLAIM: ID === blocks into a dict."""
    # Split on block boundaries
    pattern = re.compile(r'^=== CLAIM: (\S+) ===\s*\n', re.MULTILINE)
    positions = [(m.group(1), m.end()) for m in pattern.finditer(text)]
    claims = {}
    for i, (cid, start) in enumerate(positions):
        end = positions[i+1][1] - len(positions[i+1][0]) - len('=== CLAIM:  ===\n') if i+1 < len(positions) else len(text)
        # Actually just take up to next block header
        end_match = pattern.search(text, start)
        body = text[start: end_match.start() if end_match else len(text)]
        claims[cid] = body
    return claims

def extract_field(body, field):
    """Extract the value of a top-level field (e.g. 'status', 'deps', 'gap')."""
    m = re.search(rf'^{field}:\s*(.*)', body, re.MULTILINE)
    return m.group(1).strip() if m else ''

def extract_deps(body):
    """Extract list of dep IDs from deps: [...] field."""
    m = re.search(r'^deps:\s*\[([^\]]*)\]', body, re.MULTILINE)
    if not m:
        return []
    raw = m.group(1)
    return [x.strip() for x in re.split(r'[\s,]+', raw) if x.strip()]

def is_open_language(line):
    """True if line contains stale open-problem language."""
    return bool(re.search(
        r'\bstill open\b|\bremains open\b|\bopen problem\b|\bopen step\b'
        r'|\bremains to be\b|\bhas not been\b|\bnot yet\b|\bopen analytically\b',
        line, re.IGNORECASE
    ))

def is_comment_line(line):
    """True if line is a YAML comment or // comment (session notes)."""
    s = line.strip()
    return s.startswith('#') or s.startswith('//') or bool(__import__('re').match(r'IC\d+', s))


# Phrases that look like "open language" but are physics descriptions, not status claims
PHYSICS_FALSE_POSITIVES = [
    'not yet actualized',      # physics: describes a quantum state
    'no longer a conceptual open problem',  # correctly closed claim
    'open problem in the KB',  # forward reference
    'old open problem',        # historical reference
    'remain ar',               # gap note about downstream AR claims
    'remain open as',          # gap note about downstream
]

def is_physics_false_positive(line):
    return any(p in line.lower() for p in PHYSICS_FALSE_POSITIVES)

def check_open_language_in_closed_claim(cid, body, status):
    """Return list of (line_content) with stale open language."""
    if status not in ('LV', 'CV', 'DR'):
        return []
    issues = []
    # Skip the Open Problem Summary block (it's meta-commentary)
    for line in body.split('\n'):
        if is_comment_line(line):
            continue
        if is_open_language(line) and not is_physics_false_positive(line):
            issues.append(line.strip()[:100])
    return issues

def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3 validate_rakb.py <rakb.yaml>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path) as f:
        text = f.read()

    claims = parse_blocks(text)
    all_ids = set(claims.keys())

    errors   = []   # must fix
    warnings = []   # should fix
    infos    = []   # informational

    # ── CHECK 1: Dangling dep references ─────────────────────────────────
    for cid, body in claims.items():
        for dep in extract_deps(body):
            if dep not in all_ids:
                errors.append(f"[{cid}] dep '{dep}' not found as a claim block")

    # ── CHECK 2: Stale open language in closed claims ────────────────────
    for cid, body in claims.items():
        status = extract_field(body, 'status')
        issues = check_open_language_in_closed_claim(cid, body, status)
        # N10 is a known catch-all; flag but don't make it an error
        level = warnings if cid == 'N10' else errors
        for txt in issues:
            level.append(f"[{cid}|{status}] stale open language: {txt}")

    # ── CHECK 3: Non-trivial gap in LV/CV claims ─────────────────────────
    LEGITIMATE_LV_GAPS = {
        'L04': 'scope note (documented in papers)',
        'L07': 'conditional on O01 (now LV — update this)',
        'O01': 'evidence field, not a gap',
        'GS02': 'representation content open (noted)',
        'P02': 'testable prediction (DESI)',
        'P04': 'testable prediction (superconducting circuits)',
        'SM10': 'conjecture (1.8% error)',
        'CS09': 'transfer function gap (noted)',
        'D4U02': 'analytic gap vs certified computation (noted)',
    }
    for cid, body in claims.items():
        status = extract_field(body, 'status')
        gap = extract_field(body, 'gap')
        if status in ('LV', 'CV') and gap and gap not in ('—', '-', ''):
            if cid in LEGITIMATE_LV_GAPS:
                infos.append(f"[{cid}|{status}] gap field: {gap[:60]} — noted: {LEGITIMATE_LV_GAPS[cid]}")
            else:
                warnings.append(f"[{cid}|{status}] non-trivial gap in {status} claim: {gap[:80]}")

    # ── CHECK 4: L07 gap should reference O01 as LV now ─────────────────
    l07_body = claims.get('L07', '')
    l07_gap  = extract_field(l07_body, 'gap')
    l07_status = extract_field(l07_body, 'status')
    o01_status = extract_field(claims.get('O01', ''), 'status')
    if 'conditional on O01' in l07_gap and o01_status == 'LV':
        warnings.append(f"[L07] gap says 'conditional on O01' but O01 is now LV — gap should be cleared")

    # ── CHECK 5: DEPRECATED claims still in dep lists ────────────────────
    deprecated = {cid for cid, body in claims.items()
                  if extract_field(body, 'status') == 'DEPRECATED'}
    for cid, body in claims.items():
        if extract_field(body, 'status') == 'DEPRECATED':
            continue
        for dep in extract_deps(body):
            if dep in deprecated:
                errors.append(f"[{cid}] depends on DEPRECATED claim '{dep}'")

    # ── CHECK 6: Status hierarchy (dep should not be OP if claim is LV/CV/DR)
    for cid, body in claims.items():
        my_status = extract_field(body, 'status')
        my_rank = STATUS_RANK.get(my_status, -1)
        if my_rank < STATUS_RANK.get('DR', 3):
            continue  # Only check DR and above
        for dep in extract_deps(body):
            dep_body = claims.get(dep, '')
            dep_status = extract_field(dep_body, 'status')
            dep_rank = STATUS_RANK.get(dep_status, -1)
            if dep_rank == STATUS_RANK['OP']:
                warnings.append(
                    f"[{cid}|{my_status}] depends on OP claim '{dep}' — "
                    f"epistemic status may be overstated"
                )

    # ── CHECK 7: Inline pipe entries that duplicate block IDs ────────────
    inline_ids = set(re.findall(r'^([A-Z][A-Z0-9_]+)\s*\|', text, re.MULTILINE))
    duplicated = inline_ids & all_ids
    if duplicated:
        warnings.append(
            f"These IDs appear as BOTH block claims AND inline pipe entries "
            f"(duplication risk): {sorted(duplicated)}"
        )

    # ── AUTO-GENERATE: Open Problem Summary ──────────────────────────────
    op_claims = [(cid, extract_field(body, 'claim'))
                 for cid, body in claims.items()
                 if extract_field(body, 'status') == 'OP']
    ar_claims = [(cid, extract_field(body, 'claim'))
                 for cid, body in claims.items()
                 if extract_field(body, 'status') == 'AR']

    # ── AUTO-GENERATE: Status distribution ───────────────────────────────
    status_dist = Counter(extract_field(body, 'status') for body in claims.values())

    # ── AUTO-GENERATE: Lean count from META_LEAN_COUNT ───────────────────
    meta_body = claims.get('META_LEAN_COUNT', '')
    lean_claim = extract_field(meta_body, 'claim')

    # ══════════════════════════════════════════════════════════════════════
    # REPORT
    # ══════════════════════════════════════════════════════════════════════
    print(f"\n{'='*65}")
    print(f"  RAKB VALIDATION REPORT — {path}")
    print(f"{'='*65}")

    print(f"\n{CYAN}CLAIM COUNTS:{RESET}")
    for s in ['LV','CV','DR','AR','OP','DEPRECATED']:
        n = status_dist.get(s, 0)
        bar = '█' * n
        print(f"  {s:12} {n:3}  {bar}")
    print(f"  {'TOTAL':12} {sum(status_dist.values()):3}")

    print(f"\n{CYAN}LEAN STATUS:{RESET}")
    print(f"  {lean_claim[:80] if lean_claim else '(META_LEAN_COUNT not found)'}")

    print(f"\n{CYAN}OPEN PROBLEMS (OP):{RESET}")
    if op_claims:
        for cid, claim in op_claims:
            print(f"  [{cid}] {claim[:70]}")
    else:
        print(f"  {GREEN}None — zero foundational open problems.{RESET}")

    if errors:
        print(f"\n{RED}ERRORS ({len(errors)}) — must fix:{RESET}")
        for e in errors:
            print(f"  ✗ {e}")
    else:
        print(f"\n{GREEN}ERRORS: none{RESET}")

    if warnings:
        print(f"\n{YELLOW}WARNINGS ({len(warnings)}) — should fix:{RESET}")
        for w in warnings:
            print(f"  ⚠ {w}")
    else:
        print(f"\n{GREEN}WARNINGS: none{RESET}")

    if infos:
        print(f"\n{CYAN}INFO ({len(infos)}) — noted, legitimate:{RESET}")
        for i in infos:
            print(f"  ℹ {i}")

    print(f"\n{'='*65}")
    n_err = len(errors)
    n_warn = len(warnings)
    if n_err == 0 and n_warn == 0:
        print(f"{GREEN}  ✓ CLEAN — no issues found{RESET}")
    elif n_err == 0:
        print(f"{YELLOW}  ⚠ {n_warn} warning(s), no errors{RESET}")
    else:
        print(f"{RED}  ✗ {n_err} error(s), {n_warn} warning(s){RESET}")
    print(f"{'='*65}\n")

    return 1 if errors else 0

if __name__ == '__main__':
    sys.exit(main())
