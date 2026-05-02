import os

from .parsing.parsing_class import Hubs

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
        self.my_map = my_map
        self.size = 75
        self.padding = self.size / 2

        x_max = max([x.x for x in self.my_map.values() if isinstance(x, Hubs)])
        x_min = min([x.x for x in self.my_map.values() if isinstance(x, Hubs)])
        y_max = max([x.y for x in self.my_map.values() if isinstance(x, Hubs)])
        y_min = min([x.y for x in self.my_map.values() if isinstance(x, Hubs)])

        self.drone = pygame.transform.scale(
            pygame.image.load("yriffard.png").convert_alpha(), (75, 75)
        )

        self.math_utils(x_max, x_min, y_max, y_min)
        for elt in my_map.values():
            if isinstance(elt, Hubs):
                elt.x = int((elt.x - x_min) * (self.scale) + self.offset_x)
                elt.y = int((elt.y - y_min) * (self.scale) + self.offset_y)

        pygame.display.set_caption("Fly-in")

    def reset(self):
        self.screen.fill((105, 135, 138))

    def draw_lines(self, my_map, key, elt):
        for elt1 in my_map[key].links["links"]:
            pygame.draw.line(
                self.screen,
                "black",
                (
                    my_map[elt1].x + (self.size / 2),
                    my_map[elt1].y + (self.size / 2) ,
                ),
                (
                    (elt.x + (self.size / 2)),
                    (elt.y + (self.size / 2)),
                ),
                5,
            )

    def draw_one_hub(self, elt):
        pygame.draw.rect(
            self.screen,
            elt.color,
            (
                elt.x,
                elt.y,
                self.size,
                self.size,
            ),
        )

    def math_utils(self, x_max, x_min, y_max, y_min):

        temp_x = max(1, x_max - x_min)
        temp_y = max(1, y_max - y_min)
        scale_x = (self.width - (self.padding * 2) - self.size) / temp_x
        scale_y = (self.height - (self.padding * 2) - self.size) / temp_y
        scale = min(scale_x, scale_y)

        graph_width = (temp_x * scale) + self.size
        graph_height = (temp_y * scale) + self.size

        offset_x = (self.width - graph_width) / 2
        offset_y = (self.height - graph_height) / 2

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.scale = scale

    def draw_hubs(self):

        if self.my_map is None:
            raise ValueError("Map Error")

        for key, elt in self.my_map.items():
            try:
                if isinstance(elt, Hubs):
                    self.draw_one_hub(elt)
                    self.draw_lines(self.my_map, key, elt)
            except ValueError:
                raise ValueError(f"This is not a color: '{elt.color}'")

    def display_drone(self, my_x, my_y):
        self.reset()
        self.draw_hubs()
        self.screen.blit(self.drone, (my_x, my_y))
