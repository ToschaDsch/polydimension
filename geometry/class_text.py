from PySide6.QtGui import QColor

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawPointText

from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point
from variables.graphics import MyColors, Transparency


class TextDraw(GeometricObject):
    @property
    def transparent(self) -> Transparency:
        return Transparency.full

    def draw_me(self):
        coord_n = self.center.coord_n
        x_y = [int(-coord_n[0]),
               int(coord_n[1])]
        self.bus.publish(DrawPointText(x0_y0=x_y, text=self.text))

    def __init__(self, bus: EventBus, point_0: Point, text: str):
        super().__init__()
        self.bus=bus
        self.point_0 = point_0
        self.center = Point(coordinates=point_0.coord_0, bus=self.bus)
        self.color = QColor(*MyColors.default_line_color)
        self.text: str = text

    def __str__(self):
        return f"text {self.text} {str(self.point_0)}"

    def get_all_points(self) -> list[Point]:
        return [self.point_0]

    def get_center(self) -> Point:
        return self.center

    def get_color(self) -> QColor:
        return self.color
