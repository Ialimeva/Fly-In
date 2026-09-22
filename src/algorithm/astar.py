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

    def get_g(self, neighbor: str) -> float:
        zone_score: float = self.get_zone_note(neighbor)
        return zone_score

    def get_h(self, node: str) -> int:
        return self.node_distances[node]

    def get_f(self, neighbor: str) -> float:
        g: float = self.get_g(neighbor)
        h: int = self.get_h(neighbor)

        return g + h

    def pick_node(
        self,
        turn: int,
        reachable: list[str],
        explored: set[str],
        constrains: dict[int, dict[str, Any]]
    ) -> str:
        occupied: set[str] = set()

        if constrains and turn in constrains:
            for c in constrains[turn]:
                if "-" in c["target"]:
                    _, target = c["target"].split("-")
                else:
                    target = c["target"]

            occupied.add(target)
        
        for node in reachable:
            if node in occupied or node in explored:
                continue
            reachable.remove(node)
            return node

        return None


    def path_to_goal(
        self,
        drone: int,
        constrains: dict[int, list[dict[str, Any]]]
    ) -> list[tuple[int, str, str]]:
        turn: int = 1
        reachable: list[str] = []
        explored: set[str] = set()
        reachable.append(self.start_hub)
        score: dict[str, int] = {}

        while self.end_hub not in explored:
            current_node = self.pick_node(turn, reachable, explored, constrains)

            if current_node == self.start_hub:
                for neighbor in self.neighbors[current_node]:
                    if neighbor in explored:
                        continue
                    score[neighbor] = self.get_f(neighbor)
                    reachable.append(neighbor)

                explored.add(current_node)
                reachable = sorted(reachable, key=lambda k: score[k])
                continue
                
    
            while current_node is None:
                turn += 1
                current_node: str = self.pick_node(turn, reachable, explored, constrains)

            if self.nodes[current_node].metadata.zone == "restricted":
                if turn not in constrains:
                    constrains[turn] = []
                constrains[turn].append({
                    "D": drone,
                    "target": "conn" + "-" + current_node
                })
                turn += 1

            if turn not in constrains:
                constrains[turn] = []
            constrains[turn].append({
                "D": drone,
                "target": current_node
            })

            for neighbor in self.neighbors[current_node]:
                if neighbor in explored:
                    continue
                reachable.append(neighbor)
                score[neighbor] = self.get_f(neighbor)

            explored.add(current_node)
            reachable = sorted(reachable, key=lambda k: score[k])
            turn += 1

        return constrains