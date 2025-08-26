from PySide6.QtGui import QColor
from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point
from variables.graphics import MyColors


class Line(GeometricObject):
    def get_all_points(self) -> list[Point]:
        return [self.point_0, self.point_1]

    def get_center(self) -> Point:
        return self.center

    def get_color(self) -> QColor:
        return self.color

    def __init__(self, point_0: Point, point_1: Point):
        self.point_0 = point_0
        self.point_1 = point_1
        self.center = Point(coordinates=(point_0.coord_0 + point_1.coord_0)*3)
        self.color = QColor(*MyColors.default_line_color)

    def __str__(self):
        return f"line ({str(self.point_0)}-{str(self.point_1)})"

