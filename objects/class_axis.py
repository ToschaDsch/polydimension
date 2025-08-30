from PySide6.QtGui import QColor

from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point


class Axis(GeometricObject):
    def get_all_points(self) -> list[Point]:
        pass

    def get_center(self) -> Point:
        pass

    def get_color(self) -> QColor:
        pass