import math
from itertools import chain

import numpy as np
from numpy.typing import NDArray

from geometry.class_point import Point


def get_center_from_list_of_points(list_of_points: list[Point]) -> NDArray[np.float64]:
    array_1 = np.array([x.coord_0 for x in list_of_points])
    coordinate_of_the_center = np.sum(array_1, axis=0)/len(list_of_points)
    return coordinate_of_the_center

def get_rotate_matrix(sin: list[float], cos: list[float], dimension: int = 3) -> np.ndarray[np.float64]:
    """
    :param sin: list of sin a, b, g
    :param cos: list of cos a, b, g
    :param dimension: 3d, 4d
    :return: rotate matrix. for 3d -> Ra*Rb*Rg
    """
    # Start with the identity matrix of the given dimensionality
    result_matrix = np.identity(dimension, dtype=np.float64)

    if dimension == 3:
        result_matrix = np.array([
            [[cos[0], -sin[0], 0],
             [sin[0], cos[0], 0],
             [0, 0, 1]],

            [[cos[1], 0, sin[1]],
             [0, 1, 0],
             [-sin[1], 0, cos[1]]],

            [[1, 0, 0],
             [0, cos[2], -sin[2]],
             [0, sin[2], cos[2]]]
        ], dtype=np.float64)
    elif dimension == 4:
        # Pairs of axes for 4D rotations
        order = [(0,1), (0,2), (1,2), (1,3), (2,3), (0,3)]

        # Create an array of rotation matrices
        # Shape: (number_of_rotations, dimensional, dimensional)
        r = np.array([
            rotation_matrix_4d(axis_1=i, axis_2=j, sin_i=sin[n], cos_i=cos[n])
            for n, (i, j) in enumerate(order)
        ], dtype=np.float64)

        # Multiply all rotation matrices in sequence
        for r_i in r:
            result_matrix = r_i @ result_matrix  # np.dot could also be used
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



def get_2d_coordinate_with_perspective(xyz: NDArray[np.float64], diameter: float=400) -> NDArray:
    """
    Projects a 3D point (x, y, z) into 2D space,
    with perspective
    """
    return flat_perspective(xyz=xyz)
    return sphere_perspective(x=x, y=y, z=z)

def flat_perspective(xyz: NDArray[np.float64]) -> NDArray:
    a = -5.0
    x, y, z, w = xyz  # unpack once
    z_shifted = z + a
    # avoid division instability
    if abs(z_shifted) < 1e-9:
        return np.array([400.0, 400.0, 0.0], dtype=np.float64)
    factor = a / z_shifted
    return np.array([
        x * factor,
        y * factor,
        z_shifted - a
    ], dtype=np.float64)

import numpy as np
from numpy.typing import NDArray

def flat_perspective_ndarray(xyz: NDArray[np.float64]) -> NDArray[np.float64]:
    """
    Apply flat perspective projection to an array of points in vectorized form.

    Parameters
    ----------
    xyz : NDArray[np.float64]
        Input array of shape (N, 4), each row is [x, y, z, w].

    Returns
    -------
    NDArray[np.float64]
        Projected points array of shape (N, 3).
    """
    a = -5.0
    xyz = np.asarray(xyz, dtype=np.float64)  # ensure float64
    z_shifted = xyz[:, 2] + a  # column z + shift

    # Projection factor, safely avoiding division by zero
    factor = np.where(np.abs(z_shifted) < 1e-9, 0.0, a / z_shifted)

    # Compute projected coordinates
    proj = np.empty((xyz.shape[0], 3), dtype=np.float64)
    proj[:, 0] = xyz[:, 0] * factor  # x
    proj[:, 1] = xyz[:, 1] * factor  # y
    proj[:, 2] = z_shifted           # z_shifted - a = (z + a) - a = z? keep original
    proj[:, 2] -= a                  # z component after perspective

    return proj

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


def find_cycles(edges: list[list[int]], points: list[Point], cycle_size: int=5, eps=1e-9):
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


