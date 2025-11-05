import math
import logging
from dataclasses import dataclass
from typing import List, Tuple, Any

logger = logging.getLogger("myLog")

# Assumed external types:
# - MyPoint (with change_coordinate_and_return_me_all(...) and get2d_coordinate(...))
# - SourceOfLight (lamp.coordinate.getter() and maybe .intensity)
# - ColorAndPath (constructor with color, visible, distance, path)
# - Properties (attributes: how_dimension_we_have, current_draw_axis_indexes,
#               draw_with_perspective, DISPERSION_OF_LIGHT)
# - Color (constructor Color(r, g, b) or similar, with attributes .red, .green, .blue)
# - Offset (callable Offset(x, y) or replaceable by tuple)
Offset = Any


class MySurface:
    def __init__(self, vertices: List["MyPoint"], surface_color: "Color", lamp: "SourceOfLight"):
        self.vertices: List["MyPoint"] = vertices
        self.surface_color: "Color" = surface_color
        self.lamp: "SourceOfLight" = lamp

        # match Kotlin: Array(vertices.size) { Array(howDimensionWeHave) {0f} }
        h = Properties.how_dimension_we_have
        n = len(vertices)
        self.current_coordinates: List[List[float]] = [[0.0 for _ in range(h)] for _ in range(n)]
        # Array<FloatArray> = Array(vertices.size) { floatArrayOf(0f, 0f) }
        self.current_coordinates_2d: List[List[float]] = [[0.0, 0.0] for _ in range(n)]
        # MutableList<Offset> = MutableList(vertices.size) { Offset(0f, 0f) }
        offsets: List[Offset] = []
        for _ in range(n):
            try:
                offsets.append(Offset(0.0, 0.0))  # type: ignore[call-arg]
            except Exception:
                offsets.append((0.0, 0.0))
        self.current_coordinates_offset: List[Offset] = offsets
        # vectorCenter = Array(howDimensionWeHave) {0f}
        self.vector_center: List[float] = [0.0 for _ in range(h)]

    # -------------------------
    # private fun changeCoordinate(...)
    # -------------------------
    def change_coordinate(
        self,
        dx: List[float],                 # displacement matrix
        df: List[List[float]],           # angle matrix
        dimension_matrix: List[List[int]]  # list of all possible flats to rotate
    ) -> List[List[float]]:
        """
        The function moves and rotates coordinates
        """
        for index, point in enumerate(self.vertices):
            self.current_coordinates[index] = point.change_coordinate_and_return_me_all(
                dx=dx,
                df=df,
                dimension_matrix=dimension_matrix
            )
        return self.current_coordinates

    # -------------------------
    # private fun changeCoordinate2D(...)
    # -------------------------
    def change_coordinate_2d(
        self,
        old_coordinates: List[List[float]],
        dx: List[float]  # displacement matrix
    ) -> List[List[float]]:
        for index, point in enumerate(old_coordinates):
            # use Properties.current_draw_axis_indexes (snake_case)
            axes = Properties.current_draw_axis_indexes
            self.current_coordinates_2d[index] = MyPoint.get2d_coordinate(
                point[axes[0]],
                point[axes[1]],
                point[axes[2]],
                dx
            )
        return self.current_coordinates_2d

    # -------------------------
    # fun changeCoordinatesAndGiveMeColorsAndPaths(...)
    # -------------------------
    def change_coordinates_and_give_me_colors_and_paths(
        self,
        dx: List[float],                 # displacement matrix
        df: List[List[float]],           # angle matrix
        dimension_matrix: List[List[int]],  # list of all possible flats to rotate
        center: List[float],
        color: "Color" = None
    ) -> "ColorAndPath":
        if color is None:
            color = self.surface_color

        coordinate_all = self.change_coordinate(dx=dx, df=df, dimension_matrix=dimension_matrix)

        item_return_color = self.give_me_the_color(coordinate_all, center, color)
        coordinate_2d = self.change_coordinate_2d(coordinate_all, dx)
        list_of_paths = self.give_me_paths_for_the_line(coordinate_2d)

        return ColorAndPath(
            color=item_return_color.color,
            visible=item_return_color.i_see_it,
            distance=item_return_color.distance,
            path=list_of_paths
        )  # color and coordinates

    # -------------------------
    # fun changeCoordinatesAndGiveMeColorsAndPathsWithNumbers(...)
    # -------------------------
    def change_coordinates_and_give_me_colors_and_paths_with_numbers(
        self,
        coordinate_all: List[List[float]],
        center: List[float],
        coordinate_2d: List[List[float]],
        color: "Color" = None
    ) -> "ColorAndPath":
        if color is None:
            # Kotlin default was Color.Red; keep provided default behavior minimal here
            color = self.surface_color

        item_return_color = self.give_me_the_color(coordinate_all, center, color)
        list_of_paths = self.give_me_paths_for_the_line(coordinate_2d)

        return ColorAndPath(
            color=item_return_color.color,
            visible=item_return_color.i_see_it,
            distance=item_return_color.distance,
            path=list_of_paths
        )  # color and coordinates

    # -------------------------
    # private fun giveMePathsForTheLine(...)
    # -------------------------
    def give_me_paths_for_the_line(self, list_of_points: List[List[float]]) -> List[Offset]:
        """The function takes a list of 2d coordinates and returns an Offset"""
        for index, point in enumerate(list_of_points):
            # mirror Kotlin: currentCoordinatesOffset[index] = Offset(point[0], point[1])
            try:
                self.current_coordinates_offset[index] = Offset(point[0], point[1])  # type: ignore[call-arg]
            except Exception:
                self.current_coordinates_offset[index] = (point[0], point[1])
        return self.current_coordinates_offset

    # -------------------------
    # private fun giveMeTheColor(...)
    # -------------------------
    def give_me_the_color(
        self,
        coordinate_all: List[List[float]],
        center: List[float],
        color: "Color" = None
    ) -> "ReturnColor":
        if color is None:
            color = self.surface_color

        vector_of_distance, square_of_distance = self.calculate_vector_and_square_of_distance(coordinate_all)

        # distance3d: Float = 0f in Kotlin (sqrt commented)
        distance3d: float = 0.0

        for i in range(Properties.how_dimension_we_have):
            self.vector_center[i] = vector_of_distance[i] - center[i]

        normal = self.calculate_normal(coordinate_all, self.vector_center)

        vector_from_lamp, distance_from_lamp = self.calculate_lamp(vector_of_distance)

        # if (distanceFromLamp > lamp.intensity) { // in dark } -- original commented out

        if Properties.draw_with_perspective:
            vector_of_distance = MySurface.normalize_me_in_3d(vector_of_distance)
        else:
            vector_of_distance = [0.0, 1.0, 0.0]

        i_see_it = MySurface.cos_between_two_vectors(normal, vector_of_distance) < 0.0

        vector_from_lamp = MySurface.normalize_me_in_3d(vector_from_lamp)

        angle = MySurface.cos_between_two_vectors(normal, vector_from_lamp)
        new_color = self.make_color(angle, distance3d, color)
        return ReturnColor(new_color, i_see_it, square_of_distance)

    # Kotlin data class ReturnColor(...)
    @dataclass
    class ReturnColor:
        color: "Color"
        i_see_it: bool
        distance: float

    # -------------------------
    # private fun makeColor(...)
    # -------------------------
    def make_color(self, angle0: float, distance: float, color: "Color" = None) -> "Color":
        if color is None:
            color = self.surface_color

        # val add = (1f - Properties.DISPERSION_OF_LIGHT) + abs(angle0) * Properties.DISPERSION_OF_LIGHT
        add = (1.0 - Properties.DISPERSION_OF_LIGHT) + abs(angle0) * Properties.DISPERSION_OF_LIGHT

        if (add > 0.0) and (add < 1.0):
            # return Color(color.red * add, color.green * add, color.blue * add)
            return Color(color.red * add, color.green * add, color.blue * add)
        else:
            return self.surface_color

    # -------------------------
    # private fun calculateLamp(...)
    # -------------------------
    def calculate_lamp(self, vector_of_distance: List[float]) -> Tuple[List[float], float]:
        """
        the function returns not normalized vector of lamp - the point
        and the distance between
        """
        lamp_coord = self.lamp.coordinate.getter()
        vector_from_lamp = [
            lamp_coord[0] - vector_of_distance[0],
            lamp_coord[1] - vector_of_distance[1],
            lamp_coord[2] - vector_of_distance[2],
        ]
        # Kotlin had sqrt(...) commented out and set distanceFromLamp = 1f
        distance_from_lamp = 1.0
        return vector_from_lamp, distance_from_lamp

    # -------------------------
    # companion object equivalents
    # -------------------------
    @staticmethod
    def normalize_me_in_3d(vector: List[float], distance0: float = 0.0) -> List[float]:
        """
        the function normalizes a vector in 3d dimension
        """
        if distance0 == 0.0:
            s = 0.0
            for i in range(3):
                s += vector[i] * vector[i]
            distance = math.pow(s, 0.5)
        else:
            distance = distance0

        a = 1.0 if distance == 0.0 else 1.0 / distance

        return [vector[0] * a, vector[1] * a, vector[2] * a]

    @staticmethod
    def cos_between_two_vectors(normal: List[float], vector_of_distance: List[float]) -> float:
        """the function returns 3d scalar product"""
        return (
            normal[0] * vector_of_distance[0]
            + normal[1] * vector_of_distance[1]
            + normal[2] * vector_of_distance[2]
        )

    @staticmethod
    def calculate_vector_and_square_of_distance(coordinate_all: List[List[float]]) -> Tuple[List[float], float]:
        """
        the function calculates a vector to the center of the surface and average square of distance to the surface
        """
        h = Properties.how_dimension_we_have
        vector_distance: List[float] = [0.0 for _ in range(h)]
        square_of_length = 0.0
        a = 1.0 / len(coordinate_all)

        for i in range(h):
            for point in coordinate_all:
                vector_distance[i] += point[i] * a  # x
            square_of_length += vector_distance[i] * vector_distance[i]
        return vector_distance, square_of_length

    @staticmethod
    def vector_product_with_center(v1: List[float], v2: List[float], vector_center: List[float]) -> List[float]:
        """
        the function checks where is the center and returns normal of the surface
        """
        vector_product = MySurface.vector_product(v1, v2)
        if MySurface.cos_between_two_vectors(vector_product, vector_center) > 0.0:
            return vector_product
        else:
            return MySurface.vector_product(v2, v1)

    @staticmethod
    def vector_product(v1: List[float], v2: List[float]) -> List[float]:
        """the function returns vector product"""
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
        ]

    # -------------------------
    # private fun calculateNormal(...)
    # -------------------------
    def calculate_normal(self, coordinate_all: List[List[float]], vector_center: List[float]) -> List[float]:
        """
        the function takes coordinate of surfaces edge and calculate normal to the surface
        """
        h = Properties.how_dimension_we_have
        v1: List[float] = [0.0 for _ in range(h)]
        v2: List[float] = [0.0 for _ in range(h)]
        for i in range(3):
            v1[i] = coordinate_all[1][i] - coordinate_all[0][i]  # dx //vector v1 (point 1 - point 0)
            v2[i] = coordinate_all[2][i] - coordinate_all[1][i]  # dx //vector v2 (point 2 - point 1)

        normal = MySurface.vector_product_with_center(v1, v2, vector_center)

        length = math.sqrt(
            normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2]
        )

        a = 1.0 / length if length != 0.0 else 1.0
        return [normal[0] * a, normal[1] * a, normal[2] * a]
