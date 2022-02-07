import pygame
from board.dropzone import DropZone
from board.killzones.loot_and_salvage_killzone import LootAndSalvageKillzone
from .mission import Mission
from state import GameState
import game.state
from board.objectives import Objective
import utils.distance
import missions.names


class LootAndSalvage(Mission):
    def __init__(self):
        super().__init__(name=missions.names.LOOT_AND_SALVAGE)

        self.objectives_secured_this_turn = 0
        self.current_turn = 0

    def on_objective_capture(self, objective, operative):
        if game.state.get().current_turn != self.current_turn:
            self.current_turn = game.state.get().current_turn
            self.objectives_secured_this_turn = 0

        if self.objectives_secured_this_turn < 4:
            self.objectives_secured_this_turn += 1
            operative.team.score_victory_points(1)

    def determine_killzone(self):
        LootAndSalvageKillzone(self.gamestate.gameboard)

    def generate_dropzones(self):
        dropzone1 = DropZone(rects=[pygame.Rect(
            self.gamestate.gameboard.rect.left,
            self.gamestate.gameboard.rect.top,
            utils.distance.SQUARE.to_screen_size(),
            self.gamestate.gameboard.rect.height),
        ])
        dropzone2 = DropZone(rects=[pygame.Rect(
            self.gamestate.gameboard.rect.right - utils.distance.SQUARE.to_screen_size(),
            self.gamestate.gameboard.rect.top,
            utils.distance.SQUARE.to_screen_size(),
            self.gamestate.gameboard.rect.height),
        ])

        return [dropzone1, dropzone2]

    def setup_objective_markers(self):
        gamestate: GameState = game.state.get()
        gameboard_rect = gamestate.gameboard.rect

        # An operative can perform this action while within TRIANGLE of an
        # objective marker it controls that has not been looted during this
        # Turning Point. Until the start of the next Turning Point, that
        # objective marker is looted. Each objective marker can be looted a
        # maximum of three times during the battle.
        gamestate.gameboard.add_objectives(
            Objective(
                pos=(
                    gameboard_rect.centerx - utils.distance.CIRCLE.to_screen_size(),
                    gameboard_rect.top + utils.distance.SQUARE.to_screen_size()),
                once_per_turn=True,
                max_interactions=3,
            ),
            Objective(
                pos=(
                    gameboard_rect.centerx + utils.distance.CIRCLE.to_screen_size(),
                    gameboard_rect.centery - utils.distance.PENTAGON.to_screen_size()),
                once_per_turn=True,
                max_interactions=3,
            ),
            Objective(
                pos=(
                    gameboard_rect.right - utils.distance.PENTAGON.to_screen_size(),
                    gameboard_rect.centery),
                once_per_turn=True,
                max_interactions=3,
            ),
            Objective(
                pos=(
                    gameboard_rect.centerx - utils.distance.CIRCLE.to_screen_size(),
                    gameboard_rect.centery + utils.distance.PENTAGON.to_screen_size()),
                once_per_turn=True,
                max_interactions=3,
            ),
            Objective(
                pos=(
                    gameboard_rect.centerx + utils.distance.CIRCLE.to_screen_size(),
                    gameboard_rect.bottom - utils.distance.SQUARE.to_screen_size()),
                once_per_turn=True,
                max_interactions=3,
            ),
            Objective(
                pos=(
                    gameboard_rect.left + utils.distance.PENTAGON.to_screen_size(),
                    gameboard_rect.centery),
                once_per_turn=True,
                max_interactions=3,
            ),
        )

        for objective in gamestate.gameboard.objectives:
            objective.register_on_capture(self.on_objective_capture)
