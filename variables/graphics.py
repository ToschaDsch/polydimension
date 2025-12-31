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
    transparency: int = 100
    color: tuple = (50, 50, 50)
    web: tuple = (40, 0, 255)
    general_screen: tuple[int] = (100, 100, 255)
    default_point_color: tuple = (0, 130, 130)
    default_line_color: tuple = (100, 100, 100)
    default_surface_color: tuple = (200, 100, 100, 100)
    default_volume_color: tuple = (100, 100, 100)


default_palette = [(0, 0, 0, 100),
                   (255, 0, 0, 100),
                   (0, 255, 0, 100),
                   (0, 0, 255, 100),
                   (255, 255, 0, 100),
                   (0, 255, 255, 100),
                   (255, 0, 255, 100),
                   (192, 192, 192, 100),
                   (128, 128, 128, 100),
                   (128, 0, 0, 100),
                   (128, 128, 0, 100),
                   (0, 128, 0, 100),
                   (128, 0, 128, 100),
                   (0, 128, 128, 100),
                   (0, 0, 128, 100)]

@dataclass
class InitLight:
    coordinate: tuple[float] = (10, 25, 50)
    intensity: float = 1
    color: QColor = QColor.yellow
