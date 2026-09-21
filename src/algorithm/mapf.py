from .astar import Astar


class Mapf:
    def __init__(self, astar: Astar):
        self.astar: Astar = astar

    def prioritized_planning(self, drone: int) -> ...:
        ...