"""
Calculate each nodes and edges distance form goal.

This module takes a graph and calculates each node and
edge distance from goal.

Exported class:
    Dijkstra: Calculate each nodes and edges distance form goal.
"""
from models import Hub
from .graph import MakeGraph
from typing import Any


class Dijkstra:
    """
    Calculate each nodes and edges distance form goal.

    Attributes:
        graph: Graph maker instance.
        nodes: Map nodes or hubs.
        neighbors: Each nodes and edges neighbors.
        nodes_distances: Each node and edge distance from goal.
    """
    def __init__(self, graph: MakeGraph) -> None:
        self.graph: MakeGraph = graph
        self.nodes: dict[str, Hub] = self.graph.nodes
        self.neighbors: dict[str, set[str]] = self.graph.get_graph()
        self.nodes_distances: dict[str, Any] = {}

    def set_starting_distance(self) -> None:
        """Set each elements estimated distance."""
        self.start_hub, self.end_hub = self.graph.get_endpoints()
        for k in self.neighbors:
            if k == self.end_hub:
                if self.nodes[k].metadata.zone == "blocked":
                    raise Exception("end_hub is blocked.")
                self.nodes_distances[k] = 0
            else:
                self.nodes_distances[k] = float("inf")

    def nodes_distance_from_goal(self) -> dict[str, int | float]:
        """Calculate each nodes and edges distance form goal."""
        self.set_starting_distance()
        reachable: list[str] = []
        explored: set[str] = set()
        reachable.append(self.end_hub)

        while reachable:
            current_node: str = reachable.pop(0)
            if current_node in explored:
                continue

            for neighbor in self.neighbors[current_node]:
                if neighbor in explored:
                    continue
                reachable.append(neighbor)

            for node in reachable:
                if "-" in node:
                    weight: int = self.nodes_distances[current_node] + 1
                else:
                    zone: str = self.nodes[node].metadata.zone
                    if zone == "blocked":
                        continue
                    if zone == "priority":
                        weight = self.nodes_distances[current_node] + 0.5
                    else:
                        weight = self.nodes_distances[current_node] + 1
                estimated_weight: int = self.nodes_distances[node]

                if weight < estimated_weight:
                    self.nodes_distances[node] = weight

            explored.add(current_node)
            reachable = sorted(
                reachable,
                key=lambda k: self.nodes_distances[k]
            )

        return self.nodes_distances
