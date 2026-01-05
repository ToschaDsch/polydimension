from geometry import geometry_functions
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from objects.class_draw_interface import NDimensionalObject


class Octahedron3d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False,
                 dimension_shift_number: int=0,
                 dimension_shift_length: int=0):
        self._dimension_shift_number = dimension_shift_number
        self._dimension_shift_length = dimension_shift_length
        super().__init__(dimensions=dimensions, colorful=colorful)
        self.name_of_the_object = "Cube 3d"



    def make_points(self):
        init_coordinate = []
        for i in range(0, 3):
            for a_i in (self.size, -self.size):
                list_i = self.dimensions*[0]
                list_i[i] = a_i
                init_coordinate.append(list_i)
        for coord_i in init_coordinate:
            self._my_points.append(Point(coordinates=coord_i))
        self.points_to_show = self._my_points.copy()
        for i, point in enumerate(self._my_points):
            print(i, point)


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
        number_of_points = [[4, 0, 2],
                            [4, 1, 2],
                            [4, 1, 3],
                            [4, 0, 3],
                            [5, 0, 2],
                            [5, 1, 2],
                            [5, 1, 3],
                            [5, 0, 3]]
        z = 0
        for list_of_points_i in number_of_points:

            list_of_points = [self._my_points[i] for i in list_of_points_i]
            print("points", z,  *list_of_points)
            self._my_surfaces.append(Surface(list_of_points=list_of_points))
            z+=1

    def make_volumes(self):
        pass



