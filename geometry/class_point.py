import numpy as np
from PySide6.QtGui import QColor

from variables.graphics import MyColors


class Point:
    def __init__(self, coordinates = None):
        self._coordinates = coordinates if coordinates is not None else np.array([0.0, 0.0, 0.0, 0.0])
        self.coord_n = self._coordinates
        self._dimension = len(self._coordinates)
        self.color = QColor(*MyColors.default_point_color)

    def get_center(self):
        return self

    @property
    def coord_0(self) -> list[float]:
        return self._coordinates

    @coord_0.setter
    def coord_0(self, coordinates: list[float]):
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