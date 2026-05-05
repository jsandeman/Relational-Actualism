#!/usr/bin/env python3
"""
RA causal-DAG motif-commit ensemble analysis v0.5.2.

This module consumes v0.5.1 large-ensemble output CSVs and extracts
RA-native causal-severance signatures. It is intentionally analysis-only:
it does not alter simulator semantics, Lean formalizations, or RAKB registry
state.

Core objects analyzed:
  - severance mode
  - severity tier
  - support/readiness/strict-commit/selected-commit loss rates
  - finality-depth shift
  - recovery length
  - support-width fragility

The analysis avoids inherited-theory target language. The operational question is:
Which causal-support disruptions produce distinct actualization-fragility profiles?
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple
import argparse
import csv
import json
import math
import statistics

LOSS_METRICS = [
    "support_loss_rate",
    "readiness_loss_rate",
    "strict_commit_loss_rate",
    "selected_commit_loss_rate",
]
AUX_METRICS = ["mean_finality_depth_shift", "mean_recovery_length"]
ALL_SIGNATURE_METRICS = LOSS_METRICS + AUX_METRICS

MODE_INTERPRETATIONS = {
    "edge_dropout": "reachability-structure disruption; may destroy or delay support reachability",
    "frontier_dropout": "direct support-frontier removal; destroys support evidence at the cut",
    "support_delay": "support remains certified but reaches the site only later, shifting finality/recovery depth",
    "orientation_degradation": "orientation-support witness failure; certification loss without a separate reachability story",
    "ledger_failure": "local ledger gate failure; support certification is blocked at the witness layer",
    "selector_stress": "compatibility/selector-channel stress; strict commitment can fail while selected commitment survives",
}


def _parse_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return value
    s = str(value).strip()
    if s == "" or s.lower() in {"nan", "none", "null"}:
        return None
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False
    try:
        if any(ch in s for ch in [".", "e", "E"]):
            return float(s)
        return int(s)
    except ValueError:
        return s


def read_csv_rows(path: Path) -> List[Dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [{k: _parse_scalar(v) for k, v in row.items()} for row in reader]


def write_csv_rows(path: Path, rows: Sequence[Dict[str, Any]], fieldnames: Optional[Sequence[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: List[str] = []
        seen = set()
        for row in rows:
            for k in row.keys():
                if k not in seen:
                    seen.add(k)
                    keys.append(k)
        fieldnames = keys
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _format_scalar(row.get(k)) for k in fieldnames})


def _format_scalar(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return f"{value:.6f}"
    return value


def grouped(rows: Iterable[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    out: Dict[Any, List[Dict[str, Any]]] = {}
    for row in rows:
        out.setdefault(row.get(key), []).append(row)
    return out


def finite_values(rows: Iterable[Dict[str, Any]], metric: str) -> List[float]:
    vals: List[float] = []
    for row in rows:
        v = row.get(metric)
        if isinstance(v, bool):
            vals.append(1.0 if v else 0.0)
        elif isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(float(v)):
            vals.append(float(v))
    return vals


def mean_or_none(vals: Sequence[float]) -> Optional[float]:
    return statistics.fmean(vals) if vals else None


def range_or_none(vals: Sequence[float]) -> Optional[float]:
    return (max(vals) - min(vals)) if vals else None


def stdev_or_zero(vals: Sequence[float]) -> float:
    return statistics.pstdev(vals) if len(vals) > 1 else 0.0


def saturation_score(vals: Sequence[float]) -> Optional[float]:
    """Return 1.0 for perfectly flat nonzero response; lower for graded response.

    This intentionally measures *severity saturation*, not empirical truth.
    Constant near-zero responses are scored separately by the caller.
    """
    if not vals:
        return None
    mean = abs(statistics.fmean(vals))
    spread = max(vals) - min(vals)
    if mean < 1e-12:
        return 1.0 if spread < 1e-12 else 0.0
    return max(0.0, min(1.0, 1.0 - spread / max(mean, 1e-12)))


def monotone_positive_score(points: Sequence[Tuple[float, float]]) -> Optional[float]:
    """Crude monotonicity score for severity -> value, in [0,1]."""
    pts = [(float(x), float(y)) for x, y in points if math.isfinite(float(y))]
    if len(pts) <= 1:
        return None
    pts.sort()
    steps = 0
    positive = 0
    for (_, y0), (_, y1) in zip(pts, pts[1:]):
        steps += 1
        if y1 >= y0 - 1e-12:
            positive += 1
    return positive / steps if steps else None


def response_class(loss_saturation: Optional[float], nonzero_loss_mean: float,
                   finality_monotone: Optional[float], finality_range: Optional[float]) -> str:
    if nonzero_loss_mean < 0.05:
        if finality_range is not None and finality_range > 0.5 and (finality_monotone or 0.0) >= 0.75:
            return "graded_delay_without_support_loss"
        return "low_loss_or_control_like"
    if loss_saturation is not None and loss_saturation >= 0.90:
        return "threshold_saturating_loss"
    if finality_range is not None and finality_range > 0.5 and (finality_monotone or 0.0) >= 0.75:
        return "mixed_loss_with_graded_finality_shift"
    return "graded_or_mixed_loss"


def primary_failure_channel(metric_means: Dict[str, float]) -> str:
    support = metric_means.get("support_loss_rate", 0.0)
    ready = metric_means.get("readiness_loss_rate", 0.0)
    strict = metric_means.get("strict_commit_loss_rate", 0.0)
    selected = metric_means.get("selected_commit_loss_rate", 0.0)
    if support > 0.5 and abs(support - ready) < 0.1 and abs(ready - selected) < 0.1:
        return "support_certification_or_frontier_loss"
    if support < 0.05 and ready > 0.5 and strict > 0.5 and selected > 0.5:
        return "readiness_delay_without_support_loss"
    if support < 0.05 and ready < 0.05 and strict > 0.5 and selected < 0.05:
        return "strict_commit_incompatibility_channel"
    if strict > ready + 0.2:
        return "strict_commit_exclusion_excess"
    return "mixed_actualization_fragility"


def summarize_modes(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for mode, rows in sorted(grouped(aggregate_rows, "mode").items()):
        nonzero = [r for r in rows if isinstance(r.get("severity"), (int, float)) and float(r["severity"]) > 0.0]
        metric_means: Dict[str, float] = {}
        metric_ranges: Dict[str, Optional[float]] = {}
        metric_sats: Dict[str, Optional[float]] = {}
        for metric in LOSS_METRICS:
            vals = finite_values(nonzero, metric)
            metric_means[metric] = mean_or_none(vals) or 0.0
            metric_ranges[metric] = range_or_none(vals)
            metric_sats[metric] = saturation_score(vals)
        loss_mean_avg = statistics.fmean(metric_means[m] for m in LOSS_METRICS)
        sat_vals = [v for v in metric_sats.values() if v is not None]
        loss_sat = statistics.fmean(sat_vals) if sat_vals else None
        finality_vals = finite_values(nonzero, "mean_finality_depth_shift")
        recovery_vals = finite_values(nonzero, "mean_recovery_length")
        finality_points = []
        for r in nonzero:
            sev = r.get("severity")
            y = r.get("mean_finality_depth_shift")
            if isinstance(sev, (int, float)) and isinstance(y, (int, float)) and math.isfinite(float(y)):
                finality_points.append((float(sev), float(y)))
        finality_mon = monotone_positive_score(finality_points)
        finality_range = range_or_none(finality_vals)
        channel = primary_failure_channel(metric_means)
        cls = response_class(loss_sat, loss_mean_avg, finality_mon, finality_range)
        # Refine generic saturation by the RA-native failure channel. A mode can
        # have loss rates that saturate across severity while still carrying a
        # graded finality/recovery signature, especially support_delay.
        if channel == "readiness_delay_without_support_loss" and finality_range is not None and finality_range > 0.5 and (finality_mon or 0.0) >= 0.75:
            cls = "graded_delay_without_support_loss"
        elif channel == "strict_commit_incompatibility_channel" and loss_sat is not None and loss_sat >= 0.90:
            cls = "strict_channel_threshold_saturation"
        elif channel == "support_certification_or_frontier_loss" and loss_sat is not None and loss_sat >= 0.90:
            cls = "threshold_saturating_support_loss"
        out.append({
            "mode": mode,
            "samples_nonzero_total": sum(int(r.get("samples") or 0) for r in nonzero),
            "support_loss_mean_nonzero": metric_means["support_loss_rate"],
            "readiness_loss_mean_nonzero": metric_means["readiness_loss_rate"],
            "strict_commit_loss_mean_nonzero": metric_means["strict_commit_loss_rate"],
            "selected_commit_loss_mean_nonzero": metric_means["selected_commit_loss_rate"],
            "loss_saturation_score": loss_sat,
            "support_loss_range_nonzero": metric_ranges["support_loss_rate"],
            "readiness_loss_range_nonzero": metric_ranges["readiness_loss_rate"],
            "strict_commit_loss_range_nonzero": metric_ranges["strict_commit_loss_rate"],
            "selected_commit_loss_range_nonzero": metric_ranges["selected_commit_loss_rate"],
            "finality_shift_mean_nonzero": mean_or_none(finality_vals),
            "finality_shift_range_nonzero": finality_range,
            "finality_shift_monotone_score": finality_mon,
            "recovery_length_mean_nonzero": mean_or_none(recovery_vals),
            "recovery_length_range_nonzero": range_or_none(recovery_vals),
            "response_class": cls,
            "primary_failure_channel": channel,
            "ra_interpretation": MODE_INTERPRETATIONS.get(str(mode), "unclassified RA-native severance mode"),
        })
    return out


def mode_severity_rows(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for r in aggregate_rows:
        mode = r.get("mode")
        severity = float(r.get("severity") or 0.0)
        loss_vals = [float(r.get(m) or 0.0) for m in LOSS_METRICS]
        support, ready, strict, selected = loss_vals
        if support > 0.5 and ready > 0.5 and selected > 0.5:
            channel = "support/readiness/commit loss"
        elif support < 0.05 and ready > 0.5:
            channel = "readiness/commit loss without support loss"
        elif support < 0.05 and ready < 0.05 and strict > 0.5 and selected < 0.05:
            channel = "strict-only incompatibility loss"
        elif max(loss_vals) < 0.05:
            channel = "control/no-loss"
        else:
            channel = "mixed"
        rows.append({
            "mode": mode,
            "severity": severity,
            "samples": r.get("samples"),
            "support_loss_rate": r.get("support_loss_rate"),
            "readiness_loss_rate": r.get("readiness_loss_rate"),
            "strict_commit_loss_rate": r.get("strict_commit_loss_rate"),
            "selected_commit_loss_rate": r.get("selected_commit_loss_rate"),
            "mean_finality_depth_shift": r.get("mean_finality_depth_shift"),
            "mean_recovery_length": r.get("mean_recovery_length"),
            "dominant_channel": channel,
        })
    return rows


def support_width_summary(fragility_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    by_width = grouped(fragility_rows, "support_width")
    for width, rows in sorted(by_width.items(), key=lambda kv: (999999 if kv[0] is None else float(kv[0]))):
        nonzero = [r for r in rows if isinstance(r.get("severity"), (int, float)) and float(r["severity"]) > 0.0]
        out.append({
            "support_width": width,
            "rows": len(rows),
            "samples_total": sum(int(r.get("samples") or 0) for r in rows),
            "nonzero_samples_total": sum(int(r.get("samples") or 0) for r in nonzero),
            "lost_support_rate_mean_nonzero": mean_or_none(finite_values(nonzero, "lost_support_rate")),
            "lost_readiness_rate_mean_nonzero": mean_or_none(finite_values(nonzero, "lost_readiness_rate")),
            "lost_strict_commit_rate_mean_nonzero": mean_or_none(finite_values(nonzero, "lost_strict_commit_rate")),
            "lost_selected_commit_rate_mean_nonzero": mean_or_none(finite_values(nonzero, "lost_selected_commit_rate")),
            "mean_recovery_length_nonzero": mean_or_none(finite_values(nonzero, "mean_recovery_length")),
            "mean_finality_depth_shift_nonzero": mean_or_none(finite_values(nonzero, "mean_finality_depth_shift")),
        })
    return out


def pairwise_mode_separability(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_mode = grouped([r for r in aggregate_rows if isinstance(r.get("severity"), (int, float)) and float(r["severity"]) > 0.0], "mode")
    signatures: Dict[Any, List[float]] = {}
    for mode, rows in by_mode.items():
        # Flatten sorted severity vectors for stable comparison. None is imputed as 0 and noted in report.
        rows_sorted = sorted(rows, key=lambda r: float(r.get("severity") or 0.0))
        vec: List[float] = []
        for r in rows_sorted:
            for m in ALL_SIGNATURE_METRICS:
                v = r.get(m)
                vec.append(float(v) if isinstance(v, (int, float)) and math.isfinite(float(v)) else 0.0)
        signatures[mode] = vec
    modes = sorted(signatures)
    out: List[Dict[str, Any]] = []
    for i, a in enumerate(modes):
        for b in modes[i+1:]:
            va, vb = signatures[a], signatures[b]
            n = min(len(va), len(vb))
            if n == 0:
                dist = None
                cosine = None
            else:
                dist = math.sqrt(sum((va[j] - vb[j]) ** 2 for j in range(n)))
                na = math.sqrt(sum(va[j] ** 2 for j in range(n)))
                nb = math.sqrt(sum(vb[j] ** 2 for j in range(n)))
                cosine = sum(va[j] * vb[j] for j in range(n)) / (na * nb) if na > 0 and nb > 0 else None
            out.append({
                "mode_a": a,
                "mode_b": b,
                "euclidean_signature_distance": dist,
                "cosine_similarity": cosine,
                "separability_note": _separability_note(dist, cosine),
            })
    return out


def _separability_note(distance: Optional[float], cosine: Optional[float]) -> str:
    if distance is None:
        return "insufficient_signature_data"
    if cosine is not None and cosine > 0.98 and distance < 0.25:
        return "nearly_degenerate_signature"
    if distance > 3.0:
        return "strongly_separated_signature"
    if distance > 1.0:
        return "moderately_separated_signature"
    return "weakly_separated_signature"


def finality_shift_rows(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for mode, rows in sorted(grouped(aggregate_rows, "mode").items()):
        rows_sorted = sorted(rows, key=lambda r: float(r.get("severity") or 0.0))
        vals = finite_values(rows_sorted, "mean_finality_depth_shift")
        points = []
        for r in rows_sorted:
            sev = r.get("severity")
            shift = r.get("mean_finality_depth_shift")
            if isinstance(sev, (int, float)) and isinstance(shift, (int, float)) and math.isfinite(float(shift)):
                points.append((float(sev), float(shift)))
        out.append({
            "mode": mode,
            "severity_values": ";".join(str(r.get("severity")) for r in rows_sorted),
            "mean_finality_shift_all": mean_or_none(vals),
            "range_finality_shift_all": range_or_none(vals),
            "monotone_score": monotone_positive_score(points),
            "classification": _finality_class(points),
        })
    return out


def recovery_rows(aggregate_rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for mode, rows in sorted(grouped(aggregate_rows, "mode").items()):
        vals = finite_values(rows, "mean_recovery_length")
        out.append({
            "mode": mode,
            "mean_recovery_length_all": mean_or_none(vals),
            "range_recovery_length_all": range_or_none(vals),
            "nonzero_recovery_values": ";".join(str(r.get("mean_recovery_length")) for r in rows if r.get("mean_recovery_length") is not None),
            "classification": _recovery_class(vals),
        })
    return out


def _finality_class(points: Sequence[Tuple[float, float]]) -> str:
    if not points:
        return "undefined_or_destroyed_support"
    nonzero = [(s, v) for s, v in points if s > 0]
    vals = [v for _, v in nonzero]
    if not vals:
        return "control_only"
    rng = max(vals) - min(vals)
    mon = monotone_positive_score(nonzero) or 0.0
    if rng > 1.0 and mon >= 0.75 and statistics.fmean(vals) > 0:
        return "graded_positive_finality_shift"
    if statistics.fmean(vals) < -0.5:
        return "negative_or_earlier_finality_after_intervention"
    if abs(statistics.fmean(vals)) < 0.1 and rng < 0.25:
        return "no_material_finality_shift"
    return "mixed_finality_shift"


def _recovery_class(vals: Sequence[float]) -> str:
    if not vals:
        return "undefined_recovery"
    mean = statistics.fmean(vals)
    rng = max(vals) - min(vals)
    if mean == 0 and rng == 0:
        return "no_recovery_delay"
    if rng > 1:
        return "graded_recovery_delay"
    return "bounded_recovery_delay"


def make_markdown_summary(
    output_dir: Path,
    summary_rows: Sequence[Dict[str, Any]],
    separability_rows: Sequence[Dict[str, Any]],
    support_width_rows: Sequence[Dict[str, Any]],
    run_summary: Optional[Dict[str, Any]] = None,
    user_reported_context: Optional[Dict[str, Any]] = None,
) -> str:
    lines: List[str] = []
    lines.append("# RA v0.5.2 Ensemble Severance-Signature Summary")
    lines.append("")
    lines.append("This analysis is RA-native: it classifies causal-support disruption profiles, not inherited-theory formalisms.")
    lines.append("")
    if run_summary:
        lines.append("## Analyzed run summary")
        for k in ["version", "run_count", "steps", "workers", "actual_evaluations", "sampled_evaluations", "elapsed_seconds", "evaluations_per_second"]:
            if k in run_summary:
                lines.append(f"- {k}: {run_summary[k]}")
        lines.append("")
    if user_reported_context:
        lines.append("## User-reported canonical large-run context")
        lines.append("These values were supplied by the local run operator and are not independently reconstructed from packet-local files here.")
        for k, v in user_reported_context.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
    lines.append("## Mode signatures")
    for row in summary_rows:
        lines.append(f"### {row['mode']}")
        lines.append(f"- response_class: {row['response_class']}")
        lines.append(f"- primary_failure_channel: {row['primary_failure_channel']}")
        lines.append(f"- loss_saturation_score: {_format_scalar(row.get('loss_saturation_score'))}")
        lines.append(f"- finality_shift_mean_nonzero: {_format_scalar(row.get('finality_shift_mean_nonzero'))}")
        lines.append(f"- recovery_length_mean_nonzero: {_format_scalar(row.get('recovery_length_mean_nonzero'))}")
        lines.append(f"- RA interpretation: {row['ra_interpretation']}")
        lines.append("")
    lines.append("## Pairwise mode separability")
    top = sorted(separability_rows, key=lambda r: float(r.get("euclidean_signature_distance") or 0.0), reverse=True)[:10]
    for row in top:
        lines.append(
            f"- {row['mode_a']} vs {row['mode_b']}: distance={_format_scalar(row.get('euclidean_signature_distance'))}, "
            f"cosine={_format_scalar(row.get('cosine_similarity'))}, note={row['separability_note']}"
        )
    lines.append("")
    lines.append("## Support-width fragility")
    if len(support_width_rows) <= 1:
        lines.append("Only one support width appears in the analyzed output. This prevents a genuine support-width fragility curve; v0.6-level simulator development should increase support-frontier width diversity.")
    for row in support_width_rows:
        lines.append(
            f"- support_width={row.get('support_width')}: lost_readiness_mean_nonzero="
            f"{_format_scalar(row.get('lost_readiness_rate_mean_nonzero'))}, samples={row.get('samples_total')}"
        )
    lines.append("")
    lines.append("## Candidate RA-native findings")
    lines.append("1. Threshold-like severance signatures are visible when nonzero severity tiers produce nearly constant loss rates.")
    lines.append("2. Support-delay signatures are separable when support loss remains low while readiness/commit loss and finality/recovery shift increase.")
    lines.append("3. Selector-stress signatures are separable when strict commitment fails without support/readiness/selected-commit loss.")
    lines.append("4. Support-width fragility cannot yet be strongly assessed unless the ensemble contains multiple support-frontier widths.")
    lines.append("")
    out = "\n".join(lines)
    (output_dir / "ra_severance_signature_summary_v0_5_2.md").write_text(out, encoding="utf-8")
    return out


def analyze(input_dir: Path, output_dir: Path, include_user_context: bool = False) -> Dict[str, Any]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    aggregate_path = input_dir / "ra_causal_dag_ensemble_aggregate_v0_5_1.csv"
    fragility_path = input_dir / "ra_causal_dag_ensemble_fragility_v0_5_1.csv"
    summary_path = input_dir / "ra_causal_dag_ensemble_summary_v0_5_1.csv"

    aggregate_rows = read_csv_rows(aggregate_path)
    fragility_rows = read_csv_rows(fragility_path) if fragility_path.exists() else []
    run_summary_rows = read_csv_rows(summary_path) if summary_path.exists() else []
    run_summary = run_summary_rows[0] if run_summary_rows else None

    mode_rows = mode_severity_rows(aggregate_rows)
    summary_rows = summarize_modes(aggregate_rows)
    width_rows = support_width_summary(fragility_rows)
    sep_rows = pairwise_mode_separability(aggregate_rows)
    finality_rows = finality_shift_rows(aggregate_rows)
    rec_rows = recovery_rows(aggregate_rows)

    write_csv_rows(output_dir / "ra_fragility_by_mode_and_severity_v0_5_2.csv", mode_rows)
    write_csv_rows(output_dir / "ra_severance_mode_signatures_v0_5_2.csv", summary_rows)
    write_csv_rows(output_dir / "ra_fragility_by_support_width_v0_5_2.csv", width_rows)
    write_csv_rows(output_dir / "ra_mode_separability_scores_v0_5_2.csv", sep_rows)
    write_csv_rows(output_dir / "ra_finality_shift_by_mode_v0_5_2.csv", finality_rows)
    write_csv_rows(output_dir / "ra_recovery_length_by_mode_v0_5_2.csv", rec_rows)

    user_context = None
    if include_user_context:
        user_context = {
            "run_count": "100 seeds (17-117)",
            "steps": 32,
            "workers": 4,
            "actual_evaluations": 120000,
            "sampled_evaluations": 5000,
            "wall_time_seconds": 60.13,
            "throughput_eval_per_second": 1996,
            "aggregate_losses": "support=62081; readiness=77617; strict_commit=93153; selected_commit=77617",
            "reported_saturation": "edge_dropout, frontier_dropout, and ledger_failure saturate near 0.971 at all nonzero severity tiers",
        }
    md = make_markdown_summary(output_dir, summary_rows, sep_rows, width_rows, run_summary, user_context)

    state = {
        "version": "0.5.2",
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "aggregate_rows": len(aggregate_rows),
        "fragility_rows": len(fragility_rows),
        "mode_count": len(summary_rows),
        "support_width_count": len(width_rows),
        "separability_pairs": len(sep_rows),
        "outputs": [
            "ra_fragility_by_mode_and_severity_v0_5_2.csv",
            "ra_severance_mode_signatures_v0_5_2.csv",
            "ra_fragility_by_support_width_v0_5_2.csv",
            "ra_mode_separability_scores_v0_5_2.csv",
            "ra_finality_shift_by_mode_v0_5_2.csv",
            "ra_recovery_length_by_mode_v0_5_2.csv",
            "ra_severance_signature_summary_v0_5_2.md",
        ],
    }
    (output_dir / "ra_ensemble_analysis_state_v0_5_2.json").write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")
    return state


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Analyze RA v0.5.1 causal-severance ensemble outputs.")
    p.add_argument("--input-dir", required=True, type=Path, help="Directory containing v0.5.1 output CSVs")
    p.add_argument("--output-dir", required=True, type=Path, help="Directory for v0.5.2 analysis outputs")
    p.add_argument("--include-user-reported-100-seed-context", action="store_true", help="Include user-reported 100-seed run context in the markdown summary")
    args = p.parse_args(argv)
    state = analyze(args.input_dir, args.output_dir, include_user_context=args.include_user_reported_100_seed_context)
    print(json.dumps(state, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
