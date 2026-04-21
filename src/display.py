import pygame


class Displayer:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        width, height = info.current_w - 200, info.current_h - 150
        self.screen = pygame.display.set_mode((width, height))
        self.width = width
        self.height = height
        pygame.display.set_caption("Fly-in Drone Simulation")
