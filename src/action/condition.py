from board.objectives.objective import Objective
from typing import Callable, List
from .action import Action
import action.names
import utils.distance


def once_per_turn(action, op):
    from operatives import Operative
    operative: Operative = op
    return not action in operative.actions_taken


def did_not_perform(*action_names: List[str]):
    def _check_cond(_, operative):
        for action_name in [action.name for action in operative.actions_taken]:
            if action_name in action_names:
                return False
        return True
    return _check_cond


def not_concealed(_, op):
    from operatives import Operative
    operative: Operative = op

    return not operative.concealed


def within_engagement_range_of_enemy(_, op):
    from operatives import Operative
    operative: Operative = op

    return len(operative.enemies_within_engagement_range()) > 0


def not_within_engagement_range_of_enemy(ac, op):
    return not within_engagement_range_of_enemy(ac, op)


def has_ranged_weapon(_, op):
    from operatives import Operative
    operative: Operative = op

    return len(operative.datacard.ranged_weapon_profiles) > 0


def has_melee_weapon(_, op):
    from operatives import Operative
    operative: Operative = op

    return len(operative.datacard.melee_weapon_profiles) > 0


def able_to_pickup_objective(_, op):
    from operatives import Operative
    operative: Operative = op

    # Check that operative is not carrying another objective
    if operative.carrying_objective:
        return False

    # Find objective within range
    objective: Objective = operative.get_objective_in_capture_range()
    if objective == None:
        return False

    return objective.pickup_able


def not_able_to_pickup_objective(_, op):
    return not able_to_pickup_objective(_, op)


def carrying_objective(_, op):
    from operatives import Operative
    operative: Operative = op

    return operative.carrying_objective


def controls_objective(_, op):
    from operatives import Operative
    capturing_operative: Operative = op

    # Find objective within range
    objective: Objective = capturing_operative.get_objective_in_capture_range()
    if objective == None:
        return False

    friendly_apl = 0
    enemy_apl = 0
    for team in capturing_operative.team.gamestate.teams:
        for check_operative in team.operatives:
            if utils.distance.between(check_operative.rect.center, objective.rect.center) < check_operative.datacard.physical_profile.base / 2 + objective.capture_range:
                if team == capturing_operative.team:
                    friendly_apl += check_operative.datacard.physical_profile.action_point_limit
                else:
                    enemy_apl += check_operative.datacard.physical_profile.action_point_limit

    # Friendly operatives control an objective marker or token if the total APL
    # characteristic of friendly operatives within CIRCLE of the centre of it
    # is greater than that of enemy operatives.
    return friendly_apl > enemy_apl


# Action bundling


def all_of(*conds):
    from operatives import Operative
    conditions: List[Callable[[Action, Operative], bool]] = conds

    def _check_all_conds(action, operative):
        for cond in conditions:
            if not cond(action, operative):
                return False
        return True
    return _check_all_conds


def one_of(*conds):
    from operatives import Operative
    conditions: List[Callable[[Action, Operative], bool]] = conds

    def _check_all_conds(action, operative):
        for cond in conditions:
            if cond(action, operative):
                return True
        return False
    return _check_all_conds

# Operative Action Conditions


def can_move():
    return all_of(
        once_per_turn,
        did_not_perform(
            action.names.FALL_BACK,
            action.names.CHARGE),
        not_within_engagement_range_of_enemy,
    )


def can_shoot():
    return all_of(
        once_per_turn,
        one_of(
            not_concealed,
            # TODO: OR has a silent weapon
        ),
        not_within_engagement_range_of_enemy,
        has_ranged_weapon,
    )


def can_charge():
    return all_of(
        once_per_turn,
        did_not_perform(
            action.names.NORMAL_MOVE,
            action.names.DASH,
            action.names.FALL_BACK,
        ),
        not_concealed,
        not_within_engagement_range_of_enemy,
    )


def can_fight():
    return all_of(
        once_per_turn,
        within_engagement_range_of_enemy,
        has_melee_weapon,
    )


def can_dash():
    return all_of(
        once_per_turn,
        not_within_engagement_range_of_enemy,
        did_not_perform(
            action.names.CHARGE,
        ),
    )


def can_fall_back():
    return all_of(
        once_per_turn,
        within_engagement_range_of_enemy,
        did_not_perform(
            action.names.NORMAL_MOVE,
            action.names.CHARGE,
        ),
    )


def can_pick_up():
    return all_of(
        once_per_turn,
        not_within_engagement_range_of_enemy,
        controls_objective,
        able_to_pickup_objective,
    )


def can_drop_objective():
    return all_of(
        carrying_objective,
    )


def can_capture_objective():
    return all_of(
        once_per_turn,
        not_within_engagement_range_of_enemy,
        controls_objective,
        not_able_to_pickup_objective,
    )


def can_pass():
    # Can always pass
    return all_of()
