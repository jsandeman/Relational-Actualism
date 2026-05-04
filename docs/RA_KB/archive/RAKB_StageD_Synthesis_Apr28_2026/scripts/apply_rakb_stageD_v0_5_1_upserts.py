#!/usr/bin/env python3
from __future__ import annotations
import argparse, shutil
from pathlib import Path
from datetime import datetime
import pandas as pd

ART = 'RAKB_stageD_artifacts_upsert_v0_5_1_Apr28_2026.csv'
EDGE = 'RAKB_stageD_claim_artifact_edges_upsert_v0_5_1_Apr28_2026.csv'

def upsert(df, patch, keys):
    df = df.copy()
    patch = patch.copy()
    for col in patch.columns:
        if col not in df.columns:
            df[col] = ''
    for col in df.columns:
        if col not in patch.columns:
            patch[col] = ''
    df = df[df.columns]
    patch = patch[df.columns]
    keyset = set(tuple(str(row[k]) for k in keys) for _, row in patch.iterrows())
    keep = []
    for _, row in df.iterrows():
        tup = tuple(str(row[k]) for k in keys)
        keep.append(tup not in keyset)
    out = pd.concat([df.loc[keep], patch], ignore_index=True)
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--registry', required=True)
    ap.add_argument('--patch-dir', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    reg = Path(args.registry)
    pdir = Path(args.patch_dir)
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    todo = [
        ('artifacts.csv', ART, ['artifact_id']),
        ('claim_artifact_edges.csv', EDGE, ['claim_id','artifact_id','relation']),
    ]
    for target, patch_name, keys in todo:
        target_path = reg/target
        patch_path = pdir/patch_name
        if not patch_path.exists():
            print(f'skip missing patch: {patch_path}')
            continue
        df = pd.read_csv(target_path)
        patch = pd.read_csv(patch_path)
        before = len(df)
        out = upsert(df, patch, keys)
        added_or_updated = len(patch)
        print(f'{target}: upsert {added_or_updated} rows from {patch_name}; before={before}, after={len(out)}')
        if not args.dry_run:
            backup = target_path.with_suffix(target_path.suffix + f'.bak_{stamp}')
            shutil.copy2(target_path, backup)
            out.to_csv(target_path, index=False)
            print(f'  backup: {backup}')
    print('Done. Run: python scripts/validate_rakb_v0_5.py')

if __name__ == '__main__':
    main()
