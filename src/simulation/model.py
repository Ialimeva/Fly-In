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
        print(self.graph.neighbors)
        print("\n" * 2)
        print(self.dijkstra.nodes_distance_from_goal())

        print(self.astar.path_to_goal(1))
