import math

from geometry.class_point import Point
from menus.single_functions import current_displacement_changed, current_rotation_changed
from variables.geometry_var import MyCoordinates
from variables.menus import Menus


def get_scale(list_of_point: list[Point],
              screen_width: int,
              screen_height: int) -> float:
    point_0: Point = list_of_point[0]
    x_max = point_0.coord_n[0]
    y_max = point_0.coord_n[1]
    x_min = point_0.coord_n[0]
    y_min = point_0.coord_n[1]
    for point in list_of_point:
        if point.coord_n[0] > x_max:
            x_max = point.coord_n[0]
        elif point.coord_n[0]< x_min:
            x_min = point.coord_n[0]
        if point.coord_n[1] > y_max:
            y_max = point.coord_n[1]
        elif point.coord_n[1] < y_min:
            y_min = point.coord_n[1]
    max_value_x = x_max - x_min
    max_value_y = y_max - y_min
    if max_value_x == 0:
        scale_x = 1
    else:
        scale_x = (screen_width - 10) / max_value_x * 0.3
    if max_value_y == 0:
        scale_y = 1
    else:
        scale_y = (screen_height - 10) / max_value_y * 0.3
    return min(scale_x, scale_y)

def shift(x: int, y: int):
    MyCoordinates.displacement[0] = MyCoordinates.displacement[0] + x
    MyCoordinates.displacement[1] = MyCoordinates.displacement[1] + y



def rotate_the_object(x: int, y: int):
    y = -y
    for ni, di in enumerate([x, y]):  # xy, xz angles
        MyCoordinates.current_rotation = ni
        rotation = di + MyCoordinates.angles[ni] - MyCoordinates.x0_y0[ni]*math.pi/180
        current_rotation_changed(rotations=rotation)
    """
    Geometry.df_dj = (Geometry.df_dj[0] + (x - Geometry.x0y0[0]) * 0.01,
                      Geometry.df_dj[1] - (y - Geometry.x0y0[1]) * 0.01)
    Geometry.x0y0 = x, y
    """
    MyCoordinates.x0_y0 = x, y


def shift_the_object(x: int, y: int):
    old_number_of_displacement = MyCoordinates.current_displacement
    for ni, di in enumerate([x, y]):    # x, y coordinates

        MyCoordinates.current_displacement = ni
        displacement = di + MyCoordinates.displacement[ni] - MyCoordinates.x0_y0[ni]

        if old_number_of_displacement == ni:    # if the slider is current - move the slider
            Menus.general_window.shift_the_slider_displacement(shift=displacement)
            continue
        current_displacement_changed(displacement=displacement)
    MyCoordinates.current_displacement = old_number_of_displacement
    MyCoordinates.x0_y0 = x, y


def left_release(x: int, y: int):
    pass

def right_release(x: int, y: int):
    pass

def start_shift(x: int, y: int):
    """first click of the left button"""
    MyCoordinates.x0_y0 = (x, y)

def start_to_rotate(x: int, y: int):
    """first click of the right button"""
    MyCoordinates.x0_y0 = (x, y)