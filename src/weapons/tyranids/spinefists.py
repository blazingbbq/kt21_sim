from ..weapon import SpecialRule, Weapon


class Spinefists(Weapon):
    def __init__(self):
        super().__init__(
            name="Spinefists",
            attacks=4,
            skill=3,
            damage=(2, 3),
            special_rules=[SpecialRule.RNG_6],
            critical_hit_rules=[],
        )
