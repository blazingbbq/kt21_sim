import pygame
from .terrain import *
import utils.distances

GAMEBOARD_WIDTH = 22
GAMEBOARD_HEIGHT = 30


class GameBoard:
    border_color = (0, 0, 0)

    def __init__(self):
        self.terrain = Terrain()
        self.width = utils.distances.Distance.from_inch(GAMEBOARD_WIDTH)
        self.height = utils.distances.Distance.from_inch(GAMEBOARD_HEIGHT)

        screen = pygame.display.get_surface()
        self.rect = pygame.Rect(
            0, 0, self.width.to_screen_size(), self.height.to_screen_size())
        self.rect.center = screen.get_rect().center

    def redraw(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.border_color, self.rect, 1)

        # Redraw terrain
        self.terrain.redraw()
