from typing import Tuple
from board.terrain.terrain import Terrain, LShape
from board.terrain.traits import TerrainTrait
import utils.distance

PIPE_THICKNESS = utils.distance.INCH


class Pipe(Terrain):
    def __init__(self,
                 pos: Tuple[int, int],
                 horizontal_side_length: utils.distance.Distance,
                 vertical_side_length: utils.distance.Distance,
                 orientation: Tuple[int, int] = (1, 1),
                 thickness: utils.distance.Distance = PIPE_THICKNESS):
        super().__init__(pos, orientation=orientation)

        self.add_features(
            *LShape(parent=self,
                    thickness=thickness,
                    horizontal_side_length=horizontal_side_length,
                    vertical_side_length=vertical_side_length,
                    orientation=orientation,
                    traits=[TerrainTrait.LIGHT,
                            TerrainTrait.TRAVERSABLE])
        )
