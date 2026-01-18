import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_center_from_list_of_points
from objects.class_draw_interface import NDimensionalObject


class Tetrahedron3d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False, size: float = 2,
                 init_point: list[int]=None):
        self._init_points = init_point if init_point else [0, 1, 2]
        super().__init__(dimensions=dimensions, colorful=colorful, size=size)
        self.name_of_the_object = "Tetrahedron 3d"


    def make_points(self):
        w, h = self.dimensions, 3
        init_coordinate = [[0 for _ in range(w)] for _ in range(h)]
        for i in range(0, 3):
            init_coordinate[i][self._init_points[i]] = self.size

        point_0 = np.array([0 for _ in range(self.dimensions)])
        self._my_points.append(Point(coordinates=point_0))
        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(coord_i)))
        for point in self._my_points:       # take the object to the bottom
            point.coord_0[2] = point.coord_0[2] - self.size/2
        self.points_to_show = self._my_points.copy()


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



