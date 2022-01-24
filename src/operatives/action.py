from typing import Callable


class ActionNames:
    NORMAL_MOVE = "Normal Move"
    SHOOT = "Shoot"
    CHARGE = "Charge"
    FIGHT = "Fight"
    DASH = "Dash"
    FALL_BACK = "Fall Back"
    PICK_UP = "Pick Up"
    PASS = "Pass"


class Action:
    def __init__(self, name: str, ap_cost: int, on_action, valid_this_turn=None):
        """Initialize an Action objecft

        Args:
            name (str): The actions name.
            ap_cost (int): The action's Action Point cost
            on_action (Callable[[Operative], bool]): Perform an action on an operative. Returns whether the action was completed successfully.
            valid_this_turn (Callable[[Operative, str], bool]): Check the validity of this action.\
                Takes in this action and the operative attempting to perform the action as parameters.
                Defaults to once per turn.
        """
        from .operative import Operative
        self.name = name
        self.ap_cost = ap_cost
        self.valid_this_turn: Callable[[
            Action, Operative], bool] = Action.once_per_turn if valid_this_turn == None else valid_this_turn
        self.on_action: Callable[[Operative], bool] = on_action
        self.performed: bool = False

    def once_per_turn(action, op):
        from .operative import Operative
        operative: Operative = op
        return not action in operative.actions_taken

    def cost(self, free_actions=[]):
        if self.name in free_actions:
            return 0
        return self.ap_cost
