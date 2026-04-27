import os
import math

from src.display import Displayer
from src.parser import make_displayable, Hubs

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame  # noqa: E402


def main():

    choosen_map = "01_linear_path.txt"
    # choosen_map = "01_maze_nightmare.txt"
    map = make_displayable(choosen_map)
    display = Displayer()

    nbr_hubs = sum([1 for x in map.values() if isinstance(x, Hubs)])
    nb_columns = int(math.sqrt(nbr_hubs))
    nb_lines = nbr_hubs // nb_columns
    size = min(display.width // nb_columns, display.height // nb_lines)

    if size > 120:
        size = 120
    if size < 40:
        size = 40

    padding = size // 4
    for elt in map.values():  #to do securty later if not map
        try:
            if isinstance(elt, Hubs):
                pygame.draw.rect(
                    display.screen,
                    elt.color,
                    ((elt.x * ((size * 2)) + padding),
                     (elt.y * ((size * 2))) + (display.height // 2) - size,
                     size,
                     size)
                )
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
        # print()
        # print(hubs[i].name)
        # print(hubs[i].color)


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(e)



# to see how to choose the map, with or without display
# within display maybe choose all available maps

# to make parsing tested by mbichet

# to handle if there is more than two connections

# to handle correctly when hubs are outside the zone

# to handle if nbr drone bigger than the end max flow or start max flow

#negativ

# bug in that case hub:
# bug also with start_hub: start 0 0 color=green