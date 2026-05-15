import os

import questionary

from .parsing.parser import make_displayable
from .parsing.parsing_class import Hubs


def find_start_end(map):
    start = "".join(
        [
            x.name
            for x in map.values()
            if isinstance(x, Hubs) and x.start is True
        ]
    )
    end = "".join(
        [x.name for x in map.values() if isinstance(x, Hubs) and x.end is True]
    )
    return (start, end)


def get_maps():
    output = []
    for x in os.listdir("maps"):
        if x.endswith(".txt"):
            output.append(x)
        else:
            raise ValueError("Map must be a .txt")
    return output


def test_maps():
    maps = get_maps()

    for all_map in maps:
        current_map = make_displayable(all_map)
        start, end = find_start_end(current_map)
        if (
            current_map[start].max_drone < current_map["nb_drones"]
            or current_map[end].max_drone < current_map["nb_drones"]
        ):
            txt = "START and END must have at least"
            raise ValueError(
                f"{txt} {current_map['nb_drones']} max drones"
            )

    choice = questionary.select(
        "Choose one map:",
        choices=maps,
        style=questionary.Style(
            [
                ("qmark", "fg:cyan bold"),
                ("pointer", "fg:yellow bold"),
                ("highlighted", "fg:yellow"),
                ("answer", "fg:green bold"),
            ]
        ),
    ).ask()

    return choice


def setup_and_validate_map(drone_image: str = "bitcoin.png"):
    with open("visual_drones/" + drone_image):
        pass

    choosen_map = test_maps()
    my_map = make_displayable(choosen_map)

    start, end = find_start_end(my_map)
    if (
        my_map[start].max_drone < my_map["nb_drones"]
        or my_map[end].max_drone < my_map["nb_drones"]
    ):
        txt = "START and END must have at least "
        raise ValueError(f"{txt} {my_map['nb_drones']} max drones")
    
    return my_map, start, end


def assign_connections_weight(my_map, connections):
    for elt in my_map.values():
        if isinstance(elt, Hubs):
            for weight_hub in connections:
                if weight_hub.hub_1 == elt.name:
                    elt.links["weight"].append(
                        (weight_hub.capacity, weight_hub.hub_2)
                    )
                elif weight_hub.hub_2 == elt.name:
                    elt.links["weight"].append(
                        (weight_hub.capacity, weight_hub.hub_1)
                    )
