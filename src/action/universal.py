from .action import Action
import action.names
import action.condition

# Action callbacks
# TODO: Implement action callbacks


def perform_normal_move(self):
    return True


def perform_shoot(self):
    return True


def perform_charge(self):
    return True


def perform_fight(self):
    return True


def perform_dash(self):
    return True


def perform_fall_back(self):
    return True


def perform_pick_up(self):
    return True


def perform_pass(self):
    self.action_points = -1
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
