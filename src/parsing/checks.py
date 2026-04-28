from src.parsing.regex_extract import (
    extract_max_link_capacity,
    extract_max_drones,
    extract_color,
    extract_zone,
)


def make_links(my_map):
    from src.parsing.parser import Hubs

    key_names = [x.name for x in my_map.values() if isinstance(x, Hubs)]
    for elt in my_map["hubs_links"]:
        temp = elt[0].split("-")
        if len(temp) != 2:
            raise ValueError(
                "Links must respect format :'connection: start-waypoint1'"
            )
        if temp[0] not in key_names:
            raise ValueError(f"Hub does not exists : {temp[0]}")
        if temp[1] not in key_names:
            raise ValueError(f"Hub does not exists : {temp[1]}")
        my_map[temp[0]].links["links"].append(temp[1])
        my_map[temp[1]].links["links"].append(temp[0])

        my_map[temp[0]].links["max_links"] = elt[1]
    return my_map


def check_simple_connection(connection_check):
    for elt in connection_check:
        for elt1 in connection_check:
            if len(elt1.split("-")) != 2:
                raise ValueError("Invalid Connection")
            left = elt1.split("-")[0]
            right = elt1.split("-")[1]
            total = f"{right}-{left}"
            if total == elt:
                raise ValueError("Can't declare twice same connection")


def last_check(start_name, end_name, my_hubs):
    from src.parsing.parser import Utils

    if start_name == "":
        raise ValueError(f"MISSING : {Utils.START_HUB}")
    if end_name == "":
        raise ValueError(f"MISSING : {Utils.END_HUB}")
    if len(my_hubs["hubs_links"]) == 0:
        raise ValueError("MISSING : links between hubs")
    if my_hubs["nb_drones"] < 0:
        raise ValueError("You must have at least 0 drones")


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
            extract_zone(elt) is None
            and extract_color(elt) is None
            and extract_max_drones(elt) is None
        ):
            raise ValueError(
                "What are u trying to do", "Wrong Metadata format"
            )


def check_hubs(my_map):
    from src.parsing.parser import Hubs

    hubs = [x for x in my_map.values() if isinstance(x, Hubs)]

    for i in range(len(hubs)):
        for j in range(i + 1, len(hubs)):
            hub_a = hubs[i]
            hub_b = hubs[j]
            if hub_a.x == hub_b.x and hub_a.y == hub_b.y:
                raise ValueError("Two Hubs can't have the same position")
