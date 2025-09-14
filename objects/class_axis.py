import numpy as np
from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from objects.class_draw_interface import NDimensionalObject
from variables.graphics import default_palette


class Axis(NDimensionalObject):


    def make_lines(self):
        colors = [QColor(255, 0,0),
                  QColor(0,255,0),
                  QColor(0,0,255)]
        for i in range(0, len(self.my_points)-2, 2):
            print(i, i/2)
            axes_i = Line(point_0=self.my_points[i],
                            point_1=self.my_points[i+1],
                          color=colors[int(i/2)])
            self.my_lines.append(axes_i)


    def make_surfaces(self):
        pass

    def __init__(self, dimension: int):
        self.dimension = dimension
        self.k1: float = 1.2
        self.k2: float = 0.2
        super().__init__()
        self._solid = False
        self.name_of_the_object = "Axis"


    def make_points(self):
        list_of_the_points: list[Point] = []
        init_coordinate: np.ndarray = np.array([0.0]*self.dimension)
        for i in range(self.dimension):
            coord_i1 = init_coordinate.copy()
            coord_i1[i] = self.size*self.k1
            coord_i2 = init_coordinate.copy()
            coord_i2[i] = -self.size*self.k2
            list_of_the_points.append(Point(coordinates=coord_i1))
            list_of_the_points.append(Point(coordinates=coord_i2))
        self.my_points = list_of_the_points

    @property
    def solid(self):
        return False

    def make_volumes(self):
        pass


