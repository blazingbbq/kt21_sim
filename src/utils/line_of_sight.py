from math import cos, radians, sin
from typing import List, Tuple
from board.terrain.traits import TerrainTrait
import game.state
from board.gameboard import GameBoard
import utils.distance


def _generate_base_check_points(target, num_check_points=20):
    from operatives import Operative
    target: Operative = target

    radius = target.datacard.physical_profile.base.to_screen_size() / 2
    center_x = target.rect.centerx
    center_y = target.rect.centery

    check_points: List[Tuple[int, int]] = []
    for theta in range(0, 360, 360 // num_check_points):
        check_points.append(
            (center_x + radius * sin(radians(theta)), center_y + radius * cos(radians(theta))))

    return check_points


def visible(source, target):
    from operatives import Operative
    source: Operative = source
    target: Operative = target
    gameboard: GameBoard = game.state.get().gameboard

    # Visible if can draw an unobstructed straight line from the unit's head
    # to any part of the target (not its base).
    # NOTE:
    # - We use the center of the source unit's base as its head
    # - Only Tall terrain can block visibility

    check_points: List[Tuple[int, int]] = _generate_base_check_points(target)

    # For each heavy terrain feature, check if it obscures check points
    for feature in gameboard.features_with_trait(TerrainTrait.TALL):
        for check_point in list(check_points):
            if feature.rect.clipline(source.rect.center, check_point):
                check_points.remove(check_point)

    # Visible if some of the checkpoints are still visible
    return len(check_points) > 0


def obscured(source, target):
    from operatives import Operative
    source: Operative = source
    target: Operative = target
    gameboard: GameBoard = game.state.get().gameboard

    source_check_points = _generate_base_check_points(
        source, num_check_points=8)
    target_check_points = _generate_base_check_points(
        target, num_check_points=8)

    for feature in gameboard.features_with_trait(TerrainTrait.OBSCURING):
        for scp in source_check_points:
            for tcp in target_check_points:
                cover_line = (scp, tcp)

                # Check if the cover line crosses the terrain feature
                clipped_line = feature.rect.clipline(cover_line)
                if clipped_line:
                    source_within_triangle = False
                    target_outside_circle = False
                    for p in clipped_line:
                        source_within_triangle = source_within_triangle or utils.distance.between(
                            p, source.rect.center) < utils.distance.TRIANGLE + source.base_radius
                        target_outside_circle = target_outside_circle or utils.distance.between(
                            p, target.rect.center) > utils.distance.CIRCLE + target.base_radius

                    # The intended target is more than CIRCLE from a point at
                    # which a Cover line crosses a terrain feature that is
                    # Obscuring (see Terrain Traits).
                    # However, if the active operative is within TRIANGLE of a
                    # point at which a Cover line crosses a terrain feature
                    # that is Obscuring, that part of the terrain feature is
                    # not treated as Obscuring.
                    if target_outside_circle and not source_within_triangle:
                        return True

    return False


def in_cover(source, target):
    from operatives import Operative
    source: Operative = source
    target: Operative = target
    gameboard: GameBoard = game.state.get().gameboard

    # If the intended target is within CIRCLE from the active operative,
    # they are cannot be considered in cover
    if utils.distance.between(source.rect.center, target.rect.center) <= utils.distance.CIRCLE + source.base_radius + target.base_radius:
        return False

    source_check_points = _generate_base_check_points(
        source, num_check_points=8)
    target_check_points = _generate_base_check_points(
        target, num_check_points=8)

    # TODO: Also check the second part of this rule:
    # - another operative’s base (unless that other operative is not itself in the active operative’s LoS)

    for feature in gameboard.features_with_trait(TerrainTrait.COVER):
        for scp in source_check_points:
            for tcp in target_check_points:
                cover_line = (scp, tcp)

                # Check if the cover line crosses the terrain feature
                clipped_line = feature.rect.clipline(cover_line)
                if clipped_line:
                    target_within_triangle = False
                    for p in clipped_line:
                        # The intended target is within TRIANGLE of a point at
                        # which a Cover line crosses a terrain feature that
                        # provides Cover(see Terrain Traits).
                        if utils.distance.between(p, target.rect.center) < utils.distance.TRIANGLE + target.base_radius:
                            return True

    return False
