from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.graph import Graph


def _fmt_num(v):
    try:
        if float(v).is_integer():
            return str(int(v))
    except (TypeError, ValueError):
        pass
    return str(v)


def format_matrix(graph: "Graph") -> str:
    labels, m = graph.to_adjacency_matrix()
    if not labels:
        return ""
    header = "    " + "  ".join(f"{l:>3}" for l in labels)
    rows = [header]
    for i, lbl in enumerate(labels):
        row = f"{lbl:>3} " + "  ".join(f"{_fmt_num(v):>3}" for v in m[i])
        rows.append(row)
    return "\n".join(rows)


def format_adjacency_list(graph: "Graph") -> str:
    adj = graph.to_adjacency_list()
    lines = []
    for u in sorted(adj.keys()):
        if graph.weighted:
            parts = [f"{v}({_fmt_num(w)})" for v, w in adj[u]]
        else:
            parts = [v for v, _ in adj[u]]
        if parts:
            lines.append(f"{u}: " + ", ".join(parts))
        else:
            lines.append(f"{u}:")
    return "\n".join(lines)


def format_edge_list(graph: "Graph") -> str:
    edges = graph.to_edge_list()
    arrow = "->" if graph.directed else "--"
    if graph.weighted:
        return "\n".join(f"{u} {arrow} {v} (w={_fmt_num(w)})" for u, v, w in edges)
    return "\n".join(f"{u} {arrow} {v}" for u, v, _ in edges)


def parse_matrix(text: str):
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if not lines:
        return [], []
    first = lines[0].split()

    def is_num(tok):
        try:
            float(tok)
            return True
        except ValueError:
            return False

    has_header = not all(is_num(t) for t in first)
    if has_header:
        labels = first
        rows = lines[1:]
        matrix = []
        for r in rows:
            parts = r.split()
            matrix.append([float(x) for x in parts[1:]])
    else:
        n = len(first)
        labels = [f"V{i+1}" for i in range(n)]
        matrix = [[float(x) for x in ln.split()] for ln in lines]
    return labels, matrix


def parse_edge_list(text: str, weighted: bool):
    edges = []
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        line = line.replace("->", " ").replace("--", " ").replace("(w=", " ").replace(")", "")
        parts = line.split()
        if len(parts) < 2:
            continue
        u, v = parts[0], parts[1]
        w = float(parts[2]) if weighted and len(parts) >= 3 else 1
        edges.append((u, v, w))
    return edges
