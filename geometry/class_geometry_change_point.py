import math

import numpy as np
from sortedcontainers import SortedDict

from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point
from geometry.geometry_functions import get_rotate_matrix


class GeometryChangePoint:
    """the class is a singleton
    it calculates new coordinate for the object and send it to a dict
    """
    corner_f_init: float = math.pi * 0.25
    corner_j_init: float = math.pi * 0.25
    sin_j_init = math.sin(corner_j_init)
    cos_j_init = math.cos(corner_j_init)
    sin_f_init = math.sin(corner_f_init)
    cos_f_init = math.cos(corner_f_init)

    def __init__(self):
        self.dimensional: int = 4
        self.angles: list[float] = [math.pi * 0.25, math.pi * 0.25, math.pi * 0.25,
                                0.0, 0.0, 0.0] # xy, xz, xd1, yz, yd1, zd1
        self.sin: list[float] = [math.sin(x) for x in self.angles]
        self.cos: list[float] = [math.cos(x) for x in self.angles]
        self.dxi: list[float] = [0,0,0,0]
        self.rotation_matrix: np.ndarray = get_rotate_matrix(sin=self.sin,
                                                             cos=self.cos,
                                                             dimensional=self.dimensional)
        self.dict_of_objects_to_draw: SortedDict = SortedDict()


    def change_corners(self, angles: list[float], dx: list[float]):
        self.angles = angles
        self.sin: list[float] = [math.sin(x) for x in self.angles]
        self.cos: list[float] = [math.cos(x) for x in self.angles]
        self.dxi: np.ndarray = np.array(dx)
        self.rotation_matrix: np.ndarray = get_rotate_matrix(sin=self.sin,
                                                             cos=self.cos,
                                                             dimensional=self.dimensional)
        self.dict_of_objects_to_draw = SortedDict()

    def rotate_a_point(self, point):
        coord_0 = np.vstack(point.coord_0)
        result: np.ndarray = np.matmul(self.rotation_matrix, coord_0)
        point.coord_n = [result[0][0], result[1][0], result[2][0]]


    def clean_dict_of_draw_objects(self):
        self.dict_of_objects_to_draw.clear()

    def add_the_draw_element_to_sorted_dict(self, draw_object: GeometricObject|Point):
        z = draw_object.get_center().coord_n[2]
        self._add_an_object_to_the_dict(draw_object=draw_object, z=z)


    def _add_an_object_to_the_dict(self, z: float, draw_object: GeometricObject|Point):
        if z in self.dict_of_objects_to_draw:
            z += 0.01
            self._add_an_object_to_the_dict(z=z, draw_object=draw_object)
        else:
            self.dict_of_objects_to_draw[z] = draw_object
