#!/usr/bin/env python3
"""Static audit for Relational Actualism Python computation sources.

Outputs CSV/JSONL reports suitable for RAKB v0.5 claim-artifact review.
No third-party packages required.
"""
from __future__ import annotations

import argparse
import ast
import csv
import hashlib
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable

CLAIM_PATTERNS = [
    re.compile(r"\bRA-[A-Z0-9]+(?:-[A-Z0-9]+)*-\d{3}\b"),
    re.compile(r"\bD4U02\b"),
    re.compile(r"\bD[1-4][A-Z0-9_-]*\b"),
]

TERM_SETS = {
    "ra_native": [
        r"\bBDG\b", r"\bBenincasa\b", r"\bDowker\b", r"\bLLC\b", r"Local Ledger",
        r"actuali[sz]ation", r"potentia", r"severance", r"severed", r"causal\s+graph",
        r"DAG", r"ledger", r"motif", r"k[-_ ]?value", r"kval", r"cascade", r"firewall",
        r"recursive closure", r"assembly depth", r"source law", r"causal depth", r"birth term",
    ],
    "standard_qft_sm_bridge": [
        r"\bQCD\b", r"alpha_s", r"α_s", r"Lambda_QCD", r"Λ_QCD", r"PDG", r"Standard Model",
        r"\bSM\b", r"\bSU\(3\)", r"\bSU\(2\)", r"\bU\(1\)", r"Higgs", r"CKM", r"Cabibbo",
        r"Koide", r"QFT", r"quantum", r"Born rule", r"wavefunction", r"path integral",
        r"Lagrangian", r"Hamiltonian", r"gauge", r"Berry phase", r"Majorana", r"neutrino",
        r"quark", r"lepton", r"proton", r"neutron", r"pion", r"kaon",
    ],
    "gr_cosmology_bridge": [
        r"Einstein", r"metric", r"Ricci", r"Riemann", r"stress[- ]energy", r"geodesic",
        r"\bGR\b", r"dark matter", r"dark energy", r"ΛCDM", r"LCDM", r"DESI", r"\bw0\b", r"\bwa\b",
        r"Milne", r"Einstein[- ]de Sitter", r"\bEdS\b", r"Hubble", r"\bH0\b", r"lensing",
        r"Bullet Cluster", r"rotation curve", r"cosmic web", r"CMB", r"Axis of Evil",
    ],
    "empirical_or_physical_constants": [
        r"fine[- ]structure", r"alpha_EM", r"alpha_em", r"α", r"Planck", r"\bhbar\b", r"ℏ",
        r"speed of light", r"\bc\s*=", r"Newton", r"\bG\s*=", r"Boltzmann", r"\bk_B\b",
        r"eV", r"MeV", r"GeV", r"Mpc", r"km/s", r"solar mass", r"PDG",
    ],
    "execution_reproducibility": [
        r"random", r"np\.random", r"default_rng", r"seed", r"MCMC", r"Monte Carlo", r"sample",
        r"bootstrap", r"fit", r"curve_fit", r"minimize", r"optimizer", r"tolerance", r"tol",
    ],
}

IO_CALL_KEYWORDS = [
    "open", "read_text", "write_text", "read_bytes", "write_bytes", "read_csv", "to_csv",
    "loadtxt", "savetxt", "genfromtxt", "load", "save", "loadmat", "savemat",
    "json.load", "json.dump", "yaml.safe_load", "pickle.load", "pickle.dump", "savefig",
    "subprocess.run", "os.system",
]

