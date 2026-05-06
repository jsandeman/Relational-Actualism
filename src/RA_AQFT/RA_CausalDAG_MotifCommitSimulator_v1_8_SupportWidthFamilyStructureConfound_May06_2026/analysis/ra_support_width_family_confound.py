"""RA v1.8 support-width / family-structure confound audit.

This analysis consumes v1.7 orientation-keying ablation outputs and asks whether
orientation-overlap rescue gaps are better explained by support width, family
size, and binning structure than by orientation-link specificity.

It is analysis-only: no Lean, no simulator semantics, no new actualization rule.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional
import json
import math
import pandas as pd
import numpy as np

ORIENT_COL = "v1_7_orientation_overlap_all_pairs"
RESCUE_COL = "certification_rescue_event"
GROUP_COLS = ["v1_7_keying", "mode", "family_semantics"]
KEYING_COL = "v1_7_keying"
SHUFFLED = "shuffled_overlap_control"
GRAPH_KEYINGS = [
    "edge_pair_signed_no_member",
    "edge_direction_only",
    "incidence_role_signed",
    "catalog_augmented_edge_pair",
]

@dataclass
class ConfoundSummary:
    version: str
    input_rows: int
    keying_count: int
    width_classes: str
    family_size_classes: str
    selector_guardrail_passed: bool
    raw_orientation_gap_rows: int
    width_matched_gap_rows: int
    graph_vs_shuffled_width_rows: int
    mean_abs_raw_gap_graph_keyings: float
    mean_abs_width_matched_gap_graph_keyings: float
    mean_abs_graph_minus_shuffled_width_gap: float
    support_width_bin_association_mean_abs: float
    family_size_bin_association_mean_abs: float
    v1_8_posture: str


def _bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["true", "1", "yes"])


def _assign_tercile_bins(df: pd.DataFrame, value_col: str = ORIENT_COL) -> pd.DataFrame:
    """Add orientation_bin per keying/mode/semantics group.

    Uses rank-based terciles to avoid qcut duplicate-edge failures in small or
    discrete groups. Labels are ordered low/medium/high. When a group has fewer
    than three distinct rank positions, bins are still assigned deterministically;
    downstream rows report the actual bin counts.
    """
    out = df.copy()
    bins = []
    for _, g in out.groupby(GROUP_COLS, dropna=False, sort=False):
        vals = g[value_col].astype(float)
        n = len(vals)
        if n == 0:
            continue
        ranks = vals.rank(method="first", ascending=True)
        # floor terciles over ranks 1..n
        idx = np.floor((ranks - 1) * 3 / max(n, 1)).astype(int).clip(0, 2)
        labels = pd.Series(np.array(["low", "medium", "high"])[idx], index=g.index)
        bins.append(labels)
    if bins:
        out["orientation_bin"] = pd.concat(bins).sort_index()
    else:
        out["orientation_bin"] = pd.Series(dtype=str)
    return out


def load_keyed_rows(input_dir: str | Path) -> pd.DataFrame:
    input_dir = Path(input_dir)
    p = input_dir / "ra_v1_7_keyed_trial_rows.csv"
    if not p.exists():
        raise FileNotFoundError(f"missing v1.7 keyed trial rows: {p}")
    df = pd.read_csv(p)
    required = {KEYING_COL, "mode", "family_semantics", ORIENT_COL, RESCUE_COL, "support_width", "family_size"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"v1.7 keyed rows missing required columns: {sorted(missing)}")
    df[RESCUE_COL] = _bool_series(df[RESCUE_COL])
    df["selector_stress_bool"] = _bool_series(df.get("selector_stress", pd.Series(False, index=df.index)))
    return _assign_tercile_bins(df)


def width_by_orientation_bin(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, g in df.groupby(GROUP_COLS + ["orientation_bin"], dropna=False):
        keying, mode, sem, bin_label = keys
        width_counts = g["support_width"].value_counts().sort_index()
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "orientation_bin": bin_label,
            "rows": len(g),
            "rescue_rate": float(g[RESCUE_COL].mean()),
            "mean_orientation_overlap": float(g[ORIENT_COL].mean()),
            "mean_support_width": float(g["support_width"].mean()),
            "support_width_min": int(g["support_width"].min()),
            "support_width_max": int(g["support_width"].max()),
            "support_width_counts": ";".join(f"{int(k)}:{int(v)}" for k, v in width_counts.items()),
            "width1_fraction": float((g["support_width"] == 1).mean()),
        })
    return pd.DataFrame(rows)


def family_size_by_orientation_bin(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, g in df.groupby(GROUP_COLS + ["orientation_bin"], dropna=False):
        keying, mode, sem, bin_label = keys
        family_counts = g["family_size"].value_counts().sort_index()
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "orientation_bin": bin_label,
            "rows": len(g),
            "rescue_rate": float(g[RESCUE_COL].mean()),
            "mean_family_size": float(g["family_size"].mean()),
            "family_size_min": int(g["family_size"].min()),
            "family_size_max": int(g["family_size"].max()),
            "family_size_counts": ";".join(f"{int(k)}:{int(v)}" for k, v in family_counts.items()),
            "singleton_family_fraction": float((g["family_size"] == 1).mean()),
        })
    return pd.DataFrame(rows)


def raw_specificity_gaps(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, g in df.groupby(GROUP_COLS, dropna=False):
        keying, mode, sem = keys
        by = g.groupby("orientation_bin")[RESCUE_COL].agg(["mean", "count"]).to_dict("index")
        low = by.get("low", {}).get("mean", np.nan)
        high = by.get("high", {}).get("mean", np.nan)
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "rows": len(g),
            "low_count": int(by.get("low", {}).get("count", 0)),
            "medium_count": int(by.get("medium", {}).get("count", 0)),
            "high_count": int(by.get("high", {}).get("count", 0)),
            "low_rescue": float(low) if not pd.isna(low) else np.nan,
            "high_rescue": float(high) if not pd.isna(high) else np.nan,
            "raw_low_minus_high_gap": float(low - high) if not (pd.isna(low) or pd.isna(high)) else np.nan,
        })
    return pd.DataFrame(rows)


def rescue_by_width_matched_bins(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, g in df.groupby(GROUP_COLS + ["support_width", "orientation_bin"], dropna=False):
        keying, mode, sem, width, bin_label = keys
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "support_width": int(width),
            "orientation_bin": bin_label,
            "rows": len(g),
            "rescue_rate": float(g[RESCUE_COL].mean()),
            "mean_family_size": float(g["family_size"].mean()),
            "mean_orientation_overlap": float(g[ORIENT_COL].mean()),
        })
    return pd.DataFrame(rows)


def orientation_gap_after_width_matching(width_bins: pd.DataFrame, raw: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    rows = []
    for keys, g in width_bins.groupby(["keying", "mode", "family_semantics"], dropna=False):
        keying, mode, sem = keys
        gaps = []
        contributing = []
        for width, wg in g.groupby("support_width"):
            pivot = wg.set_index("orientation_bin")
            if "low" in pivot.index and "high" in pivot.index:
                low = float(pivot.loc["low", "rescue_rate"])
                high = float(pivot.loc["high", "rescue_rate"])
                gaps.append(low - high)
                contributing.append(int(width))
        raw_gap = np.nan
        if raw is not None:
            r = raw[(raw["keying"] == keying) & (raw["mode"] == mode) & (raw["family_semantics"] == sem)]
            if len(r): raw_gap = float(r.iloc[0]["raw_low_minus_high_gap"])
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "raw_low_minus_high_gap": raw_gap,
            "width_matched_low_minus_high_gap": float(np.mean(gaps)) if gaps else np.nan,
            "width_matched_gap_abs": float(abs(np.mean(gaps))) if gaps else np.nan,
            "matched_width_strata_count": len(gaps),
            "matched_width_strata": ";".join(map(str, contributing)),
            "gap_removed_by_width_matching": bool((not pd.isna(raw_gap)) and gaps and abs(np.mean(gaps)) < 0.25 * abs(raw_gap)) if raw_gap != 0 else False,
            "status": "matched_width_strata_available" if gaps else "insufficient_width_matched_low_high_bins",
        })
    return pd.DataFrame(rows)


def shuffled_vs_graph_within_width(width_gap: pd.DataFrame) -> pd.DataFrame:
    rows = []
    shuf = width_gap[width_gap["keying"] == SHUFFLED]
    for _, r in width_gap[width_gap["keying"].isin(GRAPH_KEYINGS)].iterrows():
        s = shuf[(shuf["mode"] == r["mode"]) & (shuf["family_semantics"] == r["family_semantics"])]
        if len(s):
            sr = s.iloc[0]
            rows.append({
                "graph_keying": r["keying"],
                "mode": r["mode"],
                "family_semantics": r["family_semantics"],
                "graph_raw_gap": r["raw_low_minus_high_gap"],
                "shuffled_raw_gap": sr["raw_low_minus_high_gap"],
                "raw_gap_delta_graph_minus_shuffled": float(r["raw_low_minus_high_gap"] - sr["raw_low_minus_high_gap"]),
                "graph_width_matched_gap": r["width_matched_low_minus_high_gap"],
                "shuffled_width_matched_gap": sr["width_matched_low_minus_high_gap"],
                "width_matched_gap_delta_graph_minus_shuffled": float(r["width_matched_low_minus_high_gap"] - sr["width_matched_low_minus_high_gap"]) if not (pd.isna(r["width_matched_low_minus_high_gap"]) or pd.isna(sr["width_matched_low_minus_high_gap"])) else np.nan,
                "interpretation": "graph_matches_shuffled_within_width" if not pd.isna(r["width_matched_low_minus_high_gap"]) and abs(float(r["width_matched_low_minus_high_gap"] - sr["width_matched_low_minus_high_gap"])) < 0.05 else "graph_differs_or_insufficient_width_match",
            })
    return pd.DataFrame(rows)


def association_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    bin_code = {"low":0, "medium":1, "high":2}
    d=df.copy(); d["bin_code"] = d["orientation_bin"].map(bin_code).astype(float)
    for keys, g in d.groupby(GROUP_COLS, dropna=False):
        keying, mode, sem = keys
        def corr(col):
            if g[col].nunique() < 2 or g["bin_code"].nunique() < 2: return np.nan
            return float(np.corrcoef(g["bin_code"], g[col].astype(float))[0,1])
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "rows": len(g),
            "orientation_bin_support_width_corr": corr("support_width"),
            "orientation_bin_family_size_corr": corr("family_size"),
            "orientation_bin_rescue_corr": corr(RESCUE_COL),
            "low_bin_width1_fraction": float((g[g["orientation_bin"]=="low"]["support_width"] == 1).mean()) if (g["orientation_bin"]=="low").any() else np.nan,
            "high_bin_width1_fraction": float((g[g["orientation_bin"]=="high"]["support_width"] == 1).mean()) if (g["orientation_bin"]=="high").any() else np.nan,
        })
    return pd.DataFrame(rows)


def run_analysis(input_dir: str | Path, output_dir: str | Path) -> ConfoundSummary:
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    df = load_keyed_rows(input_dir)
    wb = width_by_orientation_bin(df)
    fb = family_size_by_orientation_bin(df)
    raw = raw_specificity_gaps(df)
    rbw = rescue_by_width_matched_bins(df)
    wg = orientation_gap_after_width_matching(rbw, raw)
    sg = shuffled_vs_graph_within_width(wg)
    assoc = association_summary(df)

    wb.to_csv(output_dir/"ra_v1_8_width_by_orientation_bin.csv", index=False)
    fb.to_csv(output_dir/"ra_v1_8_family_size_by_orientation_bin.csv", index=False)
    rbw.to_csv(output_dir/"ra_v1_8_rescue_by_width_matched_bins.csv", index=False)
    wg.to_csv(output_dir/"ra_v1_8_orientation_gap_after_width_matching.csv", index=False)
    sg.to_csv(output_dir/"ra_v1_8_shuffled_vs_graph_within_width.csv", index=False)
    assoc.to_csv(output_dir/"ra_v1_8_orientation_bin_association.csv", index=False)

    graph_raw = raw[raw["keying"].isin(GRAPH_KEYINGS)]
    graph_wg = wg[wg["keying"].isin(GRAPH_KEYINGS)]
    mean_abs_raw = float(graph_raw["raw_low_minus_high_gap"].abs().mean()) if len(graph_raw) else np.nan
    mean_abs_width = float(graph_wg["width_matched_low_minus_high_gap"].abs().mean()) if len(graph_wg.dropna(subset=["width_matched_low_minus_high_gap"])) else np.nan
    mean_delta_shuf = float(sg["width_matched_gap_delta_graph_minus_shuffled"].abs().mean()) if len(sg.dropna(subset=["width_matched_gap_delta_graph_minus_shuffled"])) else np.nan
    sw_corr = float(assoc[assoc["keying"].isin(GRAPH_KEYINGS)]["orientation_bin_support_width_corr"].abs().mean()) if len(assoc) else np.nan
    fs_corr = float(assoc[assoc["keying"].isin(GRAPH_KEYINGS)]["orientation_bin_family_size_corr"].abs().mean()) if len(assoc) else np.nan
    selector_ok = True
    if "selector_stress" in set(df["mode"]):
        selector_ok = bool(df[df["mode"]=="selector_stress"][RESCUE_COL].mean() == 0)
    summary = ConfoundSummary(
        version="v1.8",
        input_rows=len(df),
        keying_count=int(df[KEYING_COL].nunique()),
        width_classes=";".join(map(str, sorted(map(int, df["support_width"].dropna().unique())))),
        family_size_classes=";".join(map(str, sorted(map(int, df["family_size"].dropna().unique())))),
        selector_guardrail_passed=selector_ok,
        raw_orientation_gap_rows=len(raw),
        width_matched_gap_rows=len(wg),
        graph_vs_shuffled_width_rows=len(sg),
        mean_abs_raw_gap_graph_keyings=mean_abs_raw,
        mean_abs_width_matched_gap_graph_keyings=mean_abs_width,
        mean_abs_graph_minus_shuffled_width_gap=mean_delta_shuf,
        support_width_bin_association_mean_abs=sw_corr,
        family_size_bin_association_mean_abs=fs_corr,
        v1_8_posture="confound_audit_outputs_ready_for_canonical_v1_7_inputs",
    )
    pd.DataFrame([asdict(summary)]).to_csv(output_dir/"ra_v1_8_confound_summary.csv", index=False)
    with open(output_dir/"ra_v1_8_confound_summary.md", "w") as f:
        f.write(render_summary(summary, raw, wg, sg, assoc))
    with open(output_dir/"ra_v1_8_state.json", "w") as f:
        json.dump({"summary": asdict(summary)}, f, indent=2)
    return summary


def render_summary(summary: ConfoundSummary, raw: pd.DataFrame, wg: pd.DataFrame, sg: pd.DataFrame, assoc: pd.DataFrame) -> str:
    lines = []
    lines.append("# RA v1.8 Support-Width / Family-Structure Confound Audit\n")
    lines.append("This analysis audits whether v1.7 orientation-overlap gaps are explained by support-width, family-size, and binning structure rather than orientation-link specificity.\n")
    lines.append("## Summary metrics\n")
    for k, v in asdict(summary).items():
        lines.append(f"- **{k}**: {v}")
    lines.append("\n## Interpretation discipline\n")
    lines.append("- A persistent graph-vs-shuffled match within width/family strata supports a binning/family-structure artifact interpretation.")
    lines.append("- A graph-derived gap that survives width/family matching and differs from shuffled controls would motivate renewed orientation-specific investigation.")
    lines.append("- This packet is analysis-only and does not introduce new Lean or simulator semantics.\n")
    return "\n".join(lines) + "\n"


JOINT_STRATUM_COLS = ["mode", "family_semantics", "threshold_fraction", "severity", "support_width", "family_size"]


@dataclass
class JointConfoundSummary:
    version: str
    input_rows: int
    keying_count: int
    n_stratum_combinations: int
    n_strata_with_data: int
    n_strata_estimable_any_keying: int
    selector_guardrail_passed: bool
    mean_abs_raw_gap_graph_keyings: float
    mean_abs_width_matched_gap_graph_keyings: float
    mean_abs_joint_matched_gap_graph_keyings: float
    mean_abs_joint_matched_gap_shuffled: float
    mean_abs_graph_minus_shuffled_joint: float
    fraction_explained_by_width_graph: float
    fraction_explained_by_joint_graph: float
    estimable_strata_fraction_graph: float
    v1_8_1_posture: str


def joint_matched_gaps(df: pd.DataFrame) -> pd.DataFrame:
    """Per-stratum tertile-bin orientation gaps within
    (mode, family_semantics, threshold_fraction, severity, support_width, family_size).

    For each (keying, stratum), tertile-bin orientation_overlap and compute
    low_rescue - high_rescue if both bins are populated and have non-tied
    orientation values.
    """
    rows = []
    for keys, g in df.groupby([KEYING_COL] + JOINT_STRATUM_COLS, dropna=False, sort=False):
        keying = keys[0]; rest = keys[1:]
        n = len(g)
        if n < 3:
            estimable = False; gap = np.nan
            low_count = high_count = 0
            low_rescue = high_rescue = np.nan
        else:
            ranks = g[ORIENT_COL].rank(method="first", ascending=True)
            idx = np.floor((ranks - 1) * 3 / max(n, 1)).astype(int).clip(0, 2)
            labels = pd.Series(np.array(["low", "medium", "high"])[idx], index=g.index)
            low_mask = labels == "low"
            high_mask = labels == "high"
            low_count = int(low_mask.sum())
            high_count = int(high_mask.sum())
            if low_count == 0 or high_count == 0:
                estimable = False; gap = np.nan
                low_rescue = high_rescue = np.nan
            else:
                low_rescue = float(g.loc[low_mask, RESCUE_COL].mean())
                high_rescue = float(g.loc[high_mask, RESCUE_COL].mean())
                # Treat structurally-tied orientation as non-estimable (orientation has no variation).
                low_orient = g.loc[low_mask, ORIENT_COL].mean()
                high_orient = g.loc[high_mask, ORIENT_COL].mean()
                if abs(float(high_orient) - float(low_orient)) < 1e-12:
                    estimable = False; gap = np.nan
                else:
                    estimable = True
                    gap = low_rescue - high_rescue

        rows.append({
            "keying": keying,
            "mode": rest[0],
            "family_semantics": rest[1],
            "threshold_fraction": float(rest[2]) if rest[2] is not None and not pd.isna(rest[2]) else np.nan,
            "severity": float(rest[3]) if rest[3] is not None and not pd.isna(rest[3]) else np.nan,
            "support_width": int(rest[4]) if rest[4] is not None and not pd.isna(rest[4]) else -1,
            "family_size": int(rest[5]) if rest[5] is not None and not pd.isna(rest[5]) else -1,
            "trials": n,
            "low_count": low_count,
            "high_count": high_count,
            "low_rescue": low_rescue,
            "high_rescue": high_rescue,
            "estimable": estimable,
            "low_minus_high_gap": gap,
        })
    return pd.DataFrame(rows)


def joint_aggregate(stratum_gaps: pd.DataFrame, raw_gaps: pd.DataFrame, width_gaps: pd.DataFrame) -> pd.DataFrame:
    """Roll stratum gaps up to (keying, mode, family_semantics) with raw / width / joint side by side."""
    rows = []
    for keys, g in stratum_gaps.groupby(["keying", "mode", "family_semantics"], dropna=False):
        keying, mode, sem = keys
        est = g[g["estimable"]]
        n_strata_total = len(g)
        n_estimable = len(est)
        if n_estimable:
            joint_gap = float(est["low_minus_high_gap"].mean())
            joint_trials = int(est["trials"].sum())
        else:
            joint_gap = np.nan
            joint_trials = 0
        r = raw_gaps[(raw_gaps["keying"] == keying) & (raw_gaps["mode"] == mode) & (raw_gaps["family_semantics"] == sem)]
        w = width_gaps[(width_gaps["keying"] == keying) & (width_gaps["mode"] == mode) & (width_gaps["family_semantics"] == sem)]
        raw_gap = float(r.iloc[0]["raw_low_minus_high_gap"]) if len(r) else np.nan
        width_gap = float(w.iloc[0]["width_matched_low_minus_high_gap"]) if len(w) else np.nan
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "raw_low_minus_high_gap": raw_gap,
            "width_matched_low_minus_high_gap": width_gap,
            "joint_width_family_matched_low_minus_high_gap": joint_gap,
            "matched_strata_count": n_estimable,
            "total_strata_count": n_strata_total,
            "estimable_fraction": float(n_estimable / n_strata_total) if n_strata_total else 0.0,
            "matched_trials_count": joint_trials,
        })
    return pd.DataFrame(rows)


def graph_vs_shuffled_joint(stratum_gaps: pd.DataFrame) -> pd.DataFrame:
    """For each joint stratum, pair graph-derived keyings with the shuffled control."""
    estimable = stratum_gaps[stratum_gaps["estimable"]]
    rows = []
    pivot = (estimable
             .pivot_table(index=JOINT_STRATUM_COLS, columns="keying",
                          values="low_minus_high_gap", aggfunc="first")
             .reset_index())
    if SHUFFLED not in pivot.columns:
        return pd.DataFrame()
    for graph_key in GRAPH_KEYINGS:
        if graph_key not in pivot.columns:
            continue
        for _, r in pivot.iterrows():
            gv = r[graph_key]; sv = r[SHUFFLED]
            if pd.isna(gv) or pd.isna(sv):
                continue
            rows.append({
                "graph_keying": graph_key,
                "mode": r["mode"],
                "family_semantics": r["family_semantics"],
                "threshold_fraction": r["threshold_fraction"],
                "severity": r["severity"],
                "support_width": r["support_width"],
                "family_size": r["family_size"],
                "graph_gap": float(gv),
                "shuffled_gap": float(sv),
                "delta_graph_minus_shuffled": float(gv - sv),
            })
    return pd.DataFrame(rows)


def graph_vs_shuffled_joint_summary(detail: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, g in detail.groupby(["graph_keying", "mode", "family_semantics"], dropna=False):
        graph_keying, mode, sem = keys
        gm = float(g["graph_gap"].mean())
        sm = float(g["shuffled_gap"].mean())
        delta = float(g["delta_graph_minus_shuffled"].mean())
        if abs(delta) >= 0.05 and abs(gm) >= 0.05:
            interp = "graph_persists_after_joint_matching"
        elif abs(delta) < 0.02:
            interp = "graph_collapses_to_shuffled_after_joint_matching"
        else:
            interp = "graph_partially_distinguishable_from_shuffled"
        rows.append({
            "graph_keying": graph_keying,
            "mode": mode,
            "family_semantics": sem,
            "matched_strata_count": len(g),
            "graph_mean_gap": gm,
            "shuffled_mean_gap": sm,
            "mean_delta_graph_minus_shuffled": delta,
            "abs_delta": abs(delta),
            "interpretation": interp,
        })
    return pd.DataFrame(rows)


def estimability_by_stratum(stratum_gaps: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for keys, g in stratum_gaps.groupby(["keying", "mode", "family_semantics"], dropna=False):
        keying, mode, sem = keys
        est = g[g["estimable"]]
        rows.append({
            "keying": keying,
            "mode": mode,
            "family_semantics": sem,
            "total_strata": len(g),
            "estimable_strata": int(g["estimable"].sum()),
            "estimable_fraction": float(g["estimable"].mean()) if len(g) else 0.0,
            "estimable_trial_count": int(est["trials"].sum()) if len(est) else 0,
            "non_estimable_trial_count": int(g[~g["estimable"]]["trials"].sum()),
            "mean_trials_per_estimable_stratum": float(est["trials"].mean()) if len(est) else np.nan,
        })
    return pd.DataFrame(rows)


def gap_decomposition(joint_agg: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, r in joint_agg.iterrows():
        raw = float(r["raw_low_minus_high_gap"]) if not pd.isna(r["raw_low_minus_high_gap"]) else np.nan
        wid = float(r["width_matched_low_minus_high_gap"]) if not pd.isna(r["width_matched_low_minus_high_gap"]) else np.nan
        joint = float(r["joint_width_family_matched_low_minus_high_gap"]) if not pd.isna(r["joint_width_family_matched_low_minus_high_gap"]) else np.nan
        f_width = (raw - wid) / raw if raw not in (0.0,) and not pd.isna(wid) else np.nan
        f_joint = (raw - joint) / raw if raw not in (0.0,) and not pd.isna(joint) else np.nan
        if pd.isna(joint):
            verdict = "joint_matched_non_estimable"
        elif abs(joint) < 0.02:
            verdict = "joint_matched_gap_collapses_to_zero"
        elif abs(joint) >= 0.05:
            verdict = "joint_matched_gap_significant_residual"
        else:
            verdict = "joint_matched_gap_weak_residual"
        rows.append({
            "keying": r["keying"],
            "mode": r["mode"],
            "family_semantics": r["family_semantics"],
            "raw_gap": raw,
            "width_matched_gap": wid,
            "joint_matched_gap": joint,
            "raw_minus_width_explained": (raw - wid) if not (pd.isna(raw) or pd.isna(wid)) else np.nan,
            "raw_minus_joint_explained": (raw - joint) if not (pd.isna(raw) or pd.isna(joint)) else np.nan,
            "fraction_explained_by_width": f_width,
            "fraction_explained_by_joint": f_joint,
            "verdict": verdict,
        })
    return pd.DataFrame(rows)


def render_joint_summary(summary: JointConfoundSummary, decomp: pd.DataFrame, gvs: pd.DataFrame) -> str:
    lines = []
    lines.append("# RA v1.8.1 Joint Width × Family-Size Confound Audit\n")
    lines.append("This refines v1.8 by stratifying simultaneously on support_width AND family_size (and threshold/severity/mode/semantics).\n")
    lines.append("## Summary metrics\n")
    for k, v in asdict(summary).items():
        lines.append(f"- **{k}**: {v}")
    lines.append("\n## Per-cell decomposition (orientation_degradation)\n")
    od = decomp[decomp["mode"] == "orientation_degradation"].sort_values(["keying", "family_semantics"])
    if len(od):
        lines.append("| keying | family_semantics | raw | width-matched | joint-matched | verdict |")
        lines.append("|---|---|---|---|---|---|")
        for _, r in od.iterrows():
            def f(x): return f"{x:.4f}" if not pd.isna(x) else "n/a"
            lines.append(f"| {r['keying']} | {r['family_semantics']} | {f(r['raw_gap'])} | {f(r['width_matched_gap'])} | {f(r['joint_matched_gap'])} | {r['verdict']} |")
    lines.append("\n## Graph vs shuffled within joint strata (orientation_degradation)\n")
    od2 = gvs[gvs["mode"] == "orientation_degradation"].sort_values(["graph_keying", "family_semantics"])
    if len(od2):
        lines.append("| graph_keying | family_semantics | graph_mean | shuffled_mean | delta | interpretation |")
        lines.append("|---|---|---|---|---|---|")
        for _, r in od2.iterrows():
            def f(x): return f"{x:.4f}" if not pd.isna(x) else "n/a"
            lines.append(f"| {r['graph_keying']} | {r['family_semantics']} | {f(r['graph_mean_gap'])} | {f(r['shuffled_mean_gap'])} | {f(r['mean_delta_graph_minus_shuffled'])} | {r['interpretation']} |")
    lines.append("\n## Interpretation discipline\n")
    lines.append("- If joint-matched graph gap collapses (|gap| < 0.02), the v1.7 reversed gap is fully explained by support_width × family_size structure (Case A).")
    lines.append("- If joint-matched graph gap survives (|gap| >= 0.05) AND graph differs from shuffled in joint strata, there is a candidate residual orientation-overlap association (Case B).")
    lines.append("- If non-estimable strata dominate, a redesigned sampler is needed (Case C).")
    lines.append("- This packet remains analysis-only; nothing here is a Nature-facing claim.\n")
    return "\n".join(lines) + "\n"


def run_joint_analysis(input_dir: str | Path, output_dir: str | Path) -> JointConfoundSummary:
    """v1.8.1 entry point: joint width × family-size stratified matching."""
    output_dir = Path(output_dir); output_dir.mkdir(parents=True, exist_ok=True)
    df = load_keyed_rows(input_dir)
    raw = raw_specificity_gaps(df)
    rbw = rescue_by_width_matched_bins(df)
    wg = orientation_gap_after_width_matching(rbw, raw)

    stratum_gaps = joint_matched_gaps(df)
    joint_agg = joint_aggregate(stratum_gaps, raw, wg)
    detail_gvs = graph_vs_shuffled_joint(stratum_gaps)
    summary_gvs = graph_vs_shuffled_joint_summary(detail_gvs)
    estim = estimability_by_stratum(stratum_gaps)
    decomp = gap_decomposition(joint_agg)

    joint_agg.to_csv(output_dir / "ra_v1_8_1_joint_width_family_matched_gap.csv", index=False)
    summary_gvs.to_csv(output_dir / "ra_v1_8_1_graph_vs_shuffled_joint_matched.csv", index=False)
    estim.to_csv(output_dir / "ra_v1_8_1_estimability_by_stratum.csv", index=False)
    decomp.to_csv(output_dir / "ra_v1_8_1_orientation_gap_decomposition.csv", index=False)
    detail_gvs.to_csv(output_dir / "ra_v1_8_1_graph_vs_shuffled_joint_strata_detail.csv", index=False)

    graph_decomp = decomp[decomp["keying"].isin(GRAPH_KEYINGS)]
    shuf_joint = joint_agg[joint_agg["keying"] == SHUFFLED]
    selector_ok = bool(df[df["mode"] == "selector_stress"][RESCUE_COL].mean() == 0) if "selector_stress" in set(df["mode"]) else True
    n_strata_total = len(stratum_gaps)
    n_strata_with_data = int((stratum_gaps["trials"] >= 3).sum())
    n_strata_est_any = int(stratum_gaps[stratum_gaps["estimable"]].drop_duplicates(JOINT_STRATUM_COLS).shape[0])

    summary = JointConfoundSummary(
        version="v1.8.1",
        input_rows=len(df),
        keying_count=int(df[KEYING_COL].nunique()),
        n_stratum_combinations=n_strata_total // max(int(df[KEYING_COL].nunique()), 1),
        n_strata_with_data=n_strata_with_data,
        n_strata_estimable_any_keying=n_strata_est_any,
        selector_guardrail_passed=selector_ok,
        mean_abs_raw_gap_graph_keyings=float(graph_decomp["raw_gap"].abs().mean()) if len(graph_decomp) else np.nan,
        mean_abs_width_matched_gap_graph_keyings=float(graph_decomp["width_matched_gap"].abs().mean()) if len(graph_decomp.dropna(subset=["width_matched_gap"])) else np.nan,
        mean_abs_joint_matched_gap_graph_keyings=float(graph_decomp["joint_matched_gap"].abs().mean()) if len(graph_decomp.dropna(subset=["joint_matched_gap"])) else np.nan,
        mean_abs_joint_matched_gap_shuffled=float(shuf_joint["joint_width_family_matched_low_minus_high_gap"].abs().mean()) if len(shuf_joint.dropna(subset=["joint_width_family_matched_low_minus_high_gap"])) else np.nan,
        mean_abs_graph_minus_shuffled_joint=float(summary_gvs["abs_delta"].mean()) if len(summary_gvs) else np.nan,
        fraction_explained_by_width_graph=float(graph_decomp["fraction_explained_by_width"].mean()) if len(graph_decomp.dropna(subset=["fraction_explained_by_width"])) else np.nan,
        fraction_explained_by_joint_graph=float(graph_decomp["fraction_explained_by_joint"].mean()) if len(graph_decomp.dropna(subset=["fraction_explained_by_joint"])) else np.nan,
        estimable_strata_fraction_graph=float(estim[estim["keying"].isin(GRAPH_KEYINGS)]["estimable_fraction"].mean()) if len(estim) else np.nan,
        v1_8_1_posture="joint_width_family_matched_confound_audit_complete",
    )
    pd.DataFrame([asdict(summary)]).to_csv(output_dir / "ra_v1_8_1_joint_confound_summary.csv", index=False)
    (output_dir / "ra_v1_8_1_joint_confound_summary.md").write_text(render_joint_summary(summary, decomp, summary_gvs), encoding="utf-8")
    (output_dir / "ra_v1_8_1_state.json").write_text(json.dumps({"summary": asdict(summary)}, indent=2), encoding="utf-8")
    return summary


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--joint", action="store_true", help="Run v1.8.1 joint width x family-size matched audit")
    args = ap.parse_args()
    if args.joint:
        s = run_joint_analysis(args.input_dir, args.output_dir)
    else:
        s = run_analysis(args.input_dir, args.output_dir)
    print(json.dumps(asdict(s), indent=2))
