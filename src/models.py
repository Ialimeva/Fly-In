from pydantic import BaseModel


class MetaData(BaseModel, extra="forbid"):
    zone: str = "normal"
    color: str | None = None
    max_drones: int = 1


class Hub(BaseModel, extra="forbid"):
    type: str = "hub"
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
    hubs: dict[str, Hub] = {}
    connections: list[Connection] = []