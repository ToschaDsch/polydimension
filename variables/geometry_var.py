from geometry.class_point import Point


class MyCoordinates:
    dimensions: int = 4
    angles: list[int] = [1, 2, 3, 4, 4, 5, 6]
    displacement: list[int] = [1, 2, 3, 4]
    list_of_displacements: list[str] = ["x", "y", "z", "x1"]
    list_of_rotations: list[str] = ["x_y", "x_z", "x_x1", "y_z", "y_x1", "z_x1"]
    current_displacement: int = 0 # x
    current_rotation: int = 0 # xy

class CoordinatesScreen:
    dx_dy: tuple[int, int] = 0, 0
    df_dj = 0, 0
    scale: float = 1
    init_size_of_the_object: int = 1

class Geometry:
    points: list[Point] = []

