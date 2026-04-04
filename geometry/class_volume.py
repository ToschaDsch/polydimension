import numpy as np
from PySide6.QtGui import QColor

from frontend.event_bus.event_bus import EventBus
from geometry.class_geometric_object import GeometricObject
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_center_from_list_of_points
from variables.graphics import MyColors, Transparency


class Volume(GeometricObject):
    @property
    def z(self) -> np.ndarray:
        return self.center.coord_n[2]

    def draw_me(self):
        for surface in self.list_of_surfaces:
            surface.draw_me()

    @property
    def transparent(self) -> Transparency:
        return self._transparent





    def __init__(self, bus: EventBus, list_of_points: list[Point] = None,
                 list_of_lines: list[Line] = None,
                 list_of_surfaces: list[Surface] = None,
                 color: QColor = None):
        super().__init__()
        self.bus = bus
        self.list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = list_of_lines if list_of_lines is not None else []
        self.list_of_surfaces: list[Surface] = list_of_surfaces if list_of_surfaces is not None else []
        self.state = self.list_of_surfaces[0].list_of_points[0].state
        self._color = QColor(*MyColors.default_volume_color) if color is None else color
        points_for_center = self._get_list_of_points_for_center()
        self.center: Point = Point(coordinates=get_center_from_list_of_points(list_of_points=points_for_center),
                                   bus=self.bus, state=self.state)


    def _get_list_of_points_for_center(self) -> list[Point]:
        if self.list_of_points:
            return self.list_of_points.copy()
        list_of_points = []
        for surface in self.list_of_surfaces:
            list_of_points.extend(surface.list_of_points)
        return list_of_points

    @property
    def color(self) -> QColor:
        return self._color

    @color.setter
    def color(self, color: QColor):
        for surface in self.list_of_surfaces:
            surface.color = color