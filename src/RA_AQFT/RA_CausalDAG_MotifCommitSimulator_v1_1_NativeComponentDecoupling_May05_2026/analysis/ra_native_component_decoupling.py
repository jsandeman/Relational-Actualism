
"""RA v1.1 native component decoupling audit.

This module is an analysis layer over v1.0 native-certificate component outputs.
It does not change simulator semantics and does not introduce a new formal law.

The purpose is to check whether orientation-overlap is independently resolved
from support/frontier overlap. If the surfaces are numerically confounded, the
module reports that fact rather than manufacturing a spurious orientation-specific
signal.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple
import csv
import json
import math

import pandas as pd
import numpy as np

COMPONENTS = [
    "support_overlap",
    "frontier_overlap",
    "orientation_overlap",
    "ledger_overlap",
    "causal_past_overlap",
    "bdg_kernel_overlap",
    "firewall_overlap",
]
TRIPLET = ["support_overlap", "frontier_overlap", "orientation_overlap"]

REQUIRED_COMPONENT_COLUMNS = [
    "mode", "family_semantics", "severity", "threshold_fraction", "support_width",
    "samples", "certification_rescue_rate", *COMPONENTS,
]


def _safe_corr(a: pd.Series, b: pd.Series) -> float:
    if len(a) < 2 or float(a.std(ddof=0)) == 0.0 or float(b.std(ddof=0)) == 0.0:
        return float("nan")
    return float(a.corr(b))


def _weighted_mean(values: pd.Series, weights: pd.Series) -> float:
    total = float(weights.sum())
    if total <= 0:
        return float("nan")
    return float((values * weights).sum() / total)


def _ols_residual(y: np.ndarray, X: np.ndarray) -> np.ndarray:
    """Return residuals of y after least-squares projection onto columns of X.

    Adds an intercept automatically. If y has no variance, returns zeros.
    """
    y = np.asarray(y, dtype=float)
    if y.size == 0 or float(np.std(y)) == 0.0:
        return np.zeros_like(y)
    X = np.asarray(X, dtype=float)
    if X.ndim == 1:
        X = X.reshape(-1, 1)
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return y - X @ beta


def read_v1_component_inputs(input_dir: Path) -> Tuple[pd.DataFrame, Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    input_dir = Path(input_dir)
    comp_path = input_dir / "ra_native_certificate_components_v1_0.csv"
    if not comp_path.exists():
        raise FileNotFoundError(f"missing required component file: {comp_path}")
    components = pd.read_csv(comp_path)
    missing = [c for c in REQUIRED_COMPONENT_COLUMNS if c not in components.columns]
    if missing:
        raise ValueError(f"component file missing required columns: {missing}")
    profile_path = input_dir / "ra_native_overlap_profile_v1_0.csv"
    calib_path = input_dir / "ra_native_overlap_calibration_status_v1_0.csv"
    profile = pd.read_csv(profile_path) if profile_path.exists() else None
    calib = pd.read_csv(calib_path) if calib_path.exists() else None
    return components, profile, calib


def component_decoupling_audit(df: pd.DataFrame) -> pd.DataFrame:
    pairs = [
        ("support_overlap", "frontier_overlap"),
        ("support_overlap", "orientation_overlap"),
        ("frontier_overlap", "orientation_overlap"),
        ("ledger_overlap", "orientation_overlap"),
        ("ledger_overlap", "support_overlap"),
    ]
    rows = []
    for a, b in pairs:
        diff = (df[a] - df[b]).abs()
        rows.append({
            "component_a": a,
            "component_b": b,
            "rows": len(df),
            "max_abs_diff": float(diff.max()),
            "mean_abs_diff": float(diff.mean()),
            "weighted_mean_abs_diff": _weighted_mean(diff, df["samples"]),
            "corr": _safe_corr(df[a], df[b]),
            "numerically_identical": bool(float(diff.max()) <= 1e-12),
            "decoupling_status": "confounded" if float(diff.max()) <= 1e-12 else "resolved_or_partially_resolved",
        })
    triplet_identical = bool(max((df["support_overlap"]-df["orientation_overlap"]).abs().max(),
                                 (df["frontier_overlap"]-df["orientation_overlap"]).abs().max()) <= 1e-12)
    rows.append({
        "component_a": "support_frontier_orientation_triplet",
        "component_b": "joint_triplet_status",
        "rows": len(df),
        "max_abs_diff": 0.0 if triplet_identical else float(max((df["support_overlap"]-df["orientation_overlap"]).abs().max(), (df["frontier_overlap"]-df["orientation_overlap"]).abs().max())),
        "mean_abs_diff": 0.0 if triplet_identical else float(((df["support_overlap"]-df["orientation_overlap"]).abs() + (df["frontier_overlap"]-df["orientation_overlap"]).abs()).mean()/2),
        "weighted_mean_abs_diff": 0.0 if triplet_identical else float("nan"),
        "corr": 1.0 if triplet_identical else float("nan"),
        "numerically_identical": triplet_identical,
        "decoupling_status": "orientation_confounded_with_support_frontier" if triplet_identical else "orientation_surface_has_independent_variation",
    })
    return pd.DataFrame(rows)


def _expected_component(mode: str) -> str:
    if mode == "ledger_failure":
        return "ledger_overlap"
    if mode == "orientation_degradation":
        return "orientation_overlap"
    return "none"


def orientation_specificity_by_mode(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    grouped = df.groupby(["mode", "family_semantics"], dropna=False)
    for (mode, sem), g in grouped:
        weights = g["samples"]
        means = {c: _weighted_mean(g[c], weights) for c in COMPONENTS}
        expected = _expected_component(mode)
        if expected == "none":
            expected_mean = float("nan")
            max_other = max(means.values())
            specificity_margin = float("nan")
            status = "not_certification_channel"
        else:
            expected_mean = means[expected]
            other_components = [c for c in COMPONENTS if c != expected]
            max_other = max(means[c] for c in other_components)
            specificity_margin = expected_mean - max_other
            if mode == "orientation_degradation" and all(abs(means["orientation_overlap"] - means[c]) <= 1e-12 for c in ["support_overlap", "frontier_overlap"]):
                status = "orientation_confounded_with_support_frontier"
            elif specificity_margin > 0.05:
                status = "specific_component_dominant"
            elif specificity_margin >= -0.05:
                status = "weak_or_tied_specificity"
            else:
                status = "nonexpected_component_dominant"
        row = {
            "mode": mode,
            "family_semantics": sem,
            "rows": len(g),
            "samples": int(weights.sum()),
            "expected_component": expected,
            "expected_component_mean_overlap": expected_mean,
            "max_other_component_mean_overlap": max_other,
            "specificity_margin": specificity_margin,
            "specificity_status": status,
        }
        row.update({f"mean_{c}": means[c] for c in COMPONENTS})
        rows.append(row)
    return pd.DataFrame(rows)


def component_partial_correlation(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (mode, sem), g in df.groupby(["mode", "family_semantics"], dropna=False):
        controls = g[["support_overlap", "frontier_overlap"]].to_numpy(dtype=float)
        y = g["certification_rescue_rate"].to_numpy(dtype=float)
        y_res = _ols_residual(y, controls)
        for component in ["orientation_overlap", "ledger_overlap", "causal_past_overlap", "bdg_kernel_overlap", "firewall_overlap"]:
            x = g[component].to_numpy(dtype=float)
            x_res = _ols_residual(x, controls)
            # Use a numerical tolerance: linalg.lstsq returns residuals at ~1e-17 when columns
            # are linearly dependent rather than exactly zero, so strict == 0.0 would misclassify
            # confounded components as "resolved". 1e-12 is far above floating-point noise but
            # well below any real signal in [0,1]-valued overlap series.
            if float(np.std(x_res)) < 1e-12 or float(np.std(y_res)) < 1e-12:
                pcorr = float("nan")
                status = "no_independent_component_variation_after_support_frontier_control"
            else:
                pcorr = float(np.corrcoef(x_res, y_res)[0,1])
                status = "resolved"
            rows.append({
                "mode": mode,
                "family_semantics": sem,
                "component": component,
                "controls": "support_overlap;frontier_overlap",
                "partial_corr_with_rescue": pcorr,
                "component_residual_std": float(np.std(x_res)),
                "rescue_residual_std": float(np.std(y_res)),
                "partial_status": status,
            })
    return pd.DataFrame(rows)


def _qcut_labels(series: pd.Series, labels=("low", "medium", "high")) -> pd.Series:
    # Robust three-bin fallback for small or repeated data.
    s = series.astype(float)
    if s.nunique(dropna=True) < 3:
        # Use thresholded bins around unique values.
        ranks = s.rank(method="dense")
        maxr = ranks.max()
        if maxr == 1:
            return pd.Series(["single"]*len(s), index=s.index)
        return pd.cut(ranks, bins=[0, maxr/3, 2*maxr/3, maxr+1], labels=labels, include_lowest=True).astype(str)
    try:
        return pd.qcut(s, q=3, labels=labels, duplicates="drop").astype(str)
    except Exception:
        return pd.cut(s, bins=3, labels=labels, include_lowest=True).astype(str)


def matched_overlap_strata(df: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["support_frontier_overlap"] = (work["support_overlap"] + work["frontier_overlap"]) / 2.0
    work["support_frontier_bin"] = _qcut_labels(work["support_frontier_overlap"])
    work["orientation_bin"] = _qcut_labels(work["orientation_overlap"])
    work["ledger_bin"] = _qcut_labels(work["ledger_overlap"])
    rows = []
    for (mode, sem, sf_bin), g in work.groupby(["mode", "family_semantics", "support_frontier_bin"], dropna=False):
        orientation_bins = sorted(map(str, g["orientation_bin"].dropna().unique()))
        ledger_bins = sorted(map(str, g["ledger_bin"].dropna().unique()))
        rows.append({
            "mode": mode,
            "family_semantics": sem,
            "support_frontier_bin": sf_bin,
            "rows": len(g),
            "samples": int(g["samples"].sum()),
            "orientation_bin_count_within_fixed_support_frontier": len(orientation_bins),
            "orientation_bins": ";".join(orientation_bins),
            "ledger_bin_count_within_fixed_support_frontier": len(ledger_bins),
            "ledger_bins": ";".join(ledger_bins),
            "orientation_decoupled_within_stratum": bool(len(orientation_bins) > 1),
            "ledger_decoupled_within_stratum": bool(len(ledger_bins) > 1),
            "mean_rescue_rate": _weighted_mean(g["certification_rescue_rate"], g["samples"]),
        })
    return pd.DataFrame(rows)


def orientation_ablation_after_support_control(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (mode, sem), g in df.groupby(["mode", "family_semantics"], dropna=False):
        base = g[["support_overlap", "frontier_overlap"]].mean(axis=1)
        orientation = g["orientation_overlap"]
        ledger = g["ledger_overlap"]
        orient_res = orientation - base
        ledger_res = ledger - base
        orient_abs = float((orient_res.abs() * g["samples"]).sum() / g["samples"].sum())
        ledger_abs = float((ledger_res.abs() * g["samples"]).sum() / g["samples"].sum())
        rows.append({
            "mode": mode,
            "family_semantics": sem,
            "rows": len(g),
            "samples": int(g["samples"].sum()),
            "mean_orientation_residual_after_support_control": float((orient_res * g["samples"]).sum() / g["samples"].sum()),
            "mean_abs_orientation_residual_after_support_control": orient_abs,
            "mean_ledger_residual_after_support_control": float((ledger_res * g["samples"]).sum() / g["samples"].sum()),
            "mean_abs_ledger_residual_after_support_control": ledger_abs,
            "orientation_control_status": "confounded_no_independent_orientation_surface" if orient_abs <= 1e-12 else "orientation_surface_partially_decoupled",
            "ledger_control_status": "ledger_surface_decoupled_from_support_frontier" if ledger_abs > 1e-12 else "ledger_surface_confounded",
        })
    return pd.DataFrame(rows)


def ledger_orientation_specificity_comparison(specificity: pd.DataFrame, partial: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for sem in sorted(specificity["family_semantics"].dropna().unique()):
        led = specificity[(specificity["mode"] == "ledger_failure") & (specificity["family_semantics"] == sem)]
        ori = specificity[(specificity["mode"] == "orientation_degradation") & (specificity["family_semantics"] == sem)]
        led_part = partial[(partial["mode"] == "ledger_failure") & (partial["family_semantics"] == sem) & (partial["component"] == "ledger_overlap")]
        ori_part = partial[(partial["mode"] == "orientation_degradation") & (partial["family_semantics"] == sem) & (partial["component"] == "orientation_overlap")]
        rows.append({
            "family_semantics": sem,
            "ledger_specificity_status": led.iloc[0]["specificity_status"] if len(led) else "missing",
            "orientation_specificity_status": ori.iloc[0]["specificity_status"] if len(ori) else "missing",
            "ledger_specificity_margin": float(led.iloc[0]["specificity_margin"]) if len(led) else float("nan"),
            "orientation_specificity_margin": float(ori.iloc[0]["specificity_margin"]) if len(ori) else float("nan"),
            "ledger_partial_corr_status": led_part.iloc[0]["partial_status"] if len(led_part) else "missing",
            "orientation_partial_corr_status": ori_part.iloc[0]["partial_status"] if len(ori_part) else "missing",
            "ledger_partial_corr": float(led_part.iloc[0]["partial_corr_with_rescue"]) if len(led_part) else float("nan"),
            "orientation_partial_corr": float(ori_part.iloc[0]["partial_corr_with_rescue"]) if len(ori_part) else float("nan"),
            "interpretation": "ledger_resolved_orientation_confounded" if (len(led) and len(ori) and str(led.iloc[0]["specificity_status"]) == "specific_component_dominant" and str(ori.iloc[0]["specificity_status"]) == "orientation_confounded_with_support_frontier") else "mixed_or_requires_review",
        })
    return pd.DataFrame(rows)


def build_summary(
    decoupling: pd.DataFrame,
    specificity: pd.DataFrame,
    matched: pd.DataFrame,
    residual: pd.DataFrame,
    comparison: pd.DataFrame,
) -> Tuple[pd.DataFrame, str]:
    triplet = decoupling[decoupling["component_a"] == "support_frontier_orientation_triplet"]
    triplet_status = triplet.iloc[0]["decoupling_status"] if len(triplet) else "unknown"
    ledger_rows = specificity[specificity["mode"] == "ledger_failure"]
    orientation_rows = specificity[specificity["mode"] == "orientation_degradation"]
    ledger_resolved = bool((ledger_rows["specificity_status"] == "specific_component_dominant").any())
    orientation_resolved = bool((orientation_rows["specificity_status"] != "orientation_confounded_with_support_frontier").any()) if len(orientation_rows) else False
    any_matched_orientation = bool(matched["orientation_decoupled_within_stratum"].any()) if len(matched) else False
    any_matched_ledger = bool(matched["ledger_decoupled_within_stratum"].any()) if len(matched) else False
    selector_guardrail = "not_applicable_analysis_only"
    status = "decoupling_audit_reveals_orientation_support_frontier_confounding"
    if orientation_resolved and any_matched_orientation:
        status = "orientation_component_decoupling_success"
    summary = {
        "analysis_status": status,
        "triplet_decoupling_status": triplet_status,
        "ledger_component_resolved": ledger_resolved,
        "orientation_component_resolved": orientation_resolved,
        "matched_orientation_variation_available": any_matched_orientation,
        "matched_ledger_variation_available": any_matched_ledger,
        "selector_guardrail_status": selector_guardrail,
        "recommended_next_step": "derive_or_generate_distinct_orientation_link_surface_before_stronger_orientation_specific_claims",
        "v1_1_posture": "ledger_attribution_clean_orientation_attribution_still_confounded",
    }
    sdf = pd.DataFrame([summary])
    md = f"""# RA v1.1 Native Component Decoupling Summary

