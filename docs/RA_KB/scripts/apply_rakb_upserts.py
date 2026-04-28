#!/usr/bin/env python3
"""Apply RAKB v0.5 CSV upsert patches.

Run from the RA repo root, for example:

    python docs/RA_KB/scripts/apply_rakb_upserts.py \
      --registry docs/RA_KB/registry \
      --patch-dir docs/RA_KB/reports/patches/Apr27_v5

This script does not edit Lean/Python/TeX sources. It only merges CSV rows into
RAKB registry tables. Existing rows are updated by stable key; new rows are appended.
Backups are created next to each modified target file.
"""

from __future__ import annotations
import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path


def read_csv(path: Path):
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader), list(reader.fieldnames or [])


def write_csv(path: Path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def upsert_csv(target: Path, patch: Path, key_cols: list[str], dry_run: bool = False):
    target_rows, target_fields = read_csv(target)
    patch_rows, patch_fields = read_csv(patch)

    if not patch_rows:
        print(f"SKIP: no patch rows in {patch}")
        return

    if not target_fields:
        fields = patch_fields
    else:
        # preserve target column order; append patch-only columns if any
        fields = target_fields + [c for c in patch_fields if c not in target_fields]

    index = {tuple(r.get(k, "") for k in key_cols): i for i, r in enumerate(target_rows)}
    added = updated = 0

    for prow in patch_rows:
        key = tuple(prow.get(k, "") for k in key_cols)
        if key in index:
            i = index[key]
            # Only overwrite columns present in the patch.
            for col in patch_fields:
                target_rows[i][col] = prow.get(col, "")
            updated += 1
        else:
            target_rows.append(prow)
            index[key] = len(target_rows) - 1
            added += 1

    print(f"{target}: {added} added, {updated} updated from {patch.name}")
    if dry_run:
        return

    if target.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = target.with_suffix(target.suffix + f".bak_{stamp}")
        shutil.copy2(target, backup)
        print(f"  backup: {backup}")

    write_csv(target, target_rows, fields)


def copy_report(patch_dir: Path, reports_dir: Path, name: str, dry_run: bool = False):
    src = patch_dir / name
    if not src.exists():
        print(f"SKIP: missing report patch {src}")
        return
    dst = reports_dir / name
    print(f"copy report: {src.name} -> {dst}")
    if not dry_run:
        reports_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default="docs/RA_KB/registry")
    ap.add_argument("--patch-dir", required=True)
    ap.add_argument("--reports", default="docs/RA_KB/reports")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    registry = Path(args.registry)
    patch_dir = Path(args.patch_dir)
    reports = Path(args.reports)

    upsert_csv(
        registry / "artifacts.csv",
        patch_dir / "RAKB_artifacts_upsert_v5_D2_build_confirmed_Apr27_2026.csv",
        ["artifact_id"],
        dry_run=args.dry_run,
    )

    upsert_csv(
        registry / "claim_artifact_edges.csv",
        patch_dir / "RAKB_claim_artifact_edges_upsert_v5_D2_build_confirmed_Apr27_2026.csv",
        ["claim_id", "artifact_id", "relation"],
        dry_run=args.dry_run,
    )

    upsert_csv(
        registry / "restoration_candidates.csv",
        patch_dir / "RAKB_restoration_candidates_upsert_v5_D2_build_confirmed_Apr27_2026.csv",
        ["candidate_id"],
        dry_run=args.dry_run,
    )

    copy_report(
        patch_dir,
        reports,
        "RAKB_support_status_upgrades_v5_D2_build_confirmed_Apr27_2026.csv",
        dry_run=args.dry_run,
    )

    print("Done. Run: python docs/RA_KB/scripts/validate_rakb_v0_5.py")


if __name__ == "__main__":
    main()
