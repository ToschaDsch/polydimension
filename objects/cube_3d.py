import functools
import itertools
import math

import numpy
from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from objects.class_draw_interface import NDimensionalObject
from variables import graphics
from variables.graphics import MyColors


class Cube3d(NDimensionalObject):

    def __init__(self):
        self.list_of_point = [[0, 1, 5, 4],
                              [0, 2, 6, 4],
                              [0, 1, 3, 2],
                              [2, 6, 7, 3],
                              [4, 6, 7, 5],
                              [1, 3, 7, 5]]
        super().__init__()
        self.name_of_the_object = "Cube 3d"


    def make_points(self):
        a = self.size
        initial_set = [a, -a]
        init_list_of_coordinates = numpy.array([numpy.array(x) for x in itertools.product(initial_set,repeat=3)])
        for coordinate in init_list_of_coordinates:
            new_coordinate = numpy.append(coordinate, numpy.array([0]))
            self.my_points.append(Point(coordinates=new_coordinate))


    def make_lines(self):
        for i in range(len(self.my_points)):
            for j in range(i+1,len(self.my_points)):
                point_i = self.my_points[i]
                point_j = self.my_points[j]
                delta_point = point_i.coord_0 - point_j.coord_0
                if sum(delta_point) == 2*self.size:
                    set_delta = set(delta_point)
                    if set_delta in ({0, 2*self.size}, {0, -2*self.size}):
                        self.my_lines.append(Line(point_i, point_j))

        print(self.my_lines)

    def make_surfaces(self):
        print(*[str(n) + " " + str(point) + "\n" for n, point in enumerate(self.my_points)])

        for numbers_of_points in self.list_of_point:
            points_for_surface_i = [self.my_points[i] for i in numbers_of_points]
            self.my_surfaces.append(Surface(list_of_points=points_for_surface_i, color=self.surface_color))

        for surface in self.my_surfaces: #check it
            is_it_a_surface(surface)

    def make_volumes(self):
        pass

    def change_color(self, color_is_out: bool=True):
        if color_is_out:
            color =  [self.surface_color]*len(self.my_points)
        else:
            color = [QColor(*x) for x in graphics.default_palette]
        for surface, color in zip(self.my_surfaces, color):
            surface.color = color


def is_it_a_surface(surface: Surface) -> bool:
    res = functools.reduce(lambda x, y: x.coord_0 if isinstance(x, Point) else x + y.coord_0, surface.list_of_points, 0)
    print(res)
    return res