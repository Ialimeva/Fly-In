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

    def get_link_capacity(self, name1: str, name2: str) -> int:
        conn: str = name1 + "-" + name2
        if self.link_capacity[conn]:
            return self.link_capacity[conn]
        raise Exception("Link does not exist")

    def get_zone_capacity(self, zone: str) -> int:
        return self.nodes[zone].metadata.max_drones

    def get_node_coords(self, node: str) -> tuple[int, int]:
        return (
            self.nodes[node].x,
            self.nodes[node].y,
        )

    def goal_manhattan(self, node1: str) -> int:
        _, end_hub = self.get_endpoints()
        x1, y1 = self.get_node_coords(node1)
        x2, y2 = self.get_node_coords(end_hub)

        return abs(x1 - x2) + abs(y1 - y2)