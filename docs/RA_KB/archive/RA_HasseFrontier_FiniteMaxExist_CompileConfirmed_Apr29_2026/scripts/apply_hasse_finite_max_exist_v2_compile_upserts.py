#!/usr/bin/env python3
import argparse, csv, shutil
from pathlib import Path
from datetime import datetime

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def upsert(target, patch, key, dry):
    rows = read_csv(target) if target.exists() else []
    fields = list(rows[0].keys()) if rows else list(read_csv(patch)[0].keys())
    incoming = read_csv(patch)
    idx = {r[key]: i for i,r in enumerate(rows)}
    add=upd=0
    for r in incoming:
        for f in fields:
            r.setdefault(f,'')
        if r[key] in idx:
            rows[idx[r[key]]] = {f:r.get(f,'') for f in fields}; upd += 1
        else:
            rows.append({f:r.get(f,'') for f in fields}); add += 1
    print(f"{target}: {add} added, {upd} updated from {patch.name}")
    if not dry:
        if target.exists(): shutil.copy2(target, target.with_suffix(target.suffix + '.bak_' + datetime.now().strftime('%Y%m%d_%H%M%S')))
        write_csv(target, rows, fields)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--registry', required=True)
    ap.add_argument('--reports', required=True)
    ap.add_argument('--packet-root', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args=ap.parse_args()
    root=Path(args.packet_root); reg=Path(args.registry); reports=Path(args.reports)
    patch=root/'registry_upserts_hasse_finite_max_exist_v2'
    upsert(reg/'artifacts.csv', patch/'RAKB_hasse_finite_max_exist_v2_artifacts_upsert_compile_confirmed_Apr29_2026.csv', 'artifact_id', args.dry_run)
    upsert(reg/'claim_artifact_edges.csv', patch/'RAKB_hasse_finite_max_exist_v2_claim_artifact_edges_upsert_compile_confirmed_Apr29_2026.csv', 'artifact_id', args.dry_run)
    if not args.dry_run:
        out=reports/'selector_closure_Apr29_2026'; out.mkdir(parents=True, exist_ok=True)
        for p in (root/'reports').glob('*.md'):
            shutil.copy2(p, out/p.name)
    print('Done. Run: python scripts/validate_rakb_v0_5.py')
if __name__ == '__main__': main()
