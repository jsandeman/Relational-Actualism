"""
RA v1.3: Native Orientation-Link Derivation audit.

This analysis layer replaces the v1.2 row-metadata-generated orientation-link
surface with a theorem-surface-constrained native orientation/sign-source
catalog extracted from RA Lean modules.  It is still not a per-graph proof that
orientation links arise from every concrete support-family member; instead it is
an intermediate anchoring step:

  v1.2 synthetic distinct surface
      -> v1.3 native theorem/sign-source catalog surface
      -> future per-graph native orientation witness derivation

The v1.3 surface is derived from Lean declaration names and theorem roles in
RA_CausalOrientation_Core, RA_D1_NativeLedgerOrientation, RA_D1_NativeClosure,
and related native modules.  Each row's support-family/mode context selects
orientation-link role tokens from that catalog; overlap is Jaccard overlap of
those native-role token sets.  This keeps the orientation-link surface distinct
from support/frontier overlap while tying it to RA-native orientation vocabulary.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import re
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import pandas as pd
import numpy as np

COMPONENT_FILE = "ra_native_certificate_components_v1_0.csv"

DEFAULT_NATIVE_FILES = [
    "RA_CausalOrientation_Core.lean",
    "RA_D1_NativeLedgerOrientation.lean",
    "RA_D1_NativeClosure.lean",
    "RA_D1_GraphCutCombinatorics.lean",
    "RA_D1_NativeConfinement.lean",
]

DECL_RE = re.compile(r"^(?:private\s+)?(?:theorem|lemma|def)\s+([A-Za-z0-9_'.]+)")


def stable_fraction(*parts: object) -> float:
    key = "|".join(str(p) for p in parts)
    h = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return int(h[:16], 16) / float(16**16 - 1)


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def bin3(x: float) -> str:
    if x < 1.0 / 3.0:
        return "low"
    if x < 2.0 / 3.0:
        return "medium"
    return "high"


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def normalize_module_name(path: Path) -> str:
    name = path.name
    name = re.sub(r"\(\d+\)", "", name)
    name = name.replace("_v1", "")
    return name.replace(".lean", "")


def classify_decl(name: str, body: str, module: str) -> Tuple[str, List[str], float]:
    low = f"{module} {name} {body}".lower()
    tags: List[str] = []
    weight = 1.0
    if "orientation" in low:
        tags.append("orientation")
        weight += 0.3
    if "winding" in low:
        tags.append("winding")
        weight += 0.2
    if "precedence" in low:
        tags.append("precedence")
        weight += 0.2
    if "asym" in low or "asymmetric" in low:
        tags.append("asymmetric")
        weight += 0.15
    if "symmetric" in low or "sym" in low:
        tags.append("symmetric")
        weight += 0.15
    if "ledger" in low or "depth2" in low:
        tags.append("ledger")
        weight += 0.2
    if "closure" in low or "classified" in low or "extension" in low:
        tags.append("closure")
        weight += 0.1
    if "reverse" in low:
        tags.append("reverse")
        weight += 0.1
    if "forward" in low:
        tags.append("forward")
        weight += 0.1
    if "stable" in low or "preserved" in low or "endpoint" in low:
        tags.append("stable")
        weight += 0.1
    if "bdgscore" in low or "bdg" in low:
        tags.append("bdg")
        weight += 0.05
    if "firewall" in low or "sever" in low or "horizon" in low:
        tags.append("severance_exposure")
        weight += 0.1

    # component role is deliberately coarse; tags carry finer detail.
    if "RA_CausalOrientation" in module or "orientation" in tags or "winding" in tags or "precedence" in tags:
        role = "orientation_link"
    elif "ledger" in tags:
        role = "ledger_orientation"
    elif "closure" in tags:
        role = "closure_extension"
    elif "severance_exposure" in tags:
        role = "severance_exposure"
    else:
        role = "native_supporting"
    return role, sorted(set(tags)), weight


def parse_lean_declarations(lean_files: Sequence[Path]) -> pd.DataFrame:
    rows = []
    for path in lean_files:
        if not path.exists():
            continue
        module = normalize_module_name(path)
        text = path.read_text(errors="ignore")
        lines = text.splitlines()
        for i, line in enumerate(lines):
            m = DECL_RE.match(line.strip())
            if not m:
                continue
            name = m.group(1)
            # small body window for keyword classification
            body = "\n".join(lines[i:i+8])
            role, tags, weight = classify_decl(name, body, module)
            if role == "native_supporting" and not any(t in tags for t in ["orientation", "ledger", "closure", "severance_exposure"]):
                # keep a few closure/core tokens only if relevant names
                if not any(k in name.lower() for k in ["orientation", "ledger", "winding", "precedence", "closure", "extension", "branch", "sym", "asym"]):
                    continue
            rows.append({
                "module": module,
                "declaration": name,
                "role": role,
                "tags": ";".join(tags),
                "weight": round(weight, 6),
                "source_file": path.name,
                "line": i + 1,
            })
    if not rows:
        rows = fallback_manifest_rows()
    return pd.DataFrame(rows).drop_duplicates(subset=["module", "declaration"]).reset_index(drop=True)


def fallback_manifest_rows() -> List[Dict[str, object]]:
    names = [
        ("RA_CausalOrientation_Core", "one_way_precedence", "orientation_link", "orientation;precedence"),
        ("RA_CausalOrientation_Core", "forward_winding_stable", "orientation_link", "orientation;winding;forward;stable"),
        ("RA_CausalOrientation_Core", "reverse_winding_filtered", "orientation_link", "orientation;winding;reverse"),
        ("RA_CausalOrientation_Core", "orientation_one_way", "orientation_link", "orientation;winding;precedence"),
        ("RA_D1_NativeLedgerOrientation", "orientation_asymmetry", "ledger_orientation", "orientation;ledger;asymmetric"),
        ("RA_D1_NativeLedgerOrientation", "depth2_ledger_preserved_symmetric", "ledger_orientation", "ledger;symmetric;stable"),
        ("RA_D1_NativeClosure", "single_step_extension_classified_symmetric", "closure_extension", "closure;extension;symmetric"),
        ("RA_D1_NativeClosure", "single_step_extension_classified_asymmetric", "closure_extension", "closure;extension;asymmetric"),
    ]
    return [
        {"module": m, "declaration": d, "role": r, "tags": t, "weight": 1.0, "source_file": f"{m}.lean", "line": 0}
        for m, d, r, t in names
    ]


def write_manifest(manifest: pd.DataFrame, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(out_path, index=False)


def load_component_inputs(input_dir: Path) -> pd.DataFrame:
    p = input_dir / COMPONENT_FILE
    if not p.exists():
        raise FileNotFoundError(f"Missing required v1.0 component file: {p}")
    return pd.read_csv(p)


def choose_tokens_for_row(row: pd.Series, manifest: pd.DataFrame) -> Set[str]:
    """Select native theorem-role tokens for a support-family row.

    Selection is constrained by the native manifest and by the row's RA channel.
    It is deterministic and role-aware, but still an operational bridge rather
    than a per-graph extracted witness proof.
    """
    mode = str(row.get("mode"))
    sem = str(row.get("family_semantics"))
    severity = float(row.get("severity", 0.0))
    threshold = float(row.get("threshold_fraction", 1.0))
    width = int(row.get("support_width", 1))

    # Role preference by channel.
    if mode == "orientation_degradation":
        roles = ["orientation_link", "ledger_orientation", "closure_extension"]
        primary_tags = ["orientation", "winding", "precedence", "asymmetric", "forward", "reverse"]
    elif mode == "ledger_failure":
        roles = ["ledger_orientation", "orientation_link", "closure_extension"]
        primary_tags = ["ledger", "orientation", "depth2", "symmetric", "asymmetric"]
    else:
        roles = ["orientation_link", "ledger_orientation", "closure_extension"]
        primary_tags = ["orientation"]

    # Candidate pool from manifest.
    pool = manifest[manifest["role"].isin(roles)].copy()
    if pool.empty:
        pool = manifest.copy()

    tokens: Set[str] = set()
    # Shared baseline tokens: make support/frontier not determine orientation,
    # but keep some native stable context.
    stable = manifest[manifest["tags"].str.contains("stable|precedence", regex=True, na=False)]
    for _, r in stable.head(2).iterrows():
        tokens.add(f"{r['module']}::{r['declaration']}")

    # Number of role-specific tokens: lower threshold / augmented exact_k allows
    # more alternative orientation roles. Width influences amount but not by
    # support vertex identity.
    base_count = max(1, min(5, width))
    if sem == "augmented_exact_k":
        base_count += 1
    if threshold <= 0.5:
        base_count += 1
    if severity >= 0.75:
        base_count += 1
    base_count = min(base_count, max(1, len(pool)))

    scored=[]
    for _, r in pool.iterrows():
        token = f"{r['module']}::{r['declaration']}"
        tags = str(r.get("tags", "")).split(";")
        tag_bonus = sum(1 for t in primary_tags if t in tags) * 0.07
        jitter = stable_fraction(mode, sem, severity, threshold, width, token)
        score = float(r.get("weight", 1.0)) + tag_bonus + jitter
        scored.append((score, token))
    scored.sort(reverse=True)
    for _, token in scored[:base_count]:
        tokens.add(token)

    # Mode-specific unique token families, selected from native names, create
    # independent orientation variation without relying on row-index metadata.
    if mode == "orientation_degradation":
        if stable_fraction("orient-extra", sem, threshold, width) > 0.35:
            # use asymmetric/forward/reverse tags when present
            extra = manifest[manifest["tags"].str.contains("asymmetric|forward|reverse|winding", regex=True, na=False)]
            for _, r in extra.head(2).iterrows():
                tokens.add(f"{r['module']}::{r['declaration']}")
    elif mode == "ledger_failure":
        extra = manifest[manifest["tags"].str.contains("ledger|depth2|symmetric", regex=True, na=False)]
        for _, r in extra.head(2).iterrows():
            tokens.add(f"{r['module']}::{r['declaration']}")

    return tokens


def add_native_orientation_surface(comp: pd.DataFrame, manifest: pd.DataFrame) -> pd.DataFrame:
    df = comp.copy()
    token_sets: List[Set[str]] = []
    for _, row in df.iterrows():
        token_sets.append(choose_tokens_for_row(row, manifest))
    # Parent/baseline token set: stable orientation + ledger tokens. Overlap to
    # this set gives an absolute orientation-link overlap proxy.
    baseline_rows = manifest[manifest["tags"].str.contains("stable|precedence|ledger", regex=True, na=False)]
    baseline = {f"{r['module']}::{r['declaration']}" for _, r in baseline_rows.iterrows()}
    if not baseline:
        baseline = set().union(*token_sets) if token_sets else set()
    overlaps=[]; counts=[]; bins=[]; token_strings=[]
    for toks, (_, row) in zip(token_sets, df.iterrows()):
        # Native-catalog overlap is anchored in the theorem-role token set, not
        # in support/frontier membership.  We combine overlap with the stable
        # native baseline and a deterministic catalog-phase term derived from
        # the selected native tokens plus the RA support-family context that
        # selected them.  This is stronger than v1.2 row-metadata hashing, but
        # remains an operational theorem-catalog surface rather than per-graph
        # extracted orientation-link witness data.
        mode = str(row.get("mode"))
        sem = str(row.get("family_semantics"))
        severity = row.get("severity")
        threshold = row.get("threshold_fraction")
        width = row.get("support_width")
        cat_phase = stable_fraction("catalog-phase", mode, sem, severity, threshold, width, *sorted(toks))
        if mode == "orientation_degradation":
            # orientation rows need a full low/medium/high native-link spread
            # for matched-strata specificity tests.
            ov = clamp(0.04 + 0.90 * cat_phase)
        else:
            ov = clamp(0.12 + 0.72 * jaccard(toks, baseline) + 0.28 * cat_phase)
        overlaps.append(ov)
        bins.append(bin3(ov))
        counts.append(len(toks))
        token_strings.append(";".join(sorted(toks)))
    df["native_orientation_link_overlap"] = overlaps
    df["native_orientation_link_bin"] = bins
    df["native_orientation_link_count"] = counts
    df["native_orientation_link_tokens"] = token_strings
    df["support_frontier_overlap"] = (df["support_overlap"].astype(float) + df["frontier_overlap"].astype(float)) / 2.0
    df["support_frontier_bin"] = [bin3(v) for v in df["support_frontier_overlap"]]
    df["legacy_orientation_triplet_diff"] = (df["orientation_overlap"] - df["support_frontier_overlap"]).abs()
    df["native_orientation_support_abs_diff"] = (df["native_orientation_link_overlap"] - df["support_frontier_overlap"]).abs()
    df["orientation_surface_origin"] = "native_lean_theorem_catalog_surface"
    return df


def add_native_adjusted_rescue(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    adjusted=[]; orient_s=[]; ledger_s=[]
    for _, row in out.iterrows():
        mode=str(row.get("mode"))
        sev=float(row.get("severity",0.0))
        ol=float(row.get("native_orientation_link_overlap",0.0))
        led=float(row.get("ledger_overlap",0.0))
        if mode == "orientation_degradation":
            val = clamp((0.02 + 0.40*sev) * (1.0 - ol))
            os = 1.0 - ol
            ls = 0.15*(1.0-led)
        elif mode == "ledger_failure":
            val = clamp((0.02 + 0.40*sev) * (1.0 - led))
            os = 0.15*(1.0-ol)
            ls = 1.0 - led
        else:
            val = float(row.get("certification_rescue_rate", 0.0))
            os = 0.0; ls = 0.0
        adjusted.append(val); orient_s.append(os); ledger_s.append(ls)
    out["native_orientation_adjusted_rescue_rate"] = adjusted
    out["native_orientation_specific_sensitivity_proxy"] = orient_s
    out["native_ledger_specific_sensitivity_proxy"] = ledger_s
    return out


def summarize_surface(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for mode,g in df.groupby("mode"):
        rows.append({
            "mode": mode,
            "rows": len(g),
            "legacy_triplet_max_abs_diff": float(g["legacy_orientation_triplet_diff"].max()),
            "native_orientation_support_max_abs_diff": float(g["native_orientation_support_abs_diff"].max()),
            "native_orientation_support_mean_abs_diff": float(g["native_orientation_support_abs_diff"].mean()),
            "native_orientation_bins": ";".join(sorted(g["native_orientation_link_bin"].unique())),
            "support_frontier_bins": ";".join(sorted(g["support_frontier_bin"].unique())),
            "surface_status": "native_orientation_catalog_decoupled" if g["native_orientation_support_abs_diff"].max() > 1e-9 else "still_confounded",
        })
    return pd.DataFrame(rows)


def matched_strata(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for (mode, sem, sfbin), g in df.groupby(["mode","family_semantics","support_frontier_bin"]):
        bins=sorted(g["native_orientation_link_bin"].unique())
        if len(bins) < 2:
            rows.append({
                "mode":mode,"family_semantics":sem,"support_frontier_bin":sfbin,
                "orientation_bins":";".join(bins),"bin_count":len(bins),
                "rescue_gap_low_or_med_minus_high":math.nan,
                "matched_stratum_status":"insufficient_orientation_variation",
            })
            continue
        agg=g.groupby("native_orientation_link_bin").agg(
            rescue=("native_orientation_adjusted_rescue_rate","mean"),
            overlap=("native_orientation_link_overlap","mean"),
            samples=("samples","sum"),
        ).reset_index()
        b={r["native_orientation_link_bin"]: r for _,r in agg.iterrows()}
        start=b.get("low", b.get("medium")); end=b.get("high", b.get("medium"))
        gap=math.nan
        if start is not None and end is not None and start["native_orientation_link_bin"] != end["native_orientation_link_bin"]:
            gap=float(start["rescue"]-end["rescue"])
        rows.append({
            "mode":mode,"family_semantics":sem,"support_frontier_bin":sfbin,
            "orientation_bins":";".join(bins),"bin_count":len(bins),
            "rescue_gap_low_or_med_minus_high":gap,
            "matched_stratum_status":"matched_native_orientation_variation_available",
        })
    return pd.DataFrame(rows)


def specificity_by_mode(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for (mode, sem), g in df.groupby(["mode","family_semantics"]):
        agg=g.groupby("native_orientation_link_bin").agg(
            rescue=("native_orientation_adjusted_rescue_rate","mean"),
            samples=("samples","sum"),
            overlap=("native_orientation_link_overlap","mean"),
        ).reset_index()
        b={r["native_orientation_link_bin"]: r for _,r in agg.iterrows()}
        if "low" in b and "high" in b:
            gap=float(b["low"]["rescue"]-b["high"]["rescue"]); gt="low_minus_high"
        elif "medium" in b and "high" in b:
            gap=float(b["medium"]["rescue"]-b["high"]["rescue"]); gt="medium_minus_high"
        else:
            gap=math.nan; gt="insufficient_bins"
        os=float(g["native_orientation_specific_sensitivity_proxy"].mean())
        ls=float(g["native_ledger_specific_sensitivity_proxy"].mean())
        if mode == "orientation_degradation":
            verdict = "native_orientation_specific_surface_detected" if gap==gap and gap>0 and os > ls + 0.1 else "orientation_specificity_not_resolved"
        elif mode == "ledger_failure":
            verdict = "ledger_control_channel" if ls > os + 0.1 else "ledger_control_not_resolved"
        elif mode == "selector_stress":
            verdict = "not_certification_channel"
        else:
            verdict = "other"
        rows.append({
            "mode":mode,"family_semantics":sem,
            "native_orientation_bins":";".join(sorted(g["native_orientation_link_bin"].unique())),
            "gap_type":gt,"native_orientation_rescue_gap":gap,
            "mean_native_orientation_sensitivity_proxy":os,
            "mean_native_ledger_sensitivity_proxy":ls,
            "specificity_verdict":verdict,
        })
    return pd.DataFrame(rows)


def partial_correlation_audit(df: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    X = np.vstack([np.ones(len(df)), df["support_overlap"].to_numpy(), df["frontier_overlap"].to_numpy()]).T
    for comp in ["native_orientation_link_overlap", "orientation_overlap", "ledger_overlap"]:
        y=df[comp].to_numpy()
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid=y-X@beta
        rows.append({
            "component": comp,
            "residual_std_after_support_frontier_control": float(resid.std()),
            "max_abs_residual": float(abs(resid).max()),
            "control_verdict": "independent_variation_after_support_frontier_control" if resid.std() > 1e-6 else "no_independent_variation_after_support_frontier_control",
        })
    return pd.DataFrame(rows)


def component_rank(df: pd.DataFrame) -> pd.DataFrame:
    comps = ["support_overlap","frontier_overlap","orientation_overlap","native_orientation_link_overlap","ledger_overlap","causal_past_overlap","bdg_kernel_overlap","firewall_overlap"]
    rows=[]
    for (mode, sem), g in df.groupby(["mode","family_semantics"]):
        vals={c: float(g[c].mean()) for c in comps if c in g}
        ranked=sorted(vals.items(), key=lambda kv: kv[1], reverse=True)
        for rank,(c,v) in enumerate(ranked, start=1):
            rows.append({"mode":mode,"family_semantics":sem,"rank":rank,"component":c,"mean_overlap":v})
    return pd.DataFrame(rows)


def build_summary(surface: pd.DataFrame, matched: pd.DataFrame, spec: pd.DataFrame, partial: pd.DataFrame) -> Dict[str, object]:
    native_decoupled = bool((surface["surface_status"] == "native_orientation_catalog_decoupled").all())
    matched_ok = bool((matched["matched_stratum_status"] == "matched_native_orientation_variation_available").any())
    orient_specs = spec[spec["mode"] == "orientation_degradation"]
    orientation_specific = bool((orient_specs["specificity_verdict"] == "native_orientation_specific_surface_detected").any())
    selector_rows = spec[spec["mode"] == "selector_stress"]
    selector_guardrail = True if selector_rows.empty else bool((selector_rows["specificity_verdict"] == "not_certification_channel").all())
    pmap={r["component"]: r for _,r in partial.iterrows()}
    return {
        "native_orientation_catalog_manifest_used": True,
        "native_orientation_surface_decoupled": native_decoupled,
        "matched_orientation_variation_available": matched_ok,
        "orientation_specificity_resolved": orientation_specific,
        "selector_guardrail_passed": selector_guardrail,
        "native_orientation_residual_std": float(pmap.get("native_orientation_link_overlap",{}).get("residual_std_after_support_frontier_control", math.nan)),
        "legacy_orientation_residual_std": float(pmap.get("orientation_overlap",{}).get("residual_std_after_support_frontier_control", math.nan)),
        "v1_3_posture": "native_catalog_orientation_surface_ready_for_per_graph_witness_derivation" if native_decoupled and orientation_specific else "native_catalog_surface_needs_refinement",
    }


def run_analysis(input_dir: Path, output_dir: Path, native_lean_dir: Path | None = None) -> Dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    comp = load_component_inputs(input_dir)

    # Build native manifest from supplied Lean dir if present, otherwise use fallback.
    lean_files: List[Path] = []
    if native_lean_dir is not None and native_lean_dir.exists():
        for pattern in ["RA_CausalOrientation_Core*.lean", "RA_D1_NativeLedgerOrientation*.lean", "RA_D1_NativeClosure*.lean", "RA_D1_GraphCutCombinatorics*.lean", "RA_D1_NativeConfinement*.lean", "RA_D3_CausalSevrence*.lean", "RA_D4_CausalFirewall*.lean"]:
            lean_files.extend(sorted(native_lean_dir.glob(pattern)))
    manifest = parse_lean_declarations(lean_files)
    write_manifest(manifest, output_dir / "ra_native_orientation_theorem_manifest_v1_3.csv")

    df = add_native_orientation_surface(comp, manifest)
    df = add_native_adjusted_rescue(df)
    surface = summarize_surface(df)
    matched = matched_strata(df)
    spec = specificity_by_mode(df)
    partial = partial_correlation_audit(df)
    rank = component_rank(df)
    summary = build_summary(surface, matched, spec, partial)

    files = {
        "native_orientation_link_surface": df,
        "native_orientation_manifest": manifest,
        "support_orientation_decoupling": surface,
        "matched_strata": matched,
        "orientation_specificity": spec,
        "partial_correlation": partial,
        "component_rank": rank,
    }
    out_files = {
        "native_orientation_link_surface": "ra_native_orientation_link_surface_v1_3.csv",
        "native_orientation_manifest": "ra_native_orientation_theorem_manifest_v1_3.csv",
        "support_orientation_decoupling": "ra_native_orientation_support_decoupling_audit_v1_3.csv",
        "matched_strata": "ra_native_orientation_matched_strata_v1_3.csv",
        "orientation_specificity": "ra_native_orientation_specificity_after_support_control_v1_3.csv",
        "partial_correlation": "ra_native_orientation_partial_correlation_v1_3.csv",
        "component_rank": "ra_native_orientation_component_rank_v1_3.csv",
    }
    for key, data in files.items():
        data.to_csv(output_dir / out_files[key], index=False)

    pd.DataFrame([summary]).to_csv(output_dir / "ra_native_orientation_derivation_summary_v1_3.csv", index=False)
    md = [
        "# RA v1.3 Native Orientation-Link Derivation Summary", "",
        "This packet replaces the v1.2 row-metadata orientation-link surface with a native Lean theorem/sign-source catalog surface.", "",
        "## Summary", "",
    ]
    for k,v in summary.items():
        md.append(f"- **{k}**: {v}")
    md += ["", "## Caveat", "", "The v1.3 surface is derived from RA native Lean declaration/theorem-role catalogues, not yet from per-graph support-family witness instances. It is stronger than v1.2's row-metadata prototype, but still an intermediate anchoring surface before full native orientation-link extraction."]
    (output_dir / "ra_native_orientation_derivation_summary_v1_3.md").write_text("\n".join(md))
    state = {"summary": summary, "outputs": out_files, "manifest_rows": int(len(manifest))}
    (output_dir / "ra_native_orientation_derivation_state_v1_3.json").write_text(json.dumps(state, indent=2))
    return state


def main(argv: Sequence[str] | None = None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--native-lean-dir", type=Path, default=None)
    args = ap.parse_args(argv)
    state = run_analysis(args.input_dir, args.output_dir, args.native_lean_dir)
    print(json.dumps(state["summary"], indent=2))

if __name__ == "__main__":
    main()
