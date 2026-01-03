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

    def __init__(self, list_of_points: list[Point] = None,
                 list_of_lines: list[Line] = None,
                 list_of_surfaces: list[Surface] = None,
                 color: QColor = None):
        super().__init__()
        self.list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = list_of_lines if list_of_lines is not None else []
        self.list_of_surfaces: list[Surface] = list_of_surfaces if list_of_surfaces is not None else []
        self.color = QColor(*MyColors.default_volume_color) if color is None else color
        points_for_center = self._get_list_of_points_for_center()
        self.center: Point = get_center_from_list_of_points(list_of_points=points_for_center)

    def _get_list_of_points_for_center(self) -> list[Point]:
        if self.list_of_points:
            return self.list_of_points.copy()
        list_of_points = []
        for surface in self.list_of_surfaces:
            list_of_points.extend(surface.list_of_points)
        return list_of_points

    @property
    def color(self) -> QColor:
        return self.color

    @color.setter
    def color(self, color: QColor):
        for surface in self.list_of_surfaces:
            surface.color = color