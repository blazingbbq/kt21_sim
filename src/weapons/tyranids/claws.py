from ..weapon import Weapon


class Claws(Weapon):
    def __init__(self):
        super().__init__(
            name="Claws",
            attacks=3,
            skill=4,
            damage=(2, 3),
            special_rules=[],
            critical_hit_rules=[],
        )
