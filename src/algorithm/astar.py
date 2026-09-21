from ..models import Hub
from .graph import MakeGraph
from typing import Any


class Astar:
    def __init__(
        self,
        node_distances: dict[str, int],
        graph: MakeGraph
    ) -> None:
        self.node_distances: dict[str, int] = node_distances
        print(self.node_distances)
        self.graph: MakeGraph = graph
        self.nodes: dict[str, Hub] = self.graph.nodes
        self.start_hub, self.end_hub = self.graph.get_endpoints()
        self.neighbors: dict[str, set[str]] = self.graph.get_graph()

    def get_zone_note(self, node: str) -> float:
        zone: str = self.nodes[node].metadata.zone
        if zone == "normal":
            return 1
        elif zone == "priority":
            return 0.5
        elif zone == "restricted":
            return 2
        else:
            return float("inf")

    def get_g(self, node: str, neighbor: str) -> float:
        zone_type: float = self.get_zone_note(neighbor)
        coords_distance: int = self.graph.goal_manhattan(neighbor)
        return (
            zone_type +
            coords_distance
        )

    def get_h(self, node: str) -> int:
        return self.node_distances[node]

    def get_f(self, current_node: str, neighbor: str) -> float:
        g: float = self.get_g(current_node, neighbor)
        h: int = self.get_h(neighbor)

        return g + h

    def min_node(self, choices: dict[str, float]) -> str:
        return min(
            choices,
            key=lambda k: choices[k],
            default=None
        )


    def get_choice(
        self, 
        turn: int,
        current_node: str,
        visited: set[str],
        constraint: dict[int, list[dict[str, Any]]] | None
    ) -> str | None:
        previous_choices: list[str] = []

        if constraint and turn in constraint:
            for c in constraint[turn]:
                if "-" in c["target"]:
                    _, current = c["target"].split("-")
                    previous_choices.append(current)
                else:
                    previous_choices.append(c["target"])
        choices: dict[str, float] = {}
        for neighbor in self.neighbors[current_node]:
            if neighbor not in visited:
                f: float = self.get_f(current_node, neighbor)
                choices[neighbor] = f

        choice: str = self.min_node(choices)
        if choice in previous_choices:
            second_choice: str | None = None
            for k, v in choices.items():
                if v == choices[choice] and k != choice:
                    second_choice = k
            return second_choice

        return choice


    def path_to_goal(
        self,
        drone: int,
        constrains: dict[int, list[dict[str, Any]]]
    ) -> list[tuple[int, str, str]]:
        turn: int = 0
        visited: set[str] = set()
        current_node: str = self.start_hub

        while current_node != self.end_hub:
            choice: str | None = None
            while choice is None:
                turn += 1
                choice = self.get_choice(turn, current_node, visited, constrains)

            visited.add(current_node)
            parent_node: str = current_node
            current_node = choice
            if self.nodes[current_node].metadata.zone == "restricted":
                if turn not in constrains:
                    constrains[turn] =  []
                constrains[turn].append({
                    "D": drone,
                    "source": parent_node,
                    "target": parent_node + "-" + current_node,
                })
                parent_node = parent_node + "-" + current_node
                turn += 1
            if turn not in constrains:
                constrains[turn] = []
            constrains[turn].append({
                "D": drone,
                "source": parent_node,
                "target": current_node,
            })            
        return constrains