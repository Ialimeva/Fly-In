from ..models import Hub, Connection
from .graph import MakeGraph
from typing import Any


class Astar:
    def __init__(
        self,
        node_distances: dict[str, int],
        graph: MakeGraph
    ) -> None:
        self.node_distances: dict[str, int] = node_distances
        self.graph: MakeGraph = graph
        self.nodes: dict[str, Hub] = self.graph.nodes
        self.edges: dict[str, Connection] = self.graph.edges
        self.start_hub, self.end_hub = self.graph.get_endpoints()
        self.neighbors: dict[str, set[str]] = self.graph.get_graph()
        self.cost_so_far: dict[str, int] = {
            k: 0 if k == self.start_hub else float("inf") 
            for k in self.neighbors
        }

    def get_zone_note(self, node: str) -> float:
        zone: str = self.nodes[node].metadata.zone
        if zone in ("normal", "restricted"):
            return 1
        elif zone == "priority":
            return 0.5
        else:
            return float("inf")

    def get_g(self, current: str, neighbor: str) -> float:
        g: int = self.cost_so_far[current] + self.get_zone_note(neighbor)
        return g

    def get_h(self, node: str) -> int:
        return self.node_distances[node]

    def get_f(self, neighbor: str) -> float:
        g: float = self.get_g(neighbor)
        h: int = self.get_h(neighbor)

        return g + h

    def path_to_goal(self) -> ...:
        reachable: list[str] = []
        explored: set[str] = set()
        reachable.append(self.start_hub)

        while reachable:
            current: str = reachable.pop(0)

            for neighbor in self.neighbors[current]:
                if neighbor in explored:
                    continue
                reachable.append(neighbor)

            for neighbor in reachable:
                if "-" in neighbor:
                    weight: int = self.cost_so_far[current] + 1
                else:
                    weight: int = self.get_g(current, neighbor)
                estimated_weight: int = self.cost_so_far[neighbor]
                if weight < estimated_weight:
                    self.cost_so_far[neighbor] = weight

            explored.add(current)
            reachable = sorted(reachable, key=lambda k: self.cost_so_far[k])
        
        return self.cost_so_far
