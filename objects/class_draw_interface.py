from abc import ABC, abstractmethod

from PySide6.QtGui import QColor

from geometry.class_line import Line
from geometry.class_point import Point
from geometry.class_surface import Surface
from geometry.class_volume import Volume
from variables.geometry_var import CoordinatesScreen


class DrawObject(ABC):
    def __init__(self, size: int = CoordinatesScreen.init_size_of_the_object):
        self.dimensions = 4
        self.my_points: list[Point] = []
        self.my_lines: list[Line] = []
        self.my_surfaces: list[Surface] = []
        self.my_volumes: list[Volume] = []
        self._solid: bool = True
        self.transparent: bool = True
        self.color_of_lines: QColor = QColor(0,0,0)
        self.size: int = size
        self.name_of_the_object: str = "Noname"
        self.make_geometry()

    def make_geometry(self):
        self.make_points()
        self.make_lines()
        self.make_surfaces()
        self.make_volumes()

    @abstractmethod
    def make_points(self):
        pass
    def make_lines(self):
        pass
    def make_surfaces(self):
        pass
    @abstractmethod
    def make_volumes(self):
        pass

    def get_the_objects(self):
        if self.solid:
            return self.my_volumes
        else:
            return self.my_lines

    def init_geometry(self) -> None:
        pass

    @property
    def solid(self)->bool:
        return self._solid

    @solid.setter
    def solid(self, solid: bool):
        self._solid = solid


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