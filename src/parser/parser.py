from ..models import Map, Hub, Connection, MetaData
from .get_map_path import GetMapPath
from .regex_validation import RegexValidator
from typing import Any


class Parser:
    def __init__(self) -> None:
        self.map_getter: GetMapPath = GetMapPath()
        self.map_path: str = self.map_getter.get_map_path()
        self.regex_validator: RegexValidator = RegexValidator(self.map_path)
        (
            self.raw_nb_drones,
            self.raw_hubs,
            self.raw_connections
        ) = self.regex_validator.validate_file_content()

        self.hubs: dict[str, Hub] = {}
        self.connections: dict[str, Connection] = {}

    def validate_nb_drones(self) -> int:
        nb_drones: int = int(self.raw_nb_drones["nb_drones"])
        if nb_drones > 0:
            return nb_drones
        return 1

    def validate_hubs(self) -> dict[str, Hub]:
        coords: set[tuple[int, int]] = set()
        count_start: int = 0
        count_end: int = 0

        for hub in self.raw_hubs:
            name: str = hub["name"]
            zone_type: str = hub["type"]
            x: int = int(hub["x"])
            y: int = int(hub["y"])

            if zone_type == "start_hub":
                count_start += 1
                if count_start > 1:
                    raise ValueError(f"Duplicate {zone_type}")

            if zone_type == "end_hub":
                count_end += 1
                if count_end > 1:
                    raise ValueError(f"Duplicate {zone_type}")

            if name in self.hubs:
                raise ValueError(f"Duplicate zone name found: {name!r}")

            if (x, y) in coords:
                raise ValueError(f"Duplicate zone coordinates found: {(x, y)}")
            coords.add((x, y))

            if hub["metadata"]:
                metadata: dict[str, Any] = hub["metadata"]
                hub["metadata"]: MetaData = MetaData(**metadata)

            else:
                hub.pop("metadata")

            if hub["type"] in ("start_hub", "end_hub"):
                nb_drones: int = self.validate_nb_drones()
                if "metadata" in hub:
                    hub["metadata"].max_drones = nb_drones
                else:
                    hub["metadata"] = MetaData(
                        max_drones=self.validate_nb_drones()
                    )

            self.hubs[hub["name"]] = Hub(**hub)

        return self.hubs
            
    def validate_connextions(self) -> dict[str, Connection]:
        for connection in self.raw_connections:
            name1: str = connection["name1"]
            name2: str = connection["name2"]
            edge: str = name1 + "-" + name2
            duplicate: str = name2 + "-" + name1
            max_link_capacity: str = connection["max_link_capacity"]

            for name in (name1, name2):
                if name not in self.hubs:
                    raise Exception(f"Unknown hub: {name!r}")

            if name1 == name2:
                raise Exception(
                    "A zone does not connect to itself"
                    f": {name1}-{name2}"
                )

            for conn in (edge, duplicate):
                if conn in self.connections:
                    raise Exception(f"Duplicate connection {edge}")
            
            if not connection["max_link_capacity"]:
                connection.pop("max_link_capacity")
            
            if max_link_capacity and "-" in max_link_capacity:
                raise Exception("Link capacity must be positive int")
            
            self.connections[edge] = Connection(**connection)
        
        return self.connections


    def validate_map(self) -> Map:
        nb_drones: int = self.validate_nb_drones()
        hubs: dict[str, Hub] = self.validate_hubs()
        connections: dict[str, Connection] = self.validate_connextions()

        return Map(
            nb_drones=nb_drones,
            hubs=hubs,
            connections=connections
        )
