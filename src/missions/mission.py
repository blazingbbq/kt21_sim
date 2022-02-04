from abc import ABC, abstractmethod
from board.killzones.default_killzone import DefaultKillzone
import game.state
from state import GameState, gamestate
from state.team import *
from operatives import *


class Mission(ABC):
    def __init__(self):
        self.gamestate: GameState = game.state.get()

        # Setup teams
        team1 = Team()
        team2 = Team()
        self.gamestate.add_teams(team1, team2)

        self.determine_killzone()
        self.setup_objective_markers()

        self.determine_attacker()
        self.select_dropzones()

        self.assemble_killteams()
        self.setup_barricades()
        self.deploy_operatives()

    def determine_killzone(self):
        # Determine killzone

        # TODO: Select from selection list
        DefaultKillzone(self.gamestate.gameboard)

    @abstractmethod
    def setup_objective_markers(self):
        # Setup objective markers
        pass

    def determine_attacker(self):
        # TODO: roll off, winner decides who is attacker and defender
        self.gamestate.teams[0].is_attacker = True
        self.gamestate.teams[0].has_initiative = True

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
            KommandoBoy(),
            KommandoBoy(),
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
