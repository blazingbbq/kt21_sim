import random


class Dice:
    def __init__(self):
        self.value = random.randint(1, 6)
        self.rerolled = False

    def reroll(self):
        if self.rerolled == True:
            return
        self.rerolled = True
        self.value = random.randint(1, 6)

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
