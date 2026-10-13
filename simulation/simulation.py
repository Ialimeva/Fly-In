"""
Converge point of all packages and where the pipeline starts.

This module call and use all packages together
from parsing to visual.

Extracted class:
    Simulation: Run the full pipeline.
"""
from models import Map
from parser import Parser
from algorithm import MakeGraph, Dijkstra, Astar, Mapf
from visual import Visual
from typing import Any


class Simulation:
    """
    Run the full pipeline.

    Attributes:
        parser: Map parser.
        map: Parsed map.
        graph: Graph of the parsed map.
        dikstra: Check all nodes distance from goal of
        the map and used as heuristic value.
        astar: Check path of a drone from start to end
        using dijkstra heuristic distance.
        mapf: Call astar for all drones path.
        actions_per_turn: Organize all drones path by turn.
        visual: Visualize all drones path
    """
    def __init__(self) -> None:
        self.parser: Parser = Parser()
        self.map: Map = self.parser.validate_map()
        self.graph: MakeGraph = MakeGraph(self.map)
        self.dijkstra: Dijkstra = Dijkstra(self.graph)

        heuristic = self.dijkstra.nodes_distance_from_goal()
        if heuristic[self.graph.start_hub] == float("inf"):
            print("An error occured:")
            raise SystemExit("No route from start to goal")

        self.astar: Astar = Astar(
            self.dijkstra.nodes_distance_from_goal(),
            self.graph
        )
        self.mapf: Mapf = Mapf(self.astar)
        self.actions_per_turn: dict[int, Any] = {}
        self.visual: Visual = Visual(
            self.actions_per_turn,
            self.map.hubs,
            self.map.connections
        )

    def set_action_per_turn(
        self,
        joint_plan: dict[int, Any],
        reservation_table: list[tuple[Any, ...]],
    ) -> dict[int, Any]:
        """Organize all drones path by turn."""
        goal_capacity: int = 0
        for drone in joint_plan:
            for source, target, turn in joint_plan[drone]:
                if turn not in self.actions_per_turn:
                    self.actions_per_turn[turn] = []
                capacity: str = ""
                if target == self.graph.end_hub:
                    goal_capacity += 1
                    capacity = f"{goal_capacity}/{self.map.nb_drones}"
                elif source:
                    free_capacity, _ = self.astar.get_capacity(
                        turn,
                        source,
                        target,
                        reservation_table
                    )
                    if "-" in target:
                        base_capacity: int = self.graph.link_capacity[target]
                    else:
                        base_capacity = self.graph.zone_capacity[target]
                    used_capacity: int = base_capacity - free_capacity
                    capacity = f"{used_capacity}/{base_capacity}"
                self.actions_per_turn[turn].append(
                    {
                        "D": drone,
                        "source": source,
                        "target": target,
                        "capacity": capacity
                    }
                )

        return self.actions_per_turn

    def output_format(
        self,
        joint_plan: dict[int, Any],
        reservation_table: list[tuple[Any, ...]],
    ) -> None:
        """Show all actions per turn on terminal"""
        self.set_action_per_turn(joint_plan, reservation_table)
        for turn in self.actions_per_turn:
            if turn == 0:
                continue
            for action in self.actions_per_turn[turn]:
                print(f"D{action['D']}-{action['target']}", end=" ")
            print()

    def run(self) -> None:
        """Call and display each turn on terminal and visual"""
        joint_plan, reservation_table = self.mapf.cooperative_astar(
            self.map.nb_drones
        )
        self.output_format(joint_plan, reservation_table)
        self.visual.start()
