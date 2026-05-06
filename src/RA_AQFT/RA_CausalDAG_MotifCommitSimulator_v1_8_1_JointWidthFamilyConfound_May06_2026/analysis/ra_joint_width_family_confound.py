"""RA v1.8.1 joint support-width × family-size confound audit.

This packet extends v1.8.  v1.8 showed that width-only matching does not
explain the graph-derived orientation-overlap rescue gaps seen in v1.7, while
shuffled-control gaps shrink or flip under width matching.  However, v1.8 also
found strong association between orientation-overlap bins and family_size.

v1.8.1 therefore performs a stricter apples-to-apples audit:

    orientation bin gap within support_width × family_size strata

It is analysis-only: no Lean, no simulator semantics, no new orientation keying.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import json
import math
import numpy as np
import pandas as pd

ORIENT_COL = "v1_7_orientation_overlap_all_pairs"
RESCUE_COL = "certification_rescue_event"
KEYING_COL = "v1_7_keying"
SHUFFLED = "shuffled_overlap_control"
GRAPH_KEYINGS = [
    "edge_pair_signed_no_member",
    "edge_direction_only",
    "incidence_role_signed",
    "catalog_augmented_edge_pair",
]
ALL_KEYINGS = [
    "member_indexed_edge_pair",
    *GRAPH_KEYINGS,
    SHUFFLED,
]
GROUP_COLS = [KEYING_COL, "mode", "family_semantics"]
CELL_COLS = [KEYING_COL, "mode", "family_semantics", "severity", "threshold_fraction"]
OUT_CELL_COLS = ["keying", "mode", "family_semantics", "severity", "threshold_fraction"]
WIDTH_STRATA = ["support_width"]
JOINT_STRATA = ["support_width", "family_size"]


@dataclass
class JointConfoundSummary:
    version: str
    input_rows: int
    keying_count: int
    width_classes: str
    family_size_classes: str
    selector_guardrail_passed: bool
    raw_gap_rows: int
    width_matched_gap_rows: int
    joint_matched_gap_rows: int
    graph_vs_shuffled_joint_rows: int
    estimable_joint_group_fraction_graph: float
    mean_abs_raw_gap_graph: float
    mean_abs_width_gap_graph: float
    mean_abs_joint_gap_graph: float
    mean_abs_graph_minus_shuffled_joint_gap: float
    mean_joint_gap_reduction_from_raw_graph: float
    v1_8_1_posture: str


def _bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["true", "1", "yes"])


def _assign_tercile_bins(df: pd.DataFrame, value_col: str = ORIENT_COL) -> pd.DataFrame:
    """Add orientation_bin per keying/mode/family_semantics group.

    This intentionally matches the v1.8 binning convention so v1.8.1 is a
    direct confound audit rather than a new binning model.
    """
    out = df.copy()
    bins = []
    for _, g in out.groupby(GROUP_COLS, dropna=False, sort=False):
        vals = g[value_col].astype(float)
        n = len(vals)
        if n == 0:
            continue
        ranks = vals.rank(method="first", ascending=True)
        idx = np.floor((ranks - 1) * 3 / max(n, 1)).astype(int).clip(0, 2)
        labels = pd.Series(np.array(["low", "medium", "high"])[idx], index=g.index)
        bins.append(labels)
    out["orientation_bin"] = pd.concat(bins).sort_index() if bins else pd.Series(dtype=str)
    return out


def load_keyed_rows(input_dir: str | Path) -> pd.DataFrame:
    input_dir = Path(input_dir)
    p = input_dir / "ra_v1_7_keyed_trial_rows.csv"
    if not p.exists():
        raise FileNotFoundError(f"missing v1.7 keyed trial rows: {p}")
    df = pd.read_csv(p)
    required = {
        KEYING_COL, "mode", "family_semantics", "severity", "threshold_fraction",
        ORIENT_COL, RESCUE_COL, "support_width", "family_size",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"v1.7 keyed rows missing required columns: {sorted(missing)}")
    df[RESCUE_COL] = _bool_series(df[RESCUE_COL])
    if "selector_stress" in df.columns:
        df["selector_stress_bool"] = _bool_series(df["selector_stress"])
    else:
        df["selector_stress_bool"] = df["mode"].astype(str).eq("selector_stress")
    df["support_width"] = df["support_width"].astype(int)
    df["family_size"] = df["family_size"].astype(int)
    return _assign_tercile_bins(df)


def _gap_stats(g: pd.DataFrame) -> dict:
    by = g.groupby("orientation_bin")[RESCUE_COL].agg(["mean", "count"]).to_dict("index")
    low = by.get("low", {}).get("mean", np.nan)
    high = by.get("high", {}).get("mean", np.nan)
    low_n = int(by.get("low", {}).get("count", 0))
    high_n = int(by.get("high", {}).get("count", 0))
    paired = min(low_n, high_n)
    return {
        "low_rescue": float(low) if not pd.isna(low) else np.nan,
        "high_rescue": float(high) if not pd.isna(high) else np.nan,
        "low_count": low_n,
        "high_count": high_n,
        "paired_count": int(paired),
        "low_minus_high_gap": float(low - high) if not (pd.isna(low) or pd.isna(high)) else np.nan,
    }


def raw_specificity_gaps(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, g in df.groupby(CELL_COLS, dropna=False):
        keying, mode, sem, severity, threshold = keys
        d = _gap_stats(g)
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "severity": severity,
            "threshold_fraction": threshold,
            "rows": len(g),
            **{f"raw_{k}": v for k, v in d.items()},
            "status": "raw_gap_estimable" if not pd.isna(d["low_minus_high_gap"]) else "raw_gap_not_estimable",
        })
    return pd.DataFrame(rows)


def matched_stratum_gaps(df: pd.DataFrame, strata_cols: list[str], label: str) -> pd.DataFrame:
    """Low-high rescue gaps within exact matching strata."""
    rows = []
    group_cols = CELL_COLS + strata_cols
    for keys, g in df.groupby(group_cols, dropna=False):
        keying, mode, sem, severity, threshold, *strata_vals = keys
        d = _gap_stats(g)
        row = {
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "severity": severity,
            "threshold_fraction": threshold,
            "matching_level": label,
            "rows": len(g),
            "low_count": d["low_count"],
            "high_count": d["high_count"],
            "paired_count": d["paired_count"],
            "low_rescue": d["low_rescue"],
            "high_rescue": d["high_rescue"],
            "low_minus_high_gap": d["low_minus_high_gap"],
            "stratum_estimable": bool(d["paired_count"] > 0 and not pd.isna(d["low_minus_high_gap"])),
        }
        for c, v in zip(strata_cols, strata_vals):
            row[c] = int(v) if isinstance(v, (int, np.integer)) or str(v).isdigit() else v
        rows.append(row)
    return pd.DataFrame(rows)


def aggregate_matched_gaps(stratum_gaps: pd.DataFrame, label: str, raw: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Aggregate stratum gaps by cell.

    The primary matched gap is paired-count weighted.  An unweighted mean is also
    reported for auditability.
    """
    rows = []
    for keys, g0 in stratum_gaps.groupby(OUT_CELL_COLS, dropna=False):
        keying, mode, sem, severity, threshold = keys
        g = g0[g0["stratum_estimable"]].copy()
        if len(g):
            weights = g["paired_count"].astype(float)
            weighted_gap = float(np.average(g["low_minus_high_gap"].astype(float), weights=weights)) if weights.sum() > 0 else np.nan
            unweighted_gap = float(g["low_minus_high_gap"].mean())
            matched_trials = int(g["paired_count"].sum() * 2)
            matched_strata = int(len(g))
            strata_desc = ";".join(_format_stratum_desc(r, label) for _, r in g.iterrows())
        else:
            weighted_gap = np.nan
            unweighted_gap = np.nan
            matched_trials = 0
            matched_strata = 0
            strata_desc = ""
        total_strata = int(len(g0))
        raw_gap = np.nan
        if raw is not None and len(raw):
            rr = raw[
                (raw["keying"] == keying)
                & (raw["mode"] == mode)
                & (raw["family_semantics"] == sem)
                & (raw["severity"] == severity)
                & (raw["threshold_fraction"] == threshold)
            ]
            if len(rr):
                raw_gap = float(rr.iloc[0]["raw_low_minus_high_gap"])
        reduction = np.nan
        if not pd.isna(raw_gap) and raw_gap != 0 and not pd.isna(weighted_gap):
            reduction = float(1.0 - (abs(weighted_gap) / abs(raw_gap)))
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "severity": severity,
            "threshold_fraction": threshold,
            "matching_level": label,
            "raw_low_minus_high_gap": raw_gap,
            "matched_low_minus_high_gap_weighted": weighted_gap,
            "matched_low_minus_high_gap_unweighted": unweighted_gap,
            "matched_gap_abs_weighted": float(abs(weighted_gap)) if not pd.isna(weighted_gap) else np.nan,
            "gap_reduction_from_raw": reduction,
            "matched_strata_count": matched_strata,
            "total_strata_count": total_strata,
            "estimable_strata_fraction": float(matched_strata / total_strata) if total_strata else np.nan,
            "matched_trials_paired_low_high": matched_trials,
            "matched_strata": strata_desc,
            "status": "matched_strata_available" if matched_strata else "insufficient_joint_matched_low_high_bins",
        })
    return pd.DataFrame(rows)


