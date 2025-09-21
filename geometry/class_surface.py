from typing import Any

import numpy as np
from PySide6.QtGui import QColor

from geometry.class_geometric_object import GeometricObject
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.geometry_functions import get_center_from_list_of_points
from variables.graphics import MyColors


class Surface(GeometricObject):
    def get_center(self) -> Point:
        return self.center

    def get_all_points(self) -> list[Point]:
        return self._list_of_points

    def get_color(self) -> QColor:
        return self.color

    def __init__(self, list_of_points: list[Point] = None, color: QColor = None, width: int = None):
        color = color if color else QColor(*MyColors.default_surface_color)
        super().__init__(color=color, width=width)
        self._list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = []
        self.make_lines()
        self.dimension: int = list_of_points[0].dimension
        self.normal: np.ndarray[tuple[Any]] = self.get_normal()
        self.center = get_center_from_list_of_points(list_of_points=self._list_of_points)

    def make_lines(self):
        for i in range(len(self._list_of_points)-1):
            self.list_of_lines.append(Line(point_0=self._list_of_points[i],
                                           point_1=self._list_of_points[i+1], color=self._color))
        self.list_of_lines.append(Line(point_0=self._list_of_points[0],
                                       point_1=self.list_of_points[-1], color=self.color)) # closing the path

    @property
    def list_of_points(self) -> list[Point]:
        return self._list_of_points

    @list_of_points.setter
    def list_of_points(self, list_of_points: list[Point]):
        self._list_of_points = list_of_points
        self.normal = self.get_normal()

    def get_normal(self) -> np.ndarray | None:
        if len(self.list_of_lines) < 2:
            print("too few lines")
            return None
        a = self.list_of_lines[0].point_0.coord_0 - self.list_of_lines[0].point_1.coord_0
        b = self.list_of_lines[1].point_0.coord_0 - self.list_of_lines[1].point_1.coord_0
        a = np.resize(a, (3,))
        b = np.resize(b, (3,))
        normal = np.cross(a, b)
        return normal/np.linalg.norm(normal)


