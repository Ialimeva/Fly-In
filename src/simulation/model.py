from ..models import Map
from ..parser import Parser
from ..algorithm import MakeGraph, Dijkstra, Astar


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

    def run(self) -> None:
        # for i, p in enumerate(path):
        # for i in range(self.map.nb_drones):
        path = self.astar.path_to_goal(1)
        print(path)
            # if i == len(path) - 1:
            #     print(f"{p[1]} -> {p[2]}")
            # else:
            #     print(p[1], flush=True, end=" -> ")