def _format_stratum_desc(r: pd.Series, label: str) -> str:
    if label == "width":
        return f"w{int(r['support_width'])}"
    if label == "width_family_size":
        return f"w{int(r['support_width'])}:f{int(r['family_size'])}"
    return "stratum"


def graph_vs_shuffled_joint_matched(joint: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "graph_keying", "mode", "family_semantics", "severity", "threshold_fraction",
        "graph_joint_matched_gap", "shuffled_joint_matched_gap",
        "joint_matched_gap_delta_graph_minus_shuffled", "graph_matched_strata_count",
        "shuffled_matched_strata_count", "graph_matched_trials", "shuffled_matched_trials",
        "interpretation",
    ]
    rows = []
    shuf = joint[joint["keying"] == SHUFFLED]
    for _, r in joint[joint["keying"].isin(GRAPH_KEYINGS)].iterrows():
        s = shuf[
            (shuf["mode"] == r["mode"])
            & (shuf["family_semantics"] == r["family_semantics"])
            & (shuf["severity"] == r["severity"])
            & (shuf["threshold_fraction"] == r["threshold_fraction"])
        ]
        if len(s):
            sr = s.iloc[0]
            ggap = r["matched_low_minus_high_gap_weighted"]
            sgap = sr["matched_low_minus_high_gap_weighted"]
            delta = float(ggap - sgap) if not (pd.isna(ggap) or pd.isna(sgap)) else np.nan
            if pd.isna(delta):
                interp = "insufficient_joint_match"
            elif abs(delta) < 0.05:
                interp = "graph_matches_shuffled_after_joint_matching"
            else:
                interp = "graph_differs_from_shuffled_after_joint_matching"
            rows.append({
                "graph_keying": r["keying"],
                "mode": r["mode"],
                "family_semantics": r["family_semantics"],
                "severity": r["severity"],
                "threshold_fraction": r["threshold_fraction"],
                "graph_joint_matched_gap": ggap,
                "shuffled_joint_matched_gap": sgap,
                "joint_matched_gap_delta_graph_minus_shuffled": delta,
                "graph_matched_strata_count": r["matched_strata_count"],
                "shuffled_matched_strata_count": sr["matched_strata_count"],
                "graph_matched_trials": r["matched_trials_paired_low_high"],
                "shuffled_matched_trials": sr["matched_trials_paired_low_high"],
                "interpretation": interp,
            })
    return pd.DataFrame(rows, columns=cols)


