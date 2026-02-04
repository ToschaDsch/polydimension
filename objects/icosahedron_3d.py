import itertools

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
        a, c = self.size, self.size * (1 + 5**.5) * 0.5
        # this is the first triangle
        init_coordinate = [[0, a, c],
                           [a, c ,0],
                           [c, 0, a]]

        # make other points(mirror it)
        for i in range(0, 3):
            init_coordinate = mirror_it(list_0=init_coordinate, axis=i)

        # make a 4 coordinate
        for coord_i in init_coordinate:
            coord_i.insert(self._position_for_addition_coordination_4d, 0.0)

        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(coord_i)))

        for point in self._my_points:       # take the object to the bottom
            point.coord_0[2] = point.coord_0[2] - a + c
        self.points_to_show = self._my_points.copy()


    def make_lines(self):
        """ the function makes all vertex coordinates for the wedge"""
        temporal_set: list[set[Point]] = list()
        a = self.size*2
        for i in range(len(self._my_points)):
            for j in range(i + 1, len(self._my_points)):
                point_i = self._my_points[i]
                point_j = self._my_points[j]
                length = space_between_two_points(point_0=point_i, point_1=point_j)
                if  a * 0.99 < length < a * 1.01:
                    new_set = {point_i, point_j}
                    if new_set not in temporal_set:
                        temporal_set.append(new_set)
        for pair_of_points in temporal_set:
            point_0, point_1 = pair_of_points
            self._my_lines.append(Line(point_0=point_0, point_1=point_1))

    def make_surfaces(self):
        """the function make 3D coordinates of icos surfaces
        """
        center = get_center_from_list_of_points(self._my_points)
        points_for_surfaces: list[set[Point]] = []
        for i in range(len(self._my_lines)):
            for j in range(i + 1, len(self._my_lines)):
                for k in range(j + 1, len(self._my_lines)):
                    line_i = self._my_lines[i]
                    line_j = self._my_lines[j]
                    line_k = self._my_lines[k]
                    set_of_points: set[Point] = {line_i.point_0, line_i.point_1,
                                                 line_j.point_0, line_j.point_1,
                                                 line_k.point_0, line_k.point_1}
                    if len(set_of_points) == 3 and set_of_points not in points_for_surfaces:
                        points_for_surfaces.append(set_of_points)

        for set_of_points in points_for_surfaces:
            self._my_surfaces.append(Surface(list_of_points=list(set_of_points), init_center_of_the_volume=center))



    def make_volumes(self):
        pass



    def condition_0(self, point_i: Point, point_k_i: Point, point_j: Point, point_k_j: Point) -> bool:
        return ((((space_between_two_points(point_0=point_i, point_1=point_k_i) < 0.1 * self.size) &
           (space_between_two_points(point_0=point_j, point_1=point_k_j) < 0.1 * self.size))) or
         ((space_between_two_points(point_0=point_i, point_1=point_k_j) < 0.1 * self.size) &
          (space_between_two_points(point_0=point_j, point_1=point_k_i) < 0.1 * self.size)))

    def condition_1(self, point_i: Point, point_k_i: Point, point_j: Point, point_k_j: Point) -> bool:
        return ((((space_between_two_points(point_0=point_i, point_1=point_k_i) < 0.1 * self.size) &
           (space_between_two_points(point_0=point_j, point_1=point_k_j) < 0.1 * self.size))) or
         ((space_between_two_points(point_0=point_i, point_1=point_k_j) < 0.1 * self.size) &
          (space_between_two_points(point_0=point_j, point_1=point_k_i) < 0.1 * self.size)))