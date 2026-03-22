import math

from frontend.event_bus.event_bus import EventBus
from frontend.event_bus.events import ShiftTheSliderRotation, ShiftTheSliderDisplacement, \
    RecalculateAndDrawAllPrimitives
from geometry.class_point import Point
from variables.class_state import MyState


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

def shift(state: MyState, x: int, y: int):
    state.MyCoordinates.displacement[0] = state.MyCoordinates.displacement[0] + x
    state.MyCoordinates.displacement[1] = state.MyCoordinates.displacement[1] + y


def rotate_the_object(state: MyState, x: int, y: int, bus: EventBus):
    old_number_of_rotation = state.MyCoordinates.current_rotation
    dxy = [x - state.MyCoordinates.x0_y0[0],y - state.MyCoordinates.x0_y0[1]]
    order = {0:dxy[0], 2:dxy[1]}
    for ni, di in order.items():  # xy, xz angles
        state.MyCoordinates.current_rotation = ni
        rotation = int(-di + state.MyCoordinates.angles[ni]/math.pi*180)  #   in grad
        if old_number_of_rotation == ni:    # if the slider is current - move the slider
            bus.publish(ShiftTheSliderRotation(angle=rotation))
            continue
        current_rotation_changed(rotations=int(rotation), bus=bus, state=state)    # in Rad
    state.MyCoordinates.current_rotation = old_number_of_rotation
    state.MyCoordinates.x0_y0 = [x, y]


def shift_the_object(state: MyState, x: int, y: int, bus: EventBus):
    old_number_of_displacement = state.MyCoordinates.current_displacement
    for ni, di in enumerate([x, y]):    # x, y coordinates
        state.MyCoordinates.current_displacement = ni
        displacement = int(di + state.MyCoordinates.displacement[ni] - state.MyCoordinates.x0_y0[ni])

        if old_number_of_displacement == ni:    # if the slider is current - move the slider
            bus.publish(ShiftTheSliderDisplacement(shift=displacement))
            continue
        current_displacement_changed(displacement=int(displacement), bus=bus, state=state)
    state.MyCoordinates.current_displacement = old_number_of_displacement
    state.MyCoordinates.x0_y0 = [x, y]


def left_release(state: MyState, x: int, y: int):
    pass

def right_release(state: MyState, x: int, y: int):
    pass

def start_shift(state: MyState, x: int, y: int):
    """first click of the left button"""
    state.MyCoordinates.x0_y0 = [x, y]

def start_to_rotate(state: MyState, x:  int, y: int):
    """first click of the right button"""
    state.MyCoordinates.x0_y0 = [x, y]

def current_displacement_changed(state: MyState, bus:EventBus, displacement: int = 0) -> None:
    state.MyCoordinates.displacement[state.MyCoordinates.current_displacement] = displacement
    bus.publish(RecalculateAndDrawAllPrimitives(dxi=state.MyCoordinates.displacement))

def current_rotation_changed(state: MyState, bus:EventBus, rotations: int = 0) -> None:
    """
    :param state:
    :param bus:
    :param rotations: angle in grad -180 +180:
    :return None:
    """
    state.MyCoordinates.angles[state.MyCoordinates.current_rotation] = rotations * math.pi / 180
    bus.publish(RecalculateAndDrawAllPrimitives(angles=state.MyCoordinates.angles))