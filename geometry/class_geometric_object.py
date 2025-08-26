from abc import ABC, abstractmethod

from PySide6.QtGui import QColor

from geometry.class_point import Point


class GeometricObject(ABC):

    @abstractmethod
    def get_all_points(self) -> list[Point]:
        pass

    @abstractmethod
    def get_center(self) -> Point:
        pass

    @abstractmethod
    def get_color(self) -> QColor:
        pass
