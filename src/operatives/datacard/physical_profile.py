from utils.distances import *

class PhysicalProfile:
    def __init__(self, movement: Distance, action_point_limit: int, group_activation: int, defence: int, save: int, wounds: int, base: Distance):
        """Init physical profile

        Args:
            movement (Distance): The speed at which the operative moves across the killzone, represented by a distance value.
            action_point_limit (int): The number of action points an operative generates when it is activated, which are used to perform actions.
            group_activation (int): Most operatives are activated individually, but some operatives must be activated in a group. This number states how many of these operatives are activated together.
            defence (int): How many attacks the operative can defend each time another operative attacks it with a ranged weapon.
            save (int): How likely the operative is to avert an attack each time another operative attacks it with a ranged weapon, represented by the result required when rolling a D6. Note that a lower result is a better characteristic.
            wounds (int): How many wounds an operative can lose before it is incapacitated.
            base (Distance): The unit's base size.
        """

        # TODO: movement should be measured as a MovementUnits object
        self.movement = movement
        self.action_point_limit = action_point_limit
        self.group_activation = group_activation
        self.defence = defence
        self.save = save
        self.wounds = wounds
        self.base = base
