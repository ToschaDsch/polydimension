import math

import numpy as np

from geometry.class_point import Point


def get_center_from_list_of_points(list_of_points: list[Point]) -> Point:
    dimension = list_of_points[0].dimension
    summ_vector = np.zeros((dimension,), float)
    for point in list_of_points:
        summ_vector += point.coord_0
    coordinate_of_the_center = summ_vector / len(list_of_points)
    return Point(coordinates=coordinate_of_the_center)

def get_rotate_matrix(sin: list[float], cos: list[float], dimensional: int = 3) -> np.ndarray:
    """
    :param sin: list of sin a, b, g
    :param cos: list of cos a, b, g
    :param dimensional: 3d, 4d
    :return: rotate matrix. for 3d -> Ra*Rb*Rg
    """
    r = []
    if dimensional == 3:
        r.append(np.array([[cos[0], -sin[0], 0],
                         [sin[0], cos[0], 0],
                         [0, 0, 1]
                         ]))
        r.append(np.array([[cos[1], 0, sin[1]],
                         [0, 1, 0],
                         [-sin[1], 0, cos[1]]
                         ]))
        r.append(np.array([[1, 0, 0],
                         [0, cos[2], -sin[2]],
                         [0, sin[2], cos[2]]
                         ]))
    elif dimensional == 4:
        n = 0
        order = [(0,1), (0, 2), (1,2), (1,3), (2,3), (0, 3)]
        for i, j in order:
            r.append(rotation_matrix_4d(axis_1=i, axis_2=j, sin_i=sin[n], cos_i=cos[n]))
            n+=1

    result_matrix = np.identity(dimensional, dtype=np.float64)

    for r_i in r:
        result_matrix = np.dot(r_i, result_matrix)
    return result_matrix

def rotation_matrix_4d(axis_1: int, axis_2: int, cos_i: float, sin_i: float) -> np.ndarray:
    """
    Create a 4x4 rotation matrix in 4D space for rotation in the plane (axis1, axis2).
    axis1, axis2 ∈ {0, 1, 2, 3} correspond to x, y, z, w.
    cos_i, sin_i - in plane axis_1, axis_2
    """
    r = np.eye(4)
    r[axis_1, axis_1] = cos_i
    r[axis_1, axis_2] = -sin_i
    r[axis_2, axis_1] = sin_i
    r[axis_2, axis_2] = cos_i
    return r



def get_2d_coordinate_with_perspective(x: float, y: float, z: float, diameter: float=400) -> np.ndarray:
    """
    Projects a 3D point (x, y, z) into 2D space,
    with perspective
    """
    return flat_perspective(x, y, z)
    return sphere_perspective(x=x, y=y, z=z)

def flat_perspective(x: float, y: float, z: float) -> np.ndarray:
    a = -5
    z += a
    if z == 0:
        return np.array([400, 400])
    return np.array([a*x/z,
                     a*y/z])

def sphere_perspective(x: float, y: float, z: float, diameter: float=400) -> np.ndarray:
    max_l = diameter * 10000.0
    # y *=-1    back perspective
    z-=25

    try:
        # Perspective projection
        if math.fabs(z) <= 0.0001:
            l = diameter * math.atan(math.sqrt(y * y + x * x) * 100000.0)
        else:
            l = diameter * math.atan(math.sqrt(y * y + x * x) / z)

        if -0.0001 < y < 0.0001:
            alpha = math.atan(x * 10000.0) % (2.0 * math.pi)
        else:
            alpha = math.atan(x / y) % (2.0 * math.pi)

        if l > max_l:
            if y >= 0:
                return np.array([max_l, max_l])
            else:
                return np.array([-max_l, -max_l])
        else:
            k = 1
            if y >= 0:
                return np.array([
                    + k*l * math.sin(alpha),
                    - k*l * math.cos(alpha)
                ])
            else:
                return np.array([
                    - k*l * math.sin(alpha),
                    + k*l * math.cos(alpha)
                ])
    except Exception as err:
        raise("TransformTo2D, Arithmetic exception", err)
