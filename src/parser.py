import os
import re

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
                 color
                 ):
        self.name = name

        self.x = int(x)
        self.y = int(y)

        self.links = {}
        self.links["max_links"] = 1
        self.links["links"] = []

        self.start, self.end = check
        if max_capacity is None:
            self.max_drone = 1
        else:
            self.max_drone = int(max_capacity)

        if color is None:
            self.color = "white"
        else:
            self.color = color

        if zone_type is None:
            self.cost = float(1)
        elif zone_type == ZoneType.NORMAL:
            self.cost = float(1)
        elif zone_type == ZoneType.BLOCKED:
            self.cost = float('inf')
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
    j = 1
    connection_check = []
    try:
        with open("maps/" + my_map) as f:
            my_hubs = {}
            start_name = ""
            end_name = ""
            my_hubs["hubs_links"] = []
            format_err = "Format Error: Must respect pattern 'nb_drones: int'"
            i = 0
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
                        my_map = {
                            ord("["): "", ord("]"): "",
                            ord(","): "", ord("'"): ""}
                        if key[0] == Utils.START_HUB:
                            data = key[1].split()[0:3]
                            pre_metadata = key[1].split()[3::]

                            print(key[1].split()[3::])
                            if len(pre_metadata) > 0:
                                if (pre_metadata[0][0] != "["
                                        or pre_metadata[-1][-1] != "]"):
                                    raise ValueError("Wrong Metadata Format")

                            metadata = str(pre_metadata).translate(my_map)
                            check_metadata(metadata)
                            if start_name != "":
                                raise ValueError("Can't init twice start,")
                            start_name = data[0]
                            my_hubs[data[0]] = Hubs(
                                data[0],
                                data[1],
                                data[2],
                                (True, False),
                                extract_zone(str(metadata)),
                                extract_max_drones(metadata),
                                extract_color(str(metadata))
                                                    )
                        elif key[0] == Utils.END_HUB:
                            data = key[1].split()[0:3]
                            pre_metadata = key[1].split()[3::]
                            metadata = str(pre_metadata).translate(my_map)

                            if len(pre_metadata) > 0:
                                if (pre_metadata[0][0] != "["
                                        or pre_metadata[-1][-1] != "]"):
                                    raise ValueError("Wrong Metadata Format")

                            check_metadata(metadata)
                            if end_name != "":
                                raise ValueError(
                                      "Cannot init twice end_hub"
                                      )
                            end_name = data[0]
                            my_hubs[data[0]] = Hubs(
                                data[0],
                                data[1],
                                data[2],
                                (False, True),
                                extract_zone(str(line)),
                                extract_max_drones(line),
                                extract_color(str(line))
                                                    )
                        elif key[0] == Utils.HUB:
                            data = key[1].split()[0:3]
                            pre_metadata = key[1].split()[3::]

                            if len(pre_metadata) > 0:
                                if (pre_metadata[0][0] != "["
                                        or pre_metadata[-1][-1] != "]"):
                                    raise ValueError("Wrong Metadata Format")

                            metadata = str(pre_metadata).translate(my_map)
                            check_metadata(metadata)
                            if my_hubs.get(data[0]) is not None:
                                raise ValueError(
                                    "Can't declare twice a Hub with same name"
                                    )
                            my_hubs[data[0]] = Hubs(
                                data[0],
                                data[1],
                                data[2],
                                (False, False),
                                extract_zone(str(line)),
                                extract_max_drones(line),
                                extract_color(str(line))
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
                                ((key[1].split()[0].strip(),
                                  value))
                                )
                            connection_check.append(line.split()[1])
                        else:
                            raise ValueError(
                                  f"Unknown Type, {format_err}, "
                                  )
                    i = 1
                    if len(connection_check) != len(set(connection_check)):
                        raise ValueError("Can't declare twice same connection")
                j += 1
    except Exception as e:
        raise Exception(f"{e} Line: {j}")
    for elt in connection_check:
        for elt1 in connection_check:
            left = elt1.split("-")[0]
            right = elt1.split("-")[1]
            total = f"{right}-{left}"
            if total == elt:
                raise ValueError("Can't declare twice same connection")
    if start_name == "":
        raise ValueError(
                         f"MISSING : {Utils.START_HUB}"
                         )
    if end_name == "":
        raise ValueError(
                         f"MISSING : {Utils.END_HUB}"
                         )
    if len(my_hubs["hubs_links"]) == 0:
        raise ValueError(
                         "MISSING : links between hubs"
                         )
    if my_hubs["nb_drones"] < 0:
        raise ValueError("You must have at least 0 drones")
    check_hubs(my_hubs)
    return my_hubs


