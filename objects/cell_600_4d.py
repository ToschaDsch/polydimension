from menus.single_functions import even_permutations, mirror_it
from objects.class_draw_interface import NDimensionalObject, JSONData
import json

class Cell6004d(NDimensionalObject):

    def __init__(self, dimensions: int = 4, colorful: bool = False, size: float=1.0, raw_data: str = None):
        raw_data_path = "arrays_600_cell.html" # "cell_600.txt" "arrays_600_cell.html"
        super().__init__(dimensions=dimensions, colorful=colorful, size=size, raw_data_path=raw_data_path)
        self.make_points()
        self.name_of_the_object = "cell 600 4d"


    def make_points(self):
        """the function makes all vertex coordinates for the object"""

        a, c = self.size, self.size * (1 + 5**.5) * 0.5
        symbols = [a * c, a, a / c, 0]

        icosians = even_permutations(init_list=symbols)
        print("icosians", icosians, len(icosians))
        init_coordinate = icosians
        # make other points(mirror it)
        for i in range(0, 4):
            init_coordinate = mirror_it(list_0=init_coordinate, axis=i)

        tetrahedron =self.add_tetrahedron()
        print("tetrahedron", *tetrahedron, len(tetrahedron))
        init_coordinate.extend(tetrahedron)

        another_16_coordinates = self.another_16_coordinates()
        print("another_16_coordinates", *another_16_coordinates)

        init_coordinate.extend(another_16_coordinates)
        print("init_coordinate", len(init_coordinate))
        self.json_data.points = init_coordinate
        print("json_data", self.json_data)
        new_dict = {"points": self.json_data.points,
                    "edges": self.json_data.lines,
                    "surfaces": self.json_data.surfaces,
                    "volumes": self.json_data.volumes,}
        json_ = json.dumps(new_dict)
        print("json_", json_)


    def add_tetrahedron(self, init_list: list[float]=None)->list[list[float]]:
        a= self.size
        dimensions = self.dimensions
        init_list = init_list if init_list else dimensions*[0]
        tetrahedron: list[list[float]] = []
        for i in range(dimensions-1,-1,-1):
            new_list = init_list.copy()

            new_list[i] = a
            tetrahedron.append(new_list.copy())
            new_list[i] = -a
            tetrahedron.append(new_list.copy())
        return tetrahedron

    def another_16_coordinates(self) -> list[list[float]]:
        a = self.size
        init_list = self.dimensions*[a]
        return self.add_tetrahedron(init_list=init_list)

    def make_lines(self):
        pass


    def make_surfaces(self):
        pass    # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        pass
