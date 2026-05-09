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
        default="drone.png",
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
        raise ValueError(
            f"{txt} {my_map['nb_drones']} max drones"
        )
    display = Displayer(my_map, drone)
    display.reset()
    display.draw_hubs()
    pygame.display.flip()

    the_clock = pygame.time.Clock()
   

    my_drones = [Drone(my_map, start, display.drone_img) for x in range(my_map["nb_drones"])]

    reserved = set()
    for dj_drone in my_drones:
        reserved, dj_drone.path = dijkstra_init(my_map, start, end, reserved)
    step = max(reserved, key=lambda s: s[1])[1]
    for _ in range(step):
        i = 0
        for dp_drone in my_drones:
            dp_drone.path = sorted(dp_drone.path, key=lambda s: s[1])
            dp_drone.next = (my_map[dp_drone.path[i][0]].x, my_map[dp_drone.path[i][0]].y)
            display.move_drone(dp_drone.coord, dp_drone.next, the_clock)
            dp_drone.coord = dp_drone.next
            i += 1



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
