from ..models import Map, Hub, Connection


class MakeGraph:
    def __init__(self, map: Map) -> None:
        self.nodes: dict[str, Hub] = map.hubs
        self.edges: dict[str, Connection] = map.connections
        self.neighbors: dict[str, set[str]] = {
            k: set() for k in self.nodes
        }
        self.zone_capacity: dict[str, int] = {
            node: self.nodes[node].metadata.max_drones
            for node in self.nodes
        }
        self.link_capacity: dict[str, int] = {
            edge: self.edges[edge].max_link_capacity
            for edge in self.edges
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
                if self.edges[edge].name1 == node:
                    self.neighbors[node].add(self.edges[edge].name2)
                    self.neighbors[self.edges[edge].name2].add(node)

        return self.neighbors

    def get_node_weight(self, zone: str) -> int|float:
        if zone in ("normal", "priority"):
            return 1
        elif zone == "restricted":
            return 2
        else:
            return float("inf")

    def get_node_coords(self, node: str) -> tuple[int, int]:
        return (
            self.nodes[node].x,
            self.nodes[node].y,
        )
