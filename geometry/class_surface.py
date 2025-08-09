from geometry.class_point import Point


class Surface:
    def __init__(self, list_of_points: list[Point] = None):
        self.list_of_points = list_of_points if list_of_points is not None else []