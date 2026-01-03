import itertools
import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.class_volume import Volume
from objects.class_draw_interface import NDimensionalObject
from objects.cube_3d import Cube3d


class Cube4d(NDimensionalObject):

    def __init__(self, dimensions: int = 4):
        super().__init__(dimensions=dimensions)
        self.name_of_the_object = "Cube 4d"



    def make_points(self):
        a = self.size
        initial_set = [a, -a]
        init_list_of_coordinates = np.array([np.array(x) for x in itertools.product(initial_set,repeat=4)])
        for coordinate in init_list_of_coordinates:
            new_coordinate = np.resize(coordinate, self.dimensions)
            self._my_points.append(Point(coordinates=new_coordinate))
        self.points_to_show = self._my_points.copy()


    def make_lines(self):
        for i in range(len(self._my_points)):
            for j in range(i+1, len(self._my_points)):
                point_i = self._my_points[i]
                point_j = self._my_points[j]
                delta_point = point_i.coord_0 - point_j.coord_0
                if sum(delta_point) == 2*self.size:
                    set_delta = set(delta_point)
                    if set_delta in ({0, 2*self.size}, {0, -2*self.size}):
                        self._my_lines.append(Line(point_i, point_j, width=2))


    def make_surfaces(self):
        pass    # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        for i in range(4):
            for j in (1, -1):
                cube_i = Cube3d(dimensions=3, dimension_shift_number=i, dimension_shift_length=j)
                list_of_surfaces = cube_i.get_surfaces()
                # change points for my_points
                for surface in list_of_surfaces:
                    for point_i in surface.list_of_points:
                        if point_i in self._my_points:
                            continue
                        for point_j in self._my_points:
                            if np.array_equal(point_i.coord_0, point_j.coord_0):
                                point_i = point_j
                                continue
                volume_i = Volume(list_of_points=None, list_of_lines=None, list_of_surfaces=list_of_surfaces)
                self._my_volumes.append(volume_i)
