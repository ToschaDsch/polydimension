from PySide6.QtGui import QColor

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawLine
from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point
from variables.graphics import MyColors, Transparency
import numpy as np


class Line(GeometricObject):

    @property
    def z(self) -> np.ndarray:
        return 0.5 * (self.point_0.coord_n[2] + self.point_1.coord_n[2])

    @property
    def transparent(self) -> Transparency:
        return Transparency.full

    def draw_me(self):
        x1 = int(self.point_0.coord_n[0])
        y1 = int(self.point_0.coord_n[1])
        x2 = int(self.point_1.coord_n[0])
        y2 = int(self.point_1.coord_n[1])
        self.bus.publish(DrawLine(x1=x1, y1=y1, x2=x2, y2=y2,
                             brush=self.brush, pen=self.pen))

    def __init__(self, bus: EventBus, point_0: Point, point_1: Point, color: QColor=None,
                 width: int=1, name: str=None, style: str = None):
        super().__init__(color=color, width=width, style=style)
        self.bus = bus
        self.point_0 = point_0
        self.point_1 = point_1
        coord_0 = self.point_0.coord_0
        coord_1 = self.point_1.coord_0
        coord_center: np.ndarray[np.float64] = np.median([coord_0, coord_1], axis=0)
        self.center = Point(coordinates=coord_center, bus=self.bus)
        self.color: QColor = color if color else QColor(*MyColors.default_line_color)
        self.dimension: int = point_0.dimension
        self.name = name if name else ""
        self.list_of_points_change_coordinate = [point_0, point_1]

    def get_all_points(self) -> list[Point]:
        return self.list_of_points_change_coordinate

    def get_center(self) -> Point:
        return self.center

    def __str__(self):
        if self.name:
            name = f"name - {self.name}"
        else:
            name = ""
        return f"line ({str(self.point_0)}-{str(self.point_1)} {name})"

