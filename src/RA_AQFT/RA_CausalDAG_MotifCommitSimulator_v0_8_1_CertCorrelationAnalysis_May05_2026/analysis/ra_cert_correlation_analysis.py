#!/usr/bin/env python3
"""
RA v0.8.1 certified-support-family correlation-signature analysis.

Analysis-only layer over the v0.8 Independent Certified Support Families
workbench.  It reads v0.8 output CSVs and extracts RA-native diagnostics:

  * certification-rescue decay curves over certificate correlation;
  * monotonicity of rescue under increasing certificate correlation;
  * endpoint equivalence between independent-member correlation=1.0 and
    parent-shared certification fate;
  * rescue AUC / sensitivity by mode, family semantics, threshold, severity;
  * width- and threshold-conditioned correlation signatures;
  * selector-stress guardrail preservation.

This module does not alter simulator semantics and does not introduce new Lean
objects.  It is intended to make v0.8's correlation signature auditable and
ready for canonical-run RAKB promotion.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple
import argparse
import csv
import math
import statistics

try:
    import pandas as pd
except Exception as exc:  # pragma: no cover - pandas is expected in the RA workbench env
    raise RuntimeError("v0.8.1 analysis requires pandas") from exc

CERT_MODES = ("ledger_failure", "orientation_degradation")
SELECTOR_MODE = "selector_stress"


@dataclass(frozen=True)
class CertCorrelationAnalysisConfig:
    input_dir: Path
    output_dir: Path
    certification_modes: Tuple[str, ...] = CERT_MODES
    independent_regime: str = "independent_member"
    parent_shared_regime: str = "parent_shared"
    rescue_metric: str = "certification_rescue_rate"
    resilience_metric: str = "family_certification_resilience_rate"
    endpoint_tolerance: float = 1e-9
    monotonic_tolerance: float = 1e-9
    include_user_reported_context: bool = False


@dataclass(frozen=True)
class OutputPaths:
    decay_curve: Path
    sensitivity: Path
    endpoint_equivalence: Path
    auc_by_mode: Path
    by_width_threshold: Path
    guardrail: Path
    summary_md: Path
    state_json: Path


def _read_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _safe_float(x: object, default: float = 0.0) -> float:
    try:
        if x is None:
            return default
        val = float(x)
        if math.isnan(val):
            return default
        return val
    except Exception:
        return default


def _bool_str(value: bool) -> str:
    return "true" if bool(value) else "false"


def _normalized_auc(corrs: Sequence[float], vals: Sequence[float]) -> float:
    """Trapezoidal AUC normalized to correlation interval length.

    If the correlation range has zero length, return the mean value.  The
    output is in the same units as `vals`, not multiplied by interval length.
    """
    if not corrs or not vals:
        return 0.0
    pairs = sorted((float(c), float(v)) for c, v in zip(corrs, vals))
    if len(pairs) == 1:
        return pairs[0][1]
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    width = xs[-1] - xs[0]
    if width <= 0:
        return sum(ys) / len(ys)
    area = 0.0
    for i in range(len(xs) - 1):
        dx = xs[i + 1] - xs[i]
        area += dx * (ys[i] + ys[i + 1]) / 2.0
    return area / width


def _monotone_nonincreasing(vals: Sequence[float], tol: float = 1e-9) -> bool:
    return all(vals[i + 1] <= vals[i] + tol for i in range(len(vals) - 1))


def _half_decay_correlation(corrs: Sequence[float], vals: Sequence[float]) -> Optional[float]:
    """Return first correlation where value has decayed halfway from start to endpoint.

    If start <= endpoint or there is no nontrivial decay, return None.
    """
    if not corrs or not vals:
        return None
    pairs = sorted((float(c), float(v)) for c, v in zip(corrs, vals))
    start = pairs[0][1]
    end = pairs[-1][1]
    if start <= end:
        return None
    target = end + 0.5 * (start - end)
    for c, v in pairs:
        if v <= target + 1e-12:
            return c
    return None


def _load_v08_outputs(input_dir: Path) -> Dict[str, pd.DataFrame]:
    names = {
        "summary": "ra_independent_cert_family_summary_v0_8.csv",
        "runs": "ra_independent_cert_family_runs_v0_8.csv",
        "aggregate": "ra_independent_cert_family_aggregate_v0_8.csv",
        "correlation_sweep": "ra_certification_correlation_sweep_v0_8.csv",
        "resilience_by_regime": "ra_certification_resilience_by_regime_v0_8.csv",
        "by_width": "ra_independent_cert_family_by_width_v0_8.csv",
        "selector_guardrail": "ra_independent_cert_selector_guardrail_v0_8.csv",
    }
    return {k: _read_csv_if_exists(input_dir / v) for k, v in names.items()}


def _cert_sweep_base(df: pd.DataFrame, cfg: CertCorrelationAnalysisConfig) -> pd.DataFrame:
    if df.empty:
        return df.copy()
    required = {"mode", "certification_regime", "certificate_correlation", cfg.rescue_metric}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"correlation sweep missing required columns: {sorted(missing)}")
    out = df.copy()
    out = out[out["mode"].isin(cfg.certification_modes)]
    out = out[out["certification_regime"] == cfg.independent_regime]
    out["certificate_correlation"] = out["certificate_correlation"].astype(float)
    out[cfg.rescue_metric] = out[cfg.rescue_metric].astype(float)
    if cfg.resilience_metric in out.columns:
        out[cfg.resilience_metric] = out[cfg.resilience_metric].astype(float)
    return out


def compute_decay_curve(frames: Mapping[str, pd.DataFrame], cfg: CertCorrelationAnalysisConfig) -> pd.DataFrame:
    df = _cert_sweep_base(frames["correlation_sweep"], cfg)
    if df.empty:
        return pd.DataFrame()
    keys = [c for c in ["mode", "family_semantics", "severity", "threshold_fraction"] if c in df.columns]
    # Average across any dimensions not in the curve key, notably support width if the input already
    # carries it, and across samples using sample-weighted means when possible.
    rows = []
    for group_key, g in df.groupby(keys + ["certificate_correlation"], dropna=False):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        d = dict(zip(keys + ["certificate_correlation"], group_key))
        samples = g["samples"].sum() if "samples" in g.columns else len(g)
        def wmean(col: str) -> float:
            if col not in g.columns:
                return 0.0
            if "samples" in g.columns and samples > 0:
                return float((g[col] * g["samples"]).sum() / samples)
            return float(g[col].mean())
        d.update({
            "samples": int(samples),
            "certification_rescue_rate": wmean(cfg.rescue_metric),
            "family_certification_resilience_rate": wmean(cfg.resilience_metric),
            "family_internal_loss_rate": wmean("family_internal_loss_rate"),
            "family_internal_survival_rate": wmean("family_internal_survival_rate"),
            "mean_certified_family_member_count": wmean("mean_certified_family_member_count"),
            "metric_artifact_risk_rate": wmean("metric_artifact_risk_rate"),
        })
        rows.append(d)
    return pd.DataFrame(rows).sort_values(keys + ["certificate_correlation"]).reset_index(drop=True)


def compute_sensitivity(decay: pd.DataFrame, cfg: CertCorrelationAnalysisConfig) -> pd.DataFrame:
    if decay.empty:
        return pd.DataFrame()
    keys = [c for c in ["mode", "family_semantics", "severity", "threshold_fraction"] if c in decay.columns]
    rows = []
    for group_key, g in decay.groupby(keys, dropna=False):
        if not isinstance(group_key, tuple):
            group_key = (group_key,)
        d = dict(zip(keys, group_key))
        gg = g.sort_values("certificate_correlation")
        corrs = gg["certificate_correlation"].astype(float).tolist()
        vals = gg["certification_rescue_rate"].astype(float).tolist()
        res_vals = gg["family_certification_resilience_rate"].astype(float).tolist()
        start = vals[0] if vals else 0.0
        end = vals[-1] if vals else 0.0
        d.update({
            "correlation_points": len(corrs),
            "start_correlation": corrs[0] if corrs else None,
            "end_correlation": corrs[-1] if corrs else None,
            "start_rescue_rate": start,
            "end_rescue_rate": end,
            "rescue_decay": start - end,
            "rescue_slope_over_unit_corr": (end - start) / ((corrs[-1] - corrs[0]) if corrs and corrs[-1] != corrs[0] else 1.0),
            "rescue_auc_normalized": _normalized_auc(corrs, vals),
            "resilience_auc_normalized": _normalized_auc(corrs, res_vals),
            "monotone_nonincreasing": _bool_str(_monotone_nonincreasing(vals, cfg.monotonic_tolerance)),
            "half_decay_correlation": _half_decay_correlation(corrs, vals),
            "max_step_increase": max([vals[i+1] - vals[i] for i in range(len(vals)-1)] or [0.0]),
            "mean_samples_per_point": float(gg["samples"].mean()) if "samples" in gg.columns and not gg.empty else 0.0,
        })
        rows.append(d)
    return pd.DataFrame(rows).sort_values(keys).reset_index(drop=True)


def compute_endpoint_equivalence(frames: Mapping[str, pd.DataFrame], decay: pd.DataFrame, cfg: CertCorrelationAnalysisConfig) -> pd.DataFrame:
    agg = frames["aggregate"]
    if agg.empty:
        return pd.DataFrame()
    keys = [c for c in ["mode", "family_semantics", "severity", "threshold_fraction"] if c in agg.columns]
    df = agg[agg["mode"].isin(cfg.certification_modes)].copy()
    if df.empty:
        return pd.DataFrame()
    ind = df[(df["certification_regime"] == cfg.independent_regime) & (df["certificate_correlation"].astype(float) == 1.0)]
    parent = df[df["certification_regime"] == cfg.parent_shared_regime]
    # Parent-shared rows may be repeated across certificate_correlation values; combine them.
    def weighted_group_mean(frame: pd.DataFrame, prefix: str) -> pd.DataFrame:
        rows = []
        for group_key, g in frame.groupby(keys, dropna=False):
            if not isinstance(group_key, tuple): group_key = (group_key,)
            d = dict(zip(keys, group_key))
            samples = g["samples"].sum() if "samples" in g.columns else len(g)
            for col in ["certification_rescue_rate", "family_certification_resilience_rate", "family_internal_loss_rate", "strict_parent_loss_rate"]:
                if col in g.columns:
                    if "samples" in g.columns and samples > 0:
                        d[prefix + col] = float((g[col] * g["samples"]).sum() / samples)
                    else:
                        d[prefix + col] = float(g[col].mean())
            d[prefix + "samples"] = int(samples)
            rows.append(d)
        return pd.DataFrame(rows)
    im = weighted_group_mean(ind, "independent_corr1_")
    ps = weighted_group_mean(parent, "parent_shared_")
    if im.empty or ps.empty:
        return pd.DataFrame()
    merged = im.merge(ps, on=keys, how="outer")
    for col in ["certification_rescue_rate", "family_certification_resilience_rate", "family_internal_loss_rate", "strict_parent_loss_rate"]:
        a = "independent_corr1_" + col
        b = "parent_shared_" + col
        if a in merged.columns and b in merged.columns:
            merged[col + "_delta_ind_corr1_minus_parent"] = merged[a].fillna(0.0) - merged[b].fillna(0.0)
    delta_cols = [c for c in merged.columns if c.endswith("_delta_ind_corr1_minus_parent")]
    if delta_cols:
        merged["endpoint_equivalent_within_tolerance"] = [
            _bool_str(all(abs(_safe_float(row[c])) <= cfg.endpoint_tolerance for c in delta_cols))
            for _, row in merged.iterrows()
        ]
        merged["max_abs_endpoint_delta"] = [
            max(abs(_safe_float(row[c])) for c in delta_cols)
            for _, row in merged.iterrows()
        ]
    return merged.sort_values(keys).reset_index(drop=True)


def compute_auc_by_mode(sensitivity: pd.DataFrame) -> pd.DataFrame:
    if sensitivity.empty:
        return pd.DataFrame()
    keys = [c for c in ["mode", "family_semantics"] if c in sensitivity.columns]
    rows = []
    for group_key, g in sensitivity.groupby(keys, dropna=False):
        if not isinstance(group_key, tuple): group_key = (group_key,)
        d = dict(zip(keys, group_key))
        d.update({
            "curve_count": int(len(g)),
            "all_monotone_nonincreasing": _bool_str((g["monotone_nonincreasing"] == "true").all()),
            "mean_rescue_auc": float(g["rescue_auc_normalized"].mean()),
            "mean_resilience_auc": float(g["resilience_auc_normalized"].mean()),
            "mean_rescue_decay": float(g["rescue_decay"].mean()),
            "max_rescue_decay": float(g["rescue_decay"].max()),
            "mean_start_rescue_rate": float(g["start_rescue_rate"].mean()),
            "mean_end_rescue_rate": float(g["end_rescue_rate"].mean()),
            "mean_half_decay_correlation": float(g["half_decay_correlation"].dropna().mean()) if g["half_decay_correlation"].notna().any() else None,
        })
        rows.append(d)
    return pd.DataFrame(rows).sort_values(keys).reset_index(drop=True)


def compute_by_width_threshold(frames: Mapping[str, pd.DataFrame], cfg: CertCorrelationAnalysisConfig) -> pd.DataFrame:
    df = frames["by_width"]
    if df.empty:
        return pd.DataFrame()
    df = df.copy()
    df = df[(df["mode"].isin(cfg.certification_modes)) & (df["certification_regime"] == cfg.independent_regime)]
    if df.empty:
        return pd.DataFrame()
    keys = [c for c in ["mode", "family_semantics", "severity", "threshold_fraction", "support_width"] if c in df.columns]
    rows = []
    for group_key, g in df.groupby(keys, dropna=False):
        if not isinstance(group_key, tuple): group_key = (group_key,)
        d = dict(zip(keys, group_key))
        gg = g.sort_values("certificate_correlation")
        corrs = gg["certificate_correlation"].astype(float).tolist()
        vals = gg["certification_rescue_rate"].astype(float).tolist()
        res_vals = gg["family_certification_resilience_rate"].astype(float).tolist()
        d.update({
            "correlation_points": len(corrs),
            "start_rescue_rate": vals[0] if vals else 0.0,
            "end_rescue_rate": vals[-1] if vals else 0.0,
            "rescue_decay": (vals[0] - vals[-1]) if vals else 0.0,
            "rescue_auc_normalized": _normalized_auc(corrs, vals),
            "resilience_auc_normalized": _normalized_auc(corrs, res_vals),
            "monotone_nonincreasing": _bool_str(_monotone_nonincreasing(vals, cfg.monotonic_tolerance)),
            "mean_family_size": float(gg["family_size_mean"].mean()) if "family_size_mean" in gg.columns else 0.0,
            "samples_total": int(gg["samples"].sum()) if "samples" in gg.columns else len(gg),
        })
        rows.append(d)
    return pd.DataFrame(rows).sort_values(keys).reset_index(drop=True)


def compute_selector_guardrail(frames: Mapping[str, pd.DataFrame], cfg: CertCorrelationAnalysisConfig) -> pd.DataFrame:
    guard = frames["selector_guardrail"]
    agg = frames["aggregate"]
    rows = []
    if not guard.empty:
        gd = guard.copy()
        rows.append({
            "source": "ra_independent_cert_selector_guardrail_v0_8.csv",
            "rows": len(gd),
            "selector_rows_all_guardrail_passed": _bool_str(bool((gd.get("selector_guardrail_passed", pd.Series([True])) == True).all()) if "selector_guardrail_passed" in gd.columns else True),
            "max_selector_certification_rescue_rate": float(gd.get("certification_rescue_rate", pd.Series([0.0])).max()) if "certification_rescue_rate" in gd.columns else 0.0,
            "max_selector_family_certification_resilience_rate": float(gd.get("family_certification_resilience_rate", pd.Series([0.0])).max()) if "family_certification_resilience_rate" in gd.columns else 0.0,
        })
    if not agg.empty and "mode" in agg.columns:
        sel = agg[agg["mode"] == SELECTOR_MODE]
        if not sel.empty:
            rows.append({
                "source": "aggregate_selector_rows",
                "rows": len(sel),
                "selector_rows_all_guardrail_passed": _bool_str(float(sel.get("certification_rescue_rate", pd.Series([0.0])).max()) <= cfg.endpoint_tolerance),
                "max_selector_certification_rescue_rate": float(sel.get("certification_rescue_rate", pd.Series([0.0])).max()),
                "max_selector_family_certification_resilience_rate": float(sel.get("family_certification_resilience_rate", pd.Series([0.0])).max()),
            })
    return pd.DataFrame(rows)


def build_summary_md(
    cfg: CertCorrelationAnalysisConfig,
    decay: pd.DataFrame,
    sensitivity: pd.DataFrame,
    endpoint: pd.DataFrame,
    auc_by_mode: pd.DataFrame,
    width_threshold: pd.DataFrame,
    guardrail: pd.DataFrame,
) -> str:
    def yesno(flag: bool) -> str:
        return "yes" if flag else "no"
    total_curves = len(sensitivity)
    monotone_count = int((sensitivity["monotone_nonincreasing"] == "true").sum()) if not sensitivity.empty else 0
    endpoint_count = len(endpoint)
    endpoint_ok = int((endpoint.get("endpoint_equivalent_within_tolerance", pd.Series(dtype=str)) == "true").sum()) if not endpoint.empty else 0
    max_endpoint_delta = float(endpoint.get("max_abs_endpoint_delta", pd.Series([0.0])).max()) if not endpoint.empty else 0.0
    guardrail_ok = True
    if not guardrail.empty and "selector_rows_all_guardrail_passed" in guardrail.columns:
        guardrail_ok = bool((guardrail["selector_rows_all_guardrail_passed"] == "true").all())
    top_decay_rows = []
    if not sensitivity.empty:
        top = sensitivity.sort_values("rescue_decay", ascending=False).head(8)
        for _, r in top.iterrows():
            top_decay_rows.append(
                f"- {r.get('mode')} / {r.get('family_semantics')} / severity={r.get('severity')} / "
                f"threshold={r.get('threshold_fraction')}: {r.get('start_rescue_rate'):.6g} → {r.get('end_rescue_rate'):.6g} "
                f"(decay={r.get('rescue_decay'):.6g}, monotone={r.get('monotone_nonincreasing')})"
            )
    auc_rows = []
    if not auc_by_mode.empty:
        for _, r in auc_by_mode.iterrows():
            auc_rows.append(
                f"- {r.get('mode')} / {r.get('family_semantics')}: mean rescue AUC={r.get('mean_rescue_auc'):.6g}, "
                f"mean decay={r.get('mean_rescue_decay'):.6g}, all monotone={r.get('all_monotone_nonincreasing')}"
            )
    md = f"""# RA v0.8.1 Certified-Support-Family Correlation Signature Analysis

