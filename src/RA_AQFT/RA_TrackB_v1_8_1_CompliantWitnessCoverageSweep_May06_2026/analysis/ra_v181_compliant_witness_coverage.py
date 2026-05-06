#!/usr/bin/env python3
"""Track B.3: v1.8.1-compliant witness coverage sweep.

This module audits whether graph/cut witness extraction outputs populate fixed
orientation-overlap bins inside support_width × family_size strata.  It does not
compute or assert orientation-rescue claims.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional

import pandas as pd

BIN_ORDER = ["low", "medium", "high"]


@dataclass(frozen=True)
class CoverageSummary:
    input_rows: int
    source_count: int
    keying_count: int
    surface_count: int
    support_width_classes: str
    family_size_classes: str
    fixed_bin_classes: str
    joint_strata_rows: int
    estimable_joint_strata: int
    estimable_joint_strata_fraction: float
    configs_with_low_medium_high: int
    orientation_rescue_claim_made: bool
    v1_8_1_compliance_posture: str


def _read_csv_if_exists(path: Path) -> Optional[pd.DataFrame]:
    return pd.read_csv(path) if path.exists() else None


def _normalize_active_b2(input_dir: Path, config_id: str) -> pd.DataFrame:
    p = input_dir / "ra_trackB2_active_graph_orientation_overlap.csv"
    df = _read_csv_if_exists(p)
    if df is None:
        return pd.DataFrame()
    out = pd.DataFrame(index=range(len(df)))
    out["config_id"] = config_id
    out["source"] = "trackB_active_graph_witness"
    out["keying"] = "graph_cut_member_index_free"
    out["surface"] = "active_graph_cut_orientation_overlap"
    out["mode"] = "coverage_only"
    out["severity"] = 0.0
    out["threshold_fraction"] = df.get("threshold_fraction", pd.Series([None]*len(df)))
    out["family_semantics"] = df.get("family_semantics", pd.Series([None]*len(df)))
    out["support_width"] = df.get("support_width", pd.Series([None]*len(df)))
    out["family_size"] = df.get("family_size", pd.Series([None]*len(df)))
    out["orientation_overlap"] = df.get("active_all_pairs_orientation_jaccard", pd.Series([None]*len(df)))
    out["orientation_overlap_parent_anchored"] = df.get("active_parent_anchored_orientation_jaccard", pd.Series([None]*len(df)))
    out["orientation_bin"] = df.get("active_orientation_overlap_bin", pd.Series([None]*len(df))).astype(str)
    out["trial_key"] = (
        df.get("run_seed", pd.Series(["?"]*len(df))).astype(str)+":"+
        df.get("motif", pd.Series(["?"]*len(df))).astype(str)+":"+
        df.get("site", pd.Series(["?"]*len(df))).astype(str)+":"+
        out["threshold_fraction"].astype(str)+":"+out["family_semantics"].astype(str)
    )
    return out


def _normalize_v17(input_dir: Path, config_id: str) -> pd.DataFrame:
    p = input_dir / "ra_v1_7_keyed_trial_rows.csv"
    df = _read_csv_if_exists(p)
    if df is None:
        return pd.DataFrame()
    out = pd.DataFrame(index=range(len(df)))
    out["config_id"] = config_id
    out["source"] = "v1_7_matched_graph_keyed_trials"
    out["keying"] = df.get("v1_7_keying", pd.Series(["unknown"]*len(df))).astype(str)
    out["surface"] = "v1_7_orientation_overlap"
    out["mode"] = df.get("mode", pd.Series([None]*len(df))).astype(str)
    out["severity"] = df.get("severity", pd.Series([None]*len(df)))
    out["threshold_fraction"] = df.get("threshold_fraction", pd.Series([None]*len(df)))
    out["family_semantics"] = df.get("family_semantics", pd.Series([None]*len(df)))
    out["support_width"] = df.get("support_width", pd.Series([None]*len(df)))
    out["family_size"] = df.get("family_size", pd.Series([None]*len(df)))
    out["orientation_overlap"] = df.get("v1_7_orientation_overlap_all_pairs", pd.Series([None]*len(df)))
    out["orientation_overlap_parent_anchored"] = df.get("v1_7_orientation_overlap_parent_anchored", pd.Series([None]*len(df)))
    # Fixed bins must come from the original v1.7 keying binning if present. If absent,
    # use global tertiles per config/keying/mode/semantics to mirror v1.7 cell-level bins.
    if "v1_7_orientation_bin" in df.columns:
        out["orientation_bin"] = df["v1_7_orientation_bin"].astype(str)
    else:
        out["orientation_bin"] = _assign_fixed_bins(out, ["config_id","keying","mode","family_semantics"])
    out["trial_key"] = df.get("v1_7_trial_key", pd.Series(range(len(df)))).astype(str)
    return out


def _assign_fixed_bins(df: pd.DataFrame, group_cols: List[str]) -> pd.Series:
    bins = pd.Series(index=df.index, dtype=object)
    for _, g in df.groupby(group_cols, dropna=False):
        vals = g["orientation_overlap"].astype(float)
        if vals.nunique(dropna=True) <= 1:
            bins.loc[g.index] = "single"
            continue
        try:
            q = pd.qcut(vals.rank(method="first"), 3, labels=BIN_ORDER)
            bins.loc[g.index] = q.astype(str)
        except ValueError:
            bins.loc[g.index] = "single"
    return bins.fillna("missing")


def load_normalized_inputs(input_dirs: Iterable[Path]) -> pd.DataFrame:
    frames = []
    for idx, d in enumerate(input_dirs):
        config_id = d.name or f"config_{idx}"
        frames.append(_normalize_active_b2(d, config_id))
        frames.append(_normalize_v17(d, config_id))
    frames = [f for f in frames if not f.empty]
    if not frames:
        raise FileNotFoundError("No supported Track B.2 or v1.7 output files found in input dirs")
    df = pd.concat(frames, ignore_index=True)
    for c in ["support_width","family_size"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").astype("Int64")
    df["has_low"] = df["orientation_bin"].eq("low")
    df["has_high"] = df["orientation_bin"].eq("high")
    return df


def compute_bin_coverage(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["config_id","source","keying","surface","mode","family_semantics","threshold_fraction"]
    rows = []
    for keys, g in df.groupby(group_cols, dropna=False):
        bins = sorted([b for b in g["orientation_bin"].dropna().astype(str).unique() if b not in {"nan","missing"}])
        rows.append(dict(zip(group_cols, keys)) | {
            "rows": len(g),
            "orientation_bins": ";".join(bins),
            "bin_count": len(bins),
            "has_low": "low" in bins,
            "has_medium": "medium" in bins,
            "has_high": "high" in bins,
            "has_low_medium_high": all(b in bins for b in BIN_ORDER),
            "support_width_classes": ";".join(map(str, sorted(g["support_width"].dropna().unique()))),
            "family_size_classes": ";".join(map(str, sorted(g["family_size"].dropna().unique()))),
        })
    return pd.DataFrame(rows)


def compute_joint_strata(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["config_id","source","keying","surface","mode","family_semantics","threshold_fraction","support_width","family_size"]
    rows = []
    for keys, g in df.groupby(group_cols, dropna=False):
        bins = sorted([b for b in g["orientation_bin"].dropna().astype(str).unique() if b not in {"nan","missing"}])
        low_n = int((g["orientation_bin"] == "low").sum())
        high_n = int((g["orientation_bin"] == "high").sum())
        rows.append(dict(zip(group_cols, keys)) | {
            "rows": len(g),
            "orientation_bins": ";".join(bins),
            "low_rows": low_n,
            "high_rows": high_n,
            "estimable_low_high": low_n > 0 and high_n > 0,
            "medium_rows": int((g["orientation_bin"] == "medium").sum()),
            "mean_orientation_overlap": float(pd.to_numeric(g["orientation_overlap"], errors="coerce").mean()) if len(g) else float("nan"),
        })
    return pd.DataFrame(rows)


def compute_estimability_by_config(joint: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["config_id","source","keying","surface","mode","family_semantics","threshold_fraction"]
    rows = []
    for keys, g in joint.groupby(group_cols, dropna=False):
        total = len(g)
        est = int(g["estimable_low_high"].sum()) if total else 0
        rows.append(dict(zip(group_cols, keys)) | {
            "joint_strata": total,
            "estimable_joint_strata": est,
            "estimable_joint_fraction": est / total if total else 0.0,
            "estimable_rows": int(g.loc[g["estimable_low_high"], "rows"].sum()) if total else 0,
            "status": "v1_8_1_estimable" if est > 0 else "non_estimable_under_fixed_bins",
        })
    return pd.DataFrame(rows)


def compute_width_family_distribution(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["config_id","source","keying","mode","family_semantics","orientation_bin","support_width","family_size"]
    dist = df.groupby(group_cols, dropna=False).size().reset_index(name="rows")
    totals = df.groupby(["config_id","source","keying","mode","family_semantics","orientation_bin"], dropna=False).size().reset_index(name="bin_rows")
    return dist.merge(totals, on=["config_id","source","keying","mode","family_semantics","orientation_bin"], how="left").assign(
        fraction=lambda x: x["rows"] / x["bin_rows"].where(x["bin_rows"] != 0, 1)
    )


def compute_sampler_recommendation(bin_cov: pd.DataFrame, est: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in bin_cov.iterrows():
        est_rows = est[(est["config_id"] == r["config_id"]) & (est["source"] == r["source"]) & (est["keying"] == r["keying"]) & (est["mode"] == r["mode"]) & (est["family_semantics"] == r["family_semantics"]) & (est["threshold_fraction"].astype(str) == str(r["threshold_fraction"]))]
        est_frac = float(est_rows["estimable_joint_fraction"].max()) if not est_rows.empty else 0.0
        if not r["has_high"]:
            recommendation = "increase_high_overlap_coverage"
        elif not r["has_low"]:
            recommendation = "increase_low_overlap_coverage"
        elif est_frac == 0:
            recommendation = "rebalance_width_family_bins_or_sampler"
        else:
            recommendation = "coverage_sufficient_for_v1_8_1_audit"
        rows.append({
            "config_id": r["config_id"],
            "source": r["source"],
            "keying": r["keying"],
            "mode": r["mode"],
            "family_semantics": r["family_semantics"],
            "threshold_fraction": r["threshold_fraction"],
            "orientation_bins": r["orientation_bins"],
            "estimable_joint_fraction": est_frac,
            "recommendation": recommendation,
        })
    return pd.DataFrame(rows)


def write_outputs(df: pd.DataFrame, outdir: Path) -> CoverageSummary:
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir / "ra_trackB3_normalized_witness_coverage_rows.csv", index=False)
    bin_cov = compute_bin_coverage(df)
    joint = compute_joint_strata(df)
    est = compute_estimability_by_config(joint)
    dist = compute_width_family_distribution(df)
    rec = compute_sampler_recommendation(bin_cov, est)
    bin_cov.to_csv(outdir / "ra_trackB3_fixed_bin_coverage_by_config.csv", index=False)
    joint.to_csv(outdir / "ra_trackB3_joint_width_family_strata.csv", index=False)
    est.to_csv(outdir / "ra_trackB3_v181_estimability_by_config.csv", index=False)
    dist.to_csv(outdir / "ra_trackB3_width_family_distribution_by_bin.csv", index=False)
    rec.to_csv(outdir / "ra_trackB3_sampler_recommendations.csv", index=False)

    input_rows = len(df)
    source_count = df["source"].nunique()
    keying_count = df["keying"].nunique()
    surface_count = df["surface"].nunique()
    width_classes = ";".join(map(str, sorted(df["support_width"].dropna().unique())))
    family_classes = ";".join(map(str, sorted(df["family_size"].dropna().unique())))
    fixed_bins = ";".join(sorted(df["orientation_bin"].dropna().astype(str).unique()))
    est_count = int(joint["estimable_low_high"].sum()) if not joint.empty else 0
    total_joint = len(joint)
    configs_lmh = int(bin_cov["has_low_medium_high"].sum()) if not bin_cov.empty else 0
    if est_count > 0:
        posture = "v1_8_1_valid_comparison_domains_available"
    elif configs_lmh > 0:
        posture = "low_medium_high_bins_available_but_no_joint_width_family_estimability"
    else:
        posture = "coverage_insufficient_sampler_redesign_or_larger_sweep_needed"
    summary = CoverageSummary(
        input_rows=input_rows,
        source_count=source_count,
        keying_count=keying_count,
        surface_count=surface_count,
        support_width_classes=width_classes,
        family_size_classes=family_classes,
        fixed_bin_classes=fixed_bins,
        joint_strata_rows=total_joint,
        estimable_joint_strata=est_count,
        estimable_joint_strata_fraction=est_count / total_joint if total_joint else 0.0,
        configs_with_low_medium_high=configs_lmh,
        orientation_rescue_claim_made=False,
        v1_8_1_compliance_posture=posture,
    )
    pd.DataFrame([asdict(summary)]).to_csv(outdir / "ra_trackB3_witness_coverage_summary.csv", index=False)
    (outdir / "ra_trackB3_witness_coverage_summary.md").write_text(render_summary(summary, rec), encoding="utf-8")
    (outdir / "ra_trackB3_witness_coverage_state.json").write_text(json.dumps({"summary": asdict(summary)}, indent=2), encoding="utf-8")
    return summary


def render_summary(summary: CoverageSummary, rec: pd.DataFrame) -> str:
    top_recs = rec["recommendation"].value_counts().to_dict() if not rec.empty else {}
    return f"""# Track B.3 v1.8.1-Compliant Witness Coverage Summary

