from abc import ABC, abstractmethod
from board.dropzone import DropZone
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

NUM_BARRICADES_PER_TEAM = 2


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

    @abstractmethod
    def generate_dropzones(self) -> List[DropZone]:
        return []

    def select_dropzones(self):
        # Defender selects dropzone
        defender_idx = 0
        while defender_idx < len(self.gamestate.teams) and self.gamestate.teams[defender_idx].is_attacker:
            defender_idx += 1

        self.gamestate.gameboard.dropzones = self.generate_dropzones()
        self.gamestate.gameboard.show_dropzones()
        print(
            f"{self.gamestate.teams[defender_idx].console_name} Select drop zone")

        # Wait for player to select a dropzone
        defender_dropzone_idx = None
        for click_loc in utils.player_input.wait_for_click():
            if click_loc != None:
                for i, dropzone in enumerate(self.gamestate.gameboard.dropzones):
                    if dropzone.collide_point(click_loc):
                        defender_dropzone_idx = i

            if defender_dropzone_idx != None:
                break
            self.gamestate.redraw()

        self.gamestate.gameboard.hide_dropzones()
        self.gamestate.redraw()

        self.gamestate.teams[defender_idx].dropzone = self.gamestate.gameboard.dropzones[defender_dropzone_idx]
        self.gamestate.teams[(defender_idx + 1) % len(self.gamestate.teams)].dropzone = self.gamestate.gameboard.dropzones[(
            defender_dropzone_idx + 1) % len(self.gamestate.gameboard.dropzones)]

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
        # Starting with defender
        defender_idx = 0
        while defender_idx < len(self.gamestate.teams) and self.gamestate.teams[defender_idx].is_attacker:
            defender_idx += 1

        num_teams = len(self.gamestate.teams)
        for i in range(0, num_teams * NUM_BARRICADES_PER_TEAM):
            deploying_team = self.gamestate.teams[(
                defender_idx + i) % num_teams]
            print(
                f"{deploying_team.console_name} Deploy barricade")

            self.gamestate.gameboard.deploy_barricade(deploying_team)

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
