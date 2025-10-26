import math

import numpy as np

from geometry.class_point import Point


class MyCoordinates:
    dimensions: int = 4
    init_angle: float = math.pi / 3
    init_x: float = 0.0
    init_y: float = 0.0
    angles: np.ndarray = np.array([init_angle,init_angle,init_angle,0.0,0.0,0.0])
    displacement: np.ndarray = np.array([init_x,init_y,0.0,0.0])
    list_of_displacements: list[str] = ["x", "y", "z", "x1"]
    list_of_rotations: list[str] = ["x_y", "x_z", "x_x1", "y_z", "y_x1", "z_x1"]
    current_displacement: int = 0 # x
    current_rotation: int = 0 # xy
    angles_0: np.ndarray = np.array([init_angle, init_angle, init_angle, 0.0, 0.0, 0.0])
    displacement_0 = np.array([init_x,init_y,0.0,0.0])
    x0_y0: list[int] = [0,0] # init position of the mouse

class CoordinatesScreen:
    dx_dy: tuple[int, int] = 0, 0
    df_dj = 0, 0
    scale: float = 1
    init_size_of_the_object: int = 1

class Geometry:
    points: list[Point] = []

