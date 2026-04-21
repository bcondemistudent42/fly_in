import math
import pygame

from src.display import Displayer
from src.parser import make_displayable, Hubs





def main():

    map = make_displayable()
    display = Displayer()

    # drone_img: pygame.Surface = pygame.image.load("cube.png").convert_alpha()
    # new_size = (65, 65)
    # drone_img = pygame.transform.smoothscale(drone_img, new_size)
    # img_rect = drone_img.get_rect(center=(100, 100))
    # display.screen.blit(drone_img, img_rect)

    nbr_hubs = sum([1 for x in map.values() if isinstance(x, Hubs)])
    running = True
    nb_columns = int(math.sqrt(nbr_hubs))
    nb_lines = nbr_hubs // nb_columns
    size = min(display.width // nb_columns, display.height // nb_lines)
    if size > 100:
        size = 100
    if size < 40:
        size = 40
    padding = size // 4
    for elt in map.values():  #to do securty later if not map
        if isinstance(elt, Hubs):
            pygame.draw.rect(
                display.screen,
                (255, 0, 0),
                ((elt.x * (size + (padding))) + display.width // 2,
                 (elt.y * (size + (padding))) + display.height // 2,
                 size,
                 size)
            )
    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    # try:
    main()
    # except BaseException as e:
        # print(e)



# to see how to choose the map, with or without display
# within display maybe choose all available maps

# to make parsing tested by mbichet

# to do security if two hubs with same x,y or with same name