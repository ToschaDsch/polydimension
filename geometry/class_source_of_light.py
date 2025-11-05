from dataclasses import dataclass

from PySide6.QtGui import QColor

from geometry.class_point import Point
from variables.graphics import InitLight


@dataclass
class SourceOfLight:
    coordinate: Point = InitLight.coordinate
    intensity: float = InitLight.intensity
    color: QColor = InitLight.color