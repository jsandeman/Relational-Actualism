#!/usr/bin/env python3
"""Apply RAKB charge/ledger upserts.

Run from docs/RA_KB, for example:

python scripts/apply_rakb_charge_upserts.py \
  --registry ./registry \
  --patch-dir ./reports/patches/Apr28_charge_v1 \
  --reports ./reports \
  --dry-run

Then rerun without --dry-run and validate:

python scripts/validate_rakb_v0_5.py
"""
from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path: Path) -> Path:
    b = path.with_name(path.name + ".bak_" + stamp())
    shutil.copy2(path, b)
    return b


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: dict, dry_run: bool) -> Path | None:
    if dry_run:
        return None
    b = backup(path) if path.exists() else None
    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, width=100)
    return b


def upsert_list_by_id(items: List[dict], incoming: Iterable[dict]) -> Tuple[int, int, List[dict]]:
    index = {item.get("id"): i for i, item in enumerate(items)}
    added = updated = 0
    for inc in incoming:
        nid = inc.get("id")
        if not nid:
            raise ValueError(f"incoming item lacks id: {inc}")
        if nid in index:
            # Merge fields so hand-curated extras survive unless explicitly overwritten.
            merged = dict(items[index[nid]])
            merged.update(inc)
            items[index[nid]] = merged
            updated += 1
        else:
            index[nid] = len(items)
            items.append(dict(inc))
            added += 1
    return added, updated, items


def read_csv(path: Path) -> Tuple[List[str], List[dict]]:
    if not path.exists():
        return [], []
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fieldnames: List[str], rows: List[dict], dry_run: bool) -> Path | None:
    if dry_run:
        return None
    b = backup(path) if path.exists() else None
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})
    return b


def upsert_csv_file(target: Path, patch: Path, key_cols: List[str], dry_run: bool) -> Tuple[int, int, Path | None]:
    p_fields, p_rows = read_csv(patch)
    if not p_fields:
        raise ValueError(f"empty or missing patch csv: {patch}")
    t_fields, t_rows = read_csv(target)
    if not t_fields:
        t_fields = p_fields
    # Preserve target order, append any new patch columns if needed.
    fieldnames = list(t_fields)
    for col in p_fields:
        if col not in fieldnames:
            fieldnames.append(col)
    for col in key_cols:
        if col not in fieldnames:
            raise ValueError(f"key column {col!r} not in {target} / {patch}")

    def key(row: dict) -> tuple:
        return tuple(row.get(c, "") for c in key_cols)

    index: Dict[tuple, int] = {key(row): i for i, row in enumerate(t_rows)}
    added = updated = 0
    for prow in p_rows:
        k = key(prow)
        if k in index:
            merged = dict(t_rows[index[k]])
            merged.update(prow)
            t_rows[index[k]] = merged
            updated += 1
        else:
            t_rows.append(dict(prow))
            index[k] = len(t_rows) - 1
            added += 1
    b = write_csv(target, fieldnames, t_rows, dry_run)
    return added, updated, b


def find_one(patch_dir: Path, pattern: str) -> Path | None:
    matches = sorted(patch_dir.glob(pattern))
    return matches[0] if matches else None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True, type=Path)
    ap.add_argument("--patch-dir", required=True, type=Path)
    ap.add_argument("--reports", required=False, type=Path, default=None)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    registry: Path = args.registry
    patch_dir: Path = args.patch_dir
    reports: Path | None = args.reports

    yaml_patch = find_one(patch_dir, "RAKB_charge_claim_issue_upsert*_*.yaml") or find_one(patch_dir, "RAKB_charge_claim_issue_upsert*.yaml")
    if not yaml_patch:
        raise SystemExit(f"No charge claim/issue YAML upsert found in {patch_dir}")
    patch_data = load_yaml(yaml_patch)

    # claims.yaml
    claims_path = registry / "claims.yaml"
    claims_data = load_yaml(claims_path)
    claims = claims_data.get("claims", [])
    added, updated, claims = upsert_list_by_id(claims, patch_data.get("claims_upsert", []))
    claims_data["claims"] = claims
    b = write_yaml(claims_path, claims_data, args.dry_run)
    print(f"registry/claims.yaml: {added} added, {updated} updated from {yaml_patch.name}" + (f"\n  backup: {b}" if b else ""))

    # issues.yaml
    issues_path = registry / "issues.yaml"
    issues_data = load_yaml(issues_path)
    issues = issues_data.get("issues", [])
    added, updated, issues = upsert_list_by_id(issues, patch_data.get("issues_upsert", []))
    issues_data["issues"] = issues
    b = write_yaml(issues_path, issues_data, args.dry_run)
    print(f"registry/issues.yaml: {added} added, {updated} updated from {yaml_patch.name}" + (f"\n  backup: {b}" if b else ""))

    jobs = [
        ("RAKB_charge_claim_edges_upsert*.csv", registry / "claim_edges.csv", ["src", "dst", "kind"]),
        ("RAKB_charge_issue_edges_upsert*.csv", registry / "issue_edges.csv", ["src", "dst", "kind"]),
        ("RAKB_charge_all_dependency_edges_upsert*.csv", registry / "all_dependency_edges.csv", ["src", "dst", "kind"]),
        ("RAKB_charge_artifacts_upsert*.csv", registry / "artifacts.csv", ["artifact_id"]),
        ("RAKB_charge_claim_artifact_edges_upsert*.csv", registry / "claim_artifact_edges.csv", ["claim_id", "artifact_id", "relation"]),
        ("RAKB_charge_source_text_references_upsert*.csv", registry / "source_text_references.csv", ["node_id", "source_label", "relation"]),
    ]
    for pattern, target, keys in jobs:
        patch = find_one(patch_dir, pattern)
        if not patch:
            continue
        added, updated, b = upsert_csv_file(target, patch, keys, args.dry_run)
        rel_target = f"registry/{target.name}"
        print(f"{rel_target}: {added} added, {updated} updated from {patch.name}" + (f"\n  backup: {b}" if b else ""))

    # Copy report files if present in patch-dir/report payload.
    if reports:
        reports.mkdir(parents=True, exist_ok=True)
        for md in sorted(patch_dir.glob("RAKB_Ledger_Rule_Analysis_Apr28_2026.md")):
            dest = reports / md.name
            if not args.dry_run:
                shutil.copy2(md, dest)
            print(f"copy report: {md.name} -> reports/{dest.name}")

    print("Done. Run: python scripts/validate_rakb_v0_5.py")


if __name__ == "__main__":
    main()
