import math
from itertools import combinations

import numpy as np

from geometry.class_line import Line
from geometry.class_point import Point


def get_center_from_list_of_points(list_of_points: list[Point]) -> Point:
    array_1 = np.array([x.coord_0 for x in list_of_points])
    coordinate_of_the_center = np.sum(array_1, axis=0)/len(list_of_points)
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
        return np.array([400, 400, 0])
    return np.array([a*x/z,
                     a*y/z,
                     z-a])

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


def space_between_two_points(point_0: Point, point_1: Point) -> float:
        coord: np.ndarray = np.subtract(point_1.coord_0, point_0.coord_0)
        return np.sqrt(np.dot(coord, coord))


def find_closed_contours_from_lines(lines: list[list[int]], how_lines_in_the_surface: int = 3) -> list[tuple[int, int, int]]:
    """the function finds all the surfaces in the given lines
    how_lines_in_the_surface = 2 for triangles
    return numbers of points of the contour lines
    """
    surfaces = []

    for l1, l2, l3 in combinations(lines, how_lines_in_the_surface):
        # set of all points
        points = {
            l1[0], l1[1],
            l2[0], l2[1],
            l3[0], l3[1]
        }

        # a triangle have only 3 points/ check
        if len(points) != 3:
            continue

        # check degree for all points/ double-check
        degree = {p: 0 for p in points}

        for line in (l1, l2, l3):
            degree[line[0]] += 1
            degree[line[1]] += 1

        if all(d == 2 for d in degree.values()):
            surfaces.append((l1, l2, l3))

    # make a list of points from lists of lines
    numbers_of_points = []
    for number_of_lines_i in surfaces:
        set_of_point_i = set()
        for line_i in number_of_lines_i:
            set_of_point_i.add(line_i[0])
            set_of_point_i.add(line_i[1])
        numbers_of_points.append(list(set_of_point_i))
    return numbers_of_points

def find_lines(points: list[Point], length: float = 1.0) -> list[set[int]]:
    """the function finds all the lines in the given points with length = length"""
    l_0 = length*0.99
    l_1 = length*1.01
    number_of_points = []
    for (i, p1), (j, p2) in combinations(enumerate(points), 2):
        if l_0 < space_between_two_points(point_0=p1, point_1=p2) < l_1:
            set_l = {i, j}
            if set_l not in number_of_points:
                number_of_points.append(set_l)
    return number_of_points