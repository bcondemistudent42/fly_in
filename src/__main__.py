import os

from .display import Displayer
from .parsing.parser import Hubs, make_displayable

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame  # noqa: E402


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

    choosen_map = "01_the_impossible_dream.txt"
    map = make_displayable(choosen_map)
    start, end = find_start_end(map)
    if (
        map[start].max_drone < map["nb_drones"]
        or map[end].max_drone < map["nb_drones"]
    ):
        raise ValueError(
            f"START and END must have at least {map['nb_drones']} max drones"
        )
    display = Displayer()

    x_max = max([x.x for x in map.values() if isinstance(x, Hubs)])
    x_min = min([x.x for x in map.values() if isinstance(x, Hubs)])
    y_min = min([x.y for x in map.values() if isinstance(x, Hubs)])

    size = 75
    padding = size / 2

    for elt in map.values():
        if isinstance(elt, Hubs):
            elt.x = elt.x - x_min
            elt.y = elt.y - y_min

    temp_x = max(1, x_max - x_min)
    scale = (display.width - (padding * 2) - 75) / temp_x

    walpaper = (105, 135, 138)
    display.screen.fill(walpaper)
    for key,elt in map.items():  # to do securty later if not map
        try:
            if isinstance(elt, Hubs):
                pygame.draw.rect(
                    display.screen,
                    elt.color,
                    ((elt.x * scale) + padding,
                     (elt.y * scale) + display.height / 4,
                     size, size ),
                )
                pygame.draw.line(
                    display.screen,
                    "black",
                    ((map[map[key].links["links"][0]].x * (scale) + (scale / 4) + padding),
                     (map[map[key].links["links"][0]].y * (scale) + (scale / 4) + display.height / 4) ),
                    ((elt.x * (scale) + (scale / 4) + padding), (elt.y * (scale) + (scale / 4) + display.height / 4)), 10)
        except ValueError:
            running = False
            raise ValueError(f"This is not a color: '{elt.color}'")
    pygame.display.flip()

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

# to make parsing tested by mbichet

# to handle correctly when hubs are outside the zone
