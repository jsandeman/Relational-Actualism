#!/usr/bin/env python3
"""
Apply RAKB methodological guardrail upserts for RA's target discipline.

Purpose
-------
This script records the methodological updates discussed after the
RA_MotifCommitProtocol / causal-DAG simulator work:

  1. RA targets Nature, not QM, GR, or distributed consensus formalisms.
  2. QM/GR are correspondence benchmarks for empirical content, not ontological
     or mathematical targets to be copied.
  3. Motif-commit simulations should be described in RA-native vocabulary.

Default target filenames under --registry:
  claims.csv
  artifacts.csv
  claim_artifact_edges.csv

The script performs idempotent CSV upserts. Existing rows are matched by:
  claims: claim_id
  artifacts: artifact_id
  claim_artifact_edges: claim_id + artifact_id + relation + source_span

It also writes a methodology report under:
  --reports/method_guardrails_May04_2026/

Usage
-----
  python apply_ra_method_guardrails_upsert.py \
    --registry /path/to/RAKB/registry \
    --reports /path/to/RAKB/reports

Preview only:
  python apply_ra_method_guardrails_upsert.py \
    --registry /path/to/RAKB/registry \
    --reports /path/to/RAKB/reports \
    --dry-run

Optional backup:
  By default, existing CSV files are copied to:
    <registry>/.backups/ra_method_guardrails_May04_2026_<timestamp>/
  Use --no-backup to skip this.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

DATE_LABEL = "May04_2026"
REPORT_DIRNAME = f"method_guardrails_{DATE_LABEL}"
REPORT_FILENAME = f"RA_MethodGuardrails_NatureAsTarget_Report_{DATE_LABEL}.md"

CLAIMS = [
    {
        "claim_id": "RA-METHOD-001",
        "claim_name": "Nature is the target of RA, not prior theoretical formalisms",
        "claim_node_type": "methodological_guardrail",
        "status": "active",
        "proof_status": "philosophical_methodology",
        "formal_anchor": "RAKB methodological guardrail: target discipline for RA development",
        "dependencies": "",
        "notes": (
            "Relational Actualism is to be evaluated against Nature: observations, "
            "experiments, invariances, regularities, scaling laws, limiting regimes, "
            "and novel predictions. Quantum Mechanics, General Relativity, classical "
            "mechanics, Newtonian gravity, and distributed-consensus systems are not "
            "fundamental targets for RA's ontology or formal apparatus."
        ),
    },
    {
        "claim_id": "RA-METHOD-002",
        "claim_name": "Correspondence recovery concerns empirical content, not inherited ontology",
        "claim_node_type": "methodological_guardrail",
        "status": "active",
        "proof_status": "philosophical_methodology",
        "formal_anchor": "RAKB methodological guardrail: correspondence-regime discipline",
        "dependencies": "RA-METHOD-001",
        "notes": (
            "When RA is compared with QM, GR, or classical theories, the goal is to "
            "recover the observed phenomena and successful limiting predictions of "
            "those theories where empirically required. RA need not adopt their "
            "primitive entities, interpretive commitments, or mathematical formalisms "
            "as fundamental."
        ),
    },
    {
        "claim_id": "RA-MOTIF-COMMIT-METHOD-001",
        "claim_name": "Motif-commit simulations are RA-native actualization models, not QM or consensus simulations",
        "claim_node_type": "modeling_guardrail",
        "status": "active",
        "proof_status": "modeling_discipline",
        "formal_anchor": (
            "RA_MotifCommitProtocol; RA_CausalDAG_MotifCommitSimulator_v0_1; "
            "RA_CausalDAG_MotifCommitSimulator_v0_2; RA_CausalDAG_MotifCommitSimulator_v0_3"
        ),
        "dependencies": "RA-METHOD-001; RA-METHOD-002; RA-CONSENSUS-BRIDGE-001",
        "notes": (
            "The causal-DAG motif-commit simulator explores RA-native structures: "
            "pre-actualized multiplicity, candidate motif families, causal support "
            "cuts, certified readiness, incompatibility, selector closure, commitment, "
            "and causal finality. Distributed consensus and quantum superposition are "
            "comparison analogies only; they are not the formal targets of the simulator. "
            "If RA recovers QM/GR-like empirical regimes, this should be by correspondence "
            "or limiting behavior, not by importing their conceptual apparatus as primitive."
        ),
    },
]

# The report artifact is created by this script. The sha256 is filled after the
# report is written.
ARTIFACT_ID = "ART-METHOD-REPORT-NatureAsTarget-May04-2026"

EDGE_RELATION = "methodological_anchor"
EDGE_VERIFICATION_STATUS = "methodological_guardrail_recorded"


@dataclass(frozen=True)
class UpsertResult:
    target: Path
    inserted: int
    updated: int
    total: int


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        return [], []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def merge_fieldnames(a: Iterable[str], b: Iterable[str]) -> list[str]:
    out: list[str] = []
    for key in list(a) + list(b):
        if key and key not in out:
            out.append(key)
    return out


def upsert_rows(
    target: Path,
    source_rows: list[dict[str, str]],
    key_fields: list[str],
    dry_run: bool,
) -> UpsertResult:
    target_fields, target_rows = read_rows(target)
    if not source_rows:
        return UpsertResult(target, 0, 0, len(target_rows))

    source_fields: list[str] = []
    for row in source_rows:
        source_fields = merge_fieldnames(source_fields, row.keys())
    fieldnames = merge_fieldnames(target_fields, source_fields)

    index: dict[tuple[str, ...], int] = {}
    for i, row in enumerate(target_rows):
        key = tuple(row.get(k, "") for k in key_fields)
        if all(key):
            index[key] = i

    inserted = 0
    updated = 0
    for row in source_rows:
        key = tuple(row.get(k, "") for k in key_fields)
        if not all(key):
            raise ValueError(f"Missing key fields {key_fields} in upsert row for {target}: {row}")
        if key in index:
            target_rows[index[key]].update(row)
            updated += 1
        else:
            target_rows.append(row)
            index[key] = len(target_rows) - 1
            inserted += 1

    if not dry_run:
        write_rows(target, fieldnames, target_rows)

    return UpsertResult(target, inserted, updated, len(target_rows))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def build_report() -> str:
    claim_lines = "\n".join(
        f"- **{row['claim_id']}** — {row['claim_name']}" for row in CLAIMS
    )
    return f"""# RA Method Guardrails: Nature as Target

