"""Map structure definitions.

This module defines the core data classes for representing map structures, 
including the map itself, hubs, connections, and metadata.

Exported Classes:
    Map: Represents the overall map structure.
    Hub: Represents a node or hub within the map.
    Connection: Represents a link or edge between hubs.
    Metadata: Represents descriptive metadata for the map.
"""
from pydantic import BaseModel, Field
from typing import Literal


class MetaData(BaseModel, extra="forbid"):
    """
    Represents the overall map structure.

    Attributes:
        zone (str): Given zone type of a hub
        color (str): Given color of a hub
        max_drones (int): Maximum drone a hub can contain
    """
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
    x: int = Field(le=100)
    y: int = Field(le=100)
    metadata: MetaData = Field(default=MetaData())


class Connection(BaseModel, extra="forbid"):
    name1: str
    name2: str
    max_link_capacity: int = Field(default=1, gt=0)


class Map(BaseModel, extra="forbid"):
    nb_drones: int = Field(default=1, gt=0, le=1000)
    hubs: dict[str, Hub] = {}
    connections: dict[str, Connection] = {}
