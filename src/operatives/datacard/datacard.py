import pygame
from typing import List

from game.console import bold, newline, with_background, with_color
from .physical_profile import *
from action import Action
from weapons import Weapon
import game.ui

DATACARD_BACKGROUND_COLOR = 0xdedee5
DATACARD_ORANGE = 0xc54c21
DATACARD_WHITE = 0xffffff
# Cannot be fully black otherwise pygame_gui fails to render it as a text color
DATACARD_BLACK = 0x010000
DATACARD_GREY_DARK = 0x7d7c7d
DATACARD_GREY_LIGHT_1 = 0xcfd2d3
DATACARD_GREY_LIGHT_2 = 0xb6b9ba


class Datacard:
    def __init__(self,
                 operative_type: str,
                 physical_profile: PhysicalProfile,
                 ranged_weapon_profiles: List[Weapon],
                 melee_weapon_profiles: List[Weapon],
                 # TODO: Add classes for these parameters
                 abilities,
                 unique_actions: List[Action],
                 keywords):
        self.operative_type = operative_type
        self.physical_profile = physical_profile
        self.ranged_weapon_profiles = ranged_weapon_profiles
        self.melee_weapon_profiles = melee_weapon_profiles
        self.abilities = abilities
        self.unique_actions = unique_actions
        self.keywords = keywords

        self.ui_element = game.ui.elements.UITextBox(html_text=self.datacard_text,
                                                     relative_rect=pygame.rect.Rect(
                                                         game.ui.layout.info_panel_flush_offset,
                                                         (game.ui.layout.info_panel.rect.width,
                                                          game.ui.layout.info_panel.rect.height)
                                                     ),
                                                     container=game.ui.layout.info_panel,
                                                     manager=game.ui.manager,
                                                     visible=False,
                                                     )
        # TODO: Set datacard's background color
        # FIXME: Gets overwritten by the ui theme
        self.ui_element.background_colour = DATACARD_BACKGROUND_COLOR

    @property
    def datacard_text(self):
        rendered_wounds: str = "{:<2}".format(
            str(self.physical_profile.wounds))
        rendered_base: str = "{:<2}".format(
            int(self.physical_profile.base.to_mm())
        )

        text = ""
        text += bold(" [" + self.operative_type.upper() + "]") + newline()
        text += _with_orange_bg(
            "    M   APL   GA   DF   SV   W   Base     ") + newline()
        text += _with_white_bg(f"    {int(self.physical_profile.movement)}    {self.physical_profile.action_point_limit}    {self.physical_profile.group_activation}    {self.physical_profile.defence}    {self.physical_profile.save}+   {rendered_wounds}  {rendered_base}mm     ") + newline()

        text += _with_grey_dark_bg(
            "  Name              A   BS  D     SR   !  ") + newline()

        with_current_bg = None
        for ranged_weapon in self.ranged_weapon_profiles + self.melee_weapon_profiles:
            with_current_bg = _with_grey_light_1_bg if with_current_bg != _with_grey_light_1_bg else _with_grey_light_2_bg

            rendered_name = "{:<16}".format(ranged_weapon.name)
            rendered_attacks = "{:<2}".format(ranged_weapon.attacks)
            text += with_current_bg(
                f"  {rendered_name}  {rendered_attacks}  {ranged_weapon.skill}+ {ranged_weapon.normal_damage}/{ranged_weapon.critical_damage}    -    -  ") + newline()

        text += _with_grey_dark_bg(
            "  Abilities                               ") + newline()
        if len(self.abilities) <= 0:
            text += _with_grey_light_1_bg(
                "  -                                       ") + newline()
        # TODO: Display ability names

        text += _with_grey_dark_bg(
            "  Unique Actions                          ") + newline()
        if len(self.unique_actions) <= 0:
            text += _with_grey_light_1_bg(
                "  -                                       ") + newline()
        # TODO: Display special rule names

        return text

    def show(self):
        game.ui.replace_info_panel(self.ui_element)


def _with_orange_bg(str: str):
    return bold(with_background(with_color(str, DATACARD_BLACK), DATACARD_ORANGE))


def _with_white_bg(str: str):
    return with_background(with_color(str, DATACARD_BLACK), DATACARD_WHITE)


def _with_grey_dark_bg(str: str):
    return bold(with_background(with_color(str, DATACARD_BLACK), DATACARD_GREY_DARK))


def _with_grey_light_1_bg(str: str):
    return with_background(with_color(str, DATACARD_BLACK), DATACARD_GREY_LIGHT_1)


def _with_grey_light_2_bg(str: str):
    return with_background(with_color(str, DATACARD_BLACK), DATACARD_GREY_LIGHT_2)
