#!/usr/bin/env python3
"""Track B.2 active simulator graph/cut orientation witness extraction.

This module applies the Track B graph/cut witness surface to active v0.9
simulator graph states.  It is infrastructure only: it extracts member-level
orientation witness tokens and overlap diagnostics from the same simulator DAG
states used by the native-overlap workbench.  It does not compute or assert an
orientation-specific rescue claim.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, List, Mapping, Optional, Sequence, Set, Tuple


def _jaccard(a: Iterable[object], b: Iterable[object]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    union = sa | sb
    return len(sa & sb) / len(union) if union else 1.0


def _bin_overlap(x: float) -> str:
    if x < 1.0 / 3.0:
        return "low"
    if x < 2.0 / 3.0:
        return "medium"
    return "high"


def _stable_unit(*parts: object) -> float:
    h = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(h[:16], 16) / float(16**16 - 1)


def all_pairs_mean_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    if len(witnesses) < 2:
        return 0.0
    vals = [_jaccard(a, b) for a, b in combinations(witnesses, 2)]
    return sum(vals) / len(vals) if vals else 0.0


def parent_anchored_jaccard(witnesses: Sequence[FrozenSet[str]]) -> float:
    if len(witnesses) < 2:
        return 0.0
    parent = witnesses[0]
    vals = [_jaccard(parent, w) for w in witnesses[1:]]
    return sum(vals) / len(vals) if vals else 0.0


def active_graph_cut_orientation_tokens(dag: Any, cut: Iterable[int]) -> FrozenSet[str]:
    """Graph/cut-derived orientation-link tokens from active simulator DAG data.

    The token set depends only on graph incidence, edge direction, cut vertices,
    and depth/local orientation parity. It deliberately does not depend on
    support-family member index or output row order.
    """
    out: Set[str] = set()
    parents = getattr(dag, "parents", {})
    children = getattr(dag, "children", {})
    depth = getattr(dag, "depth", {})
    for v in sorted(int(x) for x in cut):
        dv = int(depth.get(v, 0))
        ps = sorted(int(p) for p in parents.get(v, ()))
        cs = sorted(int(c) for c in children.get(v, ()))
        if not ps and not cs:
            out.add(f"orient:isolated:{v}:d{dv}")
        for p in ps:
            dp = int(depth.get(p, 0))
            delta = dv - dp
            sign = 1 if (dv + dp) % 2 == 0 else -1
            out.add(f"in:{p}->{v}:delta{delta}:sign{sign}")
        for c in cs:
            dc = int(depth.get(c, 0))
            delta = dc - dv
            sign = 1 if (dc + dv + 1) % 2 == 0 else -1
            out.add(f"out:{v}->{c}:delta{delta}:sign{sign}")
        for p in ps:
            for c in cs:
                dp, dc = int(depth.get(p, 0)), int(depth.get(c, 0))
                turn = (dc - dp) % 3
                parity = (p + v + c + dv) % 2
                out.add(f"through:{p}->{v}->{c}:turn{turn}:parity{parity}")
    return frozenset(out)


def member_indexed_control_tokens(tokens: Iterable[str], member_idx: int) -> FrozenSet[str]:
    return frozenset(f"{tok}:m{member_idx % 3}" for tok in tokens)


def load_v09(simulator_dir: Path):
    """Load v0.9 simulator modules from either a package parent or simulator dir."""
    simulator_dir = simulator_dir.resolve()
    sys.path.insert(0, str(simulator_dir))
    sys.path.insert(0, str(simulator_dir.parent))
    for name in (
        "simulator.ra_causal_dag_native_cert_overlap",
        "ra_causal_dag_native_cert_overlap",
    ):
        try:
            return importlib.import_module(name)
        except Exception:
            continue
    raise ImportError(f"could not import v0.9 native overlap simulator from {simulator_dir}")


@dataclass(frozen=True)
class ActiveExtractorConfig:
    seeds: Tuple[int, ...]
    steps: int = 16
    max_parents: int = 4
    target_frontier_min: int = 5
    branch_probability: float = 0.42
    wide_join_probability: float = 0.72
    conflict_rate: float = 0.22
    defect_rate: float = 0.02
    orientation_defect_rate: float = 0.02
    conflict_witness_defect_rate: float = 0.08
    max_targets: Optional[int] = 8
    threshold_fractions: Tuple[float, ...] = (1.0, 0.75, 0.5, 0.25)
    family_semantics: Tuple[str, ...] = ("at_least_k", "augmented_exact_k")


def _make_v09_config(v09: Any, cfg: ActiveExtractorConfig, seed: int) -> Any:
    return v09.NativeCertificateOverlapConfig(
        seeds=(seed,),
        steps=cfg.steps,
        max_parents=cfg.max_parents,
        target_frontier_min=cfg.target_frontier_min,
        branch_probability=cfg.branch_probability,
        wide_join_probability=cfg.wide_join_probability,
        conflict_rate=cfg.conflict_rate,
        defect_rate=cfg.defect_rate,
        orientation_defect_rate=cfg.orientation_defect_rate,
        conflict_witness_defect_rate=cfg.conflict_witness_defect_rate,
        max_targets=cfg.max_targets,
        threshold_fractions=cfg.threshold_fractions,
        family_semantics=cfg.family_semantics,
    )


def extract_active_graph_rows(v09: Any, cfg: ActiveExtractorConfig) -> Tuple[List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    witness_rows: List[Dict[str, object]] = []
    overlap_rows: List[Dict[str, object]] = []
    member_index_rows: List[Dict[str, object]] = []
    coverage_rows: List[Dict[str, object]] = []
    estimability_rows: List[Dict[str, object]] = []

    for seed in cfg.seeds:
        vcfg = _make_v09_config(v09, cfg, seed)
        state = v09.build_channel_seed_state(vcfg.channel_config(seed), seed)
        targets = v09.target_motifs_for_channel_severance(
            state.motifs,
            include_alternatives=False,
            max_targets=cfg.max_targets,
        )
        for motif in targets:
            site = max(motif.carrier) if motif.carrier else -1
            if site < 0 or not motif.support_cut:
                continue
            for fraction in cfg.threshold_fractions:
                for semantics in cfg.family_semantics:
                    family = v09.support_family_by_semantics(motif, fraction, semantics)
                    cuts = sorted(family.cuts, key=lambda c: (len(c), tuple(sorted(c))))
                    witnesses: List[FrozenSet[str]] = []
                    bad_witnesses: List[FrozenSet[str]] = []
                    for member_idx, cut in enumerate(cuts):
                        toks = active_graph_cut_orientation_tokens(state.dag, cut)
                        bad = member_indexed_control_tokens(toks, member_idx)
                        witnesses.append(toks)
                        bad_witnesses.append(bad)
                        witness_rows.append({
                            "run_seed": seed,
                            "motif": motif.name,
                            "motif_kind": motif.kind,
                            "site": site,
                            "threshold_fraction": fraction,
                            "family_semantics": semantics,
                            "support_width": len(motif.support_cut),
                            "family_size": len(cuts),
                            "member_idx": member_idx,
                            "cut_vertices": ";".join(map(str, sorted(int(x) for x in cut))),
                            "token_count": len(toks),
                            "token_sample": ";".join(sorted(toks)[:8]),
                            "graph_cut_derived": True,
                            "uses_member_index": False,
                            "source_surface": "active_v0_9_simulator_graph_state",
                        })
                    all_pairs = all_pairs_mean_jaccard(witnesses)
                    parent = parent_anchored_jaccard(witnesses)
                    bad_all = all_pairs_mean_jaccard(bad_witnesses)
                    overlap_rows.append({
                        "run_seed": seed,
                        "motif": motif.name,
                        "motif_kind": motif.kind,
                        "site": site,
                        "threshold_fraction": fraction,
                        "family_semantics": semantics,
                        "support_width": len(motif.support_cut),
                        "family_size": len(cuts),
                        "pair_count": len(cuts) * (len(cuts) - 1) // 2,
                        "active_all_pairs_orientation_jaccard": round(all_pairs, 6),
                        "active_parent_anchored_orientation_jaccard": round(parent, 6),
                        "active_orientation_overlap_bin": _bin_overlap(all_pairs),
                        "bad_member_indexed_all_pairs_jaccard": round(bad_all, 6),
                        "member_index_delta": round(all_pairs - bad_all, 6),
                    })
                    if cuts:
                        base_cut = cuts[0]
                        good_stable = active_graph_cut_orientation_tokens(state.dag, base_cut) == active_graph_cut_orientation_tokens(state.dag, base_cut)
                        bad_stable = member_indexed_control_tokens(active_graph_cut_orientation_tokens(state.dag, base_cut), 0) == member_indexed_control_tokens(active_graph_cut_orientation_tokens(state.dag, base_cut), 1)
                        member_index_rows.append({
                            "run_seed": seed,
                            "motif": motif.name,
                            "threshold_fraction": fraction,
                            "family_semantics": semantics,
                            "same_cut_graph_tokens_stable": good_stable,
                            "same_cut_member_indexed_tokens_stable": bad_stable,
                            "graph_surface_uses_member_index": False,
                            "bad_control_uses_member_index": True,
                        })

    # Coverage: fixed-bin and support_width × family_size strata.
    cov: Dict[Tuple[str, str, int, int], List[Dict[str, object]]] = {}
    for r in overlap_rows:
        cov.setdefault((str(r["family_semantics"]), str(r["active_orientation_overlap_bin"]), int(r["support_width"]), int(r["family_size"])), []).append(r)
    for (sem, bin_, width, famsize), rows in sorted(cov.items()):
        coverage_rows.append({
            "family_semantics": sem,
            "active_orientation_overlap_bin": bin_,
            "support_width": width,
            "family_size": famsize,
            "rows": len(rows),
            "mean_overlap": round(sum(float(r["active_all_pairs_orientation_jaccard"]) for r in rows) / len(rows), 6),
        })

    # Estimability: whether each width×family_size stratum has low and high bins.
    strata: Dict[Tuple[str, int, int], Set[str]] = {}
    counts: Dict[Tuple[str, int, int], int] = {}
    for r in overlap_rows:
        key = (str(r["family_semantics"]), int(r["support_width"]), int(r["family_size"]))
        strata.setdefault(key, set()).add(str(r["active_orientation_overlap_bin"]))
        counts[key] = counts.get(key, 0) + 1
    for (sem, width, famsize), bins in sorted(strata.items()):
        estimability_rows.append({
            "family_semantics": sem,
            "support_width": width,
            "family_size": famsize,
            "orientation_bins": ";".join(sorted(bins)),
            "rows": counts[(sem, width, famsize)],
            "has_low_and_high": "low" in bins and "high" in bins,
            "fixed_bin_discipline_required": True,
        })

    return witness_rows, overlap_rows, member_index_rows, coverage_rows, estimability_rows


def write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader(); w.writerows(rows)


def run(output_dir: Path, v0_9_simulator_dir: Path, cfg: ActiveExtractorConfig) -> Dict[str, object]:
    v09 = load_v09(v0_9_simulator_dir)
    witness_rows, overlap_rows, audit_rows, coverage_rows, estimability_rows = extract_active_graph_rows(v09, cfg)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "ra_trackB2_active_graph_witness_members.csv", witness_rows)
    write_csv(output_dir / "ra_trackB2_active_graph_orientation_overlap.csv", overlap_rows)
    write_csv(output_dir / "ra_trackB2_member_index_audit.csv", audit_rows)
    write_csv(output_dir / "ra_trackB2_fixed_bin_coverage.csv", coverage_rows)
    write_csv(output_dir / "ra_trackB2_width_family_estimability.csv", estimability_rows)
    bins = sorted({str(r["active_orientation_overlap_bin"]) for r in overlap_rows})
    widths = sorted({int(r["support_width"]) for r in overlap_rows})
    famsizes = sorted({int(r["family_size"]) for r in overlap_rows})
    estimable = sum(1 for r in estimability_rows if bool(r["has_low_and_high"]))
    summary = {
        "seeds": ";".join(map(str, cfg.seeds)),
        "steps": cfg.steps,
        "max_targets": cfg.max_targets,
        "witness_rows": len(witness_rows),
        "overlap_rows": len(overlap_rows),
        "member_index_audit_rows": len(audit_rows),
        "fixed_bin_coverage_rows": len(coverage_rows),
        "width_family_estimability_rows": len(estimability_rows),
        "active_orientation_overlap_bins": ";".join(bins),
        "support_width_classes": ";".join(map(str, widths)),
        "family_size_classes": ";".join(map(str, famsizes)),
        "graph_surface_member_index_free": all(not bool(r["graph_surface_uses_member_index"]) for r in audit_rows),
        "bad_control_detects_member_index_instability": any(not bool(r["same_cut_member_indexed_tokens_stable"]) for r in audit_rows),
        "estimable_width_family_strata": estimable,
        "fixed_bin_discipline_required": True,
        "orientation_rescue_claim_made": False,
        "trackB2_posture": "active_state_witness_extraction_surface_no_rescue_claim",
    }
    write_csv(output_dir / "ra_trackB2_active_graph_witness_summary.csv", [summary])
    (output_dir / "ra_trackB2_active_graph_witness_summary.md").write_text(
        "# Track B.2 active simulator graph witness extraction\n\n"
        f"- witness rows: {len(witness_rows)}\n"
        f"- overlap rows: {len(overlap_rows)}\n"
        f"- overlap bins: {summary['active_orientation_overlap_bins']}\n"
        f"- support widths: {summary['support_width_classes']}\n"
        f"- family sizes: {summary['family_size_classes']}\n"
        f"- graph surface member-index-free: {summary['graph_surface_member_index_free']}\n"
        f"- bad member-index control detected: {summary['bad_control_detects_member_index_instability']}\n"
        f"- estimable width×family-size strata: {summary['estimable_width_family_strata']}\n\n"
        "This is an active-state witness extraction surface, not an orientation-specific rescue claim.\n",
        encoding="utf-8",
    )
    (output_dir / "ra_trackB2_active_graph_witness_state.json").write_text(json.dumps({"summary": summary}, indent=2), encoding="utf-8")
    return summary


def _parse_csv_ints(s: str) -> Tuple[int, ...]:
    return tuple(int(x) for x in s.split(",") if x.strip())


def _parse_csv_floats(s: str) -> Tuple[float, ...]:
    return tuple(float(x) for x in s.split(",") if x.strip())


def _parse_csv_strs(s: str) -> Tuple[str, ...]:
    return tuple(x.strip() for x in s.split(",") if x.strip())


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Track B.2 active simulator graph/cut witness extraction")
    p.add_argument("--v0-9-simulator-dir", required=True)
    p.add_argument("--output-dir", default="outputs")
    p.add_argument("--seed-start", type=int, default=17)
    p.add_argument("--seed-stop", type=int, default=21)
    p.add_argument("--seed-list", default=None)
    p.add_argument("--steps", type=int, default=16)
    p.add_argument("--max-parents", type=int, default=4)
    p.add_argument("--target-frontier-min", type=int, default=5)
    p.add_argument("--branch-probability", type=float, default=0.42)
    p.add_argument("--wide-join-probability", type=float, default=0.72)
    p.add_argument("--max-targets", type=int, default=6)
    p.add_argument("--threshold-fractions", default="1.0,0.75,0.5,0.25")
    p.add_argument("--family-semantics", default="at_least_k,augmented_exact_k")
    return p


def config_from_args(args: argparse.Namespace) -> ActiveExtractorConfig:
    seeds = _parse_csv_ints(args.seed_list) if args.seed_list else tuple(range(args.seed_start, args.seed_stop))
    return ActiveExtractorConfig(
        seeds=seeds,
        steps=args.steps,
        max_parents=args.max_parents,
        target_frontier_min=args.target_frontier_min,
        branch_probability=args.branch_probability,
        wide_join_probability=args.wide_join_probability,
        max_targets=None if args.max_targets < 0 else args.max_targets,
        threshold_fractions=_parse_csv_floats(args.threshold_fractions),
        family_semantics=_parse_csv_strs(args.family_semantics),
    )


def main(argv: Optional[Sequence[str]] = None) -> None:
    p = build_arg_parser()
    args = p.parse_args(argv)
    summary = run(Path(args.output_dir), Path(args.v0_9_simulator_dir), config_from_args(args))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
