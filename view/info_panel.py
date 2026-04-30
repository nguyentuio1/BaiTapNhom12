import tkinter as tk
from tkinter import ttk, scrolledtext

from model.graph import Graph
from model.representations import (
    format_matrix, format_adjacency_list, format_edge_list,
)


class InfoPanel(tk.Frame):
    def __init__(self, master, on_apply_representation=None):
        super().__init__(master, width=320)
        self.on_apply_representation = on_apply_representation

        tk.Label(self, text="Trạng thái thuật toán", font=("TkDefaultFont", 10, "bold")).pack(fill=tk.X)
        self.status = scrolledtext.ScrolledText(self, height=10, state=tk.DISABLED, wrap=tk.WORD)
        self.status.pack(fill=tk.BOTH, expand=False, padx=5, pady=2)

        tk.Label(self, text="Biểu diễn", font=("TkDefaultFont", 10, "bold")).pack(fill=tk.X, pady=(8, 0))
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        self.tabs = {}
        for name in ("Ma trận", "Danh sách kề", "Danh sách cạnh"):
            frame = tk.Frame(self.notebook)
            text = scrolledtext.ScrolledText(frame, wrap=tk.NONE, height=12, font=("Consolas", 9))
            text.pack(fill=tk.BOTH, expand=True)
            self.tabs[name] = text
            self.notebook.add(frame, text=name)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=5, pady=2)
        tk.Button(btn_frame, text="Áp dụng tab hiện tại", command=self._apply).pack(side=tk.LEFT)

    def update_status(self, info: dict):
        self.status.config(state=tk.NORMAL)
        self.status.delete("1.0", tk.END)
        for k, v in info.items():
            self.status.insert(tk.END, f"{k}: {v}\n")
        self.status.config(state=tk.DISABLED)

    def update_representations(self, graph: Graph):
        for name, content in (
            ("Ma trận", format_matrix(graph)),
            ("Danh sách kề", format_adjacency_list(graph)),
            ("Danh sách cạnh", format_edge_list(graph)),
        ):
            self.tabs[name].delete("1.0", tk.END)
            self.tabs[name].insert("1.0", content)

    def _apply(self):
        if not self.on_apply_representation:
            return
        idx = self.notebook.index(self.notebook.select())
        names = ("Ma trận", "Danh sách kề", "Danh sách cạnh")
        name = names[idx]
        text = self.tabs[name].get("1.0", tk.END)
        self.on_apply_representation(name, text)
