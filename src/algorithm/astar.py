from ..models import Hub
from .graph import MakeGraph


class Astar:
    def __init__(
        self,
        node_distances: dict[str, int],
        graph: MakeGraph
    ) -> None:
        self.node_distances: dict[str, int] = node_distances
        self.graph: MakeGraph = graph
        self.nodes: dict[str, Hub] = self.graph.nodes
        self.start_hub, self.end_hub = self.graph.get_endpoints()
        self.neighbors: dict[str, set[str]] = self.graph.get_graph()

    def get_zone_note(self, node: str) -> float:
        zone: str = self.nodes[node].metadata.zone
        if zone == "normal":
            return 1
        elif zone == "priority":
            return 0.5
        elif zone == "restricted":
            return 2
        else:
            return float("inf")

    def get_g(self, node: str, neighbor: str) -> float:
        zone_type: float = self.get_zone_note(neighbor)
        coords_distance: int = self.graph.goal_manhattan(neighbor)
        return (
            zone_type +
            coords_distance
        )

    def get_h(self, node: str) -> int:
        return self.node_distances[node]

    def get_f(self, current_node: str, neighbor: str) -> float:
        g: float = self.get_g(current_node, neighbor)
        h: int = self.get_h(neighbor)

        return g + h

    def path_to_goal(self, drone: int) -> list[tuple[int, str, str]]:
        turn: int = 0
        visited: set[str] = set()
        current_node: str = self.start_hub
        path: list[tuple[int, str, str]] = []

        while current_node != self.end_hub:
            choices: dict[str, float] = {}
            for neigbor in self.neighbors[current_node]:
                if neigbor not in visited:
                    f: float = self.get_f(current_node, neigbor)
                    choices[neigbor] = f
                else:
                    continue
            visited.add(current_node)
            parent_node: str = current_node
            current_node = min(
                choices,
                key=lambda k: (
                    choices[k] if k not in visited
                    else float("inf")
                )
            )
            path.append((drone, parent_node, current_node))

        return path