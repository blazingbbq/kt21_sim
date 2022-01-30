from typing import Callable


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
        from operatives import Operative
        import action.condition
        self.name = name
        self.ap_cost = ap_cost
        self.valid_this_turn: Callable[[
            Action, Operative], bool] = action.condition.once_per_turn if valid_this_turn == None else valid_this_turn
        self.on_action: Callable[[Operative], bool] = on_action
        self.performed: bool = False

    def cost(self, free_actions=[]):
        if self.name in free_actions:
            return 0
        return self.ap_cost

    @property
    def description(self):
        return f"{self.name} {self.ap_cost}AP"
