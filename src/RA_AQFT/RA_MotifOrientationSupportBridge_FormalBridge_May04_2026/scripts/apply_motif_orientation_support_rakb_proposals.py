#!/usr/bin/env python3
"""Apply proposed RAKB upserts for RA_MotifOrientationSupportBridge.

This script targets the active YAML/CSV schema used by the current RAKB:
claims.yaml, framing.yaml, artifacts.csv, and claim_artifact_edges.csv.

The proposal status is intentionally pending-compile. After local Lean
compilation, update `auxiliary_support_status` and `legacy_support_status` as
appropriate before or after applying.
"""
from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

CLAIMS_FILE = "RAKB_motif_orientation_support_claims_proposed_May04_2026.yaml"
FRAMING_FILE = "RAKB_motif_orientation_support_framing_proposed_May04_2026.yaml"
ARTIFACTS_FILE = "RAKB_motif_orientation_support_artifacts_proposed_May04_2026.csv"
EDGES_FILE = "RAKB_motif_orientation_support_claim_artifact_edges_proposed_May04_2026.csv"


def load_yaml_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return []
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {path}")
    return data


def write_yaml_list(path: Path, items: list[dict[str, Any]]) -> None:
    path.write_text(yaml.safe_dump(items, sort_keys=False, allow_unicode=True), encoding="utf-8")


def upsert_yaml_items(target: Path, incoming: list[dict[str, Any]]) -> tuple[int, int]:
    current = load_yaml_list(target)
    by_id = {item.get("id"): i for i, item in enumerate(current) if isinstance(item, dict) and item.get("id")}
    inserts = updates = 0
    for item in incoming:
        item_id = item.get("id")
        if not item_id:
            raise ValueError(f"Incoming YAML item lacks id: {item}")
        if item_id in by_id:
            current[by_id[item_id]] = item
            updates += 1
        else:
            current.append(item)
            by_id[item_id] = len(current) - 1
            inserts += 1
    write_yaml_list(target, current)
    return inserts, updates


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def upsert_csv(target: Path, incoming_path: Path, key_fields: list[str]) -> tuple[int, int]:
    incoming = read_csv(incoming_path)
    if not incoming:
        return 0, 0
    fieldnames = list(incoming[0].keys())
    current = read_csv(target)
    if current:
        # Preserve existing columns first, append new columns if any.
        existing_fields = list(current[0].keys())
        fieldnames = existing_fields + [f for f in fieldnames if f not in existing_fields]
    key_to_idx = {tuple(row.get(k, "") for k in key_fields): i for i, row in enumerate(current)}
    inserts = updates = 0
    for row in incoming:
        key = tuple(row.get(k, "") for k in key_fields)
        if key in key_to_idx:
            merged = dict(current[key_to_idx[key]])
            merged.update(row)
            current[key_to_idx[key]] = merged
            updates += 1
        else:
            current.append(row)
            key_to_idx[key] = len(current) - 1
            inserts += 1
    write_csv(target, current, fieldnames)
    return inserts, updates


def backup_files(registry: Path, files: list[str]) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = registry / ".backups" / f"motif_orientation_support_bridge_{stamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    for name in files:
        src = registry / name
        if src.exists():
            shutil.copy2(src, backup_dir / name)
    return backup_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, type=Path)
    parser.add_argument("--packet-root", required=True, type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-backup", action="store_true")
    args = parser.parse_args()

    registry = args.registry.resolve()
    proposals = args.packet_root.resolve() / "registry_proposals"
    if not registry.exists():
        raise FileNotFoundError(registry)
    if not proposals.exists():
        raise FileNotFoundError(proposals)

    print("RA motif orientation support bridge RAKB proposals")
    print(f"registry: {registry}")
    print(f"packet:   {args.packet_root.resolve()}")
    print(f"dry_run:  {args.dry_run}")

    claims = load_yaml_list(proposals / CLAIMS_FILE)
    framing = load_yaml_list(proposals / FRAMING_FILE)
    artifacts = read_csv(proposals / ARTIFACTS_FILE)
    edges = read_csv(proposals / EDGES_FILE)

    print(f"claims incoming:   {len(claims)}")
    print(f"framing incoming:  {len(framing)}")
    print(f"artifacts incoming:{len(artifacts)}")
    print(f"edges incoming:    {len(edges)}")

    if args.dry_run:
        print("Dry run only; no files changed.")
        return

    if not args.no_backup:
        backup_dir = backup_files(registry, ["claims.yaml", "framing.yaml", "artifacts.csv", "claim_artifact_edges.csv"])
        print(f"Backup: {backup_dir}")

    ci, cu = upsert_yaml_items(registry / "claims.yaml", claims)
    fi, fu = upsert_yaml_items(registry / "framing.yaml", framing)
    ai, au = upsert_csv(registry / "artifacts.csv", proposals / ARTIFACTS_FILE, ["artifact_id"])
    ei, eu = upsert_csv(registry / "claim_artifact_edges.csv", proposals / EDGES_FILE, ["claim_id", "artifact_id", "edge_type"])

    print(f"claims.yaml: {ci} insert(s), {cu} update(s)")
    print(f"framing.yaml: {fi} insert(s), {fu} update(s)")
    print(f"artifacts.csv: {ai} insert(s), {au} update(s)")
    print(f"claim_artifact_edges.csv: {ei} insert(s), {eu} update(s)")


if __name__ == "__main__":
    main()
