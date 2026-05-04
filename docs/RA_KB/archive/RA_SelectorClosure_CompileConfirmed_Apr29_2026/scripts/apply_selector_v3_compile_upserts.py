#!/usr/bin/env python3
"""Apply Selector Closure v3 compile-confirmed upserts to RAKB v0.5 registry."""
from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]], dry_run: bool) -> None:
    if dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(path, path.with_suffix(path.suffix + f".bak_{stamp}"))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def upsert_csv(target: Path, patch: Path, key_fields: list[str], dry_run: bool) -> tuple[int, int]:
    target_fields, target_rows = read_csv(target)
    patch_fields, patch_rows = read_csv(patch)
    if not patch_fields:
        print(f"skip: {patch} not found or empty")
        return 0, 0
    fieldnames = target_fields[:] if target_fields else patch_fields[:]
    for f in patch_fields:
        if f not in fieldnames:
            fieldnames.append(f)
    index = {tuple(row.get(k, "") for k in key_fields): i for i, row in enumerate(target_rows)}
    added = updated = 0
    for prow in patch_rows:
        key = tuple(prow.get(k, "") for k in key_fields)
        if key in index:
            target_rows[index[key]].update(prow)
            updated += 1
        else:
            target_rows.append(prow)
            index[key] = len(target_rows) - 1
            added += 1
    print(f"{target}: {added} added, {updated} updated from {patch.name}")
    write_csv(target, fieldnames, target_rows, dry_run)
    return added, updated


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True, type=Path)
    ap.add_argument("--reports", required=True, type=Path)
    ap.add_argument("--packet-root", required=True, type=Path)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    patch_dir = args.packet_root / "registry_upserts_selector_v3"
    upsert_csv(
        args.registry / "artifacts.csv",
        patch_dir / "RAKB_selector_v3_artifacts_upsert_compile_confirmed_Apr29_2026.csv",
        ["artifact_id"],
        args.dry_run,
    )
    upsert_csv(
        args.registry / "claim_artifact_edges.csv",
        patch_dir / "RAKB_selector_v3_claim_artifact_edges_upsert_compile_confirmed_Apr29_2026.csv",
        ["claim_id", "artifact_id", "relation", "source_span"],
        args.dry_run,
    )

    dest = args.reports / "selector_closure_Apr29_2026"
    src = args.packet_root / "reports" / "RA_SelectorClosure_CompileConfirmed_Report_Apr29_2026.md"
    print(f"copy report: {src.name} -> {dest / src.name}")
    if not args.dry_run:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest / src.name)
    print("Done. Run: python scripts/validate_rakb_v0_5.py")


if __name__ == "__main__":
    main()
