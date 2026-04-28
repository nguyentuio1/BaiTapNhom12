from collections import defaultdict
from model.graph import Graph
from algorithms.frame import Frame, COLOR_CURRENT, COLOR_SELECTED


def hierholzer(graph: Graph, source: str):
    odd = [n for n in graph.nodes() if len(graph.neighbors(n)) % 2 == 1]
    if len(odd) not in (0, 2):
        return [Frame(info={"has_euler": False, "circuit": []},
                      log=f"Đồ thị có {len(odd)} đỉnh bậc lẻ — không có chu trình Euler")]
    if len(odd) == 2 and source not in odd:
        source = odd[0]

    if source not in graph.nodes():
        return [Frame(info={"has_euler": False}, log="Đỉnh nguồn không tồn tại")]

    adj = defaultdict(list)
    for u, v, _ in graph.to_edge_list():
        adj[u].append(v)
        if not graph.directed:
            adj[v].append(u)

    frames = []
    stack = [source]
    circuit = []

    frames.append(Frame(
        node_colors={source: COLOR_CURRENT},
        info={"stack": list(stack), "circuit": list(circuit), "has_euler": None},
        log=f"Bắt đầu Hierholzer từ {source}",
    ))

    while stack:
        u = stack[-1]
        if adj[u]:
            v = adj[u].pop()
            if not graph.directed:
                if u in adj[v]:
                    adj[v].remove(u)
            stack.append(v)
            frames.append(Frame(
                node_colors={n: COLOR_CURRENT for n in stack},
                info={"stack": list(stack), "circuit": list(circuit), "has_euler": None},
                log=f"Đẩy {v} vào stack (cạnh {u}-{v})",
            ))
        else:
            popped = stack.pop()
            circuit.append(popped)
            colors = {n: COLOR_CURRENT for n in stack}
            for n in circuit:
                colors[n] = COLOR_SELECTED
            frames.append(Frame(
                node_colors=colors,
                info={"stack": list(stack), "circuit": list(circuit), "has_euler": None},
                log=f"{popped} hết cạnh — đưa vào kết quả",
            ))

    circuit.reverse()
    has_euler = len(circuit) - 1 == graph.num_edges()

    edge_colors = {}
    for i in range(len(circuit) - 1):
        edge_colors[(circuit[i], circuit[i + 1])] = COLOR_SELECTED

    frames.append(Frame(
        node_colors={n: COLOR_SELECTED for n in circuit},
        edge_colors=edge_colors,
        info={"circuit": list(circuit), "has_euler": has_euler},
        log=f"Hierholzer hoàn tất: {' → '.join(circuit)}",
    ))
    return frames
