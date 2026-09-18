from ..models import Map, Hub, Connection


class MakeGraph:
    def __init__(self, map: Map) -> None:
        self.nodes: dict[str, Hub] = map.hubs
        self.edges: list[Connection] = map.connections
        self.neighbors: dict[str, set[str]] = {
            k: set() for k in self.nodes
        }
        self.link_capacity: dict[str, int] = {
            c.name1 + "-" + c.name2: c.max_link_capacity
            for c in self.edges
        }

    def get_endpoints(self) -> None:
        for k, v in self.nodes.items():
            if v.type == "start_hub":
                self.start_hub: str = k
            elif v.type == "end_hub":
                self.end_hub: str = k
            continue

        return (self.start_hub, self.end_hub)

    def get_graph(self) -> dict[str, set[str]]:
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

