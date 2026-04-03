from dataclasses import dataclass
from enum import Enum

from PySide6.QtGui import QColor



class Transparency(Enum):
    transparent = 0
    full = 1
    sceleton = 2
    


@dataclass
class GraphicRegimes:
    perspective: bool = True
    web: bool = True
    transparency: int = Transparency.transparent
    color: bool = False
    show_with_points: bool = False


@dataclass
class PenThicknessToDraw:
    boards = 2


@dataclass
class MyColors:
    transparency: int = 50
    color: tuple = (50, 50, 50)
    web: tuple = (40, 0, 255)
    general_screen: tuple[int] = (100, 100, 255)
    default_point_color: tuple = (158, 235, 52)
    default_line_color: tuple = (50, 50, 100)
    default_surface_color: tuple = (200, 100, 100, transparency)
    default_volume_color: tuple = (100, 100, 100)
    normal_line_color: tuple = (0, 255, 0)


default_palette = [(155, 235, 255, MyColors.transparency),
                   (255, 0, 0, MyColors.transparency),
                   (0, 155, 0, MyColors.transparency),
                   (0, 0, 235, MyColors.transparency),
                   (185, 155, 0, MyColors.transparency),
                   (0, 185, 185, MyColors.transparency),
                   (155, 0, 155, MyColors.transparency),
                   (192, 192, 192, MyColors.transparency),
                   (228, 128, 228, MyColors.transparency),
                   (128, 0, 0, MyColors.transparency),
                   (128, 228, 0, MyColors.transparency),
                   (0, 128, 0, MyColors.transparency),
                   (228, 0, 228, MyColors.transparency),
                   (0, 128, 128, MyColors.transparency),
                   (0, 0, 128, MyColors.transparency),
                   (0, 128, 150, MyColors.transparency),
                   (128, 228, 150, MyColors.transparency),
                   (150, 125, 15, MyColors.transparency),
                   (12, 158, 54, MyColors.transparency),
                   (125, 135, 178, MyColors.transparency),
                   (1, 85, 265, MyColors.transparency)]

@dataclass
class InitLight:
    coordinate: tuple[float] = (10.0, 10.0, 100.0)
    intensity: float = 1
    color: QColor = QColor.yellow
