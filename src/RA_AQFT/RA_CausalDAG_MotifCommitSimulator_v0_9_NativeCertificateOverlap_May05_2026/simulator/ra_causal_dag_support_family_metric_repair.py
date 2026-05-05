#!/usr/bin/env python3
"""
RA causal-DAG motif-commit simulator v0.7.2 support-family metric repair.

v0.7.1 separated exact-k family replacement from monotone family augmentation.
A subsequent audit showed that one interpretation of the v0.7 certification
results was too coarse: comparing strict parent-cut loss against family-member
loss can be a metric-definition artifact when the parent cut is not a member of
an exact-k family.

This module repairs the metric layer. It keeps the v0.7.1 simulator semantics
unchanged, but adds apples-to-apples diagnostics:

  strict_parent_loss
      the parent support cut loses readiness.

  family_internal_loss
      the support-cut family loses any-cut readiness.

  strict_rescue
      the parent cut fails but some family cut remains ready.

  family_internal_survival
      at least one family cut remains ready under the intervention.

  comparison_valid
      strict-parent and family-member loss are compared only when they are in a
      common intervention domain. In cut-level certification modes, exact-k
      families with parent ∉ family.cuts are explicitly marked as incomparable
      for strict-vs-family loss deltas.

This is a metric repair / audit layer. It introduces no new Lean claims and no
new RA ontology.
"""
from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Mapping, Optional, Sequence, Tuple

try:
    from .ra_causal_dag_simulator import MotifCandidate, rows_to_csv
    from .ra_causal_dag_channel_workbench import SEVERANCE_MODES, build_channel_seed_state, target_motifs_for_channel_severance
    from .ra_causal_dag_support_family_monotonicity import (
        CERTIFICATION_MODES,
        CERTIFICATION_REGIMES,
        FAMILY_SEMANTICS,
        SupportFamilyMonotonicityConfig,
        evaluate_support_family_monotonicity,
        family_includes_strict_cut,
        support_family_by_semantics,
    )
    from .ra_causal_dag_simulator import motif_site
except ImportError:
    from ra_causal_dag_simulator import MotifCandidate, rows_to_csv, motif_site  # type: ignore
    from ra_causal_dag_channel_workbench import SEVERANCE_MODES, build_channel_seed_state, target_motifs_for_channel_severance  # type: ignore
    from ra_causal_dag_support_family_monotonicity import (  # type: ignore
        CERTIFICATION_MODES,
        CERTIFICATION_REGIMES,
        FAMILY_SEMANTICS,
        SupportFamilyMonotonicityConfig,
        evaluate_support_family_monotonicity,
        family_includes_strict_cut,
        support_family_by_semantics,
    )


