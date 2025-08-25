import math

import numpy as np
from numpy.ma.core import identity
from sortedcontainers import SortedDict

from geometry import class_point, class_line, class_surface, class_volume
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
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
        self.angles: list[float] = [math.pi * 0.25, math.pi * 0.25, math.pi * 0.25,
                                0.0, 0.0, 0.0] # xy, xz, xd1, yz, yd1, zd1
        self.sin: list[float] = [math.sin(x) for x in self.angles]
        self.cos: list[float] = [math.cos(x) for x in self.angles]
        self.dxi: list[float] = [0,0,0,0]
        self.rotate_j = np.array([[self.cos_j, - self.sin_j, 0],
                                  [self.sin_j, self.cos_j, 0],
                                  [0, 0, 1]])

        self.rotate_f = np.array([[1, 0, 0],
                                  [0, self.cos_f, - self.sin_f],
                                  [0, self.sin_f, self.cos_f]])

        self.dict_of_objects_to_draw: SortedDict = SortedDict()

    def get_rotate_matrix(self, sinx: list[float], cosx: list[float], dimensional: int = 3) -> np.ndarray:
        """
        :param sinx: list of sin a, b, g
        :param cosx: list of cos a, b, g
        :param dimensional: 3d, 4d
        :return: rotate matrix. for 3d -> Ra*Rb*Rg
        """
        r = []
        if dimensional == 3:
            r[0] = np.array([[cosx[0], -sinx[0], 0],
                          [sinx[0], cosx[0], 0],
                           [0, 0, 1]
                          ])
            r[1] = np.array([[cosx[1], 0 -sinx[1]],
                           [0, 1, 0],
                           [-sinx[1], 0, cosx[1]]
                           ])
            r[2] = np.array([[1,0,0],
                           [0, cosx[2], -sinx[2]],
                           [0, -sinx[2], cosx[2]]
                           ])
        elif dimensional == 4:
            r[0] = np.array([[cosx[2], 0 -sinx[2]],])
        result_matrix = np.identity(dimensional, dtype=np.float64)
        print("identity matrix", identity)
        for r_i in r:
            result_matrix = np.dot(r_i, result_matrix)
        return result_matrix

    def change_corners(self, f: float, j: float, dx: float = 0, dy: float = 0, dz: float = 0):
        self.corner_f = f
        self.corner_j = j
        self.sin_j = math.sin(self.corner_j)
        self.cos_j = math.cos(self.corner_j)
        self.sin_f = math.sin(self.corner_f)
        self.cos_f = math.cos(self.corner_f)
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.rotate_j = np.array([[self.cos_j, - self.sin_j, 0],
                                  [self.sin_j, self.cos_j, 0],
                                  [0, 0, 1]])

        self.rotate_f = np.array([[1, 0, 0],
                                  [0, self.cos_f, - self.sin_f],
                                  [0, self.sin_f, self.cos_f]])
        self.dict_of_objects_to_draw = SortedDict()

    def rotate_a_point(self, point: Point):
        point.coord_n = self.rotate_coord_0(coord_0=point.coord_0)

    def rotate_coord_0(self, coord_0: list[float]) -> list[float]:
        coord_1 = np.array(coord_0) - np.array([self.dx, self.dy, self.dz])
        coord_0 = np.vstack(coord_1)
        result = np.matmul(self.rotate_f, np.matmul(self.rotate_j, coord_0))
        return [result[0][0], result[1][0], result[2][0]]

    def rotate_a_point_without_shift(self, point: Point):
        coord_1 = np.array(point.coord_0)
        coord_0 = np.vstack(coord_1)
        result = np.matmul(self.rotate_f, np.matmul(self.rotate_j, coord_0))
        point.coord_n = [result[0][0], result[1][0], result[2][0]]

    def rotate_a_big_point(self, point):
        coord_0 = np.vstack(point.coord_0)
        result = np.matmul(self.rotate_f, np.matmul(self.rotate_j, coord_0))
        point.coord_n = [result[0][0], result[1][0], result[2][0]]

    def rotate_a_line(self, line: Line):
        for point in (line.point_0, line.point_1):
            self.rotate_a_point(point)

    def rotate_a_line_without_shift(self, line: Line):
        for point in (line.point_0, line.point_1):
            self.rotate_a_point_without_shift(point)

    def clean_dict_of_draw_objects(self):
        self.dict_of_objects_to_draw.clear()

    def add_the_draw_element_to_sorted_dict(self, draw_object: Line | Surface):
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
