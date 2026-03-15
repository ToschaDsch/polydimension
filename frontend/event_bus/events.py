from dataclasses import dataclass

import numpy as np
from PySide6.QtGui import QPen, QBrush, QPolygon

from variables.geometry_var import CoordinatesScreen


class DrawEvent:
    pass

@dataclass
class DrawAllPrimitives(DrawEvent):
    scale: float = None

@dataclass
class RecalculateAndDrawAllPrimitives(DrawEvent):
    angles: np.ndarray = None
    dxi: np.ndarray = None
    scale:float = CoordinatesScreen.scale

@dataclass
class DrawPoint(DrawEvent):
    brush: QBrush
    pen: QPen
    x: int = 0
    y: int = 0
    radius: int = 2


@dataclass
class DrawPointText(DrawEvent):
    x0_y0: list[int]
    text: str


@dataclass
class DrawLine(DrawEvent):
    x1: int
    y1: int
    x2: int
    y2: int
    brush: QBrush
    pen: QPen

@dataclass
class DrawCircle(DrawEvent):
    x: int
    y: int
    r: int
    type_of_line: str = None

@dataclass
class DrawPolygon(DrawEvent):
    polygon: QPolygon
    brush: QBrush
    pen: QPen

@dataclass
class ShiftTheObject(DrawEvent):
    x: int
    y: int

@dataclass
class ClearCanvas:
    pass

@dataclass
class ScaleFactor:
    factor: int # > 0

class DrawRegime:
    pass

@dataclass
class DrawWithPoints(DrawRegime):
    with_points: bool = False

@dataclass
class DrawWithPerspective(DrawRegime):
    with_perspective: bool = True

@dataclass
class DrawWithWeb(DrawRegime):
    with_web: bool = False

@dataclass
class DrawTransparent(DrawRegime):
    transparent: bool = True

@dataclass
class DrawColorful(DrawRegime):
    colorful: bool = True

class EventsForMenuInput:
    pass

@dataclass
class ShiftTheSliderDisplacement(EventsForMenuInput):
    shift: int = 0

@dataclass
class ShiftTheSliderRotation(EventsForMenuInput):
    angle: int = 0