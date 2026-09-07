import re
from pydantic import TypeAdapter
from typing import Any
from .get_map_path import GetMapPath
from models import Map, Hub, Connection, MetaData


class Parser:
    def __init__(self) -> None:
        self.map_getter: GetMapPath = GetMapPath()
        self.nb_drones: int = 0
        self.start_hub: Hub = Hub()
        self.end_hub: Hub = Hub()
        self.hubs: list[Hub] = []
        self.connections: list[Connection] = []

    def get_map_file(self) -> str:
        self.map_path = self.map_getter.get_map_path()

        return self.map_path

    def validate_map(self) -> Map:
        self.get_map_file()
        try:
            with open(self.map_path, "r") as f:
                self.file_content = [
                    l for l in f.read().split("\n")
                    if l and l[0] != '#'
                ]
            for i, line in enumerate(self.file_content):
                regex: dict[str, tuple[str, ...]] = {
                    "nb_drones": (r"^nb_drones:\s+(?P<nb_drones>\d+)$"),
                    "start_hub": (
                        r"start_hub:\s+(?P<name>[^\s-]+)",
                        r"\s+(?P<x>\d+)\s+(?P<y>\d+)",
                        r"(\s+\[(?P<metadata>[^\]]+)\])?"
                    ),
                    "end_hub": (
                        r"end_hub:\s+(?P<name>[^-\s]+)",
                        r"\s+(?P<x>\d+)\s+(?P<y>\d+)",
                        r"(\s+\[(?P<metadata>[^\]]+)\])?"
                    ),
                    "hub": (
                        r"hub:\s+(?P<name>[^-\s]+)",
                        r"\s+(?P<x>\d+)\s+(?P<y>\d+)",
                        r"(\s+\[(?P<metadata>[^\]]+)\])?"
                    ),
                    "connection": (
                        r"connection:\s+(?P<name1>[^-\s]+)",
                        r"-(?P<name2>[^-\s]+)",
                        r"(\s+\[max_link_capacity=(?P<max_link_capacity>\d+)\])?"
                    ),
                }
                if i == 0 and (match := re.match("".join(regex["nb_drones"]), line)):
                    self.nb_drones = match.group("nb_drones")

                elif i > 0 and (match := re.match("".join(regex["start_hub"]), line)):
                    elements: dict[str, Any] = match.groupdict()
                    if elements["metadata"]:
                        datas: list[str] = elements["metadata"].split()
                        metadata: dict[str, str] = {}
                        for d in datas:
                            key, value = d.split("=", 1)
                            metadata[key] = value
                            elements["metadata"] = metadata
                    else:
                        elements["metadata"] = MetaData()
                    self.start_hub = Hub(**elements)

                elif i > 0 and (match := re.match("".join(regex["end_hub"]), line)):
                    elements: dict[str, Any] = match.groupdict()
                    if elements["metadata"]:
                        datas: list[str] = elements["metadata"].split()
                        metadata: dict[str, str] = {}
                        for d in datas:
                            key, value = d.split("=", 1)
                            metadata[key] = value
                            elements["metadata"] = metadata
                    else:
                        elements["metadata"] = MetaData()
                    self.end_hub = Hub(**elements)

                elif i > 0 and (match := re.match("".join(regex["hub"]), line)):
                    elements: dict[str, Any] = match.groupdict()
                    if elements["metadata"]:
                        datas: list[str] = elements["metadata"].split()
                        metadata: dict[str, str] = {}
                        for d in datas:
                            key, value = d.split("=", 1)
                            metadata[key] = value
                            elements["metadata"] = metadata
                    else:
                        elements["metadata"] = MetaData()
                    self.hubs.append(Hub(**elements))

                elif i > 0 and (match := re.match("".join(regex["connection"]), line)):
                    elements: dict[str, Any] = match.groupdict()
                    if elements["max_link_capacity"] is None:
                        elements.pop("max_link_capacity")
                    self.connections.append(Connection(**elements))

                else:
                    continue

            return Map(
                nb_drones=self.nb_drones,
                start_hub=self.start_hub,
                end_hub=self.end_hub,
                hubs=self.hubs,
                connections=self.connections
            )
                        
        except Exception as e:
            raise Exception(e)