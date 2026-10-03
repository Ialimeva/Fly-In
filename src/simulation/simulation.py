from ..models import Map
from ..parser import Parser
from ..algorithm import MakeGraph, Dijkstra, Astar, Mapf
from ..visual import Visual
from typing import Any


class Simulation:
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
    ) -> dict[int, Any]:
        for drone in joint_plan:
            for target, turn in joint_plan[drone]:
                if turn not in self.actions_per_turn:
                    self.actions_per_turn[turn] = []
                self.actions_per_turn[turn].append(
                    {
                        "D": drone,
                        "target": target,
                    }
                )

        return self.actions_per_turn

# TODO: Change the output to follow the subject
    def output_format(
        self,
        joint_plan: dict[int, Any],
    ) -> None:
        self.set_action_per_turn(joint_plan)
        for turn in self.actions_per_turn:
            if turn == 0:
                continue
            print(f"Turn {turn} -> ", end="")
            for action in self.actions_per_turn[turn]:
                print(f"D{action['D']}-{action['target']}", end=" ")
            print()


    def run(self) -> None:
        joint_plan = self.mapf.cooperative_astar(
            self.map.nb_drones
        )
        self.output_format(joint_plan)
        self.visual.start()