#!/usr/bin/env python3
"""
Apply Stage C RAKB registry upserts.

This appends/upserts:
  - source_text_references.csv by key (node_id, source_label, relation)
  - restoration_candidates.csv by key candidate_id

Run from docs/RA_KB, e.g.

python scripts/apply_rakb_stageC_upserts.py \
  --registry ./registry \
  --patch-dir ./reports/patches/Apr28_stageC_v1 \
  --reports ./reports \
  --dry-run
"""
from __future__ import annotations
import argparse, csv, shutil
from pathlib import Path
from datetime import datetime

def read_csv(path: Path):
    if not path.exists():
        return [], []
    with path.open(newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        return list(r), list(r.fieldnames or [])

def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, '') for k in fieldnames})

def merge_by_key(registry_path: Path, patch_path: Path, key_fields, dry_run=False):
    old_rows, old_fields = read_csv(registry_path)
    patch_rows, patch_fields = read_csv(patch_path)
    if not patch_rows:
        print(f"{registry_path}: no patch rows from {patch_path.name}")
        return
    fieldnames = list(old_fields or patch_fields)
    for f in patch_fields:
        if f not in fieldnames:
            fieldnames.append(f)
    idx = {tuple(r.get(k,'') for k in key_fields): i for i,r in enumerate(old_rows)}
    added = updated = 0
    rows = [dict(r) for r in old_rows]
    for pr in patch_rows:
        key = tuple(pr.get(k,'') for k in key_fields)
        if key in idx:
            i = idx[key]
            changed = False
            for f,v in pr.items():
                if v != '' and rows[i].get(f,'') != v:
                    rows[i][f]=v
                    changed = True
            if changed: updated += 1
        else:
            rows.append(dict(pr))
            idx[key]=len(rows)-1
            added += 1
    print(f"{registry_path}: {added} added, {updated} updated from {patch_path.name}")
    if not dry_run:
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        if registry_path.exists():
            bak = registry_path.with_name(registry_path.name + f".bak_{ts}")
            shutil.copy2(registry_path, bak)
            print(f"  backup: {bak}")
        write_csv(registry_path, rows, fieldnames)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--registry', required=True)
    ap.add_argument('--patch-dir', required=True)
    ap.add_argument('--reports', required=False)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    reg = Path(args.registry)
    pdir = Path(args.patch_dir)

    merge_by_key(
        reg / 'source_text_references.csv',
        pdir / 'RAKB_stageC_source_text_references_upsert_v1_Apr28_2026.csv',
        ['node_id','source_label','relation'],
        dry_run=args.dry_run,
    )
    merge_by_key(
        reg / 'restoration_candidates.csv',
        pdir / 'RAKB_stageC_restoration_candidates_upsert_v1_Apr28_2026.csv',
        ['candidate_id'],
        dry_run=args.dry_run,
    )
    if args.reports:
        reports = Path(args.reports)
        for f in pdir.glob('RAKB_stageC_*_Apr28_2026.csv'):
            if f.name.startswith('RAKB_stageC_source_text_references') or f.name.startswith('RAKB_stageC_restoration_candidates'):
                continue
            dest = reports / f.name
            print(f"copy report: {f.name} -> {dest}")
            if not args.dry_run:
                reports.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dest)
    print("Done. Run: python scripts/validate_rakb_v0_5.py")

if __name__ == '__main__':
    main()
