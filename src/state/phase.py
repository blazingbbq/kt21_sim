from abc import ABC
from typing import Callable


class Phase(ABC):
    def __init__(self, steps: Callable[[], None]):
        from state.gamestate import GameState
        # GameState is attached when phases are added to the gamestate
        self.gamestate: GameState = None
        self.steps = steps

    def attach_gamestate(self, gamestate):
        self.gamestate = gamestate

    def run(self):
        """Run through the steps that make up this phase.
        Each step is called with a reference to the gamestate
        """
        for step in self.steps:
            step(self.gamestate)
