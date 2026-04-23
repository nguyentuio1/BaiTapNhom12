import heapq
from collections import deque
from model.graph import Graph
from algorithms.frame import Frame, COLOR_CURRENT, COLOR_VISITED, COLOR_SELECTED


def shortest_path(graph: Graph, source: str, target: str):
    if source not in graph.nodes() or target not in graph.nodes():
        return [Frame(log="Đỉnh nguồn hoặc đích không tồn tại")]
    if graph.weighted:
        return _dijkstra(graph, source, target)
    return _bfs_path(graph, source, target)


def _dijkstra(graph: Graph, source: str, target: str):
    frames = []
    dist = {n: float("inf") for n in graph.nodes()}
    prev = {}
    dist[source] = 0
    pq = [(0, source)]
    visited = set()

    frames.append(Frame(
        node_colors={source: COLOR_CURRENT},
        info={"distances": dict(dist), "visited": [], "path": None},
        log=f"Khởi tạo Dijkstra từ {source}, dist[{source}]=0",
    ))

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        node_colors = {n: COLOR_VISITED for n in visited}
        node_colors[u] = COLOR_CURRENT
        frames.append(Frame(
            node_colors=dict(node_colors),
            info={"distances": dict(dist), "visited": list(visited), "path": None},
            log=f"Chọn {u} (khoảng cách {d}) làm đỉnh hiện tại",
        ))

        if u == target:
            break

        for v in sorted(graph.neighbors(u)):
            if v in visited:
                continue
            w = graph.get_edge_weight(u, v)
            alt = dist[u] + w
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))
                frames.append(Frame(
                    node_colors=dict(node_colors),
                    edge_colors={(u, v): COLOR_CURRENT},
                    info={"distances": dict(dist), "visited": list(visited), "path": None},
                    log=f"Cập nhật dist[{v}] = {alt} qua {u}",
                ))

    if dist[target] == float("inf"):
        frames.append(Frame(
            info={"distances": dict(dist), "visited": list(visited), "path": None},
            log=f"Không có đường từ {source} đến {target}",
        ))
        return frames

    path = []
    cur = target
    while cur != source:
        path.append(cur)
        cur = prev[cur]
    path.append(source)
    path.reverse()

    node_colors = {n: COLOR_SELECTED for n in path}
    edge_colors = {}
    for i in range(len(path) - 1):
        edge_colors[(path[i], path[i + 1])] = COLOR_SELECTED
    frames.append(Frame(
        node_colors=node_colors,
        edge_colors=edge_colors,
        info={"distances": dict(dist), "visited": list(visited),
              "path": path, "distance": dist[target]},
        log=f"Đường ngắn nhất {source} → {target}: {' → '.join(path)} (tổng {dist[target]})",
    ))
    return frames


def _bfs_path(graph: Graph, source: str, target: str):
    frames = []
    prev = {}
    visited = {source}
    queue = deque([source])

    frames.append(Frame(
        node_colors={source: COLOR_CURRENT},
        info={"queue": [source], "visited": [], "path": None},
        log=f"BFS tìm đường ngắn nhất (không trọng số) từ {source}",
    ))

    found = source == target
    while queue and not found:
        u = queue.popleft()
        for v in sorted(graph.neighbors(u)):
            if v not in visited:
                visited.add(v)
                prev[v] = u
                queue.append(v)
                if v == target:
                    found = True
                    break

    if not found and target != source:
        frames.append(Frame(
            info={"queue": [], "visited": list(visited), "path": None},
            log=f"Không có đường từ {source} đến {target}",
        ))
        return frames

    path = []
    cur = target
    while cur != source:
        path.append(cur)
        cur = prev[cur]
    path.append(source)
    path.reverse()

    node_colors = {n: COLOR_SELECTED for n in path}
    edge_colors = {}
    for i in range(len(path) - 1):
        edge_colors[(path[i], path[i + 1])] = COLOR_SELECTED
    frames.append(Frame(
        node_colors=node_colors,
        edge_colors=edge_colors,
        info={"queue": [], "visited": list(visited), "path": path, "distance": len(path) - 1},
        log=f"Đường ngắn nhất: {' → '.join(path)} (độ dài {len(path) - 1})",
    ))
    return frames