@dataclass(frozen=True)
class MetricRepairConfig:
    """Parameters for the v0.7.2 metric-repair audit."""

    seeds: Tuple[int, ...] = tuple(range(17, 21))
    steps: int = 16
    max_parents: int = 4
    target_frontier_min: int = 5
    branch_probability: float = 0.42
    wide_join_probability: float = 0.72
    conflict_rate: float = 0.22
    defect_rate: float = 0.02
    orientation_defect_rate: float = 0.02
    conflict_witness_defect_rate: float = 0.08
    severance_seeds: Tuple[int, ...] = (101, 103)
    severities: Tuple[float, ...] = (0.0, 0.25, 0.50, 0.75, 1.0)
    modes: Tuple[str, ...] = SEVERANCE_MODES
    threshold_fractions: Tuple[float, ...] = (1.0, 0.75, 0.50, 0.25)
    family_semantics: Tuple[str, ...] = FAMILY_SEMANTICS
    certification_regimes: Tuple[str, ...] = CERTIFICATION_REGIMES
    include_alternatives: bool = False
    max_targets: Optional[int] = 8
    sample_limit: int = 1000

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> "MetricRepairConfig":
        seeds = tuple(range(args.seed_start, args.seed_stop)) if args.seed_list is None else tuple(int(x) for x in args.seed_list.split(",") if x.strip())
        return cls(
            seeds=seeds,
            steps=args.steps,
            max_parents=args.max_parents,
            target_frontier_min=args.target_frontier_min,
            branch_probability=args.branch_probability,
            wide_join_probability=args.wide_join_probability,
            conflict_rate=args.conflict_rate,
            defect_rate=args.defect_rate,
            orientation_defect_rate=args.orientation_defect_rate,
            conflict_witness_defect_rate=args.conflict_witness_defect_rate,
            severance_seeds=tuple(int(x) for x in args.severance_seeds.split(",") if x.strip()),
            severities=tuple(float(x) for x in args.severities.split(",") if x.strip()),
            modes=tuple(x.strip() for x in args.modes.split(",") if x.strip()),
            threshold_fractions=tuple(float(x) for x in args.threshold_fractions.split(",") if x.strip()),
            family_semantics=tuple(x.strip() for x in args.family_semantics.split(",") if x.strip()),
            certification_regimes=tuple(x.strip() for x in args.certification_regimes.split(",") if x.strip()),
            include_alternatives=args.include_alternatives,
            max_targets=None if args.max_targets < 0 else args.max_targets,
            sample_limit=args.sample_limit,
        )

    def monotonicity_config(self, seed: int) -> SupportFamilyMonotonicityConfig:
        return SupportFamilyMonotonicityConfig(
            seeds=(seed,),
            steps=self.steps,
            max_parents=self.max_parents,
            target_frontier_min=self.target_frontier_min,
            branch_probability=self.branch_probability,
            wide_join_probability=self.wide_join_probability,
            conflict_rate=self.conflict_rate,
            defect_rate=self.defect_rate,
            orientation_defect_rate=self.orientation_defect_rate,
            conflict_witness_defect_rate=self.conflict_witness_defect_rate,
            severance_seeds=self.severance_seeds,
            severities=self.severities,
            modes=self.modes,
            threshold_fractions=self.threshold_fractions,
            family_semantics=self.family_semantics,
            certification_regimes=self.certification_regimes,
            include_alternatives=self.include_alternatives,
            max_targets=self.max_targets,
            sample_limit=self.sample_limit,
        )


def _rate(rows: Sequence[Mapping[str, object]], key: str) -> float:
    return round(sum(1 for r in rows if bool(r.get(key))) / len(rows), 6) if rows else 0.0


def _mean(values: Sequence[float]) -> Optional[float]:
    return round(sum(values) / len(values), 6) if values else None


def _numeric(rows: Sequence[Mapping[str, object]], key: str) -> List[float]:
    out: List[float] = []
    for r in rows:
        v = r.get(key)
        if v not in (None, ""):
            out.append(float(v))
    return out


def _is_certification_metric_mismatch(row: Mapping[str, object]) -> bool:
    return (
        str(row.get("mode")) in CERTIFICATION_MODES
        and str(row.get("certification_regime")) == "cut_level"
        and not bool(row.get("family_includes_strict_cut"))
    )