RANDOM_CALL_KEYWORDS = ["random", "default_rng", "rand", "randn", "seed", "choice", "shuffle", "normal", "uniform", "poisson"]
PLOT_CALL_KEYWORDS = ["plot", "scatter", "hist", "imshow", "figure", "savefig", "show"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def strip_comments_and_docstrings(source: str) -> str:
    # Lightweight text version for term scans; AST still sees docstrings elsewhere.
    lines = []
    for line in source.splitlines():
        if line.lstrip().startswith("#"):
            continue
        lines.append(line)
    return "\n".join(lines)


def node_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = node_name(node.value)
        return f"{base}.{node.attr}" if base else node.attr
    if isinstance(node, ast.Call):
        return node_name(node.func)
    if isinstance(node, ast.Subscript):
        return node_name(node.value)
    if isinstance(node, ast.Constant):
        return repr(node.value)
    return ""


def literal_value(node: ast.AST) -> str:
    try:
        v = ast.literal_eval(node)
    except Exception:
        return "<nonliteral>"
    if isinstance(v, (list, tuple, dict, set)):
        s = repr(v)
        return s[:500] + ("..." if len(s) > 500 else "")
    return repr(v)


def target_names(target: ast.AST) -> list[str]:
    if isinstance(target, ast.Name):
        return [target.id]
    if isinstance(target, (ast.Tuple, ast.List)):
        out: list[str] = []
        for elt in target.elts:
            out.extend(target_names(elt))
        return out
    if isinstance(target, ast.Attribute):
        return [node_name(target)]
    return []


def line_context(lines: list[str], lineno: int, radius: int = 0) -> str:
    if lineno <= 0:
        return ""
    start = max(1, lineno - radius)
    end = min(len(lines), lineno + radius)
    return " ".join(lines[i - 1].strip() for i in range(start, end + 1))[:700]


def classify_path(path: Path) -> tuple[str, str]:
    p = str(path).lower()
    name = path.name.lower()
    domain = "general"
    role = "script"
    if "berry" in name:
        domain = "berry_phase"
    elif "d4u02" in name or "cross_dimensional" in name or "o14" in name:
        domain = "dimensionality_arithmetic"
    elif "d1" in name or "d2" in name or "d3" in name or "hadron" in name or "alpha_s" in name or "qcd" in name or "f0" in name:
        domain = "matter_interactions"
    elif any(k in name for k in ["dark", "desi", "lensing", "bullet", "rotation", "structure", "rindler", "cosmological"]):
        domain = "gravity_cosmology"
    elif any(k in name for k in ["thermo", "assembly", "complexity"]):
        domain = "complexity_life_thermo"
    elif "rakb" in p or "audit" in name or "validate" in name or "migrate" in name:
        domain = "kb_tooling"

    if any(k in name for k in ["proof", "derive", "derivation", "enumeration"]):
        role = "computational_derivation_candidate"
    elif any(k in name for k in ["benchmark", "verify", "forecast", "simulation", "mcmc"]):
        role = "computational_experiment_or_benchmark"
    elif any(k in name for k in ["table", "summary", "deliverables"]):
        role = "report_generator"
    elif domain == "kb_tooling":
        role = "kb_tool"
    return domain, role


def relpath(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except Exception:
        return str(path)


def find_py_files(repo: Path, roots: list[str]) -> list[Path]:
    out: list[Path] = []
    for r in roots:
        rp = (repo / r).resolve()
        if rp.is_file() and rp.suffix == ".py":
            out.append(rp)
        elif rp.is_dir():
            out.extend(sorted(p.resolve() for p in rp.rglob("*.py") if ".venv" not in p.parts and ".lake" not in p.parts))
    # dedupe while preserving order
    seen = set()
    dedup = []
    for p in out:
        if p not in seen:
            seen.add(p)
            dedup.append(p)
    return dedup


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fieldnames})


