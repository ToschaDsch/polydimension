from enum import Enum


class MenuLine:
    def __init__(self, name: str, pict: str, obj: str = None, info: str = None):
        self.name = name
        self.pict = pict
        self.info = info


class MenusLines(Enum):
    cube_3d = MenuLine(name="cube 3d", pict="with_perspective.png", info="info_cube_3d.png")
    cube_4d = MenuLine(name="cube 4d", pict="cube_4d.png", info="info_cube_4d.png")
    octahedron_3d = MenuLine(name="octahedron 3d", pict="octahedron_3d.png", info="info_octahedron.png")
    e16cell_4d = MenuLine(name="16-cell 4d", pict="ico16cell.png", info="info_16cell.png")
