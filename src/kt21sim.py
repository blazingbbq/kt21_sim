import pygame
from state.gamestate import *
from state.team import *
from operatives import *
from utils.distances import *
import game.screen


class KT21Sim:
    def start():
        # Init display
        game.screen.init("KT21 Sim")

        Distance.update_inch_size()

        # Init gamestate
        gamestate: GameState = GameState()

        # Populate teams
        team1 = Team()
        team2 = Team()
        gamestate.add_teams(team1, team2)

        team1.add_operatives(TrooperVeteran())
        team2.add_operatives(TrooperVeteran())

        # Run through game phases
        gamestate.redraw()
        gamestate.run()

        # Spin once game is over
        print("--- Sim complete ---")
        # TODO: Do something once game is over
        running = True
        while running:
            gamestate.redraw()
