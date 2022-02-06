from ..weapon import SpecialRule, Weapon


class Devourer(Weapon):
    def __init__(self):
        super().__init__(
            name="Devourer",
            attacks=5,
            skill=4,
            damage=(3, 4),
            special_rules=[SpecialRule.CEASELESS],
            critical_hit_rules=[],
        )
