import functools
from abc import ABC, abstractmethod

import numpy as np
from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.class_volume import Volume
from variables.geometry_var import CoordinatesScreen
from variables.graphics import Transparency, MyColors, default_palette


class NDimensionalObject(ABC):
    def __init__(self, dimensions: int = 4,
                 size: float = CoordinatesScreen.init_size_of_the_object,
                 line_color: QColor=None, colorful: bool = False):
        self.dimensions = dimensions
        self.draw_with_normal = False            # normal on/ off
        self.points_to_show: list[Point] = []
        self._my_points: list[Point] = []
        self._my_lines: list[Line] = []
        self._my_surfaces: list[Surface] = []
        self._my_volumes: list[Volume] = []
        self._solid: bool = True
        self._transparent: bool = True
        self.line_color: QColor = line_color if line_color else QColor(*MyColors.default_line_color)
        self.size: int = size
        self.name_of_the_object: str = "Noname"
        self.make_geometry()
        self.change_color(colorful=colorful)
        self.z_min = self.get_z_min()
        self._send_normals_from_surfaces()

    def get_surfaces(self) -> list[Surface]:
        return self._my_surfaces

    def get_z_min(self):
        return functools.reduce(lambda x, y: min(x.coord_0[2] if isinstance(x, Point) else x, y.coord_0[2]), self._my_points, 0)

    @property
    def transparent(self):
        return self._transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._transparent = value
        for surface in self._my_surfaces:
            surface.transparent = value

    def make_geometry(self):
        self.make_points()
        self.make_lines()
        self.make_surfaces()
        self.make_volumes()

    def _send_normals_from_surfaces(self):
        for surface in self._my_surfaces:
            if self.draw_with_normal:
                self._my_lines.append(surface.normal_line)
                self._my_points.append(surface.normal_line.point_0)
                self._my_points.append(surface.normal_line.point_1)
            self._my_points.append(surface.normal)
            self._my_points.append(surface.center)

    @abstractmethod
    def make_points(self):
        pass

    @abstractmethod
    def make_lines(self):
        pass

    @abstractmethod
    def make_surfaces(self):
        pass
    @abstractmethod
    def make_volumes(self):
        pass

    def change_color(self, colorful: bool=True):
        if colorful:
            list_of_colors = default_palette
        else:
            list_of_colors = 100*[MyColors.default_surface_color]

        if len(self._my_volumes):
            color_elements = self._my_volumes
        elif len(self._my_surfaces):
            color_elements = self._my_surfaces
        else:
            color_elements = []

        for i, color_element in enumerate(color_elements):
            color_element.color = QColor(*list_of_colors[i])

    def init_geometry(self) -> None:
        pass

    @property
    def solid(self)->bool:
        return self._solid

    @solid.setter
    def solid(self, solid: bool):
        self._solid = solid

    def get_geometric_objects(self, transparency: int = Transparency.transparent) \
            -> list[Line] | list[Surface] | list[Volume] | None:
        if not self._solid:
            return self._my_lines

        objects_with_area = self._my_volumes if len(self._my_volumes) else self._my_surfaces

        match transparency:
            case Transparency.full:
                return objects_with_area
            case Transparency.sceleton:
                return self._my_lines
            case Transparency.transparent:
                return objects_with_area + self._my_lines
            case _:
                print("there is no case for transparency")
                return None


    def __str__(self):
        list_of_points: list[str] = [str(x) for x in self._my_points]
        list_of_lines: list[str] = [str(x) for x in self._my_lines]
        list_of_surfaces: list[str] = [str(x) for x in self._my_surfaces]
        return (f"i'm {self.name_of_the_object}, \n"
                f"I have {self.dimensions} dimensions\n"
                f"my points: {len(list_of_points)} {list_of_points}\n"
                f"my lines: {len(list_of_lines)} {list_of_lines}\n"
                f"my surfaces: {list_of_surfaces}\n"
                f"my volumes: {self._my_volumes}\n")

    def update_lighting_for_all_surfaces(self):
        for surface in self._my_surfaces:
            surface.change_coordinate()

    def _get_a_volume_surfaces_and_points_form_another_object(self, obj) -> Volume:
        """the function get an NDimensionalObject object,
        take all surfaces of it, send all important points to self._my_points"""
        list_of_surfaces = obj.get_surfaces()
        for surface in list_of_surfaces:
            for point_i in surface.list_of_points:
                if point_i in self._my_points:
                    continue
                for point_j in self._my_points:
                    if np.array_equal(point_i.coord_0, point_j.coord_0):
                        index = surface.list_of_points.index(point_i)
                        surface.list_of_points[index] = point_j
                        continue
        return Volume(list_of_points=None, list_of_lines=None, list_of_surfaces=list_of_surfaces)
