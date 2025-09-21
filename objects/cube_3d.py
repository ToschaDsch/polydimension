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
                if numpy.sum(self.my_points[i].coord_0 - self.my_points[j].coord_0) == 2:
                    self.my_lines.append(Line(point_0=self.my_points[i], point_1=self.my_points[j]))

    def make_surfaces(self):
        print(*[str(n) + " " + str(point) + "\n" for n, point in enumerate(self.my_points)])
        points_for_surface_0 = [self.my_points[0],
                               self.my_points[1],
                               self.my_points[5],
                               self.my_points[4]]
        self.my_surfaces.append(Surface(list_of_points=points_for_surface_0))
        points_for_surface_1 = [self.my_points[0],
                                 self.my_points[2],
                                 self.my_points[6],
                                 self.my_points[7]]
        self.my_surfaces.append(Surface(list_of_points=points_for_surface_1))
        points_for_surface_2 = [self.my_points[0],
                                 self.my_points[1],
                                 self.my_points[3],
                                 self.my_points[2]]
        self.my_surfaces.append(Surface(list_of_points=points_for_surface_2))
        points_for_surface_3 = [self.my_points[2],
                                 self.my_points[6],
                                 self.my_points[7],
                                 self.my_points[3]]
        self.my_surfaces.append(Surface(list_of_points=points_for_surface_3))
        points_for_surface_4 = [self.my_points[4],
                                 self.my_points[6],
                                 self.my_points[7],
                                 self.my_points[5]]
        self.my_surfaces.append(Surface(list_of_points=points_for_surface_4))
        points_for_surface_5 = [self.my_points[1],
                                 self.my_points[3],
                                 self.my_points[7],
                                 self.my_points[6]]
        self.my_surfaces.append(Surface(list_of_points=points_for_surface_5))
        for surface in self.my_surfaces:
            is_it_a_surface(surface)

    def make_volumes(self):
        pass

def is_it_a_surface(surface: Surface) -> bool:
    res = functools.reduce(lambda x, y: x.coord_0 if isinstance(x, Point) else x + y.coord_0[2], surface.list_of_points, 0)
    print(res)
    return res