This analysis packet consumes v0.8 Independent Certified Support Families outputs and extracts the RA-native certification-correlation signature.

## Scope

- Analysis-only packet: no simulator semantic changes and no new Lean module.
- Target quantities: certification rescue, family-internal certification resilience, endpoint equivalence, and selector-stress guardrail preservation.
- Nature-target discipline: these are RA-native simulation diagnostics, not direct claims about Nature.

## Top-line diagnostics

- Correlation decay curves analyzed: **{total_curves}**
- Monotone non-increasing curves: **{monotone_count}/{total_curves}**
- Endpoint equivalence rows: **{endpoint_ok}/{endpoint_count}** within tolerance `{cfg.endpoint_tolerance}`
- Maximum endpoint delta: **{max_endpoint_delta:.6g}**
- Selector-stress guardrail passed: **{yesno(guardrail_ok)}**

## Highest rescue-decay curves

"""
    md += "\n".join(top_decay_rows) if top_decay_rows else "No decay rows available."
    md += "\n\n## Rescue AUC by mode and family semantics\n\n"
    md += "\n".join(auc_rows) if auc_rows else "No AUC rows available."
    md += "\n\n## Interpretation\n\n"
    md += """The core v0.8 signature is strengthened when certification rescue is monotone non-increasing as certificate-correlation increases, and when the correlation=1.0 endpoint matches the parent-shared certification shape.  That pattern supports the RA-native distinction between support-route redundancy and certification-witness redundancy.

