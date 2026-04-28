from model.graph import Graph
from algorithms.frame import Frame, COLOR_CURRENT, COLOR_SELECTED, COLOR_REJECTED


class _DSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        self.parent[ra] = rb
        return True


def kruskal(graph: Graph):
    frames = []
    edges = sorted(graph.to_edge_list(), key=lambda e: e[2])
    dsu = _DSU(graph.nodes())
    mst_edges = []
    total = 0

    frames.append(Frame(
        info={"sorted_edges": list(edges), "mst_edges": [], "total_weight": 0},
        log=f"Sắp xếp cạnh tăng dần theo trọng số: {len(edges)} cạnh",
    ))

    for u, v, w in edges:
        edge_colors = {(eu, ev): COLOR_SELECTED for eu, ev, _ in mst_edges}
        edge_colors[(u, v)] = COLOR_CURRENT
        frames.append(Frame(
            edge_colors=dict(edge_colors),
            info={"current": (u, v, w), "mst_edges": list(mst_edges),
                  "total_weight": total},
            log=f"Xét cạnh ({u},{v}) trọng số {w}",
        ))
        if dsu.union(u, v):
            mst_edges.append((u, v, w))
            total += w
            edge_colors[(u, v)] = COLOR_SELECTED
            frames.append(Frame(
                edge_colors=dict(edge_colors),
                info={"mst_edges": list(mst_edges), "total_weight": total},
                log=f"Thêm vào MST. Tổng = {total}",
            ))
        else:
            edge_colors[(u, v)] = COLOR_REJECTED
            frames.append(Frame(
                edge_colors=dict(edge_colors),
                info={"mst_edges": list(mst_edges), "total_weight": total},
                log="Tạo chu trình → bỏ qua",
            ))

    final_edges = {(u, v): COLOR_SELECTED for u, v, _ in mst_edges}
    frames.append(Frame(
        node_colors={n: COLOR_SELECTED for n in graph.nodes()},
        edge_colors=final_edges,
        info={"mst_edges": list(mst_edges), "total_weight": total},
        log=f"Kruskal hoàn tất. Tổng trọng số MST = {total}",
    ))
    return frames
