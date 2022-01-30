from typing import Callable, List
from .action import Action
import action.names


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
    # TODO: Check if within range of an objective marker
    # Find objectives within range of operative
    # Check that operative controls objects
    # Check that operative is not carrying another objective
    return False

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
        able_to_pickup_objective,
    )


def can_pass():
    # Can always pass
    return all_of()
