from dataclasses import fields

import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point
from menus.single_functions import open_and_read_a_file
from objects.class_draw_interface import NDimensionalObject, JSONData
from variables.menus import Menus
import json


class Cell244d(NDimensionalObject):

    def __init__(self, dimensions: int = 4, colorful: bool = False, size: float=1.0, raw_data: str = None):
        if raw_data is None:
            raw_data = "cell_24.txt"
        path = Menus.raw_data_path + "//" + raw_data
        raw_data = open_and_read_a_file(path=path)
        details_of_the_objects = json.loads(raw_data)
        self.json_data = JSONData(points=details_of_the_objects["points"],
                                  lines=details_of_the_objects["edges"],
                                  surfaces=details_of_the_objects["surfaces"],
                                  volumes=details_of_the_objects["volumes"],)
        for field in fields(self.json_data):
            print(field.name, getattr(self.json_data, field.name))
        super().__init__(dimensions=dimensions, colorful=colorful, size=size)
        self.name_of_the_object = "24 cell 4d"



    def make_points(self):
        a = self.size
        ...
        self.points_to_show = self._my_points.copy()


    def make_lines(self):
        ...


    def make_surfaces(self):
        pass    # the object take all the surfaces from 3d cubs in 4d (see volumes)

    def make_volumes(self):
        """the function make a cube in 3d, shifts it in one of dimension in 4d and get the surfaces of it"""
        ...