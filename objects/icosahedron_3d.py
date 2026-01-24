import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_center_from_list_of_points, space_between_two_points
from menus.single_functions import mirror_it
from objects.class_draw_interface import NDimensionalObject


class Icosahedron3d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False, size: float = 2.0,
                 position_for_addition_coordination_4d: int = 3):
        self._position_for_addition_coordination_4d = position_for_addition_coordination_4d

        super().__init__(dimensions=dimensions, colorful=colorful, size=size)
        self.name_of_the_object = "Tetrahedron 3d"


    def make_points(self):
        """ the function makes all vertex coordinates for the wedge"""
        a, c = self.size, self.size * (1 + 5**.5) *0.5
        # this is the first triangle
        init_coordinate = [[0, a, c],
                           [a, c ,0],
                           [c, 0, a]]

        # make other points(mirror it)
        for i in range(0, 3):
            init_coordinate = mirror_it(list_0=init_coordinate, axis=0)

        # make a 4 coordinate
        for coord_i in init_coordinate:
            coord_i.insert(self._position_for_addition_coordination_4d, 0.0)

        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(coord_i)))

        print("points created", *self._my_points)

    def make_lines(self):
        """ the function makes all vertex coordinates for the wedge"""
        temporal_set: list[set[Point]] = list()
        a = self.size*self.size*4
        for i in range(len(self._my_points)):
            for j in range(i + 1, len(self._my_points)):
                point_i = self._my_points[i]
                point_j = self._my_points[j]
                length = space_between_two_points(point_0=point_i, point_1=point_j)
                if  a * 0.99 < length < a * 1.01:
                    print("there is a line!")
                    new_set = {point_i, point_j}
                    if new_set not in temporal_set:
                        temporal_set.append(new_set)
        for pair_of_points in temporal_set:
            point_0, point_1 = pair_of_points
            self._my_lines.append(Line(point_0=point_0, point_1=point_1))
        print("lines created", *self._my_lines)

    def make_surfaces(self):
        center = get_center_from_list_of_points(self._my_points)


    def make_volumes(self):
        pass



