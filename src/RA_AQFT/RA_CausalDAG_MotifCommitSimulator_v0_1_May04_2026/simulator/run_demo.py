#!/usr/bin/env python3
from pathlib import Path

from ra_causal_dag_simulator import dump_state_json, generate_growth_demo, rows_to_csv


if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "outputs"
    dag, motifs, rows = generate_growth_demo(steps=24, seed=17, max_parents=3, conflict_rate=0.30)
    rows_to_csv(rows, out / "ra_causal_dag_demo_summary.csv")
    dump_state_json(dag, motifs, rows, out / "ra_causal_dag_demo_state.json")
    print(f"nodes={len(dag.nodes)} edges={len(dag.edges)} motifs={len(motifs)}")
    print(f"wrote {out / 'ra_causal_dag_demo_summary.csv'}")
    print(f"wrote {out / 'ra_causal_dag_demo_state.json'}")
