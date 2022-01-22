from typing import Callable
from operatives import *


class Team:
    def __init__(self):
        # TODO: Include information about faction

        self.victory_points = 0
        self.command_points = 0
        self.has_initiative = False
        self.operatives: list[Operative] = []

        # Team based callbacks
        self.on_initiative_roll: list[Callable[[int], int]] = []

    def redraw(self):
        # TODO: Draw team information on each side of the screen

        for op in self.operatives:
            op.redraw()

    def attach_gamestate(self, gamestate):
        from state.gamestate import GameState
        self.gamestate: GameState = gamestate

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
        # TODO: Prompt player to select operative to activate
        return False

    # Register callbacks

    def register_on_initiative_roll(self, cb: Callable[[int], int]):
        """Register a callback that overrides an initiate roll.

        Args:
            cb (Callable[[int], int]): Callback must take in a dice result as input and return a result to replace the dice roll.
        """
        self.on_initiative_roll.append(cb)
