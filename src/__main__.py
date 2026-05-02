import clock

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame  # noqa: E402

from .drone import Drone
from .display import Displayer
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


# def get_maps():
# output = []
# for x in os.listdir("maps"):
# if x.endswith(".txt"):
# output.append(x)
# else:
# raise ValueError("Map must be a .txt")
# return output
#
# def test_maps():
# for choosen_map in get_maps():
# map = make_displayable(choosen_map)
# print(choosen_map)
# start, end = find_start_end(map)
# if (map[start].max_drone < map["nb_drones"] or
# map[end].max_drone < map["nb_drones"]):
# raise ValueError(
# f"START and END must have at least {map['nb_drones']} max drones")


def main():

    choosen_map = "03_ultimate_challenge.txt"
    my_map = make_displayable(choosen_map)
    start, end = find_start_end(my_map)
    if (
        my_map[start].max_drone < my_map["nb_drones"]
        or my_map[end].max_drone < my_map["nb_drones"]
    ):
        raise ValueError(
            f"START and END must have at least {my_map['nb_drones']} max drones"
        )
    display = Displayer(my_map)
    display.reset()
    display.draw_hubs()
    pygame.display.flip()
    
    test = pygame.time.Clock()

    my_drones = [Drone(my_map, start) for x in range(my_map["nb_drones"])]

    first_drone = my_drones[0]
    first_drone.next = (my_map["dist_gate1"].x, my_map["dist_gate1"].y)

    i = first_drone.coord[0]
    j = first_drone.coord[1]
    while (i < first_drone.next[0] or j < first_drone.next[1]):
            if i == first_drone.next[0]:
                 pass
            else:
                 i += 1
            if j == first_drone.next[1]:
                 pass
            else:
                 j += 1
            test.tick(60)
            display.display_drone(i, j)
            pygame.display.flip()
            # to make this pattern a function
            # and after the call of the function overide the past coord



    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

    # hubs = [x for x in map.values() if isinstance(x, Hubs)]
    # for i in range(len(hubs)):
    #     print()
    #     print(hubs[i].name)
    #     print(hubs[i].max_drone)


if __name__ == "__main__":
    # try:
        main()
    # except BaseException as e:
        # print(e)

# to see how to choose the map, with or without display
# within display maybe choose all available maps

# to put in place a system where can put any picutre instad of drone
# to do the djikstra algorythm and see when