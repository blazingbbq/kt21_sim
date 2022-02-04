from ..phase import Phase


class SetupPhase(Phase):
    def __init__(self, gamestate):
        super().__init__(gamestate=gamestate,
                         steps=[])

    def deployment(self):
        self.alternate_action_starting_with_initiative_player(
            actions=[team.deploy_operative for team in self.gamestate.teams])
