import math

import numpy as np
from sortedcontainers import SortedDict

from geometry import class_point, class_line, class_surface, class_volume
from geometry.class_geometric_object import GeometricObject
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_rotate_matrix
from variables.graphics import ObjectToDraw, TypeOfTheObjects


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

    def rotate_a_point(self, point: Point):
        point.coord_n = self.rotate_coord_0(coord_0=point.coord_0)

    def rotate_coord_0(self, coord_0: list[float]) -> list[np.ndarray]:
        coord_1 = np.array(coord_0) - self.dxi
        coord_0 = np.vstack(coord_1)
        result: np.ndarray = np.matmul(self.rotation_matrix, coord_0)
        return [result[0][0], result[1][0], result[2][0]]

    def rotate_a_point_without_shift(self, point: Point):
        coord_1 = np.array(point.coord_0)
        coord_0 = np.vstack(coord_1)
        result = np.matmul(self.rotation_matrix, coord_0)
        point.coord_n = [result[0][0], result[1][0], result[2][0]]

    def rotate_a_big_point(self, point):
        coord_0 = np.vstack(point.coord_0)
        result: np.ndarray = np.matmul(self.rotation_matrix, coord_0)
        point.coord_n = [result[0][0], result[1][0], result[2][0]]

    def rotate_a_line(self, line: Line):
        for point in (line.point_0, line.point_1):
            self.rotate_a_point(point)


    def clean_dict_of_draw_objects(self):
        self.dict_of_objects_to_draw.clear()

    def add_the_draw_element_to_sorted_dict(self, draw_object: GeometricObject|Point):
        match draw_object:
            case class_point.Point:
                self._add_to_dict_a_point(draw_object)
            case class_line.Line:
                self._add_to_dict_a_line(draw_object)
            case class_surface.Surface:
                self._add_to_dict_a_surface(draw_object)
            case class_volume.Volume:
                self._add_to_dict_a_volume(draw_object)
            case TypeOfTheObjects.surface:
                self._add_to_dict_a_surface(draw_object)
            case other:
                print('object is not found')

    def _add_to_dict_a_point(self, draw_object: ObjectToDraw):
        coord = draw_object.self_object.coord_n
        z = coord[2]
        self._add_an_object_to_the_dict(z=z, draw_object=draw_object)

    def _add_to_dict_a_text(self, draw_object: ObjectToDraw):
        coord = draw_object.self_object[0].coord_n
        z = coord[2]
        self._add_an_object_to_the_dict(z=z, draw_object=draw_object)

    def _add_to_dict_a_light_line(self, draw_object: ObjectToDraw):
        line = draw_object.self_object
        z = .5 * (line.point_0.coord_n[2] + line.point_1.coord_n[2])
        self._add_an_object_to_the_dict(z=z, draw_object=draw_object)

    def _add_to_dict_a_line(self, draw_object: ObjectToDraw):
        line = draw_object.self_object
        z = .5 * (line.point_0.coord_n[2] + line.point_1.coord_n[2]) + .0001 * (
                line.point_0.coord_n[0] + line.point_1.coord_n[0] +
                line.point_0.coord_n[1] + line.point_1.coord_n[1])
        self._add_an_object_to_the_dict(z=z, draw_object=draw_object)

    def _add_to_dict_an_joint(self, draw_object: ObjectToDraw):
        coord = draw_object.self_object[0]
        z = +coord[2] - draw_object.self_object[1]
        self._add_an_object_to_the_dict(z=z, draw_object=draw_object)

    def _add_to_dict_a_surface(self, draw_object: ObjectToDraw):
        surface: Surface = draw_object.self_object
        z = 0
        if len(surface.list_of_points) == 0:
            return None
        for point in surface.list_of_points:
            z += point.coord_n[2]

        z = z / len(surface.list_of_points)
        self._add_an_object_to_the_dict(z=z, draw_object=draw_object)
        return None

    def _add_an_object_to_the_dict(self, z: float, draw_object: ObjectToDraw):
        if z in self.dict_of_objects_to_draw:
            z += 0.01
            self._add_an_object_to_the_dict(z=z, draw_object=draw_object)
        else:
            self.dict_of_objects_to_draw[z] = draw_object
