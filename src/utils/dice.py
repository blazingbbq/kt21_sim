import random
from typing import Union
import game.console


class Dice:
    def __init__(self, val: Union[int, None] = None):
        if val == None:
            self.value = random.randint(1, 6)
        else:
            self.value = val
        self.rerolled = False

    def can_reroll(self):
        return not self.rerolled

    def reroll(self):
        # Any dice can only be rerolled once
        if self.rerolled == True:
            return
        self.rerolled = True
        old_val = self.value
        self.value = random.randint(1, 6)

        game.console.debug(f"Rerolled from {old_val} -> {self.value}")

    def reroll_lt(self, val):
        if self.value < val:
            self.reroll()

    def reroll_lte(self, val):
        if self.value <= val:
            self.reroll()

    def reroll_gt(self, val):
        if self.value > val:
            self.reroll()

    def reroll_gte(self, val):
        if self.value >= val:
            self.reroll()

    def reroll_eq(self, val):
        if self.value == val:
            self.reroll()

    def __gt__(self, other):
        if isinstance(other, Dice):
            return self.value > other.value
        return self.value > other

    def __lt__(self, other):
        if isinstance(other, Dice):
            return self.value < other.value
        return self.value < other

    def __ge__(self, other):
        if isinstance(other, Dice):
            return self.value >= other.value
        return self.value >= other

    def __le__(self, other):
        if isinstance(other, Dice):
            return self.value <= other.value
        return self.value <= other

    def __eq__(self, other):
        if isinstance(other, Dice):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return not self == other

    def __str__(self) -> str:
        return f"{self.value}"


def roll():
    """Rolls a d6.

    Returns:
        [int]: The result of the dice roll
    """
    return Dice()
