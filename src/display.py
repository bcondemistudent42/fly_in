
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

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
