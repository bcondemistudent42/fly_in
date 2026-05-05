from .dijkstra_solver import dijkstra_init
from .display import Displayer
from .drone import Drone
from .parsing.parser import make_displayable
from .utils_main import find_start_end, test_maps

import os
import argparse

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame  # noqa: E402


def drone_path(my_map, display, drone, way, the_clock):
    for elt in way:
        display.move_drone(drone, the_clock)
        drone.next = (my_map[elt].x, my_map[elt].y)
        display.move_drone(drone, the_clock)

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
   

    my_drones = [Drone(my_map, start) for x in range(my_map["nb_drones"])]

    from  .dijkstra_solver import Dijkstra_Node
    work_hub = Dijkstra_Node(my_map[start].name, my_map[start].cost, my_map[start].max_drone, my_map[start].links["links"])
    work_hub.visited = True
    work_hub.relative_cost = 0
    work_hub.true_cost = 0
    reserved = {}
    reserved[work_hub.name] = []
    k = 0
    for drone in my_drones:
        k += 1
        reserved = dijkstra_init(my_map, start, end, work_hub, reserved) #do unpack technique later let it like this for now
        drone.path = reserved
        print(drone.path)
        print("______________________________________")


    



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


# to add security when no link to the end
