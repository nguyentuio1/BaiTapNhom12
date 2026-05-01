import tkinter as tk
from tkinter import ttk


ALGORITHMS = ["BFS", "DFS", "Dijkstra", "Bipartite", "Prim", "Kruskal",
              "Ford-Fulkerson", "Fleury", "Hierholzer"]


class ControlPanel(tk.Frame):
    def __init__(self, master, on_new=None, on_open=None, on_save=None,
                 on_run_algorithm=None, on_clear=None):
        super().__init__(master)
        self.on_run_algorithm = on_run_algorithm

        tk.Button(self, text="Mới", command=on_new, width=6).pack(side=tk.LEFT, padx=2)
        tk.Button(self, text="Mở", command=on_open, width=6).pack(side=tk.LEFT, padx=2)
        tk.Button(self, text="Lưu", command=on_save, width=6).pack(side=tk.LEFT, padx=2)
        tk.Button(self, text="Xóa", command=on_clear, width=6).pack(side=tk.LEFT, padx=2)

        tk.Label(self, text="  Nguồn:").pack(side=tk.LEFT)
        self.source = ttk.Combobox(self, width=6, values=[])
        self.source.pack(side=tk.LEFT)

        tk.Label(self, text=" Đích:").pack(side=tk.LEFT)
        self.target = ttk.Combobox(self, width=6, values=[])
        self.target.pack(side=tk.LEFT)

        tk.Label(self, text="  ").pack(side=tk.LEFT)
        for algo in ALGORITHMS:
            b = tk.Button(self, text=algo, command=lambda a=algo: self._run(a))
            b.pack(side=tk.LEFT, padx=1)

    def update_node_options(self, nodes):
        nodes = list(nodes)
        cur_src = self.source.get()
        cur_tgt = self.target.get()
        self.source["values"] = nodes
        self.target["values"] = nodes
        if cur_src not in nodes:
            self.source.set(nodes[0] if nodes else "")
        if cur_tgt not in nodes:
            self.target.set(nodes[-1] if nodes else "")

    def _run(self, algo: str):
        if self.on_run_algorithm:
            self.on_run_algorithm(algo, self.source.get(), self.target.get())
