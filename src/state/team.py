from typing import Callable

from pygame import K_ESCAPE
from board.dropzone import DropZone
from operatives import *
import utils.player_input
import utils.collision
import game.ui
import action.condition

TEAM_NAME_CONSOLE_COLOR = 0x3f6ca3


class Team:
    ready_operative_highlight_color = 0x00ff00

    def __init__(self):
        # TODO: Include information about faction
        self.console_name_color = TEAM_NAME_CONSOLE_COLOR

        # GameState attached when the team is added to the gamestate
        from state.gamestate import GameState
        self.gamestate: GameState = None
        self.team_id: int = None
        self.dropzone: DropZone = None

        self.victory_points = 0
        self.command_points = 0
        self.has_initiative = False
        self.is_attacker = False
        self.operatives: list[Operative] = []
        self.incapacitated_operatives: list[Operative] = []
        self.total_operatives = 0

        # Team based callbacks
        self.on_initiative_roll: list[Callable[[int], int]] = []

    @property
    def console_name(self):
        return tag(self.name, color=self.console_name_color)

    def print(self, msg: str):
        print(self.console_name + " " + str(msg))

    def score_victory_points(self, num: int = 1):
        self.victory_points += num
        points = "point" if num == 1 else "points"
        self.print(
            f"Scored {num} victory {points} ({self.victory_points} total)")

    @property
    def name(self):
        # TODO: Use the faction's name
        return "Team {}".format(self.team_id)

    @property
    def remaining_operatives(self):
        return len(self.operatives)

    def create_ui(self):
        # TODO: What to do if there's more than 2 teams?
        self.side_panel = game.ui.layout.team1_panel if self.team_id % 2 == 0 else game.ui.layout.team2_panel

    def update_ui(self):
        text = ""

        # Show team info
        text += self.console_name + newline()
        text += f"VP: {self.victory_points}    CP: {self.command_points}    Units: {self.remaining_operatives}/{self.total_operatives}" + newline()

        # Display operative statuses
        if self.total_operatives > 0:
            text += bold("Operatives:") + newline()
            for operative in self.operatives:
                text += "- " + operative.oneline_description + newline()
            for operative in self.incapacitated_operatives:
                text += with_color("x " + operative.oneline_description,
                                   color=0xff0000) + newline()

        # Set panel text
        self.side_panel.set_text(text)

    def redraw(self):
        self.update_ui()
        for op in self.operatives:
            op.redraw()

    def attach_gamestate(self, gamestate, team_id: int):
        self.gamestate = gamestate
        self.team_id = team_id

        self.create_ui()

    def add_operatives(self, *operatives: Operative):
        for operative in operatives:
            self.operatives.append(operative)
            self.total_operatives += 1
            operative.team = self
            operative.on_added_to_team()

    def deploy_operative(self):
        undeployed_operatives: list[Operative] = [
            op for op in self.operatives if not op.deployed]

        if len(undeployed_operatives) <= 0:
            # Nothing left to deploy
            return False

        # TODO: Deploy operatives in player decided order
        op: Operative = undeployed_operatives.pop()
        self.print(f"Deploying {op.console_name}")
        self.gamestate.gameboard.deploy(op)
        op.on_deployed()

        return True

    def use_strategic_ploy(self):
        """Prompt player to use a strategic ploy

        Returns:
            [bool]: Returns whether a strategic ploy was used
        """
        # TODO: Prompt player to use strategic ploy
        return False

    def target_reveal_tac_ops(self):
        """Prompt player to reveal Tac Ops during Target Reveal step

        Returns:
            [bool]: Returns whether a Tac Ops was revealed
        """
        # TODO: Prompt player to reveal Tac Ops
        return False

    def perform_overwatch(self):
        enemy_ready_operatives = 0
        for team in self.gamestate.teams:
            if team == self:
                continue
            enemy_ready_operatives += sum(
                1 for op in team.operatives if op.ready)

        # Cannot overwatch if the enemy does not have any remaining ready operatives
        if enemy_ready_operatives <= 0:
            return False

        # Get overwatchable operatives
        overwatch_operatives: list[Operative] = [
            op for op in self.operatives if (not op.ready and
                                             not op.overwatched and
                                             op.order == Order.ENGAGE and
                                             action.condition.not_within_engagement_range_of_enemy(None, op) and
                                             action.condition.has_ranged_weapon(None, op))]
        if len(overwatch_operatives) <= 0:
            # Nothing left to overwatch
            return False

        # Prompt player to select operative to overwatch
        self.print("Select an operative to overwatch")

        # Get operative selection, highlight ready operatives
        for op in overwatch_operatives:
            op.highlight(self.ready_operative_highlight_color)

        active_operative = None
        for click_loc in utils.player_input.wait_for_click():
            if utils.player_input.key_pressed(K_ESCAPE):
                break
            if click_loc != None:
                active_operative = utils.collision.get_selected_sprite(
                    click_loc, overwatch_operatives)
                if active_operative != None:
                    break
            self.gamestate.redraw()

        [op.unhighlight() for op in overwatch_operatives]
        self.gamestate.redraw()

        # Overwatch operative
        if active_operative:
            active_operative.overwatch()

        return False

    def activate_operative(self):
        """Prompt player to activate operative. Includes overwatch actions.

        Returns:
            [bool]: Return whether an operative was activated (excludes overwatch actions)
        """
        ready_operatives: list[Operative] = [
            op for op in self.operatives if op.ready]

        if len(ready_operatives) <= 0:
            # Nothing left to activate, try to overwatch
            return self.perform_overwatch()

        # Get operative selection, highlight ready operatives
        for op in ready_operatives:
            op.highlight(self.ready_operative_highlight_color)

        for click_loc in utils.player_input.wait_for_click():
            if click_loc != None:
                active_operative = utils.collision.get_selected_sprite(
                    click_loc, ready_operatives)
                if active_operative != None:
                    break
            self.gamestate.redraw()

        [op.unhighlight() for op in ready_operatives]
        self.gamestate.redraw()

        # Activate operative
        active_operative.activate()
        return True

    # Register callbacks

    def register_on_initiative_roll(self, cb: Callable[[int], int]):
        """Register a callback that overrides an initiate roll.

        Args:
            cb (Callable[[int], int]): Callback must take in a dice result as input and return a result to replace the dice roll.
        """
        self.on_initiative_roll.append(cb)
