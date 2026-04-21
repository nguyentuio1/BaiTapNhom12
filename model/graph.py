import networkx as nx
from typing import Optional


class Graph:
    def __init__(self, directed: bool = False, weighted: bool = False):
        self.directed = directed
        self.weighted = weighted
        self._nx = nx.DiGraph() if directed else nx.Graph()

    def add_node(self, name: str, x: Optional[float] = None, y: Optional[float] = None) -> None:
        self._nx.add_node(name, x=x if x is not None else 0.0, y=y if y is not None else 0.0)

    def remove_node(self, name: str) -> None:
        if name in self._nx:
            self._nx.remove_node(name)

    def rename_node(self, old: str, new: str) -> None:
        if old not in self._nx or new in self._nx:
            return
        self._nx = nx.relabel_nodes(self._nx, {old: new})

    def add_edge(self, u: str, v: str, weight: float = 1) -> None:
        if u not in self._nx or v not in self._nx:
            return
        w = weight if self.weighted else 1
        self._nx.add_edge(u, v, weight=w)

    def remove_edge(self, u: str, v: str) -> None:
        if self._nx.has_edge(u, v):
            self._nx.remove_edge(u, v)

    def has_edge(self, u: str, v: str) -> bool:
        return self._nx.has_edge(u, v)

    def get_edge_weight(self, u: str, v: str) -> float:
        return self._nx[u][v].get("weight", 1)

    def set_edge_weight(self, u: str, v: str, weight: float) -> None:
        if self._nx.has_edge(u, v):
            self._nx[u][v]["weight"] = weight

    def neighbors(self, u: str) -> list:
        if u not in self._nx:
            return []
        return list(self._nx.neighbors(u))

    def in_neighbors(self, u: str) -> list:
        if not self.directed or u not in self._nx:
            return self.neighbors(u)
        return list(self._nx.predecessors(u))

    def nodes(self) -> list:
        return list(self._nx.nodes())

    def edges(self) -> list:
        return [(u, v, d.get("weight", 1)) for u, v, d in self._nx.edges(data=True)]

    def get_node_pos(self, name: str):
        d = self._nx.nodes[name]
        return d.get("x", 0.0), d.get("y", 0.0)

    def set_node_pos(self, name: str, x: float, y: float) -> None:
        if name in self._nx:
            self._nx.nodes[name]["x"] = x
            self._nx.nodes[name]["y"] = y

    def clear(self) -> None:
        self._nx.clear()

    def copy(self) -> "Graph":
        g = Graph(self.directed, self.weighted)
        g._nx = self._nx.copy()
        return g

    def num_nodes(self) -> int:
        return self._nx.number_of_nodes()

    def num_edges(self) -> int:
        return self._nx.number_of_edges()

    # --- Representation conversions ---
    def to_adjacency_matrix(self):
        labels = sorted(self.nodes())
        n = len(labels)
        idx = {name: i for i, name in enumerate(labels)}
        m = [[0 for _ in range(n)] for _ in range(n)]
        for u, v, w in self.edges():
            m[idx[u]][idx[v]] = w
            if not self.directed:
                m[idx[v]][idx[u]] = w
        return labels, m

    def to_adjacency_list(self):
        result = {n: [] for n in self.nodes()}
        for u, v, w in self.edges():
            result[u].append((v, w))
            if not self.directed:
                result[v].append((u, w))
        return result

    def to_edge_list(self):
        if self.directed:
            return self.edges()
        seen = set()
        result = []
        for u, v, w in self.edges():
            key = tuple(sorted([u, v]))
            if key in seen:
                continue
            seen.add(key)
            result.append((u, v, w))
        return result

    @classmethod
    def from_adjacency_matrix(cls, labels, matrix, directed: bool, weighted: bool) -> "Graph":
        g = cls(directed=directed, weighted=weighted)
        for name in labels:
            g.add_node(name)
        n = len(labels)
        for i in range(n):
            jrange = range(n) if directed else range(i + 1, n)
            for j in jrange:
                w = matrix[i][j]
                if w != 0:
                    g.add_edge(labels[i], labels[j], w)
        return g

    @classmethod
    def from_adjacency_list(cls, adj, directed: bool, weighted: bool) -> "Graph":
        g = cls(directed=directed, weighted=weighted)
        for name in adj:
            g.add_node(name)
        seen = set()
        for u, lst in adj.items():
            for v, w in lst:
                if v not in g._nx:
                    g.add_node(v)
                if not directed:
                    key = tuple(sorted([u, v]))
                    if key in seen:
                        continue
                    seen.add(key)
                g.add_edge(u, v, w)
        return g

    @classmethod
    def from_edge_list(cls, edges, directed: bool, weighted: bool) -> "Graph":
        g = cls(directed=directed, weighted=weighted)
        for edge in edges:
            u, v = edge[0], edge[1]
            w = edge[2] if len(edge) >= 3 else 1
            if u not in g._nx:
                g.add_node(u)
            if v not in g._nx:
                g.add_node(v)
            g.add_edge(u, v, w)
        return g
