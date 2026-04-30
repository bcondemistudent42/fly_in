import os

from .parsing.parser import Hubs

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame  # noqa: E402


class Displayer:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        width, height = 3 * (info.current_w / 4), 3 * (info.current_h / 4)
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        pygame.display.set_caption("Fly-in")

    def to_screen(self, my_map):

        x_max = max([x.x for x in my_map.values() if isinstance(x, Hubs)])
        x_min = min([x.x for x in my_map.values() if isinstance(x, Hubs)])
        y_max = max([x.y for x in my_map.values() if isinstance(x, Hubs)])
        y_min = min([x.y for x in my_map.values() if isinstance(x, Hubs)])

        size = 75
        padding = size / 2

        for elt in my_map.values():
            if isinstance(elt, Hubs):
                elt.x = elt.x - x_min
                elt.y = elt.y - y_min

        temp_x = max(1, x_max - x_min)
        temp_y = max(1, y_max - y_min)
        scale_x = (self.width - (padding * 2) - 75) / temp_x
        scale_y = (self.height - (padding * 2) - 75) / temp_y
        scale = min(scale_x, scale_y)

        graph_width = (temp_x * scale) + size
        graph_height = (temp_y * scale) + size

        offset_x = (self.width - graph_width) / 2
        offset_y = (self.height - graph_height) / 2

        walpaper = (105, 135, 138)
        self.screen.fill(walpaper)
        if my_map is None:
            raise ValueError("Map Error")
        for key, elt in my_map.items():  # to do securty later if not my_map
            try:
                if isinstance(elt, Hubs):
                    pygame.draw.rect(
                        self.screen,
                        elt.color,
                        (
                            (elt.x * scale) + offset_x,
                            (elt.y * scale) + offset_y,
                            size,
                            size,
                        ),
                    )
                    for elt1 in my_map[key].links["links"]:
                        pygame.draw.line(
                            self.screen,
                            "black",
                            (
                                my_map[elt1].x * (scale)
                                + (size / 2)
                                + offset_x,
                                my_map[elt1].y * (scale)
                                + (size / 2)
                                + offset_y,
                            ),
                            (
                                (elt.x * (scale) + (size / 2) + offset_x),
                                (elt.y * (scale) + (size / 2) + offset_y),
                            ),
                            5,
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
