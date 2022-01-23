from typing import Callable
from operatives import *
import utils.player_input
import game.ui


class Team:
    def __init__(self):
        # TODO: Include information about faction

        # GameState attached when the team is added to the gamestate
        from state.gamestate import GameState
        self.gamestate: GameState = None
        self.team_id: int = None

        self.victory_points = 0
        self.command_points = 0
        self.has_initiative = False
        self.operatives: list[Operative] = []

        # Team based callbacks
        self.on_initiative_roll: list[Callable[[int], int]] = []

    def create_ui(self):
        # TODO: What to do if there's more than 2 teams?
        self.side_panel = game.ui.layout.left_panel if self.team_id % 2 == 0 else game.ui.layout.right_panel

        # FIXME: Replace with faction name
        self.faction_name_label = game.ui.elements.UILabel(
            relative_rect=pygame.Rect(
                0, 0, -1, -1),  # NOTE: Width/height -1 => size to text
            text="Team {}".format(self.team_id),
            manager=game.ui.manager,
            container=self.side_panel)

    def update_ui(self):
        pass

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

    def activate_operative(self):
        """Prompt player to activate operative. Includes overwatch actions.

        Returns:
            [bool]: Return whether an operative was activated (excludes overwatch actions)
        """
        ready_operatives: list[Operative] = [
            op for op in self.operatives if op.ready]

        if len(ready_operatives) <= 0:
            # TODO: Check for overwatch

            # Nothing left to activate
            return False

        # Get operative selection
        # TODO: Show operative info on hover
        active_operative: Operative = utils.player_input.wait_for_sprite_selection(
            targets=ready_operatives, spin=self.gamestate.redraw)

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
