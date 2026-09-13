from models import Map, Hub, Connection


class MakeGraph:
    def __init__(self, map: Map) -> None:
        self.nodes: dict[str, Hub] = map.hubs
        self.edges: list[Connection] = map.connections
        self.neighbors: dict[str, set[str]] = {
            k: set() for k in self.nodes
        }

    def get_graph(self) -> dict[str, list[str]]:
        for node in self.nodes:
            for edge in self.edges:
                if edge.name1 == node:
                    self.neighbors[node].add(edge.name2)
                    self.neighbors[edge.name2].add(node)

        return self.neighbors

    def get_node_weight(self, zone: str) -> int|float:
        if zone in ("normal", "priority"):
            return 1
        elif zone == "restricted":
            return 2
        else:
            return float("inf")
