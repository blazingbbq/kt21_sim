from typing import Callable
from operatives import *


class Team:
    def __init__(self):
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

    def add_operative(self, operative: Operative):
        self.operatives.append(operative)
        operative.team = self
        operative.on_added_to_team()

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

    # Register callbacks

    def register_on_initiative_roll(self, cb: Callable[[int], int]):
        """Register a callback that overrides an initiate roll.

        Args:
            cb (Callable[[int], int]): Callback must take in a dice result as input and return a result to replace the dice roll.
        """
        self.on_initiative_roll.append(cb)
