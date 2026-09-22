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
        self.start_hub, self.end_hub = self.graph.get_endpoints()
        for k in self.nodes:
            if k == self.end_hub:
                self.nodes_distances[k] = 0
            else:
                self.nodes_distances[k] = float("inf")

    def nodes_distance_from_goal(self) -> dict[str, int|float]:
        self.set_starting_distance()
        reachable: list[str] = []
        explored: set[str] = set()
        reachable.append(self.end_hub)

        while self.start_hub not in explored:
            current_node: str = reachable.pop(0)
            print(current_node, self.graph.get_node_weight(self.nodes[current_node].metadata.zone))

            for neighbor in self.neighbors[current_node]:
                if neighbor in explored:
                    continue
                reachable.append(neighbor)

            for node in reachable:
                zone: str = self.nodes[node].metadata.zone
                weight: int = self.graph.get_node_weight(zone) + self.nodes_distances[current_node]
                estimated_weight: int = self.nodes_distances[node]

                if weight < estimated_weight:
                    self.nodes_distances[node] = weight

            explored.add(current_node)
            reachable = sorted(reachable, key=lambda k: self.nodes_distances[k])

        return self.nodes_distances