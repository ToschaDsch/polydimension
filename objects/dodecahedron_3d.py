from itertools import combinations

import numpy as np

from geometry import geometry_functions
from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.geometry_functions import get_center_from_list_of_points
from menus.single_functions import mirror_it
from objects.class_draw_interface import NDimensionalObject


class Dodecahedron3d(NDimensionalObject):

    def __init__(self, dimensions: int=4, colorful: bool = False, size: float=1.0,
                 init_point: list[int]=None):
        self._init_points = init_point if init_point else [0, 1, 2]
        super().__init__(dimensions=dimensions, colorful=colorful, size=size)
        self.name_of_the_object = "Dodecahedron 3d"


    def make_points(self):
        a, c = self.size, (1 + 5**.5) * 0.5
        init_coordinate = [[0, c*a, a/c],
                           [c*a, a/c, 0],
                           [a/c, 0, c*a],
                           [a,a,a]]
        for i in range(3):
            init_coordinate = mirror_it(init_coordinate, axis=i)
        for point in init_coordinate:
            point = np.array(point
                             )
            point.resize( (self.dimensions, ))
            self._my_points.append(Point(coordinates=np.array(point)))
        for point in self._my_points:
            point.coord_0[2] +=c*a-a
        self.points_to_show = self._my_points.copy()

    def make_lines(self):
        a, c = self.size, (1 + 5 ** .5) * 0.5
        target_length_sq =  2*a/c #a * a * (5**0.5 - 1)**2

        tolerance = 0.01 * target_length_sq

        for p0, p1 in combinations(self._my_points, 2):
            length_sq = geometry_functions.space_between_two_points(
                point_0=p0,
                point_1=p1)

            if abs(length_sq - target_length_sq) <= tolerance:
                self._my_lines.append(Line(point_0=p0, point_1=p1, width=2))

    def make_surfaces(self):
        number_of_points = []

        # iterate over all 5-line combinations
        for indices in combinations(range(len(self._my_lines)), 5):
            list_of_lines = [self._my_lines[i] for i in indices]

            # collect unique points
            points = {line.point_0 for line in list_of_lines} | {line.point_1 for line in list_of_lines}

            if len(points) == 5:
                result = convex_hull(list(points))
                if result:
                    number_of_points.append(result)

        center = get_center_from_list_of_points(self._my_points)
        for list_of_points_i in number_of_points:
            self._my_surfaces.append(Surface(list_of_points=list_of_points_i, init_center_of_the_volume=center))

    def make_volumes(self):
        pass



def cross(o: Point, a: Point, b: Point, order: str='xy'):
    """Векторное произведение (2D)"""
    if order == 'xy':
        x1, x2 = 0, 1
    else:  # yz
        x1, x2 = 1, 2
    return (a.coord_0[x1] - o.coord_0[x1]) * (b.coord_0[x2] - o.coord_0[x2]) - \
           (a.coord_0[x2] - o.coord_0[x2]) * (b.coord_0[x1] - o.coord_0[x1])



def convex_hull(points: list[Point], order: str = "xy") -> list[Point]:
    """Monotone chain convex hull"""

    if len(points) <= 1:
        return points

    # Используем только x, y
    if order == "xy":
        points = sorted(points, key=lambda p: (p.coord_0[0], p.coord_0[1]))
    else:   #yz
        points = sorted(points, key=lambda p: (p.coord_0[1], p.coord_0[2]))

    EPS = 1e-9

    # Нижняя оболочка
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p, order=order) <= EPS:
            lower.pop()
        lower.append(p)

    # Верхняя оболочка
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p, order=order) <= EPS:
            upper.pop()
        upper.append(p)

    # Объединяем
    result = lower[:-1] + upper[:-1]
    if len(result) == 5:
        return result
    return convex_hull(points=points, order="yz")