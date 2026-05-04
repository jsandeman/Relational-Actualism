#!/usr/bin/env python3
"""Insert non-rendering `% RAKB:` comments into canonical RA TeX files.

Expected comment-plan columns:
  paper, section_level, section_title, rakb_comment, mapped_node_ids, ...

Example:
  python scripts/insert_rakb_tex_ids.py \
    --tex-dir docs/RA_Canonical_Papers \
    --comment-plan docs/RA_KB/reports/RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv \
    --out-dir docs/RA_Canonical_Papers_RAKB_IDs
"""
from __future__ import annotations

import argparse
import csv
import difflib
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

PAPER_FILE_PATTERNS = {
    "Paper I": "RA_Paper_I_*.tex",
    "Paper II": "RA_Paper_II_*.tex",
    "Paper III": "RA_Paper_III_*.tex",
    "Paper IV": "RA_Paper_IV_*.tex",
}


def find_matching_brace(s: str, open_idx: int) -> int:
    depth = 0
    escaped = False
    for i in range(open_idx, len(s)):
        ch = s[i]
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
    raise ValueError(f"no matching brace at {open_idx}")


def parse_heading_at(s: str, start: int) -> Tuple[str, bool, str, int, int]:
    backslash = start + s[start:].find("\\")
    m = re.match(r"\\(section|subsection|subsubsection)(\*)?\s*\{", s[backslash:])
    if not m:
        raise ValueError("not a section-like command")
    level = m.group(1)
    starred = bool(m.group(2))
    open_idx = backslash + m.end() - 1
    close_idx = find_matching_brace(s, open_idx)
    return level, starred, s[open_idx + 1 : close_idx], backslash, close_idx + 1


def iter_headings(s: str) -> List[dict]:
    pattern = re.compile(r"(?m)^[ \t]*\\(?:section|subsection|subsubsection)\*?\s*\{")
    out = []
    for m in pattern.finditer(s):
        try:
            level, starred, title_tex, start, end = parse_heading_at(s, m.start())
            out.append({
                "level": level,
                "starred": starred,
                "title_tex": title_tex,
                "start": start,
                "end": end,
                "line": s.count("\n", 0, start) + 1,
            })
        except Exception as exc:
            out.append({"error": str(exc), "start": m.start()})
    return out


def strip_texorpdfstring(text: str) -> str:
    token = r"\texorpdfstring"
    out = []
    i = 0
    while i < len(text):
        j = text.find(token, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        k = j + len(token)
        while k < len(text) and text[k].isspace():
            k += 1
        if k >= len(text) or text[k] != "{":
            out.append(token)
            i = k
            continue
        a1 = find_matching_brace(text, k)
        k2 = a1 + 1
        while k2 < len(text) and text[k2].isspace():
            k2 += 1
        if k2 >= len(text) or text[k2] != "{":
            out.append(text[j:k2])
            i = k2
            continue
        a2 = find_matching_brace(text, k2)
        out.append(text[k2 + 1 : a2])
        i = a2 + 1
    return "".join(out)


def norm_title(text: str) -> str:
    text = strip_texorpdfstring(text)
    for cmd in ["emph", "textit", "textbf", "mathrm", "mathit", "textrm"]:
        pat = re.compile(r"\\" + cmd + r"\s*\{([^{}]*)\}")
        while True:
            new = pat.sub(r"\1", text)
            if new == text:
                break
            text = new
    text = text.replace("$", " ").replace("~", " ")
    text = text.replace(r"\ell", "l").replace(r"\Lambda", "Lambda")
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)
    text = text.replace("{", " ").replace("}", " ").lower()
    text = text.replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", "", text)


