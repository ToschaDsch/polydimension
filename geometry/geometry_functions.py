import math
from itertools import combinations
import numpy as np
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



def get_2d_coordinate_with_perspective(xyz: np.ndarray, diameter: float=400) -> np.ndarray:
    """
    Projects a 3D point (x, y, z) into 2D space,
    with perspective
    """
    return flat_perspective(xyz=xyz)
    return sphere_perspective(x=x, y=y, z=z)

def flat_perspective(xyz: np.ndarray) -> np.ndarray:
    a = -5
    xyz[2] += a
    if xyz[2] == 0:
        return np.array([400, 400, 0])
    return np.array([a*xyz[0]/xyz[2],
                     a*xyz[1]/xyz[2],
                     xyz[2]-a])

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

import numpy as np


def find_cycles(edges: list[tuple[int]], points: list[Point], cycle_size: int=5, eps=1e-9):
    """
    Find simple cycles of given size where vertices lie in a common 3D hyperplane in 4D space.

    Parameters
    ----------
    edges : array-like (N,2)
        Graph edges as vertex index pairs.

    points : array-like (M,)
        Each element must have attribute coord_0 (4D numpy array).

    cycle_size : int
        Number of vertices in cycle.

    eps : float
        Numerical tolerance.

    Returns
    -------
    list of tuples
        Each tuple contains Python int vertex indices forming a valid cycle.
    """

    edges = np.asarray(edges, dtype=np.int32)

    n_points = edges.max() + 1

    # -------------------------------------------------
    # Build adjacency list
    # -------------------------------------------------
    deg = np.zeros(n_points, dtype=np.int32)

    for a, b in edges:
        deg[a] += 1
        deg[b] += 1

    graph = [np.empty(deg[i], dtype=np.int32) for i in range(n_points)]
    fill = np.zeros(n_points, dtype=np.int32)

    for a, b in edges:
        graph[a][fill[a]] = b
        fill[a] += 1

        graph[b][fill[b]] = a
        fill[b] += 1

    # -------------------------------------------------
    # Extract 4D coordinates
    # -------------------------------------------------
    coords = np.array([list(p.coord_0) for p in points], dtype=np.float64)

    # -------------------------------------------------
    # Hyperplane coplanarity check in 4D
    # Rank of difference matrix must be <= 3
    # -------------------------------------------------
    def is_coplanar(indices):
        pts = coords[list(indices)]  # shape (cycle_size,4)
        base = pts[0]
        diffs = pts[1:] - base  # shape (cycle_size-1,4)
        rank = np.linalg.matrix_rank(diffs, tol=eps)
        return rank <= 3

    # -------------------------------------------------
    # DFS cycle search
    # -------------------------------------------------
    visited = np.zeros(n_points, dtype=np.bool_)
    path = np.empty(cycle_size, dtype=np.int32)

    cycles = []

    def dfs(start, current, depth):
        """
        Depth-first search recursive traversal.
        """

        if depth == cycle_size:

            # Check cycle closure
            for nxt in graph[current]:
                if nxt == start:
                    # remove reverse duplicates
                    if path[1] > path[cycle_size - 1]:
                        return
                    cycle = tuple(int(x) for x in path)
                    if is_coplanar(cycle):
                        cycles.append(cycle)
                    break
            return

        for nxt in graph[current]:

            if visited[nxt]:
                continue

            # Canonical ordering to avoid duplicate cycles
            if nxt < start:
                continue

            visited[nxt] = True
            path[depth] = nxt

            dfs(start, nxt, depth + 1)

            visited[nxt] = False

    # -------------------------------------------------
    # Main loop
    # -------------------------------------------------
    for start in range(n_points):

        visited[start] = True
        path[0] = start

        dfs(start, start, 1)

        visited[start] = False

    return cycles
