import functools
import itertools
from abc import ABC, abstractmethod

from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.class_volume import Volume
from variables.geometry_var import CoordinatesScreen
from variables.graphics import Transparency, MyColors


class NDimensionalObject(ABC):
    def __init__(self, size: int = CoordinatesScreen.init_size_of_the_object, line_color: QColor=None, surface_color: QColor=None):
        self.dimensions = 4
        self.my_points: list[Point] = []
        self.my_lines: list[Line] = []
        self.my_surfaces: list[Surface] = []
        self.my_volumes: list[Volume] = []
        self._solid: bool = True
        self._transparent: bool = True
        self.line_color: QColor = line_color if line_color else QColor(*MyColors.default_line_color)
        self.surface_color: QColor = surface_color if surface_color else QColor(*MyColors.default_surface_color)
        self.size: int = size
        self.name_of_the_object: str = "Noname"
        self.make_geometry()
        self.z_min = self.get_z_min()

    def get_z_min(self):
        return functools.reduce(lambda x, y: min(x.coord_0[2] if isinstance(x, Point) else x, y.coord_0[2]), self.my_points, 0)

    @property
    def transparent(self):
        return self._transparent

    @transparent.setter
    def transparent(self, value: bool):
        self._transparent = value
        for surface in self.my_surfaces:
            surface.transparent = value

    def make_geometry(self):
        self.make_points()
        self.make_lines()
        self.make_surfaces()
        self.make_volumes()

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

    @abstractmethod
    def change_color(self, color_is_out: bool=True):
        pass


    def init_geometry(self) -> None:
        pass

    @property
    def solid(self)->bool:
        return self._solid

    @solid.setter
    def solid(self, solid: bool):
        self._solid = solid

    def get_geometric_objects(self, transparency: int = Transparency.transparent) -> list[Line] | list[Surface] | None:
        if not self._solid:
            return self.my_lines
        match transparency:
            case Transparency.full:
                return self.my_surfaces
            case Transparency.sceleton:
                return self.my_lines
            case Transparency.transparent:
                return self.my_surfaces + self.my_lines
            case _:
                print("there is no case for transparency")
                return None


    def __str__(self):
        list_of_points: list[str] = [str(x) for x in self.my_points]
        list_of_lines: list[str] = [str(x) for x in self.my_lines]
        list_of_surfaces: list[str] = [str(x) for x in self.my_surfaces]
        return (f"i'm {self.name_of_the_object}, \n"
                f"I have {self.dimensions} dimensions\n"
                f"my points: {len(list_of_points)} {list_of_points}\n"
                f"my lines: {len(list_of_lines)} {list_of_lines}\n"
                f"my surfaces: {list_of_surfaces}\n"
                f"my volumes: {self.my_volumes}\n")