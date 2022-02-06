from abc import ABC, abstractmethod
from board.killzones.default_killzone import DefaultKillzone
import game.state
import operatives.tyranids
from state import GameState
from state.team import *
from operatives import *
from game.console import print
import utils.dice

MISSION_CONSOLE_NAME_COLOR = 0xffffff
MISSION_CONSOLE_TEXT_COLOR = 0xffffff


class Mission(ABC):
    def __init__(self, name: str):
        self.gamestate: GameState = game.state.get()
        self.name = name
        self.console_name_color = MISSION_CONSOLE_NAME_COLOR

        # Print mission selection to console
        print(bold("Selected mission: ") + self.console_name)

        # Setup teams
        team1 = Team()
        team2 = Team()
        self.gamestate.add_teams(team1, team2)

        # Run through mission sequence
        self.determine_killzone()
        self.setup_objective_markers()

        self.determine_attacker()
        self.select_dropzones()

        self.assemble_killteams()
        self.setup_barricades()
        self.deploy_operatives()

    @property
    def console_name(self):
        return bold(with_color("[" + self.name.upper() + "]", color=self.console_name_color))

    def determine_killzone(self):
        # Determine killzone
        # TODO: Select from selection list
        DefaultKillzone(self.gamestate.gameboard)

    @abstractmethod
    def setup_objective_markers(self):
        # Setup objective markers
        pass

    def determine_attacker(self):
        # Roll off to decide who is the attacker and defender
        team1_roll = utils.dice.roll()
        team2_roll = utils.dice.roll()

        # Ensure both teams roll different result
        while team1_roll == team2_roll:
            team1_roll = utils.dice.roll()
            team2_roll = utils.dice.roll()

        # Prompt winning player to be attacker
        decider_idx = 0 if team1_roll > team2_roll else 1
        attacker_decision = utils.player_input.prompt_true_false(
            msg=f"{self.gamestate.teams[decider_idx].name}, do you want to be the attacker?")
        attacker_idx = decider_idx if attacker_decision == True else (
            decider_idx + 1) % 2

        self.gamestate.teams[attacker_idx].is_attacker = True
        self.gamestate.teams[attacker_idx].has_initiative = True

    def select_dropzones(self):
        # TODO: Defender selects dropzone
        pass

    def assemble_killteams(self):
        # TODO: Both players simultaneously select killteams from their rosters
        self.gamestate.teams[0].add_operatives(
            TrooperVeteran(),
            TrooperVeteran(),
            TrooperVeteran(),
        )
        self.gamestate.teams[1].add_operatives(
            operatives.tyranids.Hormagaunt(),
            operatives.tyranids.Termagant(),
            operatives.tyranids.Genestealer(),
        )

    def setup_barricades(self):
        # TODO: Starting with defender, players alternate setting up barricades
        # Must be within PENTAGON of player's dropzone and not on terrain feature

        pass

    def deploy_operatives(self):
        # Defender deploys all their operatives first
        for team in self.gamestate.teams:
            if team.is_attacker:
                continue
            while team.deploy_operative():
                pass

        # Then attacker does the same
        for team in self.gamestate.teams:
            while team.deploy_operative():
                pass
