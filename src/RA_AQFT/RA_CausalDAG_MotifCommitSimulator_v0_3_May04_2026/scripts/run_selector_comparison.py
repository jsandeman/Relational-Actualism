#!/usr/bin/env python3
"""Run a small selector-mode comparison for the v0.3 RA causal-DAG simulator."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulator.ra_causal_dag_simulator import generate_growth_demo, rows_to_csv, summarize_run


def main() -> None:
    out = []
    modes = [
        ("none", "lexicographic"),
        ("greedy", "lexicographic"),
        ("greedy", "stalemate"),
    ]
    for selector_mode, selector_tie_policy in modes:
        dag, motifs, rows, _support_rows, _selector_rows = generate_growth_demo(
            steps=24,
            seed=17,
            max_parents=3,
            conflict_rate=0.30,
            defect_rate=0.12,
            selector_mode=selector_mode,
            selector_tie_policy=selector_tie_policy,
        )
        out.append({
            "selector_mode": selector_mode,
            "selector_tie_policy": selector_tie_policy,
            "seed": 17,
            "steps": 24,
            "nodes": len(dag.nodes),
            "edges": len(dag.edges),
            "motifs": len(motifs),
            "conflict_rate": 0.30,
            "defect_rate": 0.12,
            **summarize_run(rows),
        })
    rows_to_csv(out, Path("outputs/ra_causal_dag_selector_comparison_v0_3.csv"))
    print("wrote outputs/ra_causal_dag_selector_comparison_v0_3.csv")


if __name__ == "__main__":
    main()
