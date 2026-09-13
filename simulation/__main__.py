import re
from parser import Parser
from models import Map, Hub, Connection
from algorithm import MakeGraph, ReversedDijkstra


def main() -> None:
    try:
        parser: Parser = Parser()
        map: Map = parser.validate_map()
        print(map.connections)
        graph: MakeGraph = MakeGraph(map)
        dijkstra: ReversedDijkstra = ReversedDijkstra(map, graph)
        for k, v in graph.get_graph().items():
            print(k, v)
        print()
        for k, v in graph.get_reversed_graph().items():
            print(k, v)
        dijkstra.nodes_distance_from_goal()
    except Exception as e:
        print(f"An error occured: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
