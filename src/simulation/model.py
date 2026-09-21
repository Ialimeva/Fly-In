from ..models import Map
from ..parser import Parser
from ..algorithm import MakeGraph, Dijkstra, Astar, Mapf
from typing import Any


class Simulation:
    def __init__(self) -> None:
        self.parser: Parser = Parser()
        self.map: Map = self.parser.validate_map()
        self.graph: MakeGraph = MakeGraph(self.map)
        self.dijkstra: Dijkstra = Dijkstra(self.graph)
        self.astar: Astar = Astar(
            self.dijkstra.nodes_distance_from_goal(),
            self.graph
        )
        self.mapf: Mapf = Mapf(self.astar)

    def run(self) -> None:
        mapf: dict[int, list[dict[str, Any]]] = self.mapf.prioritized_planning(
            self.map.nb_drones
        )
        # for key, value in mapf.items():
        #     print(f"Turn: {key} -> {value}")
