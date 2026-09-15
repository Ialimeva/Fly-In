from ..models import Map
from ..parser import Parser
from ..algorithm import MakeGraph, Dijkstra


class Simulation:
    def __init__(self) -> None:
        self.parser: Parser = Parser()
        self.map: Map = self.parser.validate_map()
        self.graph: MakeGraph = MakeGraph(self.map)
        self.dijkstra: Dijkstra = Dijkstra(self.graph)

    def run(self) -> None:
        print(self.dijkstra.nodes_distance_from_goal())
