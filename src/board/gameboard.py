import pygame
from .terrain import *
import utils.distances
import utils.player_input

GAMEBOARD_WIDTH = 22
GAMEBOARD_HEIGHT = 30

# Padding around gameboard (in pixels)
GAMEBOARD_PADDING = 5

class GameBoard:
    border_color = (0, 0, 0)
    board_color = 0xb29175

    def __init__(self):
        self.terrain = Terrain()
        self.width = utils.distances.Distance.from_inch(GAMEBOARD_WIDTH)
        self.height = utils.distances.Distance.from_inch(GAMEBOARD_HEIGHT)

        screen = pygame.display.get_surface()
        self.rect = pygame.Rect(
            0, 0, self.width.to_screen_size(), self.height.to_screen_size())
        self.rect.center = screen.get_rect().center

    def attach_gamestate(self, gamestate):
        from state.gamestate import GameState
        self.gamestate: GameState = gamestate

    def deploy(self, op):
        from operatives import Operative
        operative: Operative = op

        def while_waiting():
            operative.show()
            operative.move(utils.player_input.mouse_pos())

            self.gamestate.redraw()
            self.gamestate.pump()

        click_loc = utils.player_input.wait_for_selection(
            validate=self.valid_deploy_loc, spin=while_waiting)

        operative.move(click_loc)

    def valid_deploy_loc(self, loc):
        # TODO: Check deployment validity using terrain and deployment zones
        return self.rect.collidepoint(loc)

    def redraw(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.board_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 1)

        # Redraw terrain
        self.terrain.redraw()
