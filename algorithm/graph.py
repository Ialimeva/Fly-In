from models import Map, Hub, Connection


class MakeGraph:
    def __init__(self, map: Map) -> None:
        self.nodes: dict[str. Hub] = map.hubs
        self.edges: list[Connection] = map.connections

    def get_graph(self) -> dict[str, list[str]]:
        neighbors: dict[str, list[str]] = {}
        for node in self.nodes:
            node_neighbors: list[str] = []
            for edge in self.edges:
                if edge.name1 == node:
                    node_neighbors.append(
                        edge.name2
                    )
            neighbors[node] = node_neighbors

        return neighbors

    def get_reversed_graph(self) -> dict[str, list[str]]:
        neighbors: dict[str, list[str]] = {}
        for node in self.nodes:
            node_neighbors: list[str] = []
            for edge in self.edges:
                if edge.name2 == node:
                    node_neighbors.append(
                        edge.name1
                    )
            neighbors[node] = node_neighbors

        return neighbors