def scan_file(path: Path, repo: Path) -> dict[str, Any]:
    source = safe_read(path)
    lines = source.splitlines()
    text_no_comment = strip_comments_and_docstrings(source)
    rel = relpath(path, repo)
    domain, role = classify_path(Path(rel))
    result: dict[str, Any] = {
        "path": rel,
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "line_count": len(lines),
        "parse_status": "ok",
        "parse_error": "",
        "domain_guess": domain,
        "role_guess": role,
        "main_guard": "if __name__ == '__main__'" in source or 'if __name__ == "__main__"' in source,
        "function_count": 0,
        "class_count": 0,
        "import_count": 0,
        "constant_assignment_count": 0,
        "io_call_count": 0,
        "random_call_count": 0,
        "plot_call_count": 0,
        "claim_ref_count": 0,
        "bridge_hit_count": 0,
        "ra_native_hit_count": 0,
        "risk_score": 0,
    }
    records = {k: [] for k in [
        "imports", "defs", "constants", "numeric_literals", "io_calls", "randomness", "plot_calls",
        "claim_refs", "bridge_terms", "call_edges", "module_jsonl"
    ]}
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as e:
        result["parse_status"] = "syntax_error"
        result["parse_error"] = f"{e.msg} at {e.lineno}:{e.offset}"
        tree = None

    # text/term scan
    for pat in CLAIM_PATTERNS:
        for m in pat.finditer(source):
            lineno = source.count("\n", 0, m.start()) + 1
            records["claim_refs"].append({
                "path": rel, "lineno": lineno, "claim_ref": m.group(0), "context": line_context(lines, lineno)
            })
    result["claim_ref_count"] = len(records["claim_refs"])

    for category, patterns in TERM_SETS.items():
        for pattern in patterns:
            rgx = re.compile(pattern, flags=re.IGNORECASE)
            for m in rgx.finditer(source):
                lineno = source.count("\n", 0, m.start()) + 1
                rec = {"path": rel, "lineno": lineno, "category": category, "term": m.group(0), "pattern": pattern, "context": line_context(lines, lineno)}
                records["bridge_terms"].append(rec)
    result["ra_native_hit_count"] = sum(1 for r in records["bridge_terms"] if r["category"] == "ra_native")
    result["bridge_hit_count"] = sum(1 for r in records["bridge_terms"] if r["category"] != "ra_native")

    if tree is not None:
        parents: dict[ast.AST, ast.AST] = {}
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                parents[child] = parent

        # imports
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    records["imports"].append({"path": rel, "lineno": node.lineno, "kind": "import", "module": alias.name, "name": "", "asname": alias.asname or ""})
            elif isinstance(node, ast.ImportFrom):
                mod = "." * node.level + (node.module or "")
                for alias in node.names:
                    records["imports"].append({"path": rel, "lineno": node.lineno, "kind": "from_import", "module": mod, "name": alias.name, "asname": alias.asname or ""})
        result["import_count"] = len(records["imports"])

        # definitions with nesting stack
        def walk_defs(node: ast.AST, prefix: str = "") -> None:
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    kind = "class" if isinstance(child, ast.ClassDef) else ("async_function" if isinstance(child, ast.AsyncFunctionDef) else "function")
                    qn = f"{prefix}.{child.name}" if prefix else child.name
                    records["defs"].append({"path": rel, "lineno": child.lineno, "kind": kind, "name": child.name, "qualname": qn})
                    walk_defs(child, qn)
                else:
                    walk_defs(child, prefix)
        walk_defs(tree)
        result["function_count"] = sum(1 for r in records["defs"] if "function" in r["kind"])
        result["class_count"] = sum(1 for r in records["defs"] if r["kind"] == "class")

        # constants and calls
        current_def_stack: list[str] = []
        class Visitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
                current_def_stack.append(node.name)
                self.generic_visit(node)
                current_def_stack.pop()
            def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
                current_def_stack.append(node.name)
                self.generic_visit(node)
                current_def_stack.pop()
            def visit_ClassDef(self, node: ast.ClassDef) -> Any:
                current_def_stack.append(node.name)
                self.generic_visit(node)
                current_def_stack.pop()
            def visit_Assign(self, node: ast.Assign) -> Any:
                names: list[str] = []
                for t in node.targets:
                    names.extend(target_names(t))
                if names and isinstance(node.value, (ast.Constant, ast.Tuple, ast.List, ast.Dict, ast.Set)):
                    for nm in names:
                        if nm.isupper() or re.search(r"(alpha|lambda|mass|scale|sigma|theta|mu|kappa|h0|omega|coef|coeff|constant|pdg|qcd|higgs|proton|neutron|pion|f0)", nm, flags=re.I):
                            records["constants"].append({"path": rel, "lineno": node.lineno, "scope": ".".join(current_def_stack), "name": nm, "value": literal_value(node.value), "context": line_context(lines, node.lineno)})
                self.generic_visit(node)
            def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
                names = target_names(node.target)
                if names and node.value is not None and isinstance(node.value, (ast.Constant, ast.Tuple, ast.List, ast.Dict, ast.Set)):
                    for nm in names:
                        records["constants"].append({"path": rel, "lineno": node.lineno, "scope": ".".join(current_def_stack), "name": nm, "value": literal_value(node.value), "context": line_context(lines, node.lineno)})
                self.generic_visit(node)
            def visit_Constant(self, node: ast.Constant) -> Any:
                if isinstance(node.value, (int, float, complex)) and not isinstance(node.value, bool):
                    if node.value not in (0, 1, -1):
                        records["numeric_literals"].append({"path": rel, "lineno": getattr(node, "lineno", 0), "scope": ".".join(current_def_stack), "value": repr(node.value), "context": line_context(lines, getattr(node, "lineno", 0))})
                self.generic_visit(node)
            def visit_Call(self, node: ast.Call) -> Any:
                cname = node_name(node.func)
                lineno = getattr(node, "lineno", 0)
                lower = cname.lower()
                if any(k.lower() in lower for k in IO_CALL_KEYWORDS):
                    records["io_calls"].append({"path": rel, "lineno": lineno, "scope": ".".join(current_def_stack), "call": cname, "context": line_context(lines, lineno)})
                if any(k.lower() in lower for k in RANDOM_CALL_KEYWORDS):
                    records["randomness"].append({"path": rel, "lineno": lineno, "scope": ".".join(current_def_stack), "call": cname, "context": line_context(lines, lineno)})
                if any(k.lower() == lower.split(".")[-1] or k.lower() in lower for k in PLOT_CALL_KEYWORDS):
                    records["plot_calls"].append({"path": rel, "lineno": lineno, "scope": ".".join(current_def_stack), "call": cname, "context": line_context(lines, lineno)})
                if current_def_stack and cname:
                    records["call_edges"].append({"path": rel, "lineno": lineno, "src": ".".join(current_def_stack), "dst": cname})
                self.generic_visit(node)
        Visitor().visit(tree)

        result["constant_assignment_count"] = len(records["constants"])
        result["io_call_count"] = len(records["io_calls"])
        result["random_call_count"] = len(records["randomness"])
        result["plot_call_count"] = len(records["plot_calls"])

    risk = 0
    risk += min(result["bridge_hit_count"], 25)
    risk += 5 if result["random_call_count"] else 0
    risk += 4 if result["io_call_count"] else 0
    risk += 3 if result["plot_call_count"] else 0
    risk += 4 if result["claim_ref_count"] == 0 and role not in ("kb_tool", "report_generator") else 0
    risk += 6 if result["parse_status"] != "ok" else 0
    result["risk_score"] = risk

    records["module_jsonl"].append({"kind": "py_file_summary", **result})
    return {"summary": result, **records}


