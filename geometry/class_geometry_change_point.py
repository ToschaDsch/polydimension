import math

import numpy as np
from sortedcontainers import SortedDict

import geometry.class_line
from geometry.class_geometric_object import GeometricObject
from geometry.class_point import Point
from geometry.geometry_functions import get_rotate_matrix, get_2d_coordinate_with_perspective
from variables.geometry_var import CoordinatesScreen
from variables.menus import Menus


class  GeometryChangePoint:
    """the class is a singleton
    it calculates new coordinate for the object and send it to a dict
    """
    corner_init: float = math.pi * 0.25

    def __init__(self):
        self.dimensional: int = 4
        self.angles: np.ndarray = np.array([GeometryChangePoint.corner_init,
                                    GeometryChangePoint.corner_init,
                                    GeometryChangePoint.corner_init,
                                    0.0, 0.0, 0.0]) # xy, xz, xd1, yz, yd1, zd1
        self.sin: list[float] = [math.sin(x) for x in self.angles]
        self.cos: list[float] = [math.cos(x) for x in self.angles]
        self.dxi: np.ndarray = np.array([0,0])
        self.rotation_matrix: np.ndarray = get_rotate_matrix(sin=self.sin,
                                                             cos=self.cos,
                                                             dimensional=self.dimensional)

        self.x0y0: np.ndarray= np.array([int(Menus.display_width / 2),
                                        int(Menus.display_height / 2),
                                         0])

        self.scale: float = CoordinatesScreen.scale

        self.dict_of_objects_to_draw: SortedDict = SortedDict()
        self.draw_with_perspective: bool = False

    def _change_corners(self):
        self.sin: list[float] = [math.sin(x) for x in self.angles]
        self.cos: list[float] = [math.cos(x) for x in self.angles]

        self.rotation_matrix: np.ndarray = get_rotate_matrix(sin=self.sin,
                                                             cos=self.cos,
                                                             dimensional=self.dimensional)


    def calculate_new_coordinates_for_the_list_of_points(self, angles: np.ndarray=None, dx: np.ndarray=None,
                                                         points: list[Point]=None, scale: float=None):
        if angles is not None and dx is not None:
            self.angles = angles
            self.dxi = dx
        if scale is not None:
            self.scale = scale
        self._change_corners()
        self.dict_of_objects_to_draw = SortedDict() #clear the dict
        for point in points:
            self._rotate_and_shift_a_point(point=point)

    def _rotate_and_shift_a_point(self, point: Point):
        coord_0 = np.vstack(point.coord_0)
        x0_y0: np.ndarray = np.matmul(self.rotation_matrix, coord_0)
        point.coord_only_rotate = np.resize(x0_y0, len(point.coord_0))
        if self.draw_with_perspective:
            x0_y0 = get_2d_coordinate_with_perspective(x=x0_y0[0], y=x0_y0[1], z=x0_y0[2])
        point.coord_n = np.resize(x0_y0, 3) * self.scale + self.x0y0  + np.resize(self.dxi, 3)

    def clean_dict_of_draw_objects(self):
        self.dict_of_objects_to_draw.clear()

    def add_the_draw_element_to_sorted_dict(self, draw_object: GeometricObject|Point):
        match type(draw_object):
            case geometry.class_point.Point:
                z = draw_object.coord_n[2]
            case geometry.class_line.Line:
                z = 0.5*(draw_object.point_0.coord_n[2] + draw_object.point_1.coord_n[2])
            case geometry.class_surface.Surface:
                z = draw_object.get_center().coord_n[2]
            case _other:
                z = 0

        self._add_an_object_to_the_dict(draw_object=draw_object, z=z)


    def _add_an_object_to_the_dict(self, z: float, draw_object: GeometricObject|Point):
        if z in self.dict_of_objects_to_draw:
            z += 0.0000001
            self._add_an_object_to_the_dict(z=z, draw_object=draw_object)
        else:
            self.dict_of_objects_to_draw[z] = draw_object
