import argparse
import os

from .display import Displayer
from .drone import Drone
from .parsing.parser import make_displayable
from .utils_main import find_start_end, test_maps

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import time

from dataclasses import dataclass

import pygame  # noqa: E402

from .dijkstra_solver import Connection


@dataclass
class WorkHub:
    hub_1: str
    hub_2: str
    max: int






# def assign_connections_cost()

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

    with open("visual_drones/" + drone):
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
    



    from .dijkstra_solver import convert_to_connection
    connections = convert_to_connection(my_map)

    start, end = find_start_end(my_map)
    #making links weight correctly for dijkstra to put in function later
    from .parsing.parsing_class import Hubs
    for elt in my_map.values():
        if isinstance(elt, Hubs):
            for weight_hub in connections:
                if weight_hub.hub_1 == elt.name:
                    elt.links["weight"].append((weight_hub.capacity, weight_hub.hub_2))
                elif weight_hub.hub_2 == elt.name:
                    elt.links["weight"].append((weight_hub.capacity, weight_hub.hub_1))


    from .dijkstra_solver import Graph
    g = Graph()
    g.dijkstra_init(my_map, start, end)
    ditances = g.shortest_distances()
    path = g.get_pathway(ditances)
    g.do_reservation(ditances)

    display = Displayer(my_map, drone)
    display.reset()
    display.draw_hubs()
    pygame.display.flip()

    my_drones = [
        Drone(my_map, start, display.drone_img)
        for x in range(my_map["nb_drones"])
    ]

    # Assign path to first drone
    my_drones[0].path = path
    
    # Set initial drone positions for movement
    for i, hub_name in enumerate(my_drones[0].path[:-1]):
        my_drones[0].next = (my_map[my_drones[0].path[i + 1]].x, my_map[my_drones[0].path[i + 1]].y)
    
    the_clock = pygame.time.Clock()
    
    running = True
    path_index = 0
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
        
        # Move drone through each hub on its path
        if path_index < len(my_drones[0].path) - 1:
            my_drones[0].next = (
                my_map[my_drones[0].path[path_index + 1]].x,
                my_map[my_drones[0].path[path_index + 1]].y
            )
            display.move_drones([my_drones[0]], the_clock)
            path_index += 1
        else:
            # Affichage final une fois arrivé
            display.display_drones([drone.coord for drone in my_drones])
            pygame.display.flip()


if __name__ == "__main__":
    # try:
        main()
    # except BaseException as e:
        # print(e)


# URGENT GERER LEX MAX LINKS PROPREMENT

# to handle when fisrt connection after start have max drone at 0
# to handle when max_links < max_capacity dron still goiing but should not