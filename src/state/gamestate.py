from .team import *
from board import *
from .phases import *
import kt21sim


class GameState:
    MAX_TURNS = 4

    def __init__(self):
        self.teams: Team = []
        self.gameboard: GameBoard = GameBoard()
        self.gameboard.attach_gamestate(self)

        # Game phases
        self.turn_phases: list[Phase] = []
        self.setup_phase = SetupPhase()
        self.setup_phase.attach_gamestate(self)
        self.initiative_phase = InitiativePhase()
        self.strategy_phase = StrategyPhase()
        self.firefight_phase = FirefightPhase()
        self.add_phases(self.initiative_phase,
                        self.strategy_phase, self.firefight_phase)

        self.max_turns = self.MAX_TURNS
        self.current_turn = 1

        # TODO: Track Mission

    def run(self):
        self.setup_phase.run()
        while self.current_turn <= self.max_turns:
            for phase in self.turn_phases:
                phase.run()

            self.current_turn += 1

    def redraw(self):
        kt21sim.KT21Sim.wipe()
        self.gameboard.redraw()
        for t in self.teams:
            t.redraw()
        pygame.display.flip()

    def add_teams(self, *teams: Team):
        for team in teams:
            team.attach_gamestate(self)
            self.teams.append(team)

    def add_phases(self, *phases):
        for phase in phases:
            phase.attach_gamestate(self)
            self.turn_phases.append(phase)

    def pump(self):
        """ Wrapper function for pumping the current simulation state.
            Can be used directly on a gamestate reference instead of using the global KT21Sim.
        """
        kt21sim.KT21Sim.pump()
