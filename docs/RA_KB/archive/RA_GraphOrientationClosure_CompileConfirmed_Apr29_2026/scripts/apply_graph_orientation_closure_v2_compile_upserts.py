#!/usr/bin/env python3
"""
Apply RAKB graph-orientation-closure compile-confirmation upserts.

This script updates:
  registry/artifacts.csv
  registry/claim_artifact_edges.csv

It looks in --packet-root for CSV files whose names contain:
  artifacts
  claim_artifact_edges

It performs an upsert:
  artifacts.csv key: artifact_id if present, else path if present, else first column
  claim_artifact_edges.csv key:
      (claim_id, artifact_id, relation) if present
      else (source_id, target_id, relation) if present
      else all columns in the patch row

It creates timestamped backups before writing.
"""

from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing CSV: {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        rows = [{k: (v if v is not None else "") for k, v in row.items()} for row in reader]
        return list(reader.fieldnames), rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def union_fields(base_fields: list[str], patch_fields: list[str]) -> list[str]:
    out = list(base_fields)
    for f in patch_fields:
        if f not in out:
            out.append(f)
    return out


def choose_key(kind: str, fields: list[str]) -> tuple[str, ...]:
    fs = set(fields)
    if kind == "artifacts":
        for candidate in [("artifact_id",), ("path",), ("filename",)]:
            if set(candidate).issubset(fs):
                return candidate
        return (fields[0],)

    if kind == "claim_artifact_edges":
        for candidate in [
            ("claim_id", "artifact_id", "relation"),
            ("node_id", "artifact_id", "relation"),
            ("source_id", "target_id", "relation"),
            ("src", "dst", "kind"),
        ]:
            if set(candidate).issubset(fs):
                return candidate
        return tuple(fields)

    raise ValueError(f"Unknown kind: {kind}")


def key_for(row: dict[str, str], key_fields: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(row.get(k, "") for k in key_fields)


def find_patch_csv(packet_root: Path, kind: str) -> Path:
    candidates = []
    for p in packet_root.rglob("*.csv"):
        name = p.name.lower()
        if kind == "artifacts":
            if "artifact" in name and "claim_artifact" not in name:
                candidates.append(p)
        elif kind == "claim_artifact_edges":
            if "claim_artifact" in name and "edge" in name:
                candidates.append(p)

    if not candidates:
        raise FileNotFoundError(f"Could not find {kind} upsert CSV under {packet_root}")

    candidates.sort(key=lambda p: (
        0 if "registry_upserts" in str(p).lower() else 1,
        0 if "compile" in p.name.lower() or "confirmed" in p.name.lower() else 1,
        len(str(p)),
    ))
    return candidates[0]


def upsert_csv(
    target_path: Path,
    patch_path: Path,
    kind: str,
    dry_run: bool,
) -> tuple[int, int, tuple[str, ...]]:
    target_fields, target_rows = read_csv(target_path)
    patch_fields, patch_rows = read_csv(patch_path)

    fields = union_fields(target_fields, patch_fields)
    key_fields = choose_key(kind, fields)

    existing: Dict[Tuple[str, ...], dict[str, str]] = {}
    order: list[Tuple[str, ...]] = []

    for row in target_rows:
        k = key_for(row, key_fields)
        existing[k] = {f: row.get(f, "") for f in fields}
        order.append(k)

    added = 0
    updated = 0

    for prow_raw in patch_rows:
        prow = {f: prow_raw.get(f, "") for f in fields}
        k = key_for(prow, key_fields)

        if k in existing:
            merged = dict(existing[k])
            changed = False
            for f in fields:
                val = prow.get(f, "")
                if val != "" and merged.get(f, "") != val:
                    merged[f] = val
                    changed = True
            existing[k] = merged
            if changed:
                updated += 1
        else:
            existing[k] = prow
            order.append(k)
            added += 1

    if not dry_run:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = target_path.with_name(target_path.name + f".bak_{timestamp}")
        shutil.copy2(target_path, backup)
        out_rows = [existing[k] for k in order]
        write_csv(target_path, fields, out_rows)
        print(f"  backup: {backup}")

    return added, updated, key_fields


def copy_report_files(packet_root: Path, reports_dir: Path, dry_run: bool) -> int:
    report_dir_candidates = [p for p in packet_root.rglob("reports") if p.is_dir()]
    copied = 0
    if not report_dir_candidates:
        return 0
    reports_dir.mkdir(parents=True, exist_ok=True)

    for rdir in report_dir_candidates:
        for p in rdir.iterdir():
            if p.is_file() and p.suffix.lower() in {".md", ".csv", ".json", ".txt"}:
                dest = reports_dir / p.name
                print(f"copy report: {p.name} -> {dest}")
                copied += 1
                if not dry_run:
                    shutil.copy2(p, dest)
    return copied


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True, type=Path, help="Path to docs/RA_KB/registry")
    ap.add_argument("--reports", required=False, type=Path, help="Path to docs/RA_KB/reports")
    ap.add_argument("--packet-root", required=True, type=Path, help="Unzipped packet root")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    registry = args.registry
    packet_root = args.packet_root

    targets = [
        ("artifacts", registry / "artifacts.csv"),
        ("claim_artifact_edges", registry / "claim_artifact_edges.csv"),
    ]

    for kind, target in targets:
        patch = find_patch_csv(packet_root, kind)
        added, updated, key_fields = upsert_csv(target, patch, kind, args.dry_run)
        print(f"registry/{target.name}: {added} added, {updated} updated from {patch.name}")
        print(f"  key fields: {', '.join(key_fields)}")

    if args.reports is not None:
        copy_report_files(packet_root, args.reports, args.dry_run)

    if args.dry_run:
        print("Dry run complete. No files were changed.")
    else:
        print("Done. Run: python scripts/validate_rakb_v0_5.py")


if __name__ == "__main__":
    main()
