import json
import os
from model.graph import Graph


def save_graph(graph: Graph, path: str) -> None:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        _save_txt(graph, path)
    else:
        _save_json(graph, path)


def load_graph(path: str) -> Graph:
    ext = os.path.splitext(path)[1].lower()
    if ext == ".txt":
        return _load_txt(path)
    return _load_json(path)


def _save_json(graph: Graph, path: str) -> None:
    data = {
        "directed": graph.directed,
        "weighted": graph.weighted,
        "nodes": [],
        "edges": []
    }
    for name in graph.nodes():
        x, y = graph.get_node_pos(name)
        data["nodes"].append({"name": name, "x": x, "y": y})
    for u, v, w in graph.to_edge_list():
        data["edges"].append({"u": u, "v": v, "weight": w})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _load_json(path: str) -> Graph:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    g = Graph(directed=data.get("directed", False),
              weighted=data.get("weighted", False))
    for n in data.get("nodes", []):
        g.add_node(n["name"], n.get("x", 0), n.get("y", 0))
    for e in data.get("edges", []):
        g.add_edge(e["u"], e["v"], e.get("weight", 1))
    return g


def _fmt_num(v):
    try:
        if float(v).is_integer():
            return str(int(v))
    except (TypeError, ValueError):
        pass
    return str(v)


def _save_txt(graph: Graph, path: str) -> None:
    labels, m = graph.to_adjacency_matrix()
    n = len(labels)
    lines = [f"{n} {1 if graph.directed else 0}"]
    for row in m:
        lines.append(" ".join(_fmt_num(v) for v in row))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def _load_txt(path: str) -> Graph:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip().splitlines()
    raw = [ln.split("#")[0].strip() for ln in raw if ln.split("#")[0].strip()]
    header = raw[0].split()
    n = int(header[0])
    directed = len(header) > 1 and header[1] == "1"
    matrix = []
    for i in range(1, n + 1):
        matrix.append([float(x) for x in raw[i].split()])
    weighted = any(v not in (0, 1) for row in matrix for v in row)
    labels = [f"V{i+1}" for i in range(n)]
    return Graph.from_adjacency_matrix(labels, matrix, directed, weighted)
