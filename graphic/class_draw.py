import math
from tkinter import Canvas

from graphic.functions_for_class_draw.draw_from_draw_dict import draw_from_dict
from graphic.functions_for_class_draw.send_to_draw_dict import shift_and_draw_on_the_canvas
from geometry.class_line import Line
from geometry.class_point import Point
from  geometry.class_geometry_change_point import GeometryChangePoint
from objects.class_draw_interface import DrawObject
from variables.menus import Menus


class DrawAll:
    """the class is a singleton to draw all object at the general canvas
    it calculates new coordinate(by rotate)
    sends all object to dict for draw (objects there are sorted by z coordinate) - modul send_to_draw_doct
    draws all object from the dict - modul draw_from_draw_dict"""

    def __init__(self, list_of_draw_objects: list[DrawObject],
                 initial_dimensions: int = 3,   #2d
                 canvas: Canvas = None):
        self._geometry: GeometryChangePoint = GeometryChangePoint()
        self._canvas: Canvas = canvas

        self._list_of_draw_objects: list[DrawObject] = list_of_draw_objects
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

        self._scale: float = 10

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
        self._length_axes = 1
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

    def _take_all_the_points(self, list_of_draw_objects: list[DrawObject]) -> list[Point]:
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
        if len(Geometry.points) > 0:
            self.make_center()
            self.change_isometry()
            self.first_scale()
            self.draw_all()

    def draw_all(self, dx_dy: () = (0, 0), df_dj: () = (0, 0)):
        self._dx_dy = dx_dy
        if self._df_dj != df_dj:
            self._df_dj = df_dj
            self.change_isometry()
        self._shift_and_draw_on_the_canvas()

    def scale_change(self, ds: int, mouse_pos: () = (0, 0)):
        # old_scale = self._scale
        # new_pos = (mouse_pos[0] - self._dx_dy[0] - self._xy_scale[0], mouse_pos[1] - self._dx_dy[1] - self._xy_scale[1])
        self._scale += ds * .03
        Geometry.scale = self._scale
        # print('old scale = ', self._scale)
        # print('new_pos = ', new_pos)
        if self._scale < 1:
            self._scale = 1
        # d = self._scale / old_scale

        # self._xy_scale = (self._dx_dy[0] - new_pos[0] * d * ds,
        #                  self._dx_dy[1] - new_pos[1] * d * ds)
        # self._xy_scale = (mouse_pos[0] * (self._scale - old_scale),
        #                  mouse_pos[1] * (self._scale - old_scale))
        # print('dx,dy = ', self._xy_scale)

    def first_scale(self):
        point_0: Point = list(Geometry.points.values())[0]
        x_max = point_0.coord_n[0]
        y_max = point_0.coord_n[1]
        x_min = point_0.coord_n[0]
        y_min = point_0.coord_n[1]
        for key, point in Geometry.points.items():
            if point.coord_n[0] > x_max:
                x_max = point.coord_n[0]
            elif point.coord_n[0] < x_min:
                x_min = point.coord_n[0]
            if point.coord_n[1] > y_max:
                y_max = point.coord_n[1]
            elif point.coord_n[1] < y_min:
                y_min = point.coord_n[1]
        max_value_x = max(abs(x_max), abs(x_min))
        max_value_y = max(abs(y_max), abs(y_min))
        if max_value_x == 0:
            scale_x = 1
        else:
            scale_x = (Variables.screen_BH[0] - 10) / max_value_x * 0.3
        if max_value_y == 0:
            scale_y = 1
        else:
            scale_y = (Variables.screen_BH[1] - 10) / max_value_y * 0.3
        self._scale = min(scale_x, scale_y)
        self.change_isometry()

    def change_isometry(self):
        corner_j = self._f0_j0[0] + self._df_dj[0]
        self._sin_j = math.sin(corner_j)
        self._cos_j = math.cos(corner_j)

        corner_f = self._f0_j0[1] + self._df_dj[1]
        self._sin_f = math.sin(corner_f)
        self._cos_f = math.cos(corner_f)

        self._geometry.change_corners(f=corner_f, j=corner_j, dx=self._x_c, dy=self._y_c, dz=self._z_c)

        for axes_i in self._line_axes:
            self._rotate_a_line(axes_i)

        # upgrade all points
        for point_i in self._list_of_all_points:
            self._rotate_a_point(point_i)
        return None

    def _rotate_a_line(self, line: Line):
        self._rotate_a_point(line.point_0)
        self._rotate_a_point(line.point_1)

    def make_center(self):
        #TODO correct it to make universal
        self._x_c = 0
        self._y_c = 0
        self._z_c = 0

    def end_of_shift(self):
        self._x0y0 = (self._x0y0[0] + self._dx_dy[0],
                      self._x0y0[1] + self._dx_dy[1],)
        self._dx_dy = (0, 0)

    def _shift_and_draw_on_the_canvas(self):
        self._geometry.clean_dict_of_draw_objects()
        # draw only the map
        if Geometry.show_elements:
            show_the_model(scale=self._scale, dx_dy=self._dx_dy, x0y0=self._x0y0)
            return None
        # draw the model
        self._calculate_all_points()

        shift_and_draw_on_the_canvas(geometry=self._geometry, line_axes=self._line_axes,
                                     scale=self._scale, dx_dy=self._dx_dy, x0y0=self._x0y0)
        draw_from_dict(geometry=self._geometry, scale=self._scale, dx_dy=self._dx_dy, x0y0=self._x0y0)
        Variables.animation_screen.draw_picked_frame()

    def end_of_rotate(self):
        self._f0_j0 = (self._f0_j0[0] + self._df_dj[0],
                       self._f0_j0[1] + self._df_dj[1])
        self._df_dj = (0, 0)

    def _rotate_a_point(self, point: Point):
        self._geometry.rotate_a_big_point(point=point)

    def _calculate_all_points(self):
        for key, point_i in Geometry.points.items():
            x0_y0: () = (
                -point_i.coord_n[0] * self._scale + self._dx_dy[0] + self._x0y0[0],
                point_i.coord_n[1] * self._scale + self._dx_dy[1] + self._x0y0[1])

            point_i.real_coordinate = x0_y0

        for axes_i in self._line_axes:
            point_0 = axes_i.point_0
            x0_y0: () = (
                -point_0.coord_n[0] * self._scale + self._dx_dy[0] + self._x0y0[0],
                point_0.coord_n[1] * self._scale + self._dx_dy[1] + self._x0y0[1])
            point_0.real_coordinate = x0_y0

            point_1 = axes_i.point_1
            x0_y0: () = (
                -point_1.coord_n[0] * self._scale + self._dx_dy[0] + self._x0y0[0],
                point_1.coord_n[1] * self._scale + self._dx_dy[1] + self._x0y0[1])
            point_1.real_coordinate = x0_y0

