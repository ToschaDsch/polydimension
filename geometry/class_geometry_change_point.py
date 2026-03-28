import math

import numpy as np
from sortedcontainers import SortedDict

from frontend.event_bus.decorators import timer
from geometry.class_geometric_object import GeometricObject
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.class_volume import Volume
from geometry.geometry_functions import get_rotate_matrix, get_2d_coordinate_with_perspective
from variables.menus import Menus


class  GeometryChangePoint:
    """the class is a singleton
    it calculates new coordinate for the object and send it to a dict
    """
    corner_init: float = math.pi * 0.25

    def __init__(self, init_scale: float):
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

        self.scale: float = init_scale

        self.dict_of_objects_to_draw: SortedDict = SortedDict()
        self.draw_with_perspective: bool = True

    @timer
    def _change_corners(self):
        self.sin: list[float] = [math.sin(x) for x in self.angles]
        self.cos: list[float] = [math.cos(x) for x in self.angles]

        self.rotation_matrix: np.ndarray = get_rotate_matrix(sin=self.sin,
                                                             cos=self.cos,
                                                             dimensional=self.dimensional)


    def calculate_new_coordinates_for_the_list_of_points(self, angles: np.ndarray=None, dx: np.ndarray=None,
                                                         points: list[Point]=None, scale: float=None):
        if angles is not None:
            self.angles = angles
        if dx is not None:
            self.dxi = np.asarray(dx, dtype=float)[:3]
        if scale is not None:
            self.scale = scale
        self._change_corners()
        self.dict_of_objects_to_draw.clear() #clear the dict
        self.rotate_all_points(points)


    def rotate_all_points(self, points: list[Point]):
        for point in points:
            self._rotate_and_shift_a_point(point=point)

    def _rotate_and_shift_a_point(self, point: Point):
        coord_0 = np.asarray(point.coord_0)  # fast, no unnecessary stacking
        # matrix multiplication
        x0_y0 = self.rotation_matrix @ coord_0
        # store rotated only (no resize)
        point.coord_only_rotate = x0_y0.copy()
        # perspective transform (if needed)
        if self.draw_with_perspective:
            x0_y0 = get_2d_coordinate_with_perspective(xyz=x0_y0)
        # final transform (avoid resize)
        point.coord_n = x0_y0 * self.scale + self.x0y0 + self.dxi

    def clean_dict_of_draw_objects(self):
        self.dict_of_objects_to_draw.clear()

    def add_the_draw_element_to_sorted_dict(self, draw_object: GeometricObject|Point):
        if isinstance(draw_object, Point):
            z = draw_object.coord_n[2]
        elif isinstance(draw_object, Line):
            z = 0.5 * (draw_object.point_0.coord_n[2] +
                       draw_object.point_1.coord_n[2])
        elif isinstance(draw_object, (Surface, Volume)):
            center = draw_object.get_center()
            z = center.coord_n[2]
            if isinstance(draw_object, Volume):
                surfaces = get_all_unic_surfaces_from_a_volume(
                    draw_object.list_of_surfaces
                )
                for surface in surfaces:
                    self.add_the_draw_element_to_sorted_dict(surface)

        else:
            z = 0.0
        self._add_an_object_to_the_dict(draw_object=draw_object, z=z)


    def _add_an_object_to_the_dict(self, z: float, draw_object: GeometricObject|Point):
        while z in self.dict_of_objects_to_draw:
            z += 1e-7
        self.dict_of_objects_to_draw[z] = draw_object

def get_all_unic_surfaces_from_a_volume(list_of_surfaces: list[Surface]) -> list[Surface]:
    surfaces = []
    for surface in list_of_surfaces:
        pass
    return list_of_surfaces