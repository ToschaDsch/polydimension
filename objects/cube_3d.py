import itertools
import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from objects.class_draw_interface import NDimensionalObject


class Cube3d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False,
                 dimension_shift_number: int=0,
                 dimension_shift_length: int=0):
        self.list_of_point = [[0, 1, 5, 4],
                              [0, 2, 6, 4],
                              [0, 1, 3, 2],
                              [2, 6, 7, 3],
                              [4, 6, 7, 5],
                              [1, 3, 7, 5]]
        self._dimension_shift_number = dimension_shift_number
        self._dimension_shift_length = dimension_shift_length
        super().__init__(dimensions=dimensions, colorful=colorful)
        self.name_of_the_object = "Cube 3d"



    def make_points(self):
        a = self.size
        initial_set = [a, -a]
        init_list_of_coordinates = np.array([np.array(x) for x in itertools.product(initial_set,repeat=3)])
        for coordinate in init_list_of_coordinates:
            new_coordinate = np.resize(coordinate, self.dimensions)
            self._my_points.append(Point(coordinates=new_coordinate))

        if self._dimension_shift_length:    # shift all the points for a cube in 4d
            self.dimensions+=1
            for point in self._my_points:
                point.coord_0 = np.insert(point.coord_0, self._dimension_shift_number, self._dimension_shift_length)
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
        center = Point(coordinates=np.array([0,0,0,0]))
        for numbers_of_points in self.list_of_point:
            points_for_surface_i = [self._my_points[i] for i in numbers_of_points]
            self._my_surfaces.append(Surface(list_of_points=points_for_surface_i,
                                             init_center_of_the_volume=center))

    def make_volumes(self):
        pass



