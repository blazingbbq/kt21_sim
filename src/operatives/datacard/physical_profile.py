class PhysicalProfile:
    def __init__(self, movement: int, action_point_limit: int, group_activation: int, defence: int, save: int, wounds: int, base: int):
        # TODO: movement should be measured as a MovementUnits object
        self.movement = movement
        self.action_point_limit = action_point_limit
        self.group_activation = group_activation
        self.defence = defence
        self.save = save
        self.wounds = wounds
        self.base = base
