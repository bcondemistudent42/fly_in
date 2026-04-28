import os
from enum import StrEnum

from src.parsing.checks import (
    check_hubs,
    check_metadata,
    check_metadata_connection,
    check_simple_connection,
    last_check,
    make_links,
)
from src.parsing.regex_extract import (
    extract_color,
    extract_max_drones,
    extract_zone,
)


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


def get_maps():
    output = []
    for x in os.listdir("maps"):
        if x.endswith(".txt"):
            output.append(x)
        else:
            raise ValueError("Map must be a .txt")
    return output


def map_valid(my_map):
    i = 0
    j = 1
    connection_check = []
    my_replace = {ord("["): "", ord("]"): "", ord(","): "", ord("'"): ""}
    my_hubs = {}
    start_name = ""
    end_name = ""
    my_hubs["hubs_links"] = []
    format_err = "Format Error: Must respect pattern 'nb_drones: int'"

    try:
        with open("maps/" + my_map) as f:
            for line in f:
                if line.startswith("#") or len(line.strip()) == 0:
                    pass
                elif ":" not in line:
                    raise ValueError(format_err)
                else:
                    if i == 0 and "nb_drones" not in line:
                        raise ValueError("First line must be 'nb_drones'")
                    elif i == 0:
                        try:
                            temp = line.split(":")
                            int(temp[1])
                            if len(temp) != 2:
                                raise ValueError
                        except Exception:
                            raise ValueError(f"{format_err}, ")
                        if temp[0] != "nb_drones":
                            raise ValueError(format_err)
                        else:
                            my_hubs["nb_drones"] = int(temp[1])
                    else:
                        key = line.split(":")
                        if key[0] == Utils.START_HUB:
                            if len(connection_check) != 0:
                                j -= 1
                                raise ValueError("Must init HUBS before links")
                            data = key[1].split()[0:3]
                            metadata = handle_start_hub(
                                key, format_err, my_replace, start_name, data
                            )

                            max_drones = extract_max_drones(metadata)
                            if max_drones is None:
                                max_drones = my_hubs["nb_drones"]

                            start_name = data[0]
                            my_hubs[data[0]] = Hubs(
                                data[0],
                                data[1],
                                data[2],
                                (True, False),
                                extract_zone(str(metadata)),
                                max_drones,
                                extract_color(str(metadata)),
                            )

                        elif key[0] == Utils.END_HUB:
                            if len(connection_check) != 0:
                                j -= 1
                                raise ValueError("Must init HUBS before links")
                            data = key[1].split()[0:3]
                            metadata = handle_end_hub(
                                key, format_err, my_replace, end_name, data
                            )

                            end_name = data[0]
                            max_drones = extract_max_drones(metadata)
                            if max_drones is None:
                                max_drones = my_hubs["nb_drones"]
                            my_hubs[data[0]] = Hubs(
                                data[0],
                                data[1],
                                data[2],
                                (False, True),
                                extract_zone(str(metadata)),
                                max_drones,
                                extract_color(str(metadata)),
                            )

                        elif key[0] == Utils.HUB:
                            if len(connection_check) != 0:
                                j -= 1
                                raise ValueError("Must init HUBS before links")
                            data = key[1].split()[0:3]
                            metadata = handle_hub(
                                key, format_err, my_replace, my_hubs, data
                            )

                            my_hubs[data[0]] = Hubs(
                                data[0],
                                data[1],
                                data[2],
                                (False, False),
                                extract_zone(str(metadata)),
                                extract_max_drones(metadata),
                                extract_color(str(metadata)),
                            )

                        elif key[0] == Utils.CONNECTION:
                            data = key[1].split()[0:2]
                            meta = key[1].split()[1::]
                            if len(meta) == 0:
                                value = 1
                            else:
                                if meta[0][0] != "[" or meta[-1][-1] != "]":
                                    raise ValueError("Wrong Metadata Format")
                                value = check_metadata_connection(str(meta))
                            my_hubs["hubs_links"].append(
                                ((key[1].split()[0].strip(), value))
                            )
                            if len(line.split(":")) != 2:
                                raise ValueError(
                                    f"Invalid line, {format_err}, "
                                )
                            connection_check.append(line.split(":")[1])
                        else:
                            raise ValueError(f"Invalid line, {format_err}, ")
                    if len(connection_check) != len(set(connection_check)):
                        raise ValueError("Can't declare twice same connection")
                    check_simple_connection(connection_check)
                    i = 1
                j += 1

    except Exception as e:
        raise Exception(f"{e} Line: {j}")
    check_hubs(my_hubs)
    last_check(start_name, end_name, my_hubs)
    return my_hubs


def handle_hub(key, format_err, my_replace, my_hubs, data):
    pre_metadata = key[1].split()[3::]

    if len(data) < 3 or len(key[1].split()) > 6:
        raise ValueError(format_err)
    if len(pre_metadata) > 0:
        if pre_metadata[0][0] != "[" or pre_metadata[-1][-1] != "]":
            raise ValueError("Wrong Metadata Format")

    metadata = str(pre_metadata).translate(my_replace)
    check_metadata(metadata)

    if my_hubs.get(data[0]) is not None:
        raise ValueError("Can't declare twice a Hub with same name")

    return metadata


def handle_start_hub(key, format_err, my_replace, start_name, data):
    pre_metadata = key[1].split()[3::]

    if len(data) < 3 or len(key[1].split()) > 6:
        raise ValueError(format_err)
    if len(pre_metadata) > 0:
        if pre_metadata[0][0] != "[" or pre_metadata[-1][-1] != "]":
            raise ValueError("Wrong Format")

    metadata = str(pre_metadata).translate(my_replace)
    check_metadata(metadata)

    if start_name != "":
        raise ValueError("Can't init twice start,")
    return metadata


def handle_end_hub(key, format_err, my_replace, end_name, data):
    pre_metadata = key[1].split()[3::]

    if len(data) < 3 or len(key[1].split()) > 6:
        raise ValueError(format_err)
    if len(pre_metadata) > 0:
        if pre_metadata[0][0] != "[" or pre_metadata[-1][-1] != "]":
            raise ValueError("Wrong Format")

    metadata = str(pre_metadata).translate(my_replace)
    check_metadata(metadata)

    if end_name != "":
        raise ValueError("Cannot init twice end_hub")
    return metadata


def make_displayable(choosen_map: str):
    full_maps = {}
    try:
        maps = get_maps()
        if len(maps) == 0 or not maps:
            raise ValueError("At least one map must be available")
    except Exception as e:
        raise ValueError(f"File error: {e}")
    valid_maps = []
    for elt in maps:
        try:
            full_maps[elt] = map_valid(elt)
            valid_maps.append(elt)
        except Exception as e:
            raise ValueError(f"Error in file {elt}: {e}")

    if choosen_map not in valid_maps:
        raise ValueError(f"The choosen map is not valid : '{choosen_map}'")
    displayable_map = make_links(full_maps[choosen_map])

    return displayable_map
