from ..phase import Phase
import utils


class InitiativePhase(Phase):
    def __init__(self):
        super().__init__(
            steps=[self.ready_operatives, self.determine_initiative])

    def ready_operatives(self, state):
        from state.gamestate import GameState
        gamestate: GameState = state

        for team in gamestate.teams:
            for operative in team.operatives:
                operative.ready = True

    def determine_initiative(self, state):
        from state.gamestate import GameState
        gamestate: GameState = state

        # NOTE: Initiative does not need to be rolled on first turn, it is determined in setup phase
        if gamestate.current_turn == 1:
            return

        rolls = []
        for _ in gamestate.teams:
            rolls.append(utils.dice.roll())

        # TODO: Display results to screen for players to see

        # Call hooks for abilities that let players reroll initiative rolls
        for i, team in enumerate(gamestate.teams):
            for on_initiative_roll in team.on_initiative_roll:
                rolls[i] = on_initiative_roll(rolls[i])
