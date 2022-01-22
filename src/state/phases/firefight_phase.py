from ..phase import Phase


class FirefightPhase(Phase):
    def __init__(self):
        super().__init__(steps=[self.perform_actions])

    def perform_actions(self):
        self.alternate_action_starting_with_initiative_player(
            actions=[team.activate_operative for team in self.gamestate.teams])
