from dataclasses import dataclass
from typing import Any

import numpy as np
from PySide6.QtGui import QColor
from numpy import ndarray

from geometry.class_geometric_object import GeometricObject
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_source_of_light import SourceOfLight
from geometry.geometry_functions import get_center_from_list_of_points
from variables.graphics import MyColors


class Surface(GeometricObject):
    def get_center(self) -> Point:
        return self.center

    def get_all_points(self) -> list[Point]:
        return self._list_of_points

    def get_color(self) -> QColor:
        return self.color

    def __init__(self, list_of_points: list[Point] = None, color: QColor = None, width: int = None,
                 source_of_light: SourceOfLight = None, init_center_of_the_volume: Point = None):
        color = color if color else QColor(*MyColors.default_surface_color)
        super().__init__(color=color, width=width)
        self._list_of_points: list[Point] = list_of_points if list_of_points is not None else []
        self.list_of_lines: list[Line] = []
        self.make_lines()
        self.dimension: int = list_of_points[0].dimension
        self.center = get_center_from_list_of_points(list_of_points=self._list_of_points)
        init_center_of_the_volume = init_center_of_the_volume if init_center_of_the_volume else Point()
        self.normal: Point = self.get_coordinate_of_the_normal(init_center_of_the_volume = init_center_of_the_volume)
        self._init_color = color
        self._source_of_light: SourceOfLight = source_of_light if source_of_light else SourceOfLight()

        return_color = self.give_me_return_color(points=self._list_of_points, center_of_the_volume=init_center_of_the_volume,
                                                 color=self._init_color,
                                                 lamp=self._source_of_light)
        self.color = return_color.color
        self.visible = return_color.i_see_it
        self.draw_with_normal = True
        self.normal.coord_0 = np.resize(self.normal.coord_0, (len(self.center.coord_0)))
        self.normal_line = Line(point_0=self.center, point_1=self.normal)
        
    def get_coordinate_of_the_normal(self, init_center_of_the_volume: Point) -> Point:
        coordinates = calculate_normal(points=self._list_of_points, vector_center=init_center_of_the_volume.coord_0)
        return Point(coordinates=coordinates)



    def change_coordinate(self):
        pass

    def make_lines(self):
        for i in range(len(self._list_of_points)-1):
            self.list_of_lines.append(Line(point_0=self._list_of_points[i],
                                           point_1=self._list_of_points[i+1], color=self._color))
        self.list_of_lines.append(Line(point_0=self._list_of_points[0],
                                       point_1=self.list_of_points[-1], color=self.color)) # closing the path

    @property
    def list_of_points(self) -> list[Point]:
        return self._list_of_points

    @list_of_points.setter
    def list_of_points(self, list_of_points: list[Point]):
        self._list_of_points = list_of_points


    def give_me_return_color(self, points: list[Point],
                             center_of_the_volume: Point,
                             color: "QColor",
                             lamp: SourceOfLight = None,
                             draw_with_perspective: bool = False) -> "ReturnColor":
        if color is None:
            color = self.color

        vector_of_distance, square_of_distance = calculate_vector_and_square_of_distance(points=points)
        distance3d: float = 0.0

        vector_center = vector_of_distance - center_of_the_volume.coord_0


        vector_from_lamp, distance_from_lamp = calculate_lamp(vector_of_distance=vector_of_distance,
                                                              lamp_coord=lamp.coordinate.coord_n)

        # if (distanceFromLamp > lamp.intensity) { // in dark } -- original commented out

        if draw_with_perspective:
            vector_of_distance = normalize_me_in_3d(vector_of_distance)
        else:
            vector_of_distance = [0.0, 1.0, 0.0]

        i_see_it = cos_between_two_vectors(self.normal.coord_0, vector_of_distance) < 0.0

        vector_from_lamp = normalize_me_in_3d(vector_from_lamp)

        angle = cos_between_two_vectors(self.normal.coord_0, vector_from_lamp)
        new_color = make_color(angle0=angle, distance=distance3d, color=color)
        return ReturnColor(color=new_color, i_see_it=i_see_it, distance=square_of_distance)

@dataclass
class ReturnColor:
    color: "QColor"
    i_see_it: bool
    distance: float

def vector_product_with_center(v1: np.ndarray, v2: np.ndarray, vector_center: np.ndarray) -> np.ndarray:
    """
    the function checks where is the center and returns normal of the surface
    """
    v1_=np.resize(v1, 3,)
    v2_=np.resize(v2, 3,)
    vector_center=np.resize(vector_center,3,)
    vector_product = np.cross(v1_, v2_)
    if vector_product.dot(vector_center) > 0.0:
        return vector_product
    else:
        return np.cross(v2_, v1_)

def calculate_vector_and_square_of_distance(points: list[Point]) -> tuple[np.ndarray, float]:
    """
    the function calculates a vector to the center of the surface and average square of distance to the surface
    from center of coordinate
    """
    h = len(points[0].coord_n)
    vector_distance: np.ndarray = np.empty((h,))
    square_of_length = 0.0
    a = 1.0 / len(points)

    for i in range(h):
        for point in points:
            vector_distance[i] += point.coord_n[i] * a  # x
        square_of_length += vector_distance[i] * vector_distance[i]
    return vector_distance, square_of_length

def calculate_normal(points: list[Point], vector_center: np.ndarray) -> np.ndarray:
    """
    the function takes coordinate of surfaces edge and calculate normal to the surface
    """
    v1: np.ndarray = points[1].coord_n - points[0].coord_n  # dx //vector v1 (point 1 - point 0)
    v2: np.ndarray = points[2].coord_n - points[1].coord_n  # dx //vector v2 (point 2 - point 1)
    np.resize(v1, (3,))
    np.resize(v2, (3,))
    normal = vector_product_with_center(v1=v1, v2=v2, vector_center=vector_center)

    length = np.sqrt(normal.dot(normal))

    a = 1.0 / length if length != 0.0 else 1.0
    return normal*a

def calculate_lamp(vector_of_distance: np.ndarray, lamp_coord: np.ndarray) -> tuple[np.ndarray, float]:
    """
    the function returns not normalized vector of lamp - the point
    and the distance between
    """
    vector_from_lamp = lamp_coord - np.resize(vector_of_distance, (3,),)
    # Kotlin had sqrt(...) commented out and set distanceFromLamp = 1f
    distance_from_lamp = 1.0
    return vector_from_lamp, distance_from_lamp

def normalize_me_in_3d(vector: np.ndarray, distance0: float = 0.0) -> np.ndarray:
    """
    the function normalizes a vector in 3d dimension
    """
    if distance0 == 0.0:
        vector_3d = np.resize(vector, (3,))
        distance = np.sqrt(vector_3d.dot(vector_3d))
    else:
        distance = distance0

    a = 1.0 if distance == 0.0 else 1.0 / distance

    return vector * a

def cos_between_two_vectors(normal: np.ndarray, vector_of_distance: np.ndarray) -> float:
    """the function returns 3d scalar product"""
    return np.dot(normal, vector_of_distance)

def make_color(angle0: float, distance: float, color: "QColor" = None) -> QColor:
    if color is None:
        return QColor(100,100,0)
    dispersion_of_light = 0.5
    # val add = (1f - Properties.DISPERSION_OF_LIGHT) + abs(angle0) * Properties.DISPERSION_OF_LIGHT
    add = (1.0 - dispersion_of_light) + abs(angle0) * dispersion_of_light

    if (add > 0.0) and (add < 1.0):
        # return Color(color.red * add, color.green * add, color.blue * add)
        return QColor(*[color.redF()* add, color.green() * add, color.blue() * add])
    else:
        return color