from menus.single_functions import even_permutations, mirror_it, only_even_permutations
from objects.class_draw_interface import NDimensionalObject, JSONData
import json

class Cell6004d(NDimensionalObject):

    def __init__(self, dimensions: int = 4, colorful: bool = False, size: float=1.0, raw_data: str = None):
        raw_data_path = "cell_600.txt" # "cell_600.txt" "arrays_600_cell.html"
        super().__init__(dimensions=dimensions, colorful=colorful, size=size, raw_data_path=raw_data_path)
        self.make_points()
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
        pass


    def make_surfaces(self):
        pass    # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        pass
