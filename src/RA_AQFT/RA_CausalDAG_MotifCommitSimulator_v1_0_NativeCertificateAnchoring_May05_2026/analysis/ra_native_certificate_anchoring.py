#!/usr/bin/env python3
"""
RA v1.0 Native Certificate Anchoring analysis layer.

This module consolidates the v0.9/v0.9.1/v0.9.2 native-certificate-overlap
track without changing simulator semantics.  It packages component-level native
witness overlap into v1.0 anchoring outputs and records the calibrated posture:

  * augmented_exact_k is the primary signal-carrier semantics;
  * at_least_k is retained as a monotone guardrail semantics;
  * native-overlap bins are qualitative structural bins, not exact external
    certificate-correlation values;
  * selector stress remains outside support/certification-family rescue.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

COMPONENTS: Tuple[str, ...] = (
    "support", "frontier", "orientation", "ledger", "causal_past", "bdg_kernel", "firewall"
)
PRIMARY_SEMANTICS = "augmented_exact_k"
GUARDRAIL_SEMANTICS = "at_least_k"


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def write_csv_rows(path: Path, rows: Sequence[Mapping[str, object]], fieldnames: Optional[Sequence[str]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        keys: List[str] = []
        for row in rows:
            for k in row.keys():
                if k not in keys:
                    keys.append(k)
        fieldnames = keys
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(fieldnames))
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, '') for k in fieldnames})


def f(row: Mapping[str, object], key: str, default: float = 0.0) -> float:
    try:
        val = row.get(key, default)
        if val in ('', None):
            return default
        return float(val)  # type: ignore[arg-type]
    except Exception:
        return default


def s(row: Mapping[str, object], key: str, default: str = '') -> str:
    val = row.get(key, default)
    return default if val is None else str(val)


def mean(xs: Iterable[float]) -> Optional[float]:
    vals = [x for x in xs if x is not None and not math.isnan(x)]
    return round(sum(vals) / len(vals), 6) if vals else None


def component_anchor_rows(component_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    rows = []
    for r in component_rows:
        out: Dict[str, object] = {
            "mode": s(r, "mode"),
            "family_semantics": s(r, "family_semantics"),
            "severity": f(r, "severity"),
            "threshold_fraction": f(r, "threshold_fraction"),
            "support_width": int(f(r, "support_width")),
            "samples": int(f(r, "samples")),
            "mean_weighted_native_overlap": f(r, "mean_weighted_native_overlap"),
            "mean_induced_certificate_correlation": f(r, "mean_induced_certificate_correlation"),
            "certification_rescue_rate": f(r, "certification_rescue_rate"),
            "primary_signal_semantics": PRIMARY_SEMANTICS,
            "guardrail_semantics": GUARDRAIL_SEMANTICS,
            "anchoring_status": "component_proxy_anchored_to_formal_surface",
        }
        for c in COMPONENTS:
            out[f"{c}_overlap"] = f(r, f"mean_{c}_overlap")
        rows.append(out)
    return rows


def overlap_profile_rows(rescue_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    out = []
    for r in rescue_rows:
        semantics = s(r, "family_semantics")
        out.append({
            "mode": s(r, "mode"),
            "family_semantics": semantics,
            "semantics_role": "primary_signal_carrier" if semantics == PRIMARY_SEMANTICS else "monotone_guardrail" if semantics == GUARDRAIL_SEMANTICS else "other",
            "native_overlap_bin": s(r, "native_overlap_bin"),
            "samples": int(f(r, "samples")),
            "mean_induced_certificate_correlation": f(r, "mean_induced_certificate_correlation"),
            "certification_rescue_rate": f(r, "certification_rescue_rate"),
            "family_certification_resilience_rate": f(r, "family_certification_resilience_rate"),
            "family_internal_loss_rate": f(r, "family_internal_loss_rate"),
        })
    return out


def component_attribution_rows(component_rows: Sequence[Mapping[str, object]], rescue_rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    # Join component means by mode/semantics/bin inferred from the rescue table via induced-correlation bins.
    # Component table lacks explicit bins, so aggregate by mode/semantics and report component ranges.
    groups: Dict[Tuple[str, str], List[Mapping[str, object]]] = {}
    for r in component_rows:
        groups.setdefault((s(r,"mode"), s(r,"family_semantics")), []).append(r)
    rescue_groups: Dict[Tuple[str, str], List[Mapping[str, object]]] = {}
    for r in rescue_rows:
        rescue_groups.setdefault((s(r,"mode"), s(r,"family_semantics")), []).append(r)
    rows = []
    for key, rs in sorted(groups.items()):
        mode, semantics = key
        resc = rescue_groups.get(key, [])
        rescue_gap = None
        bin_rates = {s(r,"native_overlap_bin"): f(r,"certification_rescue_rate") for r in resc}
        if "low" in bin_rates and "high" in bin_rates:
            rescue_gap = round(bin_rates["low"] - bin_rates["high"], 6)
        elif "medium" in bin_rates and "high" in bin_rates:
            rescue_gap = round(bin_rates["medium"] - bin_rates["high"], 6)
        comp_stats = {}
        for c in COMPONENTS:
            vals = [f(r, f"mean_{c}_overlap") for r in rs]
            comp_stats[f"mean_{c}_overlap"] = mean(vals)
            comp_stats[f"range_{c}_overlap"] = round((max(vals)-min(vals)), 6) if vals else None
        expected = "ledger" if mode == "ledger_failure" else "orientation" if mode == "orientation_degradation" else "none"
        rows.append({
            "mode": mode,
            "family_semantics": semantics,
            "semantics_role": "primary_signal_carrier" if semantics == PRIMARY_SEMANTICS else "monotone_guardrail" if semantics == GUARDRAIL_SEMANTICS else "other",
            "native_overlap_bins": ";".join(sorted(bin_rates.keys())),
            "low_high_or_medium_high_rescue_gap": rescue_gap if rescue_gap is not None else "",
            "expected_mode_component": expected,
            "expected_component_mean_overlap": comp_stats.get(f"mean_{expected}_overlap", "") if expected != "none" else "",
            "expected_component_overlap_range": comp_stats.get(f"range_{expected}_overlap", "") if expected != "none" else "",
            **comp_stats,
        })
    return rows


def signal_rows(rescue_rows: Sequence[Mapping[str, object]], semantics: str) -> List[Dict[str, object]]:
    rows = []
    grouped: Dict[Tuple[str,str], List[Mapping[str,object]]] = {}
    for r in rescue_rows:
        if s(r,"family_semantics") == semantics:
            grouped.setdefault((s(r,"mode"), s(r,"family_semantics")), []).append(r)
    order = {"low":0, "medium":1, "high":2}
    for (mode, sem), rs in sorted(grouped.items()):
        rs2 = sorted(rs, key=lambda r: order.get(s(r,"native_overlap_bin"), 9))
        rates = {s(r,"native_overlap_bin"): f(r,"certification_rescue_rate") for r in rs2}
        bins = [s(r,"native_overlap_bin") for r in rs2]
        monotone = True
        vals = [rates[b] for b in bins]
        for a,b in zip(vals, vals[1:]):
            if b > a + 1e-12:
                monotone = False
        gap = None
        if "low" in rates and "high" in rates:
            gap = round(rates["low"] - rates["high"], 6)
        elif "medium" in rates and "high" in rates:
            gap = round(rates["medium"] - rates["high"], 6)
        rows.append({
            "mode": mode,
            "family_semantics": sem,
            "semantics_role": "primary_signal_carrier" if sem == PRIMARY_SEMANTICS else "monotone_guardrail",
            "bins": ";".join(bins),
            "low_rescue_rate": rates.get("low", ""),
            "medium_rescue_rate": rates.get("medium", ""),
            "high_rescue_rate": rates.get("high", ""),
            "gap_used": "low_minus_high" if "low" in rates and "high" in rates else "medium_minus_high" if "medium" in rates and "high" in rates else "none",
            "rescue_gap": gap if gap is not None else "",
            "monotone_nonincreasing": monotone,
            "bin_count": len(bins),
        })
    return rows


def calibration_status_rows(calibration_dir: Optional[Path], rescue_rows: Sequence[Mapping[str,object]]) -> List[Dict[str, object]]:
    rows: List[Dict[str,object]] = []
    if calibration_dir:
        cand = calibration_dir / "ra_native_vs_external_correlation_mapping_v0_9_2.csv"
        if cand.exists():
            for r in read_csv_rows(cand):
                rows.append({
                    "source": "v0_9_2_mapping",
                    **dict(r),
                    "v1_posture": "qualitative_alignment_not_absolute_calibration",
                })
            return rows
    # Fallback: summarize native rescue profile only.
    for r in rescue_rows:
        rows.append({
            "source": "v1_0_fallback_native_only",
            "mode": s(r,"mode"),
            "family_semantics": s(r,"family_semantics"),
            "native_overlap_bin": s(r,"native_overlap_bin"),
            "native_certification_rescue_rate": f(r,"certification_rescue_rate"),
            "external_calibration_status": "not_provided",
            "v1_posture": "qualitative_structural_bin",
        })
    return rows


def selector_guardrail_status(input_dir: Path) -> bool:
    for name in ["ra_native_certificate_overlap_selector_guardrail_v0_9.csv", "ra_cert_selector_guardrail_v0_8_1.csv"]:
        rows = read_csv_rows(input_dir / name)
        if rows:
            return all(str(r.get("selector_guardrail_passed", "True")).lower() in ("true","1","yes") for r in rows)
    return True


def build_summary(
    component_rows_: Sequence[Mapping[str, object]],
    rescue_rows_: Sequence[Mapping[str, object]],
    primary_rows_: Sequence[Mapping[str, object]],
    guardrail_rows_: Sequence[Mapping[str, object]],
    calibration_rows_: Sequence[Mapping[str, object]],
    selector_passed: bool,
) -> Dict[str, object]:
    comp_bins = sorted({s(r,"native_overlap_bin") for r in rescue_rows_ if s(r,"native_overlap_bin")})
    primary_gaps = [f(r,"rescue_gap") for r in primary_rows_ if str(r.get("rescue_gap","")).strip() != ""]
    guard_gaps = [f(r,"rescue_gap") for r in guardrail_rows_ if str(r.get("rescue_gap","")).strip() != ""]
    return {
        "version": "1.0",
        "component_rows": len(component_rows_),
        "native_overlap_profile_rows": len(rescue_rows_),
        "native_overlap_bins": comp_bins,
        "native_overlap_bin_count": len(comp_bins),
        "primary_family_semantics": PRIMARY_SEMANTICS,
        "guardrail_family_semantics": GUARDRAIL_SEMANTICS,
        "primary_signal_rows": len(primary_rows_),
        "primary_signal_monotone_count": sum(1 for r in primary_rows_ if str(r.get("monotone_nonincreasing","")).lower() in ("true","1")),
        "primary_mean_rescue_gap": mean(primary_gaps),
        "guardrail_signal_rows": len(guardrail_rows_),
        "guardrail_monotone_count": sum(1 for r in guardrail_rows_ if str(r.get("monotone_nonincreasing","")).lower() in ("true","1")),
        "guardrail_mean_rescue_gap": mean(guard_gaps),
        "calibration_rows": len(calibration_rows_),
        "selector_guardrail_passed": selector_passed,
        "v1_posture": "component_anchored_proxy_ready_for_BDG_LLC_native_formalization",
    }


def write_summary_md(path: Path, summary: Mapping[str, object], primary_rows: Sequence[Mapping[str, object]], guardrail_rows: Sequence[Mapping[str, object]], calibration_rows: Sequence[Mapping[str, object]]) -> None:
    lines = [
        "# RA v1.0 Native Certificate Anchoring Summary",
        "",
        "This v1.0 analysis consolidates the native certificate-overlap track. It does not add a new rescue law; it packages native witness-component surfaces and records the v1.0 modeling posture.",
        "",
        "## Summary",
        "",
    ]
    for k, v in summary.items():
        lines.append(f"- {k}: {v}")
    lines += [
        "",
        "## Primary signal semantics",
        "",
        "`augmented_exact_k` is the primary signal-carrier semantics because it preserves the parent support structure while adding focused alternatives and tends to populate low/medium/high native-overlap bins.",
        "",
    ]
    for r in primary_rows[:10]:
        lines.append(f"- mode={r.get('mode')} bins={r.get('bins')} gap={r.get('rescue_gap')} monotone={r.get('monotone_nonincreasing')}")
    lines += [
        "",
        "## Guardrail semantics",
        "",
        "`at_least_k` remains the monotone guardrail semantics. Missing low-overlap bins should be treated as bin-population structure, not as zero-rescue failure.",
        "",
    ]
    for r in guardrail_rows[:10]:
        lines.append(f"- mode={r.get('mode')} bins={r.get('bins')} gap={r.get('rescue_gap')} monotone={r.get('monotone_nonincreasing')}")
    lines += [
        "",
        "## Calibration posture",
        "",
        "Native-overlap bins are qualitative structural bins. They align directionally with the external v0.8.1 certificate-correlation curve, but they are not asserted as exact external-correlation values.",
        "",
        f"- calibration rows: {len(calibration_rows)}",
        "",
        "## BDG-LLC / native-certificate caution",
        "",
        "The current simulator components are operational proxies for native support/frontier/orientation/ledger/causal-past/kernel/firewall evidence. v1.0 prepares formal surfaces for anchoring these components, but does not yet derive the overlap weights or rescue law from the BDG-LLC action.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines)+"\n", encoding="utf-8")


def run_analysis(input_dir: Path, output_dir: Path, calibration_dir: Optional[Path] = None) -> Dict[str, object]:
    comp = read_csv_rows(input_dir / "ra_witness_overlap_components_v0_9.csv")
    rescue = read_csv_rows(input_dir / "ra_cert_rescue_by_native_overlap_v0_9.csv")
    if not comp:
        raise FileNotFoundError(f"missing component overlap CSV in {input_dir}")
    if not rescue:
        raise FileNotFoundError(f"missing rescue-by-native-overlap CSV in {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    components = component_anchor_rows(comp)
    profiles = overlap_profile_rows(rescue)
    attribution = component_attribution_rows(comp, rescue)
    primary = signal_rows(rescue, PRIMARY_SEMANTICS)
    guard = signal_rows(rescue, GUARDRAIL_SEMANTICS)
    calib = calibration_status_rows(calibration_dir, rescue)
    selector = selector_guardrail_status(input_dir)
    summary = build_summary(components, profiles, primary, guard, calib, selector)

    write_csv_rows(output_dir/"ra_native_certificate_components_v1_0.csv", components)
    write_csv_rows(output_dir/"ra_native_overlap_profile_v1_0.csv", profiles)
    write_csv_rows(output_dir/"ra_component_attribution_by_mode_v1_0.csv", attribution)
    write_csv_rows(output_dir/"ra_augmented_exactk_signal_v1_0.csv", primary)
    write_csv_rows(output_dir/"ra_atleastk_guardrail_v1_0.csv", guard)
    write_csv_rows(output_dir/"ra_native_overlap_calibration_status_v1_0.csv", calib)
    write_csv_rows(output_dir/"ra_native_certificate_anchoring_summary_v1_0.csv", [summary])
    write_summary_md(output_dir/"ra_native_certificate_anchoring_summary_v1_0.md", summary, primary, guard, calib)
    (output_dir/"ra_native_certificate_anchoring_state_v1_0.json").write_text(json.dumps({
        "summary": summary,
        "primary": primary,
        "guardrail": guard,
        "calibration": calib,
    }, indent=2, sort_keys=True), encoding="utf-8")
    return summary


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="RA v1.0 native certificate anchoring analysis.")
    p.add_argument("--input-dir", required=True, help="Directory containing v0.9 outputs.")
    p.add_argument("--calibration-dir", default=None, help="Optional directory containing v0.9.2 calibration outputs.")
    p.add_argument("--output-dir", default="outputs")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_arg_parser().parse_args(argv)
    summary = run_analysis(Path(args.input_dir), Path(args.output_dir), Path(args.calibration_dir) if args.calibration_dir else None)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
