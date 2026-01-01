import itertools
import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from objects.class_draw_interface import NDimensionalObject


class Cube4d(NDimensionalObject):

    def __init__(self, dimensions: int = 4):
        self.list_of_point = [[0, 1, 5, 4],
                              [0, 2, 6, 4],
                              [0, 1, 3, 2],
                              [2, 6, 7, 3],
                              [4, 6, 7, 5],
                              [1, 3, 7, 5]]
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
        center = Point(coordinates=np.array([0,0,0,0]))
        for numbers_of_points in self.list_of_point:
            points_for_surface_i = [self._my_points[i] for i in numbers_of_points]
            self._my_surfaces.append(Surface(list_of_points=points_for_surface_i,
                                             color=self.surface_color,
                                             init_center_of_the_volume=center))

    def make_volumes(self):
        pass


def plus_a_dimension(list_0: list[float], a: float) -> list:
    """
     the function take n-dimensional cube and return (n+1) dimensional cube
    :param a: size of cube
    :param list_0: list n dimension ([-a, a])
    :return: list n+1 dimensional ([[-a, -a],[a, -a], [a,a], [a, -a]])
    """
    print("******* n-dimensional *******")
    list_n = []
    print("list 0", *list_0)
    for i in list_0:
        for ai in (a, -a):
            temp_list = add_an_element(point=i, a=ai)
            list_n.append(temp_list)
    print("list n", *list_n)
    return list_n

def add_an_element(point: float|list, a: float) -> list[float] | None:
    if isinstance(point, float|int):
        return [point, a]
    elif isinstance(point, list):
        list_i = point.copy() + [a]
        return list_i
    else:
        print("error", point)
        return None