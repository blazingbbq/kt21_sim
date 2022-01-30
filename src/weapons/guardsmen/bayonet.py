from ..weapon import Weapon


class Bayonet(Weapon):
    def __init__(self):
        super().__init__(
            name="Bayonet",
            attacks=3,
            skill=4,
            damage=(2, 3),
            special_rules=[],
            critical_hit_rules=[],
        )
