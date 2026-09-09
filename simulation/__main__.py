import re
from parser import Parser
from models import Map, Hub, Connection
from algorithm import MakeGraph


def main() -> None:
    try:
        parser: Parser = Parser()
        map: Map = parser.validate_map()
        graph: MakeGraph = MakeGraph(map)
    except Exception as e:
        print(f"An error occured: {e}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
