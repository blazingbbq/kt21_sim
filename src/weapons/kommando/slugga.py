from ..weapon import SpecialRule, Weapon


class Slugga(Weapon):
    def __init__(self):
        super().__init__(
            name="Slugga",
            attacks=4,
            skill=4,
            damage=(3, 4),
            special_rules=[SpecialRule.RNG_6],
            critical_hit_rules=[],
        )
