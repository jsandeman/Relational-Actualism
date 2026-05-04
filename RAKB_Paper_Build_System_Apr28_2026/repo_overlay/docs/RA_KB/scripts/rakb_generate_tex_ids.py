#!/usr/bin/env python3
"""Regenerate RAKB ID comments in canonical RA TeX papers.

This tool treats the RAKB registry as the canonical source of paper-to-node
mappings and writes non-rendering comments of the form

    % RAKB: RA-ONT-001;RA-LLC-001

immediately before matching TeX section/subsection/... commands.

Default paths assume the RA repository layout:

    docs/RA_KB/registry/source_text_references.csv
    docs/RA_Canonical_Papers/*.tex
    docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026/

It can also fall back to the Stage-D comment-plan CSV when the registry has not
yet been updated with canonical_tex_projection source references.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import difflib
import json
import os
import re
import shutil
import subprocess
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

PAPER_LABELS = ("Paper I", "Paper II", "Paper III", "Paper IV")
PAPER_PATTERNS = OrderedDict([
    ("Paper I", "RA_Paper_I_*.tex"),
    ("Paper II", "RA_Paper_II_*.tex"),
    ("Paper III", "RA_Paper_III_*.tex"),
    ("Paper IV", "RA_Paper_IV_*.tex"),
])
SECTION_RE = re.compile(r"^(?P<prefix>\s*)\\(?P<level>section|subsection|subsubsection|paragraph)\*?\s*\{")
SOURCE_LABEL_RE = re.compile(r"^(Paper\s+(?:I|II|III|IV))\s+[—-]\s+(section|subsection|subsubsection|paragraph):\s*(.+?)\s*$")
RA_ID_RE = re.compile(r"\bRA-[A-Z0-9][A-Z0-9-]*\b")


def now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def unique_keep_order(items: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for x in items:
        if x and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def split_ids(s: str) -> List[str]:
    if not s:
        return []
    return unique_keep_order(RA_ID_RE.findall(s))


def strip_tex_commands_for_title(s: str) -> str:
    """Normalize a TeX section title enough to match registry labels.

    This is intentionally conservative: it is meant for section headers, not
    arbitrary TeX prose.
    """
    x = s.strip()
    # \\texorpdfstring{TeX}{PDF} -> PDF branch
    x = re.sub(r"\\texorpdfstring\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", x)
    # Remove labels in titles, if any.
    x = re.sub(r"\\label\s*\{[^{}]*\}", "", x)
    # Turn common protected spaces/dashes into normal text.
    x = x.replace("~", " ").replace("---", "-").replace("--", "-")
    # Remove math delimiters while preserving content.
    x = x.replace("$", "")
    # Drop simple formatting commands but keep braced content.
    x = re.sub(r"\\(?:textbf|emph|textit|mathrm|mathbf|mathcal|mathbb)\s*\{([^{}]*)\}", r"\1", x)
    # Common commands in headings.
    replacements = {
        r"\\ell": "l",
        r"\\Lambda": "Lambda",
        r"\\Delta": "Delta",
        r"\\mu": "mu",
        r"\\alpha": "alpha",
        r"\\beta": "beta",
        r"\\gamma": "gamma",
        r"\\theta": "theta",
        r"\\mathrm": "",
    }
    for pat, repl in replacements.items():
        x = re.sub(pat, repl, x)
    # Remove remaining backslash commands, keeping following bare word if any out.
    x = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", "", x)
    # Remove braces left by simple macros.
    x = x.replace("{", "").replace("}", "")
    # Normalize unicode dashes.
    x = x.replace("–", "-").replace("—", "-")
    # Collapse whitespace and normalize spacing around hyphen.
    x = re.sub(r"\s+", " ", x).strip()
    x = re.sub(r"\s*-\s*", "-", x)
    return x


def norm_key_title(s: str) -> str:
    x = strip_tex_commands_for_title(s)
    x = x.casefold()
    x = re.sub(r"[^a-z0-9]+", " ", x)
    return re.sub(r"\s+", " ", x).strip()


def extract_braced_argument(line: str, start_index: int) -> Optional[Tuple[str, int]]:
    """Extract braced argument whose opening brace is at or after start_index."""
    open_idx = line.find("{", start_index)
    if open_idx < 0:
        return None
    depth = 0
    buf = []
    i = open_idx
    while i < len(line):
        ch = line[i]
        if ch == "{" and (i == 0 or line[i-1] != "\\"):
            depth += 1
            if depth > 1:
                buf.append(ch)
        elif ch == "}" and (i == 0 or line[i-1] != "\\"):
            depth -= 1
            if depth == 0:
                return "".join(buf), i + 1
            buf.append(ch)
        else:
            if depth >= 1:
                buf.append(ch)
        i += 1
    return None


def section_info(line: str) -> Optional[Tuple[str, str, str]]:
    m = SECTION_RE.match(line)
    if not m:
        return None
    arg = extract_braced_argument(line, m.end() - 1)
    if arg is None:
        return None
    raw_title, _ = arg
    return m.group("level"), raw_title, norm_key_title(raw_title)


def find_paper_files(papers_dir: Path) -> Dict[str, Path]:
    out: Dict[str, Path] = {}
    for label, pattern in PAPER_PATTERNS.items():
        candidates = []
        for p in papers_dir.glob(pattern):
            if not p.is_file():
                continue
            if "RAKB_TeX_RAKB_IDs" in p.parts:
                continue
            if p.name.endswith("_rakb_ids.tex"):
                continue
            candidates.append(p)
        candidates = sorted(candidates, key=lambda p: p.name)
        if candidates:
            # Prefer the longest/final-looking canonical filename, but avoid PDFs etc.
            out[label] = candidates[-1]
    return out


def load_mapping_from_source_refs(registry_dir: Path) -> Tuple[Dict[Tuple[str, str, str], List[str]], List[dict]]:
    path = registry_dir / "source_text_references.csv"
    mapping: Dict[Tuple[str, str, str], List[str]] = defaultdict(list)
    raw_rows: List[dict] = []
    if not path.exists():
        return {}, []
    with path.open(newline="", encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        for row in rdr:
            source_label = (row.get("source_label") or "").strip()
            rel = (row.get("relation") or "").strip()
            # Prefer Stage-C canonical projections. Ignore old vague rows such as "RA Paper I, Axiom 1".
            if rel != "canonical_tex_projection" and "—" not in source_label and " - " not in source_label:
                continue
            m = SOURCE_LABEL_RE.match(source_label)
            if not m:
                continue
            paper, level, title = m.group(1), m.group(2), m.group(3)
            node_id = (row.get("node_id") or "").strip()
            if not node_id:
                continue
            key = (paper, level, norm_key_title(title))
            mapping[key].append(node_id)
            raw_rows.append({**row, "paper": paper, "section_level": level, "section_title": title})
    return {k: unique_keep_order(v) for k, v in mapping.items()}, raw_rows


def load_mapping_from_plan(plan_csv: Path) -> Tuple[Dict[Tuple[str, str, str], List[str]], List[dict]]:
    mapping: Dict[Tuple[str, str, str], List[str]] = defaultdict(list)
    raw_rows: List[dict] = []
    if not plan_csv or not plan_csv.exists():
        return {}, []
    with plan_csv.open(newline="", encoding="utf-8") as fh:
        rdr = csv.DictReader(fh)
        for row in rdr:
            paper = (row.get("paper") or "").strip()
            level = (row.get("section_level") or "").strip()
            title = (row.get("section_title") or "").strip()
            ids = split_ids(row.get("mapped_node_ids") or row.get("rakb_comment") or "")
            if paper and level and title and ids:
                key = (paper, level, norm_key_title(title))
                mapping[key].extend(ids)
                raw_rows.append(row)
    return {k: unique_keep_order(v) for k, v in mapping.items()}, raw_rows


def load_mapping(registry_dir: Path, plan_csv: Optional[Path], mapping_source: str) -> Tuple[str, Dict[Tuple[str, str, str], List[str]], List[dict]]:
    if mapping_source in ("registry", "auto"):
        reg_map, reg_rows = load_mapping_from_source_refs(registry_dir)
        if reg_map or mapping_source == "registry":
            return "registry/source_text_references.csv", reg_map, reg_rows
    if mapping_source in ("plan", "auto") and plan_csv:
        plan_map, plan_rows = load_mapping_from_plan(plan_csv)
        if plan_map or mapping_source == "plan":
            return str(plan_csv), plan_map, plan_rows
    return "none", {}, []


def collect_registry_ids(registry_dir: Path) -> set:
    ids = set()
    if registry_dir.exists():
        for p in registry_dir.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".csv", ".yaml", ".yml", ".md", ".json"}:
                try:
                    ids.update(RA_ID_RE.findall(p.read_text(encoding="utf-8", errors="ignore")))
                except Exception:
                    pass
    return ids


def rakb_comment(ids: Sequence[str]) -> str:
    return "% RAKB: " + ";".join(unique_keep_order(ids))


def process_tex(text: str, paper_label: str, mapping: Dict[Tuple[str, str, str], List[str]], visible_ids: bool = False) -> Tuple[str, List[dict], List[dict]]:
    lines = text.splitlines(keepends=True)
    out: List[str] = []
    insertion_log: List[dict] = []
    unmapped_sections: List[dict] = []
    existing_comment_buffer: List[str] = []
    for idx, line in enumerate(lines, start=1):
        if line.strip().startswith("% RAKB:"):
            existing_comment_buffer.append(line.strip())
            # Drop old generated comments. They will be regenerated from the registry.
            continue
        info = section_info(line)
        if info:
            level, raw_title, title_key = info
            key = (paper_label, level, title_key)
            ids = mapping.get(key, [])
            if ids:
                comment = rakb_comment(ids)
                out.append(comment + ("\n" if line.endswith("\n") else "\n"))
                if visible_ids:
                    out.append(r"\RAKBID{" + ";".join(ids) + "}\n")
                insertion_log.append({
                    "paper": paper_label,
                    "line": idx,
                    "section_level": level,
                    "section_title_raw": raw_title,
                    "section_title_normalized": strip_tex_commands_for_title(raw_title),
                    "mapped_node_ids": ";".join(ids),
                    "inserted_comment": comment,
                    "replaced_existing_comments": " | ".join(existing_comment_buffer),
                })
            else:
                unmapped_sections.append({
                    "paper": paper_label,
                    "line": idx,
                    "section_level": level,
                    "section_title_raw": raw_title,
                    "section_title_normalized": strip_tex_commands_for_title(raw_title),
                })
            existing_comment_buffer = []
        elif existing_comment_buffer:
            # Old comment was not attached to a section. Preserve it as a warning-like source comment.
            for c in existing_comment_buffer:
                out.append("% STALE-RAKB-COMMENT: " + c + "\n")
            existing_comment_buffer = []
        out.append(line)
    return "".join(out), insertion_log, unmapped_sections


def write_csv(path: Path, rows: List[dict], fieldnames: Optional[List[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys = []
        for r in rows:
            for k in r.keys():
                if k not in keys:
                    keys.append(k)
        fieldnames = keys or ["status"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=fieldnames)
        wr.writeheader()
        for r in rows:
            wr.writerow({k: r.get(k, "") for k in fieldnames})


def run_latexmk(tex_files: List[Path], workdir: Path, reports_dir: Path) -> List[dict]:
    results = []
    for tex in tex_files:
        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", tex.name]
        try:
            proc = subprocess.run(cmd, cwd=str(workdir), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
            status = "passed" if proc.returncode == 0 else "failed"
            log_path = reports_dir / f"compile_{tex.stem}.log"
            write_text(log_path, proc.stdout)
            results.append({"tex_file": str(tex), "status": status, "returncode": proc.returncode, "log": str(log_path)})
        except FileNotFoundError:
            results.append({"tex_file": str(tex), "status": "skipped_latexmk_not_found", "returncode": "", "log": ""})
            break
        except subprocess.TimeoutExpired as e:
            log_path = reports_dir / f"compile_{tex.stem}.timeout.log"
            write_text(log_path, e.stdout or "")
            results.append({"tex_file": str(tex), "status": "timeout", "returncode": "", "log": str(log_path)})
    return results


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Regenerate RAKB ID comments in canonical RA TeX papers.")
    ap.add_argument("--repo", default=".", help="RA repository root. Default: current directory.")
    ap.add_argument("--kb", default="docs/RA_KB", help="Path to RA_KB relative to repo or absolute.")
    ap.add_argument("--papers", default="docs/RA_Canonical_Papers", help="Canonical papers dir relative to repo or absolute.")
    ap.add_argument("--output-root", default="docs/RA_Canonical_Papers/RAKB_TeX_RAKB_IDs_Apr28_2026", help="Output root for generated TeX/report files.")
    ap.add_argument("--plan-csv", default="docs/RA_KB/reports/RAKB_stageD_tex_rakb_comment_plan_Apr28_2026.csv", help="Fallback comment-plan CSV.")
    ap.add_argument("--mapping-source", choices=["auto", "registry", "plan"], default="auto", help="Where to read paper-to-RAKB mappings.")
    ap.add_argument("--suffix", default="_rakb_ids", help="Suffix for generated TeX filenames.")
    ap.add_argument("--drop-in", action="store_true", help="Also write drop-in replacement TeX files with original filenames.")
    ap.add_argument("--in-place", action="store_true", help="Overwrite canonical TeX files in place. A timestamped backup is created. Use only after review.")
    ap.add_argument("--visible-ids", action="store_true", help="Insert visible \\RAKBID{...} macros after comments. Requires ra_suite.sty or equivalent. Default uses comments only.")
    ap.add_argument("--compile", action="store_true", help="Run latexmk on generated TeX files if latexmk is available.")
    ap.add_argument("--fail-on-unmatched", action="store_true", help="Exit nonzero if any mapping row is not inserted.")
    args = ap.parse_args(argv)

    repo = Path(args.repo).resolve()
    kb_dir = (repo / args.kb).resolve() if not Path(args.kb).is_absolute() else Path(args.kb)
    registry_dir = kb_dir / "registry"
    papers_dir = (repo / args.papers).resolve() if not Path(args.papers).is_absolute() else Path(args.papers)
    output_root = (repo / args.output_root).resolve() if not Path(args.output_root).is_absolute() else Path(args.output_root)
    generated_dir = output_root / "generated_tex"
    dropin_dir = output_root / "drop_in_replacements"
    reports_dir = output_root / "reports"
    diffs_dir = output_root / "diffs"
    plan_csv = (repo / args.plan_csv).resolve() if args.plan_csv and not Path(args.plan_csv).is_absolute() else Path(args.plan_csv) if args.plan_csv else None

    mapping_label, mapping, mapping_rows = load_mapping(registry_dir, plan_csv, args.mapping_source)
    if not mapping:
        print("ERROR: No RAKB paper mappings found. Expected registry/source_text_references.csv canonical_tex_projection rows or a Stage-D plan CSV.", file=sys.stderr)
        return 2

    paper_files = find_paper_files(papers_dir)
    missing_papers = [p for p in PAPER_LABELS if p not in paper_files]
    if missing_papers:
        print(f"WARNING: missing canonical TeX files for: {', '.join(missing_papers)}", file=sys.stderr)

    valid_ids = collect_registry_ids(registry_dir)
    id_warnings = []
    for key, ids in mapping.items():
        for rid in ids:
            if valid_ids and rid not in valid_ids:
                id_warnings.append({"paper": key[0], "section_level": key[1], "section_title_normalized": key[2], "node_id": rid, "warning": "id_not_found_elsewhere_in_registry_text"})

    all_insertions: List[dict] = []
    all_unmapped_sections: List[dict] = []
    inserted_keys = set()
    generated_files: List[Path] = []
    file_summary: List[dict] = []

    for paper_label, src in paper_files.items():
        original = read_text(src)
        annotated, insertions, unmapped_sections = process_tex(original, paper_label, mapping, visible_ids=args.visible_ids)
        for ins in insertions:
            inserted_keys.add((ins["paper"], ins["section_level"], norm_key_title(ins["section_title_raw"])))
        all_insertions.extend(insertions)
        all_unmapped_sections.extend(unmapped_sections)

        out_name = src.with_name(src.stem + args.suffix + src.suffix).name
        out_path = generated_dir / out_name
        write_text(out_path, annotated)
        generated_files.append(out_path)

        # Write drop-in replacement with original filename for review/copying.
        if args.drop_in or True:
            write_text(dropin_dir / src.name, annotated)

        # Unified diff against source.
        diff = "".join(difflib.unified_diff(
            original.splitlines(keepends=True),
            annotated.splitlines(keepends=True),
            fromfile=str(src),
            tofile=str(out_path),
        ))
        write_text(diffs_dir / f"{src.stem}.diff", diff)

        if args.in_place:
            backup = src.with_suffix(src.suffix + f".bak_{now_stamp()}")
            shutil.copy2(src, backup)
            write_text(src, annotated)

        file_summary.append({
            "paper": paper_label,
            "source_file": str(src.relative_to(repo) if src.is_relative_to(repo) else src),
            "generated_file": str(out_path.relative_to(repo) if out_path.is_relative_to(repo) else out_path),
            "drop_in_file": str((dropin_dir / src.name).relative_to(repo) if (dropin_dir / src.name).is_relative_to(repo) else (dropin_dir / src.name)),
            "inserted_comments": sum(1 for r in insertions if r["paper"] == paper_label),
            "unmapped_sections": sum(1 for r in unmapped_sections if r["paper"] == paper_label),
        })

    unmatched_mapping = []
    for key, ids in sorted(mapping.items()):
        if key not in inserted_keys:
            unmatched_mapping.append({
                "paper": key[0],
                "section_level": key[1],
                "section_title_normalized": key[2],
                "mapped_node_ids": ";".join(ids),
                "status": "mapping_not_inserted",
            })

    compile_results = run_latexmk(generated_files, generated_dir, reports_dir) if args.compile else []

    write_csv(reports_dir / "rakb_tex_id_insertion_log.csv", all_insertions)
    write_csv(reports_dir / "rakb_tex_id_unmapped_sections.csv", all_unmapped_sections)
    write_csv(reports_dir / "rakb_tex_id_unmatched_mapping_rows.csv", unmatched_mapping)
    write_csv(reports_dir / "rakb_tex_id_file_summary.csv", file_summary)
    write_csv(reports_dir / "rakb_tex_id_registry_id_warnings.csv", id_warnings)
    if compile_results:
        write_csv(reports_dir / "rakb_tex_id_compile_results.csv", compile_results)

    manifest = {
        "generated_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "repo": str(repo),
        "kb_dir": str(kb_dir),
        "papers_dir": str(papers_dir),
        "output_root": str(output_root),
        "mapping_source": mapping_label,
        "mapping_keys": len(mapping),
        "inserted_comments": len(all_insertions),
        "unmatched_mapping_rows": len(unmatched_mapping),
        "unmapped_sections": len(all_unmapped_sections),
        "id_warnings": len(id_warnings),
        "generated_files": [str(p) for p in generated_files],
    }
    write_text(reports_dir / "rakb_tex_generation_manifest.json", json.dumps(manifest, indent=2))

    report = f"""# RAKB TeX ID generation report

Generated at: `{manifest['generated_at']}`

Mapping source: `{mapping_label}`

Output root: `{output_root}`

## Summary

- Mapping keys: {len(mapping)}
- Inserted comments: {len(all_insertions)}
- Unmatched mapping rows: {len(unmatched_mapping)}
- Unmapped TeX sections: {len(all_unmapped_sections)}
- Registry ID warnings: {len(id_warnings)}

Generated TeX files are in:

```text
{generated_dir}
```

Drop-in replacements are in:

```text
{dropin_dir}
```

The comments are non-rendering source annotations. They are regenerated from the RAKB registry/comment plan and should not be hand-edited in TeX.
"""
    write_text(output_root / "RAKB_TeX_ID_Generation_Report.md", report)

    print(json.dumps(manifest, indent=2))
    if args.fail_on_unmatched and unmatched_mapping:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