def point_key(p):
    return tuple(np.round(p.coord_0, 8))



def find_surfaces(lines):
    # --- 1. граф смежности ---
    graph = {}
    for a, b in lines:
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)

    surfaces = set()

    # --- 2. поиск циклов длины 5 ---
    def dfs(path, start):
        if len(path) == 5:
            # проверяем замыкание
            if start in graph[path[-1]]:
                cycle = path[:]

                # каноническая форма (убираем дубликаты)
                min_idx = min(range(5), key=lambda i: cycle[i])
                cycle = cycle[min_idx:] + cycle[:min_idx]

                # ещё нужно учесть обратный обход
                rev = list(reversed(cycle))
                min_idx_rev = min(range(5), key=lambda i: rev[i])
                rev = rev[min_idx_rev:] + rev[:min_idx_rev]

                surfaces.add(tuple(min(cycle, rev)))
            return

        last = path[-1]

        for nxt in graph[last]:
            if nxt in path:
                continue
            dfs(path + [nxt], start)

    # --- 3. запускаем ---
    for v in graph:
        dfs([v], v)

    return [list(s) for s in surfaces]


def extract_volumes(surfaces, lines=None):
    # Преобразуем каждый surface в set заранее
    surfaces_sets = [set(surface) for surface in surfaces]
    n = 0
    cells = []
    for idx_combo in combinations(range(len(surfaces)), 12):
        # объединяем все точки из выбранных 12 поверхностей
        combined_points = set(chain.from_iterable(surfaces_sets[i] for i in idx_combo))

        if len(combined_points) == 20:
            # сохраняем не индексы, а сами поверхности
            cells.append([surfaces[i] for i in idx_combo])
            n+=1
            print(n)

    return cells

from itertools import combinations

def extract_volumes_fast(lines, surfaces):
    # --- 1. нормализация рёбер ---
    def normalize_edge(a, b):
        return (a, b) if a < b else (b, a)

    lines_set = set(normalize_edge(a, b) for a, b in lines)
    edge_index = {e: i for i, e in enumerate(lines_set)}
    num_edges = len(edge_index)

    # --- 2. поверхности → рёбра ---
    surface_edges = []
    for surf in surfaces:
        n = len(surf)
        edges = []
        for i in range(n):
            a = surf[i]
            b = surf[(i + 1) % n]
            e = normalize_edge(a, b)
            edges.append(edge_index[e])
        surface_edges.append(edges)

    # --- 3. ребро → поверхности ---
    edge_to_surfaces = [[] for _ in range(num_edges)]
    for i, edges in enumerate(surface_edges):
        for e in edges:
            edge_to_surfaces[e].append(i)

    # --- 4. строим граф граней по общим рёбрам ---
    neighbors = [[] for _ in range(len(surfaces))]
    for edge_surfs in edge_to_surfaces:
        if len(edge_surfs) == 2:
            a, b = edge_surfs
            neighbors[a].append(b)
            neighbors[b].append(a)

    # --- 5. построение ячеек ---
    cells = set()

    for i in range(len(surfaces)):
        # начальная ячейка
        cell = {i}
        edge_count = [0] * num_edges
        for e in surface_edges[i]:
            edge_count[e] = 1

        # очередь добавления соседей
        queue = [i]
        while queue:
            curr = queue.pop()
            for n in neighbors[curr]:
                if n in cell:
                    continue

                # проверяем, что новые рёбра не превышают 2
                can_add = True
                for e in surface_edges[n]:
                    if edge_count[e] >= 2:
                        can_add = False
                        break
                if not can_add:
                    continue

                # добавляем грань
                cell.add(n)
                queue.append(n)
                for e in surface_edges[n]:
                    edge_count[e] += 1

        # проверяем корректность: должно быть 12 граней и все рёбра используются 0 или 2 раза
        if len(cell) == 12 and all(c in (0, 2) for c in edge_count if c > 0):
            cells.add(tuple(sorted(cell)))

    # --- 6. возвращаем как список списков ---
    return [list(c) for c in cells]