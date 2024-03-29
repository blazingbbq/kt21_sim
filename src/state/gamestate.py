from .team import *
from board import *
from .phases import *
import game.clock
import game.events
import game.screen
import game.ui

MAX_TURNS = 4


class GameState:

    def __init__(self):
        self.teams: Team = []
        self.gameboard: GameBoard = GameBoard(self)

        # Game phases
        self.turn_phases: list[Phase] = []
        self.setup_phase = SetupPhase(self)
        self.initiative_phase = InitiativePhase(self)
        self.strategy_phase = StrategyPhase(self)
        self.firefight_phase = FirefightPhase(self)
        self.add_phases(self.initiative_phase,
                        self.strategy_phase, self.firefight_phase)

        self.max_turns = MAX_TURNS
        self.current_turn = 1

        # TODO: Track Mission

    def run(self):
        self.setup_phase.run()
        while self.current_turn <= self.max_turns:
            for phase in self.turn_phases:
                phase.run()

            self.current_turn += 1

    def redraw(self):
        """Redraw the gamestate. Also pumps game events
        """
        # Update debounced key statuses and mouse state
        # NOTE: Update this before ticking the clock, otherwise the input window is too small
        utils.player_input.update_input_state()

        # Tick clock to prevent spinning too fast
        game.clock.tick(60)

        game.screen.wipe()
        self.gameboard.redraw()
        for t in self.teams:
            t.redraw()
        game.ui.redraw()
        game.screen.redraw()

        # Also pump game events
        game.events.pump()

    def add_teams(self, *teams: Team):
        for team in teams:
            team_id = len(self.teams)
            team.attach_gamestate(self, team_id)
            self.teams.append(team)

    def add_phases(self, *phases):
        for phase in phases:
            self.turn_phases.append(phase)
