import numpy as np

from geometry import geometry_functions
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from objects.class_draw_interface import NDimensionalObject


class Octahedron3d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False,
                 init_point: list[int]=None):
        self._init_points = init_point if init_point else [0, 1, 2]
        super().__init__(dimensions=dimensions, colorful=colorful)
        self.name_of_the_object = "Octahedron 3d"


    def make_points(self):
        w, h = self.dimensions, 6
        init_coordinate = [[0 for _ in range(w)] for _ in range(h)]
        for i in range(0, 3):
            init_coordinate[i][self._init_points[i]] = self.size
            init_coordinate[i + 3][self._init_points[i]] = -self.size
        print("new points", *init_coordinate)
        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(coord_i)))
            self.points_to_show = self._my_points.copy()


    def make_lines(self):
        temporal_list = []
        for i in range(len(self._my_points)):
            for j in range(i + 1, len(self._my_points)):
                length = geometry_functions.space_between_two_points(point_0=self._my_points[i],
                                                                     point_1=self._my_points[j])
                if 2 * self.size * self.size * 0.99 <= length*length <= 2 * self.size * self.size * 1.01:
                        new_set = {self._my_points[i], self._my_points[j]}
                        if new_set not in temporal_list:
                            temporal_list.append(new_set)
        for set_of_points in temporal_list:
            point_0=set_of_points.pop()
            point_1=set_of_points.pop()
            self._my_lines.append(Line(point_0=point_0, point_1=point_1, width=2))

    def make_surfaces(self):
        number_of_points = [[0, 1, 2],
                            [3, 1, 2],
                            [0, 2, 4],
                            [3, 2, 4],
                            [0, 4, 5],
                            [3, 4, 5],
                            [0, 5, 1],
                            [3, 5, 1]]
        for list_of_points_i in number_of_points:
            list_of_points = [self._my_points[i] for i in list_of_points_i]
            self._my_surfaces.append(Surface(list_of_points=list_of_points))

    def make_volumes(self):
        pass



