#!/usr/bin/env python3
"""Validate the typed RAKB v0.5 migration layout.

Run from the RAKB_v0_5 root:
    python scripts/validate_rakb_v0_5.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required: pip install pyyaml", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]

def load_yaml(rel: str):
    with open(ROOT / rel, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_csv(rel: str):
    with open(ROOT / rel, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def fail(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)

def warn(msg: str):
    print(f"WARNING: {msg}")

claims = load_yaml("registry/claims.yaml").get("claims", [])
issues = load_yaml("registry/issues.yaml").get("issues", [])
targets = load_yaml("registry/targets.yaml").get("targets", [])
framing = load_yaml("registry/framing.yaml").get("framing_policies", [])
archived = load_yaml("archive/legacy_registries/archived_claims_from_v0_4_5.yaml").get("archived_claims", [])

node_sets = {
    "claim": {n["id"] for n in claims},
    "issue": {n["id"] for n in issues},
    "target": {n["id"] for n in targets},
    "framing": {n["id"] for n in framing},
    "archived": {n["id"] for n in archived},
}
all_ids = set().union(*node_sets.values())

# Duplicate IDs across typed state; archived may not duplicate active.
seen = {}
for kind, ids in node_sets.items():
    for nid in ids:
        if nid in seen:
            fail(f"duplicate node id {nid!r} appears in both {seen[nid]} and {kind}")
        seen[nid] = kind

for collection_name, collection in [
    ("claims", claims),
    ("issues", issues),
    ("targets", targets),
    ("framing", framing),
    ("archived", archived),
]:
    ids = [n["id"] for n in collection]
    if len(ids) != len(set(ids)):
        fail(f"duplicate IDs inside {collection_name}")

edges = load_csv("registry/all_dependency_edges.csv")
for e in edges:
    if e["src"] not in all_ids:
        warn(f"edge source {e['src']} is not in typed node sets")
    if e["dst"] not in all_ids:
        warn(f"edge destination {e['dst']} is not in typed node sets")

# Active claim graph cycle check
claim_edges = load_csv("registry/claim_edges.csv")
adj = defaultdict(list)
for e in claim_edges:
    if e["src"] not in node_sets["claim"]:
        fail(f"claim_edges.csv source not a claim: {e['src']}")
    if e["dst"] not in node_sets["claim"]:
        fail(f"claim_edges.csv destination not a claim: {e['dst']}")
    adj[e["src"]].append(e["dst"])

visiting, visited = set(), set()
cycle_path = []

def dfs(n: str):
    if n in visiting:
        cycle_path.append(n)
        return True
    if n in visited:
        return False
    visiting.add(n)
    for m in adj[n]:
        if dfs(m):
            cycle_path.append(n)
            return True
    visiting.remove(n)
    visited.add(n)
    return False

for nid in node_sets["claim"]:
    if dfs(nid):
        fail("cycle detected in active claim graph: " + " -> ".join(reversed(cycle_path)))

artifacts = load_csv("registry/artifacts.csv")
artifact_ids = {a["artifact_id"] for a in artifacts}
if len(artifact_ids) != len(artifacts):
    fail("duplicate artifact_id in registry/artifacts.csv")

claim_artifact_edges = load_csv("registry/claim_artifact_edges.csv")
for e in claim_artifact_edges:
    if e["claim_id"] not in all_ids:
        warn(f"claim_artifact edge references node absent from typed files: {e['claim_id']}")
    if e["artifact_id"] not in artifact_ids:
        fail(f"claim_artifact edge references missing artifact: {e['artifact_id']}")

print("RAKB v0.5 structural validation passed.")
print(f"claims={len(claims)} issues={len(issues)} targets={len(targets)} framing={len(framing)} archived={len(archived)}")
print(f"claim_edges={len(claim_edges)} all_dependency_edges={len(edges)} artifacts={len(artifacts)} claim_artifact_edges={len(claim_artifact_edges)}")
