from collections import defaultdict, deque
from model.graph import Graph
from algorithms.frame import Frame, COLOR_CURRENT, COLOR_SELECTED


def ford_fulkerson(graph: Graph, source: str, sink: str):
    frames = []
    if source not in graph.nodes() or sink not in graph.nodes():
        return [Frame(log="Đỉnh nguồn hoặc đích không tồn tại")]

    capacity = defaultdict(int)
    for u, v, w in graph.edges():
        capacity[(u, v)] += w
        if not graph.directed:
            capacity[(v, u)] += w

    flow = defaultdict(int)
    total = 0

    nodes = list(graph.nodes())

    def bfs_path():
        prev = {source: None}
        q = deque([source])
        while q:
            u = q.popleft()
            for v in nodes:
                if v not in prev and capacity[(u, v)] - flow[(u, v)] > 0:
                    prev[v] = u
                    if v == sink:
                        return prev
                    q.append(v)
        return None

    frames.append(Frame(
        info={"max_flow": 0, "edge_flows": {}},
        log=f"Bắt đầu Ford-Fulkerson từ {source} đến {sink}",
    ))

    iteration = 0
    while True:
        prev = bfs_path()
        if prev is None:
            break
        iteration += 1
        path = []
        cur = sink
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        bottleneck = min(capacity[(path[i], path[i + 1])] - flow[(path[i], path[i + 1])]
                         for i in range(len(path) - 1))

        edge_colors = {(path[i], path[i + 1]): COLOR_CURRENT for i in range(len(path) - 1)}
        edge_labels = {}
        for u, v, _ in graph.edges():
            if flow[(u, v)] > 0:
                edge_labels[(u, v)] = f"{flow[(u, v)]}/{capacity[(u, v)]}"

        frames.append(Frame(
            edge_colors=edge_colors,
            edge_labels=edge_labels,
            info={"path": path, "bottleneck": bottleneck, "max_flow": total},
            log=f"Lần {iteration}: tìm được đường tăng {' → '.join(path)}, bottleneck = {bottleneck}",
        ))

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            flow[(u, v)] += bottleneck
            flow[(v, u)] -= bottleneck
        total += bottleneck

        edge_labels_after = {}
        for u, v, _ in graph.edges():
            if flow[(u, v)] > 0:
                edge_labels_after[(u, v)] = f"{flow[(u, v)]}/{capacity[(u, v)]}"
        edge_colors_after = {(path[i], path[i + 1]): COLOR_SELECTED for i in range(len(path) - 1)}
        frames.append(Frame(
            edge_colors=edge_colors_after,
            edge_labels=edge_labels_after,
            info={"max_flow": total, "edge_flows": dict(edge_labels_after)},
            log=f"Đẩy {bottleneck} đơn vị luồng. Max flow hiện tại = {total}",
        ))

    final_labels = {}
    for u, v, _ in graph.edges():
        if flow[(u, v)] > 0:
            final_labels[(u, v)] = f"{flow[(u, v)]}/{capacity[(u, v)]}"
    frames.append(Frame(
        edge_labels=final_labels,
        info={"max_flow": total, "edge_flows": dict(final_labels)},
        log=f"Ford-Fulkerson hoàn tất. Max flow = {total}",
    ))
    return frames
