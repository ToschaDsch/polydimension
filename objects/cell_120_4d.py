import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.geometry_functions import find_lines, find_cycles
from frontend.menus.single_functions import mirror_it, only_even_permutations
from objects.class_draw_interface import NDimensionalObject, JSONData
import json

from variables.graphics import Transparency


class Cell1204d(NDimensionalObject):

    def __init__(self, dimensions: int = 4, colorful: bool = False, size: float=1.0, raw_data: str = None,
                 transparent: Transparency=Transparency.transparent):
        raw_data_path = "cell_120.txt" # "cell_120.txt"
        super().__init__(dimensions=dimensions, colorful=colorful, size=size, raw_data_path=raw_data_path, transparent=transparent)

        self.name_of_the_object = "cell 120 4d"
        self.correct_all_points(d=self.size*(1 + 5**.5) * 0.5-0.3)


    def make_points(self):
        """make points"""

        a, b, c = self.size, self.size*5**0.5, (1 + 5**.5) * 0.5
        symbols_0 = [0, a/(c*c), a, c*c]
        init_coordinate = only_even_permutations(symbols=symbols_0)
        symbols_1 = [0, a/c, a*c, b]
        init_coordinate += only_even_permutations(symbols=symbols_1)
        symbols_2 = [a/c, a,  a*c, 2*a]
        init_coordinate += only_even_permutations(symbols=symbols_2)
        init_coordinate += [[2 * a, 2 * a, 0, 0],
                            [0, 2 * a, 0, 2 * a],
                            [0, 0, 2 * a, 2 * a],
                            [0, 2 * a, 2 * a, 0],
                            [2 * a, 0, 2 * a, 0],
                            [2 * a, 0, 0, 2 * a]]
        init_coordinate += [[a, a, a, b],
                            [a, a, b, a],
                            [a, b, a, a],
                            [b, a, a, a]]
        init_coordinate += [[a / (c * c),  a*c, a*c, a*c],
                            [a*c, a / (c * c), a*c, a*c],
                            [a*c, a*c, a / (c * c), a*c],
                            [a*c, a*c, a*c, a / (c * c)]]
        init_coordinate += [[a*c * c, a / c, a / c, a / c],
                            [a / c, a*c * c, a / c, a / c],
                            [a / c, a / c, a*c * c, a / c],
                            [a / c, a / c, a / c, a*c * c]]

        # make other points(mirror it)
        for i in range(0, 4):
            init_coordinate = mirror_it(list_0=init_coordinate, axis=i)
        for i in init_coordinate:
            self._my_points.append(Point(coordinates=np.array(i)))

        self.json_data = JSONData(points=init_coordinate,
                                    lines = [],
                                    surfaces = [],
                                    volumes = [])

    def make_lines(self):
        a, b, c = self.size, self.size * 5 ** 0.5, (1 + 5 ** .5) * 0.5
        length = a * (3 - 5**0.5)

        number_of_lines = find_lines(points=self._my_points, length=length)
        number_of_lines_2 = [list(x) for x in number_of_lines]
        self.json_data.lines.extend(number_of_lines_2)
        numbers_of_points_in_contour = find_cycles(edges=number_of_lines_2, points=self._my_points, cycle_size=5)
        self.json_data.surfaces = numbers_of_points_in_contour

        dict_json = {"points": self.json_data.points,
                     "edges": self.json_data.lines,
                     "surfaces": self.json_data.surfaces,
                     "volumes": self.json_data.volumes}
        for key, value in dict_json.items():
            print("dict_json", key, len(value))
        print("*******")
        dict_json_2 = json.dumps(dict_json)
        print("dict_json_2", dict_json_2)

        #with open("demofile.txt", "w") as f:
         #   f.write(dict_json_2)

        # open and read the file after the overwriting:
        #with open("demofile.txt") as f:
         #   print(f.read())
        return None
        for i, j in number_of_lines:
            self._my_lines.append(Line(point_0=self._my_points[i], point_1=self._my_points[j]))
        self.json_data.lines = [list(x) for x in number_of_lines]




    def make_surfaces(self):
        pass




    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        pass
