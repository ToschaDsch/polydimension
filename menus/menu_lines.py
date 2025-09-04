from enum import Enum


class MenuLine:
    def __init__(self, name: str, pict: str, obj: str = None, dimensions: int = 3,  info: str = None):
        self.name = name
        self.pict = pict
        self.info = info
        self.dimensions = dimensions


class MenusLines(Enum):
    cube_3d = MenuLine(name="cube 3d", pict="with_perspective.png", info="info_cube_3d.png", dimensions=3)
    cube_4d = MenuLine(name="cube 4d", pict="cube_4d.png", info="info_cube_4d.png", dimensions=4)
    octahedron_3d = MenuLine(name="octahedron 3d", pict="octahedron_3d.png", info="info_octahedron.png", dimensions=3)
    e16cell_4d = MenuLine(name="16-cell 4d", pict="ico16cell.png", info="info_16cell.png", dimensions=4)
