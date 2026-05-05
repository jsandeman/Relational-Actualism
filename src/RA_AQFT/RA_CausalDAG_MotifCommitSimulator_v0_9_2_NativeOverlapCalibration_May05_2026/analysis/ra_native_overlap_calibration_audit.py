#!/usr/bin/env python3
"""RA v0.9.2 native-overlap calibration and family-semantics audit.

This is a pure analysis layer over v0.9 and v0.8.1 outputs.  It does not
change simulator semantics and introduces no new Lean objects.  Its purpose is
threefold:

1. Audit the family-semantics asymmetry seen in v0.9.1, especially cases where
   ledger_failure / at_least_k carries little or no native-overlap rescue signal.
2. Calibrate native-overlap bins against the external certificate-correlation
   baseline from v0.8.1.
3. Recommend a conservative v1.0 candidate semantics/diagnostic basis for
   BDG-LLC/native-certificate anchoring.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

BIN_ORDER = ("low", "medium", "high")
MODE_ORDER = ("ledger_failure", "orientation_degradation", "selector_stress")
SEMANTICS_ORDER = ("at_least_k", "augmented_exact_k")


def _float(x: object, default: float = 0.0) -> float:
    if x is None:
        return default
    s = str(x).strip()
    if s == "":
        return default
    try:
        return float(s)
    except Exception:
        return default


def _int(x: object, default: int = 0) -> int:
    try:
        return int(float(str(x).strip()))
    except Exception:
        return default


def _bool(x: object) -> bool:
    return str(x).strip().lower() in {"true", "1", "yes", "y"}


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
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def group_by(rows: Iterable[Mapping[str, str]], keys: Sequence[str]) -> Dict[Tuple[str, ...], List[Mapping[str, str]]]:
    out: Dict[Tuple[str, ...], List[Mapping[str, str]]] = defaultdict(list)
    for r in rows:
        out[tuple(str(r.get(k, "")) for k in keys)].append(r)
    return out


def sum_samples(rows: Sequence[Mapping[str, str]]) -> int:
    return sum(max(0, _int(r.get("samples", 1), 1)) for r in rows)


def weighted_rate(rows: Sequence[Mapping[str, str]], field: str) -> float:
    total = sum_samples(rows)
    if total <= 0:
        return 0.0
    return sum(max(0, _int(r.get("samples", 1), 1)) * _float(r.get(field, 0.0)) for r in rows) / total


def fmt(x: object) -> object:
    if x is None:
        return ""
    if isinstance(x, float):
        return round(x, 6)
    return x


def native_bin_rates(native_rows: Sequence[Mapping[str, str]], mode: str, sem: str) -> Dict[str, Dict[str, float]]:
    rows = [r for r in native_rows if str(r.get("mode")) == mode and str(r.get("family_semantics")) == sem]
    out: Dict[str, Dict[str, float]] = {}
    for b in BIN_ORDER:
        br = [r for r in rows if str(r.get("native_overlap_bin")) == b]
        if br:
            out[b] = {
                "samples": float(sum_samples(br)),
                "certification_rescue_rate": weighted_rate(br, "certification_rescue_rate"),
                "family_certification_resilience_rate": weighted_rate(br, "family_certification_resilience_rate"),
                "family_internal_loss_rate": weighted_rate(br, "family_internal_loss_rate"),
                "mean_induced_certificate_correlation": weighted_rate(br, "mean_induced_certificate_correlation"),
            }
    return out


def low_high_gap(rates: Mapping[str, Mapping[str, float]], field: str = "certification_rescue_rate") -> Optional[float]:
    if "low" in rates and "high" in rates:
        return rates["low"].get(field, 0.0) - rates["high"].get(field, 0.0)
    return None


def ordered_monotone_nonincreasing(rates: Mapping[str, Mapping[str, float]], field: str = "certification_rescue_rate") -> bool:
    vals = [rates[b][field] for b in BIN_ORDER if b in rates]
    return all(a + 1e-12 >= b for a, b in zip(vals, vals[1:]))


def trapz_auc(points: Sequence[Tuple[float, float]]) -> float:
    pts = sorted((float(x), float(y)) for x, y in points)
    if len(pts) < 2:
        return 0.0
    width = pts[-1][0] - pts[0][0]
    if width <= 0:
        return 0.0
    area = 0.0
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        area += (x2 - x1) * (y1 + y2) / 2.0
    return area / width


def inverse_external_correlation(external_points: Sequence[Tuple[float, float]], native_rate: float) -> Tuple[float, float]:
    """Return nearest external correlation and absolute residual for a native rescue rate."""
    if not external_points:
        return (math.nan, math.nan)
    best = min(external_points, key=lambda p: abs(float(p[1]) - float(native_rate)))
    return float(best[0]), abs(float(best[1]) - float(native_rate))


def load_external_curves(external_dir: Optional[Path]) -> Dict[Tuple[str, str], List[Tuple[float, float]]]:
    if not external_dir:
        return {}
    rows = read_csv(external_dir / "ra_cert_rescue_decay_curve_v0_8_1.csv")
    curves: Dict[Tuple[str, str], List[Tuple[float, float]]] = defaultdict(list)
    # Aggregate over severity/threshold by correlation using sample weights.
    tmp: Dict[Tuple[str, str, float], List[Mapping[str, str]]] = defaultdict(list)
    for r in rows:
        key = (str(r.get("mode")), str(r.get("family_semantics")), round(_float(r.get("certificate_correlation")), 6))
        tmp[key].append(r)
    for (mode, sem, corr), rs in tmp.items():
        curves[(mode, sem)].append((corr, weighted_rate(rs, "certification_rescue_rate")))
    return {k: sorted(v) for k, v in curves.items()}


def semantics_signal_carriers(native_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for mode in sorted({str(r.get("mode")) for r in native_rows}):
        for sem in sorted({str(r.get("family_semantics")) for r in native_rows if str(r.get("mode")) == mode}):
            rates = native_bin_rates(native_rows, mode, sem)
            gap = low_high_gap(rates)
            vals = [(rates[b]["mean_induced_certificate_correlation"], rates[b]["certification_rescue_rate"]) for b in BIN_ORDER if b in rates]
            rows.append({
                "mode": mode,
                "family_semantics": sem,
                "native_overlap_bins_present": ";".join([b for b in BIN_ORDER if b in rates]),
                "samples": int(sum(rates[b]["samples"] for b in rates)),
                "low_rescue_rate": fmt(rates.get("low", {}).get("certification_rescue_rate")),
                "medium_rescue_rate": fmt(rates.get("medium", {}).get("certification_rescue_rate")),
                "high_rescue_rate": fmt(rates.get("high", {}).get("certification_rescue_rate")),
                "low_high_gap": fmt(gap),
                "rescue_auc_proxy": fmt(trapz_auc(vals)),
                "monotone_low_to_high": ordered_monotone_nonincreasing(rates),
                "signal_status": classify_signal(gap, rates),
            })
    return rows


def classify_signal(gap: Optional[float], rates: Mapping[str, Mapping[str, float]]) -> str:
    if gap is None:
        return "insufficient_bins"
    if abs(gap) < 1e-12:
        return "zero_baseline_or_no_gap"
    if gap > 0.10:
        return "strong_low_overlap_rescue_signal"
    if gap > 0.03:
        return "moderate_low_overlap_rescue_signal"
    if gap > 0:
        return "weak_low_overlap_rescue_signal"
    return "reversed_or_negative_gap"


def semantics_audit(native_rows: Sequence[Mapping[str, str]], aggregate_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    carriers = semantics_signal_carriers(native_rows)
    aggregate_by_key = group_by(aggregate_rows, ["mode", "family_semantics"])
    out: List[Dict[str, object]] = []
    for c in carriers:
        mode = str(c["mode"]); sem = str(c["family_semantics"])
        ars = aggregate_by_key.get((mode, sem), [])
        support_widths = sorted({_int(r.get("support_width_count")) for r in ars if str(r.get("support_width_count", ""))})
        mean_family_size = weighted_rate(ars, "mean_family_size") if ars else 0.0
        mean_support_width = weighted_rate(ars, "mean_support_width") if ars else 0.0
        out.append({
            **c,
            "mean_support_width": fmt(mean_support_width),
            "mean_family_size": fmt(mean_family_size),
            "support_width_count_values": ";".join(map(str, support_widths)),
            "v1_semantics_recommendation": recommend_semantics(mode, sem, c),
        })
    return out


def recommend_semantics(mode: str, sem: str, carrier: Mapping[str, object]) -> str:
    status = str(carrier.get("signal_status"))
    if sem == "augmented_exact_k" and "strong" in status:
        return "primary_candidate_for_native_cert_overlap_v1"
    if sem == "augmented_exact_k" and ("moderate" in status or "weak" in status):
        return "secondary_candidate_pending_native_formalization"
    if sem == "at_least_k" and status == "zero_baseline_or_no_gap":
        return "retain_as_guardrail_semantics_not_primary_signal_carrier"
    if sem == "at_least_k":
        return "compare_against_augmented_exact_k_before_v1_selection"
    return "diagnostic_only"


def ledger_atleastk_zero_baseline_audit(native_rows: Sequence[Mapping[str, str]], component_rows: Sequence[Mapping[str, str]]) -> List[Dict[str, object]]:
    # Native bin-level audit.
    out: List[Dict[str, object]] = []
    for mode in sorted({str(r.get("mode")) for r in native_rows}):
        if mode != "ledger_failure":
            continue
        for sem in sorted({str(r.get("family_semantics")) for r in native_rows if str(r.get("mode")) == mode}):
            rates = native_bin_rates(native_rows, mode, sem)
            gap = low_high_gap(rates)
            out.append({
                "audit_scope": "native_bin_summary",
                "mode": mode,
                "family_semantics": sem,
                "low_rate": fmt(rates.get("low", {}).get("certification_rescue_rate")),
                "medium_rate": fmt(rates.get("medium", {}).get("certification_rescue_rate")),
                "high_rate": fmt(rates.get("high", {}).get("certification_rescue_rate")),
                "low_samples": int(rates.get("low", {}).get("samples", 0)),
                "medium_samples": int(rates.get("medium", {}).get("samples", 0)),
                "high_samples": int(rates.get("high", {}).get("samples", 0)),
                "low_high_gap": fmt(gap),
                "zero_baseline": bool(gap is not None and abs(gap) < 1e-12),
                "interpretation": ledger_interpretation(sem, gap),
            })
    # Width/threshold/severity slices for ledger / at_least_k.
    target = [r for r in component_rows if str(r.get("mode")) == "ledger_failure" and str(r.get("family_semantics")) == "at_least_k"]
    grouped = group_by(target, ["severity", "threshold_fraction", "support_width"])
    for (sev, th, width), rows in sorted(grouped.items(), key=lambda kv: (float(kv[0][0]), float(kv[0][1]), int(float(kv[0][2])))):
        out.append({
            "audit_scope": "ledger_atleastk_width_slice",
            "mode": "ledger_failure",
            "family_semantics": "at_least_k",
            "severity": sev,
            "threshold_fraction": th,
            "support_width": width,
            "samples": sum_samples(rows),
            "mean_native_overlap": fmt(weighted_rate(rows, "mean_weighted_native_overlap")),
            "mean_induced_certificate_correlation": fmt(weighted_rate(rows, "mean_induced_certificate_correlation")),
            "certification_rescue_rate": fmt(weighted_rate(rows, "certification_rescue_rate")),
            "zero_rescue_slice": bool(abs(weighted_rate(rows, "certification_rescue_rate")) < 1e-12),
            "interpretation": "width-stratified slice used to diagnose at_least_k zero-baseline or suppressed-signal behavior",
        })
    return out


def ledger_interpretation(sem: str, gap: Optional[float]) -> str:
    if gap is None:
        return "insufficient native-overlap bins to classify"
    if abs(gap) < 1e-12:
        return "zero native-overlap rescue gap under this semantics; treat as guardrail/semantics asymmetry"
    if sem == "augmented_exact_k" and gap > 0:
        return "positive native-overlap rescue signal; augmented exact-k carries ledger certification signature"
    return "positive but semantics-specific signal; compare against augmented exact-k before v1 selection"


def calibration_curve(native_rows: Sequence[Mapping[str, str]], external_curves: Mapping[Tuple[str, str], Sequence[Tuple[float, float]]]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    grouped = group_by(native_rows, ["mode", "family_semantics", "native_overlap_bin"])
    for (mode, sem, bin_name), rows in sorted(grouped.items()):
        rescue = weighted_rate(rows, "certification_rescue_rate")
        native_corr = weighted_rate(rows, "mean_induced_certificate_correlation")
        ext_curve = external_curves.get((mode, sem), [])
        equiv_corr, residual = inverse_external_correlation(ext_curve, rescue)
        out.append({
            "mode": mode,
            "family_semantics": sem,
            "native_overlap_bin": bin_name,
            "samples": sum_samples(rows),
            "native_mean_induced_correlation": fmt(native_corr),
            "native_certification_rescue_rate": fmt(rescue),
            "external_equivalent_correlation_nearest": fmt(equiv_corr),
            "external_calibration_residual_abs": fmt(residual),
            "external_curve_available": bool(ext_curve),
            "calibration_status": classify_calibration(native_corr, equiv_corr, residual),
        })
    return out


def classify_calibration(native_corr: float, equiv_corr: float, residual: float) -> str:
    if math.isnan(equiv_corr):
        return "external_curve_missing"
    if residual < 0.02:
        return "close_rate_match"
    if residual < 0.08:
        return "qualitative_rate_match"
    return "steeper_or_uncalibrated_native_curve"


def native_vs_external_mapping(native_rows: Sequence[Mapping[str, str]], external_curves: Mapping[Tuple[str, str], Sequence[Tuple[float, float]]]) -> List[Dict[str, object]]:
    out: List[Dict[str, object]] = []
    for key, rows in sorted(group_by(native_rows, ["mode", "family_semantics"]).items()):
        mode, sem = key
        # Native points by bin.
        native_pts = []
        for b in BIN_ORDER:
            br = [r for r in rows if str(r.get("native_overlap_bin")) == b]
            if br:
                native_pts.append((weighted_rate(br, "mean_induced_certificate_correlation"), weighted_rate(br, "certification_rescue_rate")))
        native_pts.sort()
        native_auc = trapz_auc(native_pts)
        native_decay = (native_pts[0][1] - native_pts[-1][1]) if len(native_pts) >= 2 else 0.0
        ext_pts = list(external_curves.get((mode, sem), []))
        ext_auc = trapz_auc(ext_pts)
        ext_decay = (ext_pts[0][1] - ext_pts[-1][1]) if len(ext_pts) >= 2 else 0.0
        out.append({
            "mode": mode,
            "family_semantics": sem,
            "native_point_count": len(native_pts),
            "external_point_count": len(ext_pts),
            "native_auc_proxy": fmt(native_auc),
            "external_auc_proxy": fmt(ext_auc),
            "auc_delta_native_minus_external": fmt(native_auc - ext_auc),
            "native_low_high_or_start_end_decay": fmt(native_decay),
            "external_start_end_decay": fmt(ext_decay),
            "decay_delta_native_minus_external": fmt(native_decay - ext_decay),
            "qualitative_alignment": bool((native_decay >= -1e-12) and (ext_decay >= -1e-12)),
            "mapping_interpretation": "native bins qualitative-alignment check; absolute calibration remains proxy-level" if ext_pts else "external curve missing",
        })
    return out


def v1_candidate_summary(semantics_rows: Sequence[Mapping[str, object]], calibration_rows: Sequence[Mapping[str, object]]) -> Dict[str, object]:
    # Choose primary semantics by sum of positive low-high gaps for certification channels.
    score: Dict[str, float] = defaultdict(float)
    zero_baseline: Dict[str, int] = defaultdict(int)
    for r in semantics_rows:
        sem = str(r.get("family_semantics"))
        try:
            gap = float(r.get("low_high_gap") or 0.0)
        except Exception:
            gap = 0.0
        if gap > 0:
            score[sem] += gap
        if str(r.get("signal_status")) == "zero_baseline_or_no_gap":
            zero_baseline[sem] += 1
    primary = max(score.items(), key=lambda kv: kv[1])[0] if score else ""
    residuals = []
    for r in calibration_rows:
        if str(r.get("external_curve_available")) == "True":
            try: residuals.append(float(r.get("external_calibration_residual_abs") or 0.0))
            except Exception: pass
    return {
        "candidate_primary_family_semantics": primary,
        "semantics_score_augmented_exact_k": round(score.get("augmented_exact_k", 0.0), 6),
        "semantics_score_at_least_k": round(score.get("at_least_k", 0.0), 6),
        "zero_baseline_count_augmented_exact_k": zero_baseline.get("augmented_exact_k", 0),
        "zero_baseline_count_at_least_k": zero_baseline.get("at_least_k", 0),
        "mean_external_calibration_residual_abs": round(sum(residuals)/len(residuals), 6) if residuals else 0.0,
        "max_external_calibration_residual_abs": round(max(residuals), 6) if residuals else 0.0,
        "v1_recommendation": "use augmented_exact_k as primary signal-carrier; retain at_least_k as monotone guardrail semantics" if primary == "augmented_exact_k" else "semantics unresolved; inspect signal-carrier table before v1 anchoring",
    }


def selector_guardrail(selector_rows: Sequence[Mapping[str, str]]) -> bool:
    if not selector_rows:
        return True
    return all(_bool(r.get("selector_guardrail_passed", "true")) for r in selector_rows)


def run_analysis(input_dir: Path, external_correlation_dir: Optional[Path], output_dir: Path) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    native_rows = read_csv(input_dir / "ra_cert_rescue_by_native_overlap_v0_9.csv")
    aggregate_rows = read_csv(input_dir / "ra_native_certificate_overlap_aggregate_v0_9.csv")
    component_rows = read_csv(input_dir / "ra_witness_overlap_components_v0_9.csv")
    selector_rows = read_csv(input_dir / "ra_native_certificate_overlap_selector_guardrail_v0_9.csv")
    if not native_rows:
        raise FileNotFoundError(f"missing or empty ra_cert_rescue_by_native_overlap_v0_9.csv in {input_dir}")
    external_curves = load_external_curves(external_correlation_dir)

    semantics_rows = semantics_audit(native_rows, aggregate_rows)
    ledger_rows = ledger_atleastk_zero_baseline_audit(native_rows, component_rows)
    calib_rows = calibration_curve(native_rows, external_curves)
    mapping_rows = native_vs_external_mapping(native_rows, external_curves)
    carrier_rows = semantics_signal_carriers(native_rows)
    v1_summary = v1_candidate_summary(semantics_rows, calib_rows)

    write_csv(output_dir / "ra_native_overlap_semantics_audit_v0_9_2.csv", semantics_rows,
              ["mode","family_semantics","native_overlap_bins_present","samples","low_rescue_rate","medium_rescue_rate","high_rescue_rate","low_high_gap","rescue_auc_proxy","monotone_low_to_high","signal_status","mean_support_width","mean_family_size","support_width_count_values","v1_semantics_recommendation"])
    write_csv(output_dir / "ra_ledger_atleastk_zero_baseline_audit_v0_9_2.csv", ledger_rows,
              ["audit_scope","mode","family_semantics","severity","threshold_fraction","support_width","samples","low_rate","medium_rate","high_rate","low_samples","medium_samples","high_samples","low_high_gap","zero_baseline","mean_native_overlap","mean_induced_certificate_correlation","certification_rescue_rate","zero_rescue_slice","interpretation"])
    write_csv(output_dir / "ra_native_overlap_calibration_curve_v0_9_2.csv", calib_rows,
              ["mode","family_semantics","native_overlap_bin","samples","native_mean_induced_correlation","native_certification_rescue_rate","external_equivalent_correlation_nearest","external_calibration_residual_abs","external_curve_available","calibration_status"])
    write_csv(output_dir / "ra_native_vs_external_correlation_mapping_v0_9_2.csv", mapping_rows,
              ["mode","family_semantics","native_point_count","external_point_count","native_auc_proxy","external_auc_proxy","auc_delta_native_minus_external","native_low_high_or_start_end_decay","external_start_end_decay","decay_delta_native_minus_external","qualitative_alignment","mapping_interpretation"])
    write_csv(output_dir / "ra_family_semantics_signal_carriers_v0_9_2.csv", carrier_rows,
              ["mode","family_semantics","native_overlap_bins_present","samples","low_rescue_rate","medium_rescue_rate","high_rescue_rate","low_high_gap","rescue_auc_proxy","monotone_low_to_high","signal_status"])

    summary = {
        "version": "0.9.2",
        "input_dir": str(input_dir),
        "external_correlation_dir": str(external_correlation_dir) if external_correlation_dir else "",
        "native_rows": len(native_rows),
        "aggregate_rows": len(aggregate_rows),
        "component_rows": len(component_rows),
        "semantics_rows": len(semantics_rows),
        "calibration_rows": len(calib_rows),
        "mapping_rows": len(mapping_rows),
        "selector_guardrail_passed": selector_guardrail(selector_rows),
        **v1_summary,
    }
    write_csv(output_dir / "ra_native_overlap_v1_candidate_summary_v0_9_2.csv", [summary], list(summary.keys()))
    (output_dir / "ra_native_overlap_calibration_state_v0_9_2.json").write_text(json.dumps({"summary": summary}, indent=2), encoding="utf-8")
    md_lines = [
        "# RA v0.9.2 Native Overlap Calibration / Family-Semantics Audit",
        "",
        "This analysis audits whether native-overlap certification rescue is carried uniformly across support-family semantics, and calibrates native-overlap bins against the v0.8.1 external certificate-correlation baseline.",
        "",
        "## Summary",
        "",
    ]
    for k, v in summary.items():
        md_lines.append(f"- {k}: {v}")
    md_lines += [
        "",
        "## Interpretation guardrail",
        "",
        "v0.9.2 is analysis-only. It does not promote any overlap weighting or family semantics to a derived RA law. It identifies candidate semantics and calibration diagnostics for the next BDG-LLC/native-certificate anchoring step.",
        "",
        "## Recommended v1.0 posture",
        "",
        str(summary.get("v1_recommendation", "")),
    ]
    (output_dir / "ra_native_overlap_v1_candidate_summary_v0_9_2.md").write_text("\n".join(md_lines), encoding="utf-8")
    return summary


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Run RA v0.9.2 native-overlap calibration/family-semantics audit")
    ap.add_argument("--input-dir", required=True, help="Directory containing v0.9 outputs")
    ap.add_argument("--external-correlation-dir", default="", help="Optional directory containing v0.8.1 external-correlation outputs")
    ap.add_argument("--output-dir", required=True, help="Output directory")
    args = ap.parse_args(argv)
    ext = Path(args.external_correlation_dir) if args.external_correlation_dir else None
    summary = run_analysis(Path(args.input_dir), ext, Path(args.output_dir))
    print("RA v0.9.2 native-overlap calibration audit complete")
    for k in ["selector_guardrail_passed", "candidate_primary_family_semantics", "semantics_score_augmented_exact_k", "semantics_score_at_least_k", "mean_external_calibration_residual_abs"]:
        print(f"{k}={summary.get(k)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
