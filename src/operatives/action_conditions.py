from typing import Callable, List
from .action import Action, ActionNames


class ActionConditions:
    ### Helpers

    def did_not_perform(*action_names: List[str]):
        def _check_cond(_, operative):
            for action_name in [action.name for action in operative.actions_taken]:
                if action_name in action_names:
                    return False
            return True
        return _check_cond

    def not_concealed(_, op):
        from .operative import Operative
        operative: Operative = op

        return not operative.concealed

    def within_engagement_range_of_enemy(_, op):
        from .operative import Operative
        operative: Operative = op

        return len(operative.enemies_within_engagement_range()) > 0

    def not_within_engagement_range_of_enemy(ac, op):
        return not ActionConditions.within_engagement_range_of_enemy(ac, op)

    def able_to_pickup_objective(_, op):
        # TODO: Check if within range of an objective marker
        # Find objectives within range of operative
        # Check that operative controls objects
        # Check that operative is not carrying another objective
        return False

    ### Action bundling

    def all_of(*conds):
        from .operative import Operative
        conditions: List[Callable[[Action, Operative], bool]] = conds

        def _check_all_conds(action, operative):
            for cond in conditions:
                if not cond(action, operative):
                    return False
            return True
        return _check_all_conds

    def one_of(*conds):
        from .operative import Operative
        conditions: List[Callable[[Action, Operative], bool]] = conds

        def _check_all_conds(action, operative):
            for cond in conditions:
                if cond(action, operative):
                    return True
            return False
        return _check_all_conds

    ### Operative Action Conditions

    def can_move():
        return ActionConditions.all_of(
            Action.once_per_turn,
            ActionConditions.did_not_perform(
                ActionNames.FALL_BACK,
                ActionNames.CHARGE),
            ActionConditions.not_within_engagement_range_of_enemy,
        )

    def can_shoot():
        return ActionConditions.all_of(
            Action.once_per_turn,
            ActionConditions.not_within_engagement_range_of_enemy,
            ActionConditions.one_of(
                ActionConditions.not_concealed,
                # TODO: OR has a silent weapon
            ),
            ActionConditions.not_within_engagement_range_of_enemy
        )

    def can_charge():
        return ActionConditions.all_of(
            Action.once_per_turn,
            ActionConditions.did_not_perform(
                ActionNames.NORMAL_MOVE,
                ActionNames.DASH,
                ActionNames.FALL_BACK,
            ),
            ActionConditions.not_concealed,
            ActionConditions.not_within_engagement_range_of_enemy,
        )

    def can_fight():
        return ActionConditions.all_of(
            Action.once_per_turn,
            ActionConditions.within_engagement_range_of_enemy,
        )

    def can_dash():
        return ActionConditions.all_of(
            Action.once_per_turn,
            ActionConditions.not_within_engagement_range_of_enemy,
            ActionConditions.did_not_perform(
                ActionNames.CHARGE,
            ),
        )

    def can_fall_back():
        return ActionConditions.all_of(
            Action.once_per_turn,
            ActionConditions.within_engagement_range_of_enemy,
            ActionConditions.did_not_perform(
                ActionNames.NORMAL_MOVE,
                ActionNames.CHARGE,
            ),
        )

    def can_pick_up():
        return ActionConditions.all_of(
            Action.once_per_turn,
            ActionConditions.not_within_engagement_range_of_enemy,
            ActionConditions.able_to_pickup_objective,
        )

    def can_pass():
        # Can always pass
        return ActionConditions.all_of()
