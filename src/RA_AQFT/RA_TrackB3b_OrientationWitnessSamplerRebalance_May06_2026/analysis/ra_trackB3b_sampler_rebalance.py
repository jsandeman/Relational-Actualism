#!/usr/bin/env python3
"""Track B.3b orientation-witness sampler/topology rebalance.

This packet is a coverage/sampler audit only. It asks whether available graph
state generator settings can populate v1.8.1-valid comparison domains for
legitimate native-witness keyings. It makes no orientation-rescue claim.

Legitimate sufficiency excludes tainted/member-indexed keyings and shuffled/null
controls. Those can be kept as diagnostics by downstream analysis, but they are
not counted here.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import sys
from dataclasses import dataclass, asdict
from itertools import combinations, product
from pathlib import Path
from typing import Any, Dict, FrozenSet, Iterable, List, Optional, Sequence, Set, Tuple

import pandas as pd

LEGITIMATE_KEYINGS = (
    "edge_pair_signed_no_member",
    "edge_direction_only",
    "incidence_role_signed",
    "catalog_augmented_edge_pair",
    "graph_cut_member_index_free",
)
TAINTED_OR_NULL_KEYINGS = (
    "member_indexed_edge_pair",
    "shuffled_overlap_control",
)
BIN_ORDER = ("low", "medium", "high")


def _jaccard(a: Iterable[object], b: Iterable[object]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    u = sa | sb
    return len(sa & sb) / len(u) if u else 1.0


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


def absolute_overlap_bin(x: float) -> str:
    if x < 1.0 / 3.0:
        return "low"
    if x < 2.0 / 3.0:
        return "medium"
    return "high"


def _stable_int(*parts: object, modulus: int = 10_000_000) -> int:
    h = hashlib.sha256("|".join(map(str, parts)).encode("utf-8")).hexdigest()
    return int(h[:16], 16) % modulus


def load_v09(simulator_dir: Path):
    simulator_dir = simulator_dir.resolve()
    sys.path.insert(0, str(simulator_dir))
    sys.path.insert(0, str(simulator_dir.parent))
    for name in ("simulator.ra_causal_dag_native_cert_overlap", "ra_causal_dag_native_cert_overlap"):
        try:
            return importlib.import_module(name)
        except Exception:
            continue
    raise ImportError(f"could not import v0.9 native overlap simulator from {simulator_dir}")


def load_catalog_tokens(manifest_dir: Optional[Path]) -> Tuple[str, ...]:
    if manifest_dir is None:
        return ("catalog:orientation", "catalog:precedence", "catalog:winding")
    candidates = [
        manifest_dir / "ra_native_orientation_theorem_manifest_v1_3.csv",
        manifest_dir / "ra_native_orientation_theorem_manifest.csv",
    ]
    toks: List[str] = []
    for p in candidates:
        if p.exists():
            try:
                df = pd.read_csv(p)
                for _, r in df.head(64).iterrows():
                    name = str(r.get("theorem", r.get("name", "native")))
                    tags = str(r.get("tags", "orientation"))
                    toks.append("catalog:" + name + ":" + tags.replace(";", "+"))
                break
            except Exception:
                pass
    return tuple(toks or ("catalog:orientation", "catalog:precedence", "catalog:winding"))


@dataclass(frozen=True)
class RebalanceConfig:
    config_id: str
    seeds: Tuple[int, ...]
    steps: int
    max_targets: int
    max_parents: int = 4
    target_frontier_min: int = 5
    branch_probability: float = 0.42
    wide_join_probability: float = 0.72
    conflict_rate: float = 0.22
    defect_rate: float = 0.02
    orientation_defect_rate: float = 0.02
    conflict_witness_defect_rate: float = 0.08
    threshold_fractions: Tuple[float, ...] = (1.0, 0.75, 0.5, 0.25)
    family_semantics: Tuple[str, ...] = ("augmented_exact_k", "at_least_k")


def _make_v09_config(v09: Any, cfg: RebalanceConfig, seed: int) -> Any:
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


def _incidence_sets(dag: Any, cut: Iterable[int]) -> Tuple[Dict[int, List[int]], Dict[int, List[int]], Dict[int, int]]:
    parents = getattr(dag, "parents", {})
    children = getattr(dag, "children", {})
    depth = getattr(dag, "depth", {})
    vs = sorted(int(x) for x in cut)
    ps = {v: sorted(int(p) for p in parents.get(v, ())) for v in vs}
    cs = {v: sorted(int(c) for c in children.get(v, ())) for v in vs}
    ds = {v: int(depth.get(v, 0)) for v in vs}
    return ps, cs, ds


def tokens_for_keying(dag: Any, cut: Iterable[int], keying: str, catalog_tokens: Sequence[str]) -> FrozenSet[str]:
    ps, cs, ds = _incidence_sets(dag, cut)
    out: Set[str] = set()
    for v in sorted(ds):
        dv = ds[v]
        if not ps[v] and not cs[v]:
            out.add(f"isolated:{v}:d{dv}")
        for p in ps[v]:
            dp = int(getattr(dag, "depth", {}).get(p, 0))
            if keying == "edge_direction_only":
                out.add(f"in:{p}->{v}")
            elif keying == "incidence_role_signed":
                sign = (dv + dp) % 2
                out.add(f"role:parent:sign{sign}:d{dv-dp}")
            else:
                sign = (dv + dp) % 2
                out.add(f"in:{p}->{v}:d{dv-dp}:s{sign}")
        for c in cs[v]:
            dc = int(getattr(dag, "depth", {}).get(c, 0))
            if keying == "edge_direction_only":
                out.add(f"out:{v}->{c}")
            elif keying == "incidence_role_signed":
                sign = (dc + dv + 1) % 2
                out.add(f"role:child:sign{sign}:d{dc-dv}")
            else:
                sign = (dc + dv + 1) % 2
                out.add(f"out:{v}->{c}:d{dc-dv}:s{sign}")
        if keying in {"graph_cut_member_index_free", "edge_pair_signed_no_member", "catalog_augmented_edge_pair"}:
            for p in ps[v]:
                for c in cs[v]:
                    dp = int(getattr(dag, "depth", {}).get(p, 0))
                    dc = int(getattr(dag, "depth", {}).get(c, 0))
                    turn = (dc - dp) % 3
                    parity = (p + v + c + dv) % 2
                    out.add(f"through:{p}->{v}->{c}:turn{turn}:parity{parity}")
        if keying == "catalog_augmented_edge_pair":
            # Native theorem-catalog augmentation keyed by graph/cut data, not row order/member index.
            n = len(catalog_tokens) or 1
            idx = _stable_int("catalog", v, dv, len(ps[v]), len(cs[v]), modulus=n)
            out.add(catalog_tokens[idx])
    return frozenset(out)


def extract_config_rows(v09: Any, cfg: RebalanceConfig, catalog_tokens: Sequence[str]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for seed in cfg.seeds:
        vcfg = _make_v09_config(v09, cfg, seed)
        state = v09.build_channel_seed_state(vcfg.channel_config(seed), seed)
        targets = v09.target_motifs_for_channel_severance(
            state.motifs,
            include_alternatives=False,
            max_targets=cfg.max_targets,
        )
        for motif in targets:
            if not motif.support_cut:
                continue
            site = max(motif.carrier) if motif.carrier else -1
            for fraction in cfg.threshold_fractions:
                for semantics in cfg.family_semantics:
                    family = v09.support_family_by_semantics(motif, fraction, semantics)
                    cuts = sorted(family.cuts, key=lambda c: (len(c), tuple(sorted(c))))
                    for keying in LEGITIMATE_KEYINGS:
                        witnesses = [tokens_for_keying(state.dag, cut, keying, catalog_tokens) for cut in cuts]
                        all_pairs = all_pairs_mean_jaccard(witnesses)
                        parent = parent_anchored_jaccard(witnesses)
                        rows.append({
                            "config_id": cfg.config_id,
                            "run_seed": seed,
                            "steps": cfg.steps,
                            "max_targets": cfg.max_targets,
                            "max_parents": cfg.max_parents,
                            "target_frontier_min": cfg.target_frontier_min,
                            "branch_probability": cfg.branch_probability,
                            "wide_join_probability": cfg.wide_join_probability,
                            "keying": keying,
                            "keying_legitimacy": "legitimate_native_witness_keying",
                            "motif": motif.name,
                            "motif_kind": motif.kind,
                            "site": site,
                            "threshold_fraction": fraction,
                            "family_semantics": semantics,
                            "support_width": len(motif.support_cut),
                            "family_size": len(cuts),
                            "pair_count": len(cuts) * (len(cuts) - 1) // 2,
                            "orientation_overlap": round(all_pairs, 6),
                            "orientation_overlap_parent_anchored": round(parent, 6),
                            "orientation_bin": absolute_overlap_bin(all_pairs),
                            "source_surface": "trackB3b_active_graph_state_sampler_rebalance",
                        })
    return rows


def build_configs(
    seeds: Sequence[int],
    steps_values: Sequence[int],
    max_targets_values: Sequence[int],
    branch_probabilities: Sequence[float],
    wide_join_probabilities: Sequence[float],
    threshold_fractions: Sequence[float],
    family_semantics: Sequence[str],
) -> List[RebalanceConfig]:
    configs: List[RebalanceConfig] = []
    for steps, targets, bp, wjp in product(steps_values, max_targets_values, branch_probabilities, wide_join_probabilities):
        cid = f"steps{steps}_targets{targets}_bp{bp:.2f}_wj{wjp:.2f}"
        configs.append(RebalanceConfig(
            config_id=cid,
            seeds=tuple(int(s) for s in seeds),
            steps=int(steps),
            max_targets=int(targets),
            branch_probability=float(bp),
            wide_join_probability=float(wjp),
            threshold_fractions=tuple(float(x) for x in threshold_fractions),
            family_semantics=tuple(str(x) for x in family_semantics),
        ))
    return configs


def fixed_bin_coverage(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["config_id","keying","family_semantics","threshold_fraction"]
    rows = []
    for keys, g in df.groupby(group_cols, dropna=False):
        bins = sorted([b for b in g["orientation_bin"].dropna().astype(str).unique() if b])
        rows.append(dict(zip(group_cols, keys)) | {
            "rows": len(g),
            "orientation_bins": ";".join(bins),
            "bin_count": len(bins),
            "has_low": "low" in bins,
            "has_medium": "medium" in bins,
            "has_high": "high" in bins,
            "has_low_high": "low" in bins and "high" in bins,
            "support_width_classes": ";".join(map(str, sorted(g["support_width"].dropna().unique()))),
            "family_size_classes": ";".join(map(str, sorted(g["family_size"].dropna().unique()))),
            "high_bin_presence_rate": float((g["orientation_bin"] == "high").mean()) if len(g) else 0.0,
        })
    return pd.DataFrame(rows)


def joint_strata(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["config_id","keying","family_semantics","threshold_fraction","support_width","family_size"]
    rows = []
    for keys, g in df.groupby(group_cols, dropna=False):
        low_rows = int((g["orientation_bin"] == "low").sum())
        med_rows = int((g["orientation_bin"] == "medium").sum())
        high_rows = int((g["orientation_bin"] == "high").sum())
        rows.append(dict(zip(group_cols, keys)) | {
            "rows": len(g),
            "orientation_bins": ";".join(b for b in BIN_ORDER if int((g["orientation_bin"] == b).sum()) > 0),
            "low_rows": low_rows,
            "medium_rows": med_rows,
            "high_rows": high_rows,
            "estimable_low_high": low_rows > 0 and high_rows > 0,
            "rows_per_estimable_stratum": len(g) if low_rows > 0 and high_rows > 0 else 0,
        })
    return pd.DataFrame(rows)


def coverage_by_config(df: pd.DataFrame, min_rows_per_stratum: int = 25) -> pd.DataFrame:
    fc = fixed_bin_coverage(df)
    js = joint_strata(df)
    rows = []
    group_cols = ["config_id","keying","family_semantics","threshold_fraction"]
    for keys, g in js.groupby(group_cols, dropna=False):
        est = g[g["estimable_low_high"]]
        sufficient = est[est["rows"] >= min_rows_per_stratum]
        fc_row = fc
        for c, v in zip(group_cols, keys):
            fc_row = fc_row[fc_row[c].astype(str) == str(v)]
        high_rate = float(fc_row["high_bin_presence_rate"].iloc[0]) if not fc_row.empty else 0.0
        bins = str(fc_row["orientation_bins"].iloc[0]) if not fc_row.empty else ""
        rows.append(dict(zip(group_cols, keys)) | {
            "joint_strata": len(g),
            "estimable_joint_strata_count": len(est),
            "sufficient_joint_strata_count": len(sufficient),
            "estimable_joint_strata_fraction": len(est)/len(g) if len(g) else 0.0,
            "sufficient_joint_strata_fraction": len(sufficient)/len(g) if len(g) else 0.0,
            "estimable_rows": int(est["rows"].sum()) if len(est) else 0,
            "min_rows_per_stratum": min_rows_per_stratum,
            "high_bin_presence_rate": high_rate,
            "orientation_bins": bins,
            "coverage_sufficient_legitimate": bool(len(sufficient) > 0),
        })
    out = pd.DataFrame(rows)
    return out


def high_overlap_deficit(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    group_cols = ["config_id","keying","family_semantics","threshold_fraction","support_width","family_size"]
    for keys, g in df.groupby(group_cols, dropna=False):
        rows.append(dict(zip(group_cols, keys)) | {
            "rows": len(g),
            "high_rows": int((g["orientation_bin"] == "high").sum()),
            "low_rows": int((g["orientation_bin"] == "low").sum()),
            "medium_rows": int((g["orientation_bin"] == "medium").sum()),
            "high_overlap_deficit": max(0, 1 - int((g["orientation_bin"] == "high").sum())),
            "low_high_deficit": int(not ((g["orientation_bin"] == "low").any() and (g["orientation_bin"] == "high").any())),
        })
    return pd.DataFrame(rows)


def recommendations(cov: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in cov.iterrows():
        if r["coverage_sufficient_legitimate"]:
            rec = "coverage_sufficient_legitimate_keying"
        elif "high" not in str(r["orientation_bins"]).split(";"):
            rec = "increase_high_overlap_coverage"
        elif "low" not in str(r["orientation_bins"]).split(";"):
            rec = "increase_low_overlap_coverage"
        elif int(r["estimable_joint_strata_count"]) == 0:
            rec = "rebalance_width_family_bins"
        else:
            rec = "increase_rows_per_estimable_stratum"
        rows.append({**r.to_dict(), "recommendation": rec})
    return pd.DataFrame(rows)


def write_outputs(rows: List[Dict[str, object]], output_dir: Path, min_rows_per_stratum: int) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_csv(output_dir / "ra_trackB3b_sampler_sweep.csv", index=False)
    fc = fixed_bin_coverage(df)
    js = joint_strata(df)
    cov = coverage_by_config(df, min_rows_per_stratum=min_rows_per_stratum)
    hd = high_overlap_deficit(df)
    rec = recommendations(cov)
    fc.to_csv(output_dir / "ra_trackB3b_legitimate_keying_coverage.csv", index=False)
    js.to_csv(output_dir / "ra_trackB3b_width_family_bin_support.csv", index=False)
    cov.to_csv(output_dir / "ra_trackB3b_coverage_sufficiency_by_config.csv", index=False)
    hd.to_csv(output_dir / "ra_trackB3b_high_overlap_deficit.csv", index=False)
    rec.to_csv(output_dir / "ra_trackB3b_recommended_configurations.csv", index=False)
    sufficient = int(cov["coverage_sufficient_legitimate"].sum()) if not cov.empty else 0
    summary = {
        "trial_rows": int(len(df)),
        "config_count": int(df["config_id"].nunique()) if not df.empty else 0,
        "legitimate_keying_count": int(df["keying"].nunique()) if not df.empty else 0,
        "coverage_sufficient_cells_excluding_tainted_and_null": sufficient,
        "legitimate_coverage_sufficient_cells": sufficient,
        "max_estimable_joint_strata_count": int(cov["estimable_joint_strata_count"].max()) if not cov.empty else 0,
        "max_sufficient_joint_strata_count": int(cov["sufficient_joint_strata_count"].max()) if not cov.empty else 0,
        "max_high_bin_presence_rate": float(cov["high_bin_presence_rate"].max()) if not cov.empty else 0.0,
        "posture": "valid_trackB_orientation_coverage_candidate_found" if sufficient else "no_legitimate_keying_reaches_coverage_sufficiency_sampler_or_topology_redesign_needed",
        "orientation_rescue_claim_made": False,
    }
    pd.DataFrame([summary]).to_csv(output_dir / "ra_trackB3b_summary.csv", index=False)
    with (output_dir / "ra_trackB3b_sampler_limitations.md").open("w", encoding="utf-8") as f:
        f.write("# Track B.3b sampler/topology rebalance limitations\n\n")
        f.write(f"Trial rows: {summary['trial_rows']}\n\n")
        f.write(f"Coverage-sufficient legitimate cells: {sufficient}\n\n")
        if sufficient:
            f.write("At least one legitimate native-witness keying/configuration reached the configured coverage criterion. This is a coverage result only; it is not an orientation-rescue result.\n")
        else:
            f.write("No legitimate native-witness keying/configuration reached coverage sufficiency. Current simulator settings do not support Track B orientation-rescue inference without sampler/topology redesign.\n")
        f.write("\nTainted/member-indexed and shuffled/null keyings are deliberately excluded from sufficiency counts.\n")
    return summary


def parse_csv_ints(s: str) -> Tuple[int, ...]:
    return tuple(int(x) for x in s.split(",") if x.strip())


def parse_csv_floats(s: str) -> Tuple[float, ...]:
    return tuple(float(x) for x in s.split(",") if x.strip())


def parse_csv_strs(s: str) -> Tuple[str, ...]:
    return tuple(str(x).strip() for x in s.split(",") if x.strip())


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--v0-9-simulator-dir", required=True, type=Path)
    ap.add_argument("--native-manifest-dir", type=Path, default=None)
    ap.add_argument("--output-dir", type=Path, default=Path("outputs"))
    ap.add_argument("--seed-start", type=int, default=17)
    ap.add_argument("--seed-stop", type=int, default=21)
    ap.add_argument("--steps-values", default="16,24")
    ap.add_argument("--max-targets-values", default="6,10")
    ap.add_argument("--branch-probabilities", default="0.35,0.50")
    ap.add_argument("--wide-join-probabilities", default="0.55,0.80")
    ap.add_argument("--threshold-fractions", default="1.0,0.75,0.5,0.25")
    ap.add_argument("--family-semantics", default="augmented_exact_k,at_least_k")
    ap.add_argument("--min-rows-per-stratum", type=int, default=25)
    args = ap.parse_args(argv)

    v09 = load_v09(args.v0_9_simulator_dir)
    seeds = tuple(range(args.seed_start, args.seed_stop))
    configs = build_configs(
        seeds=seeds,
        steps_values=parse_csv_ints(args.steps_values),
        max_targets_values=parse_csv_ints(args.max_targets_values),
        branch_probabilities=parse_csv_floats(args.branch_probabilities),
        wide_join_probabilities=parse_csv_floats(args.wide_join_probabilities),
        threshold_fractions=parse_csv_floats(args.threshold_fractions),
        family_semantics=parse_csv_strs(args.family_semantics),
    )
    catalog = load_catalog_tokens(args.native_manifest_dir)
    rows: List[Dict[str, object]] = []
    for cfg in configs:
        rows.extend(extract_config_rows(v09, cfg, catalog))
    summary = write_outputs(rows, args.output_dir, min_rows_per_stratum=args.min_rows_per_stratum)
    print(json_dumps(summary))
    return 0


def json_dumps(obj: object) -> str:
    import json
    return json.dumps(obj, indent=2, sort_keys=True)


if __name__ == "__main__":
    raise SystemExit(main())
