from .dijkstra_solver import dijkstra_init
from .display import Displayer
from .drone import Drone
from .parsing.parser import make_displayable
from .utils_main import find_start_end, test_maps

import os
import argparse

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame  # noqa: E402


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
    display = Displayer(my_map, drone)
    display.reset()
    display.draw_hubs()
    pygame.display.flip()

    the_clock = pygame.time.Clock()

    my_drones = [
        Drone(my_map, start, display.drone_img)
        for x in range(my_map["nb_drones"])
    ]

    reserved = []
    for dj_drone in my_drones:
        reserved, dj_drone.path = dijkstra_init(my_map, start, end, reserved)

    all_steps = []
    for drone in my_drones:
        for hub_name, hub_step in drone.path:
            all_steps.append(hub_step)
    step = max(all_steps)

    display.reset() # to do a function display to clean main
    display.draw_hubs()
    drones_initial_pos = [drone.coord for drone in my_drones]
    display.display_drones(drones_initial_pos)
    pygame.display.flip()
    the_clock.tick(60)

    for current_step in range(1, step + 1):
        for drone in my_drones:
            drone.path = sorted(drone.path, key=lambda s: s[1])
            found = False
            for hub_name, hub_step in drone.path:
                if hub_step == current_step:
                    drone.next = (my_map[hub_name].x, my_map[hub_name].y)
                    found = True
                    break
            if not found:
                drone.next = drone.coord

        display.move_drones(my_drones, the_clock)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False


if __name__ == "__main__":
    # try:
    main()

# except BaseException as e:
# print(e)


# URGENT GERER LEX MAX LINKS PROPREMENT

# to handle when fisrt connection after start have max drone at 0
# to handle when max_links < max_capacity dron still goiing but should not