from geometry import geometry_functions
from geometry.class_line import Line
from geometry.class_point import Point
from objects.class_draw_interface import NDimensionalObject
from objects.octahedron_3d import Octahedron3d


class Cell164d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False, size: float=1.0,
                 dimension_shift_number: int=0,
                 dimension_shift_length: int=0):
        self._dimension_shift_number = dimension_shift_number
        self._dimension_shift_length = dimension_shift_length
        super().__init__(dimensions=dimensions, colorful=colorful, size=size)
        self.name_of_the_object = "16Cell 4d"


    def make_points(self):
        init_coordinate = []
        n = 4
        for i in range(0, n):
            for a_i in (self.size, -self.size):
                list_i = self.dimensions*[0]
                list_i[i] = a_i
                init_coordinate.append(list_i)
        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=coord_i))
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
        pass        # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make an octahedron in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        init_spaces = ([1, 2, 3],
                       [0, 1, 3],
                       [0, 2, 3],
                       [0, 1, 2])
        for list_of_init_spaces in init_spaces:
            octa_i = Octahedron3d(dimensions=4, init_point=list_of_init_spaces)
            volume_i = self._get_a_volume_surfaces_and_points_form_another_object(obj=octa_i)
            self._my_volumes.append(volume_i)



