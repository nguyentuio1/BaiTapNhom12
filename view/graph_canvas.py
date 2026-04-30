import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

from model.graph import Graph
from algorithms.frame import Frame


COLOR_MAP = {
    "default": "#dddddd",
    "yellow": "#ffd54f",
    "green": "#66bb6a",
    "red": "#ef5350",
    "blue": "#42a5f5",
    "gray": "#bdbdbd",
    "skyblue": "#4fc3f7",
    "orange": "#ffa726",
}


class GraphCanvas(tk.Frame):
    def __init__(self, master, on_canvas_click=None, on_node_click=None):
        super().__init__(master)
        self.figure = Figure(figsize=(7, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.mpl_connect("button_press_event", self._on_click)
        self.canvas.mpl_connect("button_release_event", self._on_release)
        self.canvas.mpl_connect("motion_notify_event", self._on_motion)

        self.graph = None
        self.positions = {}
        self.current_frame = None
        self.on_canvas_click = on_canvas_click
        self.on_node_click = on_node_click
        self._dragging = None
        self._press_xy = None
        self._was_dragged = False

    def set_graph(self, graph: Graph):
        self.graph = graph
        self._refresh_positions()
        self.render(None)

    def _refresh_positions(self):
        if not self.graph:
            self.positions = {}
            return
        explicit = {}
        missing = []
        for n in self.graph.nodes():
            x, y = self.graph.get_node_pos(n)
            if x == 0 and y == 0:
                missing.append(n)
            else:
                explicit[n] = (x, y)
        if missing:
            nxg = self.graph._nx
            try:
                layout = nx.spring_layout(nxg, seed=42)
            except Exception:
                layout = {n: (0, 0) for n in nxg.nodes()}
            for n in missing:
                fx, fy = layout.get(n, (0, 0))
                explicit[n] = (fx * 100, fy * 100)
                self.graph.set_node_pos(n, fx * 100, fy * 100)
        self.positions = explicit

    def render(self, frame):
        self.current_frame = frame
        self.ax.clear()
        self.ax.set_axis_off()
        if not self.graph:
            self.canvas.draw_idle()
            return

        node_colors = (frame.node_colors if frame else {}) or {}
        edge_colors = (frame.edge_colors if frame else {}) or {}
        edge_labels = (frame.edge_labels if frame else {}) or {}

        for u, v, w in self.graph.edges():
            if u not in self.positions or v not in self.positions:
                continue
            x1, y1 = self.positions[u]
            x2, y2 = self.positions[v]
            ckey_name = edge_colors.get((u, v), edge_colors.get((v, u), "default"))
            ckey = COLOR_MAP.get(ckey_name, "#888888")
            if self.graph.directed:
                self.ax.annotate(
                    "", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=ckey, lw=2,
                                    shrinkA=15, shrinkB=15)
                )
            else:
                self.ax.plot([x1, x2], [y1, y2], color=ckey, lw=2, zorder=1)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            label = edge_labels.get((u, v)) or edge_labels.get((v, u))
            if label is None and self.graph.weighted:
                try:
                    label = str(int(w)) if float(w).is_integer() else str(w)
                except (TypeError, ValueError):
                    label = str(w)
            if label:
                self.ax.text(mx, my, label, fontsize=9, color="#333",
                             bbox=dict(facecolor="white", edgecolor="none", pad=1))

        for n, (x, y) in self.positions.items():
            color = COLOR_MAP.get(node_colors.get(n, "default"), "#dddddd")
            self.ax.scatter([x], [y], s=600, c=color, edgecolors="#222", zorder=2)
            self.ax.text(x, y, n, ha="center", va="center", fontsize=10,
                         fontweight="bold", zorder=3)

        if self.positions:
            xs = [p[0] for p in self.positions.values()]
            ys = [p[1] for p in self.positions.values()]
            margin = 30
            xmin, xmax = min(xs), max(xs)
            ymin, ymax = min(ys), max(ys)
            if xmin == xmax:
                xmin -= 50; xmax += 50
            if ymin == ymax:
                ymin -= 50; ymax += 50
            self.ax.set_xlim(xmin - margin, xmax + margin)
            self.ax.set_ylim(ymin - margin, ymax + margin)
        self.canvas.draw_idle()

    def _node_at(self, x, y, radius=20):
        if x is None or y is None:
            return None
        for n, (nx_, ny_) in self.positions.items():
            if (x - nx_) ** 2 + (y - ny_) ** 2 <= radius ** 2:
                return n
        return None

    def _on_click(self, event):
        if event.inaxes != self.ax:
            return
        node = self._node_at(event.xdata, event.ydata)
        self._press_xy = (event.xdata, event.ydata)
        self._was_dragged = False
        if node:
            self._dragging = node
            self._click_node = (node, event.button)
        else:
            self._dragging = None
            self._click_node = None
            if event.button == 1 and self.on_canvas_click:
                self.on_canvas_click(event.xdata, event.ydata)

    def _on_motion(self, event):
        if self._dragging is None or event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return
        if self._press_xy:
            dx = event.xdata - self._press_xy[0]
            dy = event.ydata - self._press_xy[1]
            if dx * dx + dy * dy > 25:
                self._was_dragged = True
        self.positions[self._dragging] = (event.xdata, event.ydata)
        if self.graph:
            self.graph.set_node_pos(self._dragging, event.xdata, event.ydata)
        self.render(self.current_frame)

    def _on_release(self, event):
        if self._dragging is not None and not self._was_dragged and self._click_node:
            node, button = self._click_node
            if self.on_node_click:
                self.on_node_click(node, button)
        self._dragging = None
        self._press_xy = None
        self._click_node = None
        self._was_dragged = False
