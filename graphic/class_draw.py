from graphic.functions_for_class_draw.draw_from_draw_dict import draw_from_dict
from geometry.class_point import Point
from  geometry.class_geometry_change_point import GeometryChangePoint
from graphic.functions_for_class_draw.send_to_draw_dict import add_all_draw_objects_to_the_dict
from graphic.functions_for_screen_window import get_scale
from objects.class_axis import Axis
from objects.class_draw_interface import NDimensionalObject
from objects.class_web import Line2dWeb
from variables.geometry_var import CoordinatesScreen, MyCoordinates
from variables.menus import Menus
import numpy as np


class DrawAll:
    """the class is a singleton to draw all object at the general canvas
    it calculates new coordinate(by rotate)
    sends all object to dict for draw (objects there are sorted by z coordinate) - modul send_to_draw_doct
    draws all object from the dict - modul draw_from_draw_dict"""

    def __init__(self, list_of_draw_objects: list[NDimensionalObject],
                 initial_dimensions: int = 3,  #2d
                 n_web: int=10):
        """
        this is the general class to draw
        :param list_of_draw_objects: list[DrawObject], n-dimensional object to draw
        :param initial_dimensions: number of dimensions (3)
        :param n_web: number of cells in the web
        """
        # general variables
        self._length_axes = 1
        # a class to change coordinates of the objects
        self._geometry: GeometryChangePoint = GeometryChangePoint()
        web: NDimensionalObject = Line2dWeb(a=self._length_axes, n=n_web)
        axis: Axis = Axis(dimension=initial_dimensions)
        self._list_of_draw_objects: list[NDimensionalObject] = [web, axis]
        self._list_of_draw_objects.extend(list_of_draw_objects) # there are the web and the object(s) to draw
        self._list_of_all_points: list[Point] = self._take_all_the_points(
            list_of_draw_objects=self._list_of_draw_objects) # take all the points of the objects
        self._dimensions: int = initial_dimensions

        self._x_c: int = 0
        self._y_c: int = 0
        self._z_c: int = 0

        self.init_points()      # set new center

    def _take_all_the_points(self, list_of_draw_objects: list[NDimensionalObject]) -> list[Point]:
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

    def draw_all(self, angles: np.ndarray=None, dxi: np.ndarray=None):
        self.change_isometry(angles, dxi)
        self._draw_on_the_canvas()


    def first_scale(self) -> float:
        scale = get_scale(list_of_point=self._list_of_all_points,
                          screen_height=Menus.window_height,
                          screen_width=Menus.window_width)
        MyCoordinates.scale = scale
        print("scale", scale)
        return scale


    def change_isometry(self, angles:np.ndarray=None, dxi:np.ndarray=None):
        if angles is None and dxi is None:
            return None
        self._geometry.change_corners(angles=angles, dx=dxi)
        # upgrade all points
        for point_i in self._list_of_all_points:
            self._geometry.rotate_and_shift_a_point(point=point_i)
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
                                         geometry=self._geometry)
        print("dict length", len(self._list_of_draw_objects))
        draw_from_dict(dick_of_draw_objects=self._geometry.dict_of_objects_to_draw)





