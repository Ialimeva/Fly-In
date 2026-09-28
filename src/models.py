from pydantic import BaseModel, Field
from typing import Literal


class MetaData(BaseModel, extra="forbid"):
    zone: Literal[
        "normal",
        "blocked",
        "restricted",
        "priority"
    ] = Field(default="normal")
    color: str | None = Field(default=None)
    max_drones: int = Field(default=1, gt=0)

class Hub(BaseModel, extra="forbid"):
    type: Literal[
        "start_hub",
        "end_hub",
        "hub"
    ] = Field(default="hub")
    name: str
    x: int
    y: int
    metadata: MetaData = Field(default=MetaData())

class Connection(BaseModel, extra="forbid"):
    name1: str
    name2: str
    max_link_capacity: int = Field(default=1, gt=0)

class Map(BaseModel, extra="forbid"):
    nb_drones: int = Field(default=1, gt=0)
    hubs: dict[str, Hub] = {}
    connections: dict[str, Connection] = {}