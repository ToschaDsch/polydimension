from PySide6.QtGui import QColor

from geometry.class_geometric_object import GeometricObject
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_center_from_list_of_points
from variables.graphics import MyColors


class Volume(GeometricObject):
    def get_center(self) -> Point:
        return self.center

    def get_all_points(self) -> list[Point]:
        return self.list_of_points

    def get_color(self) -> QColor:
        return self.color

    def __init__(self, list_of_points: list[Point] = None):
        super().__init__()
        self.list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = []
        self.list_of_surfaces: list[Surface] = []
        self.color = QColor(*MyColors.default_volume_color)
        self.center: Point = get_center_from_list_of_points(list_of_points=self.list_of_points)

    @property
    def color(self) -> QColor:
        return self.color

    @color.setter
    def color(self, color: QColor):
        for surface in self.list_of_surfaces:
            surface.color = color