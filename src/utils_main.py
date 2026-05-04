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
            raise ValueError(
                f"START and END must have at least {current_map['nb_drones']} max drones"
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
