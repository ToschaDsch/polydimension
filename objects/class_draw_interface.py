from abc import ABC

from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.class_volume import Volume


class DrawObject(ABC):
    def __init__(self):
        self.dimensions = 4
        self.my_points: list[Point] = []
        self.my_lines: list[Line] = []
        self.my_surfaces: list[Surface] = []
        self.my_volumes: list[Volume] = []
        self._solid: bool = True
        self.transparent: bool = True
        self.color_of_lines: QColor = QColor(0,0,0)

    def make_geometry(self):
        self.make_geometry()
        self.make_lines()
        self.make_surfaces()
        self.make_volumes()

    def make_points(self):
        pass
    def make_lines(self):
        pass
    def make_surfaces(self):
        pass
    def make_volumes(self):
        pass

    def get_the_objects(self):
        if self.solid:
            return self.my_volumes
        else:
            return self.my_lines

    def init_geometry(self) -> None:
        pass

    @property
    def solid(self)->bool:
        return self._solid

    @solid.setter
    def solid(self, solid: bool):
        self._solid = solid