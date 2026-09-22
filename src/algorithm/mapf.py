from .astar import Astar
from typing import Any


class Mapf:
    def __init__(self, astar: Astar):
        self.astar: Astar = astar
        self.mafp: list[dict[int, dict[str, Any]]] = []

    def prioritized_planning(self, drone: int) -> set[dict[int, dict[str, Any]]]:
        constrains: dict[int, list[dict[str, Any]]] = {}
        for i in range(drone):
            constrains = self.astar.path_to_goal(i + 1, constrains)

        return constrains