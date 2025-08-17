from geometry.class_point import Point


class Line:
    def __init__(self, point_0: Point, point_1: Point):
        self.point_0 = point_0
        self.point_1 = point_1

    def __str__(self):
        return f"line ({str(self.point_0)}-{str(self.point_1)})"

