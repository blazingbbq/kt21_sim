import pygame
from board.dropzone import DropZone
from board.objectives.objective import Objective
from board.terrain.pieces.barricade import Barricade

from board.terrain.traits import TerrainTrait
from utils.collision import circle_rect_collide
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
        self.dropzones: DropZone = []

        # Gameboard features
        self.width = utils.distance.from_inch(GAMEBOARD_WIDTH)
        self.height = utils.distance.from_inch(GAMEBOARD_HEIGHT)

        screen = pygame.display.get_surface()
        self.rect = pygame.Rect(
            0, 0, self.width.to_screen_size(), self.height.to_screen_size())
        self.rect.center = screen.get_rect().center

    def deploy_barricade(self, team):
        from state import Team
        team: Team = team

        barricade = Barricade(pos=utils.player_input.mouse_pos())
        self.add_terrain(barricade)

        # Show drop zone for reference
        team.dropzone.show_valid_barricade_deployment()
        team.dropzone.modify_color_on_hover = False

        for click_loc in utils.player_input.wait_for_click():
            # Listen for barricade rotation
            if utils.player_input.key_pressed(pygame.K_e) or \
                    utils.player_input.key_pressed(pygame.K_q) or \
                    utils.player_input.key_pressed(pygame.K_LEFT) or \
                    utils.player_input.key_pressed(pygame.K_RIGHT):
                barricade.rotate()

            # Move and validate deployment location
            barricade.move_to(utils.player_input.mouse_pos())
            valid_deployment = barricade.validate_deployment(team.dropzone)
            if click_loc != None and valid_deployment:
                break

            self.gamestate.redraw()

        # Cleanup
        barricade.unhighlight()
        team.dropzone.hide_valid_barricade_deployment()
        team.dropzone.modify_color_on_hover = True
        barricade.move_to(click_loc)
        self.gamestate.redraw()

    def deploy(self, op):
        from operatives import Operative
        operative: Operative = op
        operative.show()
        operative.show_datacard()
        dropzone: DropZone = operative.team.dropzone

        # Show valid deployment zones
        dropzone.show()
        dropzone.modify_color_on_hover = False

        for click_loc in utils.player_input.wait_for_click():
            operative.move_to(utils.player_input.mouse_pos())
            valid_deploy = self.valid_deploy_loc(operative, dropzone)
            if click_loc != None and valid_deploy:
                break

            if valid_deploy:
                dropzone.highlight()
            else:
                dropzone.unhighlight()
            self.gamestate.redraw()

        dropzone.modify_color_on_hover = True
        dropzone.unhighlight()
        dropzone.hide()
        operative.move_to(click_loc)
        self.gamestate.redraw()

    def valid_deploy_loc(self, operative, dropzone: DropZone):
        from operatives import Operative
        operative: Operative = operative

        # Check that operative is entirely within dropzone
        if not dropzone.entirely_within(operative=operative):
            return False

        # Check that operative does not overlap terrain
        for terrain in self.gamestate.gameboard.terrain:
            for feature in terrain.features:
                if circle_rect_collide(circle=operative.rect.center,
                                       radius=operative.base_radius,
                                       rect=feature.rect):
                    return False

        # Check that operative does not overlap friendly unit
        for op in operative.team.operatives:
            if op == operative:
                continue
            if utils.distance.between(op.rect.center, operative.rect.center) < op.base_radius + operative.base_radius:
                return False

        # All conditions hold, deployment is valid
        return True

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

    def show_terrain_outlines(self):
        for terrain in self.terrain:
            terrain.show_outlines()

    def hide_terrain_outlines(self):
        for terrain in self.terrain:
            terrain.hide_outlines()

    def show_dropzones(self):
        for dropzone in self.dropzones:
            dropzone.show()

    def hide_dropzones(self):
        for dropzone in self.dropzones:
            dropzone.hide()

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

        # Redraw dropzones
        for dropzone in self.dropzones:
            dropzone.redraw()
