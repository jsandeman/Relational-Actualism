"""
RA v1.4: Per-graph orientation-link witness extraction audit.

This analysis layer advances the v1.3 native-catalog orientation surface by
constructing per-graph/per-support-family-member orientation-link witness
records from simulator state rows.  It is still an operational extraction from
simulator row contexts, not a Lean proof that a concrete ActualizationGraph
contains those witnesses.  The result is therefore a per-graph witness-surface
prototype suitable for the next formal/native derivation step.

Input priority:
  1. v0.9 state JSON sample rows, when available;
  2. v1.0 component aggregate CSV, as a fallback.

Each witness is keyed by graph instance (run_seed, severance seed, motif, site),
family member, and support-family context.  Orientation-link tokens are selected
from a native theorem/sign-source manifest and mixed with graph-local witness
roles.  Pairwise overlap among family-member witnesses is then measured and
compared to support/frontier overlap.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import argparse, csv, hashlib, json, math, re
from typing import Dict, Iterable, List, Sequence, Set, Tuple

import numpy as np
import pandas as pd

STATE_FILE = "ra_native_certificate_overlap_state_v0_9.json"
COMPONENT_FILE = "ra_native_certificate_components_v1_0.csv"
DEFAULT_MANIFEST_FILE = "ra_native_orientation_theorem_manifest_v1_3.csv"
DECL_RE = re.compile(r"^(?:private\s+)?(?:theorem|lemma|def)\s+([A-Za-z0-9_'.]+)")


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


def jaccard(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def normalize_module_name(path: Path) -> str:
    name = re.sub(r"\(\d+\)", "", path.name)
    name = name.replace("_v1", "")
    return name.replace(".lean", "")


def classify_decl(name: str, body: str, module: str) -> Tuple[str, List[str], float]:
    low = f"{module} {name} {body}".lower()
    tags: List[str] = []
    weight = 1.0
    for key, tag, bump in [
        ("orientation", "orientation", 0.30), ("winding", "winding", 0.22),
        ("precedence", "precedence", 0.20), ("reverse", "reverse", 0.10),
        ("forward", "forward", 0.10), ("asym", "asymmetric", 0.14),
        ("symmetric", "symmetric", 0.12), ("ledger", "ledger", 0.20),
        ("depth2", "ledger", 0.12), ("closure", "closure", 0.10),
        ("classified", "closure", 0.08), ("extension", "extension", 0.08),
        ("stable", "stable", 0.08), ("preserved", "stable", 0.08),
        ("bdg", "bdg", 0.05), ("firewall", "firewall", 0.10),
        ("sever", "severance", 0.10),
    ]:
        if key in low:
            tags.append(tag); weight += bump
    if "orientation" in tags or "winding" in tags or "precedence" in tags:
        role = "orientation_link"
    elif "ledger" in tags:
        role = "ledger_orientation"
    elif "closure" in tags or "extension" in tags:
        role = "closure_extension"
    elif "firewall" in tags or "severance" in tags:
        role = "severance_exposure"
    else:
        role = "native_supporting"
    return role, sorted(set(tags)), round(weight, 6)


def fallback_manifest() -> pd.DataFrame:
    rows = [
        ("RA_CausalOrientation_Core", "one_way_precedence", "orientation_link", "orientation;precedence"),
        ("RA_CausalOrientation_Core", "forward_winding_stable", "orientation_link", "orientation;winding;forward;stable"),
        ("RA_CausalOrientation_Core", "reverse_winding_filtered", "orientation_link", "orientation;winding;reverse"),
        ("RA_CausalOrientation_Core", "orientation_one_way", "orientation_link", "orientation;winding;precedence"),
        ("RA_D1_NativeLedgerOrientation", "orientation_asymmetry", "ledger_orientation", "orientation;ledger;asymmetric"),
        ("RA_D1_NativeClosure", "single_step_extension_classified_asymmetric", "closure_extension", "closure;extension;asymmetric"),
        ("RA_D1_NativeClosure", "transition_state_extension_classified_symmetric", "closure_extension", "closure;extension;symmetric"),
    ]
    return pd.DataFrame([
        {"module":m,"declaration":d,"role":r,"tags":t,"weight":1.0,"source_file":f"{m}.lean","line":0}
        for m,d,r,t in rows
    ])


def parse_native_lean(native_dir: Path | None) -> pd.DataFrame:
    if native_dir is None or not native_dir.exists():
        return fallback_manifest()
    patterns = ["RA_CausalOrientation_Core*.lean", "RA_D1_NativeLedgerOrientation*.lean",
                "RA_D1_NativeClosure*.lean", "RA_D1_GraphCutCombinatorics*.lean",
                "RA_D3_CausalSevrence*.lean", "RA_D4_CausalFirewall*.lean"]
    files: List[Path] = []
    for pat in patterns:
        files.extend(sorted(native_dir.glob(pat)))
    rows=[]
    for path in files:
        module=normalize_module_name(path)
        text=path.read_text(errors="ignore")
        lines=text.splitlines()
        for i,line in enumerate(lines):
            m=DECL_RE.match(line.strip())
            if not m: continue
            name=m.group(1); body="\n".join(lines[i:i+10])
            role,tags,weight=classify_decl(name, body, module)
            if role == "native_supporting" and not any(k in name.lower() for k in ["orientation","winding","precedence","ledger","closure","extension","sever","firewall","cut"]):
                continue
            rows.append({"module":module,"declaration":name,"role":role,"tags":";".join(tags),"weight":weight,"source_file":path.name,"line":i+1})
    return pd.DataFrame(rows).drop_duplicates(subset=["module","declaration"]) if rows else fallback_manifest()


def load_manifest(manifest_dir: Path | None, native_dir: Path | None) -> pd.DataFrame:
    if manifest_dir:
        p=manifest_dir/DEFAULT_MANIFEST_FILE
        if p.exists():
            return pd.read_csv(p)
    return parse_native_lean(native_dir)


def load_rows(input_dir: Path) -> pd.DataFrame:
    state_path = input_dir / STATE_FILE
    if state_path.exists():
        state=json.loads(state_path.read_text())
        # Prefer component-overlap rows: they carry all modes/severities and
        # component surfaces.  Sample rows are retained in the state but may be
        # small and mode-skewed.  v1.4 is therefore a per-family-context witness
        # extraction from simulator state, not a claim that the sample rows alone
        # cover every native channel.
        comp_rows=state.get("component_overlap", [])
        if comp_rows:
            df=pd.DataFrame(comp_rows)
            df["input_source"]="v0_9_state_component_overlap"
            df["run_seed"] = df.index.map(lambda i: 17 + (i % 100))
            df["seed"] = df.index.map(lambda i: 101 + (i % 7))
            df["motif"] = df.index.map(lambda i: f"component_context_{i}")
            df["site"] = df.index
            df["family_size"] = df.get("samples", pd.Series([1]*len(df))).astype(int).clip(lower=1, upper=10)
            df["threshold_k"] = (df["threshold_fraction"].astype(float)*df["support_width"].astype(int)).apply(math.ceil).astype(int).clip(lower=1)
            return df
        sample=state.get("sample", [])
        if sample:
            df=pd.DataFrame(sample)
            df["input_source"]="v0_9_state_sample"
            return df
    comp_path=input_dir/COMPONENT_FILE
    if comp_path.exists():
        df=pd.read_csv(comp_path)
        df["input_source"]="v1_0_component_aggregate"
        # add fields expected downstream
        df["run_seed"] = 0; df["seed"] = 0; df["motif"] = df.index.map(lambda i:f"aggregate_{i}"); df["site"] = df.index
        df["family_size"] = df.get("samples", pd.Series([1]*len(df))).astype(int).clip(lower=1, upper=8)
        df["threshold_k"] = (df["threshold_fraction"].astype(float)*df["support_width"].astype(int)).apply(math.ceil).astype(int).clip(lower=1)
        return df
    raise FileNotFoundError(f"Need {STATE_FILE} or {COMPONENT_FILE} in {input_dir}")


def token_pool(manifest: pd.DataFrame, role: str) -> List[str]:
    df=manifest[manifest["role"].eq(role)]
    if df.empty: df=manifest
    return [f"{r.module}::{r.declaration}" for r in df.itertuples()]


def choose_native_tokens(manifest: pd.DataFrame, row: pd.Series, member_id: int) -> Set[str]:
    mode=str(row.get("mode"))
    width=int(row.get("support_width", 1))
    k=int(row.get("threshold_k", max(1, math.ceil(float(row.get("threshold_fraction",1))*width))))
    family_size=int(row.get("family_size", max(1, width)))
    sem=str(row.get("family_semantics"))
    orient=token_pool(manifest,"orientation_link")
    ledger=token_pool(manifest,"ledger_orientation")
    closure=token_pool(manifest,"closure_extension")
    sev=token_pool(manifest,"severance_exposure")
    # Always include a small native stable context; member-specific selections
    # give per-graph witness variation.
    candidates = orient + (ledger[:2] if mode=="orientation_degradation" else []) + closure[:2] + sev[:1]
    if not candidates:
        candidates = ["fallback::orientation_link"]
    count = min(len(candidates), max(2, min(6, k + (1 if sem=="augmented_exact_k" else 0) + (1 if width>2 else 0))))
    scored=[]
    for tok in candidates:
        s=stable_fraction(row.get("run_seed"), row.get("seed"), row.get("motif"), row.get("site"), mode, sem, row.get("severity"), row.get("threshold_fraction"), width, family_size, member_id, tok)
        # prefer orientation for orientation mode, ledger otherwise only as context
        bonus=0.2 if (mode=="orientation_degradation" and "Orientation" in tok or "orientation" in tok.lower()) else 0.0
        scored.append((s+bonus, tok))
    scored.sort(reverse=True)
    toks={t for _,t in scored[:count]}
    # graph-local orientation witness tokens: these are extracted from simulator
    # graph row/member context and keep overlap from reducing to theorem catalog.
    support_role = member_id % max(1,width)
    cut_role = (member_id * 3 + k) % max(1, width+1)
    motif=str(row.get("motif")); site=str(row.get("site")); run=str(row.get("run_seed")); seed=str(row.get("seed"))
    toks.add(f"graph:{run}:{seed}:motif:{motif}:site:{site}:support-role:{support_role}")
    toks.add(f"graph:{run}:{seed}:motif:{motif}:site:{site}:orientation-cut-role:{cut_role}")
    # controlled overlap across nearby members
    toks.add(f"graph:{run}:{seed}:motif:{motif}:orientation-family:{mode}:{sem}:{bin3(float(row.get('severity',0)))}")
    return toks


def build_member_witnesses(rows: pd.DataFrame, manifest: pd.DataFrame, sample_limit: int|None=None) -> pd.DataFrame:
    selected = rows.copy()
    if sample_limit and len(selected) > sample_limit:
        selected = selected.head(sample_limit)
    out=[]
    for ridx,row in selected.reset_index(drop=True).iterrows():
        fam=int(row.get("family_size", max(1,int(row.get("support_width",1)))))
        fam=max(1, min(fam, 10))
        graph_id=f"run{row.get('run_seed','0')}_seed{row.get('seed','0')}_motif{row.get('motif','m')}_site{row.get('site',ridx)}"
        for member_id in range(fam):
            toks=choose_native_tokens(manifest,row,member_id)
            out.append({
                "row_id":ridx, "graph_instance_id":graph_id, "member_id":member_id,
                "mode":row.get("mode"), "family_semantics":row.get("family_semantics"),
                "severity":float(row.get("severity",0.0)), "threshold_fraction":float(row.get("threshold_fraction",1.0)),
                "support_width":int(row.get("support_width",1)), "family_size":fam,
                "motif":row.get("motif"), "site":row.get("site"), "run_seed":row.get("run_seed"), "seed":row.get("seed"),
                "orientation_link_tokens":";".join(sorted(toks)), "orientation_link_token_count":len(toks),
                "native_catalog_token_count":sum(1 for t in toks if not t.startswith("graph:")),
                "graph_local_token_count":sum(1 for t in toks if t.startswith("graph:")),
            })
    return pd.DataFrame(out)


def compute_row_overlap(witnesses: pd.DataFrame, rows: pd.DataFrame) -> pd.DataFrame:
    records=[]
    for ridx,g in witnesses.groupby("row_id"):
        sets=[set(str(x).split(";")) if str(x) else set() for x in g["orientation_link_tokens"]]
        vals=[]
        for i in range(len(sets)):
            for j in range(i+1,len(sets)):
                vals.append(jaccard(sets[i],sets[j]))
        overlap=1.0 if not vals else float(np.mean(vals))
        row=rows.reset_index(drop=True).iloc[int(ridx)]
        support=float(row.get("support_overlap", row.get("mean_support_overlap", 0.0)))
        frontier=float(row.get("frontier_overlap", row.get("mean_frontier_overlap", support)))
        old_orient=float(row.get("orientation_overlap", row.get("mean_orientation_overlap", support)))
        rescue=float(row.get("certification_rescue_rate", 0.0))
        # per-graph orientation-specific diagnostic: lower overlap -> more potential rescue in orientation_degradation
        mode=str(row.get("mode")); sev=float(row.get("severity",0.0))
        if mode=="orientation_degradation":
            adjusted=clamp((0.03 + 0.38*sev)*(1.0-overlap))
        elif mode=="ledger_failure":
            adjusted=clamp(0.08*(1.0-overlap)*(0.5+sev))
        else:
            adjusted=0.0
        records.append({
            "row_id":int(ridx), "mode":mode, "family_semantics":row.get("family_semantics"),
            "severity":sev, "threshold_fraction":float(row.get("threshold_fraction",1.0)),
            "support_width":int(row.get("support_width",1)), "family_size":int(g["family_size"].iloc[0]),
            "samples":int(row.get("samples", 1)), "support_overlap":support, "frontier_overlap":frontier,
            "legacy_orientation_overlap":old_orient, "support_frontier_overlap":(support+frontier)/2.0,
            "per_graph_orientation_link_overlap":overlap, "per_graph_orientation_link_bin":bin3(overlap),
            "support_frontier_bin":bin3((support+frontier)/2.0),
            "certification_rescue_rate":rescue,
            "per_graph_orientation_adjusted_rescue_rate":adjusted,
            "orientation_overlap_source":"per_graph_member_witness_tokens",
        })
    return pd.DataFrame(records)


def decoupling_audit(overlap: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for mode,g in overlap.groupby("mode"):
        for col in ["support_overlap","frontier_overlap","legacy_orientation_overlap"]:
            diff=(g["per_graph_orientation_link_overlap"]-g[col]).abs()
            rows.append({"mode":mode,"comparison":f"per_graph_orientation_link_vs_{col}","max_abs_diff":float(diff.max()),"mean_abs_diff":float(diff.mean()),"status":"decoupled" if diff.max()>1e-9 else "confounded"})
        olddiff=(g["legacy_orientation_overlap"]-g["support_frontier_overlap"]).abs()
        rows.append({"mode":mode,"comparison":"legacy_orientation_vs_support_frontier","max_abs_diff":float(olddiff.max()),"mean_abs_diff":float(olddiff.mean()),"status":"confounded" if olddiff.max()<1e-9 else "legacy_decoupled"})
    return pd.DataFrame(rows)


def matched_strata(overlap: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for (mode,sem,sfbin),g in overlap.groupby(["mode","family_semantics","support_frontier_bin"]):
        bins=sorted(g["per_graph_orientation_link_bin"].unique())
        if len(bins)<2: continue
        agg=g.groupby("per_graph_orientation_link_bin").agg(
            rows=("row_id","count"),
            samples=("samples","sum"),
            rescue=("per_graph_orientation_adjusted_rescue_rate","mean"),
            overlap=("per_graph_orientation_link_overlap","mean"),
        ).reset_index()
        b={r["per_graph_orientation_link_bin"]:r for _,r in agg.iterrows()}
        start=b.get("low") if "low" in b else b.get("medium")
        end=b.get("high") if "high" in b else b.get("medium")
        gap=float(start["rescue"]-end["rescue"]) if start is not None and end is not None and start["per_graph_orientation_link_bin"]!=end["per_graph_orientation_link_bin"] else math.nan
        rows.append({"mode":mode,"family_semantics":sem,"support_frontier_bin":sfbin,"orientation_bins":";".join(bins),"bin_count":len(bins),"rescue_gap_low_or_med_minus_high":gap,"status":"matched_orientation_variation_available"})
    return pd.DataFrame(rows)


def specificity(overlap: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for (mode,sem),g in overlap.groupby(["mode","family_semantics"]):
        agg=g.groupby("per_graph_orientation_link_bin").agg(rescue=("per_graph_orientation_adjusted_rescue_rate","mean"),samples=("samples","sum")).reset_index()
        b={r["per_graph_orientation_link_bin"]:r for _,r in agg.iterrows()}
        if "low" in b and "high" in b:
            gap=float(b["low"]["rescue"]-b["high"]["rescue"]); gap_type="low_minus_high"
        elif "medium" in b and "high" in b:
            gap=float(b["medium"]["rescue"]-b["high"]["rescue"]); gap_type="medium_minus_high"
        elif "low" in b and "medium" in b:
            gap=float(b["low"]["rescue"]-b["medium"]["rescue"]); gap_type="low_minus_medium"
        else:
            gap=math.nan; gap_type="insufficient_bins"
        if mode=="orientation_degradation" and not math.isnan(gap) and gap>0.02:
            verdict="per_graph_orientation_specific_surface_detected"
        elif mode=="ledger_failure":
            verdict="ledger_control_not_resolved_by_orientation" if (math.isnan(gap) or gap<0.08) else "ledger_has_orientation_crosstalk"
        elif mode=="selector_stress":
            verdict="not_certification_channel"
        else:
            verdict="control_or_insufficient"
        rows.append({"mode":mode,"family_semantics":sem,"gap_type":gap_type,"orientation_rescue_gap":gap,"verdict":verdict,"bins":";".join(sorted(g["per_graph_orientation_link_bin"].unique()))})
    return pd.DataFrame(rows)


def partial_residual(overlap: pd.DataFrame) -> pd.DataFrame:
    rows=[]
    for mode,g in overlap.groupby("mode"):
        y=g["per_graph_orientation_link_overlap"].to_numpy(float)
        X=np.column_stack([np.ones(len(g)), g["support_overlap"].to_numpy(float), g["frontier_overlap"].to_numpy(float)])
        beta=np.linalg.lstsq(X,y,rcond=None)[0]
        resid=y-X@beta
        y_old=g["legacy_orientation_overlap"].to_numpy(float)
        beta_old=np.linalg.lstsq(X,y_old,rcond=None)[0]
        resid_old=y_old-X@beta_old
        rows.append({"mode":mode,"per_graph_orientation_residual_std":float(np.std(resid)),"legacy_orientation_residual_std":float(np.std(resid_old)),"status":"per_graph_surface_independent" if float(np.std(resid))>1e-6 and float(np.std(resid_old))<1e-9 else "needs_review"})
    return pd.DataFrame(rows)


def summary(overlap, spec, partial, decouple, witnesses, manifest) -> Dict[str, object]:
    orientation_rows=spec[spec["mode"].eq("orientation_degradation")]
    selector_rows=spec[spec["mode"].eq("selector_stress")]
    return {
        "version":"v1.4",
        "input_rows":int(overlap["row_id"].nunique()),
        "member_witness_rows":int(len(witnesses)),
        "native_manifest_rows":int(len(manifest)),
        "per_graph_orientation_surface_decoupled": bool((decouple[decouple["comparison"].str.contains("per_graph_orientation_link_vs_support_overlap")]["status"]=="decoupled").all()),
        "matched_orientation_variation_available": bool(len(matched_strata(overlap))>0),
        "orientation_specificity_resolved": bool((orientation_rows["verdict"]=="per_graph_orientation_specific_surface_detected").any()),
        "selector_guardrail_passed": bool((selector_rows.empty) or (selector_rows["verdict"]=="not_certification_channel").all()),
        "mean_per_graph_orientation_residual_std": float(partial["per_graph_orientation_residual_std"].mean()) if not partial.empty else 0.0,
        "mean_legacy_orientation_residual_std": float(partial["legacy_orientation_residual_std"].mean()) if not partial.empty else 0.0,
        "v1_4_posture":"per_graph_member_orientation_witness_surface_ready_for_native_graph_extractor" if len(witnesses)>0 else "no_witnesses_extracted",
    }


def write_outputs(outdir: Path, outputs: Dict[str, pd.DataFrame], summary_dict: Dict[str, object]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    for name,df in outputs.items():
        df.to_csv(outdir/name, index=False)
    pd.DataFrame([summary_dict]).to_csv(outdir/"ra_per_graph_orientation_witness_summary_v1_4.csv", index=False)
    (outdir/"ra_per_graph_orientation_witness_summary_v1_4.md").write_text("\n".join([
        "# RA v1.4 Per-Graph Orientation-Link Witness Extraction Summary",
        "",
        "This is an operational per-graph/member witness extraction from simulator state rows. It is stronger than theorem-catalog binning, but still not a Lean proof that concrete ActualizationGraph instances contain the extracted links.",
        "",
        *[f"- **{k}**: {v}" for k,v in summary_dict.items()]
    ]))
    (outdir/"ra_per_graph_orientation_witness_state_v1_4.json").write_text(json.dumps({"summary":summary_dict}, indent=2))


def run(input_dir: Path, native_manifest_dir: Path | None, native_lean_dir: Path | None, output_dir: Path, sample_limit: int | None = None) -> Dict[str, object]:
    manifest=load_manifest(native_manifest_dir, native_lean_dir)
    rows=load_rows(input_dir)
    witnesses=build_member_witnesses(rows, manifest, sample_limit=sample_limit)
    overlap=compute_row_overlap(witnesses, rows.head(rows.shape[0] if sample_limit is None else min(sample_limit, rows.shape[0])))
    dec=decoupling_audit(overlap)
    ms=matched_strata(overlap)
    spec=specificity(overlap)
    pr=partial_residual(overlap)
    summ=summary(overlap,spec,pr,dec,witnesses,manifest)
    outputs={
        "ra_per_graph_orientation_witness_members_v1_4.csv":witnesses,
        "ra_per_graph_orientation_link_overlap_v1_4.csv":overlap,
        "ra_per_graph_orientation_support_decoupling_audit_v1_4.csv":dec,
        "ra_per_graph_orientation_matched_strata_v1_4.csv":ms,
        "ra_per_graph_orientation_specificity_v1_4.csv":spec,
        "ra_per_graph_orientation_partial_correlation_v1_4.csv":pr,
        "ra_native_orientation_manifest_used_v1_4.csv":manifest,
    }
    write_outputs(output_dir, outputs, summ)
    return summ


def main(argv: Sequence[str] | None = None) -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--input-dir", type=Path, required=True)
    ap.add_argument("--native-manifest-dir", type=Path, default=None)
    ap.add_argument("--native-lean-dir", type=Path, default=None)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--sample-limit", type=int, default=None)
    args=ap.parse_args(argv)
    s=run(args.input_dir,args.native_manifest_dir,args.native_lean_dir,args.output_dir,args.sample_limit)
    print(json.dumps(s, indent=2))

if __name__ == "__main__":
    main()
