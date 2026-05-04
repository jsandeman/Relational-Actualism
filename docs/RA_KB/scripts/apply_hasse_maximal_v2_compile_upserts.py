#!/usr/bin/env python3
"""Apply Hasse Frontier Maximal v2 compile-confirmation upserts to RAKB v0.5 registry."""
from __future__ import annotations
import argparse, csv, shutil
from datetime import datetime
from pathlib import Path

def read_csv(path: Path):
    if not path.exists(): return [], []
    with path.open(newline='', encoding='utf-8') as f:
        r=csv.DictReader(f); return list(r.fieldnames or []), list(r)

def write_csv(path: Path, fields, rows, dry_run: bool):
    if dry_run: return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
        shutil.copy2(path, path.with_suffix(path.suffix+f'.bak_{stamp}'))
    with path.open('w', newline='', encoding='utf-8') as f:
        w=csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for row in rows: w.writerow({k: row.get(k,'') for k in fields})

def upsert_csv(target: Path, patch: Path, keys, dry_run: bool):
    tf,tr=read_csv(target); pf,pr=read_csv(patch)
    if not pf:
        print(f'skip: {patch} missing/empty'); return
    fields=tf[:] if tf else pf[:]
    for field in pf:
        if field not in fields: fields.append(field)
    idx={tuple(row.get(k,'') for k in keys):i for i,row in enumerate(tr)}
    added=updated=0
    for row in pr:
        key=tuple(row.get(k,'') for k in keys)
        if key in idx:
            tr[idx[key]].update(row); updated += 1
        else:
            tr.append(row); idx[key]=len(tr)-1; added += 1
    print(f'{target}: {added} added, {updated} updated from {patch.name}')
    write_csv(target, fields, tr, dry_run)

def copy_report(src: Path, dst: Path, dry_run: bool):
    print(f'copy report: {src.name} -> {dst/src.name}')
    if not dry_run:
        dst.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst/src.name)

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--registry', required=True, type=Path)
    p.add_argument('--reports', required=True, type=Path)
    p.add_argument('--packet-root', required=True, type=Path)
    p.add_argument('--dry-run', action='store_true')
    a=p.parse_args()
    pd=a.packet_root/'registry_upserts_hasse_maximal_v2'
    upsert_csv(a.registry/'artifacts.csv', pd/'RAKB_hasse_maximal_v2_artifacts_upsert_compile_confirmed_Apr29_2026.csv', ['artifact_id'], a.dry_run)
    upsert_csv(a.registry/'claim_artifact_edges.csv', pd/'RAKB_hasse_maximal_v2_claim_artifact_edges_upsert_compile_confirmed_Apr29_2026.csv', ['claim_id','artifact_id','relation','source_span'], a.dry_run)
    copy_report(a.packet_root/'reports/RA_HasseFrontier_Maximal_CompileConfirmed_Report_Apr29_2026.md', a.reports/'selector_closure_Apr29_2026', a.dry_run)
    print('Done. Run: python scripts/validate_rakb_v0_5.py')
if __name__ == '__main__': main()
