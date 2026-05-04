#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import shutil
from datetime import datetime
from pathlib import Path


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"No CSV header found in {path}")
        return list(reader.fieldnames), [
            {k: (v if v is not None else "") for k, v in row.items()}
            for row in reader
        ]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def merged_fields(base: list[str], patch: list[str]) -> list[str]:
    out = list(base)
    for field in patch:
        if field not in out:
            out.append(field)
    return out


def find_upsert_csv(packet_root: Path, target: str) -> Path:
    csvs = list(packet_root.rglob("*.csv"))

    if target == "artifacts":
        matches = [
            p for p in csvs
            if "artifacts" in p.name.lower()
            and "claim_artifact" not in p.name.lower()
        ]
    elif target == "claim_artifact_edges":
        matches = [
            p for p in csvs
            if "claim_artifact" in p.name.lower()
            and "edge" in p.name.lower()
        ]
    else:
        raise ValueError(f"Unknown target: {target}")

    if not matches:
        raise FileNotFoundError(
            f"Could not find {target} upsert CSV under {packet_root}"
        )

    matches.sort(key=lambda p: (
        0 if "registry_upserts" in str(p).lower() else 1,
        0 if "compile" in p.name.lower() or "confirmed" in p.name.lower() else 1,
        len(str(p)),
    ))
    return matches[0]


def choose_key(fields: list[str], target: str) -> tuple[str, ...]:
    available = set(fields)

    if target == "artifacts":
        candidates = [
            ("artifact_id",),
            ("id",),
            ("path",),
            ("filename",),
        ]
    elif target == "claim_artifact_edges":
        candidates = [
            ("claim_id", "artifact_id", "relation"),
            ("node_id", "artifact_id", "relation"),
            ("result_id", "artifact_id", "relation"),
            ("src", "dst", "kind"),
            ("source", "target", "kind"),
        ]
    else:
        raise ValueError(f"Unknown target: {target}")

    for candidate in candidates:
        if set(candidate).issubset(available):
            return candidate

    raise ValueError(
        f"Could not infer key fields for {target}. Available fields: {fields}"
    )


def row_key(row: dict[str, str], key_fields: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(row.get(field, "") for field in key_fields)


def upsert_table(
    *,
    registry_csv: Path,
    patch_csv: Path,
    target: str,
    dry_run: bool,
) -> tuple[int, int, tuple[str, ...]]:
    base_fields, base_rows = read_csv(registry_csv)
    patch_fields, patch_rows = read_csv(patch_csv)

    fields = merged_fields(base_fields, patch_fields)
    key_fields = choose_key(fields, target)

    rows_by_key: dict[tuple[str, ...], dict[str, str]] = {}
    order: list[tuple[str, ...]] = []

    for row in base_rows:
        normalized = {field: row.get(field, "") for field in fields}
        key = row_key(normalized, key_fields)
        rows_by_key[key] = normalized
        order.append(key)

    added = 0
    updated = 0

    for patch_row_raw in patch_rows:
        patch_row = {field: patch_row_raw.get(field, "") for field in fields}
        key = row_key(patch_row, key_fields)

        if key in rows_by_key:
            existing = rows_by_key[key]
            changed = False

            for field in fields:
                new_value = patch_row.get(field, "")
                if new_value != "" and existing.get(field, "") != new_value:
                    existing[field] = new_value
                    changed = True

            if changed:
                updated += 1
        else:
            rows_by_key[key] = patch_row
            order.append(key)
            added += 1

    if not dry_run:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = registry_csv.with_name(f"{registry_csv.name}.bak_{stamp}")
        shutil.copy2(registry_csv, backup_path)
        write_csv(registry_csv, fields, [rows_by_key[key] for key in order])
        print(f"backup: {backup_path}")

    return added, updated, key_fields


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Apply GraphOrientationClosure compile-confirmation RAKB upserts."
    )
    parser.add_argument(
        "--registry",
        required=True,
        type=Path,
        help="Path to docs/RA_KB/registry",
    )
    parser.add_argument(
        "--packet-root",
        required=True,
        type=Path,
        help="Path to unzipped RA_GraphOrientationClosure_CompileConfirmed packet",
    )
    parser.add_argument(
        "--reports",
        required=False,
        type=Path,
        help="Optional path to docs/RA_KB/reports",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report changes without writing files",
    )

    args = parser.parse_args()

    registry = args.registry.resolve()
    packet_root = args.packet_root.resolve()

    targets = {
        "artifacts": registry / "artifacts.csv",
        "claim_artifact_edges": registry / "claim_artifact_edges.csv",
    }

    for target, registry_csv in targets.items():
        patch_csv = find_upsert_csv(packet_root, target)
        added, updated, key_fields = upsert_table(
            registry_csv=registry_csv,
            patch_csv=patch_csv,
            target=target,
            dry_run=args.dry_run,
        )

        print(
            f"registry/{registry_csv.name}: "
            f"{added} added, {updated} updated "
            f"from {patch_csv.name}"
        )
        print(f"key fields: {', '.join(key_fields)}")

    if args.reports is not None:
        reports_dir = args.reports.resolve()
        reports_dir.mkdir(parents=True, exist_ok=True)

        for report_dir in packet_root.rglob("reports"):
            if not report_dir.is_dir():
                continue

            for report in report_dir.iterdir():
                if report.is_file() and report.suffix.lower() in {
                    ".md", ".csv", ".json", ".txt"
                }:
                    dest = reports_dir / report.name
                    print(f"copy report: {report} -> {dest}")
                    if not args.dry_run:
                        shutil.copy2(report, dest)

    if args.dry_run:
        print("Dry run complete. No files changed.")
    else:
        print("Done. Run: python scripts/validate_rakb_v0_5.py")


if __name__ == "__main__":
    main()