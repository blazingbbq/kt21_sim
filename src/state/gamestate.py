from .team import *
from board import *
from .phases import *
import kt21sim


class GameState:
    MAX_TURNS = 4

    def __init__(self):
        self.teams: Team = []
        self.gameboard: GameBoard = GameBoard()
        self.turn_phases: list[Phase] = [
            InitiativePhase(), StrategyPhase(), FirefightPhase()]
        self.max_turns = self.MAX_TURNS
        self.current_turn = 1

    def run(self):
        while self.current_turn <= self.max_turns:
            for phase in self.turn_phases:
                phase.run()

            self.current_turn += 1

    def redraw(self):
        self.gameboard.redraw()
        for t in self.teams:
            t.redraw()

    def add_team(self, team: Team):
        self.teams.append(team)

    def pump(self):
        """ Wrapper function for pumping the current simulation state.
            Can be used directly on a gamestate reference instead of using the global KT21Sim.
        """
        kt21sim.KT21Sim.pump()
