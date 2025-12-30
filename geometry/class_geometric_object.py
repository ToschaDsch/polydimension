from abc import ABC, abstractmethod

from PySide6.QtGui import QColor, QBrush, QPen

from geometry.class_point import Point
from variables.graphics import MyColors, Transparency


class GeometricObject(ABC):
    def __init__(self, color: QColor=None, width: int=None):
        self._color =color if color else QColor(*MyColors.default_point_color)
        self._width = width if width else 3
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self._width)
        self._transparent: bool = True
        self.visible = True
        self.name: str = ""

    @property
    def transparent(self) -> bool:
        return self._transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._transparent = value
        alpha: int = MyColors.transparency if value==Transparency.transparent else 256
        self._color.setAlpha(alpha)
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self.width)


    @abstractmethod
    def get_all_points(self) -> list[Point]:
        pass

    @abstractmethod
    def get_center(self) -> Point:
        pass


    @property
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, value: QColor):
        self._color = value
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self.width)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.pen: QPen = QPen(self.brush, self.width)