def enrich_metric_repair_row(row: Mapping[str, object]) -> Dict[str, object]:
    """Add corrected v0.7.2 metric fields to one v0.7.1 row."""
    enriched = dict(row)
    mode = str(row.get("mode"))
    regime = str(row.get("certification_regime"))
    parent_in_family = bool(row.get("family_includes_strict_cut"))
    strict_before = bool(row.get("strict_before_ready"))
    strict_after = bool(row.get("strict_after_ready"))
    family_before = bool(row.get("family_before_ready"))
    family_after = bool(row.get("family_after_ready"))
    strict_loss = strict_before and not strict_after
    family_loss = family_before and not family_after
    severity = float(row.get("severity", 0.0))
    family_size = int(row.get("family_size", 0))
    uncertified_count = int(row.get("uncertified_cut_count", 0))

    cert_mode = mode in CERTIFICATION_MODES
    parent_targeted = False
    family_targeted = False
    if cert_mode and severity > 0:
        family_targeted = family_size > 0
        parent_targeted = regime == "parent_shared" or parent_in_family
    elif mode in {"edge_dropout", "frontier_dropout", "support_delay"} and severity > 0:
        parent_targeted = True
        family_targeted = True
    elif mode == "selector_stress" and severity > 0:
        parent_targeted = False
        family_targeted = False

    comparison_valid = not _is_certification_metric_mismatch(row)
    if cert_mode and regime == "parent_shared":
        targeting_domain = "shared_parent_certificate"
    elif cert_mode and parent_in_family:
        targeting_domain = "family_member_domain_includes_parent"
    elif cert_mode:
        targeting_domain = "family_member_domain_excludes_parent"
    elif mode == "selector_stress":
        targeting_domain = "selector_exclusion_domain"
    elif mode == "support_delay":
        targeting_domain = "support_delay_domain"
    elif mode == "frontier_dropout":
        targeting_domain = "support_availability_domain"
    elif mode == "edge_dropout":
        targeting_domain = "causal_reachability_domain"
    else:
        targeting_domain = "other_domain"

    family_internal_survival = family_before and family_after
    family_internal_resilience = severity > 0 and family_targeted and family_internal_survival
    strict_parent_survival = strict_before and strict_after
    strict_rescue = strict_loss and family_after
    apples_to_apples_loss_delta: object
    if comparison_valid:
        apples_to_apples_loss_delta = int(family_loss) - int(strict_loss)
    else:
        apples_to_apples_loss_delta = ""

    certified_family_member_count = max(family_size - uncertified_count, 0)
    enriched.update({
        "v072_metric_repair": True,
        "certification_mode": cert_mode,
        "parent_cut_in_family": parent_in_family,
        "parent_targeted_by_intervention": parent_targeted,
        "family_targeted_by_intervention": family_targeted,
        "targeting_domain": targeting_domain,
        "strict_parent_loss": strict_loss,
        "strict_parent_survival": strict_parent_survival,
        "family_internal_loss": family_loss,
        "family_internal_survival": family_internal_survival,
        "strict_rescue_rate_event": strict_rescue,
        "family_internal_resilience_event": family_internal_resilience,
        "comparison_valid_strict_vs_family": comparison_valid,
        "metric_artifact_risk": (not comparison_valid) and severity > 0,
        "apples_to_apples_loss_delta": apples_to_apples_loss_delta,
        "certified_family_member_count": certified_family_member_count,
        "uncertified_family_member_fraction": round(uncertified_count / family_size, 6) if family_size else 0.0,
    })
    return enriched


def iter_metric_repair_rows_for_seed(config: MetricRepairConfig, seed: int) -> Iterator[Dict[str, object]]:
    base_config = config.monotonicity_config(seed)
    state = build_channel_seed_state(base_config.channel_config(seed), seed)
    targets = target_motifs_for_channel_severance(state.motifs, include_alternatives=config.include_alternatives, max_targets=config.max_targets)
    for severance_seed in config.severance_seeds:
        for mode in config.modes:
            for severity in config.severities:
                for motif in targets:
                    site = motif_site(motif)
                    if site < 0 or not motif.support_cut:
                        continue
                    for fraction in config.threshold_fractions:
                        for semantics in config.family_semantics:
                            for regime in config.certification_regimes:
                                row = evaluate_support_family_monotonicity(
                                    state,
                                    motif,
                                    site,
                                    threshold_fraction=fraction,
                                    family_semantics=semantics,
                                    certification_regime=regime,
                                    mode=mode,
                                    severity=float(severity),
                                    seed=int(severance_seed),
                                )
                                row["run_seed"] = seed
                                yield enrich_metric_repair_row(row)


