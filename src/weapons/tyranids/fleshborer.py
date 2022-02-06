from ..weapon import SpecialRule, Weapon


class Fleshborer(Weapon):
    def __init__(self):
        super().__init__(
            name="Fleshborer",
            attacks=4,
            skill=4,
            damage=(3, 4),
            special_rules=[SpecialRule.RNG_6],
            critical_hit_rules=[],
        )
