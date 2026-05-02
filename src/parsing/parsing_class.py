from enum import StrEnum


class Utils(StrEnum):
    START_HUB = "start_hub"
    END_HUB = "end_hub"
    HUB = "hub"
    CONNECTION = "connection"


class ZoneType(StrEnum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"


class Hubs:
    def __init__(
        self,
        name: str,
        x: str,
        y: str,
        check: tuple,
        zone_type,
        max_capacity,
        color,
    ):
        if "-" in name:
            raise ValueError("Can't have a dash in name")
        self.name = name
        try:
            self.x = int(x)
            self.y = int(y)
        except ValueError:
            raise ValueError("Coordinates must be INT")

        self.links = {}
        self.links["max_links"] = 1
        self.links["links"] = []

        self.start, self.end = check
        if max_capacity is None:
            self.max_drone = 1
        else:
            self.max_drone = int(max_capacity)

        if color is None or color == "rainbow":
            self.color = "white"
        else:
            self.color = color

        if zone_type is None:
            self.cost = float(1)
        elif zone_type == ZoneType.NORMAL:
            self.cost = float(1)
        elif zone_type == ZoneType.BLOCKED:
            self.cost = float("inf")
        elif zone_type == ZoneType.RESTRICTED:
            self.cost = 2
        elif zone_type == ZoneType.PRIORITY:
            self.cost = float(0.9)
        else:
            raise ValueError(f"Wrong zone type: {zone_type} does not exist")