def aggregate_metric_repair_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, float, float], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["family_semantics"]), str(r["certification_regime"]), str(r["mode"]), float(r["severity"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (semantics, regime, mode, severity, threshold), items in sorted(buckets.items()):
        valid = [r for r in items if bool(r.get("comparison_valid_strict_vs_family"))]
        deltas = [float(r.get("apples_to_apples_loss_delta")) for r in valid if r.get("apples_to_apples_loss_delta") not in (None, "")]
        out.append({
            "family_semantics": semantics,
            "certification_regime": regime,
            "mode": mode,
            "severity": severity,
            "threshold_fraction": threshold,
            "samples": len(items),
            "support_width_count": len({int(r.get("support_width", 0)) for r in items}),
            "mean_support_width": _mean([float(r.get("support_width", 0)) for r in items]),
            "mean_family_size": _mean([float(r.get("family_size", 0)) for r in items]),
            "parent_in_family_rate": _rate(items, "parent_cut_in_family"),
            "parent_targeted_rate": _rate(items, "parent_targeted_by_intervention"),
            "family_targeted_rate": _rate(items, "family_targeted_by_intervention"),
            "strict_parent_loss_rate": _rate(items, "strict_parent_loss"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "strict_rescue_rate": _rate(items, "strict_rescue_rate_event"),
            "family_internal_survival_rate": _rate(items, "family_internal_survival"),
            "family_internal_resilience_rate": _rate(items, "family_internal_resilience_event"),
            "comparison_valid_rate": _rate(items, "comparison_valid_strict_vs_family"),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
            "mean_apples_to_apples_loss_delta": _mean(deltas),
            "mean_certified_family_member_count": _mean([float(r.get("certified_family_member_count", 0)) for r in items]),
            "mean_uncertified_member_fraction": _mean([float(r.get("uncertified_family_member_fraction", 0.0)) for r in items]),
        })
    return out


def width_stratified_metric_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, float, float, int], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["family_semantics"]), str(r["certification_regime"]), str(r["mode"]), float(r["severity"]), float(r["threshold_fraction"]), int(r["support_width"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (semantics, regime, mode, severity, threshold, width), items in sorted(buckets.items()):
        valid = [r for r in items if bool(r.get("comparison_valid_strict_vs_family"))]
        deltas = [float(r.get("apples_to_apples_loss_delta")) for r in valid if r.get("apples_to_apples_loss_delta") not in (None, "")]
        out.append({
            "family_semantics": semantics,
            "certification_regime": regime,
            "mode": mode,
            "severity": severity,
            "threshold_fraction": threshold,
            "support_width": width,
            "samples": len(items),
            "family_size_mean": _mean([float(r.get("family_size", 0)) for r in items]),
            "parent_in_family_rate": _rate(items, "parent_cut_in_family"),
            "strict_parent_loss_rate": _rate(items, "strict_parent_loss"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "strict_rescue_rate": _rate(items, "strict_rescue_rate_event"),
            "family_internal_survival_rate": _rate(items, "family_internal_survival"),
            "family_internal_resilience_rate": _rate(items, "family_internal_resilience_event"),
            "comparison_valid_rate": _rate(items, "comparison_valid_strict_vs_family"),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
            "mean_apples_to_apples_loss_delta": _mean(deltas),
        })
    return out


def targeting_audit_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    buckets: Dict[Tuple[str, str, str, bool], List[Mapping[str, object]]] = {}
    for r in rows:
        buckets.setdefault((str(r["mode"]), str(r["certification_regime"]), str(r["targeting_domain"]), bool(r.get("parent_cut_in_family"))), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, regime, domain, parent_in_family), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "certification_regime": regime,
            "targeting_domain": domain,
            "parent_cut_in_family": parent_in_family,
            "samples": len(items),
            "parent_targeted_rate": _rate(items, "parent_targeted_by_intervention"),
            "family_targeted_rate": _rate(items, "family_targeted_by_intervention"),
            "comparison_valid_rate": _rate(items, "comparison_valid_strict_vs_family"),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
            "strict_parent_loss_rate": _rate(items, "strict_parent_loss"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "family_internal_survival_rate": _rate(items, "family_internal_survival"),
        })
    return out


def certification_resilience_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    filtered = [r for r in rows if bool(r.get("certification_mode")) and float(r.get("severity", 0.0)) > 0]
    buckets: Dict[Tuple[str, str, str, float, float, int, bool], List[Mapping[str, object]]] = {}
    for r in filtered:
        buckets.setdefault((str(r["mode"]), str(r["family_semantics"]), str(r["certification_regime"]), float(r["severity"]), float(r["threshold_fraction"]), int(r["support_width"]), bool(r.get("parent_cut_in_family"))), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, regime, severity, threshold, width, parent_in_family), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "family_semantics": semantics,
            "certification_regime": regime,
            "severity": severity,
            "threshold_fraction": threshold,
            "support_width": width,
            "parent_cut_in_family": parent_in_family,
            "samples": len(items),
            "family_size_mean": _mean([float(r.get("family_size", 0)) for r in items]),
            "certified_family_member_count_mean": _mean([float(r.get("certified_family_member_count", 0)) for r in items]),
            "uncertified_member_fraction_mean": _mean([float(r.get("uncertified_family_member_fraction", 0.0)) for r in items]),
            "strict_parent_loss_rate": _rate(items, "strict_parent_loss"),
            "family_internal_loss_rate": _rate(items, "family_internal_loss"),
            "family_internal_survival_rate": _rate(items, "family_internal_survival"),
            "family_internal_resilience_rate": _rate(items, "family_internal_resilience_event"),
            "metric_artifact_risk_rate": _rate(items, "metric_artifact_risk"),
        })
    return out


def artifact_flag_rows(rows: Sequence[Mapping[str, object]]) -> List[Dict[str, object]]:
    risky = [r for r in rows if bool(r.get("metric_artifact_risk"))]
    buckets: Dict[Tuple[str, str, float, float], List[Mapping[str, object]]] = {}
    for r in risky:
        buckets.setdefault((str(r["mode"]), str(r["family_semantics"]), float(r["severity"]), float(r["threshold_fraction"])), []).append(r)
    out: List[Dict[str, object]] = []
    for (mode, semantics, severity, threshold), items in sorted(buckets.items()):
        out.append({
            "mode": mode,
            "family_semantics": semantics,
            "severity": severity,
            "threshold_fraction": threshold,
            "samples_at_risk": len(items),
            "widths_at_risk": sorted({int(r.get("support_width", 0)) for r in items}),
            "reason": "cut-level certification samples family members while strict parent cut is absent from family.cuts",
            "invalid_comparison": "strict_parent_loss_rate_vs_family_internal_loss_rate",
        })
    return out


def run_metric_repair(config: MetricRepairConfig) -> Tuple[Dict[str, object], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]], List[Dict[str, object]]]:
    started = time.perf_counter()
    all_rows: List[Dict[str, object]] = []
    run_rows: List[Dict[str, object]] = []
    for seed in config.seeds:
        seed_rows = list(iter_metric_repair_rows_for_seed(config, seed))
        all_rows.extend(seed_rows)
        run_rows.append({
            "run_seed": seed,
            "evaluations": len(seed_rows),
            "support_width_classes": sorted({int(r.get("support_width", 0)) for r in seed_rows}),
            "metric_artifact_risk_rate": _rate(seed_rows, "metric_artifact_risk"),
            "strict_rescue_rate": _rate(seed_rows, "strict_rescue_rate_event"),
            "family_internal_resilience_rate": _rate(seed_rows, "family_internal_resilience_event"),
        })
    elapsed = time.perf_counter() - started
    apples = aggregate_metric_repair_rows(all_rows)
    width = width_stratified_metric_rows(all_rows)
    targeting = targeting_audit_rows(all_rows)
    cert = certification_resilience_rows(all_rows)
    flags = artifact_flag_rows(all_rows)
    valid_deltas = [float(r.get("apples_to_apples_loss_delta")) for r in all_rows if r.get("apples_to_apples_loss_delta") not in (None, "")]
    summary = {
        "version": "0.7.2",
        "run_count": len(config.seeds),
        "steps": config.steps,
        "actual_evaluations": len(all_rows),
        "elapsed_seconds": round(elapsed, 6),
        "evaluations_per_second": round(len(all_rows) / elapsed, 6) if elapsed else None,
        "support_width_classes": sorted({int(r.get("support_width", 0)) for r in all_rows}),
        "support_width_count": len({int(r.get("support_width", 0)) for r in all_rows}),
        "family_semantics": sorted({str(r.get("family_semantics")) for r in all_rows}),
        "certification_regimes": sorted({str(r.get("certification_regime")) for r in all_rows}),
        "threshold_fractions": sorted({float(r.get("threshold_fraction", 0.0)) for r in all_rows}),
        "strict_parent_losses": sum(1 for r in all_rows if bool(r.get("strict_parent_loss"))),
        "family_internal_losses": sum(1 for r in all_rows if bool(r.get("family_internal_loss"))),
        "strict_rescues": sum(1 for r in all_rows if bool(r.get("strict_rescue_rate_event"))),
        "family_internal_resilience_events": sum(1 for r in all_rows if bool(r.get("family_internal_resilience_event"))),
        "metric_artifact_risk_events": sum(1 for r in all_rows if bool(r.get("metric_artifact_risk"))),
        "comparison_valid_rate": _rate(all_rows, "comparison_valid_strict_vs_family"),
        "metric_artifact_risk_rate": _rate(all_rows, "metric_artifact_risk"),
        "mean_valid_apples_to_apples_loss_delta": _mean(valid_deltas),
    }
    return summary, run_rows, apples, width, targeting, cert, flags, all_rows[: config.sample_limit]


