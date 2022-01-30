from .action import Action
import action.names
import action.condition
import utils.distance
import utils.player_input


def perform_normal_move(op):
    from operatives import Operative
    operative: Operative = op

    return operative.perform_move(
        distance=operative.movement_characteristic,
    )


def perform_shoot(op):
    from operatives import Operative
    operative: Operative = op

    return operative.perform_shoot()


def perform_charge(op):
    from operatives import Operative
    operative: Operative = op

    return operative.perform_move(
        distance=operative.movement_characteristic + utils.distance.CIRCLE,
        charging=True,
    )


def perform_fight(op):
    from operatives import Operative
    operative: Operative = op

    # TODO: Implement fight action
    return True


def perform_dash(op):
    from operatives import Operative
    operative: Operative = op

    return operative.perform_move(
        distance=utils.distance.SQUARE,
    )


def perform_fall_back(op):
    from operatives import Operative
    operative: Operative = op

    return operative.perform_move(
        distance=operative.movement_characteristic,
        falling_back=True,
    )


def perform_pick_up(op):
    from operatives import Operative
    operative: Operative = op

    # TODO: Implement pick_up action
    return True


def perform_pass(op):
    from operatives import Operative
    operative: Operative = op

    operative.action_points = -1
    return True


universal_actions = [
    Action(name=action.names.NORMAL_MOVE,
           ap_cost=1,
           on_action=perform_normal_move,
           valid_this_turn=action.condition.can_move()),
    Action(name=action.names.SHOOT,
           ap_cost=1,
           on_action=perform_shoot,
           valid_this_turn=action.condition.can_shoot()),
    Action(name=action.names.CHARGE,
           ap_cost=1,
           on_action=perform_charge,
           valid_this_turn=action.condition.can_charge()),
    Action(name=action.names.FIGHT,
           ap_cost=1,
           on_action=perform_fight,
           valid_this_turn=action.condition.can_fight()),
    Action(name=action.names.DASH,
           ap_cost=1,
           on_action=perform_dash,
           valid_this_turn=action.condition.can_dash()),
    Action(name=action.names.FALL_BACK,
           ap_cost=2,
           on_action=perform_fall_back,
           valid_this_turn=action.condition.can_fall_back()),
    Action(name=action.names.PICK_UP,
           ap_cost=1,
           on_action=perform_pick_up,
           valid_this_turn=action.condition.can_pick_up()),
]

pass_action = Action(name=action.names.PASS,
                     ap_cost=0,
                     on_action=perform_pass,
                     valid_this_turn=action.condition.can_pass())
