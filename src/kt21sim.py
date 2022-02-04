from board.killzones import *
from state.gamestate import *
from state.team import *
from operatives import *
import game.screen
import game.state
from game.console import keyname, print, bold, italic, with_background, with_color

DEBUG = True


class KT21Sim:
    def start():
        # Init display and UI
        game.screen.init("KT21SIM")
        game.ui.init()
        game.console.preload_fonts()

        # Init gamestate
        gamestate: GameState = game.state.init()

        # Populate teams
        team1 = Team()
        team2 = Team()
        gamestate.add_teams(team1, team2)

        team1.add_operatives(
            TrooperVeteran(),
            TrooperVeteran(),
        )
        team2.add_operatives(
            KommandoBoy(),
        )

        # Setup killzone
        DefaultKillzone(gamestate.gameboard)

        # TODO: Mission should add objectives to the gameboard instead
        from board.objectives.objective import Objective
        gamestate.gameboard.add_objectives(
            Objective(pos=(gamestate.gameboard.rect.centerx,
                           gamestate.gameboard.rect.centery + 200),
                      pickup_able=True),
        )

        # Welcome messages
        escape_text = keyname("ESCAPE")
        return_text = keyname("RETURN")
        note_text = with_background("NOTE:", 0x0077bb)
        print(bold("Welcome to KT21SIM"))
        print(bold(note_text) + italic(
            f" For any action, press {escape_text} to cancel the action, and {return_text} to end the action early."))

        # Run through game phases
        gamestate.redraw()
        gamestate.run()
        print(bold(with_color("*** Sim complete ***", color=0x00ff00)))

        # Spin once game is over
        # TODO: Do something once game is over
        running = True
        while running:
            gamestate.redraw()
