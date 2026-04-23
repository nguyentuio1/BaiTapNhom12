from collections import deque
from model.graph import Graph
from algorithms.frame import Frame, COLOR_SELECTED, COLOR_REJECTED


def is_bipartite(graph: Graph):
    frames = []
    color = {}
    nodes = sorted(graph.nodes())
    if not nodes:
        return True, [Frame(info={"bipartite": True}, log="Đồ thị rỗng — coi như 2 phía")]

    color_names = {0: "skyblue", 1: "orange"}

    for start in nodes:
        if start in color:
            continue
        color[start] = 0
        queue = deque([start])
        frames.append(Frame(
            node_colors={start: color_names[0]},
            info={"queue": [start], "color_assignments": dict(color), "bipartite": None},
            log=f"Tô màu {start} = nhóm 1",
        ))
        while queue:
            u = queue.popleft()
            for v in sorted(graph.neighbors(u)):
                if v not in color:
                    color[v] = 1 - color[u]
                    queue.append(v)
                    nc = {n: color_names[color[n]] for n in color}
                    frames.append(Frame(
                        node_colors=nc,
                        edge_colors={(u, v): COLOR_SELECTED},
                        info={"queue": list(queue), "color_assignments": dict(color), "bipartite": None},
                        log=f"Tô màu {v} = nhóm {color[v] + 1} (kề với {u})",
                    ))
                elif color[v] == color[u]:
                    nc = {n: color_names[color[n]] for n in color}
                    nc[u] = COLOR_REJECTED
                    nc[v] = COLOR_REJECTED
                    frames.append(Frame(
                        node_colors=nc,
                        edge_colors={(u, v): COLOR_REJECTED},
                        info={"color_assignments": dict(color), "bipartite": False},
                        log=f"Mâu thuẫn: {u} và {v} cùng màu → KHÔNG là đồ thị 2 phía",
                    ))
                    return False, frames

    final_colors = {n: color_names[color[n]] for n in color}
    frames.append(Frame(
        node_colors=final_colors,
        info={"color_assignments": dict(color), "bipartite": True},
        log="Đồ thị LÀ đồ thị 2 phía",
    ))
    return True, frames
