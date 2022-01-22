from ..phase import Phase
import utils


class InitiativePhase(Phase):
    def __init__(self):
        super().__init__(
            steps=[self.ready_operatives,
                   self.determine_initiative])

    def ready_operatives(self):
        for team in self.gamestate.teams:
            for operative in team.operatives:
                operative.ready = True

    def determine_initiative(self):
        # NOTE: Initiative does not need to be rolled on first turn, it is determined in setup phase
        if self.gamestate.current_turn == 1:
            return

        rolls = []
        for _ in self.gamestate.teams:
            rolls.append(utils.dice.roll())

        # TODO: Display results to screen for players to see

        # Call hooks for abilities that let players reroll initiative rolls
        for i, team in enumerate(self.gamestate.teams):
            for on_initiative_roll in team.on_initiative_roll:
                rolls[i] = on_initiative_roll(rolls[i])

        # Find current player with initiate, reset initiative
        current_initiative = 0
        for i, team in enumerate(self.gamestate.teams):
            if team.has_initiative:
                current_initiative = i
                team.has_initiative = False
                break

        # Determine initiative
        highest_roll = max(rolls)
        top_rollers = [roll == highest_roll for roll in rolls]

        check_idx = current_initiative
        for _ in top_rollers:
            # Player with highest roll, following previous player with initiative is selected
            check_idx = (check_idx + 1) % len(top_rollers)
            if top_rollers[check_idx]:
                break
        self.gamestate.teams[check_idx].has_initiative = True
