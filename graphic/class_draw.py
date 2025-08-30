import math

from graphic.functions_for_class_draw.draw_from_draw_dict import draw_from_dict
from geometry.class_line import Line
from geometry.class_point import Point
from  geometry.class_geometry_change_point import GeometryChangePoint
from graphic.functions_for_class_draw.send_to_draw_dict import add_all_draw_objects_to_the_dict
from graphic.functions_for_screen_window import get_scale
from objects.class_draw_interface import NDimensionalObject
from objects.class_web import Line2dWeb
from variables.geometry_var import CoordinatesScreen
from variables.menus import Menus


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
        self._list_of_draw_objects: list[NDimensionalObject] = [web]
        self._list_of_draw_objects.extend(list_of_draw_objects) # there are the web and the object(s) to draw
        self._list_of_all_points: list[Point] = self._take_all_the_points(
            list_of_draw_objects=self._list_of_draw_objects) # take all the points of the objects,
        self._sin_f: float = 1
        self._cos_f: float = 0
        self._cos_j: float = 1
        self._sin_j: float = 0
        # initial vectors (coordinate)
        self._dimensions: int = initial_dimensions
        self._x0y0 = (int(Menus.screen_width * 0.5), int(Menus.screen_height * 0.5)) #initial center of the screen
        self._f0_j0 = (math.pi * 0.3, math.pi * 0.3)  # initial vector of rotation
        # current modifications of the coordinates
        self._dx_dy = (0, 0)        # vector of displacements
        self._df_dj = (0.0, 0.0)    # vector of rotation

        self._scale: float = 1

        # TODO correct the variables
        self.coordinate_0 = []
        self.coordinate_j = []
        self.coordinate_i = []
        self.corner_f: float = math.pi * 0.3
        self.corner_j: float = math.pi * 0.3
        self._x_c: int = 0
        self._y_c: int = 0
        self._z_c: int = 0

        self.init_points()      # set new center

        self._line_axes: list[Line] = self._make_lines_for_axes()

    def _make_lines_for_axes(self) -> list[Line]:
        list_of_axis: list[Line] = []
        coordinate_0 = [0]*self._dimensions
        point_0 = Point(coordinates=coordinate_0)
        for i in range(self._dimensions):
            coordinate_i = [0]*self._dimensions
            coordinate_i[i] = self._length_axes
            point_i = Point(coordinates=coordinate_i)
            list_of_axis.append(Line(point_0=point_0, point_1=point_i))
        return list_of_axis

    def _take_all_the_points(self, list_of_draw_objects: list[NDimensionalObject]) -> list[Point]:
        list_of_points: list[Point] = []
        # add points of all objects
        for draw_object in list_of_draw_objects:
            list_of_points.extend(draw_object.my_points)

        #add points of the axis
        for line_i in self._line_axes:
            list_of_points.append(line_i.point_1)
        # nul point
        list_of_points.append(self._line_axes[0].point_0)
        return list_of_points


    def init_points(self):
        if len(self._list_of_all_points) > 0:
            self.make_center()
            self.change_isometry()

    def by_reset_point_list(self):
        if len(self._list_of_all_points) > 0:
            self.make_center()
            self.change_isometry()
            self.first_scale()
            self.draw_all()

    def draw_all(self, dx_dy: tuple[int, int] = (0, 0), 
                 df_dj: tuple[int, int] = (0, 0)):
        self._dx_dy = dx_dy
        # correct all the points
        if self._df_dj != df_dj:
            self._df_dj = df_dj
            self.change_isometry()
        self._draw_on_the_canvas()

    def scale_change(self, ds: int, mouse_pos: tuple[int, int] = (0, 0)):
        # old_scale = self._scale
        # new_pos = (mouse_pos[0] - self._dx_dy[0] - self._xy_scale[0], mouse_pos[1] - self._dx_dy[1] - self._xy_scale[1])
        self._scale += ds * .03
        CoordinatesScreen.scale = self._scale
        if self._scale < 1:
            self._scale = 1

    def first_scale(self):
        self._scale = get_scale(list_of_point=self._list_of_all_points,
                                screen_height=Menus.screen_height,
                                screen_width=Menus.screen_width,)
        self.change_isometry()

    def change_isometry(self):
        corner_j = self._f0_j0[0] + self._df_dj[0]

        corner_f = self._f0_j0[1] + self._df_dj[1]

        self._geometry.change_corners(f=corner_f, j=corner_j, dx=self._x_c, dy=self._y_c, dz=self._z_c)

        # upgrade all points
        for point_i in self._list_of_all_points:
            self._geometry.rotate_and_shift_a_point(point=point_i)
        return None


    def make_center(self):
        #TODO correct it to make universal
        self._x_c = 0
        self._y_c = 0
        self._z_c = 0

    def end_of_shift(self):
        self._x0y0 = (self._x0y0[0] + self._dx_dy[0],
                      self._x0y0[1] + self._dx_dy[1],)
        self._dx_dy = (0, 0)

    def _draw_on_the_canvas(self):
        self._geometry.clean_dict_of_draw_objects()

        # draw the model
        add_all_draw_objects_to_the_dict(list_of_all_objects=self._list_of_draw_objects,
                                         geometry=self._geometry)
        draw_from_dict(dick_of_draw_objects=self._geometry.dict_of_objects_to_draw)

    def end_of_rotate(self):
        self._f0_j0 = (self._f0_j0[0] + self._df_dj[0],
                       self._f0_j0[1] + self._df_dj[1])
        self._df_dj = (0, 0)