def write_summary_note(summary: Mapping[str, object], apples: Sequence[Mapping[str, object]], width: Sequence[Mapping[str, object]], targeting: Sequence[Mapping[str, object]], cert: Sequence[Mapping[str, object]], flags: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    best_resilience = sorted([r for r in cert if float(r.get("family_internal_survival_rate") or 0.0) > 0], key=lambda r: float(r.get("family_internal_survival_rate") or 0.0), reverse=True)[:10]
    high_risk = sorted(flags, key=lambda r: int(r.get("samples_at_risk") or 0), reverse=True)[:10]
    lines = [
        "# RA Support-Family Metric Repair — v0.7.2",
        "",
        "This analysis layer repairs the v0.7/v0.7.1 metric interpretation. It separates strict-parent rescue from family-internal survival and flags invalid cross-domain comparisons.",
        "",
        "## Scale",
        "",
        f"- run_count: {summary.get('run_count')}",
        f"- steps: {summary.get('steps')}",
        f"- actual_evaluations: {summary.get('actual_evaluations')}",
        f"- support_width_classes: {summary.get('support_width_classes')}",
        f"- comparison_valid_rate: {summary.get('comparison_valid_rate')}",
        f"- metric_artifact_risk_rate: {summary.get('metric_artifact_risk_rate')}",
        "",
        "## Corrected interpretation",
        "",
        "`strict_parent_loss_rate` and `family_internal_loss_rate` are not automatically comparable. In cut-level certification modes, exact-k families with the parent cut absent from family.cuts put the strict parent and the family members in different targeting domains.",
        "",
        "The correct family-internal question is whether some family member remains certified-ready under family-targeted stress. The correct strict-rescue question is whether the strict parent cut fails while a family member survives. These are distinct diagnostics.",
        "",
        "## Highest family-internal certification survival rows",
        "",
    ]
    if not best_resilience:
        lines.append("- No family-internal certification survival observed in this run.")
    for r in best_resilience:
        lines.append(
            f"- mode={r['mode']} semantics={r['family_semantics']} regime={r['certification_regime']} "
            f"sev={r['severity']} threshold={r['threshold_fraction']} width={r['support_width']} "
            f"survival={r['family_internal_survival_rate']} loss={r['family_internal_loss_rate']} "
            f"risk={r['metric_artifact_risk_rate']}"
        )
    lines += ["", "## Invalid strict-vs-family comparison flags", ""]
    if not high_risk:
        lines.append("- No metric-artifact risk rows observed.")
    for r in high_risk:
        lines.append(
            f"- mode={r['mode']} semantics={r['family_semantics']} severity={r['severity']} "
            f"threshold={r['threshold_fraction']} samples_at_risk={r['samples_at_risk']} widths={r['widths_at_risk']}"
        )
    lines += [
        "",
        "## RAKB caution",
        "",
        "The corrected claim is not that exact-k support families amplify certification failure. The corrected claim is that cross-threshold comparisons require width-stratified, parent-in-family-aware, apples-to-apples metrics. Certification resilience is a family-internal diagnostic unless the parent cut and family members share the same targeting domain.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_state(summary: Mapping[str, object], runs: Sequence[Mapping[str, object]], apples: Sequence[Mapping[str, object]], width: Sequence[Mapping[str, object]], targeting: Sequence[Mapping[str, object]], cert: Sequence[Mapping[str, object]], flags: Sequence[Mapping[str, object]], sample: Sequence[Mapping[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "version": "0.7.2",
        "summary": dict(summary),
        "runs": list(runs),
        "apples_to_apples": list(apples),
        "width_stratified": list(width),
        "targeting_audit": list(targeting),
        "certification_resilience": list(cert),
        "metric_artifact_flags": list(flags),
        "sample": list(sample),
    }, indent=2, sort_keys=True), encoding="utf-8")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run RA causal-DAG v0.7.2 support-family metric repair audit.")
    p.add_argument("--seed-start", type=int, default=17)
    p.add_argument("--seed-stop", type=int, default=21)
    p.add_argument("--seed-list", type=str, default=None)
    p.add_argument("--steps", type=int, default=16)
    p.add_argument("--max-parents", type=int, default=4)
    p.add_argument("--target-frontier-min", type=int, default=5)
    p.add_argument("--branch-probability", type=float, default=0.42)
    p.add_argument("--wide-join-probability", type=float, default=0.72)
    p.add_argument("--conflict-rate", type=float, default=0.22)
    p.add_argument("--defect-rate", type=float, default=0.02)
    p.add_argument("--orientation-defect-rate", type=float, default=0.02)
    p.add_argument("--conflict-witness-defect-rate", type=float, default=0.08)
    p.add_argument("--severance-seeds", type=str, default="101,103")
    p.add_argument("--severities", type=str, default="0.0,0.25,0.50,0.75,1.0")
    p.add_argument("--modes", type=str, default=",".join(SEVERANCE_MODES))
    p.add_argument("--threshold-fractions", type=str, default="1.0,0.75,0.5,0.25")
    p.add_argument("--family-semantics", type=str, default=",".join(FAMILY_SEMANTICS))
    p.add_argument("--certification-regimes", type=str, default=",".join(CERTIFICATION_REGIMES))
    p.add_argument("--include-alternatives", action="store_true")
    p.add_argument("--max-targets", type=int, default=8)
    p.add_argument("--sample-limit", type=int, default=1000)
    p.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return p


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = build_arg_parser().parse_args(argv)
    config = MetricRepairConfig.from_args(args)
    summary, runs, apples, width, targeting, cert, flags, sample = run_metric_repair(config)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    rows_to_csv([summary], out / "ra_support_family_metric_repair_summary_v0_7_2.csv")
    rows_to_csv(runs, out / "ra_support_family_metric_repair_runs_v0_7_2.csv")
    rows_to_csv(apples, out / "ra_support_family_apples_to_apples_v0_7_2.csv")
    rows_to_csv(width, out / "ra_support_family_width_stratified_metrics_v0_7_2.csv")
    rows_to_csv(targeting, out / "ra_support_family_targeting_audit_v0_7_2.csv")
    rows_to_csv(cert, out / "ra_support_family_certification_resilience_v0_7_2.csv")
    rows_to_csv(flags, out / "ra_support_family_metric_artifact_flags_v0_7_2.csv")
    rows_to_csv(sample, out / "ra_support_family_metric_repair_sample_v0_7_2.csv")
    write_summary_note(summary, apples, width, targeting, cert, flags, out / "ra_support_family_metric_repair_summary_v0_7_2.md")
    write_state(summary, runs, apples, width, targeting, cert, flags, sample, out / "ra_support_family_metric_repair_state_v0_7_2.json")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
