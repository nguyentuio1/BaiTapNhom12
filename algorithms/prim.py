import heapq
from model.graph import Graph
from algorithms.frame import Frame, COLOR_SELECTED, COLOR_REJECTED


def prim(graph: Graph, source: str):
    frames = []
    if source not in graph.nodes():
        return [Frame(log="Đỉnh nguồn không tồn tại")]

    in_mst = {source}
    mst_edges = []
    total = 0
    pq = []
    for v in graph.neighbors(source):
        w = graph.get_edge_weight(source, v)
        heapq.heappush(pq, (w, source, v))

    frames.append(Frame(
        node_colors={source: COLOR_SELECTED},
        info={"in_mst": [source], "mst_edges": [], "total_weight": 0},
        log=f"Bắt đầu Prim từ {source}",
    ))

    while pq and len(in_mst) < graph.num_nodes():
        w, u, v = heapq.heappop(pq)
        if v in in_mst:
            node_colors = {n: COLOR_SELECTED for n in in_mst}
            frames.append(Frame(
                node_colors=node_colors,
                edge_colors={(u, v): COLOR_REJECTED},
                info={"in_mst": list(in_mst), "mst_edges": list(mst_edges),
                      "total_weight": total},
                log=f"Bỏ cạnh ({u},{v}) trọng số {w} — {v} đã trong MST",
            ))
            continue

        in_mst.add(v)
        mst_edges.append((u, v, w))
        total += w
        node_colors = {n: COLOR_SELECTED for n in in_mst}
        edge_colors = {(eu, ev): COLOR_SELECTED for eu, ev, _ in mst_edges}
        frames.append(Frame(
            node_colors=node_colors,
            edge_colors=edge_colors,
            info={"in_mst": list(in_mst), "mst_edges": list(mst_edges),
                  "total_weight": total},
            log=f"Thêm cạnh ({u},{v}) trọng số {w} vào MST. Tổng = {total}",
        ))

        for nb in graph.neighbors(v):
            if nb not in in_mst:
                wt = graph.get_edge_weight(v, nb)
                heapq.heappush(pq, (wt, v, nb))

    frames.append(Frame(
        node_colors={n: COLOR_SELECTED for n in in_mst},
        edge_colors={(u, v): COLOR_SELECTED for u, v, _ in mst_edges},
        info={"in_mst": list(in_mst), "mst_edges": list(mst_edges), "total_weight": total},
        log=f"Prim hoàn tất. Tổng trọng số MST = {total}",
    ))
    return frames
