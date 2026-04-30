import os

from .parsing.parser import Hubs

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame  # noqa: E402


class Displayer:
    def __init__(self, my_map) -> None:
        pygame.init()
        info = pygame.display.Info()

        width, height = 3 * (info.current_w / 4), 3 * (info.current_h / 4)
        self.screen = pygame.display.set_mode((width, height))

        self.width = width
        self.height = height

        x_min = min([x.x for x in my_map.values() if isinstance(x, Hubs)])
        y_min = min([x.y for x in my_map.values() if isinstance(x, Hubs)])

        self.drone = pygame.transform.scale(
            pygame.image.load("yriffard.png").convert_alpha(), (75, 75)
        )

        for elt in my_map.values():
            if isinstance(elt, Hubs):
                elt.x = elt.x - x_min
                elt.y = elt.y - y_min
        self.my_map = my_map

        pygame.display.set_caption("Fly-in")

    def reset(self):
        self.screen.fill((105, 135, 138))

    def draw_lines(self, my_map, key, scale, size, offset_x, offset_y, elt):
        for elt1 in my_map[key].links["links"]:
            pygame.draw.line(
                self.screen,
                "black",
                (
                    my_map[elt1].x * (scale) + (size / 2) + offset_x,
                    my_map[elt1].y * (scale) + (size / 2) + offset_y,
                ),
                (
                    (elt.x * (scale) + (size / 2) + offset_x),
                    (elt.y * (scale) + (size / 2) + offset_y),
                ),
                5,
            )

    def draw_one_hub(self, elt, scale, offset_x, offset_y, size):
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

    def math_utils(self, x_max, x_min, y_max, y_min, size, padding):
        temp_x = max(1, x_max - x_min)
        temp_y = max(1, y_max - y_min)
        scale_x = (self.width - (padding * 2) - 75) / temp_x
        scale_y = (self.height - (padding * 2) - 75) / temp_y
        scale = min(scale_x, scale_y)

        graph_width = (temp_x * scale) + size
        graph_height = (temp_y * scale) + size

        offset_x = (self.width - graph_width) / 2
        offset_y = (self.height - graph_height) / 2

        return (offset_x, offset_y, scale)

    def draw_hubs(self):

        x_max = max([x.x for x in self.my_map.values() if isinstance(x, Hubs)])
        x_min = min([x.x for x in self.my_map.values() if isinstance(x, Hubs)])
        y_max = max([x.y for x in self.my_map.values() if isinstance(x, Hubs)])
        y_min = min([x.y for x in self.my_map.values() if isinstance(x, Hubs)])

        size = 75
        padding = size / 2
        offset_x, offset_y, scale = self.math_utils(
            x_max, x_min, y_max, y_min, size, padding
        )

        if self.my_map is None:
            raise ValueError("Map Error")

        for key, elt in self.my_map.items():
            try:
                if isinstance(elt, Hubs):
                    self.draw_one_hub(elt, scale, offset_x, offset_y, size)
                    self.draw_lines(
                        self.my_map, key, scale, size, offset_x, offset_y, elt
                    )
            except ValueError:
                raise ValueError(f"This is not a color: '{elt.color}'")

    def display_drone(self, my_x, my_y):
        self.reset()
        self.draw_hubs()
        self.screen.blit(self.drone, (my_x, my_y))
