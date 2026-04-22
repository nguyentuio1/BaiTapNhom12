from dataclasses import dataclass, field


@dataclass
class Frame:
    node_colors: dict = field(default_factory=dict)
    edge_colors: dict = field(default_factory=dict)
    edge_labels: dict = field(default_factory=dict)
    info: dict = field(default_factory=dict)
    log: str = ""

    def copy(self) -> "Frame":
        return Frame(
            node_colors=dict(self.node_colors),
            edge_colors=dict(self.edge_colors),
            edge_labels=dict(self.edge_labels),
            info=dict(self.info),
            log=self.log,
        )


COLOR_DEFAULT = "default"
COLOR_CURRENT = "yellow"
COLOR_SELECTED = "green"
COLOR_REJECTED = "red"
COLOR_VISITED = "blue"
COLOR_INACTIVE = "gray"
