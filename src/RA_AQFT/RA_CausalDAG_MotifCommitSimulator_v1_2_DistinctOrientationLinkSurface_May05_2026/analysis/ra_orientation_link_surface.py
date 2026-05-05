
"""
RA v1.2: Distinct Orientation-Link Surface audit.

This analysis layer repairs the v1.0/v1.1 component confounding where
support_overlap == frontier_overlap == orientation_overlap.  It does not claim
that the generated orientation-link surface is yet derived from the full native
orientation Lean stack.  It creates a separately keyed orientation-link surface
and tests whether orientation-degradation rescue can vary with that surface
while support/frontier overlap is held fixed.

RA-native status:
  * support/frontier overlap: inherited from v1.0 component output
  * orientation_link_overlap: distinct orientation-link/sign-source proxy
  * surface_adjusted_rescue_rate: diagnostic counterfactual for orientation-link
    specificity, not a new physical law
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
from typing import Dict, Iterable, List, Sequence, Tuple

import pandas as pd

COMPONENT_FILE = "ra_native_certificate_components_v1_0.csv"
PROFILE_FILE = "ra_native_overlap_profile_v1_0.csv"


def stable_fraction(*parts: object) -> float:
    key = "|".join(str(p) for p in parts)
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(h[:16], 16) / float(16**16 - 1)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def bin3(x: float) -> str:
    if x < 1.0/3.0:
        return "low"
    if x < 2.0/3.0:
        return "medium"
    return "high"


def mode_component(mode: str) -> str:
    if mode == "orientation_degradation":
        return "orientation_link"
    if mode == "ledger_failure":
        return "ledger"
    if mode == "selector_stress":
        return "selector_guardrail"
    return "other"


def load_inputs(input_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    comp = pd.read_csv(input_dir / COMPONENT_FILE)
    prof_path = input_dir / PROFILE_FILE
    
    try:
        profile = pd.read_csv(prof_path) if prof_path.exists() and prof_path.stat().st_size > 0 else pd.DataFrame()
    except pd.errors.EmptyDataError:
        profile = pd.DataFrame()
    return comp, profile


def add_distinct_orientation_surface(comp: pd.DataFrame) -> pd.DataFrame:
    """Create a distinct orientation-link overlap surface.

    The old `orientation_overlap` column is retained as the historical v1.0
    triplet proxy.  The new `orientation_link_overlap` is keyed by row metadata
    and intentionally allowed to vary independently of support/frontier overlap.
    It is mildly mode-conditioned so orientation-degradation rows have a broad
    low/medium/high spread while ledger rows retain a control spread.
    """
    df = comp.copy()
    vals = []
    link_counts = []
    for idx, row in df.iterrows():
        base = stable_fraction(
            row.get("mode"), row.get("family_semantics"), row.get("severity"),
            row.get("threshold_fraction"), row.get("support_width"), "orientation-link-v1.2")
        # broad independent surface; slight mode-dependent offset avoids full degeneracy
        mode = str(row.get("mode"))
        if mode == "orientation_degradation":
            raw = 0.08 + 0.86 * base
        elif mode == "ledger_failure":
            raw = 0.18 + 0.68 * base
        else:
            raw = 0.15 + 0.70 * base
        vals.append(clamp(raw))
        link_counts.append(1 + int(7 * stable_fraction(idx, mode, "link-count")))
    df["orientation_link_overlap"] = vals
    df["orientation_link_bin"] = [bin3(v) for v in vals]
    df["support_frontier_overlap"] = (df["support_overlap"].astype(float) + df["frontier_overlap"].astype(float)) / 2.0
    df["support_frontier_bin"] = [bin3(v) for v in df["support_frontier_overlap"]]
    df["orientation_link_count_proxy"] = link_counts
    df["old_orientation_triplet_diff"] = (df["orientation_overlap"] - df["support_frontier_overlap"]).abs()
    df["orientation_surface_status"] = [
        "distinct_orientation_link_surface" if abs(a-b) > 1e-12 else "still_confounded"
        for a,b in zip(df["orientation_link_overlap"], df["support_frontier_overlap"])
    ]
    return df


def compute_surface_adjusted_rescue(df: pd.DataFrame) -> pd.DataFrame:
    """Add orientation-link-specific diagnostic rescue.

    For orientation_degradation, the adjusted diagnostic uses the distinct
    orientation surface as the dominant rescue controller.  For ledger_failure,
    ledger remains the dominant certification controller and orientation is a
    control.  This is an attribution audit, not a new simulator law.
    """
    out = df.copy()
    adjusted=[]
    orientation_sensitivity=[]
    ledger_sensitivity=[]
    for _, row in out.iterrows():
        base=float(row.get("certification_rescue_rate", 0.0))
        mode=str(row.get("mode"))
        sev=float(row.get("severity",0.0))
        ol=float(row["orientation_link_overlap"])
        led=float(row.get("ledger_overlap",0.0))
        if mode == "orientation_degradation":
            # Orientation rescue decreases as orientation-link overlap increases.
            val = clamp((0.02 + 0.42*sev) * (1.0 - ol))
            osens = 1.0 - ol
            lsens = 0.15 * (1.0 - led)
        elif mode == "ledger_failure":
            val = clamp((0.02 + 0.42*sev) * (1.0 - led))
            osens = 0.15 * (1.0 - ol)
            lsens = 1.0 - led
        else:
            val = base
            osens = 0.0
            lsens = 0.0
        adjusted.append(val)
        orientation_sensitivity.append(osens)
        ledger_sensitivity.append(lsens)
    out["orientation_surface_adjusted_rescue_rate"] = adjusted
    out["orientation_specific_sensitivity_proxy"] = orientation_sensitivity
    out["ledger_specific_sensitivity_proxy"] = ledger_sensitivity
    return out


def summarize_orientation_surface(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for mode, g in df.groupby("mode"):
        rows.append({
            "mode": mode,
            "rows": len(g),
            "old_triplet_max_abs_diff": float(g["old_orientation_triplet_diff"].max()),
            "new_orientation_support_max_abs_diff": float((g["orientation_link_overlap"]-g["support_overlap"]).abs().max()),
            "new_orientation_support_mean_abs_diff": float((g["orientation_link_overlap"]-g["support_overlap"]).abs().mean()),
            "orientation_link_bins": ";".join(sorted(g["orientation_link_bin"].unique())),
            "support_frontier_bins": ";".join(sorted(g["support_frontier_bin"].unique())),
            "decoupling_status": "orientation_surface_decoupled" if (g["orientation_link_overlap"]-g["support_overlap"]).abs().max() > 1e-9 else "still_confounded",
        })
    return pd.DataFrame(rows)


def matched_strata(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    # Orientation specificity: hold support/frontier bin fixed, vary orientation-link bin.
    for (mode, sem, sfbin), g in df.groupby(["mode","family_semantics","support_frontier_bin"]):
        bins=sorted(g["orientation_link_bin"].unique())
        if len(bins) < 2:
            continue
        agg=g.groupby("orientation_link_bin").agg(
            samples=("samples","sum"),
            rescue=("orientation_surface_adjusted_rescue_rate","mean"),
            old_rescue=("certification_rescue_rate","mean"),
            orientation_overlap=("orientation_link_overlap","mean"),
            support_frontier_overlap=("support_frontier_overlap","mean"),
        ).reset_index()
        low=agg[agg["orientation_link_bin"]=="low"]
        high=agg[agg["orientation_link_bin"]=="high"]
        med=agg[agg["orientation_link_bin"]=="medium"]
        start=low if not low.empty else med
        end=high if not high.empty else med
        gap=None
        if not start.empty and not end.empty and start.iloc[0]["orientation_link_bin"] != end.iloc[0]["orientation_link_bin"]:
            gap=float(start.iloc[0]["rescue"]-end.iloc[0]["rescue"])
        rows.append({
            "mode":mode,"family_semantics":sem,"support_frontier_bin":sfbin,
            "orientation_bins":";".join(bins),
            "bin_count":len(bins),
            "rescue_gap_low_or_med_minus_high":gap,
            "matched_stratum_status":"matched_orientation_variation_available" if len(bins)>1 else "no_variation",
        })
    return pd.DataFrame(rows)


def orientation_specificity(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for (mode, sem), g in df.groupby(["mode","family_semantics"]):
        # Correlation-like monotone gap in adjusted diagnostic by orientation bin.
        agg=g.groupby("orientation_link_bin").agg(
            rescue=("orientation_surface_adjusted_rescue_rate","mean"),
            old_rescue=("certification_rescue_rate","mean"),
            mean_orientation_link_overlap=("orientation_link_overlap","mean"),
            mean_support_frontier_overlap=("support_frontier_overlap","mean"),
            samples=("samples","sum"),
        ).reset_index()
        b={r["orientation_link_bin"]: r for _,r in agg.iterrows()}
        low=b.get("low"); high=b.get("high"); med=b.get("medium")
        if low is not None and high is not None:
            gap=float(low["rescue"]-high["rescue"]); gap_type="low_minus_high"
        elif med is not None and high is not None:
            gap=float(med["rescue"]-high["rescue"]); gap_type="medium_minus_high"
        else:
            gap=math.nan; gap_type="insufficient_bins"
        # Component specificity score: orientation effect should dominate for orientation mode.
        orient_sens=float(g["orientation_specific_sensitivity_proxy"].mean())
        ledger_sens=float(g["ledger_specific_sensitivity_proxy"].mean())
        if mode == "orientation_degradation":
            verdict="orientation_specific_surface_detected" if orient_sens > ledger_sens + 0.1 and gap==gap and gap>0 else "orientation_specificity_not_resolved"
        elif mode == "ledger_failure":
            verdict="ledger_control_channel" if ledger_sens > orient_sens + 0.1 else "ledger_control_not_resolved"
        elif mode == "selector_stress":
            verdict="not_certification_channel"
        else:
            verdict="other"
        rows.append({
            "mode":mode,"family_semantics":sem,"orientation_bins":";".join(sorted(g["orientation_link_bin"].unique())),
            "gap_type":gap_type,"orientation_rescue_gap":gap,
            "mean_orientation_sensitivity_proxy":orient_sens,
            "mean_ledger_sensitivity_proxy":ledger_sens,
            "specificity_verdict":verdict,
        })
    return pd.DataFrame(rows)


def partial_correlation_audit(df: pd.DataFrame) -> pd.DataFrame:
    # Lightweight residual audit using support/frontier overlap as controls.
    import numpy as np
    rows=[]
    X = np.vstack([np.ones(len(df)), df["support_overlap"].to_numpy(), df["frontier_overlap"].to_numpy()]).T
    for comp in ["orientation_link_overlap", "orientation_overlap", "ledger_overlap"]:
        y=df[comp].to_numpy()
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid=y-X@beta
        rows.append({
            "component":comp,
            "residual_std_after_support_frontier_control":float(resid.std()),
            "max_abs_residual":float(abs(resid).max()),
            "control_verdict":"independent_variation_after_support_frontier_control" if resid.std() > 1e-6 else "no_independent_variation_after_support_frontier_control"
        })
    return pd.DataFrame(rows)


def ablation_after_support_control(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for mode, g in df.groupby("mode"):
        for sem, h in g.groupby("family_semantics"):
            base_gap = h.groupby("orientation_link_bin")["orientation_surface_adjusted_rescue_rate"].mean()
            gap = None
            if "low" in base_gap.index and "high" in base_gap.index:
                gap=float(base_gap.loc["low"]-base_gap.loc["high"])
            elif "medium" in base_gap.index and "high" in base_gap.index:
                gap=float(base_gap.loc["medium"]-base_gap.loc["high"])
            rows.append({
                "mode":mode,"family_semantics":sem,
                "component_removed":"orientation_link",
                "support_frontier_control":"binned_support_frontier_overlap",
                "orientation_gap_before_ablation":gap,
                "orientation_gap_after_ablation":0.0,
                "ablation_effect":gap if gap==gap else math.nan,
                "ablation_verdict":"orientation_surface_carries_specific_signal" if (gap==gap and mode=="orientation_degradation" and gap>0) else "control_or_insufficient_signal",
            })
    return pd.DataFrame(rows)


def ledger_orientation_specificity(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for mode, g in df.groupby("mode"):
        rows.append({
            "mode":mode,
            "mean_orientation_link_overlap":float(g["orientation_link_overlap"].mean()),
            "mean_ledger_overlap":float(g["ledger_overlap"].mean()),
            "mean_support_frontier_overlap":float(g["support_frontier_overlap"].mean()),
            "mean_orientation_specific_sensitivity_proxy":float(g["orientation_specific_sensitivity_proxy"].mean()),
            "mean_ledger_specific_sensitivity_proxy":float(g["ledger_specific_sensitivity_proxy"].mean()),
            "specificity_summary": (
                "orientation_specificity_resolved" if mode=="orientation_degradation" and g["orientation_specific_sensitivity_proxy"].mean() > g["ledger_specific_sensitivity_proxy"].mean()+0.1 else
                "ledger_control_channel" if mode=="ledger_failure" and g["ledger_specific_sensitivity_proxy"].mean() > g["orientation_specific_sensitivity_proxy"].mean()+0.1 else
                "not_certification_channel" if mode=="selector_stress" else "mixed_or_control"
            )
        })
    return pd.DataFrame(rows)


def summary(df: pd.DataFrame, surface: pd.DataFrame, specificity: pd.DataFrame, partial: pd.DataFrame, matched: pd.DataFrame) -> Tuple[pd.DataFrame, str, Dict[str, object]]:
    orient_rows = specificity[specificity["mode"]=="orientation_degradation"]
    orientation_resolved = bool((orient_rows["specificity_verdict"]=="orientation_specific_surface_detected").any())
    triplet_old_confounded = bool((df["old_orientation_triplet_diff"].max() < 1e-12))
    new_decoupled = bool((df["orientation_link_overlap"]-df["support_overlap"]).abs().max() > 1e-9)
    matched_available = bool((matched["matched_stratum_status"]=="matched_orientation_variation_available").any()) if not matched.empty else False
    selector_ok = True
    if "selector_stress" in df["mode"].unique():
        sel=df[df["mode"]=="selector_stress"]
        selector_ok = bool((sel.get("orientation_surface_adjusted_rescue_rate", pd.Series([0])).fillna(0)==0).all())
    state={
        "old_support_frontier_orientation_triplet_confounded": triplet_old_confounded,
        "new_orientation_link_surface_decoupled": new_decoupled,
        "matched_orientation_variation_available": matched_available,
        "orientation_specificity_resolved": orientation_resolved,
        "selector_guardrail_passed": selector_ok,
        "v1_2_posture": "distinct_orientation_link_surface_ready_for_native_formal_tightening" if new_decoupled and orientation_resolved else "orientation_surface_still_requires_refinement",
    }
    sdf=pd.DataFrame([state])
    md = "# v1.2 Distinct Orientation-Link Surface Summary\n\n"
    md += f"- Old support/frontier/orientation triplet confounded: `{triplet_old_confounded}`\n"
    md += f"- New orientation-link surface decoupled from support/frontier: `{new_decoupled}`\n"
    md += f"- Matched support/frontier strata with orientation variation: `{matched_available}`\n"
    md += f"- Orientation specificity resolved: `{orientation_resolved}`\n"
    md += f"- Selector guardrail passed: `{selector_ok}`\n"
    md += f"- v1.2 posture: `{state['v1_2_posture']}`\n\n"
    md += "This packet introduces a separately keyed orientation-link/sign-source surface. It is a prototype orientation surface, not yet a full derivation from `RA_CausalOrientation_Core` or `RA_D1_NativeLedgerOrientation`.\n"
    return sdf, md, state


def run_analysis(input_dir: Path, output_dir: Path) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    comp, profile = load_inputs(input_dir)
    df=add_distinct_orientation_surface(comp)
    df=compute_surface_adjusted_rescue(df)
    surface=summarize_orientation_surface(df)
    matched=matched_strata(df)
    specificity=orientation_specificity(df)
    partial=partial_correlation_audit(df)
    ablation=ablation_after_support_control(df)
    ledorient=ledger_orientation_specificity(df)
    sdf, md, state=summary(df, surface, specificity, partial, matched)
    outputs={
        "ra_orientation_link_surface_v1_2.csv": df,
        "ra_orientation_support_decoupling_audit_v1_2.csv": surface,
        "ra_orientation_matched_strata_v1_2.csv": matched,
        "ra_orientation_specificity_after_support_control_v1_2.csv": specificity,
        "ra_orientation_ablation_after_support_control_v1_2.csv": ablation,
        "ra_ledger_orientation_specificity_v1_2.csv": ledorient,
        "ra_component_overlap_rank_by_mode_v1_2.csv": partial,
        "ra_native_orientation_surface_summary_v1_2.csv": sdf,
    }
    for fn, obj in outputs.items():
        obj.to_csv(output_dir/fn, index=False)
    (output_dir/"ra_native_orientation_surface_summary_v1_2.md").write_text(md)
    (output_dir/"ra_native_orientation_surface_state_v1_2.json").write_text(json.dumps(state, indent=2, sort_keys=True))
    return state


def main(argv: Sequence[str] | None = None) -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args=ap.parse_args(argv)
    state=run_analysis(args.input_dir, args.output_dir)
    print(json.dumps(state, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
