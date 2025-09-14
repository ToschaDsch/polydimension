from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from objects.class_draw_interface import NDimensionalObject
import numpy as np

from variables.graphics import MyColors


class Line2dWeb(NDimensionalObject):
    def make_surfaces(self):
        pass

    def make_volumes(self):
        pass

    def __init__(self, a: int, n: int):
        self.a = a/n  # size of a cell
        self.n = n  # numbers of the cells
        self._list_of_points: list[list[Point]] = []    # 2d array to make lines
        default_color = QColor(*MyColors.web)
        super().__init__(color=default_color)
        print(self)

    def __str__(self):
        return (f"I am Line2dWeb \n"
                f"{self._list_of_points}")


    def make_points(self):
        x0 = -self.a*self.n/2
        for x in range(self.n+1):
            line_of_points: list[Point] = []
            for y in range(self.n+1):
                x_i = x0 + x*self.a
                y_i = x0 + y*self.a
                coordinate = [x_i, y_i]
                coordinate.extend([0 for _ in range(self.dimensions-2)])
                coordinate = np.array(coordinate)
                point_i = Point(coordinates=coordinate)
                line_of_points.append(point_i)
            self._list_of_points.append(line_of_points)
            self.my_points.extend(line_of_points)

    def make_lines(self):
        for i in range(self.n):
            for j in range(self.n):
                line_i = Line(
                    point_0 = self._list_of_points[i][j],
                    point_1 = self._list_of_points[i+1][j],
                    color=self.color_of_lines
                )
                self.my_lines.append(line_i)

        for i in range(self.n):
            for j in range(self.n):
                line_i = Line(
                    point_0=self._list_of_points[j][i],
                    point_1=self._list_of_points[j][i+1],
                    color=self.color_of_lines
                )
                self.my_lines.append(line_i)

    def get_geometric_objects(self) -> list[Line]:
        return self.my_lines

    @property
    def solid(self):
        return False