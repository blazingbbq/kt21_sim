from abc import ABC
from typing import Callable


class Phase(ABC):
    def __init__(self, gamestate, steps: Callable[[], None]):
        from state.gamestate import GameState
        # GameState is attached when phases are added to the gamestate
        self.gamestate: GameState = gamestate
        self.steps = steps

    def run(self):
        """Run through the steps that make up this phase.
        """
        for step in self.steps:
            step()

    def alternate_action_starting_with_initiative_player(self, actions: Callable[[], bool]):
        # Starting with player that has initiative, alternate performing action
        idx = 0
        for i, team in enumerate(self.gamestate.teams):
            if team.has_initiative:
                idx = i
                break

        # Repeat until all players have passed in succession
        num_passes = 0
        while num_passes < len(self.gamestate.teams):
            num_passes = 0 if actions[idx]() else num_passes + 1
            idx = (idx + 1) % len(self.gamestate.teams)
