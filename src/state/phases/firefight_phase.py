from ..phase import Phase


class FirefightPhase(Phase):
    def __init__(self, gamestate):
        super().__init__(gamestate=gamestate,
                         steps=[self.perform_actions])

    def perform_actions(self):
        self.alternate_action_starting_with_initiative_player(
            actions=[team.activate_operative for team in self.gamestate.teams])
