#!/usr/bin/env python3
"""
Apply RAKB framework/growth/ledger issue upserts.

Run from docs/RA_KB, for example:

python scripts/apply_rakb_framework_upserts.py \
  --registry ./registry \
  --reports ./reports \
  --packet-root /path/to/RAKB_Framework_Growth_Ledger_Update_Apr29_2026 \
  --dry-run

Then rerun without --dry-run and validate:

python scripts/validate_rakb_v0_5.py
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import os
from pathlib import Path
import shutil
import sys

try:
    import yaml
except Exception as e:
    raise SystemExit("This script requires PyYAML. Install with: pip install pyyaml") from e


ISSUES_FILE = "RAKB_framework_issues_upsert_v1_Apr29_2026.yaml"
ARTIFACTS_FILE = "RAKB_framework_artifacts_upsert_v1_Apr29_2026.csv"
EDGES_FILE = "RAKB_framework_claim_artifact_edges_upsert_v1_Apr29_2026.csv"


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path: Path) -> Path:
    b = path.with_name(path.name + ".bak_" + timestamp())
    shutil.copy2(path, b)
    return b


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        return list(r.fieldnames or []), list(r)


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def upsert_rows(existing: list[dict[str,str]], incoming: list[dict[str,str]], key_fields: list[str]) -> tuple[list[dict[str,str]], int, int]:
    index = {tuple(r.get(k,"") for k in key_fields): i for i,r in enumerate(existing)}
    added = updated = 0
    out = list(existing)
    for row in incoming:
        key = tuple(row.get(k,"") for k in key_fields)
        if key in index:
            out[index[key]].update(row)
            updated += 1
        else:
            index[key] = len(out)
            out.append(row)
            added += 1
    return out, added, updated


def load_node_names(registry: Path) -> dict[str,str]:
    names: dict[str,str] = {}
    for fname, topkey in [
        ("claims.yaml","claims"),
        ("issues.yaml","issues"),
        ("targets.yaml","targets"),
        ("framing.yaml","framing"),
    ]:
        p = registry / fname
        if not p.exists():
            continue
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        for node in data.get(topkey, []) or []:
            if isinstance(node, dict) and "id" in node:
                names[node["id"]] = node.get("name", node["id"])
    return names


def node_type(node_id: str) -> str:
    if node_id.startswith("RA-OPEN") or node_id.startswith("RA-KERNEL-004") or node_id.startswith("RA-KERNEL-005"):
        return "issue"
    if node_id.startswith("RA-PRED"):
        return "target"
    if node_id.startswith("RA-NONTARGET"):
        return "framing"
    return "claim"


def apply_issues(registry: Path, packet: Path, dry: bool) -> None:
    issues_path = registry / "issues.yaml"
    upsert_path = packet / "registry_upserts_v1" / ISSUES_FILE
    data = yaml.safe_load(issues_path.read_text(encoding="utf-8")) if issues_path.exists() else {"issues": []}
    incoming = yaml.safe_load(upsert_path.read_text(encoding="utf-8")) or {}
    incoming_issues = incoming.get("issues_upsert", [])
    existing = data.get("issues", []) or []
    idx = {x.get("id"): i for i, x in enumerate(existing) if isinstance(x, dict)}
    added = updated = 0
    for issue in incoming_issues:
        iid = issue["id"]
        if iid in idx:
            existing[idx[iid]].update(issue)
            updated += 1
        else:
            existing.append(issue)
            idx[iid] = len(existing)-1
            added += 1
    data["issues"] = existing
    print(f"registry/issues.yaml: {added} added, {updated} updated from {ISSUES_FILE}")
    if not dry:
        if issues_path.exists():
            print(f"  backup: {backup(issues_path)}")
        issues_path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")


def apply_dependency_edges(registry: Path, packet: Path, dry: bool) -> None:
    upsert_path = packet / "registry_upserts_v1" / ISSUES_FILE
    incoming = yaml.safe_load(upsert_path.read_text(encoding="utf-8")) or {}
    incoming_issues = incoming.get("issues_upsert", [])
    names = load_node_names(registry)
    # Include incoming names before generating edges.
    for issue in incoming_issues:
        names[issue["id"]] = issue.get("name", issue["id"])

    edge_rows = []
    for issue in incoming_issues:
        dst = issue["id"]
        for src in issue.get("proof_dependencies", []) or []:
            edge_rows.append({
                "src": src,
                "dst": dst,
                "kind": "proof_dependency",
                "src_node_type": node_type(src),
                "dst_node_type": "issue",
                "src_name": names.get(src, src),
                "dst_name": names.get(dst, dst),
            })

    for fname in ["issue_edges.csv", "all_dependency_edges.csv"]:
        path = registry / fname
        fields, rows = read_csv(path)
        if not fields:
            fields = ["src","dst","kind","src_node_type","dst_node_type","src_name","dst_name"]
        rows2, added, updated = upsert_rows(rows, edge_rows, ["src","dst","kind"])
        print(f"registry/{fname}: {added} added, {updated} updated dependency edges")
        if not dry:
            if path.exists():
                print(f"  backup: {backup(path)}")
            write_csv(path, fields, rows2)


def apply_csv_upsert(registry: Path, packet: Path, dry: bool, target_file: str, upsert_file: str, key_fields: list[str]) -> None:
    target = registry / target_file
    patch = packet / "registry_upserts_v1" / upsert_file
    fields, rows = read_csv(target)
    patch_fields, incoming = read_csv(patch)
    if not fields:
        fields = patch_fields
    # Preserve target field order; append new fields if needed.
    for f in patch_fields:
        if f not in fields:
            fields.append(f)
    rows2, added, updated = upsert_rows(rows, incoming, key_fields)
    print(f"registry/{target_file}: {added} added, {updated} updated from {upsert_file}")
    if not dry:
        if target.exists():
            print(f"  backup: {backup(target)}")
        write_csv(target, fields, rows2)


def copy_packet_reports(packet: Path, reports: Path, dry: bool) -> None:
    dest = reports / "framework_growth_ledger_Apr29_2026"
    items = ["reports", "data_summaries", "formalization_notes", "source_archives", "raw_simulation_outputs_Apr29_2026"]
    print(f"copy packet reports/data -> {dest}")
    if dry:
        return
    if dest.exists():
        # Do not delete; merge-overwrite files.
        pass
    dest.mkdir(parents=True, exist_ok=True)
    for item in items:
        src = packet / item
        if src.exists():
            d = dest / item if item != "reports" else dest
            if item == "reports":
                d.mkdir(parents=True, exist_ok=True)
                for file in src.iterdir():
                    if file.is_file():
                        shutil.copy2(file, d / file.name)
            else:
                if d.exists():
                    shutil.rmtree(d)
                shutil.copytree(src, d)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--reports", required=True)
    ap.add_argument("--packet-root", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    registry = Path(args.registry)
    reports = Path(args.reports)
    packet = Path(args.packet_root)

    if not (packet / "registry_upserts_v1" / ISSUES_FILE).exists():
        raise SystemExit(f"Could not find packet upsert file under {packet}")

    apply_issues(registry, packet, args.dry_run)
    apply_dependency_edges(registry, packet, args.dry_run)
    apply_csv_upsert(registry, packet, args.dry_run, "artifacts.csv", ARTIFACTS_FILE, ["artifact_id"])
    apply_csv_upsert(registry, packet, args.dry_run, "claim_artifact_edges.csv", EDGES_FILE, ["claim_id","artifact_id","relation"])
    copy_packet_reports(packet, reports, args.dry_run)
    print("Done. Run: python scripts/validate_rakb_v0_5.py")


if __name__ == "__main__":
    main()
