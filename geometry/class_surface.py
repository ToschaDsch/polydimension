
import numpy as np
from PySide6.QtCore import QPoint
from PySide6.QtGui import QColor, QBrush, QPen, QPolygon

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import DrawPolygon
from geometry.class_geometric_object import GeometricObject
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_source_of_light import SourceOfLight
from geometry.color_for_surface import give_me_return_color, calculate_normal
from geometry.geometry_functions import get_center_from_list_of_points
from variables.graphics import MyColors, Transparency


class Surface(GeometricObject):
    @property
    def z(self) -> np.ndarray:
        return self.center.coord_n[2]

    def draw_me(self):
        polygon = QPolygon([
            QPoint(int(p.coord_n[0]), int(p.coord_n[1]))
            for p in self.list_of_points
        ])
        self.bus.publish(DrawPolygon(
            brush=self.brush,
            polygon=polygon,
            pen=self.pen
        ))

    def get_center(self) -> Point:
        return self.center

    def get_all_points(self) -> list[Point]:
        return self.list_of_points_change_coordinate

    def get_color(self) -> QColor:
        return self.color

    def __init__(self, bus: EventBus, list_of_points: list[Point] = None, color: QColor = None, width: int = None,
                 source_of_light: SourceOfLight = None, init_center_of_the_volume: Point = None):
        color = color if color else QColor(*MyColors.default_surface_color)
        super().__init__(color=color, width=width)
        self.bus = bus
        self._transparent = Transparency.transparent
        self._list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = []
        self.make_lines()
        self.dimension: int = list_of_points[0].dimension
        self.center: Point = Point(coordinates=get_center_from_list_of_points(list_of_points=self._list_of_points), bus=self.bus)
        self.init_center_of_the_volume = init_center_of_the_volume if init_center_of_the_volume else Point(bus=self.bus)
        normal: np.ndarray = calculate_normal(points=self._list_of_points,
                                            vector_center=self.center.coord_0 - self.init_center_of_the_volume.coord_0)
        self._init_color = color
        self._source_of_light: np.ndarray = source_of_light if source_of_light else np.array(SourceOfLight.coordinate)
        coord_for_normal: np.ndarray[np.float64] = np.resize(normal, (len(self.center.coord_0),))
        self.normal: Point = Point(
            coordinates=coord_for_normal,bus=self.bus)  # if it more as 3d space
        self._update_color()

        # add normal line
        coord_for_normal: np.ndarray[np.float64] = self.center.coord_0 + 0.5*self.normal.coord_0
        point_1 = Point(coordinates=coord_for_normal,bus=self.bus)    #end of normal line

        self.normal_line = Line(point_0=self.center,
                                point_1=point_1, name="normal", width=2, style="dash_line",
                                color=QColor(*MyColors.normal_line_color), bus=self.bus)
        self.list_of_points_change_coordinate = self._list_of_points + [self.center, point_1, self.normal]

    def _update_color(self):
        return_color = give_me_return_color(center=self.center,
                                            base_color=self._init_color, lamp=self._source_of_light,
                                            normal=self.normal.coord_only_rotate)

        self._color = return_color.color
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self.width)

    @property
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, value: QColor):
        self._init_color = value
        self._update_transparency()
        self._update_color()

    def change_coordinate(self):
        self._update_color()

    def make_lines(self):
        for i in range(len(self._list_of_points)-1):
            self.list_of_lines.append(Line(point_0=self._list_of_points[i],
                                           point_1=self._list_of_points[i+1], color=self._color, bus=self.bus))
        self.list_of_lines.append(Line(point_0=self._list_of_points[0],
                                       point_1=self.list_of_points[-1], color=self.color, bus=self.bus)) # closing the path


    @property
    def list_of_points(self) -> list[Point]:
        return self._list_of_points

    @list_of_points.setter
    def list_of_points(self, list_of_points: list[Point]):
        self._list_of_points = list_of_points

    def __str__(self):
        if self.name:
            name = f"name - {self.name}"
        else:
            name = ""
        return f"surface ({str(self._list_of_points[0])}-{str(self._list_of_points[1])}-{str(self._list_of_points[2])} {name})"

    @property
    def transparent(self) -> Transparency:
        return self._transparent

    @transparent.setter
    def transparent(self, value: Transparency):
        self._transparent = value
        self._update_color()


    def _update_transparency(self):
        alpha: int = MyColors.transparency if self._transparent == Transparency.transparent else 255
        self._init_color.setAlpha(alpha)
        self._color.setAlpha(alpha)
        self.brush: QBrush = QBrush(self._color)
        self.pen: QPen = QPen(self.brush, self.width)