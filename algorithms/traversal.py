from collections import deque
from model.graph import Graph
from algorithms.frame import Frame, COLOR_CURRENT, COLOR_VISITED


def bfs(graph: Graph, source: str):
    frames = []
    if source not in graph.nodes():
        return frames

    visited = set()
    order = []
    queue = deque([source])
    visited.add(source)

    frames.append(Frame(
        node_colors={source: COLOR_CURRENT},
        info={"queue": [source], "visited": [], "order": []},
        log=f"Bắt đầu BFS từ {source}",
    ))

    while queue:
        u = queue.popleft()
        order.append(u)
        node_colors = {n: COLOR_VISITED for n in order}
        node_colors[u] = COLOR_CURRENT
        for q in queue:
            node_colors[q] = COLOR_CURRENT

        frames.append(Frame(
            node_colors=dict(node_colors),
            info={"queue": list(queue), "visited": list(order), "order": list(order)},
            log=f"Lấy {u} ra khỏi hàng đợi, xét các đỉnh kề",
        ))

        for v in sorted(graph.neighbors(u)):
            if v not in visited:
                visited.add(v)
                queue.append(v)
                node_colors[v] = COLOR_CURRENT
                frames.append(Frame(
                    node_colors=dict(node_colors),
                    edge_colors={(u, v): COLOR_VISITED},
                    info={"queue": list(queue), "visited": list(order), "order": list(order)},
                    log=f"Thêm {v} vào hàng đợi (kề với {u})",
                ))

    final_colors = {n: COLOR_VISITED for n in order}
    frames.append(Frame(
        node_colors=final_colors,
        info={"queue": [], "visited": list(order), "order": list(order)},
        log=f"BFS hoàn tất. Thứ tự duyệt: {' → '.join(order)}",
    ))
    return frames


def dfs(graph: Graph, source: str):
    frames = []
    if source not in graph.nodes():
        return frames

    visited = set()
    order = []
    stack = [source]

    frames.append(Frame(
        node_colors={source: COLOR_CURRENT},
        info={"stack": [source], "visited": [], "order": []},
        log=f"Bắt đầu DFS từ {source}",
    ))

    while stack:
        u = stack.pop()
        if u in visited:
            continue
        visited.add(u)
        order.append(u)

        node_colors = {n: COLOR_VISITED for n in order}
        node_colors[u] = COLOR_CURRENT
        frames.append(Frame(
            node_colors=dict(node_colors),
            info={"stack": list(stack), "visited": list(order), "order": list(order)},
            log=f"Thăm {u}",
        ))

        for v in sorted(graph.neighbors(u), reverse=True):
            if v not in visited:
                stack.append(v)
                frames.append(Frame(
                    node_colors=dict(node_colors),
                    edge_colors={(u, v): COLOR_VISITED},
                    info={"stack": list(stack), "visited": list(order), "order": list(order)},
                    log=f"Đẩy {v} vào stack (kề với {u})",
                ))

    final_colors = {n: COLOR_VISITED for n in order}
    frames.append(Frame(
        node_colors=final_colors,
        info={"stack": [], "visited": list(order), "order": list(order)},
        log=f"DFS hoàn tất. Thứ tự duyệt: {' → '.join(order)}",
    ))
    return frames
