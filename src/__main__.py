
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame  # noqa: E402

import argparse
import questionary


from .drone import Drone
from .display import Displayer
from .parsing.parser import make_displayable
from .parsing.parsing_class import Hubs

from .dijkstra_solver import dijkstra_init


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
        if (current_map[start].max_drone < current_map["nb_drones"] or
            current_map[end].max_drone < current_map["nb_drones"]):
            raise ValueError(f"START and END must have at least {current_map['nb_drones']} max drones")

    choice = questionary.select(
        "Choose one map:",
        choices=maps,
        style=questionary.Style([
            ('qmark', 'fg:cyan bold'),
            ('pointer', 'fg:yellow bold'),
            ('highlighted', 'fg:yellow'),
            ('answer', 'fg:green bold')
            ])
    ).ask()

    return choice


def main():

    parser = argparse.ArgumentParser(
                    prog='Fly_In',)
    parser.add_argument("--drone",
                        default="drone.png",
                        required=False,
                        help="Change the representation of the drones with a picture")
    args = parser.parse_args()
    drone = args.drone

    choosen_map = test_maps()
    my_map = make_displayable(choosen_map)
    start, end = find_start_end(my_map)
    if (
        my_map[start].max_drone < my_map["nb_drones"]
        or my_map[end].max_drone < my_map["nb_drones"]
    ):
        raise ValueError(
            f"START and END must have at least {my_map['nb_drones']} max drones"
        )
    display = Displayer(my_map, drone)
    display.reset()
    display.draw_hubs()
    pygame.display.flip()

    the_clock = pygame.time.Clock()
    way = dijkstra_init(my_map, start, end)

    my_drones = [Drone(my_map, start) for x in range(my_map["nb_drones"])]

    first_drone = my_drones[0]
    for elt in way:
        display.move_drone(first_drone, the_clock)
        first_drone.next = (my_map[elt].x, my_map[elt].y)
    display.move_drone(first_drone, the_clock)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(e)

# to see how to choose the map, with or without display
# within display maybe choose all available maps