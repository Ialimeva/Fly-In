# TODO: Ask Teddy about how to not add try except
try:
    import questionary
except ModuleNotFoundError:
    print("Questionary not installed.")
    raise SystemExit(1)


class GetMap:
    def __init__(self):
        self.map_path: str

    def get_level(self) -> str:
        level: str = questionary.select(
            "Choose difficulty:",
            choices=[
                "easy",
                "medium",
                "hard",
                "challenger",
                "My own map"
            ]
        ).ask()

        return level

    def get_map_path(self) -> str:
        level: str = self.get_level()
        if level == "My own map":
            self.map_path = questionary.path(
                "What's the path of your custom map?\n" + 
                "Click on Tab for navigation"
            ).ask()

        elif level == "easy":
            self.map_path = "maps/" + level + "/" + questionary.select(
                "Choose map:",
                choices=[
                    "01_linear_path.txt",
                    "02_simple_fork.txt",
                    "03_basic_capacity.txt",
                ]
            ).ask()

        elif level == "medium":
            self.map_path = "maps/" + level + "/" + questionary.select(
                "Choose map:",
                choices=[
                    "01_dead_end_trap.txt",
                    "02_circular_loop.txt",
                    "03_priority_puzzle.txt",
                ]
            ).ask()

        elif level == "hard":
            self.map_path = "maps/" + level + "/" + questionary.select(
                "Choose map:",
                choices=[
                    "01_maze_nightmare.txt",
                    "02_capacity_hell.txt",
                    "03_ultimate_challenge.txt",
                ]
            ).ask()

        elif level == "challenger":
            self.map_path = "maps/" + level + "/" + "01_the_impossible_dream.txt"

        else:
            raise ValueError("Map level does not exist")

        return self.map_path