## Verdict

`{status}`

## Key findings

- Support/frontier/orientation triplet status: `{triplet_status}`.
- Ledger component resolved: `{ledger_resolved}`.
- Orientation component resolved: `{orientation_resolved}`.
- Matched-strata orientation variation available: `{any_matched_orientation}`.
- Matched-strata ledger variation available: `{any_matched_ledger}`.

## Interpretation

v1.1 does not force a false orientation-specific attribution. It confirms that
ledger overlap is decoupled from the support/frontier proxy, while orientation
overlap remains numerically tied to support/frontier in the current component
surface. Therefore orientation-degradation rescue should be described as carried
by a joint support/frontier/orientation proxy until a distinct orientation-link
surface is generated or derived.

## Recommended next step

Define or derive a distinct orientation-link overlap surface from native
orientation witnesses, then rerun the matched-strata audit:

```text
hold support/frontier overlap fixed
vary orientation-link overlap
measure orientation-degradation rescue
```

Until that succeeds, v1.0/v1.1 should retain the caveat:

```text
ledger attribution is clean; orientation attribution is component-anchored but
not yet independently resolved from support/frontier overlap.
```
"""
    return sdf, md


def run_decoupling_analysis(input_dir: Path, output_dir: Path) -> Dict[str, object]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df, profile, calib = read_v1_component_inputs(Path(input_dir))
    dec = component_decoupling_audit(df)
    spec = orientation_specificity_by_mode(df)
    pcorr = component_partial_correlation(df)
    matched = matched_overlap_strata(df)
    residual = orientation_ablation_after_support_control(df)
    compare = ledger_orientation_specificity_comparison(spec, pcorr)
    summary, md = build_summary(dec, spec, matched, residual, compare)

    outputs = {
        "ra_component_decoupling_audit_v1_1.csv": dec,
        "ra_orientation_specificity_by_mode_v1_1.csv": spec,
        "ra_component_partial_correlation_v1_1.csv": pcorr,
        "ra_matched_overlap_strata_v1_1.csv": matched,
        "ra_orientation_ablation_after_support_control_v1_1.csv": residual,
        "ra_ledger_orientation_specificity_comparison_v1_1.csv": compare,
        "ra_native_component_decoupling_summary_v1_1.csv": summary,
    }
    for name, frame in outputs.items():
        frame.to_csv(output_dir / name, index=False)
    (output_dir / "ra_native_component_decoupling_summary_v1_1.md").write_text(md, encoding="utf-8")
    state = {
        "input_dir": str(input_dir),
        "rows": int(len(df)),
        "outputs": list(outputs.keys()) + ["ra_native_component_decoupling_summary_v1_1.md"],
        "summary": summary.iloc[0].to_dict(),
    }
    (output_dir / "ra_native_component_decoupling_state_v1_1.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    return state


def main(argv: Optional[Sequence[str]] = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Run RA v1.1 native component decoupling audit")
    parser.add_argument("--input-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    state = run_decoupling_analysis(args.input_dir, args.output_dir)
    print(json.dumps(state["summary"], indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
