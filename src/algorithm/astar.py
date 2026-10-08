from ..models import Hub, Connection
from .graph import MakeGraph
from typing import Any


class Astar:
    def __init__(
        self,
        node_distances: dict[str, int],
        graph: MakeGraph
    ) -> None:
        self.node_distances: dict[str, int] = node_distances
        self.graph: MakeGraph = graph
        self.nodes: dict[str, Hub] = self.graph.nodes
        self.edges: dict[str, Connection] = self.graph.edges
        self.start_hub, self.end_hub = self.graph.get_endpoints()
        self.neighbors: dict[str, set[str]] = self.graph.get_graph()
        self.cost_so_far: dict[str, int] = {
            k: 0 if k == self.start_hub else float("inf") 
            for k in self.neighbors
        }
        self.came_from: dict[Any, Any] = {}

    def get_note(self, neighbor: str) -> float:
        if "-" in neighbor:
            return 1

        zone: str = self.nodes[neighbor].metadata.zone
        if zone in ("normal", "priority", "restricted"):
            return 1
        else:
            return float("inf")

    def get_capacity(
        self,
        turn: int,
        source: str,
        target: str,
        reservation_table: list[tuple[str, int]]
    ) -> int:
        occupied: int = len(
            [
                dest for dest, t in reservation_table
                if t == turn and dest == target
            ]
        )

        if "-" in target:
            return (self.graph.link_capacity[target] - occupied, 1)

        edge_capacity: int = 1
        if source != target and "-" not in source:
            edge: str = source + "-" + target
            if edge in self.graph.link_capacity:
                edge_capacity = self.graph.link_capacity[edge] - 1
        return (
            self.graph.zone_capacity[target] - occupied,
            edge_capacity
        )

    def get_g(self, current: str, neighbor: str) -> float:
        g: int = self.cost_so_far[current] + self.get_note(neighbor)
        return g

    def get_h(self, neighbor: str) -> int:
        return self.node_distances[neighbor]

    def get_f(self, current: str, neighbor: str) -> float:
        g: float = self.get_g(current, neighbor)
        h: int = self.get_h(neighbor)

        return g + h

    def path_to_goal(
        self,
        nb_drone: int,
        reservation_table: list[tuple[str, int]]
    ) -> list[str]:
        self.path: list[str] = []
        reachable: list[tuple[int, str, int]] = []
        explored: set[Any] = set()
        reachable.append((self.start_hub, 0))
        final_move: tuple[str, int] = ()

        while reachable:
            current: str = reachable.pop(0)
            if current in explored:
                continue
            source, t_source = current

            if source == self.end_hub:
                final_move = current
                break

            moves: list[tuple[str, int]] = [(source, 1)] + [
                (neighbor, self.get_note(neighbor))
                for neighbor in self.neighbors[source]
            ]

            for target, duration in moves:
                t_target: int = t_source + duration
                next_move: tuple[str, int] = (target, t_target)

                if next_move in explored:
                    continue
                if next_move in reservation_table:
                    current_capacity, edge_capacity = self.get_capacity(
                        t_target,
                        source,
                        target,
                        reservation_table
                    )
                    if edge_capacity < 1:
                        continue
                    if current_capacity < 1:
                        continue
                reachable.append(next_move)
                self.came_from[next_move] = current

            for move in reachable:
                target, t = move
                weight: int = self.get_g(source, target)
                estimated_weight: int = self.cost_so_far[target]
                if weight < estimated_weight:
                    self.cost_so_far[target] = weight

            explored.add(current)
            reachable = sorted(reachable, key=lambda r: self.get_f(source, r[0]))
        
        current = final_move
        while self.start_hub not in current:
            self.path.append(current)
            current = self.came_from[current]
        self.path.append((self.start_hub, 0))

        reservation_table.extend(self.path[::-1])

        return self.path[::-1]
