try:
    from pydantic import BaseModel
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(e)


class MetaData(BaseModel, extra="forbid"):
    zone: str = "normal"
    color: str | None = None
    max_drones: int = 1


class Hub(BaseModel, extra="forbid"):
    name: str = ""
    x: int = 0
    y: int = 0
    metadata: MetaData = MetaData()


class Connection(BaseModel, extra="forbid"):
    name1: str = ""
    name2: str = ""
    max_link_capacity: int = 1


class Map(BaseModel, extra="forbid"):
    nb_drones: int = 0
    start_hub: Hub = Hub()
    end_hub: Hub = Hub()
    hubs: list[Hub] = []
    connections: list[Connection] = []