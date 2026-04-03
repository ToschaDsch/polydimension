from abc import ABC, abstractmethod

import numpy as np
from PySide6.QtGui import QColor, QBrush, QPen

from variables.graphics import MyColors, Transparency


class GeometricObject(ABC):
    def __init__(self, color: QColor=None, width: int=None, style: str=None):
        self._color =color if color else QColor(*MyColors.default_point_color)
        self._width = width if width else 3
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self._width)
        self.get_pen_style(style)
        self._transparent: Transparency = Transparency.transparent
        self.name: str = ""

    @abstractmethod
    def draw_me(self):
        pass

    @property
    @abstractmethod
    def z(self) -> np.ndarray:
        pass

    @property
    def transparent(self) -> Transparency:
        return self._transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._transparent = value
        alpha: int = MyColors.transparency if value==Transparency.transparent else 256
        self._color.setAlpha(alpha)
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self.width)


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

    def get_pen_style(self, style: str):
        if style is None:
            return
        match style:
            case "dash_line":
                self.pen.setDashPattern([3, 5])
            case "dot_line":
                self.pen.dashOffset()
            case "dash_dot_line":
                self.pen.setDashPattern([1, 5])