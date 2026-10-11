from .astar import Astar
from typing import Any


class Mapf:
    def __init__(self, astar: Astar):
        self.astar: Astar = astar
        self.reservation_table: list[tuple[Any, ...]] = []
        self.joint_plan: dict[int, Any] = {}

    def cooperative_astar(self, drone: int) -> tuple[
        dict[int, Any],
        list[tuple[Any, ...]]
    ]:
        for i in range(drone):
            path = self.astar.path_to_goal(i + 1, self.reservation_table)
            self.joint_plan[i + 1] = path

        return (
            self.joint_plan,
            self.reservation_table
        )