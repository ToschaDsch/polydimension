from dataclasses import dataclass

import numpy as np
from PySide6.QtGui import QColor

from geometry.class_point import Point
from variables.graphics import InitLight


@dataclass
class SourceOfLight:
    coordinate: Point = Point(coordinates=np.array(InitLight.coordinate))
    intensity: float = InitLight.intensity
    color: QColor = InitLight.color