def build_markdown(summary_rows: list[dict[str, Any]], outdir: Path, repo: Path) -> str:
    total = len(summary_rows)
    parsed = sum(1 for r in summary_rows if r["parse_status"] == "ok")
    risk_sorted = sorted(summary_rows, key=lambda r: int(r.get("risk_score", 0)), reverse=True)
    domains: dict[str, int] = {}
    roles: dict[str, int] = {}
    for r in summary_rows:
        domains[r["domain_guess"]] = domains.get(r["domain_guess"], 0) + 1
        roles[r["role_guess"]] = roles.get(r["role_guess"], 0) + 1
    lines = []
    lines.append("# RA Python Computation Audit — Static Report")
    lines.append("")
    lines.append(f"Repository root: `{repo}`")
    lines.append(f"Python files scanned: **{total}**")
    lines.append(f"AST parse success: **{parsed}/{total}**")
    lines.append("")
    lines.append("## Domain distribution")
    for k, v in sorted(domains.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Role distribution")
    for k, v in sorted(roles.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Highest-priority review files")
    lines.append("")
    lines.append("These are ranked by a heuristic combining bridge-language hits, randomness, IO, plotting, parse problems, and missing explicit claim references. High score does not mean wrong; it means review first.")
    lines.append("")
    lines.append("| risk | path | domain | role | bridge hits | RA-native hits | IO | random | claim refs |")
    lines.append("|---:|---|---|---|---:|---:|---:|---:|---:|")
    for r in risk_sorted[:25]:
        lines.append(f"| {r['risk_score']} | `{r['path']}` | {r['domain_guess']} | {r['role_guess']} | {r['bridge_hit_count']} | {r['ra_native_hit_count']} | {r['io_call_count']} | {r['random_call_count']} | {r['claim_ref_count']} |")
    lines.append("")
    lines.append("## Generated outputs")
    for name in [
        "python_file_inventory.csv", "python_import_edges.csv", "python_declarations.csv", "python_constants.csv",
        "python_numeric_literals.csv", "python_io_calls.csv", "python_randomness.csv", "python_plot_calls.csv",
        "python_claim_refs.csv", "python_bridge_terms.csv", "python_call_edges.csv", "python_audit_graph.jsonl",
    ]:
        lines.append(f"- `{name}`")
    lines.append("")
    lines.append("## Evidence policy")
    lines.append("")
    lines.append("Static audit evidence is not yet computational reproduction evidence. Promote a Python artifact to `computes` or `reproduces` only after recording inputs, command, environment, output files, and deterministic/non-deterministic status.")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Static audit of RA Python computation sources.")
    ap.add_argument("--repo", default=".", help="RA repository root")
    ap.add_argument("--out", default="docs/RA_KB/reports/python_audit", help="Output directory")
    ap.add_argument("--roots", nargs="*", default=["src/RA_AQFT", "src/RA_Complexity", "data/DFT_Survey", "src/ra_audit.py"], help="Files or directories to scan")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    outdir = (repo / args.out).resolve() if not Path(args.out).is_absolute() else Path(args.out).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    files = find_py_files(repo, args.roots)
    all_records: dict[str, list[dict[str, Any]]] = {k: [] for k in [
        "summary", "imports", "defs", "constants", "numeric_literals", "io_calls", "randomness", "plot_calls", "claim_refs", "bridge_terms", "call_edges", "module_jsonl"
    ]}

    for path in files:
        scanned = scan_file(path, repo)
        for k in all_records:
            if k == "summary":
                all_records[k].append(scanned["summary"])
            else:
                all_records[k].extend(scanned.get(k, []))

    write_csv(outdir / "python_file_inventory.csv", all_records["summary"], [
        "path", "filename", "size_bytes", "sha256", "line_count", "parse_status", "parse_error", "domain_guess", "role_guess", "main_guard",
        "function_count", "class_count", "import_count", "constant_assignment_count", "io_call_count", "random_call_count", "plot_call_count",
        "claim_ref_count", "bridge_hit_count", "ra_native_hit_count", "risk_score"
    ])
    write_csv(outdir / "python_import_edges.csv", all_records["imports"], ["path", "lineno", "kind", "module", "name", "asname"])
    write_csv(outdir / "python_declarations.csv", all_records["defs"], ["path", "lineno", "kind", "name", "qualname"])
    write_csv(outdir / "python_constants.csv", all_records["constants"], ["path", "lineno", "scope", "name", "value", "context"])
    write_csv(outdir / "python_numeric_literals.csv", all_records["numeric_literals"], ["path", "lineno", "scope", "value", "context"])
    write_csv(outdir / "python_io_calls.csv", all_records["io_calls"], ["path", "lineno", "scope", "call", "context"])
    write_csv(outdir / "python_randomness.csv", all_records["randomness"], ["path", "lineno", "scope", "call", "context"])
    write_csv(outdir / "python_plot_calls.csv", all_records["plot_calls"], ["path", "lineno", "scope", "call", "context"])
    write_csv(outdir / "python_claim_refs.csv", all_records["claim_refs"], ["path", "lineno", "claim_ref", "context"])
    write_csv(outdir / "python_bridge_terms.csv", all_records["bridge_terms"], ["path", "lineno", "category", "term", "pattern", "context"])
    write_csv(outdir / "python_call_edges.csv", all_records["call_edges"], ["path", "lineno", "src", "dst"])

    with (outdir / "python_audit_graph.jsonl").open("w", encoding="utf-8") as f:
        for row in all_records["module_jsonl"]:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        for row in all_records["imports"]:
            f.write(json.dumps({"kind": "py_import", **row}, ensure_ascii=False) + "\n")
        for row in all_records["call_edges"]:
            f.write(json.dumps({"kind": "py_call", **row}, ensure_ascii=False) + "\n")
        for row in all_records["claim_refs"]:
            f.write(json.dumps({"kind": "py_claim_ref", **row}, ensure_ascii=False) + "\n")

    (outdir / "python_audit_report.md").write_text(build_markdown(all_records["summary"], outdir, repo), encoding="utf-8")
    print(f"Scanned {len(files)} Python files")
    print(f"Wrote reports to {outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