Date: {DATE_LABEL}

## Purpose

This report records a methodological correction for Relational Actualism (RA):
RA's target is Nature, not the mathematical or conceptual apparatus of prior
successful theories.

Quantum Mechanics, General Relativity, classical mechanics, Newtonian gravity,
and distributed-consensus protocols may serve as comparison languages or
correspondence benchmarks. They are not the ontological targets RA must imitate.

## Claims inserted or updated

{claim_lines}

## Vocabulary discipline

Prefer RA-native language in fundamental claims:

```text
actualization
pre-actualized multiplicity
candidate motif family
causal support cut
Hasse-frontier support
certified readiness
incompatibility
selector closure
committed motif
causal finality
```

Use inherited theory terms only in explicitly marked comparison contexts:

```text
superposition
collapse
wavefunction
Hilbert space
curvature
spacetime manifold
quorum
consensus round
leader election
```

## Correspondence principle

RA may recover the empirical successes of QM, GR, and classical theories in
appropriate limiting or coarse-grained regimes, much as QM/GR recover classical
mechanics or Newtonian gravity. The required recovery concerns observed content:
experimental outcomes, invariances, regularities, scaling laws, and predictions.
It does not require RA to adopt the older theory's primitive ontology or formal
machinery.

## Simulator-specific guardrail

