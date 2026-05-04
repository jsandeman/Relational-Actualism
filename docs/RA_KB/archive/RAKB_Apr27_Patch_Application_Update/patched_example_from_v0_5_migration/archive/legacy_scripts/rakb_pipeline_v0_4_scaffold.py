
# Semi-Automated RAKB Pipeline (Python)

import yaml

def load_registry(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_registry(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)

def extract_results_from_sources(source_files):
    # placeholder: manual or assisted extraction
    return []

def update_registry(registry, new_results):
    existing_ids = {r['id'] for r in registry['results']}
    for r in new_results:
        if r['id'] not in existing_ids:
            registry['results'].append(r)
    return registry

def generate_latex_section(registry, paper_tag):
    lines = []
    for r in registry['results']:
        if paper_tag in r.get('paper', []):
            lines.append(f"\\paragraph{{{r['name']}}} ({r['status']})")
            lines.append(r['statement'])
    return "\n".join(lines)

def build_dependency_graph(registry):
    edges = []
    for r in registry['results']:
        for dep in r.get('dependencies', []):
            edges.append((dep, r['id']))
    return edges

def export_dot(edges, path):
    with open(path, 'w') as f:
        f.write("digraph RA {\n")
        for a,b in edges:
            f.write(f'  "{a}" -> "{b}";\n')
        f.write("}")

# Example usage:
registry = load_registry("RA_results_master.yaml")
edges = build_dependency_graph(registry)
export_dot(edges, "dependency_graph.dot")
