import math

import numpy as np
from sortedcontainers import SortedDict

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from variables import TypeOfTheObjects, ObjectToDraw


class GeometryChangePoint:
    """the class is a singleton
    it calculates new coordinate for the object and send it to a dict
    """
    corner_f: float = math.pi * 0.25
    corner_j: float = math.pi * 0.25
    sin_j = math.sin(corner_j)
    cos_j = math.cos(corner_j)
    sin_f = math.sin(corner_f)
    cos_f = math.cos(corner_f)

    def __init__(self):
        self.corner_f = 0
        self.corner_j = 0
        self.sin_j = 0
        self.cos_j = 0
        self.sin_f = 0
        self.cos_f = 0
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.rotate_j = np.array([[self.cos_j, - self.sin_j, 0],
                                  [self.sin_j, self.cos_j, 0],
                                  [0, 0, 1]])

        self.rotate_f = np.array([[1, 0, 0],
                                  [0, self.cos_f, - self.sin_f],
                                  [0, self.sin_f, self.cos_f]])

        self.dict_of_objects_to_draw: SortedDict = SortedDict()

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

    def add_the_draw_element_to_sorted_dict(self, draw_object: ObjectToDraw):
        match draw_object.type_of_the_objects:
            case TypeOfTheObjects.point:
                self._add_to_dict_a_point(draw_object)
            case TypeOfTheObjects.text:
                self._add_to_dict_a_text(draw_object)
            case TypeOfTheObjects.light_line:
                self._add_to_dict_a_light_line(draw_object)
            case TypeOfTheObjects.line:
                self._add_to_dict_a_line(draw_object)
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