The main structural hypothesis is:

```text
member-distinct / weakly correlated certification witnesses
  → certification-channel resilience

fully shared certification fate
  → parent-shared failure shape
```

The analysis should be rerun on canonical v0.8 outputs before RAKB promotion. Packet-local outputs are demonstration artifacts unless explicitly replaced by canonical-run outputs.
"""
    return md


def write_outputs(cfg: CertCorrelationAnalysisConfig) -> OutputPaths:
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    paths = OutputPaths(
        decay_curve=cfg.output_dir / "ra_cert_rescue_decay_curve_v0_8_1.csv",
        sensitivity=cfg.output_dir / "ra_cert_correlation_sensitivity_v0_8_1.csv",
        endpoint_equivalence=cfg.output_dir / "ra_cert_endpoint_equivalence_v0_8_1.csv",
        auc_by_mode=cfg.output_dir / "ra_cert_resilience_auc_by_mode_v0_8_1.csv",
        by_width_threshold=cfg.output_dir / "ra_cert_rescue_by_width_and_threshold_v0_8_1.csv",
        guardrail=cfg.output_dir / "ra_cert_selector_guardrail_v0_8_1.csv",
        summary_md=cfg.output_dir / "ra_cert_correlation_signature_summary_v0_8_1.md",
        state_json=cfg.output_dir / "ra_cert_correlation_analysis_state_v0_8_1.json",
    )
    frames = _load_v08_outputs(cfg.input_dir)
    decay = compute_decay_curve(frames, cfg)
    sensitivity = compute_sensitivity(decay, cfg)
    endpoint = compute_endpoint_equivalence(frames, decay, cfg)
    auc = compute_auc_by_mode(sensitivity)
    bywt = compute_by_width_threshold(frames, cfg)
    guard = compute_selector_guardrail(frames, cfg)
    decay.to_csv(paths.decay_curve, index=False)
    sensitivity.to_csv(paths.sensitivity, index=False)
    endpoint.to_csv(paths.endpoint_equivalence, index=False)
    auc.to_csv(paths.auc_by_mode, index=False)
    bywt.to_csv(paths.by_width_threshold, index=False)
    guard.to_csv(paths.guardrail, index=False)
    paths.summary_md.write_text(build_summary_md(cfg, decay, sensitivity, endpoint, auc, bywt, guard), encoding="utf-8")
    # Minimal JSON state without requiring json to serialize dataframes.
    import json
    state = {
        "packet": "RA_CausalDAG_MotifCommitSimulator_v0_8_1_CertCorrelationAnalysis_May05_2026",
        "input_dir": str(cfg.input_dir),
        "output_dir": str(cfg.output_dir),
        "correlation_decay_rows": int(len(decay)),
        "sensitivity_rows": int(len(sensitivity)),
        "endpoint_equivalence_rows": int(len(endpoint)),
        "auc_rows": int(len(auc)),
        "width_threshold_rows": int(len(bywt)),
        "selector_guardrail_rows": int(len(guard)),
        "monotone_curves": int((sensitivity["monotone_nonincreasing"] == "true").sum()) if not sensitivity.empty else 0,
        "total_curves": int(len(sensitivity)),
        "max_endpoint_delta": float(endpoint.get("max_abs_endpoint_delta", pd.Series([0.0])).max()) if not endpoint.empty else 0.0,
        "selector_guardrail_passed": bool((guard.get("selector_rows_all_guardrail_passed", pd.Series(["true"])) == "true").all()) if not guard.empty else True,
    }
    paths.state_json.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    return paths


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Run RA v0.8.1 certified-support-family correlation analysis")
    parser.add_argument("--input-dir", required=True, type=Path, help="Directory containing v0.8 output CSVs")
    parser.add_argument("--output-dir", required=True, type=Path, help="Output directory for v0.8.1 analysis artifacts")
    parser.add_argument("--include-user-reported-canonical-context", action="store_true", help="Reserved flag for report annotation; does not alter calculations")
    args = parser.parse_args(argv)
    cfg = CertCorrelationAnalysisConfig(input_dir=args.input_dir, output_dir=args.output_dir, include_user_reported_context=args.include_user_reported_canonical_context)
    paths = write_outputs(cfg)
    print("RA v0.8.1 correlation analysis complete")
    for name, path in paths.__dict__.items():
        print(f"{name}: {path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
