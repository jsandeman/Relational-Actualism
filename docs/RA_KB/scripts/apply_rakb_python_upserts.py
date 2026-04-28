#!/usr/bin/env python3
"""Apply Stage B Python-audit CSV upserts to RAKB v0.5 registry tables.

This edits only RAKB CSV registry files; it does not modify Python/Lean/TeX sources.
"""
from __future__ import annotations
import argparse, csv, shutil
from datetime import datetime
from pathlib import Path

PATCHES = [
    ("artifacts.csv", "RAKB_python_artifacts_upsert_v1_Apr28_2026.csv", ["artifact_id"]),
    ("claim_artifact_edges.csv", "RAKB_python_claim_artifact_edges_upsert_v1_Apr28_2026.csv", ["claim_id", "artifact_id", "relation"]),
    ("restoration_candidates.csv", "RAKB_python_restoration_candidates_upsert_v1_Apr28_2026.csv", ["candidate_id"]),
]

REPORTS = [
    "RAKB_python_source_classification_Apr28_2026.csv",
    "RAKB_python_reproduction_smoke_tests_Apr28_2026.csv",
    "RAKB_python_hardening_queue_Apr28_2026.csv",
    "RAKB_python_top_level_execution_audit_Apr28_2026.csv",
]

def read_csv(path: Path):
    if not path.exists(): return [], []
    with path.open(newline="", encoding="utf-8") as f:
        r=csv.DictReader(f); return list(r), list(r.fieldnames or [])

def write_csv(path: Path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader(); [w.writerow({k: row.get(k, "") for k in fields}) for row in rows]

def upsert(target: Path, patch: Path, keys, dry=False):
    trows, tfields = read_csv(target)
    prows, pfields = read_csv(patch)
    if not prows:
        print(f"SKIP: {patch} has no rows"); return
    fields = pfields if not tfields else tfields + [c for c in pfields if c not in tfields]
    idx={tuple(r.get(k,"") for k in keys):i for i,r in enumerate(trows)}
    add=upd=0
    for row in prows:
        key=tuple(row.get(k,"") for k in keys)
        if key in idx:
            for c in pfields: trows[idx[key]][c]=row.get(c,"")
            upd += 1
        else:
            trows.append(row); idx[key]=len(trows)-1; add += 1
    print(f"{target}: {add} added, {upd} updated from {patch.name}")
    if dry: return
    if target.exists():
        backup = target.with_suffix(target.suffix + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        shutil.copy2(target, backup); print(f"  backup: {backup}")
    write_csv(target, trows, fields)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--registry", default="docs/RA_KB/registry")
    ap.add_argument("--patch-dir", required=True)
    ap.add_argument("--reports", default="docs/RA_KB/reports")
    ap.add_argument("--dry-run", action="store_true")
    args=ap.parse_args()
    registry=Path(args.registry); patch_dir=Path(args.patch_dir); reports=Path(args.reports)
    for target, patch, keys in PATCHES:
        upsert(registry/target, patch_dir/patch, keys, args.dry_run)
    for name in REPORTS:
        src=patch_dir/name
        if src.exists():
            print(f"copy report: {name} -> {reports/name}")
            if not args.dry_run:
                reports.mkdir(parents=True, exist_ok=True); shutil.copy2(src, reports/name)
    print("Done. Run: python scripts/validate_rakb_v0_5.py")
if __name__ == "__main__": main()