- input_rows: {summary.input_rows}
- sources: {summary.source_count}
- keyings: {summary.keying_count}
- surfaces: {summary.surface_count}
- support_width_classes: {summary.support_width_classes}
- family_size_classes: {summary.family_size_classes}
- fixed_bin_classes: {summary.fixed_bin_classes}
- joint_strata_rows: {summary.joint_strata_rows}
- estimable_joint_strata: {summary.estimable_joint_strata}
- estimable_joint_strata_fraction: {summary.estimable_joint_strata_fraction:.6f}
- configs_with_low_medium_high: {summary.configs_with_low_medium_high}
- orientation_rescue_claim_made: {summary.orientation_rescue_claim_made}
- posture: {summary.v1_8_1_compliance_posture}

## Recommendation counts

{json.dumps(top_recs, indent=2)}

## Interpretation

This packet audits coverage only. It does not compute or promote orientation-specific rescue claims. A future rescue analysis is valid only if fixed orientation bins populate low/high contrasts inside support_width × family_size strata under the v1.8.1 rule.
"""


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dirs", required=True, help="Comma-separated output directories from Track B.2 and/or v1.7")
    ap.add_argument("--output-dir", default="outputs")
    args = ap.parse_args(argv)
    dirs = [Path(p) for p in args.input_dirs.split(",") if p]
    df = load_normalized_inputs(dirs)
    write_outputs(df, Path(args.output_dir))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
