import os
from enum import StrEnum


class Utils(StrEnum):
    START_HUB = "start_hub"
    END_HUB = "end_hub"
    HUB = "hub"
    CONNECTION = "connection"
    # NB_DRONES = to do later


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
                 zone_type=ZoneType.NORMAL,
                 max_capacity=1
                #  color: str,
                 ):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.links = []
        self.start, self.end = check
        self.max_flow = int(max_capacity)
        if zone_type == ZoneType.NORMAL:
            self.cost = float(1)
        elif zone_type == ZoneType.BLOCKED:
            self.cost = float('inf')
        elif zone_type == ZoneType.RESTRICTED:
            self.cost = 2
        elif zone_type == ZoneType.PRIORITY:
            self.cost = float(0.9)
        else:
            raise ValueError(f"Wrong zone type: {zone_type} does not exist")

        # to add some chekc for zone wtype and colors and list of connections
        # to add colors, zone type by default and list of connections


def get_maps():
    output = []
    for x in os.listdir("maps"):
        if x.endswith(".txt"):
            output.append(x)
        else:
            raise ValueError("Map must be a .txt")
    return output


def map_valid(my_map):
    with open("maps/" + my_map) as f:
        my_hubs = {}
        start_name = ""
        end_name = ""
        my_hubs["hubs_links"] = []
        format_error = "Format Error: Must respect pattern 'nb_drones: int'"
        i = 0
        j = 1
        for line in f:
            if line.startswith("#") or len(line.strip()) == 0:
                pass
            elif ":" not in line:
                raise ValueError(format_error + f"Line: {j}")
            else:
                if i == 0 and "nb_drones" not in line:
                    raise ValueError(
                          f"First line must be 'nb_drones', Line: {j}"
                          )
                elif i == 0:
                    try:
                        temp = line.split(":")
                        int(temp[1])
                        if len(temp) != 2:
                            raise ValueError
                    except Exception:
                        raise ValueError(f"{format_error}, Line: {j}")
                    if temp[0] != "nb_drones":
                        raise ValueError(format_error + f"Line: {j}")
                    else:
                        my_hubs["nb_drones"] = int(temp[1])
                else:
                    key = line.split(":")
                    data = key[1].split()
                    if key[0] == Utils.START_HUB:
                        if start_name != "":
                            raise ValueError("Can't init twice start,"
                                             f"Line: {j}") #a voir pour les couleurs
                        start_name = data[0]
                        my_hubs[data[0]] = Hubs(
                                                data[0],
                                                data[1],
                                                data[2],
                                                (True, False)
                                                )
                    elif key[0] == Utils.END_HUB:
                        if end_name != "":
                            raise ValueError(
                                  f"Cannot init twice end_hub, Line: {j}"
                                  )
                        end_name = data[0]
                        my_hubs[data[0]] = Hubs(
                                                data[0], data[1], data[2],
                                                (False, True)
                                                )
                    elif key[0] == Utils.HUB:
                        my_hubs[data[0]] = Hubs(data[0],
                                                data[1],
                                                data[2],
                                                (False, False))
                    elif key[0] == Utils.CONNECTION:
                        my_hubs["hubs_links"].append(key[1].strip())
                    else:
                        raise ValueError(
                              f"Unknown Type, {format_error}, Line: {j}"
                              )
                i = 1
            j += 1
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
    return my_hubs


def make_links(my_map):
    key_names = [x.name for x in my_map.values() if isinstance(x, Hubs)]
    for elt in my_map["hubs_links"]:
        temp = elt.split("-")
        if len(temp) != 2:
            raise ValueError(
                             "Links must respect format :'"
                             "connection: start-waypoint1'"
                             )
        if temp[0] not in key_names:
            raise ValueError(f"Links does not exists : {temp[0]}")
        if temp[1] not in key_names:
            raise ValueError(f"Links does not exists : {temp[1]}")
        my_map[temp[0]].links.append(temp[1])
        my_map[temp[1]].links.append(temp[0])
    return my_map




# to do later the connections stuff to handle
    # for elt in my_hubs.values():
    #     try:
    #         print(elt.name)
    #     except Exception:
    #         if isinstance(elt, int):
    #             print(elt)
    #         else:
    #             print("=== lst :")
    #             for elt1 in elt:
    #                 print(elt1)
    #             print("end lst ===")
    #         pass


# to see how to choose the map, with or without display
# within display maybe choose all available maps


def main():
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
        full_maps[elt] = map_valid(elt)
        valid_maps.append(elt)
    choosen_map = "02_simple_fork.txt"  #to define after full_maps created
    if choosen_map not in valid_maps:
        raise ValueError("The choosen map is not valid")
    displayable_map = make_links(full_maps[choosen_map])
    for elt in displayable_map.values():
        if isinstance(elt, Hubs):
            print(elt.name, elt.links)
            print()

if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(e)
# to add try except for main at the end