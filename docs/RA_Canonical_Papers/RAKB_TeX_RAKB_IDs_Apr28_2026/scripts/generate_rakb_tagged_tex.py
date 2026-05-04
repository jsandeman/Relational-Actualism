#!/usr/bin/env python3
from __future__ import annotations

import csv
import difflib
import re
import shutil
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional

BASE = Path('/mnt/data')
CANON = BASE / 'work_tex/canonical/docs/RA_Canonical_Papers'
PLAN = BASE / 'RAKB_StageD_Synthesis_Apr28_2026/reports/RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv'
OUTROOT = BASE / 'RAKB_TeX_RAKB_IDs_Apr28_2026'
OUTDOCS = OUTROOT / 'docs/RA_Canonical_Papers_RAKB_IDs'
REPORTS = OUTROOT / 'reports'
DIFFS = OUTROOT / 'diffs'
SCRIPTS = OUTROOT / 'scripts'

PAPER_FILE_PATTERNS = {
    'Paper I': 'RA_Paper_I_*.tex',
    'Paper II': 'RA_Paper_II_*.tex',
    'Paper III': 'RA_Paper_III_*.tex',
    'Paper IV': 'RA_Paper_IV_*.tex',
}

COMMAND_LEVELS = ('section', 'subsection', 'subsubsection')

def read_csv(path: Path) -> List[dict]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def find_matching_brace(s: str, open_idx: int) -> int:
    # open_idx is at '{'
    depth = 0
    escaped = False
    for i in range(open_idx, len(s)):
        ch = s[i]
        if escaped:
            escaped = False
            continue
        if ch == '\\':
            escaped = True
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f'no matching brace at {open_idx}')

def parse_tex_command_arg(s: str, command_start: int) -> Tuple[str, bool, str, int, int]:
    # command_start begins at backslash before section-like command.
    m = re.match(r'\\(section|subsection|subsubsection)(\*)?\s*\{', s[command_start:])
    if not m:
        raise ValueError('not section command')
    level = m.group(1)
    starred = bool(m.group(2))
    open_idx = command_start + m.end() - 1
    close_idx = find_matching_brace(s, open_idx)
    title_tex = s[open_idx+1:close_idx]
    return level, starred, title_tex, command_start, close_idx + 1

def iter_headings(s: str) -> List[dict]:
    headings = []
    # Match only at line starts, allowing leading whitespace.
    pattern = re.compile(r'(?m)^[ \t]*\\(?:section|subsection|subsubsection)\*?\s*\{')
    for m in pattern.finditer(s):
        try:
            level, starred, title_tex, start, end = parse_tex_command_arg(s, m.start() + s[m.start():m.end()].find('\\'))
        except Exception as e:
            headings.append({'error': str(e), 'start': m.start()})
            continue
        headings.append({
            'level': level,
            'starred': starred,
            'title_tex': title_tex,
            'start': start,
            'end': end,
            'line': s.count('\n', 0, start) + 1,
        })
    return headings

def texorpdf_repl(text: str) -> str:
    # Replace \texorpdfstring{tex}{pdf} with pdf argument. Minimal balanced parser.
    token = r'\texorpdfstring'
    out = []
    i = 0
    while i < len(text):
        j = text.find(token, i)
        if j == -1:
            out.append(text[i:])
            break
        out.append(text[i:j])
        k = j + len(token)
        while k < len(text) and text[k].isspace():
            k += 1
        if k >= len(text) or text[k] != '{':
            out.append(token)
            i = k
            continue
        a1_end = find_matching_brace(text, k)
        k2 = a1_end + 1
        while k2 < len(text) and text[k2].isspace():
            k2 += 1
        if k2 >= len(text) or text[k2] != '{':
            out.append(text[j:k2])
            i = k2
            continue
        a2_end = find_matching_brace(text, k2)
        pdf_arg = text[k2+1:a2_end]
        out.append(pdf_arg)
        i = a2_end + 1
    return ''.join(out)

