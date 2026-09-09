from models import Map, Hub


class MakeGraph:
    def __init__(self, map: Map) -> None:
        self.map: Map = map

    def all_node_neighbors(self) -> dict[str, list[str]]:
        neighbors: dict[str, list[str]] = {}
        for node in self.map.hubs:
            node_neighbors: list[str] = []
            for connection in self.map.connections:
                if connection.name1 == node:
                    node_neighbors.append(
                        connection.name2
                    )
            neighbors[node] = node_neighbors

        return neighbors
