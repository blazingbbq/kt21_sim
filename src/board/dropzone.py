from typing import List, Tuple
import pygame
import utils.decorator
import utils.player_input
import utils.distance
import game.state

DROP_ZONE_OUTLINE_WIDTH = 3
DROP_ZONE_OUTLINE_COLOR = 0x204c8d
DROP_ZONE_BORDER_RADIUS = 1

DROP_ZONE_HOVER_COLOR_MOD = 0x222222
DROP_ZONE_HIGHLIGHT_COLOR = 0x00ff00

DROP_ZONE_BARRICADE_DEPLOY_ZONE_WIDTH = 2
DROP_ZONE_BARRICADE_DEPLOY_ZONE_COLOR = 0x204c8d + 0x333333


class DropZone:
    def __init__(self,
                 rects: List[pygame.Rect]):
        self.rects = rects
        self.visible = False
        self.barricade_deployment_visible = False
        self.color = DROP_ZONE_OUTLINE_COLOR
        self.highlight_color = None
        self.modify_color_on_hover = True

        # Generate barricade deployment zones
        from board.gameboard import GameBoard
        gameboard_rect: GameBoard = game.state.get().gameboard.rect

        self.barricade_deployment_zones: List[pygame.Rect] = []
        for rect in self.rects:
            # Calculate bounding box for barricade deployment. Clamp to gameboard edges
            left = max(
                rect.left - utils.distance.PENTAGON.to_screen_size(), gameboard_rect.left)
            top = max(
                rect.top - utils.distance.PENTAGON.to_screen_size(), gameboard_rect.top)
            width = min(rect.right + utils.distance.PENTAGON.to_screen_size(),
                        gameboard_rect.right) - left
            height = min(rect.bottom + utils.distance.PENTAGON.to_screen_size(),
                         gameboard_rect.bottom) - top

            self.barricade_deployment_zones.append(
                pygame.Rect(left, top, width, height)
            )

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def show_valid_barricade_deployment(self):
        self.show()
        self.barricade_deployment_visible = True

    def hide_valid_barricade_deployment(self):
        self.barricade_deployment_visible = False
        self.hide()

    def highlight(self):
        self.highlight_color = DROP_ZONE_HIGHLIGHT_COLOR

    def unhighlight(self):
        self.highlight_color = None

    def collide_point(self, point: Tuple[int, int]) -> bool:
        for rect in self.rects:
            if rect.collidepoint(point):
                return True

        return False

    def entirely_within(self, operative):
        from operatives import Operative
        operative: Operative = operative

        for rect in self.rects:
            if pygame.Rect(
                rect.left + operative.base_radius.to_screen_size(),
                rect.top + operative.base_radius.to_screen_size(),
                rect.width - operative.base_radius.to_screen_size() * 2,
                rect.height - operative.base_radius.to_screen_size() * 2,
            ).collidepoint(operative.rect.center):
                return True

        return False

    def redraw(self):
        if self.visible:
            for rect in self.rects:
                color_modifier = DROP_ZONE_HOVER_COLOR_MOD if rect.collidepoint(
                    utils.player_input.mouse_pos()) and self.modify_color_on_hover else 0
                color = self.color + color_modifier

                if self.highlight_color != None:
                    color = self.highlight_color

                pygame.draw.rect(
                    surface=pygame.display.get_surface(),
                    color=color,
                    rect=rect,
                    border_radius=DROP_ZONE_BORDER_RADIUS,
                    width=DROP_ZONE_OUTLINE_WIDTH,
                )

        if self.barricade_deployment_visible:
            for zone in self.barricade_deployment_zones:
                pygame.draw.rect(
                    surface=pygame.display.get_surface(),
                    color=DROP_ZONE_BARRICADE_DEPLOY_ZONE_COLOR,
                    rect=zone,
                    border_radius=DROP_ZONE_BORDER_RADIUS,
                    width=DROP_ZONE_BARRICADE_DEPLOY_ZONE_WIDTH,
                )
