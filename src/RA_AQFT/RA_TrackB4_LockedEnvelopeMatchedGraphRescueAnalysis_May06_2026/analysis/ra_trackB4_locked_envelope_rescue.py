"""Track B.4 locked-envelope matched-graph orientation-rescue analysis.

This module is deliberately narrow.  It analyzes only the B.3b coverage
candidate envelope:

    keying = incidence_role_signed
    family_semantics = augmented_exact_k
    threshold_fraction = 0.25

It optionally compares the locked graph-derived keying to shuffled_overlap_control.
It does not create an orientation-rescue claim unless the supplied inputs contain
rescue-event columns and v1.8.1-style fixed-bin joint support_width x family_size
strata are estimable.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional, Sequence
import json
import math

import pandas as pd
import numpy as np

LOCKED_KEYING = "incidence_role_signed"
CONTROL_KEYING = "shuffled_overlap_control"
LOCKED_FAMILY_SEMANTICS = "augmented_exact_k"
LOCKED_THRESHOLD = 0.25
LEGITIMATE_KEYINGS = {LOCKED_KEYING}

RESCUE_COLUMNS = [
    "certification_rescue_event",
    "strict_rescue_event",
    "family_certification_resilience_event",
    "family_internal_survival",
]
OVERLAP_CANDIDATES = [
    "orientation_overlap",
    "v1_7_orientation_overlap_all_pairs",
    "v1_6_graph_coupled_orientation_overlap",
    "graph_cut_orientation_overlap",
]
KEYING_CANDIDATES = ["keying", "v1_7_keying", "orientation_keying"]


@dataclass
class B4Summary:
    input_rows: int
    locked_envelope_rows: int
    graph_rows: int
    control_rows: int
    rescue_column_used: str
    overlap_column_used: str
    estimable_joint_strata_graph: int
    estimable_joint_strata_control: int
    graph_mean_joint_gap: float | None
    control_mean_joint_gap: float | None
    graph_minus_control_gap: float | None
    selector_guardrail_passed: bool
    orientation_rescue_claim_made: bool
    posture: str


def _find_col(df: pd.DataFrame, candidates: Sequence[str]) -> Optional[str]:
    for c in candidates:
        if c in df.columns:
            return c
    return None


def _as_bool_series(s: pd.Series) -> pd.Series:
    if s.dtype == bool:
        return s
    if pd.api.types.is_numeric_dtype(s):
        return s.fillna(0).astype(float) != 0
    return s.astype(str).str.lower().isin(["true", "1", "yes", "y"])


def load_rows(input_dirs: Sequence[Path], explicit_files: Sequence[Path] | None = None) -> pd.DataFrame:
    """Load candidate trial rows from directories/files.

    Preference is given to files likely to contain trial-level data.  Coverage-only
    files are allowed but downstream validation will mark them not analyzable if
    rescue columns are absent.
    """
    paths: List[Path] = []
    if explicit_files:
        paths.extend([Path(p) for p in explicit_files])
    for d in input_dirs:
        d = Path(d)
        if not d.exists():
            continue
        for name in [
            "ra_v1_7_keyed_trial_rows.csv",
            "ra_trackB3b_sampler_sweep.csv",
            "ra_trackB2_active_graph_orientation_overlap.csv",
            "ra_v1_6_graph_coupled_orientation_trials.csv",
        ]:
            p = d / name
            if p.exists():
                paths.append(p)
        # Fallback: any CSV with trial/keyed/sampler in name.
        for p in d.glob("*.csv"):
            lname = p.name.lower()
            if any(k in lname for k in ["trial", "keyed", "sampler_sweep"]):
                if p not in paths:
                    paths.append(p)
    frames = []
    for p in paths:
        try:
            df = pd.read_csv(p)
        except Exception:
            continue
        df["source_file"] = p.name
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    # Normalize only intersecting/union columns via concat sort=False.
    return pd.concat(frames, ignore_index=True, sort=False)


def normalize_rows(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    out = df.copy()
    keying_col = _find_col(out, KEYING_CANDIDATES)
    if keying_col is None:
        out["keying"] = "unknown"
    else:
        out["keying"] = out[keying_col]
        # Coalesce remaining candidate columns to fill NaN rows from sources that
        # ship `v1_7_keying` (v1.7) alongside `keying` (B.3b sweeps).
        for c in KEYING_CANDIDATES:
            if c != keying_col and c in out.columns:
                out["keying"] = out["keying"].fillna(out[c])
    overlap_col = _find_col(out, OVERLAP_CANDIDATES)
    if overlap_col is None:
        out["orientation_overlap_value"] = np.nan
    else:
        out["orientation_overlap_value"] = pd.to_numeric(out[overlap_col], errors="coerce")
        for c in OVERLAP_CANDIDATES:
            if c != overlap_col and c in out.columns:
                out["orientation_overlap_value"] = out["orientation_overlap_value"].fillna(
                    pd.to_numeric(out[c], errors="coerce")
                )
    # Required dimensions with safe defaults.
    for col, default in [
        ("family_semantics", "unknown"),
        ("threshold_fraction", np.nan),
        ("mode", "unknown"),
        ("severity", np.nan),
        ("support_width", np.nan),
        ("family_size", np.nan),
    ]:
        if col not in out.columns:
            out[col] = default
    out["threshold_fraction"] = pd.to_numeric(out["threshold_fraction"], errors="coerce")
    out["support_width"] = pd.to_numeric(out["support_width"], errors="coerce")
    out["family_size"] = pd.to_numeric(out["family_size"], errors="coerce")
    out["severity"] = pd.to_numeric(out["severity"], errors="coerce")

    rescue_col = _find_col(out, RESCUE_COLUMNS)
    if rescue_col:
        out["rescue_event"] = _as_bool_series(out[rescue_col])
    else:
        out["rescue_event"] = np.nan
    # selector guardrail column may not be present; infer from selector mode if possible.
    if "mode" in out.columns and "rescue_event" in out.columns:
        selector = out[out["mode"] == "selector_stress"]
        guardrail = True if selector.empty else (selector["rescue_event"].fillna(False).astype(bool).sum() == 0)
    else:
        guardrail = True
    out.attrs["rescue_column_used"] = rescue_col or "NONE"
    out.attrs["overlap_column_used"] = overlap_col or "NONE"
    out.attrs["selector_guardrail_passed"] = bool(guardrail)
    return out


def locked_envelope(df: pd.DataFrame, include_control: bool = True) -> pd.DataFrame:
    keys = [LOCKED_KEYING]
    if include_control:
        keys.append(CONTROL_KEYING)
    mask = (
        df["keying"].isin(keys)
        & (df["family_semantics"] == LOCKED_FAMILY_SEMANTICS)
        & (np.isclose(df["threshold_fraction"], LOCKED_THRESHOLD, equal_nan=False))
    )
    return df.loc[mask].copy()


def assign_fixed_bins(df: pd.DataFrame) -> pd.DataFrame:
    """Assign fixed low/medium/high bins within mode/keying/semantics/severity.

    We keep bins fixed for subsequent width/family controls; we do not re-bin
    inside joint strata.
    """
    if df.empty:
        df = df.copy(); df["orientation_bin_fixed"] = pd.Series(dtype=str); return df
    out = df.copy()
    out["orientation_bin_fixed"] = "insufficient"
    group_cols = ["keying", "mode", "family_semantics", "threshold_fraction", "severity"]
    for _, idx in out.groupby(group_cols, dropna=False).groups.items():
        vals = out.loc[idx, "orientation_overlap_value"].astype(float)
        nonnan = vals.dropna()
        if nonnan.nunique() < 3:
            # still try binary if two unique values; otherwise single_bin.
            if nonnan.nunique() == 2:
                q1 = nonnan.min(); q2 = nonnan.max()
                bins = pd.Series("medium", index=idx)
                bins.loc[vals.index[vals <= q1]] = "low"
                bins.loc[vals.index[vals >= q2]] = "high"
                out.loc[idx, "orientation_bin_fixed"] = bins
            else:
                out.loc[idx, "orientation_bin_fixed"] = "single_bin"
            continue
        q_low = nonnan.quantile(1/3)
        q_high = nonnan.quantile(2/3)
        out.loc[idx, "orientation_bin_fixed"] = np.where(
            vals <= q_low, "low", np.where(vals >= q_high, "high", "medium")
        )
    return out


def aggregate_fixed_gaps(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if df.empty or "rescue_event" not in df.columns:
        return pd.DataFrame(rows)
    group_cols = ["keying", "mode", "family_semantics", "threshold_fraction", "severity"]
    for keys, g in df.groupby(group_cols, dropna=False):
        rates = g.groupby("orientation_bin_fixed")["rescue_event"].mean()
        counts = g.groupby("orientation_bin_fixed").size()
        low = rates.get("low", np.nan); high = rates.get("high", np.nan)
        rows.append(dict(zip(group_cols, keys)) | {
            "rows": len(g),
            "low_rows": int(counts.get("low", 0)),
            "high_rows": int(counts.get("high", 0)),
            "low_rescue_rate": low,
            "high_rescue_rate": high,
            "low_minus_high_gap": (low - high) if pd.notna(low) and pd.notna(high) else np.nan,
            "estimable_fixed_gap": int(counts.get("low", 0)) > 0 and int(counts.get("high", 0)) > 0,
        })
    return pd.DataFrame(rows)


def joint_stratum_gaps(df: pd.DataFrame, min_rows_per_bin: int = 25) -> pd.DataFrame:
    rows = []
    if df.empty:
        return pd.DataFrame(rows)
    group_cols = [
        "keying", "mode", "family_semantics", "threshold_fraction", "severity",
        "support_width", "family_size"
    ]
    for keys, g in df.groupby(group_cols, dropna=False):
        counts = g.groupby("orientation_bin_fixed").size()
        rates = g.groupby("orientation_bin_fixed")["rescue_event"].mean()
        low_n = int(counts.get("low", 0)); high_n = int(counts.get("high", 0))
        low = rates.get("low", np.nan); high = rates.get("high", np.nan)
        estimable = low_n >= min_rows_per_bin and high_n >= min_rows_per_bin
        rows.append(dict(zip(group_cols, keys)) | {
            "rows": len(g),
            "low_rows": low_n,
            "high_rows": high_n,
            "medium_rows": int(counts.get("medium", 0)),
            "low_rescue_rate": low,
            "high_rescue_rate": high,
            "low_minus_high_gap": (low - high) if pd.notna(low) and pd.notna(high) else np.nan,
            "estimable_joint_stratum": estimable,
            "min_rows_per_bin": min_rows_per_bin,
        })
    return pd.DataFrame(rows)


def weighted_joint_gap(joint: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if joint.empty:
        return pd.DataFrame(rows)
    est = joint[joint["estimable_joint_stratum"]].copy()
    group_cols = ["keying", "mode", "family_semantics", "threshold_fraction", "severity"]
    for keys, g in est.groupby(group_cols, dropna=False):
        weights = g["low_rows"] + g["high_rows"]
        gap = float(np.average(g["low_minus_high_gap"], weights=weights)) if weights.sum() else np.nan
        rows.append(dict(zip(group_cols, keys)) | {
            "estimable_joint_strata": len(g),
            "matched_rows": int(weights.sum()),
            "weighted_joint_low_minus_high_gap": gap,
            "matched_widths": ";".join(map(lambda x: str(int(x)) if pd.notna(x) else "nan", sorted(g["support_width"].dropna().unique()))),
            "matched_family_sizes": ";".join(map(lambda x: str(int(x)) if pd.notna(x) else "nan", sorted(g["family_size"].dropna().unique()))),
        })
    return pd.DataFrame(rows)


def graph_vs_control(weighted: pd.DataFrame) -> pd.DataFrame:
    rows = []
    if weighted.empty:
        return pd.DataFrame(rows)
    graph = weighted[weighted["keying"] == LOCKED_KEYING]
    ctrl = weighted[weighted["keying"] == CONTROL_KEYING]
    join_cols = ["mode", "family_semantics", "threshold_fraction", "severity"]
    merged = graph.merge(ctrl, on=join_cols, how="outer", suffixes=("_graph", "_control"))
    for _, r in merged.iterrows():
        gg = r.get("weighted_joint_low_minus_high_gap_graph", np.nan)
        cg = r.get("weighted_joint_low_minus_high_gap_control", np.nan)
        rows.append({
            **{c: r[c] for c in join_cols},
            "graph_gap": gg,
            "control_gap": cg,
            "graph_minus_control_gap": gg - cg if pd.notna(gg) and pd.notna(cg) else np.nan,
            "graph_estimable_joint_strata": r.get("estimable_joint_strata_graph", 0),
            "control_estimable_joint_strata": r.get("estimable_joint_strata_control", 0),
            "verdict": _verdict(gg, cg),
        })
    return pd.DataFrame(rows)


def _verdict(graph_gap, control_gap, tol=0.03) -> str:
    if pd.isna(graph_gap):
        return "graph_not_estimable"
    if pd.isna(control_gap):
        return "control_not_estimable"
    if abs(graph_gap - control_gap) <= tol:
        return "graph_matches_control_no_specific_signal"
    if graph_gap > control_gap + tol:
        return "graph_more_positive_than_control_candidate_signal"
    if graph_gap < control_gap - tol:
        return "graph_more_negative_than_control_candidate_signal"
    return "indeterminate"


def power_coverage(joint: pd.DataFrame) -> pd.DataFrame:
    if joint.empty:
        return pd.DataFrame()
    cols = ["keying", "mode", "family_semantics", "threshold_fraction", "severity"]
    rows=[]
    for keys,g in joint.groupby(cols, dropna=False):
        rows.append(dict(zip(cols, keys)) | {
            "joint_strata": len(g),
            "estimable_joint_strata": int(g["estimable_joint_stratum"].sum()),
            "estimable_fraction": float(g["estimable_joint_stratum"].mean()) if len(g) else 0.0,
            "total_rows": int(g["rows"].sum()),
            "estimable_rows": int((g.loc[g["estimable_joint_stratum"], "low_rows"] + g.loc[g["estimable_joint_stratum"], "high_rows"]).sum()) if g["estimable_joint_stratum"].any() else 0,
        })
    return pd.DataFrame(rows)


def run_analysis(input_dirs: Sequence[Path], output_dir: Path, explicit_files: Sequence[Path] | None = None, min_rows_per_bin: int = 25) -> B4Summary:
    output_dir.mkdir(parents=True, exist_ok=True)
    raw = load_rows(input_dirs, explicit_files)
    norm = normalize_rows(raw)
    rescue_col = norm.attrs.get("rescue_column_used", "NONE")
    overlap_col = norm.attrs.get("overlap_column_used", "NONE")
    selector_guardrail = norm.attrs.get("selector_guardrail_passed", True)
    if norm.empty or "keying" not in norm.columns:
        env = pd.DataFrame()
    else:
        env = locked_envelope(norm, include_control=True)

    if env.empty or rescue_col == "NONE" or overlap_col == "NONE":
        # Write minimal outputs and explain non-estimability.
        env.to_csv(output_dir / "ra_trackB4_locked_envelope_trials.csv", index=False)
        pd.DataFrame().to_csv(output_dir / "ra_trackB4_fixed_bin_gaps.csv", index=False)
        pd.DataFrame().to_csv(output_dir / "ra_trackB4_joint_stratum_gaps.csv", index=False)
        pd.DataFrame().to_csv(output_dir / "ra_trackB4_graph_vs_shuffled_controls.csv", index=False)
        pd.DataFrame().to_csv(output_dir / "ra_trackB4_power_coverage.csv", index=False)
        posture = "not_estimable_missing_locked_envelope_or_required_rescue_overlap_columns"
        summary = B4Summary(
            input_rows=len(norm), locked_envelope_rows=len(env),
            graph_rows=int((env.get("keying", pd.Series(dtype=str)) == LOCKED_KEYING).sum()) if not env.empty else 0,
            control_rows=int((env.get("keying", pd.Series(dtype=str)) == CONTROL_KEYING).sum()) if not env.empty else 0,
            rescue_column_used=rescue_col, overlap_column_used=overlap_col,
            estimable_joint_strata_graph=0, estimable_joint_strata_control=0,
            graph_mean_joint_gap=None, control_mean_joint_gap=None, graph_minus_control_gap=None,
            selector_guardrail_passed=selector_guardrail, orientation_rescue_claim_made=False,
            posture=posture,
        )
        _write_summary(output_dir, summary)
        return summary

    env = assign_fixed_bins(env)
    fixed = aggregate_fixed_gaps(env)
    joint = joint_stratum_gaps(env, min_rows_per_bin=min_rows_per_bin)
    weighted = weighted_joint_gap(joint)
    gvc = graph_vs_control(weighted)
    cov = power_coverage(joint)

    env.to_csv(output_dir / "ra_trackB4_locked_envelope_trials.csv", index=False)
    fixed.to_csv(output_dir / "ra_trackB4_fixed_bin_gaps.csv", index=False)
    joint.to_csv(output_dir / "ra_trackB4_joint_stratum_gaps.csv", index=False)
    weighted.to_csv(output_dir / "ra_trackB4_width_family_matched_gap.csv", index=False)
    gvc.to_csv(output_dir / "ra_trackB4_graph_vs_shuffled_controls.csv", index=False)
    cov.to_csv(output_dir / "ra_trackB4_power_coverage.csv", index=False)

    if weighted.empty or "keying" not in weighted.columns:
        graph_w = pd.DataFrame()
        ctrl_w = pd.DataFrame()
    else:
        graph_w = weighted[weighted["keying"] == LOCKED_KEYING]
        ctrl_w = weighted[weighted["keying"] == CONTROL_KEYING]
    graph_gap = float(graph_w["weighted_joint_low_minus_high_gap"].mean()) if not graph_w.empty else None
    ctrl_gap = float(ctrl_w["weighted_joint_low_minus_high_gap"].mean()) if not ctrl_w.empty else None
    delta = (graph_gap - ctrl_gap) if graph_gap is not None and ctrl_gap is not None else None
    graph_est = int(graph_w["estimable_joint_strata"].sum()) if not graph_w.empty else 0
    ctrl_est = int(ctrl_w["estimable_joint_strata"].sum()) if not ctrl_w.empty else 0
    # We still do not make a claim; we report candidate verdict only.
    if graph_est == 0:
        posture = "locked_envelope_not_estimable_under_joint_strata"
    elif ctrl_est == 0:
        posture = "graph_estimable_control_not_estimable_locked_envelope_candidate_only"
    else:
        # a cautious posture based on controls
        if delta is not None and abs(delta) > 0.03:
            posture = "locked_envelope_candidate_residual_association_requires_review"
        else:
            posture = "locked_envelope_graph_matches_control_no_specific_signal"
    summary = B4Summary(
        input_rows=len(norm), locked_envelope_rows=len(env),
        graph_rows=int((env["keying"] == LOCKED_KEYING).sum()),
        control_rows=int((env["keying"] == CONTROL_KEYING).sum()),
        rescue_column_used=rescue_col, overlap_column_used=overlap_col,
        estimable_joint_strata_graph=graph_est, estimable_joint_strata_control=ctrl_est,
        graph_mean_joint_gap=graph_gap, control_mean_joint_gap=ctrl_gap, graph_minus_control_gap=delta,
        selector_guardrail_passed=selector_guardrail,
        orientation_rescue_claim_made=False,
        posture=posture,
    )
    _write_summary(output_dir, summary, gvc)
    return summary


def _write_summary(output_dir: Path, summary: B4Summary, gvc: Optional[pd.DataFrame]=None) -> None:
    pd.DataFrame([asdict(summary)]).to_csv(output_dir / "ra_trackB4_summary.csv", index=False)
    lines = [
        "# Track B.4 locked-envelope matched-graph rescue analysis",
        "",
        "This packet analyzes only the B.3b narrow envelope:",
        "",
        f"- keying: `{LOCKED_KEYING}`",
        f"- family semantics: `{LOCKED_FAMILY_SEMANTICS}`",
        f"- threshold fraction: `{LOCKED_THRESHOLD}`",
        "",
        "It compares graph-derived incidence-role-signed orientation overlap against shuffled controls under fixed-bin, joint support-width × family-size discipline.",
        "",
        "## Summary",
        "",
    ]
    for k,v in asdict(summary).items():
        lines.append(f"- {k}: {v}")
    lines += [
        "",
        "## Guardrail",
        "",
        "`orientation_rescue_claim_made` is always false in this packet. B.4 reports a locked-envelope candidate diagnostic only; registry promotion requires human review and must not generalize beyond the B.3b envelope.",
    ]
    if gvc is not None and not gvc.empty:
        lines += ["", "## Graph vs shuffled controls", ""]
        lines.append(gvc.to_markdown(index=False))
    (output_dir / "ra_trackB4_locked_envelope_summary.md").write_text("\n".join(lines))


def make_demo_rows() -> pd.DataFrame:
    rows=[]
    rng=np.random.default_rng(123)
    keyings=[LOCKED_KEYING, CONTROL_KEYING]
    modes=["orientation_degradation","ledger_failure","selector_stress"]
    # Construct two estimable strata for orientation degradation, with a graph-specific residual.
    for keying in keyings:
        for mode in modes:
            for width,fam in [(2,4),(3,4)]:
                for bin_name, oval in [("low",0.15),("high",0.85)]:
                    for i in range(40):
                        if mode == "selector_stress":
                            rescue=False
                        elif keying == LOCKED_KEYING and mode == "orientation_degradation":
                            # high overlap has lower rescue; low-high positive.
                            p=0.35 if bin_name=="low" else 0.10
                            rescue=bool(rng.random()<p)
                        elif keying == CONTROL_KEYING and mode == "orientation_degradation":
                            p=0.20
                            rescue=bool(rng.random()<p)
                        elif mode == "ledger_failure":
                            p=0.18
                            rescue=bool(rng.random()<p)
                        else:
                            rescue=False
                        rows.append({
                            "keying":keying,"mode":mode,"family_semantics":LOCKED_FAMILY_SEMANTICS,
                            "threshold_fraction":LOCKED_THRESHOLD,"severity":0.5,
                            "support_width":width,"family_size":fam,
                            "orientation_overlap": oval + rng.normal(0,0.02),
                            "certification_rescue_event":rescue,
                            "source_file":"demo",
                        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    out=Path("outputs")
    demo=make_demo_rows()
    p=Path("_demo_rows.csv"); demo.to_csv(p,index=False)
    run_analysis([], out, [p])
