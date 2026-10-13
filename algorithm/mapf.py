"""
Computes and assemble each drones path.

This module calls astar for each drone and
assemble their path.

Exported class:
    Mapf: Computes and assemble each drones path.
"""
from .astar import Astar
from typing import Any


class Mapf:
    """
    Computes and assemble each drones path
    using reservation table.

    Attributes:
        astar: Astar instance.
        reservation_table: History of each drones path.
        joint_plan: Assembled drone paths.
    """
    def __init__(self, astar: Astar):
        self.astar: Astar = astar
        self.reservation_table: list[tuple[Any, ...]] = []
        self.joint_plan: dict[int, Any] = {}

    def cooperative_astar(self, drone: int) -> tuple[
        dict[int, Any],
        list[tuple[Any, ...]]
    ]:
        """Computes and assemble each drones path."""
        for i in range(drone):
            path = self.astar.path_to_goal(i + 1, self.reservation_table)
            self.joint_plan[i + 1] = path

        return (
            self.joint_plan,
            self.reservation_table
        )
