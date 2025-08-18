from typing import Any

import numpy
from numpy import ndarray, dtype, float64

from geometry.class_line import Line
from geometry.class_point import Point


class Surface:
    def __init__(self, list_of_points: list[Point] = None):
        self._list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = []
        self.normal: ndarray[tuple[Any]] = self.get_normal()
        self.center = self.get_center()

    @property
    def list_of_points(self) -> list[Point]:
        return self._list_of_points

    @list_of_points.setter
    def list_of_points(self, list_of_points: list[Point]):
        self._list_of_points = list_of_points
        self.normal = self.get_normal()

    def get_normal(self) -> ndarray[tuple[Any, ...], dtype[float64]]:
        a = self.list_of_lines[0].point_0.coord_0 - self.list_of_lines[0].point_1.coord_0
        b = self.list_of_lines[1].point_0.coord_0 - self.list_of_lines[1].point_1.coord_0
        normal = numpy.cross(a, b)
        return normal/numpy.linalg.norm(normal)

    def get_center(self) -> ndarray[tuple[Any, ...], dtype[float64]]:
        return numpy.sum(self.list_of_points.coord_0)/len(self.list_of_points)