def estimability_by_stratum(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize whether width×family strata can support low/high comparisons."""
    rows = []
    for keys, g in df.groupby(CELL_COLS + JOINT_STRATA, dropna=False):
        keying, mode, sem, severity, threshold, width, fsize = keys
        bins = g["orientation_bin"].value_counts().to_dict()
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "severity": severity,
            "threshold_fraction": threshold,
            "support_width": int(width),
            "family_size": int(fsize),
            "rows": len(g),
            "low_count": int(bins.get("low", 0)),
            "medium_count": int(bins.get("medium", 0)),
            "high_count": int(bins.get("high", 0)),
            "low_high_estimable": bool(bins.get("low", 0) > 0 and bins.get("high", 0) > 0),
            "bin_signature": ";".join(f"{k}:{v}" for k, v in sorted(bins.items())),
        })
    return pd.DataFrame(rows)


def orientation_gap_decomposition(raw: pd.DataFrame, width_agg: pd.DataFrame, joint_agg: pd.DataFrame) -> pd.DataFrame:
    rows = []
    idx_cols = OUT_CELL_COLS
    w = width_agg.set_index(idx_cols)
    j = joint_agg.set_index(idx_cols)
    for _, r in raw.iterrows():
        key = tuple(r[c] for c in idx_cols)
        raw_gap = float(r["raw_low_minus_high_gap"]) if not pd.isna(r["raw_low_minus_high_gap"]) else np.nan
        width_gap = np.nan
        joint_gap = np.nan
        width_reduction = np.nan
        joint_reduction = np.nan
        width_status = "missing"
        joint_status = "missing"
        if key in w.index:
            wr = w.loc[key]
            width_gap = float(wr["matched_low_minus_high_gap_weighted"]) if not pd.isna(wr["matched_low_minus_high_gap_weighted"]) else np.nan
            width_reduction = float(wr["gap_reduction_from_raw"]) if not pd.isna(wr["gap_reduction_from_raw"]) else np.nan
            width_status = str(wr["status"])
        if key in j.index:
            jr = j.loc[key]
            joint_gap = float(jr["matched_low_minus_high_gap_weighted"]) if not pd.isna(jr["matched_low_minus_high_gap_weighted"]) else np.nan
            joint_reduction = float(jr["gap_reduction_from_raw"]) if not pd.isna(jr["gap_reduction_from_raw"]) else np.nan
            joint_status = str(jr["status"])
        rows.append({
            **{c: r[c] for c in idx_cols},
            "raw_gap": raw_gap,
            "width_matched_gap": width_gap,
            "joint_width_family_matched_gap": joint_gap,
            "width_gap_reduction_from_raw": width_reduction,
            "joint_gap_reduction_from_raw": joint_reduction,
            "width_status": width_status,
            "joint_status": joint_status,
            "interpretation": _decomp_interpretation(raw_gap, width_gap, joint_gap, r["keying"]),
        })
    return pd.DataFrame(rows)


def _decomp_interpretation(raw_gap: float, width_gap: float, joint_gap: float, keying: str) -> str:
    if pd.isna(raw_gap):
        return "raw_gap_not_estimable"
    if pd.isna(joint_gap):
        return "joint_matching_not_estimable"
    if raw_gap != 0 and abs(joint_gap) < 0.25 * abs(raw_gap):
        return "joint_matching_explains_most_gap"
    if keying == SHUFFLED and raw_gap != 0 and abs(joint_gap) < 0.5 * abs(raw_gap):
        return "shuffled_gap_largely_shrinks_under_joint_matching"
    if raw_gap != 0 and abs(joint_gap) >= 0.5 * abs(raw_gap):
        return "residual_gap_survives_joint_matching"
    return "gap_small_or_ambiguous"


def selector_guardrail(df: pd.DataFrame) -> bool:
    if "selector_stress" not in set(df["mode"]):
        return True
    return bool(df[df["mode"] == "selector_stress"][RESCUE_COL].mean() == 0.0)


def run_analysis(input_dir: str | Path, output_dir: str | Path) -> JointConfoundSummary:
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    df = load_keyed_rows(input_dir)
    raw = raw_specificity_gaps(df)
    width_strata = matched_stratum_gaps(df, WIDTH_STRATA, "width")
    width_agg = aggregate_matched_gaps(width_strata, "width", raw)
    joint_strata = matched_stratum_gaps(df, JOINT_STRATA, "width_family_size")
    joint_agg = aggregate_matched_gaps(joint_strata, "width_family_size", raw)
    gvs = graph_vs_shuffled_joint_matched(joint_agg)
    estimability = estimability_by_stratum(df)
    decomp = orientation_gap_decomposition(raw, width_agg, joint_agg)

    raw.to_csv(out / "ra_v1_8_1_raw_specificity_gaps.csv", index=False)
    width_agg.to_csv(out / "ra_v1_8_1_width_matched_gap.csv", index=False)
    joint_strata.to_csv(out / "ra_v1_8_1_joint_stratum_gaps.csv", index=False)
    joint_agg.to_csv(out / "ra_v1_8_1_joint_width_family_matched_gap.csv", index=False)
    gvs.to_csv(out / "ra_v1_8_1_graph_vs_shuffled_joint_matched.csv", index=False)
    estimability.to_csv(out / "ra_v1_8_1_estimability_by_stratum.csv", index=False)
    decomp.to_csv(out / "ra_v1_8_1_orientation_gap_decomposition.csv", index=False)

    graph_raw = raw[raw["keying"].isin(GRAPH_KEYINGS)]
    graph_width = width_agg[width_agg["keying"].isin(GRAPH_KEYINGS)]
    graph_joint = joint_agg[joint_agg["keying"].isin(GRAPH_KEYINGS)]
    estimable_graph = graph_joint[graph_joint["status"] == "matched_strata_available"]
    valid_gvs = gvs.dropna(subset=["joint_matched_gap_delta_graph_minus_shuffled"])
    reduction_vals = graph_joint["gap_reduction_from_raw"].dropna()
    summary = JointConfoundSummary(
        version="v1.8.1",
        input_rows=int(len(df)),
        keying_count=int(df[KEYING_COL].nunique()),
        width_classes=";".join(map(str, sorted(map(int, df["support_width"].dropna().unique())))),
        family_size_classes=";".join(map(str, sorted(map(int, df["family_size"].dropna().unique())))),
        selector_guardrail_passed=selector_guardrail(df),
        raw_gap_rows=int(len(raw)),
        width_matched_gap_rows=int(len(width_agg)),
        joint_matched_gap_rows=int(len(joint_agg)),
        graph_vs_shuffled_joint_rows=int(len(gvs)),
        estimable_joint_group_fraction_graph=float(len(estimable_graph) / len(graph_joint)) if len(graph_joint) else np.nan,
        mean_abs_raw_gap_graph=float(graph_raw["raw_low_minus_high_gap"].abs().mean()) if len(graph_raw) else np.nan,
        mean_abs_width_gap_graph=float(graph_width["matched_low_minus_high_gap_weighted"].abs().mean()) if len(graph_width.dropna(subset=["matched_low_minus_high_gap_weighted"])) else np.nan,
        mean_abs_joint_gap_graph=float(graph_joint["matched_low_minus_high_gap_weighted"].abs().mean()) if len(graph_joint.dropna(subset=["matched_low_minus_high_gap_weighted"])) else np.nan,
        mean_abs_graph_minus_shuffled_joint_gap=float(valid_gvs["joint_matched_gap_delta_graph_minus_shuffled"].abs().mean()) if len(valid_gvs) else np.nan,
        mean_joint_gap_reduction_from_raw_graph=float(reduction_vals.mean()) if len(reduction_vals) else np.nan,
        v1_8_1_posture=_posture(graph_joint, valid_gvs),
    )
    pd.DataFrame([asdict(summary)]).to_csv(out / "ra_v1_8_1_joint_confound_summary.csv", index=False)
    with open(out / "ra_v1_8_1_joint_confound_summary.md", "w") as f:
        f.write(render_summary(summary, decomp, gvs, estimability))
    with open(out / "ra_v1_8_1_state.json", "w") as f:
        json.dump({"summary": asdict(summary)}, f, indent=2)
    return summary


def _posture(graph_joint: pd.DataFrame, gvs: pd.DataFrame) -> str:
    estimable = graph_joint.dropna(subset=["matched_low_minus_high_gap_weighted"])
    if len(estimable) == 0:
        return "joint_width_family_matching_not_estimable_redesign_sampler_needed"
    mean_abs = float(estimable["matched_low_minus_high_gap_weighted"].abs().mean())
    if mean_abs < 0.05:
        return "joint_matching_shrinks_graph_orientation_gap"
    if len(gvs.dropna(subset=["joint_matched_gap_delta_graph_minus_shuffled"])):
        md = float(gvs["joint_matched_gap_delta_graph_minus_shuffled"].abs().mean())
        if md < 0.05:
            return "graph_and_shuffled_match_after_joint_matching_binning_artifact"
        return "candidate_residual_graph_orientation_gap_after_joint_matching"
    return "joint_matching_estimable_but_shuffled_comparison_insufficient"


def render_summary(summary: JointConfoundSummary, decomp: pd.DataFrame, gvs: pd.DataFrame, estimability: pd.DataFrame) -> str:
    lines = []
    lines.append("# RA v1.8.1 Joint Width × Family-Size Confound Audit\n")
    lines.append("This analysis extends v1.8 by matching low/high orientation-overlap bins within exact support_width × family_size strata. It is analysis-only and makes no Lean or simulator-semantics changes.\n")
    lines.append("## Summary metrics\n")
    for k, v in asdict(summary).items():
        lines.append(f"- **{k}**: {v}")
    lines.append("\n## Decision discipline\n")
    lines.append("- If graph-derived gaps shrink under joint width × family-size matching, the residual v1.8 signal is explained by family-structure confounding.")
    lines.append("- If graph-derived gaps survive and differ from shuffled controls inside the same joint strata, the result supports a candidate residual graph-derived orientation association.")
    lines.append("- If few or no joint strata are estimable, the current sampler cannot decide the question and a redesigned matched sampler is required.\n")
    if len(decomp):
        focus = decomp[(decomp["mode"] == "orientation_degradation") & (decomp["keying"].isin(GRAPH_KEYINGS + [SHUFFLED]))]
        if len(focus):
            lines.append("## Orientation-degradation focus\n")
            for _, r in focus.head(20).iterrows():
                lines.append(
                    f"- {r['keying']} / {r['family_semantics']} / sev={r['severity']} / th={r['threshold_fraction']}: "
                    f"raw={r['raw_gap']:.4g}, width={r['width_matched_gap']:.4g}, joint={r['joint_width_family_matched_gap']:.4g}, {r['interpretation']}"
                )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()
    s = run_analysis(args.input_dir, args.output_dir)
    print(json.dumps(asdict(s), indent=2))
