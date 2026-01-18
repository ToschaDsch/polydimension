import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_center_from_list_of_points
from menus.single_functions import mirror_it
from objects.class_draw_interface import NDimensionalObject


class Icosahedron3d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False, size: float = 2,
                 init_point: list[int]=None):
        self._init_points = init_point if init_point else [0, 1, 2]
        self.c: float = size * (1 + 5**.5) *0.5

        super().__init__(dimensions=dimensions, colorful=colorful, size=size)
        self.name_of_the_object = "Tetrahedron 3d"


    def make_points(self):
        """ the function makes all vertex coordinates for the wedge"""
        a, c = self.size, self.c
        # this is the first triangle
        init_coordinate = [[0, a, c],
                           [a, c ,0],
                           [c, 0, a]]

        # make other points(mirror it)
        for i in range(0, 3):
            init_coordinate = mirror_it(list_0=init_coordinate, axis=0)

        if (positionForAdditionCoordination4d.first > -1)
            for (point in coordinateList) {
            point.add(positionForAdditionCoordination4d.first, 0f)




    def make_lines(self):
        for i in range(len(self._my_points)):
            for j in range(i + 1, len(self._my_points)):
                self._my_lines.append(Line(point_0=self._my_points[i],
                                           point_1=self._my_points[j], width=2))

    def make_surfaces(self):
        center = get_center_from_list_of_points(self._my_points)
        list_of_points = [[0, 1, 2],
                          [0, 2, 3],
                          [0, 3, 1],
                          [1, 2, 3]]
        for list_i in list_of_points:
            list_of_point = [self._my_points[i] for i in list_i]
            self._my_surfaces.append(Surface(list_of_points=list_of_point,
                                         init_center_of_the_volume=center))

    def make_volumes(self):
        pass



