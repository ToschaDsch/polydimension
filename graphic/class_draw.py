from typing import Literal

from graphic.functions_for_class_draw.draw_from_draw_dict import draw_from_dict
from geometry.class_point import Point
from  geometry.class_geometry_change_point import GeometryChangePoint
from graphic.functions_for_class_draw.send_to_draw_dict import add_all_draw_objects_to_the_dict
from graphic.functions_for_screen_window import get_scale
from objects.class_axis import Axis
from objects.class_draw_interface import NDimensionalObject
from objects.class_web import Line2dWeb
from variables.geometry_var import CoordinatesScreen
from variables.graphics import Transparency
from variables.menus import Menus
import numpy as np


class DrawAll:
    """the class is a singleton to draw all object at the general canvas
    it calculates new coordinate(by rotate)
    sends all object to dict for draw (objects there are sorted by z coordinate) - modul send_to_draw_doct
    draws all object from the dict - modul draw_from_draw_dict"""

    def __init__(self, draw_object: NDimensionalObject,
                 initial_dimensions: int = 3,  #2d
                 n_web: int=10):
        """
        this is the general class to draw
        :param list_of_draw_objects: list[DrawObject], n-dimensional object to draw
        :param initial_dimensions: number of dimensions (3)
        :param n_web: number of cells in the web
        """
        # general variables
        self._length_axes = 4
        # a class to change coordinates of the objects
        self._geometry: GeometryChangePoint = GeometryChangePoint()
        z = draw_object.z_min
        web: NDimensionalObject = Line2dWeb(a=self._length_axes, n=n_web, z=z)
        axis: Axis = Axis(dimension=initial_dimensions)
        self._list_of_draw_objects: list[NDimensionalObject] = [web, axis, draw_object]
        self._list_of_all_points: list[Point] = self._take_all_the_points(
            list_of_draw_objects=self._list_of_draw_objects) # take all the points of the objects
        self._dimensions: int = initial_dimensions

        self._x_c: int = 0
        self._y_c: int = 0
        self._z_c: int = 0

        # draw options
        self._transparency: Literal[Transparency.transparent] = Transparency.transparent
        self._perspective: bool = False

        self.init_points()      # set new center

    @property
    def perspective(self):
        return self._perspective

    @perspective.setter
    def perspective(self, value: bool):
        self._perspective = value
        self._geometry.draw_with_perspective = value
        self.draw_all()

    @property
    def transparency(self) -> Literal[Transparency.transparent]:
        return self._transparency

    @transparency.setter
    def transparency(self, transparency: int):
        self._transparency = transparency
        for draw_object in self._list_of_draw_objects:
            draw_object.transparent = transparency
        self.draw_all()


    @staticmethod
    def _take_all_the_points(list_of_draw_objects: list[NDimensionalObject]) -> list[Point]:
        list_of_points: list[Point] = []
        # add points of all objects
        for draw_object in list_of_draw_objects:
            list_of_points.extend(draw_object.my_points)

        return list_of_points


    def init_points(self):
        self.by_reset_point_list()

    def by_reset_point_list(self):
        if len(self._list_of_all_points) > 0:
            self.make_center()
            self.change_isometry()
            new_scale = self.first_scale()
            self._geometry.scale=new_scale
            self.change_isometry()  # with new scale
            self.draw_all()

    def draw_all(self, angles: np.ndarray=None, dxi: np.ndarray=None, scale:float=None):
        self.change_isometry(angles=angles, dxi=dxi, scale=scale)
        self._draw_on_the_canvas()


    def first_scale(self) -> float:
        scale = get_scale(list_of_point=self._list_of_all_points,
                          screen_height=Menus.window_height,
                          screen_width=Menus.window_width)
        CoordinatesScreen.scale = scale

        return scale


    def change_isometry(self, angles:np.ndarray=None, dxi:np.ndarray=None, scale: float=None):
        if angles is None and dxi is None and scale is None:
            return None
        self._geometry.calculate_new_coordinates_for_the_list_of_points(angles=angles,dx=dxi,
                                                                        points=self._list_of_all_points,
                                                                        scale=scale)
        return None

    def make_center(self):
        #TODO correct it to make universal
        self._x_c = 0
        self._y_c = 0
        self._z_c = 0


    def _draw_on_the_canvas(self):
        self._geometry.clean_dict_of_draw_objects()

        # draw the model
        add_all_draw_objects_to_the_dict(list_of_all_objects=self._list_of_draw_objects,
                                         geometry=self._geometry, transparency=self._transparency)
        draw_from_dict(dick_of_draw_objects=self._geometry.dict_of_objects_to_draw)