def check_metadata_connection(my_data: str):
    if my_data is None:
        return None
    clean_data = my_data.split()

    if len(clean_data) > 1:
        raise ValueError("What are u trying to do", "Wrong Metadata format")
    rslt = extract_max_link_capacity(clean_data[0])
    if rslt is None:
        raise ValueError("What are u trying to do", "Wrong Metadata format")
    if int(rslt) < 0:
        raise ValueError("Max connections must be > 0")
    return rslt


def check_metadata(my_data: str):
    if my_data is None:
        return None
    clean_data = my_data.split()
    if my_data.count("color=") > 1:
        raise ValueError("CHOOSE ONE COLOR")
    if my_data.count("zone=") > 1:
        raise ValueError("CHOOSE ONE ZONE")
    if my_data.count("max_drones=") > 1:
        raise ValueError("CHOOSE ONE NUMBER")
    if len(clean_data) > 3:
        raise ValueError("Wrong Metadata format")
    for elt in clean_data:
        if (
            extract_zone(elt) is None and
                extract_color(elt) is None and
                extract_max_drones(elt) is None):
            raise ValueError(
                    "What are u trying to do",
                    "Wrong Metadata format"
                    )


def extract_zone(my_string):
    pattern = r"(?:(?<=[\[\s])|^)zone=([^\]\s]+)"
    match = re.search(pattern, my_string)
    if match:
        return match.group(1)
    return None


def extract_color(my_string):
    pattern = r"(?:(?<=[\[\s])|^)color=([^\]\s]+)"
    match = re.search(pattern, my_string)
    if match:
        if (match.group(0).split("=")[0]).strip() != "color":
            raise ValueError(f"This is not valid: {match.group(0)}")
        return match.group(1)
    return None


def extract_max_drones(my_string):
    pattern = r"(?:(?<=[\[\s])|^)max_drones=([^\]\s]+)"
    match = re.search(pattern, my_string)
    rslt = None
    if match:
        try:
            rslt = int(match.group(1))
        except ValueError:
            raise ValueError("Number of drone must be an INTEGER")
        if rslt < 0:
            raise ValueError("Number of drone must be positive")
    return rslt


def extract_max_link_capacity(my_string):
    pattern = r"(?:(?<=[\[\s])|^)max_link_capacity=([^\]\s]+)"
    match = re.search(pattern, my_string)
    rslt = None
    if match:
        try:
            rslt = int(match.group(1))
        except ValueError:
            raise ValueError("Max link capacity must be an INTEGER")
        if rslt < 0:
            raise ValueError("Max link capacity must be positive")
    return rslt


def extract_metadata(my_string):
    pattern = r"\[([^\]]+)\]"
    match = re.search(pattern, my_string)
    if match:
        return match.group(1)
    return None


def check_hubs(my_map):
    hubs = [x for x in my_map.values() if isinstance(x, Hubs)]

    for i in range(len(hubs)):
        for j in range(i + 1, len(hubs)):
            hub_a = hubs[i]
            hub_b = hubs[j]
            if hub_a.x == hub_b.x and hub_a.y == hub_b.y:
                raise ValueError("Two Hubs can't have the same position")


def make_links(my_map):
    key_names = [x.name for x in my_map.values() if isinstance(x, Hubs)]
    for elt in my_map["hubs_links"]:
        temp = elt[0].split("-")
        if len(temp) != 2:
            raise ValueError(
                             "Links must respect format :'"
                             "connection: start-waypoint1'"
                             )
        if temp[0] not in key_names:
            raise ValueError(f"Links does not exists : {temp[0]}")
        if temp[1] not in key_names:
            raise ValueError(f"Links does not exists : {temp[1]}")
        my_map[temp[0]].links["links"].append(temp[1])
        my_map[temp[1]].links["links"].append(temp[0])

        my_map[temp[0]].links["max_links"] = elt[1]
    return my_map


def make_displayable(choosen_map: str):
    full_maps = {}
    try:
        maps = get_maps()
        if len(maps) == 0 or not maps:
            raise ValueError("At least one map must be available")
    except Exception as e:
        print(f"File error: {e}")
        return
    valid_maps = []
    for elt in maps:
        try:
            full_maps[elt] = map_valid(elt)
            valid_maps.append(elt)
        except Exception as e:
            raise ValueError(f"Error in file {elt}: {e}")

    # choosen_map = "03_ultimate_challenge.txt"  #to define after full_maps created
    if choosen_map not in valid_maps:
        raise ValueError(f"The choosen map is not valid : '{choosen_map}'")
    displayable_map = make_links(full_maps[choosen_map])

    return displayable_map


# to check metadata split the extract metadata then check max len < 3 then chexck every
# element if not of 3 possible type raise error