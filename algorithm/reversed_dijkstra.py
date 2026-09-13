from models import Map, Hub
from .graph import MakeGraph


class ReversedDijkstra:
    def __init__(self, map: Map, graph: MakeGraph) -> None:
        self.map: Map = map
        self.graph: MakeGraph = graph
        self.nodes_distances: dict[str, int|float] = {}

    def set_starting_distance(self) -> None:
        for k, v in self.graph.nodes.items():
            if v.type == "end_hub":
                self.nodes_distances[k] = 0
                self.end_hub: str = k
            else:
                if v.type == "start_hub":
                    self.start_hub: str = k
                self.nodes_distances[k] = float("inf")

    def get_node_weight(self, zone: str) -> int|float:
        if zone in ("normal", "priority"):
            return 1
        elif zone == "restricted":
            return 2
        else:
            return float("inf")

    def nodes_distance_from_goal(self) -> dict[str, int|float]:
        self.set_starting_distance()
        nodes: dict[str, Hub] = self.graph.nodes
        edges: dict[str, list[str]] = self.graph.get_reversed_graph()
        visited: set[str] = set()
        current_node: str = self.end_hub
        for _ in range(len(nodes)):
            if current_node not in visited:
                for neighbor in edges[current_node]:
                    weight: int|float = self.get_node_weight(
                        nodes[neighbor].metadata.zone
                    )
                    final_weight: int = self.nodes_distances[current_node] + weight
                    estimated_weight: int|float = self.nodes_distances[neighbor]
                    if final_weight < estimated_weight:
                        self.nodes_distances[neighbor] = final_weight
                visited.add(current_node)
                current_node = min(
                    self.nodes_distances,
                    key=lambda k: float("inf") if k in visited else self.nodes_distances.get(k)
                )

        return self.nodes_distances