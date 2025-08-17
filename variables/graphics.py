from dataclasses import dataclass
from enum import Enum
from typing import Any

from PySide6.QtGui import QColor


class Transparency(Enum):
    transparent = 0
    full = 1
    sceleton = 2


@dataclass
class GraphicRegimes:
    perspective: bool = True
    web: bool = True
    transparency: str = Transparency.transparent
    color: bool = False


@dataclass
class PenThicknessToDraw:
    boards = 2


@dataclass
class TypeOfTheObjects:
    dotted = 'dotted'
    axes = 'axes'
    normal = 'normal'
    selected = 'selected'
    line = 'Line'
    light_line = 'LightLine'
    surface = 'Surface'
    temporary_surface = 'temporary_surface'
    light_surface = 'LightSurface'
    light_surface_of_a_combine_beam = "light_surface_of_a_combine_beam"
    text = 'text'
    color = 'color'
    point = 'point'


class ObjectToDraw:
    def __init__(self, self_object: Any, type_of: str = 'normal', color: QColor = QColor(50, 50, 50), text: str = '',
                 type_of_the_objects: str = TypeOfTheObjects.line):
        self.self_object = self_object
        self.type_of: str = type_of
        self.color: QColor = color
        self.text: str = text
        self.type_of_the_objects = type_of_the_objects



@dataclass
class MyColors:
    color: tuple = (50, 50, 50)
    web: tuple = (0, 0, 0)
    general_screen: tuple[int] = (100,100,255)
    carbon: tuple = (0, 130, 130)