"""
Make graph from Map instance.

This module takes the Map instance and creates a graph
for the program to use.

Exported class:
    MakeGraph: Graph makes.
"""
from models import Map, Hub, Connection


class MakeGraph:
    """
    Make graph from Map instance.

    Attributes:
        nodes: Map hubs.
        edges: Map connections.
        neighbors: Each nodes and edges neighbors.
        zone_capacity: Each nodes capacity.
        link_capacity: Each edges capacity.
    """
    def __init__(self, map: Map) -> None:
        self.nodes: dict[str, Hub] = map.hubs
        self.edges: dict[str, Connection] = map.connections
        self.neighbors: dict[str, set[str]] = {
            k: set() for k in self.nodes
        }
        self.zone_capacity: dict[str, int] = {
            node: self.nodes[node].metadata.max_drones
            for node in self.nodes
        }
        self.link_capacity: dict[str, int] = {
            edge: self.edges[edge].max_link_capacity
            for edge in self.edges
        }

    def get_endpoints(self) -> tuple[str, str]:
        """Return start and end points of map."""
        for k, v in self.nodes.items():
            if v.type == "start_hub":
                self.start_hub: str = k
            elif v.type == "end_hub":
                self.end_hub: str = k
            continue

        return (self.start_hub, self.end_hub)

    def get_graph(self) -> dict[str, set[str]]:
        """Return full graph representation."""
        for node in self.nodes:
            for edge in self.edges:
                if self.edges[edge].name1 == node:
                    neighbor: str = self.edges[edge].name2
                    if self.nodes[neighbor].metadata.zone == "restricted":
                        self.neighbors[node].add(edge)
                        self.neighbors[neighbor].add(edge)
                        if edge not in neighbor:
                            self.neighbors[edge] = set()
                        self.neighbors[edge].add(node)
                        self.neighbors[edge].add(neighbor)
                    else:
                        self.neighbors[node].add(neighbor)
                        self.neighbors[neighbor].add(node)

        return self.neighbors
