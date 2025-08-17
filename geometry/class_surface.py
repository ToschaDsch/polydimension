import numpy

from geometry.class_line import Line
from geometry.class_point import Point


class Surface:
    def __init__(self, list_of_points: list[Point] = None):
        self._list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = []
        self.normal: list[float] = self.get_normal()

    @property
    def list_of_points(self) -> list[Point]:
        return self._list_of_points

    @list_of_points.setter
    def list_of_points(self, list_of_points: list[Point]):
        self._list_of_points = list_of_points
        self.normal = self.get_normal()

    def get_normal(self) -> list[float]:
        a: numpy.array() = self.list_of_lines[0].point_0.coord_0
