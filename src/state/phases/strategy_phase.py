from ..phase import Phase


class StrategyPhase(Phase):
    def __init__(self, gamestate):
        super().__init__(gamestate=gamestate,
                         steps=[self.generate_command_points,
                                self.play_strategic_ploys,
                                self.target_reveal])

    def generate_command_points(self):
        # Each player generates a CP
        for team in self.gamestate.teams:
            team.command_points += 1

    def play_strategic_ploys(self):
        self.alternate_action_starting_with_initiative_player(
            actions=[team.use_strategic_ploy for team in self.gamestate.teams])

    def target_reveal(self):
        self.alternate_action_starting_with_initiative_player(
            actions=[team.target_reveal_tac_ops for team in self.gamestate.teams])
