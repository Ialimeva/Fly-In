from .dijkstra import Dijkstra
from .graph import MakeGraph


class Astar:
    def __init__(
        self,
        node_distances: dict[str, int],
        graph: MakeGraph
    ) -> None:
        self.node_distances: dict[str, int] = node_distances
        self.graph: MakeGraph = graph

    def get_g(self, node: str) -> float:
        ...

    def get_h(self, node: str) -> int:
        return self.node_distances[node]

    def get_f(self, g: float, h: int) -> float:
        ...

    def path_to_goal(self, drone: int) -> ...:
        turn: int = 0
