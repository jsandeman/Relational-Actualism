#!/usr/bin/env python3
"""RA v0.9.1 native certificate-overlap robustness analysis.

This module is an analysis-only layer over the v0.9 native certificate-overlap
workbench. It does not change simulator semantics. It tests whether the v0.9
native-overlap signature survives component ablation and overlap-weight changes,
and whether the native-overlap-induced curve aligns qualitatively with the
explicit-correlation baseline from v0.8.1 when those files are supplied.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple

COMPONENTS: Tuple[str, ...] = (
    "support", "frontier", "orientation", "ledger", "causal_past", "bdg_kernel", "firewall"
)

BASE_WEIGHTS: Mapping[str, float] = {
    "support": 0.18,
    "frontier": 0.16,
    "orientation": 0.18,
    "ledger": 0.18,
    "causal_past": 0.12,
    "bdg_kernel": 0.10,
    "firewall": 0.08,
}

WEIGHT_PROFILES: Mapping[str, Mapping[str, float]] = {
    "balanced": BASE_WEIGHTS,
    "support_frontier_heavy": {
        "support": 0.30, "frontier": 0.25, "orientation": 0.10, "ledger": 0.10,
        "causal_past": 0.10, "bdg_kernel": 0.08, "firewall": 0.07,
    },
    "ledger_heavy": {
        "support": 0.08, "frontier": 0.08, "orientation": 0.10, "ledger": 0.42,
        "causal_past": 0.10, "bdg_kernel": 0.10, "firewall": 0.12,
    },
    "orientation_heavy": {
        "support": 0.08, "frontier": 0.08, "orientation": 0.42, "ledger": 0.10,
        "causal_past": 0.10, "bdg_kernel": 0.10, "firewall": 0.12,
    },
    "bdg_firewall_heavy": {
        "support": 0.08, "frontier": 0.08, "orientation": 0.12, "ledger": 0.12,
        "causal_past": 0.14, "bdg_kernel": 0.28, "firewall": 0.18,
    },
    "causal_past_heavy": {
        "support": 0.10, "frontier": 0.10, "orientation": 0.12, "ledger": 0.12,
        "causal_past": 0.36, "bdg_kernel": 0.10, "firewall": 0.10,
    },
}


def _float(x: object, default: float = 0.0) -> float:
    if x is None:
        return default
    s = str(x).strip()
    if s == "":
        return default
    try:
        return float(s)
    except ValueError:
        return default


def _int(x: object, default: int = 0) -> int:
    try:
        return int(float(str(x).strip()))
    except Exception:
        return default


def _bool(x: object) -> bool:
    return str(x).strip().lower() in {"true", "1", "yes", "y"}


def _clip01(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def overlap_bin(value: float) -> str:
    v = _clip01(value)
    if v < 1.0 / 3.0:
        return "low"
    if v < 2.0 / 3.0:
        return "medium"
    return "high"


def read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})


def normalize_weights(weights: Mapping[str, float]) -> Dict[str, float]:
    raw = {c: max(0.0, float(weights.get(c, 0.0))) for c in COMPONENTS}
    total = sum(raw.values())
    if total <= 0:
        return dict(BASE_WEIGHTS)
    return {k: v / total for k, v in raw.items()}


def ablated_weights(component: str) -> Dict[str, float]:
    w = dict(BASE_WEIGHTS)
    if component != "none":
        w[component] = 0.0
    return normalize_weights(w)


def component_value(row: Mapping[str, str], component: str) -> float:
    # v0.9 component rows use mean_<component>_overlap, while sample rows use <component>_overlap.
    return _float(row.get(f"mean_{component}_overlap", row.get(f"{component}_overlap", 0.0)))


def weighted_overlap(row: Mapping[str, str], weights: Mapping[str, float]) -> float:
    w = normalize_weights(weights)
    return _clip01(sum(w[c] * component_value(row, c) for c in COMPONENTS))


def weighted_rate(rows: Sequence[Mapping[str, str]], rate_field: str) -> float:
    total = sum(max(0, _int(r.get("samples", 1), 1)) for r in rows)
    if total <= 0:
        return 0.0
    return sum(max(0, _int(r.get("samples", 1), 1)) * _float(r.get(rate_field, 0.0)) for r in rows) / total


def sum_samples(rows: Sequence[Mapping[str, str]]) -> int:
    return sum(max(0, _int(r.get("samples", 1), 1)) for r in rows)


def group_by(rows: Iterable[Mapping[str, str]], keys: Sequence[str]) -> Dict[Tuple[str, ...], List[Mapping[str, str]]]:
    out: Dict[Tuple[str, ...], List[Mapping[str, str]]] = defaultdict(list)
    for r in rows:
        out[tuple(str(r.get(k, "")) for k in keys)].append(r)
    return out


def bin_rates(rows: Sequence[Mapping[str, str]], weights: Mapping[str, float], rate_field: str = "certification_rescue_rate") -> Dict[str, object]:
    buckets: Dict[str, List[Mapping[str, str]]] = {"low": [], "medium": [], "high": []}
    for r in rows:
        buckets[overlap_bin(weighted_overlap(r, weights))].append(r)
    rates = {b: (weighted_rate(buckets[b], rate_field) if buckets[b] else None) for b in ["low", "medium", "high"]}
    samples = {b: sum_samples(buckets[b]) for b in ["low", "medium", "high"]}
    present = [b for b in ["low", "medium", "high"] if rates[b] is not None]
    monotone = True
    ordered_rates = [rates[b] for b in ["low", "medium", "high"] if rates[b] is not None]
    for a, b in zip(ordered_rates, ordered_rates[1:]):
        if a + 1e-12 < b:
            monotone = False
            break
    low_high_gap = None
    if rates["low"] is not None and rates["high"] is not None:
        low_high_gap = rates["low"] - rates["high"]
    mean_overlap = 0.0
    total = sum_samples(rows)
    if total:
        mean_overlap = sum(max(0, _int(r.get("samples", 1), 1)) * weighted_overlap(r, weights) for r in rows) / total
    return {
        "low_rate": rates["low"], "medium_rate": rates["medium"], "high_rate": rates["high"],
        "low_samples": samples["low"], "medium_samples": samples["medium"], "high_samples": samples["high"],
        "bin_count": len(present), "monotone_low_to_high": monotone, "low_high_gap": low_high_gap,
        "mean_weighted_overlap": mean_overlap,
    }


def fmt(x: object) -> object:
    if x is None:
        return ""
    if isinstance(x, float):
        return round(x, 6)
    return x


def component_ablation(component_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    grouped = group_by(component_rows, ["mode", "family_semantics"])
    for ablation in ("none",) + COMPONENTS:
        weights = ablated_weights(ablation)
        for (mode, sem), rows in sorted(grouped.items()):
            br = bin_rates(rows, weights)
            out.append({
                "analysis": "component_ablation",
                "ablated_component": ablation,
                "mode": mode,
                "family_semantics": sem,
                "samples": sum_samples(rows),
                "low_rate": fmt(br["low_rate"]),
                "medium_rate": fmt(br["medium_rate"]),
                "high_rate": fmt(br["high_rate"]),
                "low_samples": br["low_samples"],
                "medium_samples": br["medium_samples"],
                "high_samples": br["high_samples"],
                "bin_count": br["bin_count"],
                "monotone_low_to_high": br["monotone_low_to_high"],
                "low_high_gap": fmt(br["low_high_gap"]),
                "mean_weighted_overlap": fmt(br["mean_weighted_overlap"]),
            })
    return out


def weight_sensitivity(component_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    grouped = group_by(component_rows, ["mode", "family_semantics"])
    for profile, weights in WEIGHT_PROFILES.items():
        for (mode, sem), rows in sorted(grouped.items()):
            br = bin_rates(rows, weights)
            out.append({
                "analysis": "weight_sensitivity",
                "weight_profile": profile,
                "mode": mode,
                "family_semantics": sem,
                "samples": sum_samples(rows),
                "low_rate": fmt(br["low_rate"]),
                "medium_rate": fmt(br["medium_rate"]),
                "high_rate": fmt(br["high_rate"]),
                "low_samples": br["low_samples"],
                "medium_samples": br["medium_samples"],
                "high_samples": br["high_samples"],
                "bin_count": br["bin_count"],
                "monotone_low_to_high": br["monotone_low_to_high"],
                "low_high_gap": fmt(br["low_high_gap"]),
                "mean_weighted_overlap": fmt(br["mean_weighted_overlap"]),
            })
    return out


def signal_attribution(ablation_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    baseline: Dict[Tuple[str, str], float] = {}
    for r in ablation_rows:
        if r.get("ablated_component") == "none":
            try: baseline[(str(r["mode"]), str(r["family_semantics"]))] = float(r.get("low_high_gap") or 0.0)
            except Exception: baseline[(str(r["mode"]), str(r["family_semantics"]))] = 0.0
    out = []
    for r in ablation_rows:
        comp = str(r.get("ablated_component"))
        if comp == "none":
            continue
        key = (str(r.get("mode")), str(r.get("family_semantics")))
        base_gap = baseline.get(key, 0.0)
        try: gap = float(r.get("low_high_gap") or 0.0)
        except Exception: gap = 0.0
        out.append({
            "mode": key[0],
            "family_semantics": key[1],
            "component": comp,
            "baseline_low_high_gap": round(base_gap, 6),
            "ablated_low_high_gap": round(gap, 6),
            "component_importance_score": round(base_gap - gap, 6),
            "interpretation": "positive_score_means_component_removal_weakened_low_high_rescue_gap",
        })
    return sorted(out, key=lambda r: (r["mode"], r["family_semantics"], -abs(float(r["component_importance_score"]))))


def external_correlation_alignment(native_rows: Sequence[Mapping[str, str]], external_dir: Optional[Path]) -> List[Dict[str, object]]:
    native_grouped = group_by(native_rows, ["mode", "family_semantics"])
    external_auc = {}
    external_available = False
    if external_dir:
        auc_rows = read_csv(external_dir / "ra_cert_resilience_auc_by_mode_v0_8_1.csv")
        for r in auc_rows:
            external_available = True
            external_auc[(str(r.get("mode")), str(r.get("family_semantics")))] = {
                "external_mean_rescue_auc": _float(r.get("mean_rescue_auc")),
                "external_mean_rescue_decay": _float(r.get("mean_rescue_decay")),
                "external_all_monotone": _bool(r.get("all_monotone_nonincreasing")),
            }
    out: List[Dict[str, object]] = []
    for key, rows in sorted(native_grouped.items()):
        # approximate native AUC using bins sorted by induced correlation.
        pts = []
        for r in rows:
            pts.append((_float(r.get("mean_induced_certificate_correlation")), _float(r.get("certification_rescue_rate")), _int(r.get("samples", 1), 1)))
        if not pts:
            continue
        # collapse duplicate correlation bins by weighted average.
        bins: Dict[float, List[Tuple[float,int]]] = defaultdict(list)
        for corr, rate, samp in pts:
            bins[round(corr, 3)].append((rate, samp))
        curve = []
        for corr, vals in bins.items():
            total = sum(s for _, s in vals)
            rate = sum(rate*s for rate, s in vals) / total if total else 0.0
            curve.append((corr, rate))
        curve.sort()
        auc = 0.0
        if len(curve) >= 2:
            lo, hi = curve[0][0], curve[-1][0]
            width = hi - lo
            if width > 0:
                for (x1,y1),(x2,y2) in zip(curve, curve[1:]):
                    auc += (x2-x1)*(y1+y2)/2
                auc /= width
        start = curve[0][1] if curve else 0.0
        end = curve[-1][1] if curve else 0.0
        decay = start - end
        ext = external_auc.get(key, {})
        out.append({
            "mode": key[0],
            "family_semantics": key[1],
            "native_point_count": len(curve),
            "native_rescue_auc_proxy": round(auc, 6),
            "native_rescue_decay_proxy": round(decay, 6),
            "external_available": bool(external_available and key in external_auc),
            "external_mean_rescue_auc": round(float(ext.get("external_mean_rescue_auc", 0.0)), 6) if ext else "",
            "external_mean_rescue_decay": round(float(ext.get("external_mean_rescue_decay", 0.0)), 6) if ext else "",
            "external_all_monotone": ext.get("external_all_monotone", "") if ext else "",
            "auc_difference_native_minus_external": round(auc - float(ext.get("external_mean_rescue_auc", 0.0)), 6) if ext else "",
            "decay_difference_native_minus_external": round(decay - float(ext.get("external_mean_rescue_decay", 0.0)), 6) if ext else "",
        })
    return out


def endpoint_audit(overlap_vs_parent_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    out = []
    grouped = group_by(overlap_vs_parent_rows, ["mode", "family_semantics", "severity", "threshold_fraction", "native_overlap_bin"])
    for key, rows in sorted(grouped.items()):
        samples = len(rows)
        native_rescue = sum(_float(r.get("native_certification_rescue_rate")) for r in rows)/samples if samples else 0.0
        parent_rescue = sum(_float(r.get("parent_shared_certification_rescue_rate")) for r in rows)/samples if samples else 0.0
        native_resilience = sum(_float(r.get("native_family_certification_resilience_rate")) for r in rows)/samples if samples else 0.0
        parent_resilience = sum(_float(r.get("parent_shared_family_certification_resilience_rate")) for r in rows)/samples if samples else 0.0
        out.append({
            "mode": key[0], "family_semantics": key[1], "severity": key[2], "threshold_fraction": key[3], "native_overlap_bin": key[4],
            "native_certification_rescue_rate": round(native_rescue, 6),
            "parent_shared_certification_rescue_rate": round(parent_rescue, 6),
            "rescue_delta_native_minus_parent": round(native_rescue-parent_rescue, 6),
            "native_family_certification_resilience_rate": round(native_resilience, 6),
            "parent_shared_family_certification_resilience_rate": round(parent_resilience, 6),
            "resilience_delta_native_minus_parent": round(native_resilience-parent_resilience, 6),
            "cert_rescue_parent_zero": parent_rescue == 0.0,
        })
    return out


def selector_guardrail_summary(selector_rows: Sequence[Mapping[str, str]]) -> Dict[str, object]:
    if not selector_rows:
        return {"selector_guardrail_passed": "unknown", "selector_rows": 0}
    passed = all(_bool(r.get("selector_guardrail_passed")) for r in selector_rows)
    return {"selector_guardrail_passed": passed, "selector_rows": len(selector_rows)}


def run_analysis(input_dir: Path, output_dir: Path, external_correlation_dir: Optional[Path] = None) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    component_rows = read_csv(input_dir / "ra_witness_overlap_components_v0_9.csv")
    native_overlap_rows = read_csv(input_dir / "ra_cert_rescue_by_native_overlap_v0_9.csv")
    selector_rows = read_csv(input_dir / "ra_native_certificate_overlap_selector_guardrail_v0_9.csv")
    endpoint_rows = read_csv(input_dir / "ra_overlap_vs_external_correlation_comparison_v0_9.csv")
    summary_rows = read_csv(input_dir / "ra_native_certificate_overlap_summary_v0_9.csv")
    if not component_rows:
        raise FileNotFoundError(f"missing or empty ra_witness_overlap_components_v0_9.csv in {input_dir}")
    ablation = component_ablation(component_rows)
    weights = weight_sensitivity(component_rows)
    attribution = signal_attribution(ablation)
    alignment = external_correlation_alignment(native_overlap_rows, external_correlation_dir)
    endpoint = endpoint_audit(endpoint_rows)
    selector = selector_guardrail_summary(selector_rows)

    write_csv(output_dir / "ra_native_overlap_component_ablation_v0_9_1.csv", ablation,
              ["analysis","ablated_component","mode","family_semantics","samples","low_rate","medium_rate","high_rate","low_samples","medium_samples","high_samples","bin_count","monotone_low_to_high","low_high_gap","mean_weighted_overlap"])
    write_csv(output_dir / "ra_native_overlap_weight_sensitivity_v0_9_1.csv", weights,
              ["analysis","weight_profile","mode","family_semantics","samples","low_rate","medium_rate","high_rate","low_samples","medium_samples","high_samples","bin_count","monotone_low_to_high","low_high_gap","mean_weighted_overlap"])
    write_csv(output_dir / "ra_native_overlap_signal_attribution_v0_9_1.csv", attribution,
              ["mode","family_semantics","component","baseline_low_high_gap","ablated_low_high_gap","component_importance_score","interpretation"])
    write_csv(output_dir / "ra_native_overlap_external_correlation_alignment_v0_9_1.csv", alignment,
              ["mode","family_semantics","native_point_count","native_rescue_auc_proxy","native_rescue_decay_proxy","external_available","external_mean_rescue_auc","external_mean_rescue_decay","external_all_monotone","auc_difference_native_minus_external","decay_difference_native_minus_external"])
    write_csv(output_dir / "ra_native_overlap_crn_endpoint_audit_v0_9_1.csv", endpoint,
              ["mode","family_semantics","severity","threshold_fraction","native_overlap_bin","native_certification_rescue_rate","parent_shared_certification_rescue_rate","rescue_delta_native_minus_parent","native_family_certification_resilience_rate","parent_shared_family_certification_resilience_rate","resilience_delta_native_minus_parent","cert_rescue_parent_zero"])

    # compact robustness summary
    ablation_monotone = sum(1 for r in ablation if r.get("monotone_low_to_high") is True)
    ablation_total = len(ablation)
    weight_monotone = sum(1 for r in weights if r.get("monotone_low_to_high") is True)
    weight_total = len(weights)
    positive_gaps = [float(r.get("low_high_gap") or 0.0) for r in weights if str(r.get("weight_profile")) == "balanced"]
    max_component_scores = sorted(attribution, key=lambda r: abs(float(r.get("component_importance_score") or 0.0)), reverse=True)[:8]
    endpoint_rescue_max_delta = max((abs(float(r.get("rescue_delta_native_minus_parent") or 0.0)) for r in endpoint), default=0.0)
    endpoint_resilience_max_delta = max((abs(float(r.get("resilience_delta_native_minus_parent") or 0.0)) for r in endpoint), default=0.0)
    summary = {
        "version": "0.9.1",
        "input_dir": str(input_dir),
        "external_correlation_dir": str(external_correlation_dir) if external_correlation_dir else "",
        "component_rows": len(component_rows),
        "native_overlap_rows": len(native_overlap_rows),
        "ablation_rows": ablation_total,
        "weight_sensitivity_rows": weight_total,
        "ablation_monotone_pass_rate": (ablation_monotone/ablation_total if ablation_total else 0.0),
        "weight_sensitivity_monotone_pass_rate": (weight_monotone/weight_total if weight_total else 0.0),
        "balanced_low_high_gap_mean": (sum(positive_gaps)/len(positive_gaps) if positive_gaps else 0.0),
        "balanced_low_high_gap_min": min(positive_gaps) if positive_gaps else 0.0,
        "balanced_low_high_gap_max": max(positive_gaps) if positive_gaps else 0.0,
        "endpoint_rescue_max_delta_native_minus_parent": endpoint_rescue_max_delta,
        "endpoint_resilience_max_delta_native_minus_parent": endpoint_resilience_max_delta,
        **selector,
    }
    write_csv(output_dir / "ra_native_overlap_robustness_summary_v0_9_1.csv", [summary], list(summary.keys()))
    state = {"summary": summary, "top_component_attribution": max_component_scores}
    (output_dir / "ra_native_overlap_robustness_state_v0_9_1.json").write_text(json.dumps(state, indent=2), encoding="utf-8")
    md = [
        "# RA v0.9.1 Native Certificate-Overlap Robustness Summary",
        "",
        "This analysis audits whether the v0.9 native witness-overlap signature survives component ablation and overlap-weight variation.",
        "",
        "## Summary metrics",
        "",
    ]
    for k, v in summary.items():
        md.append(f"- {k}: {v}")
    md += ["", "## Top component-attribution rows", ""]
    for r in max_component_scores:
        md.append(f"- mode={r['mode']} semantics={r['family_semantics']} component={r['component']} score={r['component_importance_score']}")
    md += [
        "",
        "## Interpretation guardrail",
        "",
        "This packet is analysis-only. It does not promote the overlap weights to a derived RA law. Its role is to test whether the v0.9 native-overlap signature is robust enough to guide the next native/BDG-LLC anchoring step.",
    ]
    (output_dir / "ra_native_overlap_robustness_summary_v0_9_1.md").write_text("\n".join(md), encoding="utf-8")
    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Run RA v0.9.1 native-overlap robustness analysis")
    p.add_argument("--input-dir", required=True, help="Directory containing v0.9 outputs")
    p.add_argument("--output-dir", required=True, help="Directory for v0.9.1 outputs")
    p.add_argument("--external-correlation-dir", default="", help="Optional v0.8.1 output dir for external-correlation alignment")
    args = p.parse_args(argv)
    ext = Path(args.external_correlation_dir) if args.external_correlation_dir else None
    summary = run_analysis(Path(args.input_dir), Path(args.output_dir), ext)
    print("RA v0.9.1 native-overlap robustness analysis complete")
    for k in ["component_rows", "ablation_monotone_pass_rate", "weight_sensitivity_monotone_pass_rate", "balanced_low_high_gap_mean", "selector_guardrail_passed"]:
        print(f"{k}={summary.get(k)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
