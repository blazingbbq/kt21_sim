from ..weapon import CritRule, SpecialRule, Weapon


class DoubleRendingClaws(Weapon):
    def __init__(self):
        super().__init__(
            name="Double Rending Claws",
            attacks=5,
            skill=3,
            damage=(4, 5),
            special_rules=[SpecialRule.RELENTLESS],
            critical_hit_rules=[CritRule.RENDING],
        )
