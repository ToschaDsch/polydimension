import numpy as np
from PySide6.QtGui import QColor, QPen, QBrush

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawPoint
from variables.graphics import MyColors


class Point:
    def __init__(self, bus: EventBus, coordinates: np.ndarray[np.float64] = None, color:QColor=None, width: int=6):
        self._coordinates: np.ndarray[np.float64] = coordinates if coordinates is not None else np.array([0.0, 0.0, 0.0, 0.0], dtype=np.float64)
        self.coord_n: np.ndarray[np.float64] = self._coordinates
        self.coord_only_rotate: np.ndarray[np.float64] = self._coordinates
        self._dimension: int = len(self._coordinates)
        self._color = color if color else QColor(*MyColors.default_point_color)
        self._width = width
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self._width)
        self.bus: EventBus = bus

    def draw_me(self):
        x0_y0 = self.coord_n
        self.bus.publish(DrawPoint(x=int(x0_y0[0]), y=int(x0_y0[1]), radius=self._width,
                              brush=self.brush, pen=self.pen))

    @property
    def z(self) -> np.ndarray[np.float64]:
        return self.coord_n[2]

    @property
    def radius(self) -> int:
        return int(self._width)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: QColor):
        self._color = value
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self.width)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.pen: QPen = QPen(self.brush, self.width)

    @property
    def coord_0(self) -> np.ndarray[np.float64]:
        return self._coordinates

    @coord_0.setter
    def coord_0(self, coordinates:  np.ndarray[np.float64]):
        self._coordinates = coordinates

    @property
    def dimension(self) -> int:
        return self._dimension


    def get_color(self) -> QColor:
        return self.color

    def __str__(self):
        return f"point {self._coordinates}"