from geometry.class_line import Line
from geometry.class_point import Point
from objects.class_draw_interface import DrawInterface


class Web(DrawInterface):
    def __init__(self, a: int, n: int):
        super().__init__()
        self.a = a  #seze of a cell
        self.n = n  #numbers of the cells
        self._list_of_points: list[list[Point]] = []

    def make_points(self):
        x0 = -self.a*self.n/2
        for x in range(self.n):
            line_of_points: list[Point] = []
            for y in range(self.n):
                x = x0 + x*self.n/2
                y = x0 + y*self.n/2
                coordinate = [x, y]
                coordinate.extend([t for t in range(self.dimensions-2)])
                point_i = Point(coordinate)
                line_of_points.append(point_i)
            self._list_of_points.append(line_of_points)
            self.my_points.extend(line_of_points)

    def make_lines(self):
        for i in range(self.n-1):
            for j in range(self.n-1):
                self.my_lines.append(Line(
                    point_0 = self._list_of_points[i][j],
                    point_1 = self._list_of_points[i+1][j]
                )
                )
                self.my_lines.append(Line(
                    point_0=self._list_of_points[j][i],
                    point_1=self._list_of_points[j+1][i]
                )
                )

