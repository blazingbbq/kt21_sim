from ..weapon import Weapon


class Lasgun(Weapon):
    def __init__(self):
        super().__init__(
            name="Lasgun",
            attacks=4,
            skill=4,
            damage=(2, 3),
            special_rules=[],
            critical_hit_rules=[],
        )
