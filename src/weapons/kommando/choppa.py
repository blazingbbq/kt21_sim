from ..weapon import Weapon


class Choppa(Weapon):
    def __init__(self):
        super().__init__(
            name="Choppa",
            attacks=4,
            skill=3,
            damage=(4, 5),
            special_rules=[],
            critical_hit_rules=[],
        )
