from state.gamestate import *
from state.team import *
from operatives import *
import game.screen
import utils.distance


class KT21Sim:
    def start():
        # Init display and UI
        game.screen.init("KT21 Sim")
        game.ui.init()

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
        print("--- Sim complete ---")

        # Spin once game is over
        # TODO: Do something once game is over
        running = True
        while running:
            gamestate.redraw()
