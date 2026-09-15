from ..models import Hub
from .graph import MakeGraph

# TODO: Arrange code for better code quality
class Dijkstra:
    def __init__(self, graph: MakeGraph) -> None:
        self.graph: MakeGraph = graph
        self.nodes: dict[str, Hub] = self.graph.nodes
        self.neighbors: dict[str, Hub] = self.graph.get_graph()
        self.nodes_distances: dict[str, int | float] = {}

    def set_starting_distance(self) -> None:
        for k, v in self.nodes.items():
            if v.type == "end_hub":
                self.nodes_distances[k] = 0
                self.end_hub: str = k
            else:
                if v.type == "start_hub":
                    self.start_hub: str = k
                self.nodes_distances[k] = float("inf")

    def nodes_distance_from_goal(self) -> dict[str, int|float]:
        self.set_starting_distance()
        visited: set[str] = set()
        current_node: str = self.end_hub
        for _ in range(len(self.nodes)):
            if current_node not in visited:
                for neighbor in self.neighbors[current_node]:
                    weight: int | float = self.graph.get_node_weight(
                        self.nodes[neighbor].metadata.zone
                    )
                    final_weight: int = self.nodes_distances[current_node] + weight
                    estimated_weight: int | float = self.nodes_distances[neighbor]
                    if final_weight < estimated_weight:
                        self.nodes_distances[neighbor] = final_weight
                visited.add(current_node)
                current_node = min(
                    self.nodes_distances,
                    key=lambda k: (
                        float("inf") if k in visited
                        else self.nodes_distances.get(k)
                    )
                )

        return self.nodes_distances