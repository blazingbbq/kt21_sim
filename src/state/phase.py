from abc import ABC
from typing import Callable


class Phase(ABC):
    def __init__(self, steps: Callable[[], None]):
        self.steps = steps

    def run(self):
        """Run through the steps that make up this phase.
        """
        for step in self.steps:
            step()