def read_rows(path: Path) -> List[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: List[dict], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tex-dir", required=True, type=Path)
    parser.add_argument("--comment-plan", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--diff-dir", type=Path)
    parser.add_argument("--report-dir", type=Path)
    parser.add_argument("--suffix", default="_rakb_ids")
    parser.add_argument("--clean", action="store_true")
    args = parser.parse_args()

    out_dir = args.out_dir
    diff_dir = args.diff_dir or out_dir.parent / "rakb_id_diffs"
    report_dir = args.report_dir or out_dir.parent / "rakb_id_reports"
    if args.clean:
        for p in [out_dir, diff_dir, report_dir]:
            if p.exists():
                shutil.rmtree(p)
    out_dir.mkdir(parents=True, exist_ok=True)
    diff_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    rows = read_rows(args.comment_plan)
    by_paper: Dict[str, List[dict]] = {}
    for row in rows:
        by_paper.setdefault(row["paper"], []).append(row)

    log_rows: List[dict] = []
    unmatched: List[dict] = []
    summary: List[dict] = []

    for paper, pattern in PAPER_FILE_PATTERNS.items():
        matches = sorted(args.tex_dir.glob(pattern))
        if len(matches) != 1:
            raise RuntimeError(f"{paper}: expected one {pattern}, found {len(matches)}")
        src = matches[0]
        text = src.read_text(encoding="utf-8")
        headings = [h for h in iter_headings(text) if "error" not in h]
        index: Dict[Tuple[str, str], List[dict]] = {}
        for h in headings:
            index.setdefault((h["level"], norm_title(h["title_tex"])), []).append(h)

        insertions = []
        used = set()
        for row in by_paper.get(paper, []):
            level = row["section_level"].strip()
            title = row["section_title"].strip()
            candidates = index.get((level, norm_title(title)), [])
            if not candidates:
                import difflib as _difflib
                scored = []
                for h in headings:
                    if h["level"] == level:
                        scored.append((_difflib.SequenceMatcher(None, norm_title(title), norm_title(h["title_tex"])).ratio(), h))
                scored.sort(key=lambda x: x[0], reverse=True)
                if scored and scored[0][0] >= 0.82:
                    candidates = [scored[0][1]]
                else:
                    unmatched.append({
                        "paper": paper,
                        "section_level": level,
                        "section_title": title,
                        "mapped_node_ids": row["mapped_node_ids"],
                        "reason": "no matching heading",
                        "best_match": scored[0][1]["title_tex"] if scored else "",
                        "best_match_score": f"{scored[0][0]:.3f}" if scored else "",
                    })
                    continue
            chosen = next((h for h in candidates if h["start"] not in used), candidates[0])
            used.add(chosen["start"])
            comment = row["rakb_comment"].strip() or f"% RAKB: {row['mapped_node_ids']}"
            if not comment.startswith("%"):
                comment = "% " + comment
            insertions.append((chosen["start"], comment + "\n"))
            log_rows.append({
                "paper": paper,
                "source_file": src.name,
                "output_file": src.stem + args.suffix + ".tex",
                "section_level": level,
                "section_title_plan": title,
                "section_title_tex": chosen["title_tex"],
                "line": chosen["line"],
                "mapped_node_ids": row["mapped_node_ids"],
                "rakb_comment": comment,
                "status": "inserted",
            })

        new_text = text
        for pos, comment in sorted(insertions, key=lambda x: x[0], reverse=True):
            new_text = new_text[:pos] + comment + new_text[pos:]
        new_text = (
            "% RAKB-ID annotated source generated from Stage D comment plan.\n"
            "% RAKB-ID mode: non-rendering TeX comments only; prose/equations unchanged.\n"
            + new_text
        )
        out = out_dir / (src.stem + args.suffix + ".tex")
        out.write_text(new_text, encoding="utf-8")
        diff = "".join(difflib.unified_diff(
            text.splitlines(keepends=True), new_text.splitlines(keepends=True),
            fromfile=f"a/{src.name}", tofile=f"b/{out.name}"
        ))
        (diff_dir / (src.stem + args.suffix + ".diff")).write_text(diff, encoding="utf-8")
        summary.append({
            "paper": paper,
            "source_file": src.name,
            "output_file": out.name,
            "heading_count": len(headings),
            "planned_comments": len(by_paper.get(paper, [])),
            "inserted_comments": len([r for r in log_rows if r["paper"] == paper]),
            "unmatched_comments": len([r for r in unmatched if r["paper"] == paper]),
        })

    write_csv(report_dir / "RAKB_tex_id_insertion_log.csv", log_rows,
              ["paper","source_file","output_file","section_level","section_title_plan","section_title_tex","line","mapped_node_ids","rakb_comment","status"])
    write_csv(report_dir / "RAKB_tex_id_unmatched_plan_rows.csv", unmatched,
              ["paper","section_level","section_title","mapped_node_ids","reason","best_match","best_match_score"])
    write_csv(report_dir / "RAKB_tex_id_file_summary.csv", summary,
              ["paper","source_file","output_file","heading_count","planned_comments","inserted_comments","unmatched_comments"])

if __name__ == "__main__":
    main()
