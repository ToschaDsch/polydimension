import functools
import itertools
import math

import numpy

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from objects.class_draw_interface import NDimensionalObject


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
        set_for_lines = set()   #TODO lines!!!
        for numbers_of_points in self.list_of_point:
            set_for_lines.add(set(numbers_of_points[0:1]))
            set_for_lines.add(set(numbers_of_points[1:2]))
            set_for_lines.add(set(numbers_of_points[2:3]))
            set_for_lines.add({numbers_of_points[0], numbers_of_points[3]})

        print(set_for_lines)
        for set_i in set_for_lines:
            self.my_lines.append(Line(point_0=self.my_points[set_i[0]],
                                      point_1=self.my_points[set_i[1]]))

    def make_surfaces(self):
        print(*[str(n) + " " + str(point) + "\n" for n, point in enumerate(self.my_points)])

        for numbers_of_points in self.list_of_point:
            points_for_surface_i = [self.my_points[i] for i in numbers_of_points]
            self.my_surfaces.append(Surface(list_of_points=points_for_surface_i))

        for surface in self.my_surfaces: #check it
            is_it_a_surface(surface)

    def make_volumes(self):
        pass

def is_it_a_surface(surface: Surface) -> bool:
    res = functools.reduce(lambda x, y: x.coord_0 if isinstance(x, Point) else x + y.coord_0, surface.list_of_points, 0)
    print(res)
    return res