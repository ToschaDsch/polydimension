import numpy as np
from PySide6.QtGui import QColor, QPen, QBrush

from variables.graphics import MyColors


class Point:
    def __init__(self, coordinates: np.ndarray = None, color:QColor=None, width: int=6):
        self._coordinates: np.ndarray = coordinates if coordinates is not None else np.array([0.0, 0.0, 0.0, 0.0])
        self.coord_n: np.ndarray = self._coordinates
        self.coord_only_rotate: np.ndarray = self._coordinates
        self._dimension: int = len(self._coordinates)
        self._color = color if color else QColor(*MyColors.default_point_color)
        self._width = width
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self._width)

    @property
    def radius(self) -> int:
        return int(self._width)

    def get_center(self):
        return self

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self.width)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        self.pen: QPen = QPen(self.brush, self.width)

    @property
    def coord_0(self) -> np.ndarray:
        return self._coordinates

    @coord_0.setter
    def coord_0(self, coordinates:  np.ndarray):
        self._coordinates = coordinates

    @property
    def dimension(self) -> int:
        return self._dimension

    @dimension.setter
    def dimension(self, new_dimension: int):
        change_dimensions_of_the_point(point=self, new_dimension=new_dimension)
        self._dimension = new_dimension

    def get_color(self) -> QColor:
        return self.color

    def __str__(self):
        return f"point {self._coordinates}"

def change_dimensions_of_the_point(point: Point, new_dimension: int = 4) -> None:
    old_dimension = point.dimension
    if old_dimension > new_dimension:
        for i in range(old_dimension - new_dimension):
            point.coord_0.pop()
    if old_dimension < new_dimension:
        for i in range(new_dimension - old_dimension):
            point.coord_0.append(0)