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
        self.came_from: dict[str, str] = {}

    def get_note(self, neighbor: str) -> float:
        if "-" in neighbor:
            return 1

        zone: str = self.nodes[neighbor].metadata.zone
        if zone in ("normal", "restricted"):
            return 1
        elif zone == "priority":
            return 0.5
        else:
            return float("inf")

    def get_g(self, current: str, neighbor: str) -> float:
        g: int = self.cost_so_far[current] + self.get_note(neighbor)
        return g

    def get_h(self, neighbor: str) -> int:
        return self.node_distances[neighbor]

    def get_f(self, current: str, neighbor: str) -> float:
        g: float = self.get_g(current, neighbor)
        h: int = self.get_h(neighbor)

        return g + h

    def path_to_goal(self) -> list[str]:
        self.path: list[str] = []
        reachable: list[str] = []
        explored: set[str] = set()
        reachable.append(self.start_hub)

        while reachable:
            current: str = reachable.pop(0)

            if current == self.end_hub:
                break

            for neighbor in self.neighbors[current]:
                if neighbor in explored:
                    continue
                reachable.append(neighbor)

            for neighbor in reachable:
                weight: int = self.get_g(current, neighbor)
                estimated_weight: int = self.cost_so_far[neighbor]
                if weight < estimated_weight:
                    self.cost_so_far[neighbor] = weight
                self.came_from[neighbor] = current

            explored.add(current)
            reachable = sorted(reachable, key=lambda k: self.get_f(current, k))
        
        current: str = self.end_hub
        while current != self.start_hub:
            self.path.append(current)
            current = self.came_from[current]
        self.path.append(self.start_hub)

        return self.path[::-1]
