from PySide6.QtGui import QColor
from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point
from variables.graphics import MyColors
import numpy as np


class Line(GeometricObject):
    def get_all_points(self) -> list[Point]:
        return self.list_of_points_change_coordinate

    def get_center(self) -> Point:
        return self.center


    def __init__(self, point_0: Point, point_1: Point, color: QColor=None, width: int=1, name: str=None):
        super().__init__(color=color, width=width)
        self.point_0 = point_0
        self.point_1 = point_1
        coord_0 = self.point_0.coord_0
        coord_1 = self.point_1.coord_0
        coord_center: np.ndarray = np.median([coord_0, coord_1], axis=0)
        self.center = Point(coordinates=coord_center)
        self.color: QColor = color if color else QColor(*MyColors.default_line_color)
        self.dimension: int = point_0.dimension
        self.name = name if name else ""
        self.list_of_points_change_coordinate = [point_0, point_1]

    def __str__(self):
        if self.name:
            name = f"name - {self.name}"
        else:
            name = ""
        return f"line ({str(self.point_0)}-{str(self.point_1)} {name})"

