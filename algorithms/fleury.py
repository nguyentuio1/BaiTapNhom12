from model.graph import Graph
from algorithms.frame import Frame, COLOR_CURRENT, COLOR_SELECTED


def _odd_degree_nodes(g: Graph):
    return [n for n in g.nodes() if len(g.neighbors(n)) % 2 == 1]


def _is_bridge(g: Graph, u: str, v: str) -> bool:
    if len(g.neighbors(u)) == 1:
        return False
    visited = {u}
    stack = [u]
    while stack:
        x = stack.pop()
        for y in g.neighbors(x):
            if (x == u and y == v) or (x == v and y == u):
                continue
            if y not in visited:
                visited.add(y)
                stack.append(y)
    return v not in visited


def fleury(graph: Graph, source: str):
    frames = []
    odd = _odd_degree_nodes(graph)
    if len(odd) not in (0, 2):
        return [Frame(info={"has_euler": False, "path": []},
                      log=f"Đồ thị có {len(odd)} đỉnh bậc lẻ → không có chu trình/đường đi Euler")]
    if len(odd) == 2 and source not in odd:
        source = odd[0]

    g = graph.copy()
    if source not in g.nodes():
        return [Frame(info={"has_euler": False}, log="Đỉnh nguồn không tồn tại")]

    path = [source]
    used_edges = []
    cur = source

    frames.append(Frame(
        node_colors={source: COLOR_CURRENT},
        info={"path": list(path), "has_euler": None},
        log=f"Bắt đầu Fleury từ {source}",
    ))

    while g.neighbors(cur):
        nbrs = sorted(g.neighbors(cur))
        chosen = None
        for v in nbrs:
            if not _is_bridge(g, cur, v):
                chosen = v
                break
        if chosen is None:
            chosen = nbrs[0]
        used_edges.append((cur, chosen))
        g.remove_edge(cur, chosen)
        path.append(chosen)

        node_colors = {n: COLOR_SELECTED for n in path}
        node_colors[chosen] = COLOR_CURRENT
        edge_colors = {(u, v): COLOR_SELECTED for u, v in used_edges}
        frames.append(Frame(
            node_colors=node_colors,
            edge_colors=edge_colors,
            info={"path": list(path), "has_euler": None},
            log=f"Đi {cur} → {chosen}",
        ))
        cur = chosen

    has_euler = all(len(g.neighbors(n)) == 0 for n in g.nodes())
    frames.append(Frame(
        node_colors={n: COLOR_SELECTED for n in path},
        edge_colors={(u, v): COLOR_SELECTED for u, v in used_edges},
        info={"path": list(path), "has_euler": has_euler},
        log=f"Fleury hoàn tất. Đường đi: {' → '.join(path)}",
    ))
    return frames
