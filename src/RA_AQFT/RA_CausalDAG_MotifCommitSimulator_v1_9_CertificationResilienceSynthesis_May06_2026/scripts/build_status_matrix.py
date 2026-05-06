#!/usr/bin/env python3
"""Build the v1-series epistemic status matrix from claims.yaml + audit_events.csv.

Walks the simulator-side packet list, collects principal claim IDs and
proof_status / source_status fields, and emits a CSV with columns:

    packet, principal_claim, claim_name, epistemic_status, key_caveat,
    rakb_claim_ids, last_audit_event

Usage:
    python scripts/build_status_matrix.py \
        --rakb-dir /path/to/docs/RA_KB \
        --output outputs/ra_v1_series_epistemic_status_matrix.csv
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml


PACKETS = [
    ("v0.5.x", "RA-SIM-SEVERANCE-SIGNATURE-001"),
    ("v0.6", "RA-SIM-SEVERANCE-CHANNEL-001"),
    ("v0.7", "RA-SIM-SUPPORT-FAMILY-001"),
    ("v0.7.1", "RA-SIM-SUPPORT-FAMILY-MONO-001"),
    ("v0.7.2", "RA-SIM-SUPPORT-FAMILY-METRIC-001"),
    ("v0.8", "RA-SIM-CERT-FAMILY-001"),
    ("v0.8.1", "RA-SIM-CERT-CORRELATION-001"),
    ("v0.9", "RA-SIM-NATIVE-CERT-OVERLAP-001"),
    ("v0.9.1", "RA-SIM-NATIVE-CERT-ROBUST-001"),
    ("v0.9.2", "RA-SIM-NATIVE-CERT-CALIB-001"),
    ("v1.0", "RA-SIM-NATIVE-CERT-ANCHOR-001"),
    ("v1.1", "RA-SIM-NATIVE-COMPONENT-DECOUPLE-001"),
    ("v1.2", "RA-SIM-ORIENTATION-LINK-SURFACE-001"),
    ("v1.3", "RA-SIM-NATIVE-ORIENT-LINK-001"),
    ("v1.4", "RA-SIM-PER-GRAPH-ORIENT-WITNESS-001"),
    ("v1.5", "RA-SIM-CONCRETE-GRAPH-ORIENT-002"),
    ("v1.6", "RA-SIM-GRAPH-COUPLED-ORIENT-002"),
    ("v1.7", "RA-SIM-ORIENT-KEYING-001"),
    ("v1.8", "RA-SIM-CONFOUND-V18-001"),
    ("v1.8.1 (within-stratum)", "RA-SIM-CONFOUND-V18-1-001"),
    ("v1.8.1 (cell-level)", "RA-SIM-CONFOUND-V18-1-PACKET-001"),
]

# Map proof_status strings to short epistemic status labels.
STATUS_MAP = {
    "simulation_validated_canonical_run_confirmed": "confirmed_robust",
    "simulation_methodology_confirmed_canonical_via_v1_7": "methodological_only",
    "simulation_canonical_artifact_corrigendum_resolved": "corrected_artifact",
    "simulation_retracted_by_v1_7_canonical_ablation": "retracted",
    "simulation_validated_preliminary_width_matched_diagnostic_superseded_by_v1_8_1": "superseded_preliminary",
    "simulation_methodology_confirmed_keying_tainted_pending_v1_7_ablation": "methodological_only_pending",
    "simulation_keying_tainted_pending_v1_7_ablation": "keying_tainted_resolved_via_v1_7",
}


def load_claims(rakb_dir: Path) -> List[dict]:
    with (rakb_dir / "registry/claims.yaml").open(encoding="utf-8") as f:
        return yaml.safe_load(f).get("claims", [])


def load_audit_events(rakb_dir: Path) -> List[dict]:
    p = rakb_dir / "registry/audit_events.csv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def short_status(proof_status: str) -> str:
    if not proof_status:
        return "unknown"
    return STATUS_MAP.get(proof_status, proof_status)


def first_sentence(text: str, limit: int = 200) -> str:
    text = (text or "").strip().replace("\n", " ").replace("  ", " ")
    if not text:
        return ""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    last_period = cut.rfind(".")
    if last_period > 80:
        return cut[:last_period + 1]
    return cut + "..."


def find_last_audit_event(claim_id: str, events: List[dict]) -> Optional[str]:
    """Return the latest event_id mentioning this claim."""
    matches = []
    for e in events:
        ids = (e.get("claim_ids") or "").split(";")
        if claim_id in [s.strip() for s in ids]:
            matches.append(e["event_id"])
    return matches[-1] if matches else None


def find_claim(claims: List[dict], claim_id: str) -> Optional[dict]:
    for c in claims:
        if c["id"] == claim_id:
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rakb-dir", type=Path, default=Path("docs/RA_KB"))
    ap.add_argument("--output", type=Path, default=Path("outputs/ra_v1_series_epistemic_status_matrix.csv"))
    args = ap.parse_args()

    claims = load_claims(args.rakb_dir)
    events = load_audit_events(args.rakb_dir)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "packet", "principal_claim", "claim_name", "epistemic_status",
            "proof_status_raw", "key_caveat", "rakb_claim_ids", "last_audit_event",
        ])
        for packet, claim_id in PACKETS:
            c = find_claim(claims, claim_id)
            if not c:
                w.writerow([packet, claim_id, "(MISSING)", "missing", "", "", "", ""])
                continue
            proof = c.get("proof_status", "")
            status = short_status(proof)
            caveat = first_sentence(c.get("caveats", ""))
            last_evt = find_last_audit_event(claim_id, events) or ""
            related = [c["id"]]
            for cc in claims:
                links = cc.get("framing_links", []) or []
                deps = cc.get("proof_dependencies", []) or []
                if claim_id in links + deps:
                    related.append(cc["id"])
            related = sorted(set(related))
            w.writerow([
                packet, claim_id, c.get("name", ""), status, proof, caveat,
                ";".join(related[:8]),  # cap to avoid massive cells
                last_evt,
            ])
    print(f"wrote {args.output} with {len(PACKETS)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
