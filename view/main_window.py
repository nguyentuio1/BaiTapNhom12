import tkinter as tk
from tkinter import filedialog
import string

from model.graph import Graph
from io_.file_io import save_graph, load_graph
from view.graph_canvas import GraphCanvas
from view.info_panel import InfoPanel
from view.log_panel import LogPanel
from view.animation_bar import AnimationBar
from view.control_panel import ControlPanel
from view.dialogs import NewGraphDialog, ask_weight, warn

from algorithms.traversal import bfs, dfs
from algorithms.shortest_path import shortest_path
from algorithms.bipartite import is_bipartite
from algorithms.prim import prim
from algorithms.kruskal import kruskal
from algorithms.ford_fulkerson import ford_fulkerson
from algorithms.fleury import fleury
from algorithms.hierholzer import hierholzer
from model.representations import parse_matrix, parse_edge_list


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ứng dụng Đồ thị — Bài tập nhóm")
        self.geometry("1280x800")

        self.graph = Graph()
        self.pending_edge_source = None

        top = tk.Frame(self)
        top.pack(fill=tk.BOTH, expand=True)

        self.canvas = GraphCanvas(top, on_canvas_click=self._on_canvas_click,
                                  on_node_click=self._on_node_click)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.info_panel = InfoPanel(top, on_apply_representation=self._on_apply_representation)
        self.info_panel.pack(side=tk.RIGHT, fill=tk.Y)

        self.control = ControlPanel(self,
                                    on_new=self._new_graph,
                                    on_open=self._open,
                                    on_save=self._save,
                                    on_clear=self._clear_graph,
                                    on_run_algorithm=self._run_algorithm)
        self.control.pack(fill=tk.X)

        self.anim = AnimationBar(self, on_frame_change=self._on_frame_change)
        self.anim.pack(fill=tk.X)

        self.log = LogPanel(self)
        self.log.pack(fill=tk.BOTH)

        self.canvas.set_graph(self.graph)
        self._refresh()
        self.log.append("Sẵn sàng. Click trên canvas để thêm đỉnh; click 2 đỉnh khác nhau để nối cạnh.")

    # ---- Helpers ----
    def _refresh(self):
        self.canvas.render(self.canvas.current_frame)
        self.info_panel.update_representations(self.graph)
        self.control.update_node_options(self.graph.nodes())

    def _next_node_name(self) -> str:
        existing = set(self.graph.nodes())
        for ch in string.ascii_uppercase:
            if ch not in existing:
                return ch
        i = 1
        while f"V{i}" in existing:
            i += 1
        return f"V{i}"

    # ---- Canvas events ----
    def _on_canvas_click(self, x, y):
        name = self._next_node_name()
        self.graph.add_node(name, x=x, y=y)
        self.canvas.positions[name] = (x, y)
        self.pending_edge_source = None
        self.log.append(f"Thêm đỉnh {name} tại ({x:.0f}, {y:.0f})")
        self._refresh()

    def _on_node_click(self, node: str, button: int):
        if button == 1:
            if self.pending_edge_source is None:
                self.pending_edge_source = node
                self.log.append(f"Chọn {node} làm đỉnh đầu — click đỉnh thứ hai để nối cạnh")
            elif self.pending_edge_source == node:
                self.pending_edge_source = None
                self.log.append("Hủy chọn cạnh")
            else:
                u, v = self.pending_edge_source, node
                self.pending_edge_source = None
                w = 1
                if self.graph.weighted:
                    w = ask_weight(self)
                    if w is None:
                        self.log.append("Hủy thêm cạnh")
                        return
                self.graph.add_edge(u, v, w)
                self.log.append(f"Thêm cạnh {u}-{v} (trọng số {w})")
                self._refresh()
        elif button == 3:
            self.graph.remove_node(node)
            self.canvas._refresh_positions()
            self.log.append(f"Xóa đỉnh {node}")
            self._refresh()

    # ---- File ----
    def _new_graph(self):
        d = NewGraphDialog(self, title="Đồ thị mới")
        if d.result is None:
            return
        directed, weighted = d.result
        self.graph = Graph(directed=directed, weighted=weighted)
        self.canvas.set_graph(self.graph)
        self.anim.load([])
        self.log.clear()
        self.log.append(f"Đồ thị mới: directed={directed}, weighted={weighted}")
        self._refresh()

    def _clear_graph(self):
        self.graph.clear()
        self.canvas.set_graph(self.graph)
        self.anim.load([])
        self.log.append("Đã xóa toàn bộ đồ thị")
        self._refresh()

    def _open(self):
        path = filedialog.askopenfilename(filetypes=[("Graph files", "*.json *.txt"), ("All", "*")])
        if not path:
            return
        try:
            self.graph = load_graph(path)
            self.canvas.set_graph(self.graph)
            self.anim.load([])
            self.log.append(f"Đã mở {path}")
            self._refresh()
        except Exception as e:
            warn(self, "Lỗi đọc file", str(e))

    def _save(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Text matrix", "*.txt")])
        if not path:
            return
        try:
            save_graph(self.graph, path)
            self.log.append(f"Đã lưu {path}")
        except Exception as e:
            warn(self, "Lỗi lưu file", str(e))

    # ---- Representation editing ----
    def _on_apply_representation(self, name: str, text: str):
        try:
            if name == "Ma trận":
                labels, matrix = parse_matrix(text)
                if not labels:
                    warn(self, "Trống", "Ma trận rỗng")
                    return
                self.graph = Graph.from_adjacency_matrix(
                    labels, matrix, self.graph.directed, self.graph.weighted)
            elif name == "Danh sách cạnh":
                edges = parse_edge_list(text, self.graph.weighted)
                self.graph = Graph.from_edge_list(
                    edges, self.graph.directed, self.graph.weighted)
            else:
                warn(self, "Chưa hỗ trợ", "Sửa từ tab Danh sách kề chưa hỗ trợ; dùng tab khác.")
                return
            self.canvas.set_graph(self.graph)
            self.anim.load([])
            self.log.append(f"Áp dụng biểu diễn từ tab {name}")
            self._refresh()
        except Exception as e:
            warn(self, "Lỗi parse", str(e))

    # ---- Algorithms ----
    def _run_algorithm(self, algo: str, source: str, target: str):
        if not self.graph.nodes():
            warn(self, "Đồ thị rỗng", "Hãy tạo đồ thị trước")
            return
        try:
            if algo == "BFS":
                if not source:
                    warn(self, "Thiếu", "Chọn đỉnh nguồn"); return
                frames = bfs(self.graph, source)
            elif algo == "DFS":
                if not source:
                    warn(self, "Thiếu", "Chọn đỉnh nguồn"); return
                frames = dfs(self.graph, source)
            elif algo == "Dijkstra":
                if not source or not target:
                    warn(self, "Thiếu", "Chọn đỉnh nguồn và đích"); return
                frames = shortest_path(self.graph, source, target)
            elif algo == "Bipartite":
                _, frames = is_bipartite(self.graph)
            elif algo == "Prim":
                if not source:
                    warn(self, "Thiếu", "Chọn đỉnh nguồn"); return
                frames = prim(self.graph, source)
            elif algo == "Kruskal":
                frames = kruskal(self.graph)
            elif algo == "Ford-Fulkerson":
                if not source or not target:
                    warn(self, "Thiếu", "Chọn đỉnh nguồn và đích"); return
                frames = ford_fulkerson(self.graph, source, target)
            elif algo == "Fleury":
                if not source:
                    warn(self, "Thiếu", "Chọn đỉnh nguồn"); return
                frames = fleury(self.graph, source)
            elif algo == "Hierholzer":
                if not source:
                    warn(self, "Thiếu", "Chọn đỉnh nguồn"); return
                frames = hierholzer(self.graph, source)
            else:
                return
        except Exception as e:
            warn(self, f"Lỗi chạy {algo}", str(e))
            return
        self.log.clear()
        self.log.append(f"=== Chạy {algo} ===")
        self.anim.load(frames)

    def _on_frame_change(self, frame, idx: int, total: int):
        self.canvas.render(frame)
        self.info_panel.update_status(frame.info)
        if frame.log:
            self.log.append(f"[Bước {idx + 1}/{total}] {frame.log}")