The causal-DAG motif-commit simulator should be interpreted as an RA-native
actualization model. Its operative terms are support cuts, certified readiness,
incompatibility, selector closure, commitment, and finality. Distributed consensus
and quantum superposition remain analogies or comparison regimes only.
"""


def write_report(reports_root: Path, dry_run: bool) -> tuple[Path, str]:
    report_dir = reports_root / REPORT_DIRNAME
    report_path = report_dir / REPORT_FILENAME
    content = build_report()
    if dry_run:
        digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
        return report_path, digest
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path.write_text(content, encoding="utf-8")
    return report_path, sha256_file(report_path)


def build_artifacts(report_path: Path, report_sha: str) -> list[dict[str, str]]:
    return [
        {
            "artifact_id": ARTIFACT_ID,
            "filename": REPORT_FILENAME,
            "type": "md",
            "status": "generated_methodological_guardrail",
            "artifact_role": "methodology_report",
            "supports_results": ";".join(row["claim_id"] for row in CLAIMS),
            "repo_relative_path": f"reports/{REPORT_DIRNAME}/{REPORT_FILENAME}",
            "sha256": report_sha,
            "git_sha": "",
            "path_observed": str(report_path),
            "notes": (
                "Records the RA methodological guardrail that Nature is the target, "
                "while QM, GR, classical theories, and consensus protocols are comparison "
                "or correspondence benchmarks only."
            ),
            "migration_note": "Adds target-discipline guardrails after motif-commit simulator v0.3.",
        }
    ]


def build_edges() -> list[dict[str, str]]:
    return [
        {
            "claim_id": row["claim_id"],
            "claim_name": row["claim_name"],
            "claim_node_type": row["claim_node_type"],
            "artifact_id": ARTIFACT_ID,
            "filename": REPORT_FILENAME,
            "artifact_type": "md",
            "relation": EDGE_RELATION,
            "source_span": row["claim_id"],
            "verification_status": EDGE_VERIFICATION_STATUS,
            "notes": "Methodological guardrail recorded in the Nature-as-target report.",
        }
        for row in CLAIMS
    ]


def backup_registry_files(registry: Path, dry_run: bool) -> Path | None:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_dir = registry / ".backups" / f"ra_method_guardrails_{DATE_LABEL}_{timestamp}"
    files = ["claims.csv", "artifacts.csv", "claim_artifact_edges.csv"]
    existing = [registry / name for name in files if (registry / name).exists()]
    if not existing:
        return None
    if dry_run:
        return backup_dir
    backup_dir.mkdir(parents=True, exist_ok=True)
    for path in existing:
        shutil.copy2(path, backup_dir / path.name)
    return backup_dir


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", required=True, type=Path, help="Path to RAKB registry directory")
    parser.add_argument("--reports", required=True, type=Path, help="Path to RAKB reports directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--no-backup", action="store_true", help="Do not back up existing registry CSV files")
    args = parser.parse_args()

    registry = args.registry
    reports = args.reports

    print(f"RA method guardrail upsert: {DATE_LABEL}")
    print(f"registry: {registry}")
    print(f"reports:  {reports}")
    print(f"dry_run:  {args.dry_run}")

    if not args.no_backup:
        backup_dir = backup_registry_files(registry, args.dry_run)
        if backup_dir is None:
            print("backup: no existing registry CSV files to back up")
        elif args.dry_run:
            print(f"backup: would copy existing registry CSV files to {backup_dir}")
        else:
            print(f"backup: copied existing registry CSV files to {backup_dir}")

    report_path, report_sha = write_report(reports, args.dry_run)
    if args.dry_run:
        print(f"report: would write {report_path}")
    else:
        print(f"report: wrote {report_path}")
    print(f"report sha256: {report_sha}")

    upsert_specs = [
        (registry / "claims.csv", CLAIMS, ["claim_id"]),
        (registry / "artifacts.csv", build_artifacts(report_path, report_sha), ["artifact_id"]),
        (
            registry / "claim_artifact_edges.csv",
            build_edges(),
            ["claim_id", "artifact_id", "relation", "source_span"],
        ),
    ]

    for target, rows, keys in upsert_specs:
        result = upsert_rows(target, rows, keys, args.dry_run)
        action = "would update" if args.dry_run else "updated"
        print(
            f"{target.name}: {action}; "
            f"{result.inserted} insert(s), {result.updated} update(s), total after merge {result.total}"
        )

    print("done")


if __name__ == "__main__":
    main()
