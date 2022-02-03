import pygame
from board.objectives.objective import Objective

from board.terrain.traits import TerrainTrait
from .terrain import *
import utils.distance
import utils.player_input

GAMEBOARD_WIDTH = 22
GAMEBOARD_HEIGHT = 30

# Padding around gameboard (in pixels)
GAMEBOARD_PADDING = 5
GAMEBOARD_BORDER_WIDTH = 1


class GameBoard:
    border_color = (0, 0, 0)
    board_color = 0xb29175

    def __init__(self, gamestate):
        from state.gamestate import GameState
        self.gamestate: GameState = gamestate

        # Terrain features
        self.terrain: Terrain = []
        self.objectives: Objective = []

        # Gameboard features
        self.width = utils.distance.from_inch(GAMEBOARD_WIDTH)
        self.height = utils.distance.from_inch(GAMEBOARD_HEIGHT)

        screen = pygame.display.get_surface()
        self.rect = pygame.Rect(
            0, 0, self.width.to_screen_size(), self.height.to_screen_size())
        self.rect.center = screen.get_rect().center

    def deploy(self, op):
        from operatives import Operative
        operative: Operative = op
        operative.show()

        # TODO: Show valid deployment zones

        for click_loc in utils.player_input.wait_for_click():
            if click_loc != None and self.valid_deploy_loc(click_loc):
                break
            operative.move_to(utils.player_input.mouse_pos())
            self.gamestate.redraw()

        operative.move_to(click_loc)
        self.gamestate.redraw()

    def valid_deploy_loc(self, loc):
        # TODO: Check deployment validity using terrain and deployment zones
        return self.rect.collidepoint(loc)

    def add_terrain(self, *terrain: Terrain):
        for t in terrain:
            self.terrain.append(t)

    def add_objectives(self, *objectives: Objective):
        for o in objectives:
            self.objectives.append(o)

    def features_with_trait(self, trait: TerrainTrait) -> List[Feature]:
        ret: List[Feature] = []
        for t in self.terrain:
            for feature in t.features:
                if trait in feature.traits:
                    ret.append(feature)
        return ret

    def show_objective_ranges(self):
        for objective in self.objectives:
            objective.show_capture_range()

    def hide_objective_ranges(self):
        for objective in self.objectives:
            objective.hide_capture_range()

    def redraw(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.board_color, self.rect)
        pygame.draw.rect(screen, self.border_color,
                         self.rect, GAMEBOARD_BORDER_WIDTH)

        # Redraw objectives
        for objective in self.objectives:
            objective.redraw()

        # Redraw terrain
        for terrain in self.terrain:
            terrain.redraw()
