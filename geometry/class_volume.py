from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface


class Volume:
    def __init__(self, list_of_points: list[Point] = None):
        self.list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = []
        self.list_of_surfaces: list[Surface] = []