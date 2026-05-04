#!/usr/bin/env python3
"""
Apply RA_MotifSelectorClosure formal bridge packet to a Lean project.

This script copies lean/RA_MotifSelectorClosure.lean into the project root,
optionally inserts `RA_MotifSelectorClosure into lakefile.lean after
`RA_MotifCommitProtocol, and can run a local Lean check when Lake is available.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


MODULE_NAME = "RA_MotifSelectorClosure.lean"
UPSTREAM_NAME = "RA_MotifCommitProtocol.lean"
ROOT_TOKEN = "`RA_MotifSelectorClosure"
AFTER_TOKEN = "`RA_MotifCommitProtocol"


def ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def ensure_context_gated(project: Path) -> None:
    upstream = project / UPSTREAM_NAME
    if not upstream.exists():
        raise FileNotFoundError(f"missing upstream {UPSTREAM_NAME} in {project}")
    text = read(upstream)
    required = [
        "supports : MotifCandidate",
        "supports : GraphMotifCandidate",
        "DAGCommitsAt.supports",
        "GraphCommitsAt.supports",
    ]
    missing = [token for token in required if token not in text]
    if missing:
        raise RuntimeError(
            "upstream RA_MotifCommitProtocol does not look context-gated; "
            f"missing token(s): {missing}"
        )


def copy_module(packet: Path, project: Path, dry_run: bool) -> None:
    src = packet / "lean" / MODULE_NAME
    dst = project / MODULE_NAME
    if not src.exists():
        raise FileNotFoundError(f"missing packet Lean file: {src}")
    if dry_run:
        print(f"[dry-run] copy {src} -> {dst}")
        return
    if dst.exists():
        backup = dst.with_suffix(dst.suffix + f".bak_{ts()}")
        shutil.copy2(dst, backup)
        print(f"backup: {backup}")
    shutil.copy2(src, dst)
    print(f"copied: {dst}")


def update_lakefile(project: Path, dry_run: bool) -> None:
    lakefile = project / "lakefile.lean"
    if not lakefile.exists():
        raise FileNotFoundError(f"missing lakefile: {lakefile}")
    text = read(lakefile)
    if ROOT_TOKEN in text:
        print("lakefile already contains RA_MotifSelectorClosure root")
        return
    lines = text.splitlines()
    out = []
    inserted = False
    for line in lines:
        out.append(line)
        if AFTER_TOKEN in line and not inserted:
            indent = line[: len(line) - len(line.lstrip())]
            out.append(f"{indent}{ROOT_TOKEN},    -- (May 4 2026) selector-closure bridge for motif-commit semantics.")
            inserted = True
    if not inserted:
        raise RuntimeError(f"could not find {AFTER_TOKEN} in lakefile.lean")
    new_text = "\n".join(out) + ("\n" if text.endswith("\n") else "")
    if dry_run:
        print(f"[dry-run] would insert {ROOT_TOKEN} into {lakefile}")
        return
    backup = lakefile.with_suffix(lakefile.suffix + f".bak_{ts()}")
    shutil.copy2(lakefile, backup)
    write(lakefile, new_text)
    print(f"backup: {backup}")
    print(f"updated: {lakefile}")


def lexical_check(project: Path) -> None:
    module = project / MODULE_NAME
    text = read(module)
    bad = {token: text.count(token) for token in ["sorry", "admit", "axiom"]}
    if any(bad.values()):
        raise RuntimeError(f"forbidden placeholder token(s) found: {bad}")
    print("lexical check: no sorry/admit/axiom")


def run_lean_check(project: Path) -> int:
    lake = shutil.which("lake")
    if lake is None:
        print("lake not found on PATH; skipping Lean check")
        return 0
    cmd = [lake, "env", "lean", MODULE_NAME]
    print("running:", " ".join(cmd))
    proc = subprocess.run(cmd, cwd=project, text=True)
    return proc.returncode


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean-project", required=True, type=Path)
    ap.add_argument("--packet-root", required=True, type=Path)
    ap.add_argument("--update-lakefile", action="store_true")
    ap.add_argument("--check", action="store_true", help="run lake env lean after copying")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    project = args.lean_project.resolve()
    packet = args.packet_root.resolve()
    print("RA Motif Selector Closure bridge apply")
    print("project:", project)
    print("packet: ", packet)
    print("dry-run:", args.dry_run)

    ensure_context_gated(project)
    copy_module(packet, project, args.dry_run)
    if args.update_lakefile:
        update_lakefile(project, args.dry_run)
    if not args.dry_run:
        lexical_check(project)
        if args.check:
            return run_lean_check(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
