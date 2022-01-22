from ..phase import Phase


class StrategyPhase(Phase):
    def __init__(self):
        super().__init__(steps=[self.generate_command_points,
                                self.play_strategic_ploys,
                                self.target_reveal])

    def generate_command_points(self, state):
        from state.gamestate import GameState
        gamestate: GameState = state

        # Each player generates a CP
        for team in gamestate.teams:
            team.command_points += 1

    def play_strategic_ploys(self, state):
        from state.gamestate import GameState
        gamestate: GameState = state

        # Starting with player that has initiative, alternate using strategic ploys
        idx = 0
        for i, team in enumerate(gamestate.teams):
            if team.has_initiative:
                idx = i
                break

        # Repeat until all players have passed in succession
        num_passes = 0
        while num_passes < len(gamestate.teams):
            num_passes = 0 if gamestate.teams[idx].use_strategic_ploy(
            ) else num_passes + 1
            idx = (idx + 1) % len(gamestate.teams)

    def target_reveal(self, state):
        from state.gamestate import GameState
        gamestate: GameState = state

        # Starting with player that has initiative, alternate revealing Tac Ops
        idx = 0
        for i, team in enumerate(gamestate.teams):
            if team.has_initiative:
                idx = i
                break

        # Repeat until all players have passed in succession
        num_passes = 0
        while num_passes < len(gamestate.teams):
            num_passes = 0 if gamestate.teams[idx].target_reveal_tac_ops(
            ) else num_passes + 1
            idx = (idx + 1) % len(gamestate.teams)
