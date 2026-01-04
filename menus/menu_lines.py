from enum import Enum
from typing import Callable

from objects.cube_3d import Cube3d
from objects.cube_4d import Cube4d
from objects.octahedron_3d import Octahedron3d


class MenuLine:
    def __init__(self, name: str, pict: str,
                 dimensions: int = 3,
                 info: str = None,
                 obj: Callable = None):
        self.name = name
        self.pict = pict
        self.info = info
        self.dimensions = dimensions
        self.obj = obj


class MenusLines(Enum):
    cube_3d = MenuLine(name="cube 3d", pict="with_perspective.png", info="info_cube_3d.png", dimensions=4, obj=Cube3d)
    cube_4d = MenuLine(name="cube 4d", pict="cube_4d.png", info="info_cube_4d.png", dimensions=4, obj=Cube4d)
    octahedron_3d = MenuLine(name="octahedron 3d", pict="octahedron_3d.png", info="info_octahedron.png", dimensions=4, obj=Octahedron3d)
    e16cell_4d = MenuLine(name="16-cell 4d", pict="ico16cell.png", info="info_16cell.png", dimensions=4)
