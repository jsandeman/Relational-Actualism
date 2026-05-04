#!/usr/bin/env python3
"""
Apply the RA_MotifOrientationSupportBridge formal-bridge packet to a Lean project.

Actions:
  * copy lean/RA_MotifOrientationSupportBridge.lean into the Lean project root;
  * optionally add `RA_MotifOrientationSupportBridge` to lakefile.lean roots;
  * create timestamped backups unless --no-backup is passed;
  * support --dry-run.

This script does not run Lean. After applying, run:
  lake env lean RA_MotifOrientationSupportBridge.lean
  lake build
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path

MODULE = "RA_MotifOrientationSupportBridge"
MODULE_FILE = f"{MODULE}.lean"
ROOT_LINE = f"    `{MODULE},"


def timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def backup(path: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    dest = backup_dir / f"{path.name}.bak_{timestamp()}"
    shutil.copy2(path, dest)
    return dest


def update_lakefile_text(text: str) -> tuple[str, bool, str]:
    if f"`{MODULE}" in text:
        return text, False, "module root already present"

    lines = text.splitlines()
    anchors = ["`RA_MotifSelectorClosure", "`RA_GraphOrientationClosure", "`RA_MotifCommitProtocol"]
    for anchor in anchors:
        for idx, line in enumerate(lines):
            if anchor in line:
                lines.insert(idx + 1, ROOT_LINE)
                return "\n".join(lines) + ("\n" if text.endswith("\n") else ""), True, f"inserted after {anchor}"
    raise RuntimeError(
        "Could not find a suitable lakefile root anchor. Add this manually: " + ROOT_LINE
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lean-project", required=True, help="Path to Lean project root")
    ap.add_argument("--packet-root", required=True, help="Path to this packet root")
    ap.add_argument("--update-lakefile", action="store_true", help="Add module root to lakefile.lean")
    ap.add_argument("--dry-run", action="store_true", help="Preview actions without writing")
    ap.add_argument("--no-backup", action="store_true", help="Skip backups")
    args = ap.parse_args()

    project = Path(args.lean_project).resolve()
    packet = Path(args.packet_root).resolve()
    src = packet / "lean" / MODULE_FILE
    dst = project / MODULE_FILE
    lakefile = project / "lakefile.lean"
    backup_dir = project / ".backups" / f"motif_orientation_support_bridge_{timestamp()}"

    if not project.exists():
        raise SystemExit(f"Lean project root not found: {project}")
    if not src.exists():
        raise SystemExit(f"Packet Lean source not found: {src}")

    print("RA Motif Orientation Support Bridge apply")
    print(f"project: {project}")
    print(f"packet:  {packet}")
    print(f"dry-run: {args.dry_run}")

    if dst.exists() and not args.no_backup:
        print(f"backup module: {dst}")
        if not args.dry_run:
            backup(dst, backup_dir)
    print(f"copy: {src} -> {dst}")
    if not args.dry_run:
        shutil.copy2(src, dst)

    if args.update_lakefile:
        if not lakefile.exists():
            raise SystemExit(f"lakefile.lean not found: {lakefile}")
        original = lakefile.read_text(encoding="utf-8")
        updated, changed, note = update_lakefile_text(original)
        print(f"lakefile: {note}")
        if changed:
            if not args.no_backup:
                print(f"backup lakefile: {lakefile}")
                if not args.dry_run:
                    backup(lakefile, backup_dir)
            if not args.dry_run:
                lakefile.write_text(updated, encoding="utf-8")

    print("Next checks:")
    print(f"  lake env lean {MODULE_FILE}")
    print("  lake build")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
