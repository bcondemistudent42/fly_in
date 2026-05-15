import argparse
import os

from .dijkstra_solver import convert_to_connection
from .display import Displayer
from .drone import Drone
from .utils_main import setup_and_validate_map, assign_connections_weight

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

from dataclasses import dataclass

import pygame  # noqa: E402

from .dijkstra_solver import Connection, Graph


def main():

    parser = argparse.ArgumentParser(
        prog="Fly_In",
    )
    parser.add_argument(
        "--drone",
        default="bitcoin.png",
        required=False,
        help="Change the representation of the drones with a picture",
    )
    args = parser.parse_args()
    drone = args.drone

    my_map, start, end = setup_and_validate_map(drone)

    connections = convert_to_connection(my_map)

    assign_connections_weight(my_map, connections)

    drones = [Drone(my_map, start) for x in range(my_map["nb_drones"])]

    g = Graph(my_map)
    g.dijkstra_init(my_map, start, end)
    for elt in drones:
        distances = g.shortest_distances()
        g.do_reservation(distances)
        elt.path = g.get_pathway(distances)
    for elt in drones:
        print(elt.path)



if __name__ == "__main__":
    # try:
    main()
# except BaseException as e:
# print(e)


# URGENT GERER LEX MAX LINKS PROPREMENT

# to handle when fisrt connection after start have max drone at 0
# to handle when max_links < max_capacity dron still goiing but should not
