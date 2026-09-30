import re
from typing import Any


class RegexValidator:
    def __init__(self, map_path: str) -> str:
        self.map_path: str = map_path
        self.nb_drones_regex: tuple[str] = (
            r"^nb_drones:\s+(?P<nb_drones>\d+)$"
        )
        self.hub_regex: tuple[str, ...] = (
            r"^(?P<type>start_hub|end_hub|hub):\s+(?P<name>[^\s-]+)",
            r"\s+(?P<x>(-)?\d+)\s+(?P<y>(-)?\d+)",
            r"(\s+\[(?P<metadata>[^\]]+)\])?$"
        )
        self.connection_regex: tuple[str, ...] = (
            r"^connection:\s+(?P<name1>[^-\s]+)",
            r"-(?P<name2>[^-\s]+)",
            r"(\s+\[max_link_capacity=(?P<max_link_capacity>\d+)\])?$"
        )
        self.metadata_regex: tuple[str, ...] = (
            r"^[^\s]+=[^\s-]+",
            r"( [^\s-]+=[^\s-]+)*$",
        )
        self.raw_hubs: list[dict[str, Any]] = []
        self.raw_connections: list[dict[str, Any]] = []

    def read_map(self) -> dict[int, str]:
        try:
            with open(self.map_path, "r") as f:
                file_content: dict[int, str] = {
                    i + 1: line.strip()
                    for i, line in enumerate(
                        f.read().splitlines()
                    )
                    if line.strip() and line[0] != "#"
                }
                if len(file_content) == 0:
                    raise Exception("No data to extract from file")
            
            return file_content

        except Exception as e:
            raise Exception(e)

    def validate_file_content(self) -> tuple[Any, ...]:
        self.file_content: dict[int, str] = self.read_map()
        
        nb_drone_line_count: int = 0
        self.nb_drones: dict[str, str] | None = None

        for line_number, line in self.file_content.items():
            if (
                list(self.file_content)[0] == line_number
                and (match:= re.match("".join(self.nb_drones_regex), line))
            ):
                nb_drone_line_count += 1
                if nb_drone_line_count > 1:
                    raise ValueError(
                        f"Parsing error on line {line_number}:\n"
                        f"  Line content : {line!r}\n"
                        f"  Reason       : Duplicate nb_drones"
                    )

                self.nb_drones: dict[str, str] = match.groupdict()

            elif match:= re.match("".join(self.hub_regex), line):
                elements: dict[str, Any] = match.groupdict()
                metadata: dict[str, Any] = {}

                if elements["metadata"]:
                    print(elements["metadata"])
                    metadat_str: str = elements["metadata"]
                    if re.match("".join(self.metadata_regex), metadat_str):
                        metadat_str = metadat_str.split()
                        count_color: int = 0
                        count_zone: int = 0
                        count_max_drones: int = 0

                        for m in metadat_str:
                            if zone := re.search(
                                r"^zone=(?P<zone>normal|priority|restricted|blocked)$",
                                m
                            ):
                                count_zone += 1
                                metadata["zone"] = zone.group("zone")
                            elif color := re.search(
                                r"^color=(?P<color>[A-Za-z]+)$",
                                m
                            ):
                                count_color += 1
                                metadata["color"] = color.group("color")
                            elif max_drones := re.search(
                                r"^max_drones=(?P<max_drones>\d+)$",
                                m
                            ):
                                count_max_drones += 1
                                metadata["max_drones"] = max_drones.group("max_drones")

                            else:
                                raise ValueError(
                                    f"Parsing error on line {line_number}:\n"
                                    f"  Line content : {line!r}\n"
                                    f"  Reason       : Unknown zone metadata"
                                )
                    else:
                        raise ValueError(
                            f"Parsing error on line {line_number}:\n"
                            f"  Line content : {line!r}\n"
                            f"  Reason       : Unknown zone metadata"
                        )

                    for c in (count_color, count_zone, count_max_drones):
                        if c > 1:
                            raise ValueError(
                                f"Parsing error on line {line_number}:\n"
                                f"  Line content : {line!r}\n"
                                f"  Reason       : Duplicate metadata"
                            )                    
                    elements["metadata"] = metadata

                self.raw_hubs.append(elements)
            
            elif match:= re.match("".join(self.connection_regex), line):
                self.raw_connections.append(match.groupdict())

            else:
                raise ValueError(
                    f"Parsing error on line {line_number}:\n"
                    f"  Line content : {line!r}\n"
                    f"  Reason       : Unrecognized syntax"
                )
        
        components: list[tuple[Any, str]] = [
            (self.nb_drones, "nb_drones"),
            (self.raw_hubs, "hubs"),
            (self.raw_connections, "connections"),
        ]

        for data, name in components:
            if not data:
                raise Exception(f"Missing section in map file: {name}")

        return (
            self.nb_drones,
            self.raw_hubs,
            self.raw_connections
        )