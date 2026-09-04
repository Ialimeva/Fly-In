from .get_map import GetMap


class Parser:
    def __init__(self) -> None:
        self.map_getter: GetMap = GetMap()
        self.map_path: str

    def get_map_file(self) -> str:
        self.map_path = self.map_getter.get_map_path()

        return self.map_path

    def validate_map(self) -> None:
        self.get_map_file()
        try:
            with open(self.map_path, "r") as f:
                print(f.read())
        except Exception as e:
            raise Exception(e)