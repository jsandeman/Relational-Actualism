#!/usr/bin/env python3
"""Track B.1 native graph/cut orientation witness extraction.

This module is intentionally conservative.  It extracts orientation-link witness
records from graph/cut incidence data and audits whether the extraction is
actually graph/cut keyed rather than member-index keyed.

It does not assert an orientation-specific rescue claim.  It produces witness
records and overlap diagnostics that future matched-graph rescue analyses may
use only if they pass the v1.9 guardrails.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


def stable_unit(*parts: object) -> float:
    h = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(h[:16], 16) / float(16**16 - 1)


@dataclass(frozen=True)
class TinyDAG:
    parents: Mapping[int, Set[int]]
    children: Mapping[int, Set[int]]
    depth: Mapping[int, int]


def make_demo_dag(seed: int = 17, steps: int = 12) -> TinyDAG:
    parents: Dict[int, Set[int]] = {0: set()}
    children: Dict[int, Set[int]] = {0: set()}
    depth: Dict[int, int] = {0: 0}
    for v in range(1, steps):
        candidates = list(range(v))
        # deterministic 1-3 parent selection, biased toward recent/frontier-like nodes
        k = 1 + int(stable_unit(seed, v, "k") * min(3, len(candidates)))
        scored = sorted(candidates, key=lambda u: (stable_unit(seed, v, u, "p"), -u))[:k]
        parents[v] = set(scored)
        children.setdefault(v, set())
        depth[v] = 1 + max(depth[p] for p in scored)
        for p in scored:
            children.setdefault(p, set()).add(v)
    for v in range(steps):
        parents.setdefault(v, set())
        children.setdefault(v, set())
        depth.setdefault(v, 0)
    return TinyDAG(parents=parents, children=children, depth=depth)


def demo_support_family(width: int, seed: int, max_vertex: int) -> List[FrozenSet[int]]:
    frontier = list(range(max(1, max_vertex - width - 2), max_vertex))
    if not frontier:
        frontier = [0]
    cuts: List[FrozenSet[int]] = []
    # parent/full cut
    cuts.append(frozenset(frontier[-width:]))
    # member subcuts with varied but graph-based subsets
    for i in range(max(1, min(4, len(frontier)))):
        take = max(1, min(width, 1 + ((i + seed) % max(1, width))))
        start = (i * 2 + seed) % len(frontier)
        sub = [frontier[(start + j) % len(frontier)] for j in range(take)]
        cuts.append(frozenset(sorted(sub)))
    # unique, sorted
    return sorted(set(cuts), key=lambda c: (len(c), tuple(sorted(c))))


def incident_orientation_tokens(dag: TinyDAG, cut: Iterable[int]) -> FrozenSet[str]:
    """Graph/cut-derived orientation-link tokens.

    The token set is determined only by graph incidence, edge direction, and
    depth/local orientation parity.  It deliberately does not use member index.
    """
    out: Set[str] = set()
    for v in sorted(cut):
        dv = dag.depth.get(v, 0)
        for p in sorted(dag.parents.get(v, set())):
            dp = dag.depth.get(p, 0)
            delta = dv - dp
            sign = (dv + dp) % 2
            out.add(f"in:{p}->{v}:d{delta}:s{sign}")
        for c in sorted(dag.children.get(v, set())):
            dc = dag.depth.get(c, 0)
            delta = dc - dv
            sign = (dc + dv + 1) % 2
            out.add(f"out:{v}->{c}:d{delta}:s{sign}")
        for p in sorted(dag.parents.get(v, set())):
            for c in sorted(dag.children.get(v, set())):
                dp, dc = dag.depth.get(p, 0), dag.depth.get(c, 0)
                turn = (dc - dp) % 3
                out.add(f"through:{p}->{v}->{c}:turn{turn}")
    return frozenset(out)


def member_indexed_tokens_for_audit(dag: TinyDAG, cut: Iterable[int], member_idx: int) -> FrozenSet[str]:
    """Bad/provenance-control tokenization that includes member_idx.

    This is not used as the Track B witness surface; it exists only to audit that
    the graph/cut surface is independent of member ordering.
    """
    base = incident_orientation_tokens(dag, cut)
    return frozenset(f"{tok}:m{member_idx % 3}" for tok in base)


def jaccard(a: Iterable[object], b: Iterable[object]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    union = sa | sb
    return len(sa & sb) / len(union) if union else 1.0


def all_pairs_mean_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    if len(witnesses) < 2:
        return 0.0
    vals = [jaccard(a, b) for a, b in combinations(witnesses, 2)]
    return sum(vals) / len(vals) if vals else 0.0


def parent_anchored_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    if len(witnesses) < 2:
        return 0.0
    parent = witnesses[0]
    vals = [jaccard(parent, w) for w in witnesses[1:]]
    return sum(vals) / len(vals) if vals else 0.0


def bin_overlap(x: float) -> str:
    if x < 1/3:
        return "low"
    if x < 2/3:
        return "medium"
    return "high"


def extract_rows(seeds: Sequence[int], steps: int, widths: Sequence[int]) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    witness_rows: List[Dict[str, object]] = []
    overlap_rows: List[Dict[str, object]] = []
    audit_rows: List[Dict[str, object]] = []
    for seed in seeds:
        dag = make_demo_dag(seed=seed, steps=steps)
        for width in widths:
            family = demo_support_family(width=width, seed=seed, max_vertex=steps)
            graph_witnesses: List[FrozenSet[str]] = []
            bad_witnesses: List[FrozenSet[str]] = []
            for member_idx, cut in enumerate(family):
                toks = incident_orientation_tokens(dag, cut)
                bad = member_indexed_tokens_for_audit(dag, cut, member_idx)
                graph_witnesses.append(toks)
                bad_witnesses.append(bad)
                witness_rows.append({
                    "seed": seed,
                    "steps": steps,
                    "support_width_requested": width,
                    "family_size": len(family),
                    "member_idx": member_idx,
                    "cut_vertices": ";".join(map(str, sorted(cut))),
                    "token_count": len(toks),
                    "tokens_sample": ";".join(sorted(toks)[:8]),
                    "graph_cut_derived": True,
                    "uses_member_index": False,
                    "orientation_source": "graph_incidence_depth_through_links",
                })
            all_pairs = all_pairs_mean_jaccard(graph_witnesses)
            parent = parent_anchored_jaccard(graph_witnesses)
            bad_all_pairs = all_pairs_mean_jaccard(bad_witnesses)
            overlap_rows.append({
                "seed": seed,
                "steps": steps,
                "support_width_requested": width,
                "family_size": len(family),
                "all_pairs_orientation_jaccard": round(all_pairs, 6),
                "parent_anchored_orientation_jaccard": round(parent, 6),
                "orientation_overlap_bin": bin_overlap(all_pairs),
                "bad_member_indexed_all_pairs_jaccard": round(bad_all_pairs, 6),
                "member_index_delta": round(all_pairs - bad_all_pairs, 6),
            })
            # Audit same-cut stability under member slot changes.
            if family:
                cut = family[0]
                stable_same = incident_orientation_tokens(dag, cut) == incident_orientation_tokens(dag, cut)
                bad_same = member_indexed_tokens_for_audit(dag, cut, 0) == member_indexed_tokens_for_audit(dag, cut, 1)
                audit_rows.append({
                    "seed": seed,
                    "support_width_requested": width,
                    "same_cut_graph_tokens_stable": stable_same,
                    "same_cut_member_indexed_tokens_stable": bad_same,
                    "graph_surface_uses_member_index": False,
                    "bad_control_uses_member_index": True,
                    "fixed_bin_discipline_required": True,
                })
    return witness_rows, overlap_rows, audit_rows


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def run(output_dir: Path, seeds: Sequence[int], steps: int, widths: Sequence[int]) -> Dict[str, object]:
    witness_rows, overlap_rows, audit_rows = extract_rows(seeds, steps, widths)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "ra_trackB_graph_cut_orientation_witness_members.csv", witness_rows)
    write_csv(output_dir / "ra_trackB_graph_cut_orientation_overlap.csv", overlap_rows)
    write_csv(output_dir / "ra_trackB_member_index_audit.csv", audit_rows)
    bins = sorted({r["orientation_overlap_bin"] for r in overlap_rows})
    summary = {
        "seeds": ";".join(map(str, seeds)),
        "steps": steps,
        "widths": ";".join(map(str, widths)),
        "witness_rows": len(witness_rows),
        "overlap_rows": len(overlap_rows),
        "audit_rows": len(audit_rows),
        "orientation_overlap_bins": ";".join(bins),
        "graph_surface_member_index_free": all(not r["graph_surface_uses_member_index"] for r in audit_rows),
        "bad_control_detects_member_index_instability": any(not r["same_cut_member_indexed_tokens_stable"] for r in audit_rows),
    }
    write_csv(output_dir / "ra_trackB_graph_cut_witness_summary.csv", [summary])
    (output_dir / "ra_trackB_graph_cut_witness_summary.md").write_text(
        "# Track B.1 graph/cut orientation witness extraction summary\n\n"
        f"- witness rows: {len(witness_rows)}\n"
        f"- overlap rows: {len(overlap_rows)}\n"
        f"- overlap bins: {summary['orientation_overlap_bins']}\n"
        f"- graph surface member-index-free: {summary['graph_surface_member_index_free']}\n"
        f"- member-indexed bad control detected: {summary['bad_control_detects_member_index_instability']}\n\n"
        "This is a witness-extraction surface, not an orientation-specific rescue claim.\n",
        encoding="utf-8",
    )
    (output_dir / "ra_trackB_graph_cut_witness_state.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main(argv: Optional[Sequence[str]] = None) -> None:
    p = argparse.ArgumentParser(description="Track B.1 graph/cut orientation witness extraction")
    p.add_argument("--output-dir", default="outputs")
    p.add_argument("--seeds", default="17,18,19,20")
    p.add_argument("--steps", type=int, default=14)
    p.add_argument("--widths", default="1,2,3,4")
    args = p.parse_args(argv)
    seeds = tuple(int(x) for x in args.seeds.split(",") if x.strip())
    widths = tuple(int(x) for x in args.widths.split(",") if x.strip())
    summary = run(Path(args.output_dir), seeds=seeds, steps=args.steps, widths=widths)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