def strip_simple_tex_commands(text: str) -> str:
    # Convert simple one-arg text commands by dropping the command and keeping content.
    text = texorpdf_repl(text)
    for cmd in ['emph', 'textit', 'textbf', 'mathrm', 'mathit', 'textrm']:
        # repeat until no change to handle nested simple uses.
        pat = re.compile(r'\\' + cmd + r'\s*\{([^{}]*)\}')
        while True:
            new = pat.sub(r'\1', text)
            if new == text:
                break
            text = new
    # Remove math delimiters and common TeX spacing.
    text = text.replace('$', ' ')
    text = text.replace('~', ' ')
    text = text.replace('\u00a0', ' ')
    text = text.replace('\\,', ' ')
    text = text.replace('\\;', ' ')
    text = text.replace('\\:', ' ')
    text = text.replace('\\!', ' ')
    # Greek/letter commands used in titles.
    replacements = {
        r'\ell': 'l',
        r'\Lambda': 'Lambda',
        r'\mathrm': '',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove remaining TeX command names but leave following braced text as plain after braces stripped.
    text = re.sub(r'\\[a-zA-Z]+\*?', ' ', text)
    text = text.replace('{', ' ').replace('}', ' ')
    return text

def norm_title(text: str) -> str:
    text = strip_simple_tex_commands(text)
    text = text.lower()
    text = text.replace('&', ' and ')
    # Keep alphanumeric only, so d=4 and d 4 match.
    text = re.sub(r'[^a-z0-9]+', '', text)
    return text

def make_comment(row: dict) -> str:
    # Keep the parser-friendly line first.
    ids = row['mapped_node_ids'].strip()
    return f"% RAKB: {ids}\n"

def main() -> None:
    if OUTROOT.exists():
        shutil.rmtree(OUTROOT)
    OUTDOCS.mkdir(parents=True)
    REPORTS.mkdir(parents=True)
    DIFFS.mkdir(parents=True)
    SCRIPTS.mkdir(parents=True)

    plan_rows = read_csv(PLAN)
    by_paper: Dict[str, List[dict]] = {}
    for r in plan_rows:
        by_paper.setdefault(r['paper'], []).append(r)

    log_rows = []
    unmatched = []
    file_summary = []

    for paper, pattern in PAPER_FILE_PATTERNS.items():
        matches = sorted(CANON.glob(pattern))
        if len(matches) != 1:
            raise RuntimeError(f'{paper}: expected 1 match for {pattern}, got {matches}')
        src = matches[0]
        text = src.read_text(encoding='utf-8')
        headings = iter_headings(text)
        idx: Dict[Tuple[str, str], List[dict]] = {}
        for h in headings:
            if 'error' in h:
                continue
            idx.setdefault((h['level'], norm_title(h['title_tex'])), []).append(h)

        # Add generated header after documentclass/comments block? Keep as a TeX comment at file start.
        header = (
            "% RAKB-ID annotated source generated 2026-04-28 from Stage D comment plan.\n"
            "% RAKB-ID mode: non-rendering TeX comments only; mathematical/prose content unchanged.\n"
        )
        insertions: List[Tuple[int, str, dict, dict]] = []
        used_heading_starts = set()
        for r in by_paper.get(paper, []):
            level = r['section_level'].strip()
            title = r['section_title'].strip()
            key = (level, norm_title(title))
            candidates = idx.get(key, [])
            if not candidates:
                # fuzzy fallback restricted to same level
                all_same = [h for h in headings if 'error' not in h and h['level'] == level]
                scored = []
                for h in all_same:
                    nt = norm_title(title)
                    nh = norm_title(h['title_tex'])
                    # simple similarity using SequenceMatcher
                    import difflib as _difflib
                    score = _difflib.SequenceMatcher(None, nt, nh).ratio()
                    scored.append((score, h))
                scored.sort(key=lambda x: x[0], reverse=True)
                if scored and scored[0][0] >= 0.82:
                    candidates = [scored[0][1]]
                else:
                    unmatched.append({
                        'paper': paper,
                        'section_level': level,
                        'section_title': title,
                        'mapped_node_ids': r['mapped_node_ids'],
                        'reason': 'no matching TeX heading',
                        'best_match': scored[0][1]['title_tex'] if scored else '',
                        'best_match_score': f'{scored[0][0]:.3f}' if scored else '',
                    })
                    continue
            # If duplicates, choose unused first.
            chosen = None
            for h in candidates:
                if h['start'] not in used_heading_starts:
                    chosen = h
                    break
            if chosen is None:
                chosen = candidates[0]
            used_heading_starts.add(chosen['start'])
            comment = make_comment(r)
            # Avoid duplicate insertion if already immediately above.
            prefix = text[max(0, chosen['start']-250):chosen['start']]
            if comment.strip() in prefix.splitlines()[-5:]:
                status = 'already_present'
            else:
                insertions.append((chosen['start'], comment, r, chosen))
                status = 'inserted'
            log_rows.append({
                'paper': paper,
                'source_file': src.name,
                'output_file': src.stem + '_rakb_ids.tex',
                'section_level': level,
                'section_title_plan': title,
                'section_title_tex': chosen['title_tex'],
                'line': chosen['line'],
                'mapped_node_ids': r['mapped_node_ids'],
                'rakb_comment': comment.strip(),
                'status': status,
            })

        # Apply insertions from bottom to top; plus header at start.
        new_text = text
        for pos, comment, r, h in sorted(insertions, key=lambda x: x[0], reverse=True):
            new_text = new_text[:pos] + comment + new_text[pos:]
        new_text = header + new_text
        outname = src.stem + '_rakb_ids.tex'
        out = OUTDOCS / outname
        out.write_text(new_text, encoding='utf-8')

        diff = ''.join(difflib.unified_diff(
            text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            fromfile=f'a/{src.name}',
            tofile=f'b/{outname}',
        ))
        (DIFFS / (src.stem + '_rakb_ids.diff')).write_text(diff, encoding='utf-8')
        file_summary.append({
            'paper': paper,
            'source_file': src.name,
            'output_file': outname,
            'heading_count': sum(1 for h in headings if 'error' not in h),
            'planned_comments': len(by_paper.get(paper, [])),
            'inserted_comments': sum(1 for row in log_rows if row['paper'] == paper and row['status'] == 'inserted'),
            'unmatched_comments': sum(1 for row in unmatched if row['paper'] == paper),
        })

    # Write reports.
    def write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
        with path.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in rows:
                w.writerow(r)
    write_csv(REPORTS / 'RAKB_tex_id_insertion_log_Apr28_2026.csv', log_rows, [
        'paper','source_file','output_file','section_level','section_title_plan','section_title_tex','line','mapped_node_ids','rakb_comment','status'
    ])
    write_csv(REPORTS / 'RAKB_tex_id_unmatched_plan_rows_Apr28_2026.csv', unmatched, [
        'paper','section_level','section_title','mapped_node_ids','reason','best_match','best_match_score'
    ])
    write_csv(REPORTS / 'RAKB_tex_id_file_summary_Apr28_2026.csv', file_summary, [
        'paper','source_file','output_file','heading_count','planned_comments','inserted_comments','unmatched_comments'
    ])
    shutil.copy2(PLAN, REPORTS / 'RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv')

    total_inserted = sum(int(r['inserted_comments']) for r in file_summary)
    total_planned = sum(int(r['planned_comments']) for r in file_summary)
    total_unmatched = len(unmatched)
    report = f"""# RAKB-ID TeX Annotation Report — Apr 28, 2026

Generated four canonical TeX sources with explicit, non-rendering RAKB ID comments.

## Summary

- Planned RAKB comment rows: {total_planned}
- Inserted RAKB comments: {total_inserted}
- Unmatched plan rows: {total_unmatched}
- Annotation mode: TeX comments only (`% RAKB: ...`), so prose, equations, labels, citations, and rendered PDF output should be unchanged except for source comments.

## Files

"""
    for r in file_summary:
        report += f"- {r['paper']}: `{r['output_file']}` — {r['inserted_comments']}/{r['planned_comments']} comments inserted; unmatched={r['unmatched_comments']}\n"
    report += """
## How to use

Copy the generated files from:

```text
docs/RA_Canonical_Papers_RAKB_IDs/
```

into your canonical paper directory when ready, or apply the unified diffs in:

```text
diffs/
```

The inserted comments are intentionally parser-friendly:

```tex
% RAKB: RA-ONT-001;RA-LLC-001
\subsection{From causal order to universe-state}
```

## Caveat

These comments encode the Stage D curated paper-to-RAKB crosswalk. They are not new proof claims and do not promote restoration candidates into `claims.yaml`.
"""
    (OUTROOT / 'RAKB_TeX_RAKB_ID_Annotation_Report_Apr28_2026.md').write_text(report, encoding='utf-8')

    # Include this generator as a reusable script with same defaults but repo-oriented paths as comments.
    script_text = Path(__file__).read_text(encoding='utf-8') if '__file__' in globals() else ''
    (SCRIPTS / 'generate_rakb_tagged_tex.py').write_text(script_text, encoding='utf-8')

    # README
    readme = """# RAKB-tagged TeX sources

This packet contains non-rendering TeX source annotations for the four canonical RA papers.

Each inserted annotation has the form:

```tex
% RAKB: RA-...
```

Use the generated `_rakb_ids.tex` files for review, or apply the diffs into the canonical files.

The source content is otherwise unchanged.
"""
    (OUTROOT / 'README.md').write_text(readme, encoding='utf-8')

if __name__ == '__main__':
    main()
