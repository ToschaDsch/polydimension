import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.geometry_functions import find_closed_contours_from_lines, find_lines
from menus.single_functions import even_permutations, mirror_it, only_even_permutations
from objects.class_draw_interface import NDimensionalObject, JSONData
import json

class Cell6004d(NDimensionalObject):

    def __init__(self, dimensions: int = 4, colorful: bool = False, size: float=1.0, raw_data: str = None):
        raw_data_path = "cell_600.txt" # "cell_600.txt" "arrays_600_cell.html"
        super().__init__(dimensions=dimensions, colorful=colorful, size=size, raw_data_path=raw_data_path)
        if raw_data_path == "arrays_600_cell.html":
            self.make_geometry()
        self.name_of_the_object = "cell 600 4d"


    def make_points(self):
        """the function makes all vertex coordinates for the object"""

        a, c = self.size, self.size * (1 + 5**.5) * 0.5
        symbols = [a * c, a, a / c, 0]

        icosians = only_even_permutations(symbols=symbols)
        init_coordinate = icosians
        # make other points(mirror it)
        for i in range(0, 4):
            init_coordinate = mirror_it(list_0=init_coordinate, axis=i)
        tetrahedron =self.add_tetrahedron()
        init_coordinate.extend(tetrahedron)

        another_16_coordinates = self.another_16_coordinates()

        init_coordinate.extend(another_16_coordinates)
        self.json_data.points = init_coordinate
        print("json_data", self.json_data)
        new_dict = {"points": self.json_data.points,
                    "edges": self.json_data.lines,
                    "surfaces": self.json_data.surfaces,
                    "volumes": self.json_data.volumes,}
        json_ = json.dumps(new_dict)
        print("json_", json_)

        for i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(i)))
        print("my points", len(self._my_points))
        self.json_data.points = init_coordinate


    def add_tetrahedron(self)->list[list[float]]:
        a = 2*self.size
        var1 = 1
        if var1 == 0:
            return even_permutations([2*a, 0, 0, 0]) + even_permutations([-2*a, 0, 0, 0])
        else:
            return [[0, 0, 0, a],
                    [0, 0, 0, -a],
                    [0, 0, a, 0],
                    [0, 0, -a, 0],
                    [0, a, 0, 0],
                    [0, -a, 0, 0],
                    [a, 0, 0, 0],
                    [-a, 0, 0, 0]]

    def another_16_coordinates(self) -> list[list[float]]:
        a = self.size
        var_1 = 1
        if var_1 == 0:
            list_0 = even_permutations([-a, a, a, a]) + even_permutations([-a, -a, a, a]) + even_permutations([-a, -a, -a, a])
            list_0.append([a,a,a,a])
            list_0.append([-a,-a,-a,-a])
            return  list_0
        else:
            return [[a, a, a, a],
                    [a, a, a, -a],
                    [a, a, -a, a],
                    [a, a, -a, -a],
                    [a, -a, a, a],
                    [a, -a, a, -a],
                    [a, -a, -a, a],
                    [a, -a, -a, -a],
                    [-a, a, a, a],
                    [-a, a, a, -a],
                    [-a, a, -a, a],
                    [-a, a, -a, -a],
                    [-a, -a, a, a],
                    [-a, -a, a, -a],
                    [-a, -a, -a, a],
                    [-a, -a, -a, -a]]

    def make_lines(self):
        length = 0.618*self.size*2
        number_of_lines = find_lines(points=self._my_points, length=length)
        number_of_lines_2 = [list(x) for x in number_of_lines]
        numbers_of_surfaces = find_closed_contours_from_lines(lines=number_of_lines_2)
        print("snub_lines", len(number_of_lines))
        for i, j in number_of_lines:
            self._my_lines.append(Line(point_0=self._my_points[i], point_1=self._my_points[j]))
        self.json_data.lines = [list(x) for x in number_of_lines]
        print("numbers_of_surfaces", len(numbers_of_surfaces))
        self.json_data.surfaces = numbers_of_surfaces
        print("json_data", self.json_data)

        dict_json = {"points": self.json_data.points,
                     "edges": self.json_data.lines,
                     "surfaces": self.json_data.surfaces,
                     "volumes": self.json_data.volumes}
        for key, value in dict_json.items():
            print("dict_json", key, value)
        print("*******")
        dict_json_2 = json.dumps(dict_json)
        print("dict_json_2", dict_json_2)


    def make_surfaces(self):
        pass


    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        pass
