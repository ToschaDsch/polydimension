from PySide6.QtGui import QColor
from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point
from variables.graphics import MyColors


class TextDraw(GeometricObject):
    def get_all_points(self) -> list[Point]:
        return [self.point_0]

    def get_center(self) -> Point:
        return self.center

    def get_color(self) -> QColor:
        return self.color

    def __init__(self, point_0: Point, text: str):
        self.point_0 = point_0
        self.center = Point(coordinates=point_0.coord_0)
        self.color = QColor(*MyColors.default_line_color)
        self.text: str = text

    def __str__(self):
        return f"text {self.text} {str(self.point_0)}"

