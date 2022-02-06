from board.killzones import *
from missions.loot_and_salvage import LootAndSalvage
from missions.mission import Mission
from state.gamestate import *
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
        gamestate.redraw()

        # Welcome messages
        escape_text = keyname("ESCAPE")
        return_text = keyname("RETURN")
        note_text = with_background("NOTE:", 0x0077bb)
        print(bold("Welcome to KT21SIM"))
        print(bold(note_text) + italic(
            f" For any action, press {escape_text} to cancel the action, and {return_text} to end the action early." + newline()))

        # TODO: Select mission from list
        mission: Mission = LootAndSalvage()

        # Run through game phases
        gamestate.redraw()
        gamestate.run()
        print(bold(with_color("*** Sim complete ***", color=0x00ff00)))

        # Spin once game is over
        running = True
        while running:
            gamestate.redraw()
