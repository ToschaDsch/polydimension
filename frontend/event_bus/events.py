from dataclasses import dataclass

from PySide6.QtGui import QPen, QBrush, QPolygon


class DrawEvent:
    pass

@dataclass
class DrawAllPrimitives(DrawEvent):
    scale: float = None

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
class ClearCanvas:
    pass

@dataclass
class ScaleFactor:
    factor: int # > 0