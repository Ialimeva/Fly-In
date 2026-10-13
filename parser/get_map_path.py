"""
Parse map path from user input.

Exported class:
    GetMapPath: map path getter.
"""
import questionary
from typing import Any


class GetMapPath:
    """Parse map path from user input."""
    def get_level(self) -> str:
        """Prompt the user to choose a level"""
        level: str = questionary.select(
            "Choose difficulty:",
            choices=[
                "easy",
                "medium",
                "hard",
                "challenger",
                "custom map"
            ]
        ).ask()

        return level

    def get_map_path(self) -> Any:
        """Prompt the user to choose a map and return the full path"""
        level: str = self.get_level()
        dir: str = "maps/"
        if level == "custom map":
            self.map_path = questionary.path(
                "What's the path of your custom map?" +
                " (Use Tab for anvigation)"
            ).ask()

        elif level == "easy":
            self.map_path = dir + level + "/" + questionary.select(
                "Choose map:",
                choices=[
                    "01_linear_path.txt",
                    "02_simple_fork.txt",
                    "03_basic_capacity.txt",
                ]
            ).ask()

        elif level == "medium":
            self.map_path = dir + level + "/" + questionary.select(
                "Choose map:",
                choices=[
                    "01_dead_end_trap.txt",
                    "02_circular_loop.txt",
                    "03_priority_puzzle.txt",
                ]
            ).ask()

        elif level == "hard":
            self.map_path = dir + level + "/" + questionary.select(
                "Choose map:",
                choices=[
                    "01_maze_nightmare.txt",
                    "02_capacity_hell.txt",
                    "03_ultimate_challenge.txt",
                ]
            ).ask()

        elif level == "challenger":
            self.map_path = dir + level + "/" + "01_the_impossible_dream.txt"

        else:
            raise ValueError("Map level does not exist")

        return self.map_path
